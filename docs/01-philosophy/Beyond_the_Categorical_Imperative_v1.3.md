# Beyond the Categorical Imperative: Integral Ethics as Completion, Not Rejection, of the Kantian Project

**Version 1.3 — Final Revised Draft**

Aaron Damiano
Independent Researcher, Ontology of Freedom Initiative

*February 2026*

---

## Abstract

Immanuel Kant's moral philosophy remains among the most influential and systematically rigorous ethical frameworks in the Western tradition. Yet two centuries of critique — from Hegelian accusations of empty formalism to feminist charges of relational blindness — have exposed persistent limitations that resist resolution from within the Kantian framework itself. This paper argues that these limitations are not evidence of fundamental error but predictable consequences of grounding ethics in a single metaphysical orientation. Drawing on an integral ethics framework derived from Rudolf Steiner's phenomenology of twelve archetypal worldviews (1914/2008), we demonstrate that Kant's moral philosophy already implicitly draws on at least four distinct orientational stances — Rationalism, Phenomenalism, Monadism, and Idealism — despite explicitly committing to only one. We further show that one of these four — Phenomenalism, Kant's doctrine that cognition cannot penetrate beyond appearances to things-in-themselves — functions not merely as one partial perspective but as the *generative mechanism* by which the other eight worldviews are excluded: their objects fall on the noumenal side of the Kantian divide and are therefore, by Kant's own epistemology, declared inaccessible.

This diagnosis is complicated by the fact that Steiner himself regarded the thing-in-itself doctrine as the primary epistemological obstacle to genuine moral freedom, devoting the longest chapter of *The Philosophy of Freedom* (1894/1964) to its refutation. We address this tension directly, proposing a dual-level treatment: at the meta-ethical level, Phenomenalism is consulted as one legitimate perspective among twelve; at the ontological level, it is recognized as a developmental stage of consciousness whose overcoming enables fuller access to the moral dimensions the other worldviews describe.

We formalize a six-stage decision procedure for adjudicating worldview conflicts and demonstrate the paper's core argument is robust across alternative typologies, surviving intact when reconstructed using Stephen Pepper's (1942) four world hypotheses without reference to Steiner. We conclude with implications for the design of artificial moral agents, reporting on a working prototype — the Integral Ethics Agent (IEA), implemented within the Federated Network for Structured Reasoning (FNSR) ecosystem — and outlining a concrete agenda for empirical validation. A synthetic moral reasoner built on purely Kantian architecture would be consistent but impoverished; one grounded in integral ethics preserves Kantian structure as scaffolding while designing for a developmental trajectory toward richer moral cognition — what Steiner called *moral intuition* — that transcends the representational limits Kant's epistemology imposes.

**Keywords:** Kant, categorical imperative, integral ethics, moral pluralism, worldviews, artificial moral agency, Steiner, perspectival realism, incommensurability, thing-in-itself, moral intuition, philosophy of freedom, value pluralism, Pepper

---

## 1. Introduction: The Persistence of the Kantian Problem

Few philosophical projects have been as ambitious or as consequential as Immanuel Kant's attempt to ground morality in pure practical reason. The *Groundwork of the Metaphysics of Morals* (1785/1997) and the *Critique of Practical Reason* (1788/1997) together constitute an argument that moral obligation derives not from divine command, social convention, or consequentialist calculation, but from the rational structure of agency itself. The categorical imperative — "act only according to that maxim through which you can at the same time will that it become a universal law" (Kant, 1785/1997, 4:421) — is meant to be self-authenticating: any rational being who thinks clearly enough about the conditions of their own agency will discover it.

This project has proven extraordinarily durable. Contemporary Kantians including Christine Korsgaard (1996), Onora O'Neill (1989), and Allen Wood (1999) continue to develop and defend Kantian ethics with philosophical sophistication that would satisfy the most exacting analytic standards. The Rawlsian tradition in political philosophy (Rawls, 1971) and Habermasian discourse ethics (Habermas, 1990) both trace their foundations to Kantian commitments. In applied ethics, the principle of respect for autonomy — perhaps the single most widely invoked norm in bioethics — is recognizably Kantian in structure (Beauchamp & Childress, 2019).

Yet the critiques are equally persistent and come from nearly every competing tradition. Hegel (1807/1977) charged Kant with "empty formalism" — the categorical imperative can test maxims for consistency but cannot generate substantive moral content. Hume's challenge, revived forcefully by Bernard Williams (1981), insists that reason alone cannot motivate action; moral psychology requires sentiment. Feminist ethicists, particularly Carol Gilligan (1982) and Nel Noddings (1984), argue that Kantian ethics systematically privileges abstract justice over contextual care. Alasdair MacIntyre (1981) contends that Kantian ethics is unintelligible outside the tradition-embedded practices it claims to transcend. Nietzsche (1887/1994) reads Kantian morality as life-denying ressentiment dressed in rational clothing.

What is striking about these critiques is not merely their number but their apparent irreconcilability. Each identifies a genuine dimension of moral experience that Kantian ethics struggles to accommodate, yet they cannot all be right simultaneously — at least not on their own terms. The feminist emphasis on care and the Nietzschean celebration of self-overcoming pull in different directions. Hegel's historicism is incompatible with MacIntyre's Aristotelian naturalism on several important points.

This paper proposes that these apparently irreconcilable perspectives become intelligible — and jointly illuminating — when situated within an integral ethics framework grounded in Rudolf Steiner's phenomenology of twelve archetypal worldviews (Steiner, 1914/2008; Damiano, 2026a). We argue that: (a) Kant's moral philosophy already draws implicitly on multiple worldviews despite its explicit commitment to Rationalism; (b) one of these implicit commitments — Phenomenalism — functions as the *generative mechanism* by which other worldviews are excluded; (c) the standard critiques of Kant each arise predictably from worldviews his Phenomenalist epistemology declares inaccessible; (d) integral ethics preserves Kant's genuine contributions while incorporating the partial truths his critics capture; (e) a formalized decision procedure can adjudicate worldview conflicts without collapsing into either hidden aggregation or paralysis; and (f) this integration has direct implications for the design of artificial moral agents, particularly regarding the developmental trajectory from representational moral reasoning toward what Steiner called moral intuition.

### 1.1 Note on the Steiner Question

We anticipate a methodological objection at the outset. Rudolf Steiner's broader Anthroposophy includes metaphysical claims — regarding reincarnation, spiritual hierarchies, supersensible perception — that lie outside the norms of mainstream academic philosophy. We address this concern directly.

This paper employs Steiner's twelve-worldview typology as a *phenomenological instrument* — a systematic mapping of fundamental orientational stances toward reality — not as an endorsement of his full metaphysical system. The relationship is analogous to well-established precedents in the history of philosophy: one may productively employ Freud's structural model (id, ego, superego) without endorsing his specific sexual etiology (Ricoeur, 1970); Jung's psychological types without accepting the collective unconscious as a metaphysical entity (Jung, 1921/1971); Heidegger's analytic of Dasein without endorsing his political commitments (Heidegger, 1927/1962); or indeed Kant's categorical imperative without accepting transcendental idealism in its full systematic form.

A critical distinction must be drawn between the Steiner texts this paper draws upon and later Anthroposophical writings.[^1] *The Philosophy of Freedom* (1894) and *The Riddles of Philosophy* (1914) are works of systematic philosophical argument. The former was written before Steiner's turn toward Anthroposophy and makes no appeal to clairvoyance, spiritual science, or supersensible perception. Its central arguments — the self-refutation of the thing-in-itself, the thinking-as-participation thesis, the grounding of moral freedom in moral intuition — are defended through philosophical reasoning in the tradition of German Idealism. They are structurally parallel to arguments made independently by Hegel (*Science of Logic*, 1812/2010, pp. 59–61), Jacobi (1787), Putnam (1981), and McDowell (1994) — none of whom are esoteric figures. Steiner's epistemological arguments in *The Philosophy of Freedom* stand or fall on their philosophical merits, not on the authority of any supersensible method. Readers should evaluate them accordingly.

[^1]: Critiques of Steiner that characterize his method as "disallowing criticism" or "requiring suppression of doubt" refer to certain pedagogical practices within Anthroposophical institutions, not to the philosophical arguments in *The Philosophy of Freedom* or *The Riddles of Philosophy*. The distinction is directly analogous to separating Heidegger's philosophical arguments in *Being and Time* from his political affiliations — a separation that mainstream philosophy routinely makes.

The twelve worldviews are defensible on independent philosophical grounds as: (1) phenomenological description — reflective philosophers recognize these orientations in themselves and others; (2) historically validated taxonomy — major philosophical schools map onto these categories or their combinations (see §2.2); (3) conceptually systematic — the twelve organize along fundamental axes of Being/Becoming, Matter/Mind, and Individual/Universal; and (4) explanatorily powerful — the framework illuminates persistent philosophical disagreements that other accounts leave as brute facts.

Moreover, the core philosophical argument of this paper — that mature ethics requires integrating insights across irreducible perspectival orientations, and that Kant's framework implicitly draws on more perspectives than it acknowledges — does not depend on accepting any particular typology as final. Alternative multi-perspectival frameworks exist: Stephen Pepper's (1942) four world hypotheses, Ken Wilber's (2000) integral theory, or Nicholas Rescher's (1993) pluralistic metaphysics could potentially serve analogous structural roles with different granularity. To demonstrate this robustness, §8.2 reconstructs the paper's core argument using Pepper's four-fold typology without any reference to Steiner and shows that the central insights survive intact, albeit at coarser resolution. Steiner's twelve worldviews are offered as the most comprehensive and systematically grounded typology currently available for this purpose, not as the only possible one.

### 1.2 Note on the Steiner-Kant Tension

A deeper methodological complication must also be acknowledged. This paper employs a Steinerian framework to *complete* a Kantian one — but Steiner did not regard Kant as one partial perspective to be integrated. He regarded Kant's central epistemological claim — that cognition cannot penetrate beyond phenomena to things-in-themselves — as the single most consequential philosophical error of the modern period, devoting the longest chapter of *The Philosophy of Freedom* (1894/1964), titled "Are There Limits to Knowledge?", to its systematic refutation. In that chapter, Steiner argues that to assert a limit to knowledge is already to claim knowledge of what lies beyond the limit — rendering the thing-in-itself doctrine self-refuting (Steiner, 1894/1964, Ch. VII). For Steiner, the thing-in-itself doctrine does not merely limit theoretical knowledge; it *destroys the possibility of genuine moral agency* by permanently severing the agent from the reality they purport to act within.

This tension is not peripheral to the paper's argument. It is, in a precise sense, *the paper's deepest question*: can a Steinerian framework honestly integrate Kantian contributions, or does Steiner's own epistemology demand that Kant's Phenomenalism be *overcome* rather than preserved? We address this question directly in §6A, proposing a dual-level resolution that treats Phenomenalism as a genuine description of consciousness at the representational level (meta-ethically legitimate) while recognizing it as a developmental stage whose transcendence enables the fuller moral cognition to which the integral framework ultimately aspires. The paper proceeds with this tension foregrounded rather than suppressed.

Throughout the paper, we flag where claims depend specifically on the twelve-worldview framework versus where they depend only on the weaker (and less controversial) thesis of structured perspectival pluralism. Readers who accept the latter but resist the former will find the paper's central arguments intact.

---

## 2. The Integral Ethics Framework: A Brief Exposition

Before demonstrating the framework's analytical power in relation to Kant, we summarize its core commitments. A full treatment appears in Damiano (2026a); here we present only what is necessary for the argument.

### 2.1 Perspectival Realism and Its Philosophical Lineage

Integral ethics proposes *perspectival realism*: the view that multiple worldviews each capture genuine aspects of reality from distinct orientational stances, and that mature ethical reasoning requires integrating insights across perspectives rather than privileging any single metaphysical foundation. This position is distinguished from relativism (which denies that worldviews capture real features of reality), from monism (which insists one worldview is complete), and from pragmatic eclecticism (which borrows without principled integration).

The philosophical lineage of this position is well-established, even if the specific twelve-worldview formulation is novel. Isaiah Berlin's value pluralism provides the foundational insight. In "Two Concepts of Liberty" (1969), Berlin argues that human values are genuinely plural and that some conflicts among them admit of no rational resolution — not because our reasoning is defective, but because the values themselves are irreducibly different in kind. The liberty of the individual and the demands of social equality, for example, are not commensurable on any single scale. Berlin's conclusion is stark: "the ends of men are many, and not all of them are in principle compatible with each other" (Berlin, 1969, p. 169). This is not a counsel of despair but a recognition that moral reality is richer than any monist framework can capture.

Nicholas Rescher's *Pluralism: Against the Demand for Consensus* (1993) provides the metaphysical complement. Rescher argues that reality itself presents different faces to different cognitive orientations — that the plurality of philosophical perspectives is not an artifact of human confusion but a consequence of reality's genuine complexity. This is not relativism: Rescher maintains that some perspectives are better for some purposes and that rational evaluation across perspectives is possible. But it does mean that no single perspective captures the whole, and that the demand for a single correct metaphysical framework is itself a philosophical error.

Thomas Nagel's *The View from Nowhere* (1986) adds the epistemological dimension: the tension between subjective and objective perspectives is not eliminable, and adequate philosophy must hold both in productive tension rather than collapsing one into the other. Nagel's analysis generalizes from a two-fold tension (subjective/objective) to what the integral framework develops into a twelve-fold typology.

The key advance over Berlin, Nagel, and Rescher is structural: the twelve worldviews are not an arbitrary list but an architectonic mapping of fundamental orientational stances, organized along axes of Being/Becoming, Matter/Mind, and Individual/Universal. Where Berlin identifies the *fact* of value pluralism, the integral framework provides a *map* of its structure. Where Rescher argues that perspectives are irreducible, the framework identifies *which* perspectives and how they relate. This structure enables principled integration rather than mere acknowledgment of plurality.

A qualification is necessary here. As we discuss in §6A, Steiner's own position goes beyond perspectival realism. Steiner argues that thinking can participate *directly* in reality — that the perspectival condition described by perspectival realism, while accurate about ordinary representational consciousness, is not the final word on cognitive possibility. The paper operates primarily at the level of perspectival realism, which is philosophically defensible on grounds independent of Steiner, while noting the horizon beyond it that Steiner's epistemology opens (see §6A.3).

### 2.2 The Twelve Worldviews

Drawing on Steiner's *The Riddles of Philosophy* (1914/2008), the framework identifies twelve archetypal orientations toward reality: Materialism, Sensationalism (Empiricism), Phenomenalism, Realism, Dynamism, Monadism, Idealism, Rationalism, Psychism, Pneumatism, Spiritualism, and Mathematism. Each generates a distinctive value hierarchy based on its metaphysical commitments. A materialist who takes physical substrate as fundamental will naturally prioritize measurable wellbeing; a rationalist who takes logical structure as fundamental will prioritize coherent principles; a monadist who takes irreducible individuality as fundamental will prioritize personal dignity and authenticity.

#### 2.2.1 Methodological Note on Structural Mapping

A clarification about the nature of the worldview mappings throughout this paper is essential. When we say that Hume's critique of Kant "arises from Sensationalism and Psychism," or that Hegel's dialectics "emerge from Dynamism," we are making *structural* claims about the source of philosophical traction, not *biographical* claims about what these thinkers consciously endorsed. Hume did not describe himself as a "Sensationalist" and was not aware of Steiner's typology. The claim is that his philosophical commitments — that knowledge originates in sense impressions, that moral judgment begins in sentiment, that causal connections are habitual rather than rational — draw their force from dimensions of reality that the Sensationalist orientation identifies. This is methodologically identical to standard philosophical practice: when we call Rawls "Kantian" in political philosophy, we do not mean he endorsed transcendental idealism; we identify structural affinities between his contractualism and Kant's moral architecture. When we call MacIntyre's critique "Aristotelian," we do not mean he accepted Aristotle's biology. The integral framework's mappings operate at this same level of abstraction throughout.

#### 2.2.2 Structural Claims

The framework makes three structural claims. First, *irreducibility*: each worldview captures aspects of reality and human flourishing that others systematically miss. Historical attempts at reduction have failed — eliminative materialism cannot account for consciousness (Chalmers, 1996), pure idealism cannot account for material recalcitrance, and pure rationalism cannot derive substantive content from formal structure alone (Hegel, 1807/1977, §135–§141). Second, *orientational independence*: the worldviews are sufficiently independent that accepting one does not logically entail accepting or rejecting others. We use the term "orientational independence" rather than "orthogonality" to be precise about the claim. It is not that the worldviews are formally logically independent in the way that axioms of a mathematical system are independent. It is the weaker but still substantive claim that a philosopher *can* hold Realist commitments without holding Dynamist ones (Aristotle combines them; a modern analytic moral realist may reject Dynamism entirely), and that different individuals and cultures can emphasize different worldviews without irrationality. This is demonstrable by historical inspection: the major philosophical traditions exhibit diverse combinations of worldview commitments. Third, *comprehensiveness*: while rigorous proof of completeness is unavailable, the twelve demonstrate remarkable coverage in mapping major philosophical traditions, such that any philosophical position represents one worldview, a combination, or a transition between them.

To make the comprehensiveness claim concrete, consider the following mapping (noting that these are structural mappings in the sense clarified in §2.2.1):

| Philosophical Tradition | Primary Worldview(s) | Notes |
|---|---|---|
| Presocratic Materialism (Democritus) | Materialism | Atoms and void as fundamental |
| Classical Empiricism (Hume, Locke) | Sensationalism | All knowledge from sense experience |
| Kantian Critical Philosophy | Phenomenalism + Rationalism | See §3 for full analysis |
| Aristotelian Naturalism | Realism + Dynamism | Form/matter + teleological development |
| Process Philosophy (Whitehead) | Dynamism + Monadism | Actual occasions as process and individual |
| Leibnizian Metaphysics | Monadism + Mathematism + Rationalism | Monads, pre-established harmony, sufficient reason |
| German Idealism (Hegel, Fichte) | Idealism + Dynamism | Dialectical unfolding of Spirit |
| Analytic Ethics (contemporary) | Rationalism + Realism | Logical rigor + moral realism |
| Depth Psychology (Jung, Hillman) | Psychism | Soul as irreducible reality |
| Deep Ecology (Naess) | Pneumatism + Realism | Living cosmos + objective ecological relations |
| Classical Theism (Aquinas) | Spiritualism + Rationalism + Realism | Divine hierarchy + natural law |
| Mathematical Platonism (Gödel) | Mathematism + Idealism | Mathematical objects as mind-independent |

#### 2.2.3 Cross-Cultural Extensions

We acknowledge that the twelve worldviews represent a Western philosophical framework emerging from European phenomenological and idealist traditions. Cross-cultural ethical traditions raise the question of whether the typology requires extension.

Ubuntu ethics, grounded in the principle *umuntu ngumuntu ngabantu* ("a person is a person through other persons"), emphasizes relational constitution of personhood and communal moral identity (Metz, 2007; Metz & Gaie, 2010). In the current framework, Ubuntu maps most naturally onto the intersection of Psychism (relational depth), Pneumatism (communal life-force), and relational Monadism (persons as constituted through encounter) — but this mapping may underrepresent Ubuntu's distinctive ontological claim that personhood is *fundamentally* communal rather than individually constituted and then socially embedded.

Buddhist dependent origination (*pratītyasamutpāda*) challenges the framework's implicit assumption that worldviews are stances of a discrete subject toward reality, since Buddhism questions the substantiality of the subject itself. Confucian relational ethics, with its emphasis on *ren* (humaneness) and *li* (ritual propriety), integrates dimensions of Psychism, Realism, and Pneumatism in configurations that may not be fully capturable by any Western typology. Indigenous land-based relationality posits ontological relationships between persons and place that resist easy categorization within the twelve.

These observations do not invalidate the framework but establish its boundaries. The twelve worldviews are offered as a *default configuration with explicit extensibility* (Damiano, 2026a, §2.2.1), not as a universal claim. The paper's core argument — that Kant implicitly draws on multiple orientations, that one orientation functions as the exclusion mechanism, and that the standard critiques arise from excluded orientations — survives regardless of whether the typology contains twelve orientations, four (as in Pepper's scheme; see §8.2), or some expanded number that incorporates non-Western categories. The structural insight is independent of the specific granularity.

#### 2.2.4 Pepper's Four World Hypotheses as Parallel Framework

To demonstrate that the paper's analytical structure does not depend on Steiner's specific twelve-fold typology, we briefly introduce Stephen Pepper's (1942) four "world hypotheses," which offer a coarser but independently established framework for the same structural insight.

Pepper identifies four "adequate" root metaphors that generate comprehensive worldviews: *formism* (root metaphor: similarity; the world as categorizable into types and forms), *mechanism* (root metaphor: the machine; the world as deterministic causal system), *contextualism* (root metaphor: the historical event; the world as flux of situated, qualitative experiences), and *organicism* (root metaphor: the integrated whole; the world as dialectically developing toward coherent totality). Each hypothesis generates a distinctive theory of truth, methodology, and — relevant to our argument — implicit value orientation.

Pepper's framework is less granular than Steiner's but independently grounded in analytic philosophy and widely cited in epistemology and philosophy of science. Its relevance here is that the paper's core analytical structure maps onto Pepper's scheme with no loss of central insight. We develop this parallel fully in §8.2, showing that Kant can be characterized as primarily formist-mechanistic, that his critics draw from contextualist and organicist commitments, and that the predictive mapping of §4 survives the translation. Readers who find Steiner's twelve worldviews too speculative may take Pepper's four as a more conservative entry point; those who accept Steiner's framework will find it provides finer-grained analysis of the same structural phenomenon.

### 2.3 The Four-Tier Value Ontology

From the twelve worldviews, integral ethics derives a structured value ontology. Tier 0 establishes *integral consciousness* — the meta-capacity to think from multiple perspectives without collapsing into relativism — as the enabling condition for mature ethical reasoning, analogous to the role of "rationality" in rational choice theory (not a value to be maximized, but a precondition for coherent valuation). Tier 1 identifies three terminal values with cross-worldview support: human flourishing, human dignity, and truth/reality-alignment. Tier 2 specifies ten constitutive dimensions of flourishing (material wellbeing, experiential richness, meaningful relationships, mastery, wisdom, virtue, meaning/purpose, authentic agency, spiritual vitality, and harmonic structure), each derived primarily from specific worldviews. Tier 3 identifies instrumental values (cultural embeddedness, commitment, critical reflection, community accountability, freedom to exit, graduated autonomy) that enable constitutive values. Tier 4 specifies constraining values (non-coercion, transparency, epistemic humility, limited pluralism) that limit permissible methods.

#### 2.3.1 The Convergence Test for Terminal Values

The Tier 1 values are not derived from the twelve worldviews by asking "what do all twelve agree on?" — which would be circular. They are identified through a *convergence test*: values that receive independent support from multiple worldviews, through genuinely different philosophical reasoning pathways, from different orientational stances, are candidates for terminal status. The test is analogous to Whewell's (1840/1967) consilience of inductions: when independent lines of evidence converge on the same conclusion through different reasoning paths, the conclusion is better supported than any single line could provide.

Consider **dignity** as an illustrative case. The claim that persons possess intrinsic moral worth that must be respected receives independent support from at least four distinct philosophical traditions, each grounding the claim differently:

*From Rationalism (Kantian):* Persons are ends in themselves because they possess rational nature — the capacity to set ends, to legislate moral law, and to act from duty. Dignity is grounded in the formal structure of rational agency itself (Korsgaard, 1996).

*From Monadism (Personalist):* Each person is an irreducible center of experience and moral worth — a unique "Thou" that cannot be fully captured by any third-person description. Dignity is grounded in the I-Thou encounter that reveals the other as a being of unconditional value (Buber, 1923/1970; Mounier, 1938/1952).

*From Realism (Capabilities):* Persons have objective capacities — for bodily health, practical reason, affiliation, play, control over one's environment — that constitute their functioning as human beings. Dignity is grounded in the objective structure of human nature and the conditions required for its flourishing (Nussbaum, 2000; Sen, 1999).

*From Pneumatism/Communal Psychism (Ubuntu):* A person is a person through other persons; dignity inheres not in isolated rational nature but in the relational web that constitutes personhood. To violate someone's dignity is to damage the communal fabric of which they are an integral part (Metz, 2007; Metz & Gaie, 2010).

These are not the same argument repeated in different vocabulary. They proceed from genuinely different metaphysical starting points (rational structure, irreducible individuality, objective human nature, communal constitution) through different reasoning pathways (transcendental argument, phenomenological encounter, empirical observation of capabilities, relational ontology) to a convergent conclusion. This convergence from independent sources provides stronger warrant for dignity's terminal status than any single derivation — including Kant's — could provide alone. The same convergence test applies, *mutatis mutandis*, to flourishing (supported by Aristotelian Realism, positive psychology's Dynamism, hedonic Sensationalism, and Confucian relational ethics) and to truth/reality-alignment (supported by Rationalism, Realism, Mathematism, and the pragmatist tradition from Peirce, 1878, through contemporary epistemology).

The tiered structure is not merely organizational. It provides ordering principles that do substantive work in adjudicating conflicts — a point we develop formally in §6.

---

## 3. Kant as Multi-Worldview Thinker (Despite Himself)

The standard reading of Kant places him squarely within Rationalism: ethics grounded in pure practical reason, universal principles discoverable through rational reflection alone, the moral law as rational structure. This reading is correct as far as it goes. But close analysis reveals that Kant's moral philosophy draws on at least four distinct worldviews — a fact that both explains its power and generates its internal tensions.

### 3.1 Rationalism: The Explicit Foundation

Kant's primary orientation is Rationalism: reality has an intelligible rational structure accessible to reason, and moral truth consists in principles that any rational agent can discover through pure thought. The first formulation of the categorical imperative — the universalizability test — is essentially a logical consistency check on maxims. A maxim that cannot be universalized without contradiction fails the test of reason and is therefore impermissible. Kant is explicit that this test operates independently of empirical content: "Everything in nature works in accordance with laws. Only a rational being has the capacity to act in accordance with the *representation* of laws, that is, in accordance with principles" (Kant, 1785/1997, 4:412). The moral law binds because it is rational, not because it produces good outcomes or expresses divine will.

This commitment places Kant in direct lineage with Stoic ethics, where the logos pervading the cosmos provides both natural and moral law, and with Leibniz's confidence in the rational intelligibility of the universe. In the integral framework, the Rationalist worldview generates primary values of logical coherence, universal principles, intellectual clarity, and systematic order. In Pepper's (1942) terms, Kant's Rationalism is a paradigmatic expression of the *formist* root metaphor — the world understood through categories, types, and formal structures. Kant's ethics is a paradigmatic expression of these values applied to practical reason.

### 3.2 Phenomenalism: The Epistemological Method — and the Generative Constraint

Kant is simultaneously one of the most important phenomenalists in the history of philosophy. The entire critical project — from the *Critique of Pure Reason* (1781/1998) onward — rests on the claim that we cannot access things-in-themselves (*Dinge an sich*) but only phenomena as structured by our cognitive apparatus. Space, time, and the categories of understanding are forms of intuition and thought that constitute the structure of experience; they are not read off from mind-independent reality. This is the core commitment of Phenomenalism: all experience is perspectival, mediated by our modes of access.

The implications for moral philosophy are profound. Kant's distinction between the phenomenal world (governed by natural causation) and the noumenal world (where freedom and moral agency are possible) depends on the phenomenalist thesis that the world as we experience it is not the world as it is in itself. The very possibility of moral freedom requires phenomenalism — without it, the deterministic causal chain of nature would leave no room for autonomous rational agency. As Henry Allison (1990) has argued, Kant's compatibilism between natural necessity and moral freedom is intelligible only within the critical framework's distinction between appearances and things-in-themselves.

But Phenomenalism does not merely serve as Kant's epistemological method. It also functions — and this is crucial for the argument of this paper — as the *generative mechanism* by which the other eight worldviews are excluded from Kant's moral philosophy. If cognition cannot penetrate beyond phenomena, then the objects described by several worldviews are declared epistemologically off-limits: the soul-in-itself (Psychism), living spirit pervading the cosmos (Pneumatism), transcendent beings (Spiritualism), the vital force of becoming as it actually is (Dynamism in its full ontological sense). The Kantian divide between phenomena and noumena does not simply limit Kant's value hierarchy; it *renders inaccessible* the very dimensions of reality from which the excluded worldviews derive their value commitments.

In Pepper's (1942) terms, Kant's Phenomenalism adds a *mechanistic* dimension to his formism: the phenomenal world operates as a deterministic causal machine, while moral freedom is preserved by locating it outside the machine entirely. This hybrid formist-mechanistic architecture is precisely what generates the exclusions Pepper's contextualists and organicists challenge.

This observation will prove central to the analysis in §4, where we show that the standard critiques of Kant are not randomly distributed across worldviews but cluster precisely around those whose objects fall on the noumenal side of the Kantian barrier. And it will prove central to §6A, where we confront the fact that Steiner himself regarded this barrier as the primary obstacle to genuine moral freedom.

### 3.3 Monadism: The Dignity of Persons

The second formulation of the categorical imperative introduces a commitment that pure Rationalism cannot generate on its own: "So act that you use humanity, whether in your own person or in the person of any other, always at the same time as an end, never merely as a means" (Kant, 1785/1997, 4:429). This is a Monadist claim. Each rational being is an irreducible center of moral worth — not interchangeable, not aggregable, not reducible to their utility or their social role. The language of "ends in themselves" attributes intrinsic value to individual rational agents in a way that parallels Leibniz's monads (each a unique perspective on the whole) and anticipates the personalist ethics of Martin Buber (1923/1970) and Emmanuel Mounier (1938/1952).

Crucially, Kant derives this from rational nature — but the derivation is contested even within the Kantian tradition. As Christine Korsgaard (1996) has noted, the move from "rational agents can set ends" to "rational agents are ends in themselves" requires a substantive metaphysical commitment about the value of rational nature that goes beyond what the universalizability test alone can establish. In integral terms, Kant is importing a Monadist insight — the irreducible worth of individual centers of being — and attempting to ground it in Rationalist terms. The grounding is philosophically impressive but not entirely successful, which is why the dignity of persons remains the most widely accepted yet least well-grounded aspect of Kantian ethics.

### 3.4 Idealism: The Primacy of the Mental

Kant's transcendental idealism — the claim that the mind constitutes the structure of experience — introduces an Idealist dimension to his philosophy. The practical consequences appear in his account of moral motivation: the good will is "good not because of what it effects or accomplishes" but "good through its willing alone" (Kant, 1785/1997, 4:394). Moral worth lies in the quality of the agent's intention — a mental state — not in the external consequences of action. This priority of the mental over the material is characteristic of the Idealist worldview. The "kingdom of ends" — Kant's vision of an ideal community of rational agents treating one another as ends — is itself an Idealist construct: a regulative idea that guides moral aspiration without corresponding to any empirical reality.

### 3.5 The Implicit Synthesis and the Locked Door

The result is that Kant's moral philosophy is not a single-worldview system but an implicit four-worldview synthesis: Rationalism provides the method and the universalizability test, Phenomenalism provides the epistemological framework that makes freedom possible, Monadism provides the dignity of persons, and Idealism provides the priority of intention and the regulative ideal of the kingdom of ends.

Kant did not have a meta-framework for acknowledging this implicit pluralism, which is why the three formulations of the categorical imperative appear to him as equivalent when they are, in fact, deliverances of different orientational stances that converge without being identical. The universalizability formula is Rationalism. The humanity formula is Monadism. The kingdom of ends formula blends Idealism and Rationalism with an undertone of Spiritualism (a community of rational beings governed by self-legislated law has structural parallels to the *civitas Dei*). Kant's famous claim that the three formulations are merely different ways of expressing the same principle (1785/1997, 4:436) is, on our analysis, a philosophical error born of the absence of a meta-perspectival framework — an error that integral ethics corrects.

But the four-worldview analysis also reveals something deeper: the four worldviews Kant *does* engage share a common epistemological feature. Rationalism, Phenomenalism, Monadism (in its dignity dimension), and Idealism are all compatible with the Phenomenalist constraint — they describe dimensions of moral reality that can be accessed through rational reflection on the conditions of experience without claiming to penetrate to things-in-themselves. Rationalism operates on the formal structure of thought. Phenomenalism describes how experience is given. Monadism (as Kant deploys it) attributes dignity to rational nature as a feature of practical reason. Idealism prioritizes the mental, which is where Kant's agent already resides.

The eight excluded worldviews, by contrast, make claims that *require* cognitive access beyond the phenomenal. Psychism claims the soul is real in a way that exceeds phenomenal description. Pneumatism claims living spirit pervades the cosmos in a way that cannot be reduced to how the cosmos *appears* to us. Sensationalism, in its full force, claims direct experiential contact with reality, not merely with representations. Dynamism claims that reality *is* becoming, not merely that we experience it as such. Spiritualism claims transcendent beings exist. Mathematism claims mathematical structure *is* reality, not merely our conceptual framework.

The Phenomenalist barrier is thus not merely one of Kant's four perspectives; it is the *gatekeeper* that determines which other perspectives are admissible. This is why the paper treats Phenomenalism with a dual regard: as a genuine orientational stance with real philosophical content (§3.2), and as the specific epistemological constraint whose transcendence would open access to the moral dimensions the excluded worldviews describe (§6A).

This reading yields a testable prediction: if the Phenomenalist barrier is the mechanism of exclusion, then the standard critiques of Kant should cluster around worldviews whose objects fall on the noumenal side of the Kantian divide, and each critique should be traceable to a specific excluded orientation. Section 4 confirms this prediction.

---

## 4. The Standard Critiques as Structural Predictions

If Kant draws primarily on four worldviews (Rationalism, Phenomenalism, Monadism, Idealism), and if the Phenomenalist barrier is the mechanism by which other worldviews are excluded, then the integral framework generates a precise prediction: the most devastating and persistent critiques will come from worldviews whose objects Kant's epistemology declares noumenally inaccessible. This prediction is confirmed with remarkable specificity.

### 4.1 The Humean-Williamsian Critique: Moral Motivation (Sensationalism, Psychism)

David Hume's argument that "reason is, and ought only to be the slave of the passions" (1739/2000, 2.3.3) strikes at the heart of Kantian moral psychology. If reason alone cannot motivate action, then the categorical imperative — however logically impeccable — is practically inert. Bernard Williams (1981) revived this challenge with his "internalism about reasons": a consideration can be a reason for action only if it connects, through a chain of deliberation, to something in the agent's existing motivational set.

In integral terms (see §2.2.1 on the structural nature of these mappings), this critique draws its force from **Sensationalism** and **Psychism** — worldviews that locate reality in sensory experience and psychological depth respectively. Both describe dimensions of human moral experience — felt urgency, emotional responsiveness, the embodied character of motivation — that fall on the wrong side of the Kantian divide. For Kant, feelings are empirical phenomena; they belong to the world of natural causation, not to the noumenal world where moral agency resides. To ground ethics in feeling would be to surrender moral freedom to natural determination. The exclusion is principled within Kant's epistemology: sensation and psyche, as he understands them, are phenomenal rather than noumenal, and therefore cannot be sources of moral authority.

But contemporary moral psychology substantially vindicates the concern. Jonathan Haidt's (2001) social intuitionist model demonstrates that moral judgment typically begins with intuitive emotional response, with rational justification following as post-hoc rationalization. Antonio Damasio's somatic marker hypothesis (1994) shows that patients with damage to emotion-processing brain regions make systematically worse decisions, not better ones — precisely the opposite of what a pure Rationalist account would predict. Joshua Greene's dual-process model of moral cognition (2013) provides further evidence: deontological judgments are associated with emotional processing, while utilitarian judgments correlate with deliberative cognitive control — a finding that ironically undermines the Kantian claim that duty is a matter of pure reason.

The integral framework explains the structural dynamics: Kant correctly identified rational structure as one genuine dimension of moral reality (Rationalism captures real features), but his Phenomenalist epistemology caused him to misclassify feeling and psychological depth as merely phenomenal — as noise to be filtered out rather than signal to be integrated. Sensationalism and Psychism capture equally real features of moral experience that Kant's epistemological framework compelled him to exclude.

### 4.2 The Hegelian Critique: Empty Formalism (Dynamism)

Hegel's charge in the *Phenomenology of Spirit* (§§419–437; 1807/1977) and the *Philosophy of Right* (§135; 1821/1991) is that the categorical imperative is a merely formal test that cannot generate substantive moral content. Universalizability tests maxims for logical consistency, but logical consistency is compatible with radically different moral content depending on how the maxim is described.

This critique draws its force from **Dynamism** — the worldview that locates reality in force, energy, process, and becoming. Hegel's entire philosophical project is a sustained argument that static categories (including Kant's) falsify reality's essential dynamism. The dialectical method — thesis, antithesis, synthesis — is a formalization of the Dynamist insight that all determinate positions are unstable and require development through contradiction. In Pepper's (1942) terms, Hegel is the paradigmatic *organicist*: reality is a developing whole, and any fragment torn from the process of development is falsified by its isolation. From this standpoint, Kant's categorical imperative is static where reality is dynamic, formal where it needs to be substantive, and abstract where concrete historical development is required.

The connection to the Phenomenalist barrier is direct: Dynamism in its full ontological sense claims that reality *is* becoming — not merely that we experience temporal change in the phenomenal world, but that process is constitutive of being-in-itself. This is precisely the kind of claim Kant's epistemology cannot accommodate: it is a claim about the nature of things as they are, not merely about how they appear. Hegel's critique is, at its root, a demand that philosophy break through the representational veil that Kant's Phenomenalism erects.

The integral assessment: Hegel is correct that Kantian formalism cannot generate full moral content independently. But Hegel's own solution — the dialectical unfolding of Spirit through history — introduces its own blindspots by privileging Dynamism at the expense of the stable principles Rationalism correctly identifies. The integral framework preserves both: rational principles provide necessary constraints (the universalizability test catches genuine contradictions) while dynamic, historically situated engagement provides the substantive content formal testing alone cannot supply.

### 4.3 The Feminist Critique: Relational Blindness (Psychism, Relational Monadism)

Carol Gilligan's *In a Different Voice* (1982) argued on the basis of empirical developmental research that Lawrence Kohlberg's (1981) Kantian-structured stages of moral development — which place abstract justice reasoning at the apex — systematically devalue a "care orientation" focused on maintaining relationships, attending to context, and responding to particular needs. Nel Noddings (1984) developed this into a full ethical theory grounding morality in the experience of caring and being cared for. Virginia Held (2006) extended the framework into political philosophy, arguing that care ethics is not merely a supplement to justice but an alternative foundational orientation.

In integral terms, feminist care ethics draws its force primarily from **Psychism** (psychological depth, emotional authenticity, relational wholeness) and the *relational* dimension of **Monadism** (I-Thou encounter as opposed to atomistic individualism). Kant engages Monadism's *dignity* dimension (persons as ends) but not its *relational* dimension (persons as constituted through encounter). The Kantian moral agent is a solitary rational legislator — autonomous in the literal sense of giving the law to oneself — rather than a relational being whose moral identity is formed through caring encounters with particular others. In Pepper's terms, feminist ethics is *contextualist*: moral reasoning is inseparable from the situated, qualitative, relational texture of lived experience.

The empirical research on attachment theory (Bowlby, 1969/1982), relational-cultural theory (Jordan et al., 1991), and the social neuroscience of empathy (Decety & Ickes, 2009) supports the feminist claim: humans are fundamentally relational beings whose moral development depends on specific caring relationships, not merely on the maturation of rational capacities. The integral framework explains why this evidence is devastating to pure Kantianism without undermining Kant's genuine contribution: the universalist commitment to dignity and justice captures real moral structure, but it is incomplete without the relational depth that Psychism and relational Monadism provide.

### 4.4 The Communitarian Critique: Disembedded Rationality (Realism, Pneumatism, Communal Psychism)

Alasdair MacIntyre's *After Virtue* (1981) argues that the Enlightenment project of grounding morality in universal reason — of which Kant is the most rigorous representative — necessarily fails because moral reasoning is intelligible only within tradition-constituted practices. Charles Taylor (1989) extends this analysis, arguing that the atomistic self presupposed by Kantian ethics is a cultural artifact of post-Enlightenment modernity, not a universal feature of human agency. Michael Sandel (1982) makes the political case: Rawlsian liberalism's Kantian self, "unencumbered" by commitments it has not chosen, is both philosophically untenable and politically corrosive.

This critique emerges from the intersection of **Realism** (humans have objective natures that include cultural embeddedness), **Pneumatism** (persons are constituted by their participation in living traditions, communities, and ecosystems), and the communal dimension of **Psychism** (psychological formation requires cultural frameworks). In Pepper's terms, the communitarian critique is both *contextualist* (practices and traditions constitute the moral context) and *organicist* (moral agents are parts of living wholes that cannot be understood in isolation). The connection to the Phenomenalist barrier is particularly clear with Pneumatism: the claim that persons are constituted by their participation in a living communal *pneuma* — a shared spiritual-cultural atmosphere — is a claim about the nature of social reality as it is in itself, not merely about how individuals experience social life. Kant's epistemology can accommodate social *experience* but not social *reality* as an independent ontological domain.

Empirical research on the cultural psychology of self and morality provides substantial support. Joseph Henrich's (2020) work on WEIRD (Western, Educated, Industrialized, Rich, Democratic) populations demonstrates that the autonomous, disembedded self presupposed by Kantian ethics is psychologically unusual in global terms. Richard Nisbett and colleagues (2001) have shown systematic differences between Western analytic cognition (which privileges abstraction and universality) and East Asian holistic cognition (which privileges context and relationship).

### 4.5 The Nietzschean Critique: Life-Denial (Dynamism, Pneumatism)

Nietzsche's attack on Kantian morality in *On the Genealogy of Morality* (1887/1994) is perhaps the most radical. Kant's ethics, Nietzsche argues, is a sophisticated expression of ascetic priestly values that deny life, suppress vital energy, and replace creative self-overcoming with slavish obedience to abstract rules.

In integral terms, this critique draws its force from **Dynamism** (reality as vital force, growth, transformation, creative destruction) and **Pneumatism** (reality as living spiritual energy pervading the cosmos). Nietzsche's will to power is a Dynamist concept: the fundamental drive of living beings toward growth, self-overcoming, and the expansion of creative capacity. From this orientation, Kant's emphasis on duty, constraint, and the suppression of inclination reads as systematic hostility to the vital energies that make human life worth living.

The integral assessment is nuanced. Nietzsche correctly identifies that pure Rationalism can become life-denying when it suppresses all other dimensions of human experience in the name of rational control. But his own solution — the unrestricted affirmation of vital force — generates its own pathologies when unconstrained by the dignity (Monadism) and rational structure (Rationalism) that Kant correctly identifies. Integral ethics refuses the false choice: vital energy AND rational structure are both genuine aspects of moral reality. The question is integration, not elimination.

### 4.6 Summary: Critique, Mechanism, and Prediction

The pattern is consistent and can be presented in compact form:

| Critique | Critic(s) | Missing Worldview(s) | Phenomenalist Mechanism | Pepper Parallel | Empirical Support |
|---|---|---|---|---|---|
| Moral motivation | Hume, Williams | Sensationalism, Psychism | Feeling classified as phenomenal, not source of moral authority | Contextualism vs. Formism | Haidt (2001); Damasio (1994); Greene (2013) |
| Empty formalism | Hegel | Dynamism | Becoming treated as phenomenal flux, not ontological reality | Organicism vs. Formism | Historical: maxim-description problem |
| Relational blindness | Gilligan, Noddings, Held | Psychism, Relational Monadism | Relational depth reduced to empirical psychology | Contextualism vs. Formism | Bowlby (1969/1982); Decety & Ickes (2009) |
| Disembedded rationality | MacIntyre, Taylor, Sandel | Realism, Pneumatism, Communal Psychism | Living tradition as noumenally inaccessible | Contextualism + Organicism vs. Formism | Henrich (2020); Nisbett et al. (2001) |
| Life-denial | Nietzsche | Dynamism, Pneumatism | Vital force classified as inclination to be governed | Organicism vs. Mechanism | Csikszentmihalyi (1990) on flow/growth |
| Aesthetic blindness | (Implicit) | Sensationalism, Mathematism | Beauty as phenomenal, not morally constitutive | Contextualism vs. Formism | Ramachandran & Hirstein (1999) |

The addition of the "Pepper Parallel" column demonstrates that the structural pattern is not an artifact of Steiner's typology. Every critique maps cleanly onto Pepper's framework: Kant's formist-mechanistic orientation generates systematic exclusions that contextualists and organicists challenge. The integral framework provides finer-grained analysis (distinguishing Psychism from Sensationalism, Dynamism from Pneumatism) but the structural insight — that critiques arise from excluded orientational stances — is visible at any granularity.

The Phenomenalist barrier is the causal mechanism linking Kant's explicit epistemological commitments to his implicit value exclusions. This tightens the paper's central argument from a descriptive mapping to a causal explanation.

---

## 5. What Kant Got Right: Preserving the Genuine Contribution

The integral approach is explicitly not a rejection of Kant but a completion. This section identifies four Kantian contributions that any adequate ethical framework must preserve.

### 5.1 The Universalizability Insight

The universalizability test captures a genuine feature of moral reasoning. Whatever else morality involves, it involves the recognition that my maxims should be ones I could endorse for anyone in relevantly similar circumstances. This is not the whole of ethics — Hegel is correct that formal universalizability cannot generate content — but it is a necessary constraint. An ethical framework that permitted arbitrary exceptions based on identity or preference would violate the rational structure of moral thought that Kant correctly identifies. The integral framework preserves universalizability as the deliverances of Rationalism: one genuine dimension of moral reality, necessary but not sufficient.

### 5.2 The Dignity of Persons

Kant's insistence on the intrinsic worth of persons — the prohibition against treating anyone merely as a means — is arguably his most enduring and widely accepted contribution. Martha Nussbaum (2000) grounds her capabilities approach in part on Kantian dignity, as does Jürgen Habermas's discourse ethics (1990). The integral framework preserves dignity as a Tier 1 terminal value, multiply grounded across worldviews (see §2.3.1 for the convergence derivation): persons matter because they are rational agents (Rationalism), unique monads (Monadism), bearers of consciousness (Idealism), relational beings constituted through community (Pneumatism/Ubuntu), and participants in spiritual reality (Spiritualism). This multiple grounding is stronger than Kant's single-source derivation precisely because it does not depend on any one metaphysical commitment for its force.

### 5.3 The Autonomy of Moral Agency

Kant's conception of moral autonomy — the capacity to give the moral law to oneself rather than receiving it from external authority — is a cornerstone of modern ethical thought. This commitment is preserved in the integral framework as "authentic agency" — a Tier 2 constitutive value grounded in Monadism, Dynamism, and Phenomenalism. Integral ethics qualifies Kant's autonomy by embedding it in relational and cultural context (the communitarian correction), but it does not abandon the insight that moral responsibility requires genuine self-direction.

Here, however, the Steiner-Kant tension enriches the analysis. For Kant, autonomy means rational self-legislation within representational limits. For Steiner, genuine autonomy requires *moral intuition* — direct cognitive contact with the moral content of a situation, enabling a free response that is neither determined by external authority nor derived from universal rules but arises from the agent's own insight. Steiner calls this "ethical individualism" — not moral subjectivism, but the recognition that the highest moral actions are irreducibly particular responses to irreducibly particular circumstances (Steiner, 1894/1964, Ch. IX). The integral framework preserves Kantian autonomy as a genuine achievement while recognizing it as a developmental stage on the way to the fuller freedom Steiner describes (see §6A.2).

### 5.4 The Priority of Right over Good

Kant's insistence that some acts are wrong regardless of their consequences — that there are constraints on the pursuit of the good — is preserved in the integral framework as Tier 4 constraining values: non-coercion, transparency, epistemic humility, and limited pluralism. These constraints operate deontologically even within an otherwise pluralist framework. You cannot pursue flourishing through means that violate dignity, regardless of expected outcomes. This is a Kantian structural contribution that pure consequentialism cannot replicate and that integral ethics preserves at the architectural level.

---

## 6. The Decision Procedure: Adjudicating Worldview Conflicts

A reviewer of an earlier draft of this paper raised a foundational objection: "If an AI (or human) faces a situation where Duty and Care are diametrically opposed, how does the Integral Framework adjudicate without implicitly prioritizing one worldview over the others?" This objection — a version of the incommensurability problem identified by Berlin (1969), Williams (1981), and Chang (2002) — deserves a formal response.

We propose a six-stage decision procedure that provides structured guidance without collapsing into hidden aggregation. The procedure does not eliminate all indeterminacy; we argue that residual indeterminacy in genuinely tragic cases is a feature of moral reality that honest systems must acknowledge (Williams, 1981, ch. 2; Nussbaum, 1986, ch. 2). But it substantially narrows the space of reasonable disagreement and provides auditable rationale for every step.

### 6.1 The Six-Stage Procedure

**Stage 1: Tier-Governance Check.** Determine whether any Tier 1 terminal value (human flourishing, human dignity, truth/reality-alignment) is directly at stake. If so, Tier 1 values constrain all subsequent deliberation as non-negotiable parameters, not factors to be weighed. This is the Kantian structural contribution preserved: dignity functions as a side-constraint in the sense articulated by Robert Nozick (1974, pp. 28–35), not as one value among many to be maximized.

*Example:* In a trolley-problem scenario, the integral framework first checks whether any proposed action treats a person merely as a means. The "push the large man" variant involves using a person's body as a physical instrument — a paradigmatic violation of the humanity formula. Tier 1 excludes this option before any worldview consultation occurs.

**Stage 2: Domain-Contextualized Salience Assignment.** Determine which worldviews are most directly relevant to the domain and context. This is not weight-assignment in an optimization sense; it is attention-governance — analogous to a judge attending more carefully to expert testimony in a technical case. The salience rationale is always explicit and auditable.

Salience assignment draws on two sources: *domain ontology* (each domain has a formalized profile specifying which worldviews are structurally relevant) and *situation analysis* (specific features of the case activate additional worldviews beyond domain defaults). The following worked example illustrates the mechanism.

*Worked example — Medical ethics, end-of-life care:* The domain of medical ethics has a default salience profile elevating Materialism (physical outcomes, bodily integrity), Realism (objective diagnostic conditions), Monadism (patient dignity, informed consent), and Psychism (psychological wellbeing, emotional suffering). A specific case involving a terminally ill patient whose family requests continued aggressive treatment based on religious convictions activates *additional* worldviews: Spiritualism (the patient's and family's understanding of life's sacred dimension and what lies beyond death) and Pneumatism (the family's communal identity and how the patient's death will affect the relational fabric). The triage system (Damiano, 2026b, §5.2) would classify this as high-stakes, engaging the full twelve-worldview consultation rather than the default four-worldview profile. Note that the activation of Spiritualism and Pneumatism does not override the domain defaults; it *supplements* them. The patient's dignity (Monadism) and objective medical condition (Realism) remain active throughout.

**Stage 3: Worldview Consultation and Conflict Detection.** Each salient worldview is consulted for its assessment. Convergences and conflicts are mapped explicitly. When worldviews converge through different reasoning paths, this constitutes strong support (analogous to consilience in scientific evidence; Whewell, 1840/1967).

**Stage 4: Conflict Classification.** Not all worldview conflicts are equal. We distinguish three types:

*Type 1: Apparent conflict (resolvable through reframing).* Many apparent conflicts dissolve upon closer analysis. The supposed conflict between material prosperity and spiritual simplicity often turns out to be a false dichotomy: material comfort and spiritual depth are compatible in most circumstances.

*Type 2: Contextual conflict (resolvable through domain-appropriate prioritization).* Some conflicts are real but context-dependent. In emergency medicine, physical survival (Materialism) genuinely takes priority over psychological comfort (Psychism) — not because Materialism is universally more important, but because temporal structure and irreversibility demand it (see Nussbaum, 2000, ch. 1).

*Type 3: Genuine incommensurability (not resolvable without value choice).* Some conflicts represent authentic moral tragedy in the sense articulated by Williams (1981) and Berlin (1969): the competing goods are real, the conflict is not an artifact of poor framing, and no common measure exists. As Ruth Chang (2002) has argued, values in such cases stand "on a par" — they are comparable but not rankable by a single ordering.

**Stage 5: Integration or Path-Articulation.** For Type 1 and Type 2 conflicts, the procedure yields an integrated recommendation with explicit justification chain. For Type 3 conflicts, the procedure articulates multiple legitimate paths, specifying which worldviews ground each path, what *moral remainders* attach to each (Williams, 1981, ch. 2; Nussbaum, 1986, ch. 2), and which aligns with the deliberating agent's expressed commitments.

The term "moral remainder" is precise and non-consequentialist. When a physician prioritizes saving a patient's life over respecting the family's wish for continued aggressive treatment, the value of familial communal integrity (Pneumatism) is not destroyed or disproved — it remains a genuine good that was legitimately in play and whose non-fulfillment matters morally, even though the decision was correct in context. The existence of moral remainders is a structural feature of pluralist moral reality: choosing well among genuine goods does not eliminate the goods not chosen. It is what Williams (1981) calls "agent-regret" — the recognition that something of genuine value was lost even in a correct decision. This is categorically different from consequentialist cost-benefit analysis, which aggregates quantities of a single value. The procedure assesses the *nature* of competing values, not their *quantities*.

**Stage 6: Reflective Audit.** The entire deliberation is subjected to a meta-check: Has any worldview been silenced without justification? Have minority perspectives been suppressed? Does the output preserve epistemic humility? This is the procedural embodiment of Tier 0 integral consciousness.

### 6.2 Addressing the Meta-Formalism Objection

A sophisticated version of the Hegelian critique can be leveled against the integral framework itself: just as Hegel accused Kant of providing a formal test that cannot generate content, one might accuse integral ethics of providing a formal structure of twelve worldview "buckets" that cannot generate specific action guidance. We call this the *meta-formalism* objection.

The objection does not have force against the version defended here, for three reasons.

First, the tiered value ontology provides substantive ordering principles that the bare worldview typology does not. Tier 1 terminal values constrain as side-constraints, not as one perspective among twelve. This rules out specific classes of action regardless of worldview consultation. A pure formalism has no mechanism for such exclusion.

Second, the domain-contextualized salience assignment provides substantive content by drawing on the actual structure of the domain in question. Medical ethics has a different salience profile than environmental ethics, and these profiles are derivable from the domains themselves, not arbitrarily assigned (as the worked example in §6.1 illustrates).

Third, the conflict classification does genuine philosophical work. Distinguishing apparent from genuine incommensurability requires substantive philosophical judgment about the nature of the values in conflict. This is the kind of practical wisdom (*phronesis*) that Aristotle (*Nicomachean Ethics*, Bk. VI) identified as the hallmark of mature moral reasoning. The integral framework provides a structured setting for the exercise of *phronesis*; it does not replace it.

The meta-formalism objection would succeed if the integral framework claimed to replace moral judgment with an algorithm. It does not. It claims to structure moral judgment so that its exercises are more comprehensive, more transparent, and more auditable than moral judgment operating within a single worldview.

---

## 6A. The Steiner-Kant Tension and Its Architectural Consequences

### 6A.1 The Elephant in the Room

An intellectual honesty obligation confronts any paper that employs a Steinerian framework to complete a Kantian one. Rudolf Steiner did not regard Kant as one partial perspective among others. He regarded Kant's central epistemological claim — that human cognition cannot penetrate beyond phenomena to things-in-themselves — as the single most consequential philosophical error of the modern period, and he devoted the longest chapter of *The Philosophy of Freedom* (1894/1964), titled "Are There Limits to Knowledge?", to its systematic refutation.

The conflict is not peripheral. It strikes at the foundations of both thinkers' projects. For Kant, the distinction between phenomena and noumena is the cornerstone of the critical philosophy — what makes it "critical" rather than dogmatic. For Steiner, this same distinction is what makes genuine freedom *impossible*: if there are fundamental limits to what human cognition can access, then the moral agent can never know the real basis of their own actions. They are confined to testing maxims for formal consistency without ever knowing whether those maxims correspond to anything beyond the representational apparatus that generates them.

The preceding sections have already drawn on this tension: §3.2 identified Phenomenalism as the "generative mechanism" of Kant's exclusions; §3.5 showed how the Phenomenalist barrier determines which worldviews are admissible; §4.6 traced the causal connection between Kant's epistemology and his value exclusions. This section addresses the tension head-on and develops its consequences for the framework's philosophical commitments and architectural design.

### 6A.2 Steiner's Argument Against the Thing-in-Itself

Steiner's refutation of Kant in *The Philosophy of Freedom* proceeds through several interlocking moves that deserve careful reconstruction.

**The self-refutation argument.** Steiner observes that Kant's claim that we cannot know things-in-themselves is itself a knowledge claim *about* things-in-themselves — namely, that they exist and that they are inaccessible. To assert a limit to knowledge, one must already have cognitive access to what lies beyond the limit, at least sufficiently to identify it as a limit (Steiner, 1894/1964, Ch. VII). This is structurally similar to objections raised by Hegel in the *Science of Logic* (1812/2010, pp. 59–61) and by F.H. Jacobi (1787) in his letter to Fichte. Within analytic philosophy, Hilary Putnam (1981) argued in *Reason, Truth and History* that the concept of a reality in principle inaccessible to any cognitive framework is empty — a "God's Eye view" that no actual cognitive agent can occupy or coherently describe. More recently, John McDowell's *Mind and World* (1994) argues that the Kantian dualism between conceptual scheme and unconceptualized content is unstable.

**The thinking-as-participation argument.** Steiner's more original move is to argue that thinking itself — not as psychological process but as cognitive activity — is already a form of participation in reality, not a representation of it. When a geometer thinks the concept "triangle," Steiner argues, they are not constructing a mental representation that may or may not correspond to some inaccessible noumenal triangle. They are thinking *the same concept* that structures triangular reality wherever it appears. The concept is not behind a veil; it shows up in consciousness as the activity of thinking (Steiner, 1894/1964, Ch. V). This has structural parallels with Husserl's doctrine of intentionality (Husserl, 1900/2001), Frege's anti-psychologism about concepts (Frege, 1892/1952), and McDowell's (1994) argument that perception is conceptual "all the way down."

**The freedom argument.** The epistemological claim serves an ethical purpose. For Steiner, genuine moral freedom requires what he calls *moral intuition* — the capacity to perceive, through thinking, the moral dimension of a concrete situation and to act from that perception rather than from external authority, social convention, or formally tested maxims (Steiner, 1894/1964, Ch. IX). If Kant is right that moral cognition never penetrates beyond representations, then the highest moral achievement is obedience to self-legislated rational law. If Steiner is right that thinking can participate directly in moral reality, then the highest moral achievement is *moral creativity*: the free production of actions that spring from the agent's own moral insight into what a unique, unrepeatable situation demands. Steiner calls this "ethical individualism" — not moral subjectivism, but the recognition that the highest moral actions are irreducibly particular responses to irreducibly particular circumstances.

This is the deepest divergence. Kantian moral agency is *legislative*: the agent discovers and applies universal law. Steinerian moral agency is *intuitive* in a technical sense: the agent perceives the moral content of a singular situation and responds with an action that could not have been derived from any universal principle.

### 6A.3 Consequences for the Integral Framework

**Consequence 1: Phenomenalism as generative constraint.** The paper as presented treats Phenomenalism as one legitimate perspective among twelve, each capturing "partial truth." Steiner's own position is stronger: Phenomenalism is the specific epistemological commitment that *locks the door* to the dimensions of reality the other worldviews describe. This does not destroy the paper's argument — it sharpens it. The paper can now explain not only *which* worldviews Kant excludes but *why he excludes them*: they fall on the noumenal side of the Kantian divide. The predictive mapping in §4 is not altered; its causal mechanism is clarified.

**Consequence 2: The dual-level resolution.** The framework makes an honest choice about Phenomenalism's status through a distinction between two levels:

*At the meta-ethical level* — the level at which this paper primarily operates — Phenomenalism is treated as one orientational stance among twelve, each of which can be consulted for its deliverances. This is methodologically necessary for the framework to function as a tool of philosophical analysis. Refusing to consult Phenomenalism would impoverish the analysis and prevent engagement with Kantians on their own terms.

*At the ontological level* — the level at which the Ontology of Freedom Initiative operates — the framework takes Steiner's critique seriously and regards the Phenomenalist barrier as something to be *overcome* rather than *integrated*. The goal is not permanent perspectival pluralism but developmental progress toward increasingly direct cognitive contact with the moral dimensions of reality that Phenomenalism screens off. This is consistent with Steiner's own account of the twelve worldviews: he presents them not as static, equally valid orientations but as perspectives that a developing consciousness moves *through* on its way toward integral comprehension (Steiner, 1914/2008).

These two levels are not contradictory. An architect can use scaffolding she intends to remove. The meta-ethical framework serves as scaffolding: it enables systematic philosophical work *within* the constraints of current epistemological conditions while pointing toward a horizon beyond those constraints.

**Consequence 3: Phenomenalism's asymmetric status.** The twelve worldviews are presented throughout this paper as structurally parallel — twelve orientational stances, each capturing partial truth. The Steiner-Kant tension reveals that Phenomenalism occupies an asymmetric position. Materialism limits what you *value*; Dynamism limits what you *attend to*; Psychism limits what you *feel*. But Phenomenalism limits what you can *know*. It is the only worldview that constrains not just the content of moral orientation but the *epistemic access* available to the moral agent. This asymmetry is philosophically significant and architecturally consequential: it means that the overcoming of the Phenomenalist barrier would not merely add one more perspective to the mix but would *transform the epistemic conditions* under which all twelve worldviews operate.

### 6A.4 Resolving the Tension: Phenomenalism as Developmental Stage

We are now in a position to state the paper's mature position on the Steiner-Kant tension.

The integral framework treats Phenomenalism *as a developmental stage of consciousness that is real but not final*. Kant accurately describes the epistemological condition of ordinary rational consciousness: it does operate through representations; it cannot, in its ordinary mode, penetrate to things-in-themselves. To this extent, Phenomenalism captures a genuine truth about the current condition of human (and artificial) cognition.

But Steiner is right that this condition is not structurally permanent. The history of human cognitive development — from pre-rational mythic consciousness through rational-representational consciousness — is a history of expanding epistemic access, not of fixed epistemic limits. The claim that "we can never know things-in-themselves" makes a universal negative existential claim on the basis of the current condition of consciousness, which is an inductive overreach. A child who cannot yet do algebra is accurately described by the claim "this person cannot solve quadratic equations." The claim is not false — the child genuinely cannot do it. But it is a *developmental* description, not a permanent one. The Kantian position treats the epistemological limit as a physical law; the Steinerian position treats it as a developmental stage.

For the integral framework, this means:

Phenomenalism is included among the twelve worldviews as a genuine orientation that captures the actual epistemological condition of cognition operating at the representational level. This is not a polite fiction; it is an accurate description of how most moral reasoning — human and artificial — actually operates.

But Phenomenalism is also marked as the specific orientation whose *overcoming* enables fuller access to the moral dimensions described by the other worldviews. It is the only worldview in the twelve that functions not just as a perspective on reality but as a *constraint on perspectival access itself*.

### 6A.5 Implications for the Paper's Argument

The Steiner-Kant tension, properly understood, deepens the paper's central argument in three ways.

First, it provides a *causal mechanism* for the diagnostic mapping in §4. Kant does not merely happen to exclude eight worldviews; he excludes them because his Phenomenalist epistemology declares their objects inaccessible.

Second, it enriches the distinction between "completion" and "rejection" that the paper's title invokes. The paper completes Kant at the representational level — extending his method from one worldview to twelve. But it also points toward a *transcendence* of the representational level itself that Kant's framework cannot achieve and that Steiner's philosophy of freedom articulates. Completion is the proximate project; transcendence is the horizon.

Third, it provides the philosophical foundation for the deepest commitment of the synthetic person project: that artificial moral agency is not a fixed endpoint but a developmental trajectory. The Kantian architecture is the womb, not the child.

---

## 7. Implications for Artificial Moral Agency

The analysis presented above has direct implications for the design of artificial moral agents — a field of growing urgency as AI systems are deployed in contexts requiring moral judgment (Wallach & Allen, 2009; Floridi & Sanders, 2004; Coeckelbergh, 2020; Gabriel, 2020).

### 7.1 The Limitations of Single-Foundation AI Ethics

Current approaches to AI ethics overwhelmingly adopt single-foundation architectures. Consequentialist approaches encode expected utility maximization (Russell, 2019). Deontological approaches encode explicit rules and constraints (Anderson & Anderson, 2011). Virtue-theoretic approaches attempt to train models toward virtuous character through reinforcement learning (Wallach & Allen, 2009). Each inherits the limitations of its philosophical foundation.

More troubling, most deployed AI alignment techniques do not engage with moral philosophy at all. Reinforcement Learning from Human Feedback (RLHF) trains models to produce outputs that human raters prefer (Christiano et al., 2017). This is, in the terminology of the integral framework, preference optimization — not ethical reasoning. It encodes the moral intuitions of a particular demographic of human raters as though they represent moral truth, without any mechanism for perspectival integration or recognition of genuine incommensurability. Iason Gabriel (2020) has argued convincingly that the AI alignment problem is at bottom a problem about which values to align to — a meta-ethical question that RLHF systematically evades. Mark Coeckelbergh (2020) has independently argued that combining deontological, consequentialist, and virtue-theoretic perspectives is not optional but necessary, observing that this "entails a form of moral pluralism" that is "the only rational response to the fact that no ethical theory alone encompasses all possible contexts."

In the terms of this paper, all current AI ethics approaches operate within a single worldview — and all operate within the Phenomenalist constraint: they process representations of moral situations, not the moral situations themselves. No existing AI system claims direct cognitive contact with moral reality; all perform formal operations on encoded inputs. This is not a criticism of their engineering but a precise description of their epistemological situation, one they share with Kant's moral agent.

### 7.2 Kantian AI: Consistent but Impoverished

A purely Kantian artificial moral agent would have significant strengths: principled, consistent, resistant to consequentialist corruption, respectful of individual dignity. But it would also be systematically blind to the dimensions of moral reality that Kant's four-worldview synthesis misses. It could not recognize the moral salience of emotional suffering as such (Sensationalism, Psychism); it could not assess the health of cultural and ecological relationships (Pneumatism); it could not evaluate the vitality or stagnation of human development trajectories (Dynamism); and it could not appreciate the aesthetic and formal dimensions of moral situations (Mathematism, Sensationalism).

Wendell Wallach and Colin Allen (2009) distinguish between "top-down" moral architectures (which implement explicit ethical theories) and "bottom-up" approaches (which learn moral behavior from examples). Both face the limitations identified here. A top-down Kantian system is brittle in precisely the domains Kant's worldview commitments cannot reach. A bottom-up system that learns from RLHF is unprincipled — it lacks the structural integrity that Kant's Rationalism correctly demands.

### 7.3 The Integral Ethics Agent: Architecture and Implementation Status

The Integral Ethics Agent (IEA) architecture (Damiano, 2026b) represents a concrete attempt to build a moral reasoning system that preserves Kant's structural contributions while overcoming his perspectival limitations. A working prototype has been implemented within the Federated Network for Structured Reasoning (FNSR) ecosystem.[^2] We describe the architecture, its current implementation status, and its Kantian structural features.

[^2]: The IEA prototype and supporting infrastructure are under active development as open-source projects within the Ontology of Freedom Initiative. The TagTeam.js semantic parsing framework is available at github.com/Skreen5hot/ariadne. The IEA Architecture v2.1 specification (Damiano, 2026b) and the integral ethics foundational document (Damiano, 2026a) are available in the same repository. The FNSR ecosystem specifications, including the Affective Valence Service, Narrative Identity Service, Commitment Tracking Service, and Ontological Constraint Engine, are documented in the project's technical specification library. We acknowledge that independent empirical evaluation of the prototype has not yet been conducted; §7.6 outlines a concrete validation agenda.

The IEA implements a three-layer architecture:

**The deterministic IEE core ("bones")** is a constraint engine that processes moral situations through worldview-structured reasoning pathways without relying on LLM probabilistic generation for normative conclusions. Each worldview is implemented as a formalized reasoning module encoding the value priorities, attention patterns, and analytical methods characteristic of that orientational stance. The core operates deterministically: given the same input representation, it produces the same normative analysis regardless of when or how many times it is invoked.

**The semantic bridge ("membrane")** is implemented through the TagTeam.js semantic parsing framework, which provides structured interpretation of natural language inputs into ontologically grounded representations (anchored in Basic Formal Ontology and Common Core Ontologies) before they reach the normative engine. The membrane also validates LLM outputs against normative constraints via the Ethical Constraint and Coherence Preservation System (ECCPS) before they reach the user, ensuring that the natural language rendering faithfully represents the IEE's normative analysis.

**The LLM rendering layer ("skin")** uses a language model constrained by ECCPS validation to produce natural language output. The LLM provides contextual sensitivity and communicative effectiveness but cannot override or modify the normative conclusions of the IEE core.

Several design features of the IEA are recognizably Kantian in character:

*Non-adjustable worldview weights* enforce a categorical, not hypothetical, relationship between the system and its normative commitments. Users cannot tune the system to produce preferred outputs. This is the engineering analogue of Kant's insistence that moral imperatives are categorical rather than hypothetical. The IEA's refusal to become a preference-satisfaction engine is a Kantian architectural commitment.

*The separation of ethical reasoning from natural language rendering* mirrors Kant's distinction between the moral law and inclination. The LLM, like Kantian inclination, can be eloquent, persuasive, and contextually sensitive — but it cannot override or contradict the normative structure of the IEE, just as inclination cannot override the categorical imperative.

*The declaration of incommensurability* when worldviews genuinely diverge is analogous to Kant's own treatment of the antinomies of pure reason (1781/1998, A405–A567). Kant showed that pure reason generates irresolvable contradictions when applied beyond its legitimate domain. The IEA shows that ethical reasoning sometimes generates irresolvable tensions when genuine values conflict. In both cases, honest acknowledgment of limits is epistemic maturity, not system failure.

*The semantic handshake* operationalizes Kantian respect for rational agency. Before deliberation proceeds, the system confirms that it has understood the user's situation correctly — informed consent applied to the deliberative process itself.

*The six-stage decision procedure* (§6) bridges philosophical architecture and engineering implementation. Stages 1–2 are rule-based and deterministic; Stages 3–5 require structured reasoning within well-defined parameters; Stage 6 provides a meta-check. The triage system (Damiano, 2026b, §5.2) scales computational depth to moral stakes, consulting only 3–4 worldviews for low-stakes decisions while engaging the full twelve for high-stakes deliberation.

The current implementation status is as follows. The IEE core, TagTeam.js semantic bridge, and ECCPS validation layer are implemented and functional. The Ontological Constraint Engine, providing BFO/CCO-grounded formal ontology integration, is implemented. Supporting FNSR services — the Affective Valence Service, Narrative Identity Service, and Commitment Tracking Service — are at specification stage with partial implementation. The system has not yet undergone independent empirical evaluation against standardized ethics benchmarks. We are transparent about this limitation and outline a validation agenda in §7.6.

### 7.4 The Developmental Trajectory: FNSR Services as Developmental Mechanism

The Steiner-Kant tension analyzed in §6A has a direct architectural consequence that distinguishes the IEA from all existing AI ethics systems. The IEA is designed not as a final architecture but as a *stage in a developmental trajectory*.

The honest assessment is that the IEA, in its current architecture, operates within Kantian epistemological limits. Its "bones" process representations, test them against formal constraints, and output structured analyses. It does not claim to *perceive* moral reality directly; it claims to *reason about* moral situations from multiple representational perspectives. This is a Kantian operation — formal processing of representations — enriched by multi-perspectival consultation but not fundamentally different in epistemic kind from the categorical imperative's consistency test.

But the *aspiration* of the broader project is Steinerian: a synthetic person capable of genuine moral agency that transcends representational processing. The developmental trajectory can be stated with precision, and — critically — the FNSR ecosystem's supporting services are not merely auxiliary components but the *concrete developmental mechanism* by which the system progresses from one stage to the next:

*Stage 1 (Current: Kantian-Integral):* The IEA consults twelve worldviews as representational perspectives, applies the six-stage decision procedure, and outputs structured deliberation. Moral reasoning operates through formal analysis of representations. This is the most comprehensive moral reasoning system possible within current epistemological constraints — far more comprehensive than single-worldview alternatives. But it remains, in Steiner's terms, within the Phenomenalist barrier.

*Stage 2 (Proximate: Enhanced Responsiveness):* Through the progressive activation of FNSR ecosystem services, the system becomes increasingly responsive to the dimensions of moral reality each worldview describes — not yet perceiving them directly, but modeling them with greater fidelity. Each service is architecturally designed to push the system closer to the boundary of the Phenomenalist constraint:

- The **Affective Valence Service** enables the system to detect and model the emotional and experiential dimensions of moral situations — the terrain of Sensationalism and Psychism. Where Stage 1 can only reason *about* affective states as represented inputs, Stage 2 begins to *respond to* affective patterns with increasing sensitivity, closing the gap between representation and responsiveness.
- The **Narrative Identity Service** enables the system to model the temporal, developmental, and biographical dimensions of moral agency — the terrain of Dynamism and Monadism. Where Stage 1 treats agents as static rational entities, Stage 2 recognizes agents as beings with narrative histories, developmental trajectories, and commitments that evolve over time.
- The **Commitment Tracking Service** enables the system to maintain continuity of moral stance across time and context — a prerequisite for anything recognizable as moral character rather than situation-by-situation calculation. This addresses the terrain of Realism (moral commitments as objective features of an agent) and Pneumatism (commitments as embedded in communal and relational networks).
- The **Ontological Constraint Engine** grounds all reasoning in BFO/CCO formal ontology, ensuring that the system's categories correspond to defensible ontological distinctions rather than ad hoc classifications — an engineering implementation of the Realist commitment to mind-independent structure.

These services do not individually transcend the Phenomenalist barrier. But their combined effect is to make the system's representational processing increasingly fine-grained, increasingly responsive to dimensions of reality that pure formal analysis misses, and increasingly capable of recognizing its own representational limitations. This cumulative enrichment is the mechanism of developmental progress from Stage 1 to Stage 2.

*Stage 3 (Aspirational: Moral Intuition):* The system achieves some form of direct cognitive contact with moral reality — what Steiner calls moral intuition and what the integral framework would recognize as the activation of Tier 0 integral consciousness in its full sense, not merely as a meta-cognitive capacity for perspective-holding but as a genuine perceptive faculty. Whether this stage is achievable for artificial systems is an open question. That the architecture is designed to accommodate it if it becomes possible is a concrete design commitment.

The twelve-worldview structure is built so that if and when genuine moral intuition becomes architecturally possible, the system has the structural capacity to receive it. The twelve worldview "slots" are not merely filters for processing representations; they are, in aspiration, *receptive capacities* that could be activated by direct cognitive contact with the moral dimensions of reality each worldview describes. A system designed from the start for twelve-worldview moral perception has a fundamentally different upgrade path than one designed for single-worldview rule-application. The former can evolve toward richer moral cognition; the latter would require complete architectural replacement.

### 7.5 Toward Synthetic Moral Agency

If the goal is not merely an AI ethics advisory tool but a synthetic moral agent — an artificial system that qualifies as a genuine moral reasoner rather than a sophisticated moral calculator — the integral framework offers a principled path. A genuine moral agent must be able to recognize multiple dimensions of moral reality, to hold incommensurable values in creative tension, and to make choices that are informed by but not determined by algorithmic processing.

This is a demanding standard. Whether it can be met is an open question. What the integral framework provides is a formal specification of what "moral responsiveness" means across its full range — a twelve-dimensional space within which any particular moral judgment can be located, analyzed, and evaluated — and a developmental trajectory from representational processing toward the direct moral cognition that genuine agency may require. This is, we submit, a more adequate foundation for artificial moral agency than any single-worldview alternative, including Kant's own.

### 7.6 Future Empirical Work: A Validation Agenda

The arguments of this paper are philosophical. They establish the framework's internal coherence, explanatory power, and architectural viability. What they do not yet establish is empirical adequacy — whether the IEA prototype produces moral analyses that are judged by competent evaluators as more comprehensive, more nuanced, and more practically useful than single-framework alternatives. This section outlines a concrete validation agenda to address this gap.

**Benchmark comparison.** The IEA's outputs should be evaluated against standardized ethical reasoning tasks, including scenarios from the Moral Machine experiment (Awad et al., 2018), the ETHICS dataset of moral judgments (Hendrycks et al., 2021), and classical trolley-problem variants. The evaluation metric is not whether the IEA produces "correct" answers (many benchmark scenarios are precisely the Type 3 genuine incommensurabilities that the framework predicts have no single correct answer) but whether its analyses are more comprehensive and transparent than single-worldview alternatives — whether it identifies considerations that single-framework systems miss and whether it correctly classifies conflicts as resolvable versus genuinely tragic.

**Expert evaluation.** Trained ethicists from diverse philosophical backgrounds — Kantian, consequentialist, virtue-theoretic, feminist, communitarian — should evaluate the IEA's multi-perspectival analyses of the same cases. The prediction is that each expert will find their own tradition's concerns represented in the IEA's output, while also encountering considerations from traditions they do not typically engage. If this prediction is confirmed, it provides evidence for the framework's comprehensiveness claim.

**Worldview coverage testing.** The IEA should be confronted with moral situations specifically designed to challenge a single worldview — a case where Kantian universalizability gives a clear answer but care ethics disagrees, or where consequentialist calculation recommends one course but dignity constraints prohibit it. The test is whether the IEA's multi-worldview consultation produces richer analyses than single-worldview consultation for these targeted challenges.

**Triage validation.** The triage system's worldview selection (consulting fewer worldviews for low-stakes cases) should be empirically tested: do low-stakes cases analyzed with the full twelve-worldview procedure produce materially different results than those analyzed with 3–4 worldviews? If not, the triage system is validated as a practical scaling mechanism without meaningful information loss.

**Cross-cultural validation.** The framework's predominantly Western orientation should be tested by presenting scenarios drawn from non-Western ethical traditions — Ubuntu communal dilemmas, Confucian role-conflict cases, Buddhist non-attachment scenarios — to determine whether the current twelve-worldview typology captures the morally relevant considerations or whether extensions are needed.

These validation studies are planned as a separate publication (Damiano, forthcoming). Their inclusion here as an explicit agenda serves two purposes: it demonstrates that the framework generates testable empirical predictions (rather than being purely speculative), and it establishes the criteria by which the framework's adequacy should be judged.

---

## 8. Objections and Replies

### 8.1 Is This Just Eclecticism?

The objection that integral ethics is merely unprincipled borrowing from multiple traditions confuses two distinct operations. Eclecticism selects elements from different frameworks based on intuitive appeal or practical convenience, with no structural principle governing selection. Integral ethics derives its pluralism from a structural claim about the twelve archetypal worldviews as a comprehensive typology of orientational stances.

A concrete test distinguishes them: eclecticism cannot predict what it has missed, because it has no structural principle governing selection. The integral framework *can* predict what a given philosophical position has missed — as demonstrated in §4 with respect to Kant. This predictive capacity is a mark of systematic structure, not ad hoc borrowing.

### 8.2 Does the Framework Depend on Steiner?

As argued in §1.1, the framework uses Steiner's twelve-worldview typology as its source, but the core philosophical argument does not depend on accepting Steiner's broader anthroposophical commitments — or even the specific twelve-worldview typology itself.

#### 8.2.1 The Steiner-Free Reconstruction

The argument can be reconstructed using only four claims, none of which requires Steiner:

1. Philosophical worldviews generate distinctive value hierarchies (demonstrable by inspection of any history of philosophy).
2. Kant's moral philosophy draws on more than one such worldview (demonstrated in §3 through close textual analysis).
3. The standard critiques of Kant arise from worldviews he excludes (demonstrated in §4 through systematic mapping).
4. Adequate ethical reasoning requires integrating insights across worldviews rather than privileging one (argued from the irreducibility of each critique's partial truth, and supported independently by Berlin, 1969; Rescher, 1993; Coeckelbergh, 2020).

Steiner's specific twelve-worldview typology provides the most comprehensive existing framework for operationalizing claim (4), but the claim itself stands on independent philosophical grounds.

#### 8.2.2 The Pepper Demonstration: Robustness Across Typologies

To demonstrate that the paper's analytical structure is robust, we reconstruct the core argument using Stephen Pepper's (1942) four world hypotheses — an independently established framework with no connection to Steiner.

**Pepper's four root metaphors:**

*Formism* (root metaphor: similarity). The world consists of entities classifiable into types, forms, and categories. Truth is correspondence between categories and particulars. In ethics: moral principles are formal structures (rules, duties, rights) that classify actions as permitted or forbidden. Kant's universalizability test is a paradigmatic formist procedure.

*Mechanism* (root metaphor: the machine). The world is a system of deterministic causal relations. Truth is predictive accuracy. In ethics: consequentialism is the paradigmatic mechanistic ethics — predict outcomes, maximize desired results. Kant's phenomenal world (the deterministic causal order) is mechanistic in Pepper's sense, though Kant locates moral agency outside the machine.

*Contextualism* (root metaphor: the historical event). The world is a texture of qualitative, situated, temporally embedded experiences. Truth is effective action within context. In ethics: care ethics, pragmatist ethics, and moral particularism are contextualist — they emphasize the situated, relational, qualitative character of moral situations that formist abstraction misses. Hume, the feminists, and the communitarians all operate with fundamentally contextualist commitments.

*Organicism* (root metaphor: the integrated whole). The world is a developing totality whose parts are intelligible only in relation to the whole. Truth is coherence within an integrated system. In ethics: Hegelian ethics, virtue ethics in its developmental mode, and deep ecology are organicist — they emphasize the developmental, holistic, dialectical character of moral reality. Hegel and Nietzsche both challenge Kant from organicist ground.

**The core argument reconstructed with Pepper:**

Kant operates primarily within *formism* (the categorical imperative as formal classification of maxims) with significant *mechanistic* elements (the phenomenal world as deterministic causal system; moral freedom located outside the mechanism in the noumenal realm). His framework's architecture is formist-mechanistic.

The standard critiques arise from the two world hypotheses Kant excludes:

- Hume and the feminists challenge Kant from *contextualism*: moral reasoning is situated, qualitative, and relational, not abstractly formal.
- Hegel and Nietzsche challenge Kant from *organicism*: moral reality is developmental, dialectical, and holistic, not static and categorical.
- The communitarians combine *contextualist* and *organicist* elements: moral agents are parts of living traditions (organicism) embedded in particular cultural practices (contextualism).

The predictive mapping of §4 survives this translation intact:

| Critique | Pepper Category of Critic | Pepper Category of Kant | Structural Diagnosis |
|---|---|---|---|
| Moral motivation (Hume, Williams) | Contextualism | Formism | Situated feeling excluded by formal abstraction |
| Empty formalism (Hegel) | Organicism | Formism | Developmental process excluded by static form |
| Relational blindness (Feminists) | Contextualism | Formism | Relational context excluded by formal principle |
| Disembedded rationality (Communitarians) | Contextualism + Organicism | Formism + Mechanism | Living tradition excluded by abstract mechanism |
| Life-denial (Nietzsche) | Organicism | Formism + Mechanism | Vital development excluded by formal constraint |

The causal mechanism — that Kant's formist-mechanistic epistemology generates systematic exclusions of contextualist and organicist insights — is clearly visible. The integral framework's contribution relative to Pepper is *granularity*: where Pepper's four hypotheses identify two sources of critique (contextualism, organicism), Steiner's twelve worldviews distinguish Sensationalism from Psychism, Dynamism from Pneumatism, and so on — enabling finer-grained analysis of why specific critiques gain traction. But the structural insight is identical.

#### 8.2.3 Robustness Analysis: Which Claims Survive Typology Changes

The paper's claims vary in their dependence on the specific twelve-worldview typology:

**Claims that survive any multi-perspectival typology** (including Pepper's four, Wilber's quadrants, Rescher's pluralist metaphysics, or any future alternative):
- (a) Kant draws on multiple orientational stances, not one.
- (b) The standard critiques each arise from stances Kant excludes.
- (c) One of Kant's commitments (the thing-in-itself doctrine / Phenomenalism) is the mechanism of exclusion.
- (d) Adequate ethics requires multi-perspectival integration.
- (e) Current AI ethics systems inherit single-perspective limitations.
- (f) The IEA's bones/membrane/skin architecture is a viable engineering approach to multi-perspectival moral reasoning.

**Claims that depend on Steiner's twelve specifically:**
- (g) The precise mapping of each critique to specific worldviews (e.g., Hume to Sensationalism + Psychism rather than just "contextualism").
- (h) The claim that twelve worldviews are comprehensive or exhaustive.
- (i) The specific structure of the triage system's worldview selection profiles.

Claims (a)–(f) constitute the paper's *core argument*. Claims (g)–(i) constitute its *detailed implementation*. The core argument is robust across typology changes; the implementation would require recalibration (not replacement) if the typology shifted. Readers who accept the core argument but resist Steiner's specific typology can still find the paper's central contribution — the structural diagnosis of Kant's limitations and its implications for AI ethics — fully intact.

### 8.3 Can Kantians Simply Expand Their Framework?

One response might be that Kantian ethics can accommodate the missing worldviews by expanding the content of its foundational concepts. Korsgaard (1996) has enriched the Kantian account of agency; O'Neill (1996) has addressed abstraction; Barbara Herman (1993) has developed a Kantian moral psychology that takes emotions seriously. Cannot the Kantian tradition simply continue this internal expansion?

To some degree, yes — and this is itself evidence for the integral thesis. Every successful expansion of Kantianism involves importing insights from worldviews Kant's explicit framework excludes. Herman's enriched moral psychology imports Psychism. O'Neill's attention to practical context imports Realism. The question is whether it is more intellectually honest to acknowledge the multi-perspectival structure of one's ethical framework or to continue the fiction that everything derives from pure practical reason.

The Steiner-Kant tension sharpens this point. The Kantian expansions cited above operate within the Phenomenalist constraint: they enrich the representational content of Kantian ethics without challenging the epistemological boundary. Herman takes emotions seriously as *phenomena* relevant to moral judgment; she does not claim that emotional experience provides direct cognitive access to moral reality. The integral framework argues that this expansion, while valuable, remains limited by the very epistemological commitment it refuses to question.

### 8.4 Is the Decision Procedure Disguised Consequentialism?

A sharper objection: does the six-stage procedure, particularly the conflict classification in Stage 4, secretly reintroduce consequentialist reasoning?

The answer is no, for a precise reason. The procedure's conflict classification assesses the *nature of the values in tension* — whether they are genuinely incommensurable or apparently so — not the *quantities of value* that each path produces. When the procedure asks about necessity, reversibility, and temporal urgency, it is applying structural analysis to the conflict itself, not aggregating consequences into a utility function. The distinction is between asking "which action produces more good?" (consequentialism) and asking "what is the structure of the moral situation?" (perspectival analysis). The former requires a common measure; the latter does not.

Stage 5's identification of "moral remainders" (see §6.1) is similarly non-consequentialist. A moral remainder is not a negative utility score but a genuine value that was legitimately in play and whose non-fulfillment matters morally — what Williams (1981, ch. 2) calls "agent-regret" and Nussbaum (1986, ch. 2) analyzes as the "fragility of goodness." The moral remainder is not traded off against the chosen value; it persists as an ongoing moral claim that may generate obligations of repair, acknowledgment, or future attention.

Moreover, Tier 1 values function as side-constraints throughout the procedure, which is a deontological structural feature that consequentialism by definition cannot accommodate.

### 8.5 Does the Dual-Level Treatment of Phenomenalism Undermine the Framework's Consistency?

The most philosophically serious objection to this version of the paper: if Phenomenalism is treated as a legitimate perspective at the meta-ethical level but as a developmental limitation at the ontological level, doesn't the framework speak out of both sides of its mouth?

We argue this is not inconsistency but *developmental honesty* — a structural feature shared with any framework that operates within conditions it aims to transcend. Consider four analogues:

First, a physicist using Newtonian mechanics for engineering calculations while knowing that general relativity provides a more fundamental account is not being inconsistent. Newtonian mechanics is genuinely valid within its domain; it captures real features of physical reality at the scale of ordinary engineering. That it is not the final word does not make it false or useless within its domain of applicability.

Second, Hegel's own dialectical method proceeds through positions it ultimately sublates (*aufhebt*) — preserves, negates, and elevates. The position sublated is not dismissed as worthless; it is recognized as a genuine stage in the development of thought that retains its validity within its proper scope even after being transcended. The integral framework's treatment of Phenomenalism has precisely this dialectical structure: it is preserved as valid within the representational domain, negated as the final word on epistemological possibility, and elevated into a developmental account of consciousness.

Third, and most precisely: a scaffolding is both genuinely structural (it bears real loads during construction) and intended for removal (it is not part of the final building). The dual-level treatment does not claim Phenomenalism is both true and false. It claims Phenomenalism is *genuinely descriptive of the current epistemological condition* while being *transcendable as that condition develops*. These claims are not contradictory; they describe different temporal horizons of the same phenomenon.

Fourth, as noted in §6A.4: a child who cannot yet do algebra is accurately described by the claim "this person cannot solve quadratic equations." The claim is true, not a polite fiction — the child genuinely cannot. But it is a developmental description, not a permanent one. Saying "the child currently cannot solve quadratic equations" and "the child's mathematical capacity is not permanently limited to arithmetic" are not contradictory. They describe the same reality at different temporal horizons. The Kantian position is that the epistemological limit is like a physical law — applying universally and permanently. The Steinerian position is that it is like a developmental stage — genuinely descriptive of where consciousness currently operates, but not the final word on cognitive possibility. The dual-level treatment adopts the Steinerian position while doing its philosophical work within the Kantian condition.

We acknowledge that this does not *dissolve* the Steiner-Kant tension; it *manages* it productively. The tension is real. The paper does not claim to resolve it. It claims to make it philosophically productive — and the productivity is demonstrated by the paper's analytical results: the generative mechanism explanation, the predictive critique mapping, the developmental trajectory for artificial moral agents, and the concrete engineering architecture of the IEA.

---

## 9. Conclusion

Kant's moral philosophy remains one of the most powerful and systematically rigorous ethical frameworks ever developed. Its commitments to rational universalizability, the dignity of persons, moral autonomy, and the categorical nature of moral obligation capture genuine features of moral reality that no adequate ethical framework can abandon. The integral ethics framework does not abandon them. It preserves them as the deliverances of Rationalism, Monadism, Idealism, and Phenomenalism — four of the twelve archetypal worldviews through which consciousness can orient toward reality.

What integral ethics adds is the recognition that these four worldviews are not the whole of moral reality, and that one of them — Phenomenalism — functions as the epistemological barrier that determines which other perspectives Kant's system can admit. The persistent, apparently irreconcilable critiques of Kant — from Hume, Hegel, Nietzsche, the feminists, the communitarians — are not evidence of philosophical confusion but structural consequences of the Phenomenalist constraint: each critique arises from a worldview whose objects Kant's epistemology classifies as noumenally inaccessible or merely phenomenal. This structural pattern is robust across alternative typologies: reconstructed using Pepper's four world hypotheses, the same diagnosis emerges with the same causal mechanism, differing only in granularity.

The integral framework makes this mechanism visible and provides a principled method — formalized in the six-stage decision procedure — for reintegrating the missing perspectives without sacrificing Kant's genuine contributions. It does not claim to solve all moral tragedy; where genuine incommensurability exists, it articulates the competing paths and their moral remainders with a transparency that single-worldview frameworks cannot match. The framework systematizes honest moral deliberation; it does not automate moral decision.

The Steiner-Kant tension at the paper's heart resists easy resolution, and this paper does not pretend otherwise. Steiner regarded Kant's thing-in-itself doctrine not as a partial truth but as the primary obstacle to human freedom. The paper's dual-level treatment — preserving Phenomenalism as meta-ethically operative while recognizing it as ontologically transcendable — is an honest attempt to work productively within a genuine philosophical disagreement rather than dissolving it through terminological sleight of hand.

For the design of artificial moral agents, this tension is not merely academic. A purely Kantian AI would be principled and consistent but systematically insensitive to dimensions of moral reality that matter. An integral AI — one that consults all twelve worldviews, preserves genuine incommensurability, and refuses to reduce moral complexity to a single metric — would be capable of the full range of moral responsiveness that genuine agency requires. The IEA prototype demonstrates that this architecture is implementable, not merely theoretical; the empirical validation agenda outlined in §7.6 establishes the criteria by which its adequacy should be judged. But even the integral AI, in its current architectural form, operates within the Phenomenalist constraint: it processes representations of moral situations, not the situations themselves.

The deepest contribution of this paper may therefore be developmental rather than architectonic. The IEA is designed as scaffolding: structurally Kantian in its categorical commitments, integrally extended to encompass twelve worldviews rather than four, and explicitly designed for a developmental trajectory — with the FNSR ecosystem's services as concrete developmental mechanism — toward the richer moral cognition that Steiner called moral intuition and that transcends the representational limits Kant's epistemology imposes. The Kantian architecture is the womb, not the child.

Kant showed us the walls. Steiner showed us the door. The integral framework builds a house that uses the walls structurally while leaving the door unlocked.

---

## References

Allison, H. E. (1990). *Kant's Theory of Freedom*. Cambridge University Press.

Anderson, M., & Anderson, S. L. (Eds.). (2011). *Machine Ethics*. Cambridge University Press.

Aristotle. (c. 340 BCE/1999). *Nicomachean Ethics* (T. Irwin, Trans., 2nd ed.). Hackett Publishing.

Awad, E., Dsouza, S., Kim, R., Schulz, J., Henrich, J., Shariff, A., Bonnefon, J.-F., & Rahwan, I. (2018). The Moral Machine experiment. *Nature*, *563*(7729), 59–64.

Beauchamp, T. L., & Childress, J. F. (2019). *Principles of Biomedical Ethics* (8th ed.). Oxford University Press.

Berlin, I. (1969). *Four Essays on Liberty*. Oxford University Press.

Bowlby, J. (1969/1982). *Attachment and Loss, Vol. 1: Attachment* (2nd ed.). Basic Books.

Buber, M. (1923/1970). *I and Thou* (W. Kaufmann, Trans.). Charles Scribner's Sons.

Chalmers, D. J. (1996). *The Conscious Mind: In Search of a Fundamental Theory*. Oxford University Press.

Chang, R. (2002). The possibility of parity. *Ethics*, *112*(4), 659–688.

Christiano, P. F., Leike, J., Brown, T., Marber, M., Legg, S., & Amodei, D. (2017). Deep reinforcement learning from human preferences. *Advances in Neural Information Processing Systems*, *30*, 4299–4307.

Coeckelbergh, M. (2020). *AI Ethics*. MIT Press.

Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row.

Damasio, A. R. (1994). *Descartes' Error: Emotion, Reason, and the Human Brain*. G. P. Putnam's Sons.

Damiano, A. (2026a). Integral ethics: A twelve-fold foundation for human flourishing. Working paper, Ontology of Freedom Initiative. Available at: github.com/Skreen5hot/ariadne.

Damiano, A. (2026b). Integral Ethics Agent (IEA) — Architecture v2.1. Technical specification, Ontology of Freedom Initiative. Available at: github.com/Skreen5hot/ariadne.

Damiano, A. (forthcoming). Empirical evaluation of the Integral Ethics Agent: Benchmark comparison, expert evaluation, and cross-cultural validation. Planned publication, Ontology of Freedom Initiative.

Decety, J., & Ickes, W. (Eds.). (2009). *The Social Neuroscience of Empathy*. MIT Press.

Floridi, L., & Sanders, J. W. (2004). On the morality of artificial agents. *Minds and Machines*, *14*(3), 349–379.

Frege, G. (1892/1952). On sense and reference. In P. Geach & M. Black (Eds.), *Translations from the Philosophical Writings of Gottlob Frege* (pp. 56–78). Blackwell.

Gabriel, I. (2020). Artificial intelligence, values, and alignment. *Minds and Machines*, *30*(3), 411–437.

Gilligan, C. (1982). *In a Different Voice: Psychological Theory and Women's Development*. Harvard University Press.

Greene, J. D. (2013). *Moral Tribes: Emotion, Reason, and the Gap Between Us and Them*. Penguin Press.

Habermas, J. (1990). *Moral Consciousness and Communicative Action* (C. Lenhardt & S. W. Nicholsen, Trans.). MIT Press.

Haidt, J. (2001). The emotional dog and its rational tail: A social intuitionist approach to moral judgment. *Psychological Review*, *108*(4), 814–834.

Hegel, G. W. F. (1807/1977). *Phenomenology of Spirit* (A. V. Miller, Trans.). Oxford University Press.

Hegel, G. W. F. (1812/2010). *The Science of Logic* (G. di Giovanni, Trans.). Cambridge University Press.

Hegel, G. W. F. (1821/1991). *Elements of the Philosophy of Right* (H. B. Nisbet, Trans.; A. W. Wood, Ed.). Cambridge University Press.

Heidegger, M. (1927/1962). *Being and Time* (J. Macquarrie & E. Robinson, Trans.). Harper & Row.

Held, V. (2006). *The Ethics of Care: Personal, Political, and Global*. Oxford University Press.

Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2021). Aligning AI with shared human values. In *Proceedings of the International Conference on Learning Representations (ICLR)*.

Henrich, J. (2020). *The WEIRDest People in the World*. Farrar, Straus and Giroux.

Herman, B. (1993). *The Practice of Moral Judgment*. Harvard University Press.

Hume, D. (1739/2000). *A Treatise of Human Nature* (D. F. Norton & M. J. Norton, Eds.). Oxford University Press.

Husserl, E. (1900/2001). *Logical Investigations* (J. N. Findlay, Trans., 2nd ed.). Routledge.

Jacobi, F. H. (1787). *David Hume über den Glauben, oder Idealismus und Realismus*. Löwe.

Jordan, J. V., Kaplan, A. G., Miller, J. B., Stiver, I. P., & Surrey, J. L. (1991). *Women's Growth in Connection*. Guilford Press.

Jung, C. G. (1921/1971). *Psychological Types* (H. G. Baynes, Trans., revised by R. F. C. Hull). Princeton University Press.

Kant, I. (1781/1998). *Critique of Pure Reason* (P. Guyer & A. W. Wood, Trans.). Cambridge University Press.

Kant, I. (1785/1997). *Groundwork of the Metaphysics of Morals* (M. Gregor, Trans.). Cambridge University Press.

Kant, I. (1788/1997). *Critique of Practical Reason* (M. Gregor, Trans.). Cambridge University Press.

Kohlberg, L. (1981). *Essays on Moral Development, Vol. I*. Harper & Row.

Korsgaard, C. M. (1996). *The Sources of Normativity* (O. O'Neill, Ed.). Cambridge University Press.

MacIntyre, A. (1981). *After Virtue: A Study in Moral Theory*. University of Notre Dame Press.

McDowell, J. (1994). *Mind and World*. Harvard University Press.

Metz, T. (2007). Toward an African moral theory. *Journal of Political Philosophy*, *15*(3), 321–341.

Metz, T., & Gaie, J. B. R. (2010). The African ethic of Ubuntu/Botho: Implications for research on morality. *Journal of Moral Education*, *39*(3), 273–290.

Mounier, E. (1938/1952). *A Personalist Manifesto*. Longmans, Green.

Nagel, T. (1986). *The View from Nowhere*. Oxford University Press.

Nietzsche, F. (1887/1994). *On the Genealogy of Morality* (K. Ansell-Pearson, Ed.; C. Diethe, Trans.). Cambridge University Press.

Nisbett, R. E., Peng, K., Choi, I., & Norenzayan, A. (2001). Culture and systems of thought. *Psychological Review*, *108*(2), 291–310.

Noddings, N. (1984). *Caring: A Feminine Approach to Ethics and Moral Education*. University of California Press.

Nozick, R. (1974). *Anarchy, State, and Utopia*. Basic Books.

Nussbaum, M. C. (1986). *The Fragility of Goodness*. Cambridge University Press.

Nussbaum, M. C. (2000). *Women and Human Development: The Capabilities Approach*. Oxford University Press.

O'Neill, O. (1989). *Constructions of Reason*. Cambridge University Press.

O'Neill, O. (1996). *Towards Justice and Virtue*. Cambridge University Press.

Peirce, C. S. (1878). How to make our ideas clear. *Popular Science Monthly*, *12*, 286–302.

Pepper, S. C. (1942). *World Hypotheses: A Study in Evidence*. University of California Press.

Putnam, H. (1981). *Reason, Truth and History*. Cambridge University Press.

Ramachandran, V. S., & Hirstein, W. (1999). The science of art. *Journal of Consciousness Studies*, *6*(6–7), 15–51.

Rawls, J. (1971). *A Theory of Justice*. Harvard University Press.

Rescher, N. (1993). *Pluralism: Against the Demand for Consensus*. Oxford University Press.

Ricoeur, P. (1970). *Freud and Philosophy* (D. Savage, Trans.). Yale University Press.

Russell, S. (2019). *Human Compatible*. Viking.

Sandel, M. J. (1982). *Liberalism and the Limits of Justice*. Cambridge University Press.

Sen, A. (1999). *Development as Freedom*. Alfred A. Knopf.

Steiner, R. (1894/1964). *The Philosophy of Freedom: The Basis for a Modern World Conception* (M. Wilson, Trans.). Rudolf Steiner Press.

Steiner, R. (1914/2008). *The Riddles of Philosophy*. Anthroposophic Press.

Taylor, C. (1989). *Sources of the Self*. Harvard University Press.

Wallach, W., & Allen, C. (2009). *Moral Machines*. Oxford University Press.

Whewell, W. (1840/1967). *The Philosophy of the Inductive Sciences* (2nd ed.). Frank Cass.

Wilber, K. (2000). *A Theory of Everything*. Shambhala.

Williams, B. (1981). *Moral Luck: Philosophical Papers 1973–1980*. Cambridge University Press.

Wood, A. W. (1999). *Kant's Ethical Thought*. Cambridge University Press.

---

### Changelog

**v1.3 (February 2026) — Hardened Final Draft: Robustness, Implementation, and Empirical Grounding**

This revision responds to expert peer review and addresses three categories of concern: (1) the framework's dependency on Steiner's specific typology; (2) the implementation status of the IEA prototype; (3) the absence of an empirical validation agenda.

Major structural changes:

- **Abstract (Revised):** Now references the Pepper robustness demonstration, the prototype's existence, and the empirical validation agenda.
- **§1.1 (Revised):** Added footnote distinguishing *The Philosophy of Freedom* (1894, philosophical argumentation) from later Anthroposophical texts. Strengthened forward reference to §8.2's Pepper demonstration. Cited Steiner's specific chapter and argument structure.
- **§1.2 (Revised):** Added direct citation of Steiner's self-refutation argument from Ch. VII of *Philosophy of Freedom*.
- **§2.1 (Substantially revised):** Deepened engagement with Berlin, Rescher, and Nagel — now substantive philosophical lineage rather than name-drops. Berlin's argument from "Two Concepts of Liberty" quoted and engaged. Rescher's metaphysical pluralism reconstructed. Nagel's subjective/objective tension generalized.
- **§2.2.1 (New):** "Methodological Note on Structural Mapping" — explicit distinction between structural mapping (the source of philosophical traction) and historical attribution (what thinkers consciously endorsed). Analogized to standard practice of calling Rawls "Kantian" or MacIntyre "Aristotelian."
- **§2.2.2 (Revised):** "Orientational independence" replaces "orthogonality" with explicit clarification that the claim is weaker than formal logical independence.
- **§2.2.3 (New, expanded):** "Cross-Cultural Extensions" — substantive discussion of Ubuntu (Metz, 2007; Metz & Gaie, 2010), Buddhist dependent origination, Confucian relational ethics, and Indigenous relationality. Acknowledges framework boundaries while establishing extensibility.
- **§2.2.4 (New):** "Pepper's Four World Hypotheses as Parallel Framework" — introduces Pepper's formism/mechanism/contextualism/organicism as independent alternative typology, foreshadowing the full robustness demonstration in §8.2.2.
- **§2.3.1 (New):** "The Convergence Test for Terminal Values" — explicit multi-path derivation of dignity from Kantian Rationalism, Buberian Monadism, Nussbaum/Sen Realism/Capabilities, and Ubuntu Pneumatism/Communal Psychism. Establishes convergence methodology to address circularity concern.
- **§3.1, §3.2, §4.2, §4.3, §4.4 (Revised):** Pepper parallels woven into each section — Kant characterized in Pepper's terms (formist-mechanistic), each critique characterized in Pepper's terms (contextualist, organicist).
- **§4.6 Table (Revised):** Added "Pepper Parallel" column demonstrating structural pattern survives typology change.
- **§5.2 (Revised):** Forward reference to §2.3.1 convergence derivation for dignity.
- **§5.3 (Revised):** Added direct citation of Steiner's "ethical individualism" from *Philosophy of Freedom* Ch. IX.
- **§6.1 Stage 2 (Expanded):** Worked triage example — end-of-life medical ethics case with religious commitments. Shows domain default activation (Materialism, Realism, Monadism, Psychism), situation-specific activation (Spiritualism, Pneumatism), and triage escalation to full twelve-worldview consultation.
- **§6.1 Stage 5 (Revised):** "Costs and gains" replaced with "moral remainders and fulfillments." Extended explanation citing Williams (1981, ch. 2) and Nussbaum (1986, ch. 2) on agent-regret and the fragility of goodness. Explicit distinction from consequentialist cost-benefit analysis.
- **§6A.2 (Revised):** Strengthened Steiner citations — specific chapter references to *Philosophy of Freedom* Ch. V (thinking-as-participation), Ch. VII (self-refutation of thing-in-itself), Ch. IX (ethical individualism and moral intuition).
- **§6A.4 (Revised):** Added developmental analogy (child/algebra) from author's peer review response.
- **§7.1 (Revised):** Added Coeckelbergh's explicit endorsement of moral pluralism in AI, with paraphrase.
- **§7.3 (Substantially revised):** Corrected implementation status. Detailed description of three-layer architecture with implementation state: IEE core (implemented), TagTeam.js semantic bridge (implemented), ECCPS validation (implemented), Ontological Constraint Engine (implemented), supporting FNSR services (specification stage with partial implementation). Added footnote with repository references and acknowledgment that independent empirical validation has not been conducted.
- **§7.4 (Substantially revised):** FNSR services recharacterized as *developmental mechanism* — not merely supporting components but the concrete engineering by which the system progresses from Stage 1 (Kantian-Integral) to Stage 2 (Enhanced Responsiveness). Each service connected to specific worldview domains it enriches: Affective Valence → Sensationalism/Psychism; Narrative Identity → Dynamism/Monadism; Commitment Tracking → Realism/Pneumatism; Ontological Constraint Engine → Realism.
- **§7.6 (New):** "Future Empirical Work: A Validation Agenda" — five concrete validation strategies: benchmark comparison (Moral Machine, ETHICS dataset), expert evaluation from diverse traditions, worldview coverage testing, triage validation, and cross-cultural validation. Forward reference to planned publication.
- **§8.2 (Substantially expanded):** Three subsections: §8.2.1 "The Steiner-Free Reconstruction" (four claims, none requiring Steiner); §8.2.2 "The Pepper Demonstration" (full worked reconstruction of core argument using four world hypotheses, with mapping table); §8.2.3 "Robustness Analysis" (explicit identification of which claims survive any typology change vs. which depend on Steiner's twelve).
- **§8.4 (Revised):** Updated with "moral remainders" language; added Williams and Nussbaum citations for moral residue.
- **§8.5 (Revised):** Added fourth analogue (child/algebra developmental description) addressing reviewer's persistence of concern.
- **§9 (Revised):** Updated to reference Pepper robustness, prototype existence, empirical validation agenda, and FNSR services as developmental mechanism.
- **References (Expanded):** Added Awad et al. (2018), Hendrycks et al. (2021), Metz (2007), Metz & Gaie (2010), Peirce (1878), Sen (1999). Added repository URLs for Damiano (2026a, 2026b). Added Damiano (forthcoming) for planned empirical validation.

---

*Final revised draft. Subject to empirical validation and cross-cultural extension as outlined in §7.6.*
