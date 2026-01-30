# Concepts + Synchronizations Architecture Pattern

> **Project Context:** This document describes the Concepts + Synchronizations pattern (Jackson & Meng, MIT CSAIL, 2025), which serves as the **implementation architecture for the Integral Ethics Engine (IEE)**. No-Saviors §14 specifies that the IEE "runs entirely in browser" using this pattern: worldviews are modeled as Concepts (singletons with pure functions), and ethical deliberation procedures are modeled as Synchronizations (event-driven workflows coordinating multiple worldview evaluations). The edge computing / IndexedDB / PWA patterns described below directly support the IEE's client-side deployment model.
>
> **Status:** This document currently describes the generic pattern only. IEE-specific content (worldview concepts, integration synchronizations, deadlock protocol, veto mechanism, BFO/CCO connection) needs to be added. See ARIADNE finding F-A03-1.

This document describes the **Concepts + Synchronizations** pattern from MIT CSAIL, a modular architecture optimized for agentic development and AI-agent collaboration.

## Overview

The architecture separates concerns into two primary layers:

1. **Concepts**: Independent modules representing domain entities or capabilities
2. **Synchronizations**: Workflows that coordinate multiple concepts

This separation creates a highly modular, testable, and legible codebase that AI agents can easily understand and modify.

## Core Principles

### 0. Edge Computing & User-Owned Data

Modern applications should prioritize user autonomy and offline-first architecture:

**Edge Computing**: Process and store data at the edge (user's device) rather than relying on centralized servers. This provides:
- **Better Performance**: No network latency for most operations
- **Improved Privacy**: User data stays on their device
- **Offline Capability**: App works without internet connection
- **Reduced Costs**: Less server infrastructure needed
- **User Ownership**: Users control their own data

**Implementation**:
```javascript
// storageConcept.js - User-owned data with IndexedDB
export const storageConcept = {
  state: {
    db: null,
    isOpen: false,
    pendingSyncs: []  // Queue for when back online
  },

  actions: {
    async init() {
      // Open local database on user's device
      const db = await indexedDB.open('user-data', 1);
      storageConcept.state.db = db;
      storageConcept.state.isOpen = true;
    },

    async create(storeName, data) {
      // Store locally first (edge computing)
      const record = await localStore.add(data);

      // Queue for server sync if needed
      if (data.syncToServer) {
        await storageConcept.actions.queueSync('create', record);
      }

      return record;
    },

    async processSyncQueue() {
      // Sync queued operations when online
      for (const item of storageConcept.state.pendingSyncs) {
        await syncToServer(item);
      }
    }
  }
};
```

**Key Principles**:
- **Offline-First**: All CRUD operations work offline via IndexedDB
- **Eventual Consistency**: Sync to server when online, but app works offline
- **User Control**: Data stored locally, user can export/delete anytime
- **No Lock-In**: App functions independently of backend services

### 1. Concepts Are Singletons

Each concept is a singleton object with explicit state management:

```javascript
export const userConcept = {
  state: {
    currentUser: null,
    isAuthenticated: false
  },

  actions: {
    login(credentials) { /* ... */ },
    logout() { /* ... */ }
  },

  _subscribers: [],
  notify(event, payload) { /* ... */ },
  subscribe(fn) { /* ... */ }
};
```

**Why Singletons?**
- Predictable state location
- Easy to test (reset state in beforeEach)
- No dependency injection complexity
- Clear ownership of data

### 2. Pure Functions for Business Logic

Actions contain pure, testable business logic:

```javascript
actions: {
  calculateTotal(items) {
    // Pure function - same inputs always produce same outputs
    return items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

**Benefits:**
- Deterministic behavior
- Easy to test
- No hidden dependencies
- AI agents can reason about behavior

### 3. Event-Driven Communication

Concepts communicate via events, not direct calls:

```javascript
// Concept A publishes event
userConcept.notify('userLoggedIn', { userId: 123 });

// Concept B subscribes to event
userConcept.subscribe((event, payload) => {
  if (event === 'userLoggedIn') {
    analyticsConcept.actions.trackLogin(payload.userId);
  }
});
```

**Why Events?**
- Loose coupling between concepts
- Easy to add new reactions
- Clear data flow
- Testable in isolation

### 4. State Isolation

Each test runs in a fresh process with clean state:

```javascript
describe('User Concept', () => {
  beforeEach(() => {
    // THE GOLDEN RULE: Reset state before each test
    userConcept.state.currentUser = null;
    userConcept.state.isAuthenticated = false;
  });

  test('login sets authenticated state', () => {
    userConcept.actions.login({ email: 'test@test.com' });
    assert.strictEqual(userConcept.state.isAuthenticated, true);
  });
});
```

**Why Process Isolation?**
- No test cross-contamination
- Guaranteed clean slate
- Fast, parallel execution
- Easy to debug failures

## Anatomy of a Concept

### Complete Concept Template

```javascript
export const exampleConcept = {
  /**
   * State - All mutable data
   * Reset this in test beforeEach hooks
   */
  state: {
    data: null,
    isLoading: false,
    error: null
  },

  /**
   * Actions - Pure business logic
   */
  actions: {
    async fetchData() {
      const self = exampleConcept;
      self.state.isLoading = true;
      self.notify('loadingStarted');

      try {
        const data = await api.fetch();
        self.state.data = data;
        self.state.isLoading = false;
        self.notify('dataLoaded', { data });
        return data;
      } catch (error) {
        self.state.error = error.message;
        self.state.isLoading = false;
        self.notify('loadingFailed', { error });
        throw error;
      }
    },

    reset() {
      const self = exampleConcept;
      self.state.data = null;
      self.state.isLoading = false;
      self.state.error = null;
      self.notify('reset');
    }
  },

  /**
   * Event System
   */
  _subscribers: [],

  notify(event, payload = {}) {
    this._subscribers.forEach(fn => fn(event, payload));
  },

  subscribe(fn) {
    this._subscribers.push(fn);
  },

  unsubscribe(fn) {
    this._subscribers = this._subscribers.filter(sub => sub !== fn);
  }
};
```

## Synchronizations

Synchronizations coordinate multiple concepts to implement complex workflows:

```javascript
// src/synchronizations.js

import { userConcept } from './concepts/userConcept.js';
import { analyticsConcept } from './concepts/analyticsConcept.js';
import { storageConcept } from './concepts/storageConcept.js';

/**
 * Login Synchronization
 * Coordinates user login across multiple concepts
 */
export async function loginSync(credentials) {
  // 1. Authenticate user
  const user = await userConcept.actions.login(credentials);

  // 2. Track login event
  await analyticsConcept.actions.track('login', {
    userId: user.id,
    timestamp: Date.now()
  });

  // 3. Load user preferences
  const preferences = await storageConcept.actions.get(`user:${user.id}:prefs`);

  return { user, preferences };
}
```

**Synchronization Principles:**
- Orchestrate concepts, don't contain business logic
- Handle errors and rollback if needed
- Keep thin - complex logic belongs in concepts
- Test by mocking concept actions

## Testing Strategy

### Unit Testing Concepts

Test concepts in complete isolation:

```javascript
describe('User Concept', () => {
  beforeEach(() => {
    userConcept.state.currentUser = null;
  });

  test('login updates state', () => {
    userConcept.actions.login({ email: 'test@test.com' });
    assert.ok(userConcept.state.currentUser);
  });
});
```

### Testing Synchronizations

Mock concept actions to test coordination logic:

```javascript
describe('Login Synchronization', () => {
  beforeEach(() => {
    // Mock concept actions
    userConcept.actions.login = async () => ({ id: 1, email: 'test@test.com' });
    analyticsConcept.actions.track = async () => {};
  });

  test('coordinates login workflow', async () => {
    const result = await loginSync({ email: 'test@test.com' });
    assert.ok(result.user);
  });
});
```

### UI Testing

Test complete user workflows:

```javascript
test('user can complete login flow', async () => {
  await browser.launch();
  await browser.navigate('/login');
  await browser.type('#email', 'test@test.com');
  await browser.type('#password', 'password123');
  await browser.click('#submit');
  await browser.waitForSelector('#dashboard');
  await browser.close();
});
```

## Benefits for Agentic Development

### 1. Clear Module Boundaries

AI agents can easily identify:
- What each concept is responsible for
- How concepts interact
- Where to add new features
- What to test when making changes

### 2. Testable by Design

Every concept can be tested in isolation:
- No complex setup required
- Fast feedback loop
- Easy to verify correctness
- Safe refactoring

### 3. Event-Driven Debugging

Structured event logging helps agents:
- Trace execution flow
- Diagnose failures
- Understand state changes
- Generate better solutions

### 4. Composable Architecture

New features compose existing concepts:
- No need to modify existing code
- Extend via event subscriptions
- Add synchronizations as needed
- Minimal risk of regression

## PWA & Edge Computing Patterns

### Pattern: IndexedDB CRUD Operations

```javascript
// storageConcept.js
actions: {
  async create(storeName, data) {
    const self = storageConcept;

    // Add metadata
    const record = {
      ...data,
      timestamp: Date.now(),
      createdAt: new Date().toISOString(),
      synced: false
    };

    // Store in IndexedDB
    const id = await new Promise((resolve, reject) => {
      const tx = self.state.db.transaction([storeName], 'readwrite');
      const store = tx.objectStore(storeName);
      const request = store.add(record);

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    record.id = id;
    self.notify('recordCreated', { storeName, record });

    // Queue for sync if online
    if (navigator.onLine && data.syncToServer) {
      await self.actions.queueSync('create', storeName, record);
    }

    return record;
  },

  async read(storeName, id) {
    const self = storageConcept;

    return await new Promise((resolve, reject) => {
      const tx = self.state.db.transaction([storeName], 'readonly');
      const store = tx.objectStore(storeName);
      const request = store.get(id);

      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
    });
  },

  async update(storeName, id, updates) {
    const self = storageConcept;
    const existing = await self.actions.read(storeName, id);

    const updated = {
      ...existing,
      ...updates,
      id,
      updatedAt: new Date().toISOString(),
      synced: false
    };

    await new Promise((resolve, reject) => {
      const tx = self.state.db.transaction([storeName], 'readwrite');
      const store = tx.objectStore(storeName);
      const request = store.put(updated);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    self.notify('recordUpdated', { storeName, id, updates });
    return updated;
  }
}
```

### Pattern: Offline Queue with Background Sync

```javascript
// Queue operations when offline, sync when back online
actions: {
  async queueSync(operation, storeName, data) {
    const self = storageConcept;

    const queueItem = {
      operation,
      storeName,
      data,
      timestamp: Date.now(),
      status: 'pending',
      retries: 0
    };

    // Store in sync queue
    const queueId = await new Promise((resolve, reject) => {
      const tx = self.state.db.transaction(['syncQueue'], 'readwrite');
      const store = tx.objectStore('syncQueue');
      const request = store.add(queueItem);

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    self.state.pendingSyncs.push(queueItem);
    self.notify('syncQueued', { queueId, operation });

    return queueId;
  },

  async processSyncQueue() {
    const self = storageConcept;

    // Get all pending syncs
    const queue = await self.actions.readAll('syncQueue', {
      filter: item => item.status === 'pending'
    });

    for (const item of queue) {
      try {
        // Make API call to sync with server
        await fetch('/api/sync', {
          method: 'POST',
          body: JSON.stringify(item)
        });

        // Mark as synced
        await self.actions.update('syncQueue', item.queueId, {
          status: 'synced',
          syncedAt: new Date().toISOString()
        });

        // Update original record
        if (item.data.id) {
          await self.actions.update(item.storeName, item.data.id, {
            synced: true
          });
        }
      } catch (error) {
        // Increment retry count
        await self.actions.update('syncQueue', item.queueId, {
          retries: item.retries + 1,
          lastError: error.message
        });
      }
    }

    self.notify('syncQueueProcessed', { processed: queue.length });
  }
}

// Listen for online events
window.addEventListener('online', () => {
  storageConcept.actions.processSyncQueue();
});
```

### Pattern: Service Worker Integration

```javascript
// service-worker.js
const CACHE_VERSION = 'v1';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;

// Cache-first strategy for static assets
async function cacheFirstStrategy(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(DYNAMIC_CACHE);
    cache.put(request, response.clone());
  }

  return response;
}

// Network-first strategy for API calls
async function networkFirstStrategy(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Fall back to cache when offline
    const cached = await caches.match(request);
    if (cached) return cached;

    throw error;
  }
}

// Handle fetch events
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstStrategy(request));
  } else {
    event.respondWith(cacheFirstStrategy(request));
  }
});

// Background sync
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-operations') {
    event.waitUntil(syncQueuedOperations());
  }
});
```

### Pattern: Progressive Enhancement

Build features that work offline and enhance when online:

```javascript
// Feature detection
export const capabilitiesConcept = {
  state: {
    hasIndexedDB: false,
    hasServiceWorker: false,
    isOnline: navigator.onLine
  },

  actions: {
    detect() {
      const self = capabilitiesConcept;

      self.state.hasIndexedDB = 'indexedDB' in window;
      self.state.hasServiceWorker = 'serviceWorker' in navigator;

      // Listen for online/offline
      window.addEventListener('online', () => {
        self.state.isOnline = true;
        self.notify('online');
      });

      window.addEventListener('offline', () => {
        self.state.isOnline = false;
        self.notify('offline');
      });
    },

    async enableOfflineMode() {
      const self = capabilitiesConcept;

      if (self.state.hasServiceWorker) {
        await navigator.serviceWorker.register('/service-worker.js');
      }

      if (self.state.hasIndexedDB) {
        await storageConcept.actions.init();
      }

      self.notify('offlineModeEnabled');
    }
  }
};
```

### Pattern: User Data Export

Give users control over their data:

```javascript
actions: {
  async exportAllData() {
    const self = storageConcept;

    const allStores = Array.from(self.state.db.objectStoreNames);
    const exportData = {};

    for (const storeName of allStores) {
      exportData[storeName] = await self.actions.readAll(storeName);
    }

    // Create downloadable JSON file
    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json'
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `user-data-${Date.now()}.json`;
    a.click();

    URL.revokeObjectURL(url);
    self.notify('dataExported');
  },

  async deleteAllData() {
    const self = storageConcept;

    const allStores = Array.from(self.state.db.objectStoreNames);

    for (const storeName of allStores) {
      await self.actions.clear(storeName);
    }

    self.notify('allDataDeleted');
  }
}
```

## Common Patterns

### Pattern: Loading States

```javascript
actions: {
  async fetchData() {
    const self = thisConcept;

    self.state.isLoading = true;
    self.state.error = null;
    self.notify('loadingStarted');

    try {
      const data = await api.fetch();
      self.state.data = data;
      self.state.isLoading = false;
      self.notify('dataLoaded', { data });
      return data;
    } catch (error) {
      self.state.error = error.message;
      self.state.isLoading = false;
      self.notify('loadingFailed', { error });
      throw error;
    }
  }
}
```

### Pattern: Optimistic Updates

```javascript
actions: {
  async updateItem(id, changes) {
    const self = thisConcept;
    const oldItem = self.state.items.find(i => i.id === id);

    // Optimistic update
    self.state.items = self.state.items.map(item =>
      item.id === id ? { ...item, ...changes } : item
    );
    self.notify('itemUpdated', { id, changes });

    try {
      await api.update(id, changes);
    } catch (error) {
      // Rollback on error
      self.state.items = self.state.items.map(item =>
        item.id === id ? oldItem : item
      );
      self.notify('updateFailed', { id, error });
      throw error;
    }
  }
}
```

### Pattern: Derived State

```javascript
actions: {
  getActiveUsers() {
    const self = userConcept;
    return self.state.users.filter(u => u.isActive);
  },

  getUserCount() {
    const self = userConcept;
    return self.state.users.length;
  }
}
```

## Anti-Patterns to Avoid

### ❌ Concepts Directly Calling Other Concepts

```javascript
// BAD: Direct coupling
userConcept.actions.login = () => {
  analyticsConcept.actions.track('login');  // ❌ Direct call
};
```

```javascript
// GOOD: Use events
userConcept.actions.login = () => {
  userConcept.notify('userLoggedIn');  // ✅ Event
};

userConcept.subscribe((event) => {
  if (event === 'userLoggedIn') {
    analyticsConcept.actions.track('login');
  }
});
```

### ❌ Business Logic in Synchronizations

```javascript
// BAD: Logic in synchronization
export function loginSync(credentials) {
  const hashedPassword = hashPassword(credentials.password);  // ❌ Logic here
  return userConcept.actions.login({ ...credentials, password: hashedPassword });
}
```

```javascript
// GOOD: Logic in concept
userConcept.actions.login = (credentials) => {
  const hashedPassword = hashPassword(credentials.password);  // ✅ Logic in concept
  // ... authenticate
};
```

### ❌ Shared Mutable State

```javascript
// BAD: Sharing state reference
const sharedArray = [];
concept1.state.items = sharedArray;  // ❌
concept2.state.items = sharedArray;  // ❌
```

```javascript
// GOOD: Each concept owns its state
concept1.state.items = [];  // ✅
concept2.state.items = [];  // ✅
```

## Migration Guide

### Converting Existing Code

1. **Identify Domain Entities** → Become Concepts
2. **Extract Business Logic** → Move to Concept Actions
3. **Replace Direct Calls** → Use Events
4. **Add State Management** → Explicit State Objects
5. **Write Tests** → One Test File Per Concept

### Example Migration

**Before:**
```javascript
class UserManager {
  constructor(analytics) {
    this.analytics = analytics;
    this.currentUser = null;
  }

  login(credentials) {
    this.currentUser = authenticate(credentials);
    this.analytics.track('login');
  }
}
```

**After:**
```javascript
export const userConcept = {
  state: { currentUser: null },

  actions: {
    login(credentials) {
      const self = userConcept;
      self.state.currentUser = authenticate(credentials);
      self.notify('userLoggedIn');
    }
  },

  _subscribers: [],
  notify(event, payload) { /* ... */ },
  subscribe(fn) { /* ... */ }
};

// In analytics concept
userConcept.subscribe((event) => {
  if (event === 'userLoggedIn') {
    analyticsConcept.actions.track('login');
  }
});
```

## PWA Best Practices

### 1. Always Work Offline First

Design features to work locally first, then sync:

```javascript
// BAD: Requires network
async function saveNote(note) {
  await fetch('/api/notes', { method: 'POST', body: JSON.stringify(note) });
}

// GOOD: Works offline, syncs later
async function saveNote(note) {
  // Save locally first
  const saved = await storageConcept.actions.create('notes', note);

  // Queue for sync when online
  if (navigator.onLine) {
    await storageConcept.actions.queueSync('create', 'notes', saved);
  }

  return saved;
}
```

### 2. Provide Clear Offline Indicators

Let users know when they're offline:

```javascript
// Monitor and display connection status
window.addEventListener('online', () => {
  uiConcept.actions.showBanner('Back online - syncing...', 'success');
  storageConcept.actions.processSyncQueue();
});

window.addEventListener('offline', () => {
  uiConcept.actions.showBanner('Offline mode - changes saved locally', 'info');
});
```

### 3. Handle Conflicts Gracefully

When syncing, conflicts may occur:

```javascript
async function syncRecord(localRecord) {
  try {
    const response = await fetch(`/api/records/${localRecord.id}`);
    const serverRecord = await response.json();

    // Check for conflicts
    if (serverRecord.updatedAt > localRecord.updatedAt) {
      // Server version is newer
      return await resolveConflict(localRecord, serverRecord);
    }

    // Local version wins, sync to server
    await fetch(`/api/records/${localRecord.id}`, {
      method: 'PUT',
      body: JSON.stringify(localRecord)
    });
  } catch (error) {
    console.error('Sync failed:', error);
  }
}
```

### 4. Implement Data Quotas

IndexedDB has storage limits - monitor usage:

```javascript
actions: {
  async checkStorageQuota() {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
      const { usage, quota } = await navigator.storage.estimate();
      const percentUsed = (usage / quota) * 100;

      if (percentUsed > 80) {
        // Warn user
        uiConcept.actions.showWarning(
          `Storage ${percentUsed.toFixed(0)}% full. Consider exporting old data.`
        );
      }

      return { usage, quota, percentUsed };
    }
  }
}
```

### 5. Test Offline Scenarios

Always test your app offline:

```javascript
// ui-test-framework/tests/offline.test.js
test('app works offline', async () => {
  await browserConcept.actions.launch({ headless: true });

  // Go offline
  await browserConcept.actions.sendCDPCommand('Network.enable');
  await browserConcept.actions.sendCDPCommand('Network.emulateNetworkConditions', {
    offline: true,
    downloadThroughput: 0,
    uploadThroughput: 0,
    latency: 0
  });

  // Test offline functionality
  const result = await browserConcept.actions.evaluate(() => {
    return storageConcept.actions.create('data', { test: true });
  });

  assert.ok(result.id, 'Should create record offline');
});
```

## Further Reading

- [MIT CSAIL Concepts Research](https://essenceofsoftware.com/)
- [Test Strategy](../testStrategy.md)
- [Agentic Development Guide](../agenticDevlopment.md)
- [PWA Guide](../TEMPLATE_README.md#-pwa-progressive-web-app)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)

---

**Remember:** Concepts are independent, composable, and testable. Keep them small, focused, and event-driven for maximum modularity and agentic compatibility. Prioritize user ownership of data through edge computing and offline-first design.
