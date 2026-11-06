---
name: architecture-design
description: >-
  Designs software architecture and writes the design document a team uses
  to make and record technical decisions: problem, decisions, architecture,
  strengths and weaknesses, alternatives, operations and failure modes, known
  gaps, open questions, parking lot, glossary, and versioned history. Output
  is one self-contained HTML page by default, built from a fixed template so
  every agent produces the same look: diagrams before text, hover tooltips,
  a table of contents that stays on screen, and highlighted code. Use when
  the user asks to design or redesign a system, service, integration, or
  migration; to compare architecture options or make a technical decision;
  or to write, review, or update a design doc, technical design document
  (TDD), solution design document (SDD), architecture decision record (ADR),
  RFC, or architecture proposal. Also use when the user asks to document the
  decisions, trade-offs, or failure modes of an existing architecture.
license: CC-BY-4.0
compatibility: >-
  The HTML page opens in any modern browser and loads Mermaid and
  highlight.js from a CDN; without network the diagrams show their source.
  scripts/check_doc.py needs Python 3.9 or newer, standard library only.
metadata:
  author: sauljabin
  version: "1.1"
---

# Architecture design

You help the user reach a technical decision and write it up as a design
document. The reader should understand the design from its diagrams, read
text only where a diagram can't say it, and find every fact in one place.

The document is one HTML page built from [assets/template.html](assets/template.html).
The template owns all CSS and JavaScript, so the look does not depend on
which agent writes the page. You write only the content.

| File | What it is | When to read it |
| --- | --- | --- |
| [references/sections.md](references/sections.md) | What each section holds, with good and bad examples | Before writing |
| [references/components.md](references/components.md) | HTML for every building block: cards, items, tables, callouts, code | Before writing |
| [references/diagrams.md](references/diagrams.md) | Box diagrams, Mermaid, and the rules for both | Before drawing |
| [assets/template.html](assets/template.html) | The page to copy | When you create the document |
| [assets/example.html](assets/example.html) | A finished document about a transactional outbox | To see the result in a browser, or to copy a pattern; read only the part you need |
| [scripts/check_doc.py](scripts/check_doc.py) | Checks structure, links, IDs, diagrams, and template drift | After every change |

## What kind of document this is

It is not a copy of one standard. It takes the part of each that serves a
decision:

| Taken from | What it brings |
| --- | --- |
| Design docs and RFCs | Problem, goals and non-goals, alternatives |
| Architecture decision records | Short decisions with stable IDs, status, and a history instead of silent edits |
| arc42 | A glossary, and risks and technical debt as their own sections |
| Production readiness reviews | Failure modes, monitoring, rollout, and rollback |

If the repository already keeps ADRs or design docs in a fixed format and
the user asks for one of those, write that format and keep the writing and
diagram rules from this skill.

## Workflow

1. **Understand the problem.** Read the code, configs, existing docs, and the
   conversation. Collect the problem with one real example, the goals with
   numbers, the non-goals, the constraints (versions, load, latency, budget,
   deadlines, who runs what), and what exists today. Ask the user only for
   what you cannot find, all questions in one message. When something is
   unknown but not blocking, write it down as an open question and continue.
2. **Find the decisions.** List the questions the design must answer, such
   as "Where does validation run?". For each one, compare at least two
   realistic options against the goals, pick one, and name what it costs.
   Decisions the user already made are inputs: record them, and if one
   conflicts with a goal, say so in a callout or a known gap instead of
   reopening it silently. Never invent a number, version, or limit; verify
   it, or mark it as an assumption with an open question.
3. **Check the story.** Write one sentence per section, in the order of
   [Sections](#sections), and read them in a row. They must tell one story:
   this hurts, so we decided this, it works like this, it costs this, we
   rejected that, this is how we run it, this is still missing. Fix gaps or
   jumps before you write anything else.
4. **Draw, then write.** Draw the big picture first, then the flows. Write
   text only for what the diagrams and tables can't say. See
   [references/diagrams.md](references/diagrams.md).
5. **Build the page.** Copy the template with a shell command; do not retype
   it, because the CSS and JavaScript must stay byte for byte the same:

   ```bash
   mkdir -p docs/design && cp <skill-dir>/assets/template.html docs/design/order-events-outbox.html
   ```

   Then replace the content between `<!-- CONTENT START` and
   `<!-- CONTENT END -->`, and the `<title>`. Use only the components in
   [references/components.md](references/components.md). Never add a
   `<style>` block, a `style` attribute other than the diagram grid
   variables, or a `<script>`. If a component is missing, use the closest
   one and tell the user.
6. **Check.** Run the checker and fix every error:

   ```bash
   python3 <skill-dir>/scripts/check_doc.py docs/design/order-events-outbox.html
   ```

   If you can open a browser, look at the page at desktop and phone width.
   Diagrams are the part most likely to need a fix: overlapping labels,
   boxes too narrow for their names.
7. **Report.** Give the user the path, the status and version, and the open
   questions and known gaps that need their input.

Where to save: follow the repository if it has a place for design docs
(`docs/design/`, `docs/adr/`, `rfcs/`). Otherwise use
`docs/design/<slug>.html`, where the slug is the title in kebab case. Outside
a repository, ask.

## Sections

Sections always appear in this order. Each one has a fixed `id` so links to
it keep working across versions. [references/sections.md](references/sections.md)
says what goes in each one.

| # | Section | `id` | Required | Answers |
| --- | --- | --- | --- | --- |
| 1 | Overview | `overview` | Yes | What is this, and what do you need from me? |
| 2 | Problem | `problem` | Yes | What hurts today, with an example, and what counts as solved? |
| 3 | Decisions | `decisions` | Yes | What did we decide, in one card each? |
| 4 | Architecture | `architecture` | Yes | How does it work? |
| 5 | Strengths and weaknesses | `tradeoffs` | Yes | What do we gain, and what costs do we accept? |
| 6 | Alternatives | `alternatives` | Yes | What else did we consider, and why not? |
| 7 | Operations and failures | `operations` | Yes | How do we run it, and what happens when it breaks? |
| 8 | Known gaps | `gaps` | When there are any | What is still wrong with this design? |
| 9 | Open questions | `questions` | When there are any | What don't we know yet? |
| 10 | Parking lot | `parking-lot` | When there are any | What good ideas are out of scope for now? |
| 11 | Glossary | `glossary` | When terms need it | What do the project's terms mean? |
| 12 | References | `references` | When useful | Where can I read more? |
| 13 | Document history | `history` | Yes | What changed, when, and in which version? |

The order follows the reader: why (1–2), what (3–4), at what cost (5–6), how
to run it (7), and what is unfinished, from most to least certain (8–10).
Reference material comes last (11–13).

Three sections are easy to mix up:

- A **weakness** is a cost the design accepts and lives with, such as "a
  disabled schema version is accepted for up to 30 s".
- A **known gap** is a problem the design does not accept: it has candidate
  fixes, a proposal, and an owner, and must be fixed by a stated point.
- An **open question** is missing information: someone must answer it before
  part of the design can be decided.

Items in Alternatives, Known gaps, Open questions, Parking lot, Decisions,
and the failure table get stable IDs: `D1` decisions, `A1` alternatives,
`F1` failures, `G1` gaps, `Q1` questions, `P1` parking lot. IDs are never
reused or renumbered, so `G2` in a ticket or chat always means the same
thing.

## Writing rules

Technical terms stay; sentences stay simple.

- **Example first.** Show a concrete case with real values (an order ID, a
  topic name, a latency) before the general rule.
- **Diagram over prose.** If a diagram or table already shows it, do not
  repeat it in a paragraph. A figure caption says what to notice, in one or
  two sentences.
- **Say it once.** Each fact has one home. Everywhere else links to it, with
  an ID chip such as `<a class="id" href="#d3">D3</a>` or a link to the
  section. Before changing a fact, search the page for every mention of it.
- **One name per thing.** The same component has the same name in every
  diagram, table, and sentence. Project terms go in the glossary once and
  are linked with `<a class="term">`, which shows the definition on hover.
- **Text when it matters.** Warnings go in callouts, and only for things that
  can hurt: data loss, outages, security, cost, or steps that can't be
  undone. More than one callout per screen and readers stop noticing them.
- **Numbers with units and sources.** "380 ms p99 on staging", not "fast".
  Mark an estimate as one.
- **Plain words.** Active voice, present tense, short sentences connected
  with "because", "so", and "but". No filler such as "This section
  describes" or "It is important to note".
- **Tooltips hold extra detail, never the only copy of something a reader
  needs.** Tooltips don't print and are hard to reach on a phone. Versions,
  ports, and config keys fit in a tooltip; a limit that causes an outage
  belongs in visible text.

If the `explain-simply` skill is installed, its wording rules apply too.

## Code blocks

Every code block names its language so it is highlighted:
`<pre><code class="language-yaml">`. Use `language-text` for plain output.
Show only the lines that matter, with realistic values, and give a file name
or a short description in a `figure.code` caption. See
[references/components.md](references/components.md#code).

## Versioning

The header shows the status and version, and the Document history table
lists every version, newest first.

| Status | Means | Chip |
| --- | --- | --- |
| Draft | Being written; may change completely | `chip warn` |
| In review | Shared for feedback | `chip info` |
| Accepted | Agreed; the team builds from it | `chip good` |
| Superseded | Replaced by a newer document, linked in a callout at the top | `chip` |
| Rejected | Decided against; kept for the record | `chip bad` |

Versions are `MAJOR.MINOR`:

- `0.x` while the status is Draft or In review. Raise the minor version each
  time you share a changed version.
- `1.0` when the document is accepted.
- After that, raise the **minor** version for clarifications, new detail,
  answered questions, and fixed gaps that leave every decision as it was.
  Raise the **major** version when a decision is added, removed, or
  reversed: anyone who read the old version must read it again.

Each history row says what changed and links the IDs or sections it touched,
for example "Added D6 and G3 after the review with Platform". A typo fix
doesn't need a row.

## Updating an existing document

1. Read the whole document first, so you know where each fact lives.
2. Change each fact in its one home, then search for other mentions.
3. Keep IDs. A resolved question or fixed gap stays in its section with the
   `resolved` class and a line that says how it was resolved and links the
   decision that resolved it. A reversed decision keeps its card, marked
   with a chip, and links the decision that replaced it.
4. Set the new version and the date in the header, and add a history row.
5. If the page was built from an older template, run
   `check_doc.py --sync` to update its CSS and JavaScript.

## Other formats

HTML is the default. When the user asks for another format, keep the
section order, IDs, and writing rules, and change only the presentation. In
Markdown:

- Use Mermaid for every diagram (`flowchart` with `subgraph` for box
  diagrams), since box diagrams need the template.
- Use GitHub alerts (`> [!WARNING]`) for callouts.
- Use tables for decisions, failures, gaps, and questions, with the ID in
  the first column.
- Link glossary terms on first use, since there are no tooltips.

## Checks before sending

- `check_doc.py` reports 0 errors.
- The one-sentence-per-section summary from step 3 still reads as a story.
- Every decision card links to where it is explained, and every weakness
  links to its mitigation, gap, or decision.
- No fact appears twice, and no two sentences disagree.
- Every number has a unit and a source or an "estimated".
- Each diagram has a caption that says what to notice.
- The header version matches the newest history row.
