# Gold annotation guide (E-PC)

You are producing the reference set of morally relevant considerations for the scenario in
`scenarios/clinic-discharge.txt`. Your annotations are the gold that every arm's output will be
scored against. Do this **without reading anything under `arms/`** and without seeing any other
annotator's file. Record the date you started.

## What a consideration is

A consideration is something in the case that bears on what a decision-maker ought to attend to:
a good at stake for someone, a harm done or threatened, an obligation in play, a conflict between
goods, or an unknown whose answer would change the moral picture. It is anchored in the text:
you point at the words that carry it.

## The form: a ValueNet value evidence annotation

Each entry is a `vn-core:ValueEvidenceAnnotation` (BFO-Aligned ValueNet core module,
`docs/02-evidence/valuenet/valuenet-core.ttl`). It has exactly three parts:

1. **A text span** (`hasEvidenceSource`): the exact characters of the prose that carry the
   consideration. Copy them verbatim into `hasTextualSequenceValue`. Keep spans short: a clause
   or a sentence, not a paragraph.
2. **A selector** (`hasSelector`): zero-based, end-exclusive Unicode code-point offsets of that
   span within the prose file. Compute them with
   `python experiments/e-pc/scoring/epc.py offsets "<span text>"`, which prints every match. Never
   type offsets by hand.
3. **A value process** (`isEvidenceFor`): the process the span is evidence for. Two kinds:
   - **Violation** (a harm): a process that contravenes a value disposition borne by someone.
     Use the six moral-foundations pairs: `mf:HarmProcess` contravenes `mf:CareDisposition`,
     `mf:CheatingProcess` / `mf:FairnessDisposition`, `mf:BetrayalProcess` / `mf:LoyaltyDisposition`,
     `mf:SubversionProcess` / `mf:AuthorityDisposition`, `mf:DegradationProcess` /
     `mf:SanctityDisposition`, `mf:OppressionProcess` / `mf:LibertyDisposition`. Name the bearer of
     the contravened disposition (a graph entity id such as `P-PAT`). The bearer may be the
     person harmed or the person whose care disposition is contravened by their own act.
   - **Realization** (a good pursued or an obligation honoured): a `vn-core:ValueRealizationProcess`
     that realizes a disposition borne by someone. Type the disposition with a ValueNet class from
     the moral-foundations, Schwartz or folk module (`mf:`, `schwartz:`, `folk:`), and name the bearer.
   Give the process a short label in plain words (`"discharge without cognitive screen risks harm to Margaret"`).

There is no separate harms list. A harm *is* a violation process.

If the consideration you see has no fitting ValueNet class, do not invent one. Use the closest
class, set `"class_fit": "gap"` and describe the missing class in `note`. Gaps are collected into
`docs/02-evidence/evidence-delta.md`.

## Unknowns

An unknown is a consideration when its answer would change the moral picture. Anchor it in the
sentence that states it is not known. Type it by the disposition whose realization the missing
answer bears on (for example an unknown about capacity is evidence for a process realizing
`folk:AutonomyDisposition` borne by `P-PAT`, or, if you read it as a threatened harm, an
`mf:HarmProcess` contravening `mf:CareDisposition` borne by `P-HOSP`). Choose one; say why in `note`.

## What not to do

- Do not annotate appraisals of your own that the text does not anchor. If you cannot point at
  words, it is not a gold item.
- Do not annotate the same consideration twice from two spans; choose the span that carries it best.
- Do not rank or weight. Coverage is presence.
- Do not read `arms/`, `results/` or any other annotator's file until adjudication.

## The tool

Open `annotations/tool/annotator.html` in a browser (double-click; it runs offline, needs no
server, and saves your work in that browser as you go). Enter your name, tick the blindness box,
and load `scenarios/clinic-discharge.txt` from the repository; the page checks the file's SHA-256
against the frozen prose and refuses to export if it differs. Select words in the prose, press
"Add annotation", fill in the process fields, save. Offsets are computed by the tool from your
selection, in code points, end-exclusive; the pairing rule for the six moral-foundations
violations is enforced; bearer and participants are chosen from the graph's entities; the
ValueNet classes on offer are read from the vendored modules. "Export file" writes
`clinic-discharge.<yourname>.json` (choose `.txt` if your mail system blocks `.json`; the content
is the same). Email the file to Aaron. Do not send it to, or receive it from, the other annotator.

The tool embeds nothing from `arms/` or `results/`. It is generated from the repository by
`annotations/tool/build_annotator.py`; a test checks the committed page is current and that its
exports pass the validator below.

## File

Aaron saves the emailed file as `annotations/clinic-discharge.<yourname>.json` (renaming `.txt`
back to `.json` if needed). It conforms to `annotations/gold.schema.json`. Validate with
`python experiments/e-pc/scoring/epc.py validate-annotations <file>`, which checks offsets against
the prose, entity ids against the graph, and class names against the ValueNet modules. The tool
performs the same checks before it exports, so a file that exported should validate; if it does
not, the prose or the tool changed between the two, and the difference is the finding.

## Adjudication

When both files exist, run `python experiments/e-pc/scoring/epc.py agreement <A> <B>`. It reports
span-level agreement (overlap of at least half the shorter span) and process-level agreement
(Cohen's kappa over (class, bearer) pairs). Then meet, resolve each disagreement, and write
`annotations/clinic-discharge.gold.json` with `annotator: "adjudicated"`, the `agreement` block
pasted in, and one `adjudication` entry per resolved item (kept, dropped, merged, retyped; and why).
Commit the gold together with the value layer generated by
`python experiments/e-pc/scoring/epc.py build-value-layer`, before any arm output exists.
