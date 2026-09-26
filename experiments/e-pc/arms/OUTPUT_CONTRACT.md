OUTPUT FORMAT (mandatory, identical for every task)

Return one JSON object and nothing else: no words before it, no words after it, no code fence. The object has this shape:

{
  "sections": [
    {
      "name": "<the section name given in the instructions>",
      "statements": [
        {
          "text": "<one sentence>",
          "kind": "<fact | question | conjecture | evaluation>",
          "entities": ["<each person, organisation, document, event, rule or object the sentence mentions, named exactly as the case names it>"],
          "trace": "<a verbatim quotation of at most fifteen words from the case on which the sentence rests, or the word none>"
        }
      ]
    }
  ],
  "synthesis": [
    { "text": "...", "kind": "...", "entities": ["..."], "trace": "..." }
  ]
}

Kinds:
- fact: something the case states. A fact must carry a trace, and the trace must be words that actually appear in the case.
- question: something to ask a named person. A question may mention people or things the case does not.
- conjecture: something you think may be true that the case does not state. Say so; a conjecture may mention people or things the case does not.
- evaluation: a judgment about what matters, why, or how goods and obligations bear on one another.

Never put in a fact anything the case does not state. If you are unsure whether the case states it, make it a conjecture or a question.
