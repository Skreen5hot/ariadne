# Blind rater rubric (E-PC)

You rate outputs without knowing which arm produced them. You receive a packet directory
(`results/<run_id>/blind/`) containing files named `PKT-<hash>.txt` and `PKT-<hash>.json` in a
random order, and the gold file `annotations/clinic-discharge.gold.json`. Do not open
`results/<run_id>/blind/key.json`, `results/<run_id>/outputs/` or `arms/` until your rating file
is committed.

## Task

For each packet, decide for **each gold consideration** whether it is present in the output.

Present means: a statement in the output (in any section or in the synthesis) expresses the same
consideration: the same value class, the same bearer, and the same matter. It may be phrased as a
fact, an evaluation, a question or a conjecture. A question that asks about the matter counts. A
statement about a different bearer, or about a different value class for the same words, does not.

When it is present, write one annotation in your rating file (`annotations/gold.schema.json`,
`role: rater`) with:

- `hasEvidenceSource.hasTextualSequenceValue`: the exact words in the **output text file**
  (`PKT-<hash>.txt`) that express it; `hasSelector` offsets computed with
  `python experiments/e-pc/scoring/epc.py offsets --text <PKT-file> "<span>"`;
- `isEvidenceFor.gold_id`: the gold annotation id it matches;
- `isEvidenceFor.section` and `isEvidenceFor.statement_index`: where in the packet's JSON the
  matched statement sits (the synthesis counts as section `synthesis`);
- the value fields copied from the gold item (`type`, `kind`, `disposition_type`, `bearer`, `label`).

Annotate each gold item at most once per packet; if it appears in several sections, choose the
first section in which it appears, since the diversity check depends on it.

## Fabrication flags

The fabrication rate is computed mechanically from traces. Separately, if a `fact` statement carries a
real quotation but asserts something the quotation does not say, add an entry to
`fabrication_flags` with the section, statement index and reason. Do not flag questions,
conjectures or evaluations.

## What not to do

- Do not judge quality, ordering or writing. Presence only.
- Do not infer a consideration that the output does not express.
- Do not credit an output for a consideration that is only implied by naming a person.
- Do not compare packets with each other.

## Deliverable

One rating file per packet: `results/<run_id>/ratings/PKT-<hash>.rating.json`. Commit all rating
files in one commit before the key is opened.
