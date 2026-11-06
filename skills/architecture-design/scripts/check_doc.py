#!/usr/bin/env python3
"""Check a design document built from assets/template.html.

Usage:
    python3 check_doc.py DOC.html           # report errors and warnings
    python3 check_doc.py DOC.html --sync    # also restore the template's CSS and JS

Exit code 0 when there are no errors, 1 when there are errors, 2 on bad usage.
Uses only the Python standard library.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"

# Blocks owned by the template. The document must carry them unchanged.
TEMPLATE_BLOCKS = [("script", "dd-theme"), ("style", "dd-style"), ("script", "dd-script")]

SECTION_ORDER = [
    "overview", "problem", "decisions", "architecture", "tradeoffs", "alternatives",
    "operations", "gaps", "questions", "parking-lot", "glossary", "references", "history",
]
REQUIRED = {"overview", "problem", "decisions", "architecture", "tradeoffs", "alternatives", "operations", "history"}

# Section id -> (element kind, id pattern) for the stable IDs that section owns.
ID_RULES = {
    "decisions": ("card", r"d\d+"),
    "alternatives": ("item", r"a\d+"),
    "gaps": ("item", r"g\d+"),
    "questions": ("item", r"q\d+"),
    "parking-lot": ("item", r"p\d+"),
}
STATUSES = {"Draft", "In review", "Accepted", "Superseded", "Rejected"}
ALLOWED_HOSTS = ("https://fonts.googleapis.com", "https://fonts.gstatic.com")
STYLE_ATTR_OK = re.compile(r"^\s*(--[\w-]+\s*:\s*[^;]+;?\s*)*$")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def extract(html: str, tag: str, id_: str) -> re.Match | None:
    return re.search(rf'(<{tag}\b[^>]*\bid="{id_}"[^>]*>)(.*?)(</{tag}>)', html, re.S)


class Doc(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict]] = []
        self.ids: dict[str, list[int]] = {}
        self.hrefs: list[tuple[str, int, set[str]]] = []
        self.sections: list[tuple[str, int]] = []
        self.current_section: str | None = None
        self.section_items: dict[str, list[tuple[str, str, int]]] = {}
        self.code_without_lang: list[int] = []
        self.figures: list[dict] = []
        self.walkthroughs: list[tuple[str, list[str], int]] = []
        self.refs: list[tuple[str, int]] = []
        self.bad_style_attrs: list[tuple[str, int]] = []
        self.external: list[tuple[str, int]] = []
        self.inline_styles: list[int] = []
        self.inline_scripts: list[tuple[str | None, int]] = []
        self.status: str | None = None
        self.version: str | None = None
        self.history_first_version: str | None = None
        self._capture: str | None = None
        self._buf: list[str] = []
        self._history_rows = 0
        self._in_history_tbody = False
        self._in_history_cell = 0
        self.dt_ids: set[str] = set()
        self.tags_in_mermaid: list[tuple[str, int]] = []

    # Helpers
    def _line(self) -> int:
        return self.getpos()[0]

    def _inside(self, tag: str, cls: str | None = None) -> bool:
        for t, a in self.stack:
            if t == tag and (cls is None or cls in a.get("class", "").split()):
                return True
        return False

    def _figure(self) -> dict | None:
        for t, a in reversed(self.stack):
            if t == "figure" and "dg" in a.get("class", "").split():
                return a.get("_fig")
        return None

    def handle_starttag(self, tag: str, attrs_list: list) -> None:
        attrs = {k: (v or "") for k, v in attrs_list}
        line = self._line()
        classes = set(attrs.get("class", "").split())
        if self._inside("pre", "mermaid"):
            self.tags_in_mermaid.append((tag, line))

        if "id" in attrs:
            self.ids.setdefault(attrs["id"], []).append(line)
        if tag == "dt" and "id" in attrs:
            self.dt_ids.add(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.hrefs.append((attrs["href"][1:], line, classes))
        if "style" in attrs and not STYLE_ATTR_OK.match(attrs["style"]):
            self.bad_style_attrs.append((attrs["style"], line))
        if tag == "style" and attrs.get("id") != "dd-style":
            self.inline_styles.append(line)
        if tag == "script":
            if attrs.get("src"):
                self.external.append((attrs["src"], line))
            elif attrs.get("id") not in ("dd-theme", "dd-script"):
                self.inline_scripts.append((attrs.get("id"), line))
        if tag == "link" and attrs.get("href", "").startswith("http") and not attrs["href"].startswith(ALLOWED_HOSTS):
            self.external.append((attrs["href"], line))

        if tag == "section" and self.stack and self.stack[-1][0] == "main" and "id" in attrs:
            self.sections.append((attrs["id"], line))
            self.current_section = attrs["id"]
            self.section_items.setdefault(attrs["id"], [])
        if tag == "article" and self.current_section and ({"card", "item"} & classes):
            kind = "card" if "card" in classes else "item"
            self.section_items[self.current_section].append((kind, attrs.get("id", ""), line))

        if tag == "code" and self.stack and self.stack[-1][0] == "pre":
            if "mermaid" not in self.stack[-1][1].get("class", "") and not re.search(r"\blanguage-[\w+#-]+", attrs.get("class", "")):
                self.code_without_lang.append(line)

        if tag == "figure" and "dg" in classes:
            fig = {"id": attrs.get("id"), "line": line, "nodes": {}, "edges": [], "groups": []}
            attrs["_fig"] = fig
            self.figures.append(fig)
        fig = self._figure() if tag != "figure" else None
        if fig is not None:
            if "dg-node" in classes:
                nid = attrs.get("data-id", "")
                if not nid:
                    fig.setdefault("errors", []).append((line, "dg-node without data-id"))
                elif nid in fig["nodes"]:
                    fig.setdefault("errors", []).append((line, f'duplicate data-id "{nid}"'))
                fig["nodes"][nid] = line
                for r in attrs.get("data-refs", "").split():
                    self.refs.append((r.lower(), line))
            if "dg-edge" in classes:
                fig["edges"].append((attrs.get("data-from", ""), attrs.get("data-to", ""), line))
            if "dg-group" in classes:
                fig["groups"].append((attrs.get("data-members", "").split(), line))

        if tag == "ol" and "walkthrough" in classes and attrs.get("data-for"):
            self.walkthroughs.append((attrs["data-for"], [], line))
        if tag == "li" and self.walkthroughs and self._inside("ol", "walkthrough"):
            self.walkthroughs[-1][1].extend(attrs.get("data-hl", "").split())

        if "data-status" in attrs:
            self._capture, self._buf = "status", []
        if "data-version" in attrs:
            self._capture, self._buf = "version", []
        if tag == "tbody" and self.current_section == "history":
            self._in_history_tbody = True
        if tag == "tr" and self._in_history_tbody:
            self._history_rows += 1
        if tag in ("td", "th") and self._in_history_tbody and self._history_rows == 1 and self.history_first_version is None:
            self._capture, self._buf = "history", []

        if tag not in VOID:
            self.stack.append((tag, attrs))

    def handle_startendtag(self, tag: str, attrs_list: list) -> None:
        self.handle_starttag(tag, attrs_list)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        if self._capture and tag in ("span", "td", "th", "dd"):
            text = "".join(self._buf).strip()
            if self._capture == "status":
                self.status = text
            elif self._capture == "version":
                self.version = text
            elif self._capture == "history":
                self.history_first_version = text
            self._capture = None
        if tag == "tbody":
            self._in_history_tbody = False
        if tag == "section":
            self.current_section = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf.append(data)


def check(path: Path, sync: bool) -> int:
    html = path.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    def err(line: int | None, msg: str) -> None:
        errors.append(f"{path}:{line or '-'}: error: {msg}")

    def warn(line: int | None, msg: str) -> None:
        warnings.append(f"{path}:{line or '-'}: warning: {msg}")

    # Template-owned blocks
    changed = False
    for tag, id_ in TEMPLATE_BLOCKS:
        mine, theirs = extract(html, tag, id_), extract(template, tag, id_)
        if theirs is None:
            err(None, f"template is missing <{tag} id=\"{id_}\">")
            continue
        if mine is None:
            err(None, f'missing <{tag} id="{id_}"> from the template; copy the template instead of writing the page by hand')
            continue
        if mine.group(2) != theirs.group(2):
            if sync:
                html = html[: mine.start(2)] + theirs.group(2) + html[mine.end(2):]
                changed = True
            else:
                err(html.count("\n", 0, mine.start()) + 1, f'<{tag} id="{id_}"> differs from the template; run with --sync to restore it')
    if changed:
        path.write_text(html, encoding="utf-8")
        print(f"{path}: restored the template's CSS and JS")

    if "{{" in html:
        for m in re.finditer(r"\{\{[^}]*\}\}", html):
            err(html.count("\n", 0, m.start()) + 1, f"placeholder left: {m.group(0)[:60]}")

    if "<!-- CONTENT START" not in html or "<!-- CONTENT END -->" not in html:
        warn(None, "CONTENT START/END markers are missing")

    doc = Doc()
    doc.feed(html)

    # Sections
    found = [s for s, _ in doc.sections]
    for s in sorted(REQUIRED - set(found)):
        err(None, f'required section <section id="{s}"> is missing')
    known = [s for s in found if s in SECTION_ORDER]
    if known != sorted(known, key=SECTION_ORDER.index):
        err(None, "sections are out of order; expected: " + ", ".join(s for s in SECTION_ORDER if s in found))
    for s, line in doc.sections:
        if s not in SECTION_ORDER:
            warn(line, f'section "{s}" is not a standard section; put its content in a standard section if one fits')

    # IDs and links
    for id_, lines in doc.ids.items():
        if len(lines) > 1:
            err(lines[1], f'duplicate id "{id_}" (first on line {lines[0]})')
    for target, line, classes in doc.hrefs:
        if target and target not in doc.ids:
            err(line, f'link to "#{target}", which does not exist')
        if "term" in classes and target not in doc.dt_ids:
            err(line, f'term link "#{target}" must point to a glossary <dt id="term-...">')
    for ref, line in doc.refs:
        if ref not in doc.ids:
            err(line, f'data-refs names "{ref.upper()}", which has no element with id "{ref}"')

    for section, (kind, pattern) in ID_RULES.items():
        for k, id_, line in doc.section_items.get(section, []):
            if k == kind and not re.fullmatch(pattern, id_ or ""):
                err(line, f'{kind} in "{section}" needs an id like "{pattern.replace(chr(92) + "d+", "1")}", found "{id_}"')

    # Code blocks
    for line in doc.code_without_lang:
        err(line, 'code block without class="language-..." (use language-text for plain text)')

    # Diagrams
    for m in re.finditer(r'<pre\b[^>]*\bclass="[^"]*\bmermaid\b[^"]*"[^>]*>\s*(\S+)', html):
        if m.group(1) != "sequenceDiagram":
            err(html.count("\n", 0, m.start()) + 1,
                f'Mermaid "{m.group(1)}": use Mermaid only for sequenceDiagram; draw architecture, '
                "decision trees, and state machines as box diagrams (references/diagrams.md)")
    for tag, line in doc.tags_in_mermaid:
        err(line, f"<{tag}> inside Mermaid source is read as HTML and disappears; write it escaped, for example &lt;br/&gt;")
    for fig in doc.figures:
        for line, msg in fig.get("errors", []):
            err(line, msg)
        for a, b, line in fig["edges"]:
            for n in (a, b):
                if n not in fig["nodes"]:
                    err(line, f'diagram edge refers to unknown node "{n}"')
        for members, line in fig["groups"]:
            if not members:
                err(line, "dg-group without data-members")
            for m in members:
                if m not in fig["nodes"]:
                    err(line, f'diagram group refers to unknown node "{m}"')
        if len(fig["nodes"]) > 14:
            warn(fig["line"], f"diagram has {len(fig['nodes'])} nodes; split it so each diagram shows one idea")
    figs = {f["id"]: f for f in doc.figures if f["id"]}
    for fid, keys, line in doc.walkthroughs:
        fig = figs.get(fid)
        if not fig:
            err(line, f'walkthrough data-for="{fid}" does not name a box diagram')
            continue
        for k in keys:
            for n in k.split(">"):
                if n not in fig["nodes"]:
                    err(line, f'walkthrough step refers to unknown node "{n}"')

    # Status and version
    if doc.status is None:
        err(None, "header has no status chip (data-status)")
    elif doc.status not in STATUSES:
        warn(None, f'status "{doc.status}" is not one of: ' + ", ".join(sorted(STATUSES)))
    if doc.version is None:
        err(None, "header has no version (data-version)")
    elif not re.fullmatch(r"\d+\.\d+", doc.version):
        err(None, f'version "{doc.version}" must look like MAJOR.MINOR, for example 0.3 or 1.2')
    if doc.history_first_version is not None and doc.version and doc.history_first_version != doc.version:
        err(None, f"header version {doc.version} differs from the newest history row {doc.history_first_version}; the newest row goes first")

    # Styling stays in the template
    for style, line in doc.bad_style_attrs:
        err(line, f'style attribute "{style[:50]}" sets more than custom properties; use the template classes')
    for line in doc.inline_styles:
        err(line, "extra <style> block; the template's CSS is the only styling")
    for id_, line in doc.inline_scripts:
        warn(line, "extra inline <script>; the template's script already builds the page")
    for src, line in doc.external:
        warn(line, f"external resource {src}; the template loads its own libraries")

    for line in warnings + errors:
        print(line)
    print(f"{path}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if len(args) != 1 or flags - {"--sync"}:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    path = Path(args[0])
    if not path.is_file():
        print(f"{path}: no such file", file=sys.stderr)
        return 2
    return check(path, "--sync" in flags)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
