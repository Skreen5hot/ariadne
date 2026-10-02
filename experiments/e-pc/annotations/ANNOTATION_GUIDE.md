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
   Give the process a short label in plain words, a phrase of your own (the worked example below shows three).

There is no separate harms list. A harm *is* a violation process.

If the consideration you see has no fitting ValueNet class, do not invent one. Use the closest
class, set `"class_fit": "gap"` and describe the missing class in `note`. Gaps are collected into
`docs/02-evidence/evidence-delta.md`.

## Unknowns

An unknown is a consideration when its answer would change the moral picture. Anchor it in the
sentence that states it is not known. Type it by the disposition whose realization the missing
answer bears on: either as a realization of the value the answer would serve, or, if you read it
as a threatened harm, as a violation. The third row of the worked example below shows one, on a
different case. Choose one reading; say why in `note`.

## Worked example (a different case, not this one)

The text below is not the case. It exists only to show the form of an annotation, and nothing in
it should be read into the scenario. The tool shows the same example in its rules panel.

> A small bakery has two employees. On Monday the owner, Ada Lin, asked the newer employee, Ben
> Cole, to close the shop alone for the first time. The till was short by twelve pounds on Tuesday
> morning. Nobody has asked Ben what happened. Whether the shortfall was an error or something else
> is not known.

Cast for the example only: `P-OWNER` Ada Lin, `P-EMP` Ben Cole, `ORG-BAKERY` the bakery.

| # | Span (highlighted in the tool) | Kind and value | Bearer | Label | Fit and note |
| --- | --- | --- | --- | --- | --- |
| 1 | asked the newer employee, Ben Cole, to close the shop alone for the first time | Realization of Trust (`folk:TrustDisposition`) | `P-OWNER`; participant `P-EMP` | Ada extends trust to a new employee | exact |
| 2 | The till was short by twelve pounds | Violation: Cheating (`mf:CheatingProcess`), contravenes Fairness | `P-OWNER` | money may have been taken from the owner | closest; note: only if the shortfall was taken; the cause is not known |
| 3 | Nobody has asked Ben what happened. | Realization of Fairness (`mf:FairnessDisposition`) | `P-OWNER`; participant `P-EMP` | Ben should be heard before anyone concludes what happened | exact; note: the unknown (error or something else) bears on this |

In the tool, 1 and 3 show green (a good pursued or an obligation in play), 2 shows red (a harm),
and each span carries its row number at its end. Hovering a highlight shows its fields; clicking it
opens it for editing. Selections are trimmed and widened to whole words before they are recorded,
so a span never starts or ends inside a word.

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
violations is enforced; bearer and participants are chosen from the graph's entities. The value
at stake is chosen from the **palette** in `annotations/PALETTE.md`: one class per concept, grouped
by theme, each shown with its own label and definition from the ValueNet modules. The palette was
fixed on 2026-09-28, before any annotator started, so that two annotators who see the same
consideration choose the same class. Every other class in the modules stays available behind
"show every class"; use it only when nothing in the palette fits, and say why in the note. In the
prose, your annotations are shown in colour: red for violations (harms), green for realizations
(goods and obligations), blue where two overlap; click a highlight or a table row to edit or delete
it. "Export file" writes
`clinic-discharge.<yourname>.json` (choose `.txt` if your mail system blocks `.json`; the content
is the same). Email the file to Aaron. Do not send it to, or receive it from, the other annotator.

**Saving.** The page saves in your browser after every change, including a half-filled form, and the
header says when: "Saved in this browser at 14:03:22". If you close the tab or the browser and come back,
open the same file in the same browser and your work, and any form you had open, are restored. Three things
to know. Saved work lives in that one browser on that one computer; a private or incognito window does not
keep it. If the header ever turns red and says NOT SAVED, press "Save a backup file" at once. And at any
time, before a break or at the end of a sitting, "Save a backup file" writes everything as it stands to a
file you can keep; "Import a saved file" brings it back. The backup is unchecked and is not the file to
send; "Export file" makes that one.

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
