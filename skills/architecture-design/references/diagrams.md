# Diagrams

Diagrams carry the design; text fills in what they can't show. The template
has two kinds:

| Kind | Use for |
| --- | --- |
| Box diagram (`figure.dg`) | Everything except sequences: architecture, failure maps, rollout states, decision trees, and state machines |
| Mermaid (`figure.mmd`) | Sequence diagrams only: who calls whom, in what order |

Box diagrams put each box where you choose, match the page's look, and have
tooltips, linked badges, and highlighted steps. Mermaid lays out its own
diagrams, which works well for sequences but produces tangled decision
trees and state machines, so `check_doc.py` rejects any other Mermaid type.
For a data model, use a table or the schema itself in a code block.

## Contents

- [Rules for every diagram](#rules-for-every-diagram)
- [Box diagrams](#box-diagrams)
- [Decision trees](#decision-trees)
- [State machines](#state-machines)
- [Walkthroughs](#walkthroughs)
- [Layout tips](#layout-tips)
- [Sequence diagrams with Mermaid](#sequence-diagrams-with-mermaid)

## Rules for every diagram

- **One idea per diagram.** The big picture, one flow, one decision, or one
  failure view. More than about 12 boxes means two ideas; split them.
- **Real names.** A box's title is the name the team uses for the component
  (`Orders API`, `orders.events.v1`), the same in every diagram and
  sentence. Its subtitle is its role, in a few words.
- **Label what flows.** An arrow's label is the protocol, the data, or the
  condition (`HTTPS`, `WAL`, `yes`), not a verb like "calls".
- **Color means one thing.** The kind of a box sets its color, and the
  legend explains it. Never color for decoration.
- **Details on hover.** Versions, ports, counts, and config keys go in
  `data-tip`, not in the box. A box has at most three short lines.
- **A caption that says what to notice.** One or two sentences: "Requests
  stop at PostgreSQL; everything to the right of it is asynchronous." Not
  "Architecture diagram".
- **An `id` on every figure**, starting with `fig-`, so text and
  walkthroughs can point to it.

## Box diagrams

```html
<figure class="dg" id="fig-architecture" data-legend="solid=Synchronous call; dashed=Asynchronous stream">
  <div class="dg-canvas" style="--dg-cols: 4">
    <div class="dg-group" data-label="Orders service" data-members="api pg"></div>
    <div class="dg-node external" data-id="checkout" style="--r: 1; --c: 1"><strong>Checkout</strong><span>web and mobile</span></div>
    <div class="dg-node changed" data-id="api" style="--r: 1; --c: 2" data-refs="D1" data-tip="Spring Boot 3, 3 replicas."><strong>Orders API</strong><span>writes order + outbox</span></div>
    <div class="dg-node" data-id="pg" style="--r: 1; --c: 3"><strong>PostgreSQL</strong><span><code>orders</code>, <code>outbox</code></span></div>
    <div class="dg-node new" data-id="connect" style="--r: 1; --c: 4" data-refs="D2"><strong>Debezium</strong><span>on Kafka Connect</span></div>
    <i class="dg-edge" data-from="checkout" data-to="api" data-label="HTTPS"></i>
    <i class="dg-edge" data-from="api" data-to="pg" data-label="SQL" data-tip="One transaction: INSERT order, INSERT outbox, DELETE outbox."></i>
    <i class="dg-edge dashed" data-from="pg" data-to="connect" data-label="WAL"></i>
  </div>
  <figcaption>Requests stop at PostgreSQL; Debezium reads its log asynchronously.</figcaption>
</figure>
```

The canvas is a grid. Each box sits in a cell; groups and arrows are drawn
around and between the boxes by the template's script.

### Canvas

| Setting | Default | Meaning |
| --- | --- | --- |
| `--dg-cols` | 4 | Number of columns |
| `--dg-min` | 150px | Minimum column width; the diagram scrolls sideways when the page is narrower |
| `--dg-col-gap` | 64px | Space between columns, where horizontal arrow labels go |
| `--dg-row-gap` | 64px | Space between rows |

Set them in the canvas `style` attribute. Custom properties are the only
thing a `style` attribute may contain.

### Nodes

`<div class="dg-node KIND" data-id="ID" style="--r: ROW; --c: COLUMN">`
with a `<strong>` title and an optional `<span>` subtitle.

| Attribute | Meaning |
| --- | --- |
| `data-id` | Unique within the figure; arrows, groups, and walkthroughs use it |
| `--r`, `--c` | Row and column, from 1 |
| `--span` | How many columns the box covers, default 1 |
| `data-tip` | Tooltip text |
| `data-refs` | Space-separated IDs, such as `D1 F2`, shown as linked badges on the box's corner |

Kinds for architecture diagrams:

| Kind | Color | Use for |
| --- | --- | --- |
| `new` | Green | Added by this design |
| `changed` | Green, dashed border | Exists and this design changes it |
| (none) | Blue | Exists and does not change; also a plain state in a state machine |
| `external` | Gray | Outside the team's control: clients, cloud services, other companies |
| `resource` | Purple | Configuration or data rather than a running process: a topic, a table, a Kubernetes resource |
| `removed` | Red, dashed, crossed out | Removed by this design |

Kinds for decision trees, state machines, and annotations:

| Kind | Looks like | Use for |
| --- | --- | --- |
| `decision` | White with a blue border | A yes-or-no check in a decision tree |
| `good` | Green | A successful outcome, or a healthy state |
| `bad` | Red | A failed or rejected outcome, or a failure state |
| `note` | Amber sticky note | A remark attached to a box with an arrow that has `data-dir="none"` |
| `start` | Filled dot, no text | Where a state machine begins |
| `end` | Dot in a ring, no text | Where a state machine ends |

`decision`, `note`, `start`, and `end` never appear in the legend.

### Arrows

`<i class="dg-edge" data-from="ID" data-to="ID"></i>`, placed inside the
canvas after the nodes.

| Attribute | Meaning |
| --- | --- |
| `dashed` (class) | Dashed line; by default "asynchronous or control flow" in the legend |
| `data-label` | Short text on the arrow |
| `data-tip` | Tooltip on the arrow and its label |
| `data-dir` | `both` for arrowheads on both ends, `none` for a plain line, such as a line to a note |
| `data-route` | `auto` (default), `straight`, `elbow` (horizontal, then vertical), or `elbow-v` (vertical, then horizontal) |
| `data-offset` | Shift the line sideways, in pixels, to separate two arrows between the same boxes |
| `data-side` | For an arrow from a box to itself: `right` (default), `left`, `top`, or `bottom` |
| `data-label-at="center"` | Put the label on the line instead of beside it |

With `auto`, boxes in the same row or column are joined by a straight
horizontal or vertical line, and other pairs by a diagonal line. Labels on
horizontal lines sit above the line, labels on vertical lines to its right.

For two arrows in opposite directions between the same boxes, give one
`data-offset="-12"` and the other `data-offset="12"`. Each label then moves
to its own side: above and below a horizontal pair, left and right of a
vertical pair.

An arrow whose `data-from` and `data-to` are the same box draws a loop on
the side named by `data-side`, with its label past the loop.

### Groups

`<div class="dg-group" data-label="Kafka platform" data-members="connect topic"></div>`
draws a dashed frame around the listed boxes, with the label in its top
corner. Use groups for where things run (a cluster, a namespace, outside the
network) or who owns them. A group whose members include another group's
members is drawn around it. Add the class `plain` for a label without a
frame, for example "Data plane" inside a cluster frame.

The members of a group must form a rectangle of cells with no other box
inside, or the frame will cover boxes that are not members.

### Legend

The template adds a legend for the node kinds the diagram uses, and for the
line styles when it uses dashed arrows. Rename an entry, or name the solid
and dashed lines, with `data-legend` on the figure:

```html
<figure class="dg" id="fig-x" data-legend="solid=Record path; dashed=Schema lookups; resource=Kubernetes resource">
```

Keys are the node kinds and `solid` or `dashed`. `data-legend="none"`
hides the legend.

## Decision trees

Put the checks in the middle column, one per row, so the path that
succeeds runs straight down. Put each outcome beside its check: on the left
or the right, never below another check. A check can have up to three exits
this way: left, right, and down.

```html
<figure class="dg" id="fig-billing-checks" data-legend="good=Handled; bad=Sent to the dead-letter topic">
  <div class="dg-canvas" style="--dg-cols: 3; --dg-row-gap: 48px">
    <div class="dg-node good" data-id="skip" style="--r: 1; --c: 1"><strong>Skip</strong><span>already processed</span></div>
    <div class="dg-node decision" data-id="seen" style="--r: 1; --c: 2"><strong>1 · event_id seen before?</strong></div>
    <div class="dg-node decision" data-id="version" style="--r: 2; --c: 2"><strong>2 · schema_version known?</strong></div>
    <div class="dg-node bad" data-id="dlq" style="--r: 2; --c: 3"><strong>Dead-letter topic</strong></div>
    <div class="dg-node good" data-id="invoice" style="--r: 3; --c: 2"><strong>Create the invoice</strong></div>
    <i class="dg-edge" data-from="seen" data-to="skip" data-label="yes"></i>
    <i class="dg-edge" data-from="seen" data-to="version" data-label="no"></i>
    <i class="dg-edge" data-from="version" data-to="dlq" data-label="no"></i>
    <i class="dg-edge" data-from="version" data-to="invoice" data-label="yes"></i>
  </div>
  <figcaption>Each check either stops the event at its side or passes it down.</figcaption>
</figure>
```

Number the checks in their titles (`1 ·`, `2 ·`) when the text refers to
them. When two outcomes are the same, such as two different checks that
both reject a record, draw one box for each check anyway: arrows that cross
the tree to reach a shared box are harder to follow than a repeated box.

## State machines

Put the main state in the middle, the `start` dot before it, and the other
states around it. A transition that keeps the state the same, such as
"event received, map updated", is a loop on the state's box. Attach a note
with a plain dashed line.

```html
<figure class="dg" id="fig-task-states" data-legend="none">
  <div class="dg-canvas" style="--dg-cols: 3">
    <div class="dg-node start" data-id="start" style="--r: 1; --c: 1"></div>
    <div class="dg-node good" data-id="running" style="--r: 1; --c: 2"><strong>RUNNING</strong></div>
    <div class="dg-node bad" data-id="failed" style="--r: 2; --c: 2"><strong>FAILED</strong></div>
    <div class="dg-node note" data-id="note" style="--r: 2; --c: 3"><span>While not RUNNING, the slot keeps WAL.</span></div>
    <i class="dg-edge" data-from="start" data-to="running" data-label="created"></i>
    <i class="dg-edge" data-from="running" data-to="running" data-side="top" data-label="publish events"></i>
    <i class="dg-edge" data-from="running" data-to="failed" data-offset="-12" data-label="error"></i>
    <i class="dg-edge" data-from="failed" data-to="running" data-offset="12" data-label="restart"></i>
    <i class="dg-edge dashed" data-from="failed" data-to="note" data-dir="none"></i>
  </div>
  <figcaption>The task leaves RUNNING only on an error, and only a restart brings it back.</figcaption>
</figure>
```

## Walkthroughs

A walkthrough under a box diagram tells the main flow one step at a time.
Hovering a step highlights its boxes and arrows and dims the rest:

```html
<ol class="walkthrough" data-for="fig-architecture">
  <li data-hl="checkout>api">Checkout sends <code>POST /orders</code> to Orders API.</li>
  <li data-hl="api>pg">Orders API writes the order and its event in one transaction.</li>
  <li data-hl="topic>billing topic>shipping">Billing and Shipping consume the event.</li>
</ol>
```

`data-hl` lists arrows as `from>to` and boxes as plain IDs. An arrow brings
its two boxes with it. Each step is one sentence about what happens, not a
description of the box.

Hovering a box also highlights it and its arrows, so readers can explore a
diagram without a walkthrough.

## Layout tips

- **Read left to right, top to bottom.** Put the caller on the left and the
  data on the right, the main path in the first row, and secondary parts
  below.
- **Keep horizontal labels short**, about 10 characters, because they sit in
  the gap between columns. Put longer text in `data-tip`, or widen
  `--dg-col-gap`.
- **Align boxes that talk to each other** in the same row or column, so the
  arrow is straight. Use `elbow` when a diagonal would cross another box.
- **Leave a cell empty** rather than squeezing a box in; empty cells keep
  groups apart.
- **Check the result in a browser.** The checker validates IDs and links but
  can't see overlaps.

## Sequence diagrams with Mermaid

```html
<figure class="mmd" id="fig-duplicates">
<pre class="mermaid">
sequenceDiagram
  autonumber
  participant DBZ as Debezium
  participant K as orders.events.v1
  DBZ->>K: publish event 5f0c…
  Note over DBZ: stops before saving its position
</pre>
  <figcaption>A restart between steps 1 and 2 publishes the same event again.</figcaption>
</figure>
```

- `sequenceDiagram` must be the first word inside `<pre class="mermaid">`,
  written at the start of the line. Do not add `<code>` inside it.
- The template themes Mermaid to match the page, waits for the page font
  before drawing so no text is cut off, and redraws when the reader switches
  between light and dark. Do not add `%%{init}%%` or colors.
- The browser reads the source as HTML first, so escape `<` and `&` as
  `&lt;` and `&amp;`. A line break in a note is `&lt;br/&gt;`; a bare
  `<br/>` disappears.
- Use the same participant names as the box diagrams.
