# Diagrams

Diagrams carry the design; text fills in what they can't show. The template
has two kinds:

| Kind | Use for | Why |
| --- | --- | --- |
| Box diagram (`figure.dg`) | Architecture: components, where they run, who owns them, what flows between them, where failures start | You choose the layout, it matches the page's look, boxes and arrows have tooltips, and steps can highlight parts of it |
| Mermaid (`figure.mmd`) | Interactions over time (sequence), states, data models (ER), timelines | Mermaid lays these out better than a grid can |

## Contents

- [Rules for every diagram](#rules-for-every-diagram)
- [Box diagrams](#box-diagrams)
- [Walkthroughs](#walkthroughs)
- [Layout tips](#layout-tips)
- [Mermaid](#mermaid)

## Rules for every diagram

- **One idea per diagram.** The big picture, one flow, or one failure view.
  More than about 12 boxes means two ideas; split them.
- **Real names.** A box's title is the name the team uses for the component
  (`Orders API`, `orders.events.v1`), the same in every diagram and
  sentence. Its subtitle is its role, in a few words.
- **Label what flows.** An arrow's label is the protocol or the data
  (`HTTPS`, `WAL`, `publish`), not a verb like "calls".
- **Color means one thing.** The kind of a box (new, changed, existing,
  external, resource, removed) sets its color, and the legend explains it.
  Never color for decoration.
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

| Kind | Color | Use for |
| --- | --- | --- |
| `new` | Green | Added by this design |
| `changed` | Green, dashed border | Exists and this design changes it |
| (none) | Blue | Exists and does not change |
| `external` | Gray | Outside the team's control: clients, cloud services, other companies |
| `resource` | Purple | Configuration or data rather than a running process: a topic, a table, a Kubernetes resource |
| `removed` | Red, dashed, crossed out | Removed by this design |

### Arrows

`<i class="dg-edge" data-from="ID" data-to="ID"></i>`, placed inside the
canvas after the nodes.

| Attribute | Meaning |
| --- | --- |
| `dashed` (class) | Dashed line; by default "asynchronous or control flow" in the legend |
| `data-label` | Short text on the arrow |
| `data-tip` | Tooltip on the arrow and its label |
| `data-dir="both"` | Arrowheads on both ends |
| `data-route` | `auto` (default), `straight`, `elbow` (horizontal, then vertical), or `elbow-v` (vertical, then horizontal) |
| `data-offset` | Shift the line sideways, in pixels, to separate two arrows between the same boxes |
| `data-label-at="center"` | Put the label on the line instead of beside it |

With `auto`, boxes in the same row or column are joined by a straight
horizontal or vertical line, and other pairs by a diagonal line. Labels on
horizontal lines sit above the line, labels on vertical lines to its right.

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

## Mermaid

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

- Write the Mermaid source at the start of the line inside `<pre class="mermaid">`.
  Do not add `<code>` inside it.
- The template themes Mermaid to match the page and redraws it when the
  reader switches between light and dark, so do not add `%%{init}%%` or
  colors.
- The browser reads the source as HTML first, so escape `<` and `&` as
  `&lt;` and `&amp;`. A line break in a note is `&lt;br/&gt;`; a bare
  `<br/>` disappears.
- `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, and `gantt` work well.
  Use `flowchart` only for a decision tree or a pipeline that a grid can't
  lay out; for architecture, use a box diagram.
- Use the same participant names as the box diagrams.
