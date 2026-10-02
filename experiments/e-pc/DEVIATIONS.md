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

### D-1 (2026-10-02): examples drawn from the study case removed from the annotation guide and the tool

| Field | Value |
| --- | --- |
| `date` | 2026-10-02 |
| `by` | Aaron Damiano |
| `what` | The annotation guide (PREREG §3, Materials) and the tool's label hint contained two examples drawn from the study case: a harm from discharge without a cognitive screen, and an unknown about capacity with a suggested class and bearer. Both were replaced with pointers to the bakery worked example (commit `3620dd6`). |
| `why` | The examples were written with the guide on 2026-09-26 and the tool on 2026-09-28, and found on 2026-10-02. They name two considerations the annotators are meant to find themselves. |
| `timing` | before any output was seen; before any annotation began |
| `affects` | The independent annotator never saw the examples. Aaron saw them while testing the tool. At adjudication, his annotations of those two considerations are flagged as possibly prompted. No arm prompt contained the examples. |
| `run` | none |
