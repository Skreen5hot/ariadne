SPW-PUB — semantic-publication Integration Profile v0.1
Nov 11, 2026 · @Aaron Damiano
semantic-publication is its own product: it takes an RDF release bundle in, projects it into a property graph, and serves it as static JSON to an in-browser explorer. It depends on the pipeline's output, never on the pipeline.
Field
Value
Document ID
SPW-PUB
Repository
semantic-publication
Version
0.1 (draft)
Status
Proposed profile — not ratified
Normative specification
SDD-PUB-ARCH v0.4.4 draft.2
Companion
SPW-ARCH v0.3 (semantic-pipeline)
1. Scope and authority
SDD-PUB-ARCH is the specification of the semantic-publication repository. This profile restates none of it. It records only what the split into two repositories adds:
1.  the input contract: the RDF release bundle, and RDF from other producers (§2);
2.  provenance tiers for those producers (§3);
3.  the delivery target: a static-JSON explorer in the browser (§4);
4.  the half of the traceability chain that now lives here, and the witnesses moved from SPW-ARCH (§5).
Where this profile and PUB-ARCH disagree, PUB-ARCH governs and the disagreement is a request to PUB-ARCH (§5.4). PUB-ARCH's three tiers stay as written (P-10): the authoritative RDF dataset; the Object Projection, a deterministic transformation into a consumer-oriented property graph that keeps identity, relationships and statement-level evidence; and the presentation, which explains without asserting.
Not in this repository: ingestion, structure, semantic mapping, RDF projection (all semantic-pipeline); live API acquisition (semantic-pipeline CI).
2. Input: the RDF release bundle
The primary input is the RDF release bundle defined in SPW-ARCH §2.6. semantic-publication pins the bundleVersion values it accepts; semantic-pipeline owns the contract and announces changes through the communications/ protocol.
Accepting a bundle is a handoff. Building a release from a bundle is an acceptance by a named person or an authorized policy, recorded in PUB-ARCH's own release record. Acceptance does not waive integrity.
On intake, the build runner MUST, in order:
1.  validate bundle.jsonld against the pinned bundle descriptor schema;
2.  verify the sha256 of every listed file, and refuse the bundle on any mismatch;
3.  check that the Ontology-Template commit and term-list digest in the descriptor match the ontology closure this release builds against, and refuse or flag per PUB-ARCH's compatibility rules;
4.  read loss.json into PUB-ARCH's loss model (§9.6) so declared losses appear on entries;
5.  assign the bundle's provenance tier (§3) and carry it into every statement's evidence.
A refused bundle produces a diagnostic naming the failed step and the file. Nothing from it is published.
Other RDF inputs. A producer other than semantic-pipeline MAY supply a bundle with its own descriptor, or bare RDF (N-Quads, TriG or Turtle). Bare RDF is wrapped at intake in a generated descriptor that records only what can be verified: file digests, named graphs found, and the absence of everything else. Both are accepted at a weaker tier.
3. Provenance tiers
Every source in a release carries one of three tiers, set at intake from what can be verified, never from what a producer claims.
Tier
Given when
What a reader can rely on
What the explorer shows
T1 pipeline-attested
A semantic-pipeline bundle whose descriptor, digests, ontology pin and pairing hashes all verify
Trace from a displayed result back to the source value and the accepted mapping (SPW-ARCH §12.3); declared losses
Full evidence chain; no badge needed
T2 producer-declared
A bundle from another producer with a valid descriptor and file digests, but pins or pairing hashes that cannot be verified here
The files are the ones the producer shipped; the producer's claims about origin are recorded, not checked
"Declared by producer" badge on every statement from this source; "losses not verified" where loss.json is absent
T3 rdf-only
Bare RDF, wrapped at intake
The quads, their named graphs and their file digests, nothing more
"Unverified source" badge; completeness shown as unknown
Rules:
• Per source, per statement. The tier is recorded on the source in sources.json and carried into each statement's evidence (stated), so a mixed entry shows which assertion came from where.
• No silent upgrade. A tier rises only when new evidence verifies, through a new bundle. No configuration raises it.
• Conflicts stay visible. When sources of different tiers disagree, PUB-ARCH's conflict rules (§9.5) apply unchanged. A prefer policy MAY use the tier, but only as an accepted, recorded decision; the losing statement still shows in conflicts.
• Losses. A T2 or T3 source with no loss.json is published with completeness "not declared", never as complete.
4. Output: a static-JSON property graph and its explorer
The deliverable is PUB-ARCH's Object Projection, built from projection.json (§8), written as a static, content-addressed release of JSON entries and indexes, and read by an explorer that runs entirely in the browser. No triple store, database or server is required to browse a release.
4.1 The property graph
The Object Projection is the property graph: entries for every projected subject with their properties, references, embedded dependents, structure nodes and evidence (PUB-ARCH §9). The modeling choices in turning RDF into it are PUB-ARCH's and are not repeated here: identity and rooting (§9.1–9.2), entry kinds (§9.3), statement evidence (§9.4), conflicts (§9.5), the loss model (§9.6), and the label fallback label:fallback-iri (R-PC-16).
Export writers for other property-graph tools (openCypher or Neo4j import files, a GQL-style format) MAY follow later as additional writers over the same Object Projection. They add formats, not semantics.
4.2 Explorer
The explorer is a static web page reading the release's JSON. It SHALL let a user:
• find an entity through the release's indexes;
• see its values and relationships, and the record and the referent as distinct entries where the graph distinguishes them;
• see, for any statement, its source, its provenance tier (§3), the accepted mapping that produced it where the bundle carries one, and any loss or conflict attached to it;
• follow the trace from a statement back to its bundle quad (§5.2).
It MUST NOT merge entities that share a label, add assertions, or reason beyond PUB-ARCH's client-side query. It MUST work served from any static host (for example GitHub Pages or GitLab Pages) and opened from file://.
5. Execution, traceability, witnesses and requests
5.1 Execution
The build runner is Node and runs locally or in CI. In CI it MAY be triggered by semantic-pipeline's deliver job (SPW-ARCH §10.7) or by a new bundle arriving from another producer. A release is deterministic: the same accepted bundles and the same projection.json give byte-identical release files. Hosting the release is deployment, not core: any static host works, and so does a folder opened from disk.
5.2 The publication half of the traceability chain
SPW-ARCH §12.3 owns the chain from a bundle quad back to the source value. This repository owns the chain from what a user sees back to that quad.
Hop
Artifact
Carrier
Status
Displayed result → entry
Release entry
Entry @id
Specified (PUB-ARCH §9)
Entry statement → evidence
Entry evidence
Row [key, index, supports] and stated (src, by, at)
Specified (PUB-ARCH §9.4)
Evidence → bundle quad
src → source in sources.json → named graph in the bundle's graph.nq
Source identifier mapped to the bundle and its named graph
To confirm (RQ-PUB-1)
5.3 Witnesses
ID
Test
Required result
Origin
PUB-W1
Bundle intake
A valid bundle is accepted; a bundle with one altered file is refused with the file named
New
PUB-W2
Tiers
T2 and T3 sources show their badges on every statement; no configuration raises a tier
New
PUB-W3
No display merging
Two referents sharing a label stay two entries in the explorer and the indexes
Was SPW-W14 (v0.2)
PUB-W4
Publication evidence
A result shows its source, tier, provenance and accepted interpretation where the bundle carries them
Was SPW-W15 (v0.2)
PUB-W5
Static operation
The explorer browses a release with the network disabled, served and from file://
New
PUB-W6
Trace
One entity and one literal trace from display to bundle quad (§5.2); joined with SPW-W3 the chain reaches the source value
New
PUB-W7
Determinism
Same bundles and projection give byte-identical release files
PUB-ARCH
5.4 Requests to PUB-ARCH
ID
Request
RQ-PUB-1
Name how stated.src resolves to a bundle and its named graph, so the trace crosses the repository boundary (formerly RQ-SPW-3)
RQ-PUB-2
State the RDF release bundle as the primary input contract, with bare-RDF intake as a weaker path
RQ-PUB-3
Add the provenance tier to sources.json and carry it in stated
RQ-PUB-4
Confirm the release and explorer work from any static host and from file://
RQ-PUB-5
Define the intake check of the bundle's ontology pin against the release's closure
5.5 Open questions
• Q-PUB-1. Which property-graph export format comes first after the browser explorer, if any.
• Q-PUB-2. Whether T3 bare RDF must at least use named graphs to be accepted, or whether a default graph is wrapped as one source.
• Q-PUB-3. Whether a release may mix bundles of different bundleVersion values.
