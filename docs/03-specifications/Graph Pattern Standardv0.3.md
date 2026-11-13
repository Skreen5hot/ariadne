SDD-GPS: Graph Pattern Standard for BFO/CCO Graphs — Draft v0.3
Nov 11, 2026 · @Aaron Damiano
1. Document control and lineage
SDD-GPS v0.3 is the final pre-ratification draft of the Graph Pattern Standard: the single authority for the RDF patterns that an accepted Semantic Data Dictionary and a normalized schema determine, written for the ratifying architect's review. It exists because the pattern-derivation audit of 2026-11-11 showed that the consuming services already assume patterns nobody owns, and that one obvious pattern is inconsistent under the pinned ontologies (§11, E-1).
Field
Value
Document id
SDD-GPS
Version
0.3, 2026-11-11. Lineage, all on 2026-11-11: v0.1-draft.1, the initial draft (an ICE per value, is tokenized by); v0.1-draft.2, the literal model realigned to native typed literals through attribute properties (V-3); v0.2, the ontologist's review of the v0.2 memorandum dispositioned (S-12), identity validation added (G-1.8), the aboutness target rule decided (Q-8); v0.3, the production-readiness review's bounded corrections (S-13). A version increments at each review cycle; a draft number at each amendment within one
Status
FINAL DRAFT: architectural approval granted by the production-readiness review (2026-11-11); normative ratification pending the ratifying architect and the §15 gates
Authority
Aaron Damiano, ratifying architect; authored by Claude under delegation per HIRI-RS-MSO
Normative language
BCP 14 keywords (MUST, MUST NOT, SHOULD, MAY), uppercase only
Stable identifiers
Patterns P-*, rules G-*, vocabulary decisions V-*, extensions X-*, witnesses W-G*, fixtures F-G*, seams and assumptions S-*, requests to other owners RQ-*, exceptions E-*, limits L-*, open questions Q-*. Minted once, never renumbered
Hash citation
Prose cites a governed file's sha256 by its first 8 hex characters; the full value appears once, in the §15 registry
Inputs, in order of authority.
1.  Minimum-Sufficient Symbolic Representation in BFO/CCO Knowledge Graphs, Final Development Review Draft v6.0, 2026-10-29: principles P1 to P12 and the Appendix B verification package. This standard is the pattern half of that package.
2.  The SDD Service specification v0.6 (spec/sdd-service.md), ADR-001 to ADR-010 and prop-005 revision 2: the SDD v2 contract (sddVersion 2), the permitted-term list a9e01756, and the Ontology-Template pin 7cfdfbf.
3.  SDD-PUB-ARCH v0.4.4 draft.2: the binding contract B-0 to B-7, whose rule B-6 requires every binding to cite a pattern id; projection.json.patterns; Annex A, the provisional catalogue this document replaces.
4.  The pinned closure: BFO 2020 (ISO/IEC 21838-2) and CCO v2.0-2024-11-06 exactly as Ontology-Template 7cfdfbf vendors them, with bfo-disjointness.ttl. Every CURIE in this document was checked against that pin and the SDD term list on 2026-11-11.
5.  The pattern-derivation audit of 2026-11-11 over the SDD full witness fixtures/witnesses/full/sdd.jsonld (57e14783): its findings are §11 and §13.
Place among the three documents. The split agreed on 2026-11-10 gives the method paper the principles, this standard the patterns, and SDD-PUB-ARCH the publication. Until a version of this standard is ratified, PUB-ARCH Annex A stands where the two disagree (PUB-ARCH names "GPS v0.1" as the trigger; RQ-PUB-3 reads it as the first ratified version); at that ratification Annex A is retired and the Milestone A release is rebuilt against this standard, as PUB-ARCH §3 and its limit L-26 already require. The RML service specification, not yet written, implements this standard and is bound by §13.
2. Purpose, scope and the three-document split
This standard fixes what the graph must look like: given an accepted SDD and the normalized schema it was built from, exactly which RDF quads an element of the source determines, under which IRIs, in which named graphs, and why each pattern is valid under the pinned closure. It is a data standard. It prescribes no execution order, no service and no file format of its own; the RML service produces what this standard describes, and the publication architecture consumes it.
What this standard governs.
• The core patterns (§6): the quads determined by each of the four SDD slot kinds (type, attribute, reference, containment) and by absence, for every source the SDD contract admits.
• The rules that close the gap between an SDD and a graph (§7): IRI minting, the record-to-referent relation, the attachment of a literal to an information content entity, the choice of the aboutness relation, and the named-graph envelope.
• The vocabulary decisions (§8) that the SDD deliberately leaves open (R-S9, NG-S1, NG-S6, ADR-007.1): which property carries a value, where absence is recorded, what a null iceClass becomes.
• The catalogue patterns (§9) that the method paper and PUB-ARCH Annex A require for symbolic entities, measurements, roles and processes, whether or not an SDD can produce them, so that projection.json.patterns has one hash to cite.
• The declared extensions (§10): patterns that need an SDD field v1 does not have, stated now so that the requests to the SDD registrar are concrete.
• The verification contract (§11, §12): the validity argument, the exception report the method paper's Appendix B asks for, the forbidden-entailment matrix and the witnesses.
What it leaves to others.
Concern
Owner
Where
Which classes and relations a source element maps to, and who accepted the mapping
SDD service
sdd-service.md, ADR-004
Normalized structure, element keys, source identities, datatypes, locators and joins
Schema service (the normalizer)
its contract, not yet written; prop-005 §1 states SDD's needs, §13 here states this standard's
Producing the quads, verifying that the SDD and the schema belong together, writing the source manifest and the loss report
RML service
its specification, not yet written; bound by §13
Projecting the graph into entries, evidence rows, indexes and releases
SDD-PUB-ARCH
v0.4.4 draft.2
Storage, lineage and revisions of every artifact
EPS
contract v0.2
Minimality, as this standard reads it. The method paper's rule governs every pattern here: use existing BFO and CCO categories and relations when their meanings are justified, preserve distinctions independently when they matter, and add representation only when it supplies information or reasoning capability an application needs (§4.3 there). A core pattern therefore carries the least structure that is valid under the pin and loses nothing the source stated; everything richer is a catalogue pattern or a declared extension with a stated justification.
Out of scope for v0.3. Identity of one referent across two sources; belief scopes and retraction; the SHML Middle Layer; star and snowflake sources (SDD NG-S2); OWL reasoning beyond the consistency and entailment checks of §11; any new ontology term (method paper P11).
Governing statement. The projection layer deterministically preserves source-local information and emits only the assertions the accepted SDD, the normalized schema and this standard authorize. Source-scoped identity is not global identity: a source occurrence is not thereby a distinct information content entity or a token, and a class is assigned only where its meaning and commitments are met. The projection layer performs no cross-record or cross-source entity resolution; source identity validation (G-1.8), join resolution (G-6), datatype validation (G-5) and graph consistency (§11) are distinct requirements that pipeline isolation never waives. Reconciliation after projection may establish canonical entities and identity judgments, but it preserves the source evidence, keeps occurrence, content and referent apart, and uses predicates that say what is asserted: owl:sameAs only for numerical identity, skos:exactMatch only between concepts, never either as a deduplication device. In four words: ingest deterministically, assert conservatively, resolve identity separately, preserve provenance throughout.
Behavior in plain terms, for engineers and users who need no BFO or CCO to read the graph:
• An asset tag identifies a computer: the tag is an identifier that designates the computer (G-4).
• A record says a computer weighs 10: the value is kept exactly as a typed literal on the record, and its unit is available from the schema and manifest; if the unit is not in the graph, the value is marked incomplete (incomplete:unit).
• Two records carry the same asset tag: nothing is merged; where the source says tags are unique, the extract is refused as an identity collision (G-1.8).
• A value is missing: nothing is invented; the absence is in the loss report (P-0).
• Two systems seem to describe the same computer: both are kept as their sources said; a later reconciliation step may relate them (§2).
The guiding rule: model what is known, preserve what the source says, use established ontology relationships where they fit, invent nothing, and add no complexity without a demonstrated need.
3. Inputs: what the standard assumes of an accepted SDD and a normalized schema
Two artifacts determine every pattern, joined by element key, and neither is sufficient alone. The SDD carries the meaning a person accepted: classes and relations. The normalized schema carries the structure the RML transformation runs on: element keys, source identities, the XSD datatype of every scalar attribute, locators, joins and nesting (ADR-010 A3, O1, O2). The source records are the third input, addressed only through the schema's locators. This section lists which fields each pattern reads from each artifact, so that the RML service's inputs and the Schema service's obligations are named rather than assumed.
From the SDD (sddVersion 2). Only accepted mappings determine patterns. A key listed in open or retired determines nothing: the RML service MUST report the element as unmapped in its loss report and MUST NOT project it (G-0).
Slot kind
Fields read
Guarantee relied on
type
key, recordClass, referentClass, source.externalId, source.name
recordClass is ICE-descended and referentClass is a permitted class (R-S5, R-S7)
attribute
key, iceClass or null, nullEquivalents, source.owner; datatype as the SDD recorded it, which must equal the schema's (G-9)
a non-null iceClass is ICE-descended; datatype is one of the eight R-S9 values and is the Schema service's, not a mapping choice (ADR-010 O1); nullEquivalents is the only declared null-equivalence (R-S5, R-S9, R-S15)
reference
key, relation, source.owner, source.target
relation is a permitted object property whose named domain and range admit the two referent classes, or the check was deferred with W-CHK-RANGE-UNRESOLVED (R-S7, R-S8)
containment
key, relation or sdd:NoRelation, source.child, source.container
as for a reference; sdd:NoRelation means no triple (R-S4, R-S8)
dictionary
absenceKinds, environment.termListSha256, environment.ontologyTemplateCommit, source.sha256, source.inventorySha256
the term list and the pin the patterns were checked against; the schema the SDD belongs to
From the normalized schema (prop-005 N1 to N9 and K1 to K4, plus the two obligations in §13). Until the Schema service exists, the SDD's stopgap Inventory supplies the same fields from a Jira Assets import schema.
Need
Field
Used by
Element keys, deterministic and unique within the source (K1 to K4)
key on every element
the join to the SDD; G-1
Source scope: the system and the extract the records come from
a source identifier the schema declares
G-1 minting, G-8 graph naming
Identity parts per type, in declared order (N6)
identity[], isIdentityPart
G-1: record and referent IRIs
Label attribute per type (N6)
label, isLabel
no pattern; retained for PUB-ARCH's label rule
Locators per attribute and reference (N9)
locators[]
which value a pattern reads
Reference join: which identity attribute of the target type a locator value resolves against (RQ-SCH-1)
not in the Inventory; objectMappingIQL is opaque to SDD v1 (NG-S3)
P-3
Containment join: the nesting of child records under container records (N7)
selectors[]
P-4
Record identity for every mapped type, even one with no identity parts (RQ-SCH-2)
to be declared by the Schema service
G-1
Multiplicity of a locator (RQ-SCH-3)
absent; v1 declares no cardinality (NG-S10)
P-2 mints one ICE per value, so a multi-valued locator is safe but must be read as a list
XSD datatype per scalar attribute, set by the Schema service (N4, O1); the SDD's copy must agree
datatype on every attribute element (the stopgap Inventory derives it from the Jira type by R-S9)
G-5: the literal's datatype; P-2
Other element metadata the schema declares: names, descriptions, external identifiers, parent
name, description, externalId, parent
no pattern; traceability in the loss report and the manifest, and PUB-ARCH's display vocabulary
From the source records. The values the locators address, each with the datatype the schema assigns; the source record identifier where the source has one; the extract's retrieval time, which goes into the source manifest and never into a quad (PUB-ARCH R-BLD-3). Record-level timestamps (created, updated, imported) are projected only when the source carries them as attributes the SDD mapped; nothing is synthesized.
Hierarchy. A type's parent is source hierarchy, never subclassing (R-S4). Records of a child type are typed by the child's own recordClass and referentClass alone. An attribute defined on an ancestor keeps one slot at its defining type; its values on a child's records follow that slot (G-3). The standard raises no error when a child's referentClass does not descend from its parent's; the RML service SHOULD warn (W-G-HIER), since the source's hierarchy and the ontology's may legitimately differ.
4. Pinned closure and term rules
Every term a pattern uses comes from one closure: BFO 2020 and CCO v2.0-2024-11-06 as Ontology-Template 7cfdfbf vendors them, together with bfo-disjointness.ttl. The SDD term list a9e01756 is the permitted subset the mapping choices were drawn from; the closure is what the patterns are verified against, disjointness axioms included, because that is where E-1 (§11) shows up.
Term rules.
• T-1. Every class, object property and annotation property in a pattern instance MUST be in the pinned closure by IRI. The only terms outside it are rdf:type, the XSD datatypes of R-S9, skos:notation in catalogue pattern P-12, and the attribute properties G-1.7 mints under the publication namespace, which are application properties outside the ontology, not new ontology terms.
• T-2. Two kinds of term occur: SDD-chosen terms, which an accepted mapping names (recordClass, referentClass, iceClass, relation), and pattern-fixed terms, which this standard names and no mapping can change (the table below). A pattern-fixed term is never offered to the LLM and never appears in a proposal.
• T-3. Choices this standard makes by ancestry (G-4) use named ancestry only, as the SDD does (NG-S9). Anonymous class expressions are not evaluated.
• T-4. No pattern asserts rdfs:label, owl:sameAs, rdfs:subClassOf or owl:equivalentClass on any minted individual or class. owl:differentFrom appears only where a source asserts distinctness, under PUB-ARCH's reserved-key rule.
• T-5. CCO's datatype properties (has text value and its ten siblings) are NOT used on information content entities: their pinned domain is Information Bearing Entity, which E-1 shows to be inconsistent with an ICE subject. They remain available to a pattern whose subject is an IBE. Nor is the annotation property is tokenized by used (V-3): attribute properties are source-faithful representations of what a field stated, serving a different purpose from a CCO token relation and not claimed equivalent to one; the core needs no token relation.
• T-6. Prefixes are the term list's: bfo: is http://purl.obolibrary.org/obo/, cco: is https://www.commoncoreontologies.org/. Literals carry the R-S9 datatype and no language tag unless the normalized schema declares one.
Pattern-fixed terms, each verified against the pin on 2026-11-11.
CURIE
Label
Kind
Named domain → range in the pin
Used by
cco:ont00001808
is about
object property
ICE → entity
G-2, G-4
cco:ont00001916
designates (⊑ is about)
object property
Designative ICE → (none)
G-4
cco:ont00001761
is tokenized by
annotation property
none declared
not used (V-3); listed because the method paper's §5 example and PUB-ARCH's tokens binding name it
bfo:BFO_0000176
continuant part of
object property
continuant → continuant
G-3
cco:ont00000958
Information Content Entity
class
⊑ generically dependent continuant
G-4 (a null iceClass)
cco:ont00000686
Designative Information Content Entity
class
⊑ ICE
G-4 (the ancestry test)
bfo:BFO_0000031
generically dependent continuant
class
disjoint with independent continuant (BFO_0000004) and with specifically dependent continuant (BFO_0000020)
§11
cco:ont00000253
Information Bearing Entity
class
⊑ object ⊑ material entity ⊑ independent continuant
E-1, E-2
bfo:BFO_0000197 / bfo:BFO_0000196
inheres in / bearer of
object properties
SDC → (none) / (none) → SDC
P-17
bfo:BFO_0000057 / bfo:BFO_0000056
has participant / participates in
object properties
process → (none) / (none) → process
P-18
bfo:BFO_0000055 / bfo:BFO_0000054
realizes / has realization
object properties
process → realizable entity / realizable entity → process
X-3
bfo:BFO_0000059 / bfo:BFO_0000058
concretizes / is concretized by
object properties
(none) → GDC / GDC → (none)
P-14
bfo:BFO_0000199
occupies temporal region
object property
(none) → temporal region
X-4
cco:ont00001966
is a measurement of
object property
Measurement ICE → (none)
P-16
cco:ont00001863
uses measurement unit
object property
Information Bearing Entity → Measurement Unit
E-2
cco:ont00001982
describes (⊑ is about)
object property
Descriptive ICE → (none)
V-2, rejected alternative
The inverses designated by (cco:ont00001879) and is subject of (cco:ont00001801) are not written by any pattern; PUB-ARCH materializes inverses under its entailment profile E-2.
5. Identity and IRI minting (G-1)
Every individual a pattern creates has an IRI computed from what identifies it in the source, so that two builds mint the same IRIs, a later extract keeps them, and nothing is ever identified by position or by chance. This satisfies PUB-ARCH R-DS-1 (no blank nodes) and R-DS-4 (every minted IRI under the namespace, ending in a lowercase UUID), which until now constrained a step nobody owned.
G-1. An IRI is <ns>id/<uuid>, where <ns> is the publication namespace PUB-ARCH §17 declares and <uuid> is a lowercase RFC 4122 version-5 UUID:
ns_uuid = uuid5(NAMESPACE_URL, <ns>)
uuid    = uuid5(ns_uuid, kind U+001F scope U+001F key U+001F identity)

kind      one of  record | referent | value | property | graph
scope     the source scope the normalized schema declares (system and extract lineage, not the extract time)
key       the element key: the type key for record and referent, the attribute key for value and property
identity  record, referent: the identity-part values in declared order, as a compact JSON array of strings,
                            or the source record identifier when the Schema service declares one (RQ-SCH-2)
          value:            record uuid U+001F datatype U+001F lexical form   (classified values only, P-2b)
          property:         empty   (one property per attribute slot, IRI <ns>p/<uuid>)
          graph:            the extract identifier (G-8)
G-1.1 Determinism. The same inputs mint the same IRIs on any machine. No counter, time, order or random value enters the string.
G-1.2 Stability. An identity whose parts are unchanged in a later extract keeps its IRI; an identity whose parts changed is a new individual, and the old one is absent from the new release. Identity values are used verbatim: no case folding, trimming or Unicode normalization, matching the SDD's own key rule (R-S2). A source that varies the spelling of an identifier between extracts therefore produces two individuals, and that is the correct, inspectable outcome; normalization is a Schema-service decision, never a pattern's.
G-1.3 Distinctness. The record and the referent of one source record differ in kind, so they never share an IRI (ADR-001). Two source records with the same name token are two records, two referents and two value ICEs (method paper P1); nothing in this standard merges them. A value ICE is minted per (record, attribute, datatype, lexical form): two records carrying the same value hold two ICEs, one record carrying one value twice holds one.
G-1.4 Composite and inherited identity. Identity parts are taken in the order the schema declares them; a part declared on an ancestor type counts for the child (the SDD Inventory already lists at:Hardware/Asset Tag as the identity of ot:Server). A record with any identity part absent has no identity: it is reported in the loss report as E-G-NOID and MUST NOT be projected. Projecting it under a guessed IRI would be an identity claim the source did not make.
G-1.5 Types without identity. A mapped type with no identity parts and no declared record identifier cannot be projected stably. The RML service MUST refuse the type with E-G-NOID rather than fall back to row order or a whole-record hash, both of which change IRIs when unrelated values change. RQ-SCH-2 asks the Schema service to guarantee a record identity for every mapped type; until it does, such a type is a declared loss. An unmapped abstract parent (the fixture's ot:Hardware, flagged FL-UNMAPPED-TYPE) has no records and raises nothing.
G-1.6 One referent per record. This standard mints one referent per source record. Whether two records, in one source or two, are about the same referent is an identity decision outside v0.1 (§2); when it is made, it is expressed by a declared pattern, never by minting the same IRI from different inputs.
G-1.7 Attribute properties. Every attribute slot mints one data property, <ns>p/<uuid5(property, scope, attribute key)>, the predicate that links a carrier to the typed literal the source stated for that attribute (G-5). It is an application property: it is declared in the release vocabulary with the attribute's name as its label and its source key as provenance, it carries no rdfs:domain, rdfs:range or other axiom, and it is not a term of the ontology (T-1). Records of a descendant type use the defining type's property (G-3). Two sources with an attribute of the same name have two properties, because the scope is part of the key.
G-1.8 Identity validation. Before an extract is promoted, the constructed identity string of every record (G-1, identity) MUST be unique within its type and scope. Two records with the same string are an identity collision, E-G-IDENTITY-COLLISION: the extract is refused, not one of the two records, since neither can be trusted. Precedence of identity inputs is the schema's to declare, one rule per type: a declared record identity (RQ-SCH-2) when the schema names one, else the identity parts in declared order; a type with both and no declared precedence is E-G-MAPPING. This is identity validation, which asks whether the source contract gave two records one key; it is not entity resolution, which asks whether two records describe one thing, and which never happens here (G-1.6). A row-local worker cannot prove uniqueness, so the check is a dataset-wide pass, like the joins of G-6; the RML service is stateless per record and validated per extract, never "row-isolated".
6. Core patterns P-0 to P-5
Five patterns cover everything an SDD v2 can say. Each is stated as the quads one source element determines, the condition under which it fires, and what happens when it cannot. rec, ref and val are the IRIs G-1 mints; g is the extract's graph (P-5).
Id
Fires for
Quads determined
When it cannot fire
P-0 Absence
an attribute or reference with no value, a value listed in the slot's nullEquivalents, or an empty string; a whitespace-only string is a value unless the slot lists it, since trimming is a transformation the contract did not authorize
none
never: absence is recorded in the loss report by kind (missing, explicit_null, empty_string, indistinguishable), never in a quad (ADR-003, R-S15)
P-1 Record and referent
every source record of a mapped type
rec a <recordClass> · ref a <referentClass> · rec cco:is_about ref
a record without identity (G-1.4, G-1.5): E-G-NOID, nothing projected
P-2 Attribute value
every value of a mapped attribute on a record of its owning type or a descendant
P-2a, plain (iceClass is null): rec <p_A> "lexical form"^^<datatype>, one quad, no individual. P-2b, classified (iceClass is a class): val a <iceClass> · val bfo:continuant_part_of rec · val <p_A> "lexical form"^^<datatype> · and, only when the schema marks the attribute as an identity part or the label of its type, val cco:designates ref (G-4); the record carries no literal for that value
a value that does not parse as its datatype: E-G-LEXICAL, the value is a loss, the record is still projected
P-3 Reference
every reference value that resolves to a target record under the declared join
ref(owner) <relation> ref(target)
no declared join (RQ-SCH-1) or no target record for the value: E-G-JOIN, the reference is a loss; never a guessed target
P-4 Containment
every child record nested under a container record
ref(child) <relation> ref(container), unless the relation is sdd:NoRelation
none: nesting is given by the schema's selectors
P-5 Source graph
every quad above
all quads of one extract in one named graph <ns>graph/<uuid>; the manifest beside the graph carries system, extract, retrieval time, SDD and schema hashes and this standard's version
never: there are no default-graph quads (PUB-ARCH R-DS-1)
What P-1 claims and does not claim. The record is an information content entity of the class the SDD chose, and it is about the referent; that is ADR-001 in two triples. The record is not the Jira object as a physical carrier (no bearer is minted, NG-S7) and the referent carries no literal (ADR-001). A child type's records are typed by the child's classes only; the parent's classes are never added (R-S4).
What P-2 claims. A plain value is a typed literal on the record, through the attribute's own property: the record stated it, the literal carries its XSD datatype natively, and no individual is minted to say so (P-2a). A classified value is an information content entity in its own right, typed by the class the person accepted, part of the record, carrying the same literal through the same property, and, when the schema marks the attribute as an identity part or the label, designating the referent (P-2b, G-4). Nothing stands between a carrier and its literal: no CCO value property, no is tokenized by, no bearer (V-3). A null iceClass therefore means exactly what R-S5 says, no specific classification, and costs one quad. An attribute defined on an ancestor fires on the descendant's records with the ancestor's slot and property (G-3). A multi-valued locator yields one literal, or one val, per value.
What a classified value ICE is, and is not. It is a source-scoped information item, identified by (record, attribute, value), carrying the one class the person accepted and the commitments that class brings, which P-2b makes explicit where the target is authorized (G-4). It is not a token occurrence, not a bearer and not a quality; those are representations for other needs (P-14, X-5). Nor is it a claim about any other record: that the same string appears in ten thousand records yields ten thousand source-scoped items, which is a statement about the sources, and whether they are one name is an identity judgment made after projection, if at all (G-1.6, §2). Its classification is justified by the accepted SDD mapping; its source-relative identity by this standard's projection contract; its relation to any reusable information entity is a downstream question.
What P-3 and P-4 claim. Exactly the relation the person accepted, between the two referents, and nothing about how the source arrived at it: no role, no act, no time. That is the whole of what an SDD v2 reference can say (§10, X-3, and L-2).
Worked example. Illustrative values on the synthetic fixture, with mapping choices a person might accept (the witness SDD itself maps every attribute to Descriptive ICE and means nothing by it). IRIs are abbreviated.
# record 'Finance' of ot:Organization, in graph <ns>graph/7c1e…
<ns>id/3f2a…  a cco:ont00000853 ;                    # recordClass: Descriptive ICE
               cco:ont00001808 <ns>id/9b04… .         # is about the referent
<ns>id/9b04…  a cco:ont00001180 .                    # referentClass: Organization

# at:Organization/Cost Center = "CC-410", iceClass null  (P-2a: one quad on the record)
<ns>id/3f2a…  <ns>p/61d0… "CC-410"^^xsd:string .      # the Cost Center attribute property

# at:Organization/Name = "Finance", iceClass cco:ont00001014 Proper Name, on the label attribute  (P-2b; G-4 authorizes designates)
<ns>id/c71d…  a cco:ont00001014 ;
               obo:BFO_0000176 <ns>id/3f2a… ;         # continuant part of the record
               <ns>p/2e8b… "Finance"^^xsd:string ;     # the Name attribute property
               cco:ont00001916 <ns>id/9b04… .         # designates the organization

# at:Person/Department on a Person record, relation cco:ont00001939 is affiliated with  (P-3)
<ns>id/5d20…  cco:ont00001939 <ns>id/9b04… .         # person referent -> organization referent

# ct:ot:Blade Server, relation obo:BFO_0000176 continuant part of  (P-4)
<ns>id/a8f3…  obo:BFO_0000176 <ns>id/4c6b… .         # blade referent -> server referent

# release vocabulary, outside the graph: <ns>p/61d0… label "Cost Center", source at:Organization/Cost Center
Nothing in the example is a label, a bearer, a role or a time, and nothing comes from a value the source did not state. What the method paper's scenarios add to this core is §9; what a richer source could say with three more SDD fields is §10.
7. Core rules G-0 to G-9
The rules are what an implementer builds and what a witness falsifies. Each names the witness in §12 that would catch a wrong implementation.
Id
Rule
Falsified by
G-0 Accepted mappings only
A pattern fires only from a mapping in mappings with an acceptance record. A key in open or retired MUST be reported as a loss (unmapped) and MUST NOT be projected, inferred from a sibling, or carried from an earlier SDD.
W-G2: an open key that yields any quad
G-1 Minting
IRIs as §5: <ns>id/<uuid5> over kind, scope, key and identity; no blank nodes; a record without identity is E-G-NOID and is not projected.
W-G5: two builds that differ in any IRI; a changed unrelated record that changes another record's IRI
G-2 Record aboutness
Every projected record yields exactly rec a <recordClass>, ref a <referentClass> and rec cco:is_about ref, and no other type assertion on either.
W-G2: a record typed with a parent type's class, or without is about
G-3 Value parthood and slot inheritance
Every classified value ICE (P-2b) yields val bfo:continuant_part_of rec; a plain value (P-2a) mints no individual. The slot and its attribute property are the ones at the attribute's defining type; records of descendant types fire them unchanged.
W-G2: a plain value minted as an individual; a value on a Server record projected under a slot or property other than at:Hardware/Asset Tag's
G-4 Aboutness by ancestry
For a classified value (P-2b): val cco:designates ref iff the schema marks the attribute as an identity part or the label of its type (isIdentityPart, isLabel) and the slot's iceClass is cco:ont00000686 or descends from it by named ancestry in the term list the SDD cites. An identity or label attribute whose iceClass is not Designative yields no target quad and the warning W-G-LABEL-CLASS: the schema says it identifies and the class says it does not. Every other classified value carries no target quad, because ancestry authorizes the class, not the target (V-2); an explicit target needs X-6. A plain value has no aboutness relation: the record it sits on is already about the referent (P-1). Authority: the rule draws on three accepted facts together, the schema's identity or label declaration, the person's Designative classification and the accepted type-to-referent mapping; an asset tag on an inventory record designates the computer, an employee number the person. Exceptions, where a source identifier designates the record itself or another entity, are settled by mapping governance, never by the engine: the person classifies the attribute non-Designative or leaves iceClass null (no target quad; W-G-LABEL-CLASS flags it for review), or names the target through X-6 once ratified.
W-G2: a Proper Name on the label attribute without designates; a Code Identifier on a non-identity attribute (the fixture's Cost Center) with any target quad; is about from a value ICE to a referent anywhere
G-5 Literal attachment
The value is written once, as a typed literal through the attribute's own property p_A (G-1.7): rec p_A "lexical form"^^<datatype> for a plain value, val p_A "lexical form"^^<datatype> for a classified one, with the schema's datatype (ADR-010 O1) and no language tag; time values are xsd:string (SDD Decision B). The lexical form is the source value verbatim after the null-equivalence test; leading zeros survive because the datatype is a string. A value that is not a valid lexical form of its datatype is E-G-LEXICAL: the value is a loss, the record stands. No CCO value property, no is tokenized by, no universal value predicate and no bearer stands between a carrier and its literal (T-5, V-3).
W-G2: a value carried by has text value, is tokenized by or any predicate other than its attribute property; a literal on a referent; W-G3: the has text value twin is inconsistent
G-6 Joins
P-3 fires only when the declared join resolves the locator value to exactly one target record; P-4 only on the schema's nesting. An unresolved or ambiguous join is E-G-JOIN, a loss, never a guessed target. sdd:NoRelation yields nothing. The relation IRI is written verbatim.
W-G2: a reference projected without a declared join; a value matching two targets projected to either
G-7 Determinism
The quad set, the loss report and the manifest are functions of (SDD, structure artifact, records). Output is canonical N-Quads: RDF 1.1 N-Quads with no blank nodes (G-1); every term in N-Triples canonical form, IRIs absolute in <>; literal lexical forms escaped only as \", \\, \n, \r, other characters U+0000 to U+001F and U+007F as \u with four uppercase hex digits, everything else raw UTF-8; xsd:string literals written without a datatype, every other literal with ^^<full datatype IRI>; language tags only when the schema declares them, lowercased; one space between terms,  . before the line end, LF line ends and a final LF; every quad with its graph term; duplicates removed; lines sorted by unsigned byte order of their UTF-8 bytes. The loss report and manifest are RFC 8785 JSON. The sha256 of the N-Quads bytes is the input to PUB-ARCH's dataset_hash (R-DS-3). No output carries a build time, a path or an environment value (PUB-ARCH R-BLD-3)
W-G5: two builds with different durations whose outputs differ
G-8 Graph envelope
Every quad of one extract is in one named graph <ns>graph/<uuid5(graph, scope, extract)>; there are no default-graph quads. The source manifest written beside the graph carries: system, extract identifier, retrieval time, the SDD's source.sha256 and the SDD file's sha256, the normalized schema's sha256, this standard's version and hash. Graph status (accepted-current, historical, candidate) is assigned by the publication pipeline, not here.
W-G2: a default-graph quad; a manifest missing a field
G-9 Pre-projection verification
Before any pattern fires, the RML service MUST verify, by these named hashes: sdd_sha256, the sha256 of the SDD file bytes the run cites; structure_sha256, the sha256 of the exact structure artifact bytes the run was given (the Jira import schema on the stopgap, the normalized schema after ADR-010), which MUST equal the SDD's source.sha256, in the format its source.format names; and, where the normalized schema declares the source it was normalized from, source_sha256, recorded but not compared with the SDD. It MUST then verify that every SDD key joins a structure key, that every attribute's SDD datatype equals the structure's (ADR-010 O1), and MUST re-run R-S5, R-S7 and R-S8 on every accepted mapping against the term list the SDD cites, including references whose range check was deferred (W-CHK-RANGE-UNRESOLVED). Any failure is E-G-MAPPING: the build stops and no pattern fires. The manifest records the three hashes under those names
W-G4: an SDD paired with the wrong schema; a reference whose deferred range check fails
Loss report. Every rule that withholds a quad writes a deterministic row: {code, key, record, kind} with code one of E-G-NOID, E-G-LEXICAL, E-G-JOIN, unmapped, or an absence kind from absenceKinds. A second code reports material semantic incompleteness rather than a withheld quad: incomplete:unit, for a numeric value, plain or classified, whose unit the source or the structure artifact states (a declared unit, or one the Schema service extracts from the attribute's definition, RQ-SCH-4) but the active profile does not carry in the graph. Completeness is judged from the unit information available, not from whether the iceClass is a Measurement ICE. Such a value is published with its unit available from the structure artifact and the manifest, and the publication layer MUST present it as incomplete, never as an unqualified authoritative measurement (RQ-PUB-5). The report is sorted by code, key and record, carries no time, and is the input PUB-ARCH's loss.json bounds (R-PC-9). It is the only place where "the source did not state A about R" is recorded (V-4).
8. Vocabulary decisions V-1 to V-7
These are the choices the SDD contract deliberately left open (R-S9, NG-S1, NG-S6, ADR-007.1) and that no consumer may make for itself. Each is a proposal until the ratifying architect's status changes it.
Id
Decision
Rejected alternatives
Reason
Reopen when
V-1 Value parthood
A classified value ICE is bfo:continuant_part_of its record (BFO_0000176, continuant to continuant; both are GDCs); a plain value is a literal on the record and needs no parthood
Linking the value to the referent only; is about from record to value; a CCO content-parthood relation
The content-parthood rule: a record is the information content of one source record, and the content of each field it states is a part of that content; this is what ADR-001 means by values being carried by the record's content, and the parthood is asserted on that rule, not on provenance alone. It is an explicit modeling convention: OC-1 must show it consistent under the pin, and provenance (which graph stated a quad) and parthood (which content is part of which) stay different relationships. Nothing more specific than BFO's continuant parthood exists in CCO for content parts, and the record must stay recoverable from a value ICE
CCO adds an information-parthood relation
V-2 Aboutness relation
designates ref for a classified value whose attribute the schema marks as an identity part or the label; no target quad for any other classified value; is about never by default. An explicit target or relation needs X-6
Inferring the target from ancestry alone (draft.1; withdrawn on the ontologist's review, Q-8); is about ref for every classified value; describes for Descriptive ICE; a relation chosen by the LLM
The schema's identity and label declarations are source facts: an attribute the source uses to identify or label the records of a type designates those records' referents, and a Designative class on it makes the designation explicit. Ancestry authorizes the class, not the target: a cost center code on an organization record is a Code Identifier of something other than the organization, and asserting otherwise would be a claim nobody made
X-6 is ratified (an explicit target per attribute), or the Schema service declares designata for attributes
V-3 Literal attachment
A native RDF typed literal, carried by one application property per source attribute (G-1.7): on the record for a plain value, on the ICE for a classified one. No CCO value property, no is tokenized by, no universal value predicate, no bearer
CCO's has text value and siblings (E-1: pinned domain Information Bearing Entity, inconsistent with an ICE subject); is tokenized by (a CCO token relation the core does not need; attribute properties serve a different purpose, source-faithful representation, and are not offered as its equivalent); rdf:value (NG-S6); an ICE individual per plain value (three quads to say "no classification"); an IBE per value (the over-materialization the method paper warns against, NG-S7)
RDF 1.1 literals carry their datatype natively; the attribute property names what the source stated and where it came from; the method paper's §4.1 allows ordinary values to be plain annotations and reserves ICE structure for independently identified names and identifiers; CCO's newer source vocabulary deprecates has text value. Conformance to CCO's value chain is not a goal of this architecture; minimum sufficiency is
A consumer requires CCO-conformant value chains, which would be a declared extension, never a change to the core
V-4 Absence
No quad. The loss report is the record of what a source did not state; an RDF form exists only as extension X-5
iao:information_gap individuals (rejected by ADR-003); placeholders; negated assertions; a "not stated" annotation on the record
Positing anything is itself an assertion (ADR-003 rule 1); CCO has no property for it (E-3); the publication layer reads absence from the loss report
A consumer needs absence in RDF at the edge
V-5 Record identifiers
Not materialized as ICE individuals; the record IRI is minted from them (G-1) and the source manifest carries them
A Code Identifier ICE designating each record
Three quads per record for no competency question; PUB-ARCH's evidence rows already carry the source record through sources.json
A competency question asks for the identifier as a graph entity
V-6 null iceClass
No individual: the value is a typed literal on the record through its attribute property (P-2a)
A generic cco:ont00000958 individual per value; Descriptive ICE; omitting the value
The person declined a specific classification; an individual typed only as ICE would assert a distinction the person did not draw, at three quads per value; the literal on the record states exactly what the source stated
Never: this is the meaning R-S5 gives null
V-7 Graph status
Assigned by the publication pipeline per source graph; never inferred from data
Reading historical from a status column or a boolean; per-triple status
A status column is a value the source stated about the referent (P-2), not a statement about the source's authority; status is scoped to a graph and a time (method paper P6, P8)
PUB-ARCH changes its source model
Consequence of V-3 for consumers. The graph reads as Entity → meaningful property → typed literal, and, where a classification is justified, ICE → attribute property → typed literal with designates or is about carrying the meaning. Neither the attribute properties nor the literals carry OWL semantics, which is correct: the class of a classified ICE and its aboutness relation do. PUB-ARCH's designator index therefore reads tokens from the attribute properties of classified ICEs rather than from is tokenized by; its tokens binding must become a binding over those properties, by alias group or per property (RQ-PUB-4). The datatype on the literal distinguishes a name from a date without a second predicate.
9. Catalogue patterns P-10 to P-18
The catalogue holds the shapes the method paper's scenarios and PUB-ARCH's Milestone A fixtures require, so that projection.json.patterns cites one standard whether a graph came through an SDD or was authored for a registry. Each shape is transcribed from the method paper v6.0 and Annex A with its terms re-verified against the pin; none is ratified until its Appendix B package exists (§12, W-G6). The derivable column says whether the core (§6) produces the shape from an SDD v2 without help.
Id
Shape (quads)
Source
Derivable from an SDD
PUB-ARCH fixture
P-10 Designation
d a <Designative ICE subclass> · d <p_A> "tok"^^xsd:string · d cco:designates x
method §5
yes: P-2b with a Designative iceClass on an identity or label attribute (G-4)
F-1
P-11 One designator, several tokens
d <p_A> "S.N.L."^^xsd:string, "SNL"^^xsd:string on one d
method §5
no: G-1.3 mints one ICE per value; that two values are one designator is a claim an SDD cannot make (X-7)
F-2
P-12 Reserved symbolic pattern
p a bfo:BFO_0000031 · p skos:notation "QZX-41" · a registry record r a <ICE> · r cco:is_about p; p is never typed as an ICE (method P2)
method §6.1
partly: a type whose referentClass is bfo:BFO_0000031 yields r is_about p; the notation on p is the catalogue form PUB-ARCH binds, while an SDD source yields a value ICE about p instead. Both are valid; a release declares which it uses
F-3
P-13 Subsequent assignment
c a cco:ont00000077 · c <p_A> "QZX-41"^^xsd:string · c cco:designates device; p unchanged; nothing identifies c with p
method §6.2
yes: P-2b on the device's type when the identifier attribute is an identity part and its iceClass is Code Identifier
F-4
P-14 Inscription and concretization
q a bfo:BFO_0000019 · q bfo:inheres_in doc · q bfo:concretizes p · ir a <ICE> · ir cco:is_about q
method §7
no: needs a quality individual the source does not record as a type
F-5
P-15 Referential reassignment
two d cco:designates x1 / d cco:designates x2 quads in two graphs whose statuses differ; no status on either triple
method P6, P8
partly: the core keeps each extract's assignments in its own graph with its provenance (G-8), and the pipeline assigns status (V-7). That one persistent designator changed referents is a historical interpretation needing assignment-history evidence or enrichment; the core does not establish it, and never decides whether two historically related identifiers are numerically identical
F-6
P-16 Measurement
m a cco:ont00001163 (or a subclass) · m cco:ont00001966 x · m <p_A> "10.0"^^xsd:decimal; the unit is open (E-2)
method §10
partly: P-2 with a Measurement iceClass gives everything but the unit (X-2)
F-8
P-17 Role from a record type
r a <class ⊑ bfo:BFO_0000023> · r bfo:inheres_in b
BFO
yes: a type whose referentClass is a role class, with a reference mapped inheres in to the bearer's type; R-S8 enforces the SDC domain
Milestone B sample
P-18 Process from a record type
p a <class ⊑ bfo:BFO_0000015> · p bfo:has_participant x
BFO
yes: the fixture's ot:Scan Event (Act of Observation) with has participant references; temporal regions need X-4
Milestone B sample
Two shapes the core cannot reach, and why that is correct. P-11 and P-14 both assert something about the relation between two pieces of information (two tokens are one designator; a quality concretizes a pattern) that no column of a source states. The core never asserts what the source did not state, so these shapes come only from a declared extension or from an authored fixture. P-16's gap is different: the source states the unit, in a description, and the SDD has no field to carry it (§10, X-2).
Terms used in P-12. skos:notation is the one term outside the closure (T-1), kept because Annex A already uses it and the method paper calls it an annotation-level convenience, not a classification. A pattern individual p is a generically dependent continuant and nothing more specific unless a source says so (P2).
10. Declared extensions X-1 to X-7
An extension is a pattern that needs a field the SDD v2 contract does not have. Each is stated here so that the request to the SDD registrar is a concrete field with a concrete check, not a wish; none changes the core, and a release that declares no extension projects exactly §6. The audit counted where each would have applied on the synthetic fixture.
Id
Adds
SDD field it needs (request)
Pattern when declared
Status
X-1 Value meaning
Realist meaning for boolean and select values (3 of 35 attributes in the fixture: Active, Encrypted, Status)
RQ-SDD-1: valueMeanings on an attribute slot, one entry per lexical value: {value, kind: class | none, term}; the checker verifies term ⊑ bfo:BFO_0000020 (an SDC class), and none means the value asserts nothing (ADR-003 rule 5)
k a <term> · k bfo:inheres_in ref, minted per (record, attribute, value), in addition to the core P-2 value; never a negated triple
Requested
X-2 Units
A unit and quantity kind for numeric values (4 in the fixture: cost, capacity, latitude, longitude)
RQ-SDD-2: unit on an attribute slot, a Measurement Unit individual from the pin; the checker verifies it is an instance of cco:ont00000120
m a <Measurement ICE subclass> · m cco:ont00001966 x · the unit edge is open: uses measurement unit has domain Information Bearing Entity in the pin (E-2)
Blocked by E-2; candidates in §11
X-3 Role or act behind a reference
The role, act and participants a foreign key stands for (all 5 references in the fixture)
RQ-SDD-3: elaboration on a reference slot: {roleClass, bearer: owner | target, actClass?}; the checker verifies roleClass ⊑ bfo:BFO_0000023 and actClass ⊑ bfo:BFO_0000015
r a <roleClass> · r bfo:inheres_in <bearer> · with an act: a a <actClass> · a bfo:realizes r · a bfo:has_participant <the other referent>, in addition to the core P-3 relation
Requested
X-4 Temporal regions
A temporal region for a process-referent type whose date attributes bound it (5 date or time attributes in the fixture)
RQ-SDD-4: temporalRole: start | end | instant on a date or dateTime attribute of a type whose referentClass ⊑ bfo:BFO_0000015
p bfo:occupies_temporal_region t · t a bfo:BFO_0000203 or bfo:BFO_0000038 · the date value stays where P-2 put it (on the record, or on its ICE), and that carrier cco:is_about t; a region bears no literal
Requested; optional by method P10
X-5 Absence in RDF
A record-level statement that attribute A was not stated
none in the SDD; a term CCO lacks (E-3)
not defined
Blocked by E-3; the loss report is the record (V-4)
X-6 Explicit aboutness
An explicit target for a classified attribute: suppressing G-4's default, or naming a target other than the record's referent (a cost center code on an organization record designates the cost center)
RQ-SDD-5: a target-selection field on the attribute slot: referent, none, or a resolvable target given as a target type key plus the identity attribute of that type the value matches (a join, as RQ-SCH-1); optionally relation, an object property ⊑ cco:ont00001808 whose named domain the iceClass satisfies. The checker verifies the target type, the identity attribute and the relation
val <relation, or designates for a Designative class> <the resolved target's referent>; none writes no target quad; an unresolved target is E-G-JOIN
Future extension, unratified; it needs the target-selection mechanism above and does not delay the core release. G-4 remains the core default
X-7 Token sets
Several lexical values that are tokens of one designator (P-11)
RQ-SDD-6: tokenSet: true on a multi-valued Designative attribute
one val per record with several literals through the attribute property, minted over the sorted set of lexical forms
Requested
Order of value. X-1 and X-3 change what a graph means for its consumers; X-2 is blocked on an upstream defect; X-4, X-6 and X-7 refine. The SDD registrar decides which, if any, enter SDD v1.x; this standard carries them as declared, unratified extensions until then, and W-G2 covers none of them.
11. Validity argument, exception report and forbidden entailments
Claim. For an SDD every accepted mapping of which passes R-S5, R-S7 and R-S8 (re-run under G-9), and a normalized schema that supplies identity and joins, every quad the core produces satisfies the named domain and range of its property under the pinned closure, and the quad set is consistent with the closure's disjointness axioms. The argument goes pattern by pattern.
• P-1. is about has domain ICE and range entity; recordClass is ICE-descended (R-S5). The record and the referent are distinct IRIs (G-1.3), so their classes never meet on one individual.
• P-2a. An attribute property is an application property outside the closure with no domain, range or other axiom (G-1.7), so a typed literal through it entails nothing about its carrier; the carrier is the record, never the referent (PC-1).
• P-2b. continuant part of has domain and range continuant; a value ICE and a record are both ICE-descended, ICE is a GDC, and a GDC is a continuant. designates has domain Designative ICE and is written only for a Designative iceClass on an identity or label attribute (G-4); no other target quad exists, so no other domain can be violated. The literal rides on the attribute property as in P-2a. A value ICE carries exactly one class assertion, so no disjointness axiom can fire on it.
• P-3 and P-4. The relation's named domain and range admit the two referent classes: that is R-S8, and G-9 closes the batch-deferred cases.
• P-5. A graph name carries no semantics.
What the argument does not cover, and the reasoner run (W-G3) does: that each referentClass is satisfiable in the closure, and anonymous domain and range expressions, which neither the SDD nor this standard evaluates (NG-S9, T-3).
Exception report (method paper Appendix B, item 7: where existing vocabulary is insufficient). Each entry was established by reading the pinned files on 2026-11-11.
Id
Finding
Consequence here
Disposition
E-1
CCO 2.0 declares rdfs:domain cco:ont00000253 (Information Bearing Entity) on has text value, has integer value, has double value, has decimal value, has boolean value, has date value, has datetime value and has URI value (CommonCoreOntologiesMerged.ttl, lines 3066 to 3138). An IBE is an object, hence a material entity, hence an independent continuant, which bfo-disjointness.ttl makes disjoint with generically dependent continuant; an ICE is a GDC. A value ICE carrying any of these properties is therefore entailed to be both, and the graph is inconsistent
The datatype-property form of G-5 is rejected; V-3 adopts native typed literals through attribute properties. The SDD term list carries no domain for datatype properties, so no SDD check could have caught this (RQ-SDD-7)
Report upstream to the CCO maintainers; the registrar decides whether SDD files it or Ontology-Template does
E-2
uses measurement unit (cco:ont00001863) has the same domain, Information Bearing Entity, so a Measurement ICE cannot name its unit consistently
X-2 is blocked. Candidates: attach the unit through an IBE carrier (a bearer per measurement, the over-materialization the method paper warns against); import a pinned unit vocabulary such as QUDT and use its unit relation at annotation level (a closure extension, a registrar decision); wait for an upstream correction
Registrar decision needed before X-2
E-3
Neither BFO nor CCO has a property by which a record states that it did not state something
V-4: absence lives in the loss report; X-5 undefined
None in v0.1
E-4
Attribute properties are application properties outside the ontology, and is tokenized by, had it been used, is an annotation property: in either design a literal carries no OWL semantics
By design (method P5, V-3): a question about values or tokens is answered by SPARQL, SHACL or PUB-ARCH's indexes over the literal, never by reasoning; the class of a classified ICE and its aboutness relation are where reasoning applies
None
E-5
BFO 2020's OWL as pinned omits most first-order axioms: no transitivity of continuant parthood, no chains, inherence not functional (PUB-ARCH L-21)
A chain of P-4 quads is reachability, not parthood at a time (PUB-ARCH L-27)
None
E-6
located in (bfo:BFO_0000171), is affiliated with (cco:ont00001939), bearer of and others carry no named domain or range, so R-S8 admits any pair of referents for them
The validity argument gives no protection there beyond W-G3; the person's acceptance is the only guard
Record in the SDD prompt rules (RQ-SDD-8: say which relations are unconstrained)
Verification categories. Three independently defined categories, each with its own tests; all three must pass (W-G3, W-G4). They are never mixed: a correct OWL inference is not a projection failure merely because GPS did not generate it, and the subclass axioms of the imported ontologies are not output. These checks replace FE-1 to FE-10 of v0.2.
Id
Category
Check
Guards
Replaces
PC-1
A. Projection conformance (asserted output only)
no literal, by any property, on a referent
ADR-001, G-5
FE-3
PC-2
A
each projected record asserts exactly rec a <recordClass>, ref a <referentClass> and rec cco:is_about ref; no other asserted rdf:type on either. Supertypes a reasoner infers are correct and not checked here
G-2
FE-2, FE-9
PC-3
A
the output asserts no class or property axiom (rdfs:subClassOf, owl:equivalentClass, owl:disjointWith, domain, range), in particular none read off the source hierarchy
R-S4, T-4
FE-4
PC-4
A
no quad from an open, retired or sdd:NoRelation slot; no quad for an absent, null-equivalent or empty value
G-0, G-6, P-0
FE-5, FE-6
PC-5
A
no CCO value property, no is tokenized by, no owl:sameAs and no universal value predicate in the output
V-3, T-4
FE-1 (asserted half)
PC-6
A
designates only where G-4 authorizes it; no is about from a value ICE
G-4
new
OC-1
B. Ontological consistency (output with the pinned closure and bfo-disjointness.ttl, under the pinned reasoner)
consistent; every class the output uses is satisfiable
§11 claim
new
OC-2
B
no record or value ICE is entailed to be an Information Bearing Entity or an independent continuant (the E-1 test); the datatype-property twin is inconsistent
V-3, E-1
FE-8
OC-3
B
no owl:sameAs is entailed between two distinct minted IRIs
G-1.3
FE-1 (entailed half)
OC-4
B
expected classifications are entailed: every record and value ICE is a generically dependent continuant; every referent has its referentClass and its named ancestors
P-1, P-2b
new
DC-1
C. Dataset conformance
every quad is in the extract's named graph; the manifest carries every G-8 field
G-8
FE-10
DC-2
C
constructed identity strings are unique per type and scope
G-1.8
new
DC-3
C
two records with equal values never share a value ICE or a referent
G-1.3
FE-7
DC-4
C
two builds give byte-identical canonical N-Quads, loss reports and manifests
G-1, G-7
new
DC-5
C
every withheld quad has exactly one loss-report row with its code, and no row lacks a cause
§7 loss report
new
12. Witnesses W-G1 to W-G6 and fixtures
A rule without a witness is a wish. The witnesses below are judged by a generator written from this text and never from an implementation, as the SDD's run-witnesses.mjs is; the derivation script of 2026-11-11 is that generator's seed, re-pinned once G-5 changed. Every expected file is canonical bytes with its sha256 in the §15 registry at ratification.
Fixtures.
Id
File
Content
F-G1
the SDD full witness fixtures/witnesses/full/sdd.jsonld (57e14783) with its inventory (1db35f4f)
52 accepted mappings over the synthetic IT asset register: 10 types, 35 attributes, 5 references, 2 containments; every attribute mapped to Descriptive ICE, so it exercises structure, not meaning
F-G2
fixtures/gps/sdd-meaningful.jsonld, to be produced through the SDD CLI from a hand-written validated proposal and accepted by the registrar
the same 52 keys with choices that exercise every G-4 branch: Proper Name and Code Identifier (Designative), a Measurement ICE, several null, one reference per relation kind, one sdd:NoRelation containment
F-G3
fixtures/gps/records.json, synthetic source records for the fixture schema
at least: 2 Organizations; 3 Persons, one whose Manager value resolves to no record, one with an empty Email, one missing Start Date; 2 Servers, one with a nested Blade Server and 2 Hard Drives; 1 Software installed on a Server; 1 Scan Event; every R-S9 datatype; a declared null-equivalent (N/A); an explicit null; two records sharing one token; a value that is not a valid xsd:date; a record missing an identity part
F-G4
fixtures/gps/catalogue/P-1x.ttl, one per catalogue pattern
authored graphs for P-10 to P-18; PUB-ARCH F-1 to F-8 supply P-10 to P-16
Witnesses.
Id
Scenario
Required result
Rules
W-G1 Derivation table
F-G1 through the generator, no records
one row per mapping with its pattern id and quad schema: 10 P-1, 35 P-2 (P-2a or P-2b by iceClass), 5 P-3, 2 P-4, and 35 attribute properties; no object-property domain or range violation; the flags exactly as §13's audit lists them, with G-JOIN on all 5 references until RQ-SCH-1 is met and G-NOID only on the unmapped parent ot:Hardware
G-0 to G-6
W-G2 Expected quads
F-G2 and F-G3 through the generator
expected.nq, canonical sorted N-Quads, byte-identical from any implementation; it contains every P-1 to P-5 instance the records determine, each plain value as one literal on its record and each classified value as an ICE, and nothing for the unresolvable Manager, the empty Email, the missing Start Date, the N/A, the explicit null, the NoRelation containment and the identity-less record; the loss report lists each with its code; the two records sharing a token hold two literals, or two ICEs when classified, never one
G-0 to G-8, P-0 to P-5, V-1 to V-6
W-G3 Consistency
the closure with bfo-disjointness.ttl plus expected.nq, under the reasoner PUB-ARCH pins (Q-18)
OC-1 to OC-4 hold under the reasoner PUB-ARCH pins (Q-18). The negative twin expected-datatype-form.nq, identical but with values carried by has text value and siblings, is inconsistent: the proof of E-1
G-5, V-3, E-1
W-G4 Forbidden entailments and refusals
the entailed closure of expected.nq; an SDD paired with another schema; a reference whose deferred range check fails against the final SDD
PC-1 to PC-6 hold over the asserted output and DC-1 to DC-3 and DC-5 over the dataset; an SDD paired with another structure artifact, a mismatched datatype and a reference whose deferred range check fails each stop the build with E-G-MAPPING and no quad written; a correct OWL inference is never counted as a failure
§11, G-9
W-G5 Determinism and stability
two builds of W-G2 with deliberately different durations; then F-G3 with one unrelated value changed; then F-G3 with one identity value changed
identical bytes (DC-4); for the unrelated value, only its literal changes, and an IRI changes only if the value is classified (its ICE); for the identity value, the changed record's record, referent and value IRIs change, quads that pointed at the old referent from other records (P-3, P-4) change with the join or become E-G-JOIN losses, and nothing else changes
G-1, G-7
W-G6 Catalogue packages
each F-G4 graph with its expected assertions and its forbidden entailments
consistent under the reasoner, expected assertions entailed, forbidden ones not; one package per catalogue pattern, the method paper's Appendix B
P-10 to P-18
What the witnesses do not prove. That a mapping means the right thing (ADR-004: only the person establishes meaning), that a referentClass is the right class, or that the source is complete. They prove that whatever the person accepted is projected exactly, validly and reproducibly, and that nothing else is.
13. Seams and assumption register; requests to other owners
Each row is a place where one service assumed something of another with nothing written down. The register says what this standard resolves, what it hands to an owner, and which witness or decision discharges it. Nothing here is closed until the discharging item exists.
Id
Assumption and where it lived
Resolution
Owner
Discharged by
S-1 Token property
PUB-ARCH binds tokens to is tokenized by and the method paper's P5 names it; the SDD term list marks annotation properties not permitted; the obvious RML rule used CCO datatype properties
V-3: a native typed literal through one application property per attribute; neither CCO's value properties (E-1) nor is tokenized by is used; the SDD exclusion of annotation properties governs mapping choices and is untouched; PUB-ARCH's tokens binding moves to the attribute properties of classified ICEs (RQ-PUB-4)
GPS
W-G3
S-2 Roles and processes
PUB-ARCH's rooting rules, bearers index and Milestone B sample assume role and process individuals with inherence and participation anchors
P-17 and P-18 when the source has record types for them; X-3 for roles behind foreign keys; the Milestone B sample is not SDD-derived, so PUB-ARCH must tolerate a graph with no roles
PUB-ARCH
RQ-PUB-1
S-3 Source model
PUB-ARCH consumes one named graph per source with a status and retrieved; nothing upstream emits them
G-8 writes the graph and the manifest; V-7 leaves status to the pipeline; the manifest is the input to PUB-ARCH's sources.json, whose retrieved the R-BLD-3 amendment permits
RML service
RQ-RML-1
S-4 Identity
PUB-ARCH's R-DS-1 and R-DS-4 constrain IRIs nobody minted
G-1
PUB-ARCH confirms the form <ns>id/<uuid> fits its namespace rule
RQ-PUB-2
S-5 Joins and record identity
Reference resolution is opaque IQL (NG-S3); a type may have no identity parts; multiplicity is undeclared (NG-S10)
G-6 refuses to guess; G-1.5 refuses to project
Schema service
RQ-SCH-1, RQ-SCH-2, RQ-SCH-3
S-6 Pattern ids
Binding rule B-6 requires a pattern id per binding; Annex A is provisional
The P-* identifiers here; projection.json.patterns.standard: "sdd-gps" with this document's hash; Annex A retires at ratification
PUB-ARCH
RQ-PUB-3
S-7 Pairing check
prop-005 §2 assigns RML the check that an SDD and a normalized schema belong together, in a spec RML does not have
G-9
RML service
RQ-RML-2, W-G4
S-8 Term-list coverage
The SDD term list carries no domain or range for datatype and annotation properties, so E-1 was invisible to every SDD check
GPS verification reads the pinned files directly (as the audit did) until the list carries them
SDD
RQ-SDD-7
S-9 Canonical output
PUB-ARCH's dataset_hash (R-DS-3) assumes sorted canonical N-Quads from upstream
G-7
RML service
RQ-RML-3, W-G5
S-10 Time values
SDD Decision B writes time as xsd:string; PUB-ARCH's temporal facet (CQ-5) cannot read it as a time
Declared limit L-4
GPS
none; reopen with X-4
S-11 Datatype authority
SDD v1 derives an attribute's XSD datatype from the Jira type (R-S9) and records it in the SDD; ADR-010 O1 moves that authority to the Schema service, and the literal patterns need one source of truth
G-5 reads the schema's datatype; G-9 refuses an SDD whose recorded datatype differs
Schema service, SDD
W-G4 (a mismatched datatype stops the build)
S-12 Ontologist's review of the v0.2 memorandum (2026-11-11)
Four corrections and six issues raised against a memorandum proposing an ingestion/reconciliation split: A (an occurrence is not automatically an ICE), B (no literals on referents), C (whitespace is not absence), D (no owl:sameAs for deduplication); parthood, IRI collisions, streaming joins, units, pairing, verification levels
B, C and D were already this standard's position (PC-1, P-0, PC-5, §2); A's terminology is adopted in §6 and its minting objection declined (V-1, G-1.3); identity validation added as G-1.8; pairing clarified in G-9; verification levels stated in §11; incomplete measurements reported in the loss report; the aboutness target of classified values is decided under Q-8: identity and label attributes designate the referent, nothing else by default
GPS; the ratifying architect on Q-8
W-G2, W-G4, W-G5; the Q-8 decision
S-13 Production-readiness review of v0.2 (2026-11-11)
Conditional approval for implementation; G-4 objection withdrawn; four bounded corrections: verification categories, P-15 scope, X-6 accuracy, cross-contract consistency (T-5, V-3, E-1, G-7, G-9, W-G5); unit completeness judged from available unit information
All made in v0.3: §11 verification categories PC/OC/DC replace FE-1 to FE-10; P-15 partly derivable; X-6 target selection; T-5, V-3, E-1 wording; G-7 canonical N-Quads; G-9 named hashes; W-G5 dependent changes; loss report incomplete:unit; settled decisions, core release requirements and deferrals in §15
GPS
W-G1 to W-G5 at implementation
Requests to other owners. Each is a change to another document, decided by its registrar; this standard carries the extension or rule that depends on it as unratified until then.
Id
To
Request
RQ-SDD-1
SDD
valueMeanings on attribute slots (X-1), with the SDC-ancestry check
RQ-SDD-2
SDD
unit on numeric attribute slots (X-2), checked as a Measurement Unit individual
RQ-SDD-3
SDD
elaboration on reference slots (X-3), with role and process ancestry checks
RQ-SDD-4
SDD
temporalRole on date attributes of process-referent types (X-4)
RQ-SDD-5
SDD
relation on attribute slots (X-6), checked as a subproperty of is about
RQ-SDD-6
SDD
tokenSet on multi-valued Designative attributes (X-7)
RQ-SDD-7
SDD
the term list carries named domain and range for datatype and annotation properties, so that E-1-class defects are checkable
RQ-SDD-8
SDD
the prompt's rules name the relations that carry no named domain or range (E-6), so the person knows where the checker cannot help
RQ-SCH-1
Schema service
for every reference, the join: which identity attribute of the target type the locator value resolves against
RQ-SCH-2
Schema service
a record identity for every mapped type, even one without identity parts
RQ-SCH-3
Schema service
whether a locator is multi-valued
RQ-RML-1
RML service
emit one named graph per extract and the G-8 manifest; leave status to the pipeline
RQ-RML-2
RML service
implement G-9 before any pattern fires; stop on E-G-MAPPING
RQ-RML-3
RML service
canonical sorted N-Quads and the deterministic loss report (G-7)
RQ-PUB-1
PUB-ARCH
a fixture of a role-free, process-free graph through the indexes and rooting rules
RQ-PUB-2
PUB-ARCH
confirm <ns>id/<uuid> against R-DS-4 and the w3id rules
RQ-PUB-3
PUB-ARCH
bindings cite P-* ids; patterns.standard and hash; Annex A retired at ratification; Milestone A rebuilt; PUB-ARCH's references to "GPS v0.1" read as the first ratified GPS version
RQ-OT-1
Ontology-Template
raise E-1 and E-2 with the CCO maintainers, or confirm they are known
RQ-PUB-4
PUB-ARCH
bind designator tokens and literal keys to the G-1.7 attribute properties (by alias group or per property) instead of is tokenized by; declare the attribute properties in vocab.json with their labels and source keys
RQ-SCH-4
Schema service
declare the unit of every numeric attribute whose unit the source states, in its definition or elsewhere, so that incomplete:unit can be judged and the unit retrieved
RQ-PUB-5
PUB-ARCH
show a value reported incomplete:unit with its unit from the manifest and marked incomplete, never as an unqualified measurement
14. Limits and open questions
Limits are stated so a reviewer can decide whether each is acceptable for the graphs in view; questions are decisions this standard cannot make for its owners.
Id
Limit
Consequence
L-1
The core projects only what the source stated. A column that stands for a role, an act, a status or a unit becomes an information content entity carrying a literal
Valid and shallow until the matching extension is ratified (§10); consumers must not read realist meaning into a literal
L-2
A reference is one object property between two referents
No role, act or time behind a foreign key without X-3; CCO's shortcut relations (is affiliated with, is supervised by, located in) are the ceiling
L-3
Tokens have no OWL semantics (E-4)
Questions about tokens are answered over literals, by SPARQL, SHACL or PUB-ARCH's indexes, never by reasoning
L-4
time values are xsd:string (SDD Decision B)
A temporal facet cannot order them; X-4 does not change this
L-5
One referent per record; no identity across records or sources (G-1.6)
Two systems describing one thing yield two referents until an identity decision exists; nothing merges them silently
L-6
Named ancestry only (T-3); satisfiability is the reasoner's
A referent class that is unsatisfiable in the closure is caught by W-G3, not by the SDD or by this standard's argument
L-7
Units cannot be attached consistently (E-2)
For the core release a unit travels in the structure artifact and the source manifest, not in the graph; a numeric value whose stated unit the graph does not carry is reported incomplete:unit and shown as incomplete by the publication layer (RQ-SCH-4, RQ-PUB-5); X-2 stays blocked by E-2
L-8
Types without identity are losses (G-1.5)
A source that identifies records only by position cannot be projected until RQ-SCH-2
L-9
Absence exists only in the loss report (V-4)
A consumer that needs "not stated" at the edge reads the loss report, not the graph
Open questions.
Id
Question
Who decides
Blocks
Q-1
Which of X-1 to X-7 enter SDD v1.x, and in what order
SDD registrar
the extensions
Q-2
The route for units: an IBE carrier, a pinned unit vocabulary at annotation level, or an upstream CCO correction (E-2)
ratifying architect, with Ontology-Template
X-2
Q-3
Whether describes should replace is about for Descriptive ICE descendants, given that the person accepted only the class (V-2)
ratifying architect
nothing; a V-2 revision
Q-4
Whether a record's source identifier should be an ICE in the graph when a competency question asks for it (V-5)
PUB-ARCH, from its competency questions
nothing
Q-5
Graph granularity: one graph per extract (G-8) gives one support per source; per-record graphs would give per-record provenance (PUB-ARCH L-5, Q-3)
PUB-ARCH and the RML service together
the source model
Q-6
Language tags on string tokens when a source declares a language (T-6)
Schema service
nothing in v0.3
Q-7
Whether skos:notation stays the one term outside the closure, or P-12 moves to a value ICE about the pattern
ratifying architect
P-12
Q-8
Whether G-4 may infer the target of a classified value from ancestry alone. The reviewer's objection stands for attributes whose designatum is not the record's referent (a cost center code). Proposed middle path: designates ref only where the schema marks the attribute as an identity part or the label (a source-declared fact), is about ref nowhere by default, and any other target only through X-6; otherwise a classified value ICE is part of its record and carries no target quad. Decided 2026-11-11 by the ratifying architect: adopted; G-4, P-2b and V-2 now read so
ratifying architect
G-4, P-2b, V-2, PUB-ARCH's designator index (RQ-PUB-4)
15. Acceptance, ratification gates and change discipline
Ratification is an ordered conjunction: every gate holds or the standard stays a draft. ACCEPT = g₁ ∧ … ∧ g₇, the minimum and never a mean, as in the SDD's §10.
1.  Decisions. V-1 to V-7 carry a status set by the ratifying architect; a rejected decision returns the section it governs to draft.
2.  Independent derivation. W-G1 and W-G2 are regenerated by an implementation of G-0 to G-9 written from this text alone, byte-identical to the registry's expected files.
3.  Consistency. W-G3 holds: the expected graph is consistent under the pinned reasoner, and its datatype-form twin is inconsistent.
4.  Forbidden entailments and refusals. W-G4 holds in full.
5.  Determinism. W-G5 holds.
6.  Upstream answers. Q-2 is decided or X-2 is formally deferred; RQ-SCH-1 and RQ-SCH-2 are answered, or the losses they cause on the Milestone A package are declared acceptable by the ratifying architect.
7.  Publication alignment. RQ-PUB-3 is executed: PUB-ARCH's bindings cite P-* ids, projection.json.patterns names this standard and its hash, Annex A is retired, and the Milestone A release is rebuilt.
Settled decisions. Approved as architectural foundations by the production-readiness review of 2026-11-11. They are reopened only on a demonstrated implementation failure, an ontological inconsistency or an unmet approved competency question; that a richer representation is possible is not a reason.
Decision
Where
No mandatory has text value or other CCO datatype-value property
V-3, T-5, E-1
Native RDF/XSD typed literals
G-5
Source-specific attribute properties
G-1.7
Ordinary scalar values on source records
P-2a
Classified source-local ICEs where the accepted SDD classifies them
P-2b, G-1.3
Record and referent distinct
P-1, ADR-001
Identity and label attributes designate the referent
G-4, Q-8
Source-level identity separate from global entity resolution
G-1.6, §2
Deterministic UUIDv5 identifiers with collision validation
G-1, G-1.8
Missing values preserved through deterministic loss reporting
P-0, §7
Information bearers optional, never mandatory
V-3, NG-S7
Core release requirements, demonstrated through the witnesses with expected graphs generated independently from these rules, never copied from implementation output: (1) deterministic record, referent and value IRIs; (2) source identity uniqueness and collision detection; (3) correct plain and classified values; (4) G-4 designation for identity and label attributes; (5) valid typed literals with no CCO datatype-value property; (6) correct handling of nulls, missing values, invalid lexical forms and unresolved joins; (7) consistency under the pinned closure; (8) deterministic named-graph serialization and manifests; (9) publication bindings for the attribute properties (RQ-PUB-4); (10) explicit reporting of material semantic incompleteness, units included.
Deferred, non-blocking unless an approved competency question requires one: cross-source entity resolution and canonical naming; historical designation and reassignment analysis (P-15); token sets and other lexical representations (X-7); roles and acts behind ordinary references (X-3); full measurement and quantity modeling (X-2); bearer and information-quality materialization; rich temporal regions (X-4); new domain classes. Each arrives as an independently versioned extension; the core stays useful without them. Release blockers remain: an OWL inconsistency, an identity collision, invalid serialization, or loss of essential semantic information.
Catalogue patterns ratify individually: a P-1x enters the ratified set when its W-G6 package passes, and the standard may be ratified with some catalogue patterns still provisional, listed by id in the ratification note. Extensions X-1 to X-7 ratify only after their RQ-SDD field exists and a witness covers them; v0.4 is the first version that can carry a ratified extension.
Change discipline. Identifiers are minted once and never renumbered. A change to a pattern's quads, a rule, a decision or a pattern-fixed term is a new version of this standard and a supersession event for every projection.json that cites the old hash. The supersession triggers from outside are: a new Ontology-Template pin (every term is re-verified), a change to the SDD contract (sddVersion), and a change to PUB-ARCH's binding contract. The witness generator and the expected files are re-issued with each version; superseded files are retained under superseded/v<n>/ as the SDD does.
Registry (authoritative hashes; the first 8 characters are what the prose cites).
File or artifact
sha256 or identifier
Role
fixtures/witnesses/full/sdd.jsonld (SDD v0.6)
57e1478315a20680d3b4bceb70df8e4749500f503bf827ed0ade7d456fbeedc9
F-G1
fixtures/witnesses/full/inventory.jsonld (SDD v0.6)
1db35f4f744fece9e4c018982b182cef3deaf5a7eaeb0274936ac95d16058fd8
F-G1
SDD term list, terms_sha256
a9e01756d749655a53088833bb97612791caf9a19220065848c826f99985cd39
permitted terms, named ancestry
Ontology-Template pin
commit 7cfdfbfe5dde13be7a0fd99b52711bdb0cdee3fb
the closure
vendor/cco-upstream/CommonCoreOntologiesMerged.ttl (CCO v2.0-2024-11-06)
e609db27478a2c8b52b9bb5eb5ac979ac323510e851c368e4d9ec7d1c153fe5b
pattern-fixed terms, E-1, E-2
vendor/ontology-template/bfo-disjointness.ttl
a4447e93b2024d8f93c06800cf0e35580ec097246fe08f984593272c43bdbfa5
W-G3, E-1
vendor/ontology-template/bfo-core-extract.ttl
8bbeda8fe261f74e766fb186e51e9b28e1c42948403c66c776247f84e641ecd2
BFO terms
derive_patterns.py, the audit of 2026-11-11 and the generator's seed
1c600bb2a9e915f36d03bab9c884c7d410d9e5f3a978179423a13bb9ff8486b7
W-G1 seed; its datatype-property rule is superseded by G-5
this document, expected.nq, expected-datatype-form.nq, F-G2, F-G3, F-G4
assigned at ratification
W-G1 to W-G6
Acceptance readiness: NOT READY — v0.3, 2026-11-11; architecture approved; gates 1 to 7 open; awaiting the ratifying architect's review of V-1 to V-7 (Q-8 decided) and the RQ-\* requests.
