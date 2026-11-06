# Components

The HTML for every building block of the template. Copy these snippets and
change only the text, IDs, and links. The template styles exactly these
classes; anything else renders unstyled. Diagrams have their own file,
[diagrams.md](diagrams.md).

## Contents

- [What the template does for you](#what-the-template-does-for-you)
- [Header](#header)
- [Sections and subsections](#sections-and-subsections)
- [Chips and IDs](#chips-and-ids)
- [Links, terms, and tooltips](#links-terms-and-tooltips)
- [Callouts](#callouts)
- [Decision cards](#decision-cards)
- [Panels](#panels)
- [Items](#items)
- [Stats](#stats)
- [Tables](#tables)
- [Code](#code)
- [Glossary, references, and history](#glossary-references-and-history)
- [Steps and tabs](#steps-and-tabs)

## What the template does for you

Its script builds these from your content, so do not write them:

- The table of contents, from each `<section id>` and its `<h2>`, plus every
  `<h3 id>` that is not inside a card, item, panel, or tab. It shows the
  status and version from the header, counts the cards and items in each
  section, and highlights where the reader is. On a phone it becomes a
  "Contents" menu.
- `#` links next to headings, a wrapper that scrolls wide tables, and a copy
  button and language label on code blocks.
- Tooltips for every link to a card, item, failure row, or glossary term,
  built from the target's title and first sentence.
- Light and dark themes, with a switch at the bottom of the contents.
- A short highlight on the target when the reader follows a link.

## Header

```html
<header class="dd-header" id="top">
  <p class="eyebrow">Design document</p>
  <h1>Publish order events with a transactional outbox</h1>
  <p class="subtitle">Every committed order produces exactly one OrderPlaced event.</p>
  <dl class="meta">
    <div><dt>Status</dt><dd><span class="chip info" data-status>In review</span></dd></div>
    <div><dt>Version</dt><dd><span data-version>0.3</span></dd></div>
    <div><dt>Updated</dt><dd>2026-11-06</dd></div>
    <div><dt>Authors</dt><dd>Ana Ruiz (Orders)</dd></div>
    <div><dt>Reviewers</dt><dd>Marta Gil (Platform)</dd></div>
  </dl>
</header>
```

`data-status` and `data-version` are required: the contents and the checker
read them. The chip color for each status is in
[Versioning](../SKILL.md#versioning). For a superseded document, put this
first inside the header:

```html
<aside class="callout danger">
  <p class="callout-title">Superseded</p>
  <p>Replaced by <a href="order-events-v2.html">Order events v2</a> on 2027-03-01.</p>
</aside>
```

## Sections and subsections

```html
<section id="architecture">
  <h2>Architecture</h2>
  <p>One sentence that leads into the diagram.</p>
  <h3 id="how-commit">The order and its event commit together</h3>
  <p>...</p>
</section>
```

Sections are direct children of `<main>`, with the `id`s from
[SKILL.md](../SKILL.md#sections). `data-toc="Short name"` on a section or
`h3` shortens its entry in the contents. `<p class="lead">` makes an
opening paragraph slightly larger; use it in the Overview.

## Chips and IDs

```html
<span class="chip bad">Blocking</span>
<span class="id">G1</span>
<a class="id" href="#g1">G1</a>
```

Chips label a state. Colors: `good` (green), `warn` (amber), `bad` (red),
`info` (blue), and no class for neutral gray.

An `id` chip shows a stable ID. Its color comes from the first letter: `D`
and `A` blue, `F` red, `G` amber, `Q` purple, others gray. As a link, it
shows the target's title and summary on hover. Use it every time the text
refers to a decision, alternative, failure, gap, question, or parking-lot
item.

## Links, terms, and tooltips

```html
<a class="term" href="#term-wal">WAL</a>
<span data-tip="Debezium 2.7, one task">Debezium connector</span>
<span data-tip-title="Retention" data-tip="7 days, set by retention.ms">retention</span>
```

- `a.term` links to a glossary entry and shows its definition on hover. Use
  it on the first mention of a term in each section.
- `data-tip` adds a tooltip to any element; `data-tip-title` adds a bold
  first line. Keep tooltips to one or two sentences, and never put the only
  copy of something important in one.
- Plain links to sections need nothing extra: `<a href="#rollout">rollout</a>`.

## Callouts

```html
<aside class="callout warning">
  <p class="callout-title">Turning on logical replication reboots the database</p>
  <p>RDS applies the change only after a reboot; on staging writes failed for 95 s.</p>
</aside>
```

| Class | Use for |
| --- | --- |
| `note` | Context the reader should not miss, such as what reviewers must decide |
| `tip` | A recommended practice |
| `warning` | A risk, an irreversible step, a surprising cost |
| `danger` | Data loss, outages, security problems |

The title states the point, so a reader who skips the body still gets it.

## Decision cards

```html
<div class="cards">
  <article class="card" id="d1">
    <div class="card-head"><span class="id">D1</span></div>
    <h3>The order and its event commit together</h3>
    <p>Orders API inserts the event into an outbox table in the same transaction as the order.</p>
    <p class="more"><a href="#how-commit">How it works</a><a href="#alt-consistency">Alternatives</a></p>
  </article>
</div>
```

The card `id` is the lowercase ID. Add a chip to `card-head` for a changed
decision, for example `<span class="chip">Reversed in 2.0</span>`.

## Panels

```html
<div class="panels">
  <div class="panel good">
    <h3>Strengths</h3>
    <ul><li>An event exists if and only if its order committed (<a class="id" href="#d1">D1</a>).</li></ul>
  </div>
  <div class="panel warn">
    <h3>Weaknesses</h3>
    <ul><li>Kafka Connect is a new deployment to run (<a class="id" href="#q1">Q1</a>).</li></ul>
  </div>
</div>
```

Classes color the heading: `good`, `warn`, `bad`, `info`, `neutral`. Use
`good` and `warn` for strengths and weaknesses, `good` and `neutral` for
goals and non-goals.

## Items

One component for alternatives, known gaps, open questions, and the parking
lot.

```html
<div class="items">
  <article class="item" id="g1">
    <div class="item-head"><span class="id">G1</span><h3>Shipping does not drop duplicates</h3><span class="chip bad">Blocks step 5</span></div>
    <p>After a connector restart, order 84121 would ship twice.</p>
    <dl class="facts">
      <dt>Options</dt><dd>A processed_events table, or a unique constraint on shipments(order_id).</dd>
      <dt>Proposal</dt><dd>The unique constraint.</dd>
      <dt>Owner</dt><dd>Luis Ortega (Shipping)</dd>
    </dl>
  </article>
</div>
```

The first `<p>` is the summary that tooltips show, so make it stand on its
own. The `facts` keys per section:

| Section | ID | Facts |
| --- | --- | --- |
| Alternatives | `a1` | Why not, Better if |
| Known gaps | `g1` | Options, Proposal, Owner |
| Open questions | `q1` | Who can answer, Needed by |
| Parking lot | `p1` | Revisit when |

A resolved item keeps its place with `class="item resolved"`, and a line at
the end of its summary such as "Resolved in 0.4: see D7."

## Stats

```html
<div class="stats">
  <div class="stat"><b>380 ms</b><span>Commit to topic, p99, on staging</span></div>
  <div class="stat"><b>≈ 6 h</b><span>Connector downtime before the slot reaches 50 GB</span></div>
</div>
```

For numbers a reader should remember: targets, measurements, limits. Two to
six tiles.

## Tables

Write a plain `<table>` with `<thead>` and `<tbody>`; the template wraps and
styles it.

Comparison table for alternatives:

```html
<table>
  <thead><tr><th>Criterion</th><th class="chosen">Debezium (<a class="id" href="#d2">D2</a>)</th><th>Polling (<a class="id" href="#a3">A3</a>)</th></tr></thead>
  <tbody>
    <tr><th>Latency, p99</th><td class="yes chosen">380 ms on staging</td><td class="partial">1–5 s</td></tr>
    <tr><th>New infrastructure</th><td class="no chosen">Kafka Connect</td><td class="yes">None</td></tr>
  </tbody>
</table>
```

`yes`, `no`, and `partial` add ✓, ✗, and ~ in green, red, and amber.
`chosen` tints the chosen option's column; put it on the header cell and on
every cell of that column.

Failure table, one row per failure:

```html
<table>
  <thead><tr><th>ID</th><th>Failure</th><th>What users see</th><th>How we detect it</th><th>What to do</th></tr></thead>
  <tbody>
    <tr id="f1"><td><span class="id">F1</span></td><td><strong>Connector stops</strong></td><td>Invoices are late; orders still succeed.</td><td>Task state not RUNNING for 2 min.</td><td>Restart the task (<a href="#runbook">runbook</a>).</td></tr>
  </tbody>
</table>
```

A link to `#f1` shows the second and third cells as its tooltip.

## Code

```html
<figure class="code">
  <figcaption>db/migration/V42__outbox.sql</figcaption>
<pre><code class="language-sql">CREATE TABLE outbox (
  id uuid PRIMARY KEY
);</code></pre>
</figure>
```

- `class="language-..."` is required. Common values: `java`, `kotlin`,
  `python`, `go`, `typescript`, `javascript`, `sql`, `yaml`, `json`, `xml`
  (also HTML), `bash`, `properties`, `ini` (also TOML), `protobuf`,
  `dockerfile`, `diff`, `text`.
- Escape `<`, `>`, and `&` inside code as `&lt;`, `&gt;`, `&amp;`.
- Start the code right after `<code ...>` and end it right before `</code>`;
  any extra blank line shows up in the block.
- The `figure.code` wrapper and caption are optional. Without them, write
  only the `<pre><code>`.

## Glossary, references, and history

```html
<dl class="glossary">
  <dt id="term-wal">WAL</dt><dd>Write-ahead log: PostgreSQL's record of every change.</dd>
</dl>

<ul class="refs">
  <li><a href="https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html">Debezium: Outbox event router</a><span>Every routing option of the connector config.</span></li>
</ul>

<table>
  <thead><tr><th>Version</th><th>Date</th><th>Status</th><th>Author</th><th>Changes</th></tr></thead>
  <tbody>
    <tr><td>0.3</td><td>2026-11-06</td><td>In review</td><td>Ana Ruiz</td><td>Added <a class="id" href="#d6">D6</a>.</td></tr>
  </tbody>
</table>
```

## Steps and tabs

A walkthrough is a numbered list of steps. With `data-for`, hovering a step
highlights nodes and arrows of a box diagram; see
[diagrams.md](diagrams.md#walkthroughs).

```html
<ol class="walkthrough" data-for="fig-architecture">
  <li data-hl="checkout>api">Checkout sends <code>POST /orders</code> to Orders API.</li>
</ol>
```

For ordinary ordered steps, such as rollout steps, use a plain `<ol>`.

`split` puts a narrow diagram and its walkthrough side by side on wide
screens; use it only for diagrams of three columns or fewer.

```html
<div class="split">
  <figure class="dg" id="fig-flow">...</figure>
  <ol class="walkthrough" data-for="fig-flow">...</ol>
</div>
```

Tabs show views of the same thing one at a time, such as "Today" and
"Proposed", or the states of a rollout:

```html
<div class="tabs">
  <div data-tab="Today">...</div>
  <div data-tab="Proposed">...</div>
</div>
```

Do not hide content a reader must see in a tab other than the first.
