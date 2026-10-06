---
name: explain-simply
description: >-
  Explains and documents technical topics in short, plain sentences without
  losing information. Anchors each idea in one concrete example with real
  values, names the term after the reader has the idea, says each thing once,
  uses plain wording instead of filler and inflated vocabulary, and gives
  every fact in a documentation set one home that other files link to. Use
  when the user asks what something is, how or why it works, or what an
  error, log line, or piece of code means, or asks to explain, clarify,
  simplify, summarize, or ELI5. Also use when writing or editing
  documentation such as README.md, USAGE.md, DEVELOPMENT.md, guides,
  docstrings, or comments, when the user says a text is dense, repetitive,
  too long, or hard to follow, and before writing any long explanation.
license: CC-BY-4.0
metadata:
  author: sauljabin
  version: "1.0"
---

# Explain simply

The reader understands the text on the first read and finds each fact in one
obvious place. This applies to answers in chat and to documentation in a
repository.

Two reference files hold the details:

- [references/wording.md](references/wording.md): word, phrase, sentence, and
  formatting rules, each with a bad and a good example. Read it before
  writing anything longer than a few paragraphs.
- [references/documentation.md](references/documentation.md): how to classify
  information across files, link instead of repeating, and structure files
  such as `USAGE.md`. Read it before creating or editing documentation.

## Keep the knowledge

Simple does not mean less.

- Shorten by removing repetition, filler, and inflated words. Never by
  dropping facts.
- Keep every number, default, limit, flag, version, error condition, and
  exception. If a detail does not belong where you are writing, move it to
  where it belongs and link to it.
- Keep technical terms that practitioners share, such as `commit`, `offset`,
  `TLS`, `cache`, or `endpoint`. Explain a term only when the reader may not
  know it or when it is specific to the project.
- If a simpler wording makes a statement vaguer or false, keep the precise
  one.

## Say it once

Repetition makes text longer and harder to follow, and copies drift apart.

- Before adding a sentence, check whether an earlier one already says it. If
  so, drop the new one or merge the two.
- Lead with the answer or the conclusion. Supporting detail comes after.
- Put related facts together: one topic per paragraph or section.
- Do not restate the question, announce what you are about to say, or recap
  at the end.
- In documentation, each fact has one home. Other places link to it with a
  short sentence of context. See
  [references/documentation.md](references/documentation.md).

## Pick the right shape

| Content | Shape |
| --- | --- |
| Reasoning, cause and effect, trade-offs | Short paragraphs |
| Ordered steps | Numbered list |
| Independent items of the same kind | Bulleted list |
| Several items compared on the same attributes | Table |
| Commands, code, config, output | Code block with a language tag |

Do not break reasoning into bullet fragments. A list of three-word bullets
hides how the ideas connect.

## Explaining something

1. **One plain sentence:** what it is, or what went wrong.
2. **One concrete example** from the user's context, with real values: their
   code, their error, their numbers.
3. **Walk the example:** what goes in, what happens, what comes out.
4. **Name the general idea last,** with its technical term.
5. **One caveat,** only if the example could plant a wrong idea.

Scale to the question. "What does `git stash` do?" needs two sentences and a
command, not five sections. For a deep topic, give the short version and
offer to go further.

Use one example from start to finish. Each new example makes the reader start
over. Use an analogy only when no real case fits; map each part of the
analogy to the real thing and say where it stops being true.

## Wording in short

The full rules with examples are in
[references/wording.md](references/wording.md). The most common ones:

- Plain verbs: "is", "has", "uses", not "serves as", "boasts", "leverages".
- Concrete nouns: name the command, the file, the number. Not "various
  options" or "a wide range of features".
- No claims of importance: drop "crucial", "powerful", "seamless", "robust".
  State the fact that makes it matter.
- Active voice, present tense, and "you" for instructions.
- One hedge at most, and only when the uncertainty is real.
- No openers or closers that carry no information.
- No em dashes. Use a period, comma, colon, or parentheses.
- Bold at most one phrase per section, for something the reader must not
  miss. No emoji in headings or lists.

## Worked example

The user asks why their Kafka consumer group shows lag even though the app is
running.

Abstract first, hard to follow:

> Consumer lag is the delta between the log-end offset and the committed
> offset per partition, indicating that the consumer group's throughput is
> below the producer's ingress rate or that commits are not being issued.

Example first, clear on the first read:

> Partition 0 of `orders` has 1,500 messages. The newest one is at offset
> 1,500.
>
> Your group last saved its position at offset 1,200. That saved position is
> the committed offset.
>
> 1,500 minus 1,200 is 300. Those are 300 messages your group has not
> confirmed yet. That number is the lag.
>
> Your app commits only every 1,000 messages. Until it reaches offset 2,200,
> the committed offset stays at 1,200 and the lag looks stuck, even though
> the app is reading.

Same facts. The second version keeps the technical terms (`offset`,
`committed offset`, `lag`) but shows the numbers before naming them.

## Checks before sending

- Is every fact from the source or the diff still present, here or behind a
  link?
- Does anything appear twice, in this text or across files?
- Does the answer or conclusion come first?
- Is there a concrete example with real values where an idea is abstract?
- Is each uncommon term explained once, and each common term left alone?
- Run the patterns in [references/wording.md](references/wording.md) over the
  text: inflated words, filler, em dashes, scattered bold, fragment bullets.
- Is the length right for the question?
