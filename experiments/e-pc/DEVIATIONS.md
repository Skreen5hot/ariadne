# E-PC deviations log

Deviations from the frozen protocol (`PREREG.md`, hash in `PREREG.ratified`) are recorded here and
nowhere else. `PREREG.md` is never edited after the freeze; this file sits outside its hash so that
logging a deviation cannot invalidate the freeze. Pre-freeze amendments are recorded in `PREREG.md`
§13, which closed at the freeze.

Every entry carries all of these fields. An entry with a field missing is incomplete.

| Field | Meaning |
| --- | --- |
| `date` | when the deviation was decided |
| `by` | who decided it |
| `what` | what was done differently from the protocol, with the section it deviates from |
| `why` | the reason |
| `timing` | `before any output was seen` or `after output was seen`; the second kind is reported in the results as a post hoc change |
| `affects` | which outcomes, arms or analyses it touches, or `none` |
| `run` | the run id it applies to, or `none` |

A deviation never edits `PREREG.md`, `config.json`, the arms, the scenario or the gold in place. If
one of those must change, it is a new pre-registration (a new version of `PREREG.md`, a new freeze,
a new run id), and this file records why the old one was abandoned.

## Entries

None.
