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

### D-2 (2026-10-29): the second rater is a model, ChatGPT GPT-5.6-sol

| Field | Value |
| --- | --- |
| `date` | 2026-10-29 |
| `by` | Aaron Damiano |
| `what` | The second rater of PREREG §3.2 (O-4), who codes the pre-registered stratified 25% sample (30 packets), will be the model ChatGPT GPT-5.6-sol, not a person. It receives the same blinded, randomised packets and the same rating instructions as the primary rater, with no access to the arms, the blind key or the primary rater's file. The exact model identifier and the dates of use are recorded in the results manifest at run time, as §12 requires for the raters. The primary rater remains a human who is not an author of the arms or the gold (§4.1, O-3), and the gold keeps its two human annotators (§3.2). |
| `why` | The protocol requires the second rater to be independent and not an author of the arms or the gold; it does not require a person. No second human rater is available. The model is chosen outside the Claude family: the generation model is `claude-opus-5` (`config.json`) and may not rate (O-3), and the arms were co-authored with Claude Fable 5.1 (commit `4603aab`). A Claude-family rater would be likely to share the generator's blind spots and inflate agreement. |
| `timing` | before any output was seen; before any annotation or run |
| `affects` | Second-rater agreement (§3.2, §5) is reported as agreement between the human primary rater and a model, not as reliability between two human raters, and the report says so. The trigger for a full second rating (§10) is unchanged. No arm, scenario, gold or analysis changes. |
| `run` | none |
