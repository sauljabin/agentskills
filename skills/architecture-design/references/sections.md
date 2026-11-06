# Sections

What goes in each section of the design document, in page order. The order,
the `id`s, and which sections are required are in
[SKILL.md](../SKILL.md#sections). The HTML for each building block named
here is in [components.md](components.md).

## Contents

- [Header](#header)
- [Overview](#overview)
- [Problem](#problem)
- [Decisions](#decisions)
- [Architecture](#architecture)
- [Strengths and weaknesses](#strengths-and-weaknesses)
- [Alternatives](#alternatives)
- [Operations and failures](#operations-and-failures)
- [Known gaps](#known-gaps)
- [Open questions](#open-questions)
- [Parking lot](#parking-lot)
- [Glossary](#glossary)
- [References](#references)
- [Document history](#document-history)
- [Keeping the thread](#keeping-the-thread)

## Header

The title says what the design does, not what area it belongs to. The
subtitle is one sentence with the outcome.

| Bad | Good |
| --- | --- |
| Order events | Publish order events with a transactional outbox |
| Kafka proxy design | Validate Kafka records against their schema at the proxy |

The meta row holds status, version, date (`YYYY-MM-DD`), authors, and
reviewers. Status and version follow the rules in
[Versioning](../SKILL.md#versioning). A superseded document gets a `danger`
callout at the top of the header that links its replacement.

## Overview

One `lead` paragraph of three to five sentences: the context, the problem,
the proposed solution, its main cost, and what readers need to do. A reader
who stops here should know whether the design affects them.

When the document is in review, add one `note` callout that names what
reviewers must decide, with links to the open questions or decisions.

Bad: describes the document instead of the design.

> This document describes the proposed architecture for order events. It
> covers the problem, the decisions, and the alternatives considered.

Good: states the design and its cost.

> Orders API saves an order and then publishes `OrderPlaced` as a second
> step, so a failed publish loses the event; in September that happened to
> 1,214 orders. This design writes the event to an outbox table in the same
> transaction as the order, and Debezium copies it to Kafka. The cost is a
> new Kafka Connect deployment and duplicate events that every consumer must
> drop.

No diagram here: the first diagram belongs to the Problem or the
Architecture.

## Problem

1. The problem in one or two sentences.
2. A concrete case with real values: an order ID, a timestamp, an error, a
   count. A sequence diagram of the failure is often the clearest way to
   show it.
3. Goals and non-goals in two `panels`. Goals are measurable ("99% of events
   reach Kafka within 2 s"). Non-goals name what a reader might expect this
   design to do and it won't.
4. Constraints, when they shape the decisions: versions, load, latency
   budgets, deadlines, teams. `stats` tiles work well for numbers.

Do not describe the solution here. If the reader can't tell what is wrong
without knowing the solution, the problem statement is not finished.

## Decisions

One card per decision. This section is a summary: each card is short and
links to where the decision is explained, so nothing in it is repeated
elsewhere.

- The title is the decision as a statement: "Validation is a topic setting",
  not "Validation".
- The body says what was decided and why, in one to three sentences.
- The links go to the Architecture subsection that explains it and, when
  there were real alternatives, to the Alternatives subsection.
- Order the cards in the order the Architecture explains them.

Six to ten cards is typical. More than twelve usually means some are
details of a bigger decision; merge them.

When a decision is reversed in a later version, the card stays, gets a chip
such as `Reversed in 2.0`, and links the decision that replaced it.

## Architecture

The structure depends on what is being designed. This shape works for most
designs:

1. One sentence that connects the decisions to the big picture.
2. A box diagram of the whole system: what is new, changed, and existing,
   grouped by where it runs or who owns it. See
   [diagrams.md](diagrams.md#box-diagrams).
3. A walkthrough of the main flow as numbered steps under the diagram.
   Hovering a step highlights its part of the diagram.
4. One `h3` subsection per decision, or per group of related decisions. It
   starts with the decision's ID chip and holds what a builder needs: a
   sequence diagram for an interaction, a code block for a schema, config,
   or API, a table for settings.
5. Subsections for anything else a builder needs: data model, API, security,
   capacity.

Every `h3` here gets an `id` so decision cards and the table of contents can
link to it.

## Strengths and weaknesses

Two panels, `good` and `warn`. Each bullet states a concrete effect and
links to where it comes from or how it is handled.

| Bad | Good |
| --- | --- |
| Better reliability. | An event exists if and only if its order committed: no lost events and no events for rolled-back orders (D1). |
| Some operational overhead. | Kafka Connect is a new deployment to run, upgrade, and watch (Q1). |
| Possible latency. | A disabled schema version is still accepted until the cache expires, up to 30 s (F3). |

A weakness is a cost the design accepts. If the team does not accept it, it
is a [known gap](#known-gaps) instead: move it there and link it.

## Alternatives

One `h3` subsection per decision that had real alternatives. Skip decisions
that had none; do not invent straw men.

Each subsection has:

1. A comparison table: criteria as rows, taken from the goals and
   constraints; options as columns, with the chosen one marked `chosen`.
   Cells are short and use `yes`, `no`, or `partial`. Be honest: the chosen
   option can lose on a criterion.
2. One item per rejected option, with an `A` ID, what it is, **Why not** (the
   deciding reason), and **Better if** (the situation in which it would
   win). "Better if" tells future readers when to revisit the decision.

The table does not repeat the strengths and weaknesses; it only scores the
options against each other.

## Operations and failures

What the team running the design in production needs. Use the parts that
apply:

| Part | Holds |
| --- | --- |
| Numbers | `stats` tiles: targets, measured values, capacity, headroom |
| Where things fail | A box diagram with `F` badges on the components where each failure starts |
| Failure modes | A table with one row per failure: ID, failure, what users see, how we detect it, what to do |
| Monitoring | A table of signals: normal value, when to alert |
| Rollout and rollback | Numbered steps, with a diagram of intermediate states when they differ; how to undo each step and from which step there is no way back |
| Runbook | The commands an on-call engineer runs, in code blocks |

A failure row says what the user sees, not what the component does: "orders
still succeed, invoices are late" is more useful than "connector task
fails". Each row links to the gap or decision that limits it.

If nothing in the design runs in production, for example a library
interface, say so in one sentence and keep the section with that sentence.

## Known gaps

Problems the design does not solve yet and does not accept. Each gap is an
item with a `G` ID and:

- a title that states the problem,
- a chip for when it must be fixed: `bad` when it blocks a step or the
  launch, `warn` for a later point, plain for "eventually",
- an example of what goes wrong,
- **Options**, **Proposal**, and **Owner** in a `facts` list.

When a gap is fixed, it stays with the `resolved` class and a sentence that
links the decision or change that fixed it.

## Open questions

Information the design is missing. Each question is an item with a `Q` ID
and:

- the question as the title,
- a chip: `bad` "Blocking" when a decision or step waits for the answer,
  plain "Not blocking" otherwise,
- what changes depending on the answer,
- **Who can answer** and **Needed by** in a `facts` list.

A question with known options and no information missing is a decision
waiting to be made. Write it as a known gap with a proposal instead.

When answered, the question stays with the `resolved` class and the answer
in one sentence, linking what it changed.

## Parking lot

Good ideas that came up and are out of scope now. Each is an item with a `P`
ID, a sentence on why it is not in this design, and **Revisit when**: an
event or threshold that should bring it back, such as "a third team consumes
the events". An idea without a trigger is forgotten.

## Glossary

Terms specific to the project or likely to be new to a reader, in
alphabetical order, each defined in one or two sentences. Each `dt` has an
`id` that starts with `term-`. Text links the first mention of a term in
each section with `<a class="term" href="#term-...">`, and the page shows
the definition on hover. Skip terms every reader shares, such as HTTP or
JSON.

## References

External links that add depth: vendor docs, specs, earlier design docs,
tickets. Each has one line on what the reader gets from it. Everything
needed to understand and approve the design is in the document itself;
references are for going further.

## Document history

A table with Version, Date, Status, Author, and Changes, newest first. The
rules for versions and statuses are in [Versioning](../SKILL.md#versioning).

## Keeping the thread

The sections form one story. These habits keep it readable:

- Start each section with a sentence that connects it to the previous one
  when the link isn't obvious, such as "Two of the decisions had realistic
  alternatives; each table compares them on the goals from the Problem."
- Reuse the example from the Problem in later sections. If order 84121 shows
  the failure, the Architecture shows what happens to order 84121 now.
- Every ID chip is a link. A reader in Strengths and weaknesses who sees
  `F2` can hover it for a summary and click it for the details.
