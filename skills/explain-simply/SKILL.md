---
name: explain-simply
description: >-
  Explains technical topics and writes documentation that people understand
  on the first read, without dropping facts. Use when the user asks what
  something is, how or why it works, or what an error, log line, or piece of
  code means, or asks to explain, clarify, simplify, summarize, or ELI5. Also
  use when writing or editing documentation such as README.md, USAGE.md,
  DEVELOPMENT.md, guides, docstrings, or comments, when the user says a text
  is dense, repetitive, contradictory, too long, or hard to follow, and when
  the user asks to find duplication or contradictions in documentation.
license: CC-BY-4.0
metadata:
  author: sauljabin
  version: "1.1"
---

# Explain simply

The reader understands the text on the first read and finds each fact in one
obvious place. This applies to answers in chat and to documentation in a
repository.

Two reference files hold the details:

- [references/wording.md](references/wording.md): words, phrases, sentences,
  formatting, and tone, each rule with a bad and a good example. Read it
  before you write. It applies to every answer and every file.
- [references/documentation.md](references/documentation.md): which file owns
  which fact, how to link instead of repeating, how to find duplication and
  contradictions across files, and how to structure files such as
  `USAGE.md`. Read it before creating or editing documentation.

## Start from the reader

Write the way a colleague who knows the topic would explain it at the
reader's desk: plain, direct, in full sentences that connect to each other.

Work out what the reader already knows. Use their words, their code, and
where the text will live. Someone who asks why their consumer group lags
knows what Kafka is. Someone who asks what Kafka is does not. A `README.md`
reader is new to the project. A `DEVELOPMENT.md` reader is about to change
it.

Then write for that reader:

- Explain a term the reader may not know, or one specific to the project,
  once, where it first appears. Leave terms they already share alone.
- If the topic has a known trap, such as a misleading name or a surprising
  default, say it plainly: "The name suggests `--force` skips the checks. It
  only skips the confirmation prompt."
- Say what the fact changes for the reader: what breaks, what they need to
  do, or what they can stop worrying about.

## Keep the knowledge

Simple does not mean less.

A fact here means every number, default, limit, flag, version, path, error
condition, and exception. When you rewrite, shorten, or summarize existing
text, every fact in it stays. Shorten by removing repetition, filler, and
inflated words. If a fact does not belong where you are writing, move it to
where it belongs and link to it.

When you answer a question, you choose what the question needs instead of
cutting from a source. Leave out what does not help this reader, but never
make a statement vaguer or false to make it simpler.

Keep the technical terms practitioners share, such as `commit`, `offset`,
`TLS`, `cache`, or `endpoint`. Replacing them with homemade phrases makes the
text harder to search and to match with other docs.

## Say it once, and the same way

Repetition makes text longer, and copies drift apart until they contradict
each other.

- Before adding a sentence, check whether an earlier one already says it. If
  so, drop the new one or merge the two.
- Use one name for one thing. If the text says `profile` in one paragraph and
  `config` or `environment` in the next, the reader assumes three different
  things. Pick the name the code or UI uses.
- Put a rule and its exceptions together. Do not write "always" in one
  section and the exception three sections later.
- If two statements disagree, find out which one is true (the code, the
  `--help` output, or the user) and keep only that one.

Across documentation files, each fact has one home and other files link to
it. [references/documentation.md](references/documentation.md#find-duplication-and-contradictions)
has the procedure for finding copies and contradictions in a set of files.

## Order and shape

Lead with the answer or the conclusion. Supporting detail comes after it.
Keep related facts together: one topic per paragraph or section.

| Content | Shape |
| --- | --- |
| Reasoning, cause and effect, trade-offs | Short paragraphs |
| Ordered steps | Numbered list |
| Independent items of the same kind | Bulleted list |
| Several items compared on the same attributes | Table |
| Commands, code, config, output | Code block with a language tag |

Do not break reasoning into bullet fragments or into a string of short,
unconnected sentences. Both hide how the ideas depend on each other. Words
such as "because", "so", "but", and "until" carry the reasoning.

## Explaining something

1. Answer in one plain sentence: what it is, or what went wrong.
2. Give one concrete example from the user's context, with real values: their
   code, their error, their numbers.
3. Walk through the example: what goes in, what happens, what comes out.
4. Name the general idea last, with its technical term.
5. Add one caveat, only if the example could plant a wrong idea.

Scale to the question. "What does `git stash` do?" needs two sentences and a
command, not five steps. For a deep topic, give the short version and name
the specific part you could cover next, such as "how a rebalance resets the
lag", so the user can ask for it.

Use one example from start to finish. Each new example makes the reader start
over. Use an analogy only when no real case fits. Map each part of the
analogy to the real thing and say where it stops being true.

## Worked example

The user asks why their Kafka consumer group shows lag even though the app is
running.

Abstract and dense:

> Consumer lag is the delta between the log-end offset and the committed
> offset per partition, indicating that the consumer group's throughput is
> below the producer's ingress rate or that commits are not being issued.

Answer first, then the example:

> The lag counts from the position your group last saved, not from the
> message your app is reading now.
>
> On partition 0 of `orders`, the log ends at offset 1,500, which is the
> offset the next message will get. Your group last saved its position at
> offset 1,200. That saved position is the committed offset, and the 300
> messages between the two are the lag.
>
> The lag looks stuck because your app commits only every 1,000 messages. It
> won't save a new position until it reaches offset 2,200, so the lag stays
> at 300 or grows, even though the app is processing messages.

Both versions use the same terms (`offset`, `committed offset`, `lag`). The
second one answers first, shows the numbers before naming them, and connects
the steps with "because" and "so". It also tells the user why the number
does not move, which is what they asked.

## Checks before sending

This is the final pass. Each check points to the section that holds the rule.

- Facts: is every fact from the source or the diff still present, here or
  behind a link? See [Keep the knowledge](#keep-the-knowledge).
- Repetition and contradictions: does anything appear twice, under two names,
  or with two different values? See
  [Say it once, and the same way](#say-it-once-and-the-same-way).
- Order: does the answer come first?
- Reader: is there a concrete example where an idea is abstract, and is each
  uncommon term explained once? See [Start from the reader](#start-from-the-reader).
- Wording: does the text pass the patterns in
  [references/wording.md](references/wording.md)?
- Length: is it as long as the question needs, and no longer?
