#!/usr/bin/env python3
"""Builds one printable PDF of the documentation from a tag or branch.

The docs are rendered by MkDocs itself from `git archive <ref>`, so the working
tree is neither read nor changed. The pages are then merged into a single HTML
book, which WeasyPrint lays out using print.css. WeasyPrint needs Pango and the
fonts print.css names: .github/workflows/docs.yml lists the packages.

Usage:
    pip install -r requirements-pdf.txt
    scripts/build-pdf.py --ref v0.8.4

    --out FILE       where to write the PDF (default: doriax-docs-<ref>.pdf)
    --strict         exit with an error if the build report shows a defect
    --only PATTERN   keep only pages whose source path contains PATTERN
                     (repeatable), for a quick look at the layout
"""
import argparse
import collections
import datetime
import html as htmllib
import io
import logging
import math
import os
import posixpath
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from mkdocs.commands.build import build as mkdocs_build
from mkdocs.config import load_config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Section
from weasyprint import CSS, HTML
from weasyprint.formatting_structure import boxes
from weasyprint.text.fonts import FontConfiguration

HERE = Path(__file__).resolve().parent

# Every tag the Markdown pipeline legitimately emits. Anything else in the HTML
# is text the Markdown parser mistook for a tag, see restore_lost_text().
HTML_TAGS = set(
    "a b blockquote br code dd del details div dl dt em h1 h2 h3 h4 h5 h6 hr i img input ins "
    "kbd label li mark ol p pre s small span strong sub summary sup table tbody td th thead tr u ul".split()
)
SHORT_CODE_LINES = 18  # blocks up to this long are kept on a single page
COMPACT_LINES = 42     # class pages up to this estimate may share a sheet
PAGE_TITLE_OVERRIDES = {"index.md": "Welcome"}
# Report entries that mean the PDF is wrong, as opposed to worth knowing about.
DEFECTS = (
    "Unresolved link",
    "Missing image",
    "Content outside the text area",
    "Link to a missing anchor (sent to the chapter start)",
    "API Index link to an unknown page",
    "API Index anchor not found (sent to the chapter start)",
    "Tab set with mismatched labels",
    "Card markup not recognised",
)
MONTHS = "January February March April May June July August September October November December".split()


class Report:
    """Everything worth a human look, printed once the build is done."""

    def __init__(self):
        self.items = collections.defaultdict(list)

    def add(self, kind, detail):
        self.items[kind].append(detail)

    def show(self):
        print("\n== Build report ==")
        for kind, details in self.items.items():
            print(f"{kind}: {len(details)}")
            for detail in details[:40]:
                print(f"    {detail}")
            if len(details) > 40:
                print(f"    ... and {len(details) - 40} more")


report = Report()


# ---------------------------------------------------------------- source & render

def export_ref(repo, ref, dest):
    tar = subprocess.run(["git", "-C", str(repo), "archive", ref], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as archive:
        archive.extractall(dest, filter="data")
    fmt = "--format=%h %ad"
    commit, date = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", fmt, "--date=short", ref],
        check=True, capture_output=True, text=True,
    ).stdout.split()
    day = datetime.date.fromisoformat(date)
    return commit, f"{MONTHS[day.month - 1]} {day.day}, {day.year}"


class Capture(BasePlugin):
    """Keeps the HTML MkDocs renders for each page, and the nav."""

    def __init__(self):
        self.pages = {}
        self.urls = {}
        self.nav = None

    def on_nav(self, nav, config, files):
        self.nav = nav
        return nav

    def on_page_content(self, html, page, config, files):
        self.pages[page.file.src_uri] = html
        self.urls[page.file.src_uri] = page.url
        return html


def render_docs(src, work):
    logging.getLogger("mkdocs").setLevel(logging.WARNING)
    cfg = load_config(config_file=str(src / "mkdocs.yml"), site_dir=str(work / "site"), strict=True)
    capture = Capture()
    cfg.plugins["print-capture"] = capture
    mkdocs_build(cfg)
    return cfg, capture


# ---------------------------------------------------------------- book structure

@dataclass
class Entry:
    src: str
    title: str
    duplicate: bool = False  # only a pointer: the page itself is placed elsewhere
    anchor: str = ""         # for a pointer into the middle of a page


@dataclass
class Group:
    title: str
    entries: list = field(default_factory=list)
    subgroups: list = field(default_factory=list)


@dataclass
class Part:
    title: str
    entries: list = field(default_factory=list)
    groups: list = field(default_factory=list)


def flatten(item):
    if isinstance(item, Section):
        for child in item.children:
            yield from flatten(child)
    else:
        yield item


def build_reference(section, capture, seen):
    """Lays out Reference from the API Index, the only complete list of classes.

    The nav lists about a third of the class pages. Groups the nav names come
    first, in its order, and then the groups only the API Index has.
    """
    part = Part(section.title)
    nav_groups = {}  # src -> (group, subgroup)
    order = []
    for child in section.children:
        if isinstance(child, Section):
            order.append(child.title)
            for grand in child.children:
                sub = grand.title if isinstance(grand, Section) else None
                for page in flatten(grand):
                    nav_groups.setdefault(page.file.src_uri, (child.title, sub))
        else:
            part.entries.append(Entry(child.file.src_uri, child.title))
            seen.add(child.file.src_uri)

    index_src = "reference/index.md"
    soup = BeautifulSoup(capture.pages[index_src], "html.parser")
    index_url = capture.urls[index_src]
    by_url = {capture.urls[s].rstrip("/"): s for s in capture.pages}
    groups = {}
    current = None
    target = None
    for el in soup.find_all(["h2", "h3", "ul"]):
        if el.name == "h2":
            current = groups.setdefault(heading_text(el), Group(heading_text(el)))
            target = current
        elif el.name == "h3":
            target = Group(heading_text(el))
            current.subgroups.append(target)
        elif current is not None and el.find_parent("ul") is None:  # nested lists come with their parent
            for link in el.find_all("a", href=True):
                path, _, anchor = link["href"].partition("#")
                src = by_url.get(posixpath.normpath(posixpath.join(index_url, path)))
                if src is None:
                    report.add("API Index link to an unknown page", link["href"])
                    continue
                pointer = bool(anchor) or src in seen
                target.entries.append(Entry(src, link.get_text(strip=True), duplicate=pointer, anchor=anchor))
                if not anchor:
                    seen.add(src)

    # Whatever the API Index leaves out goes to its nav group, or is placed by name.
    for src in sorted(capture.pages):
        if src in seen or not src.startswith("reference/"):
            continue
        title = page_title(capture.pages[src], src)
        group_name, sub_name = nav_groups.get(src, (None, None))
        if group_name is None:
            group_name = "Components" if src.endswith("component.md") else "Other"
        group = groups.setdefault(group_name, Group(group_name))
        if sub_name:
            found = [g for g in group.subgroups if g.title == sub_name]
            if found:
                group = found[0]
            else:
                group.subgroups.append(Group(sub_name))
                group = group.subgroups[-1]
        group.entries.append(Entry(src, title))
        group.entries.sort(key=lambda e: e.title.casefold())
        seen.add(src)
        report.add("Class page missing from the API Index, placed by rule", f"{src} -> {group_name}")

    for name in order:
        if name in groups:
            part.groups.append(groups.pop(name))
    part.groups.extend(groups.values())
    return part


def build_book(capture):
    seen = set()
    front = None
    parts = []
    for item in capture.nav.items:
        if not isinstance(item, Section):
            front = Entry(item.file.src_uri, PAGE_TITLE_OVERRIDES.get(item.file.src_uri, item.title))
            seen.add(item.file.src_uri)
            continue
        if item.title == "Reference":
            continue
        part = Part(item.title)
        for page in flatten(item):
            part.entries.append(Entry(page.file.src_uri, page.title, duplicate=page.file.src_uri in seen))
            seen.add(page.file.src_uri)
        parts.append(part)
    reference_section = next(i for i in capture.nav.items if isinstance(i, Section) and i.title == "Reference")
    reference = build_reference(reference_section, capture, seen)
    position = [i.title for i in capture.nav.items if isinstance(i, Section)].index("Reference")
    parts.insert(position, reference)

    missing = sorted(set(capture.pages) - seen)
    if missing:
        sys.exit(f"Pages with no place in the book: {missing}")
    return front, parts


def heading_text(el):
    for link in el.find_all("a", class_="headerlink"):
        link.decompose()
    return el.get_text(" ", strip=True)


def page_title(html, src):
    h1 = BeautifulSoup(html, "html.parser").find("h1")
    return heading_text(h1) if h1 else src


# ---------------------------------------------------------------- page clean-up

def restore_lost_text(html, src):
    """Signatures such as `std::function<void()> f` outside code spans reach the
    HTML as stray tags, which a browser then hides. Turn them back into text.
    The docs now escape these, but the tags published before that still need it."""
    restored = []

    def fix(match):
        if match.group(1) in HTML_TAGS:
            return match.group(0)
        restored.append(match.group(0))
        return "&lt;" + match.group(0)[1:-1].lstrip("/") + "&gt;" if not match.group(0).startswith("</") else ""

    html = re.sub(r"</?([A-Za-z][^\s<>/]*)[^<>]*>", fix, html)
    if restored:
        report.add("Signatures with template text restored (hidden on the website)",
                   f"{src}: {len(restored)} tag(s), e.g. {restored[0]}")
    escaped = html.count("\\&lt;")
    if escaped:
        report.add("Stray backslashes before < removed (visible on the website)", f"{src}: {escaped}")
        html = html.replace("\\&lt;", "&lt;")
    return html


CARD = re.compile(
    r'<p><a class="dx-card" href="([^"]*)"></p>\s*'
    r'<p class="dx-card-title">(.*?)</p>\s*'
    r'(<p class="dx-card-desc">.*?</p>)\s*'
    r"<p></a></p>",
    re.S,
)


CARD_ICON = re.compile(r'<div class="dx-card-icon">.*?</div>\s*', re.S)  # home page of the 0.7 docs


def rework_cards(html, src):
    """The Markdown pipeline splits each card's <a> across paragraphs, which only
    a forgiving browser puts back together. Link the card's title instead, so its
    page number lands right next to it."""
    html = CARD.sub(
        r'<div class="dx-card"><p class="dx-card-title"><a href="\1">\2</a></p>\3</div>', html
    )
    if 'class="dx-card"' in html.replace('<div class="dx-card">', ""):
        report.add("Card markup not recognised", src)
    return html


def chapter_id(src):
    return "p-" + re.sub(r"[^a-z0-9]+", "-", src.removesuffix(".md").lower())


def label_class(label):
    return {"C++": "lang-cpp", "Lua": "lang-lua"}.get(label, "lang-other")


def flatten_tabs(soup, new_tag):
    """A tab bar cannot be clicked on paper: print every tab, labelled."""
    for tab_set in soup.find_all(class_="tabbed-set"):
        labels = [lbl.get_text(strip=True) for lbl in tab_set.find(class_="tabbed-labels").find_all("label")]
        blocks = tab_set.find(class_="tabbed-content").find_all(class_="tabbed-block", recursive=False)
        if len(labels) != len(blocks):
            report.add("Tab set with mismatched labels", str(labels))
        tabs = new_tag("div", attrs={"class": "tabs"})
        for label, block in zip(labels, blocks):
            tab = new_tag("div", attrs={"class": "tab"})
            head = new_tag("div", attrs={"class": "tab-head"})
            chip = new_tag("span", attrs={"class": f"tab-label {label_class(label)}"})
            chip.string = label
            head.append(chip)
            tab.append(head)
            body = new_tag("div", attrs={"class": "tab-body"})
            only_code = all(
                isinstance(c, NavigableString) and not c.strip() or "highlight" in (getattr(c, "get", lambda *_: [])("class") or [])
                for c in block.contents
            )
            if not only_code:
                body["class"] = "tab-body text"
            for child in list(block.contents):
                body.append(child.extract())
            tab.append(body)
            tabs.append(tab)
            report.add("__tabs", label)
        tab_set.replace_with(tabs)


def mark_short_code(soup):
    for pre in soup.find_all("pre"):
        lines = pre.get_text().count("\n") + 1
        pre["data-lines"] = str(lines)
        if lines <= SHORT_CODE_LINES:
            pre["class"] = (pre.get("class") or []) + ["keep"]
            tab = pre.find_parent(class_="tab")
            if tab is not None:
                tab["class"] = tab["class"] + ["keep"]


def clean_tasks(soup, new_tag):
    for control in soup.find_all("label", class_="task-list-control"):
        box = control.find("input")
        mark = new_tag("span", attrs={"class": "check"})
        mark.string = "☑" if box is not None and box.has_attr("checked") else "☐"
        control.replace_with(mark)


def fix_images(soup, page_url, docs_dir, page):
    for img in soup.find_all("img"):
        rel = posixpath.normpath(posixpath.join(page_url, urllib.parse.unquote(img["src"])))
        path = docs_dir / rel
        if not path.is_file():
            report.add("Missing image", f"{page}: {img['src']}")
            continue
        img["src"] = path.as_uri()
        parent = img.parent
        if parent.name == "p" and all(
            getattr(c, "name", None) in ("img", "br") or (isinstance(c, NavigableString) and not c.strip())
            for c in parent.contents
        ):
            parent["class"] = (parent.get("class") or []) + ["figure"]


def estimate_lines(soup):
    """Rough printed height of a page, in body-text lines."""
    total = 0.0
    for el in soup.find_all(["p", "li", "tr", "pre", "h1", "h2", "h3", "h4", "img", "hr"]):
        if el.name == "pre":
            total += 1 + int(el.get("data-lines", 1)) * 0.82
        elif el.name == "tr":
            total += 1.2 + sum(len(td.get_text()) for td in el.find_all(["td", "th"])) / 200
        elif el.name == "img":
            total += 25
        elif el.name in ("h1", "h2"):
            total += 3
        elif el.name in ("h3", "h4"):
            total += 2
        elif el.name == "hr":
            total += 1
        elif not el.find_parent(["li", "td"]) or el.name == "li":
            total += 1 + math.floor(len(el.get_text()) / 110)
    return total


class Merger:
    """Cleans each page and turns its links and ids into book-wide ones."""

    def __init__(self, capture, docs_dir):
        self.capture = capture
        self.docs_dir = docs_dir
        self.by_url = {capture.urls[s].rstrip("/") or ".": s for s in capture.pages}
        self.soups = {}
        self.ids = {}

    def prepare(self, src):
        html = CARD_ICON.sub("", self.capture.pages[src])
        soup = BeautifulSoup(rework_cards(restore_lost_text(html, src), src), "html.parser")
        for link in soup.find_all("a", class_="headerlink"):
            link.decompose()
        flatten_tabs(soup, soup.new_tag)
        mark_short_code(soup)
        clean_tasks(soup, soup.new_tag)
        fix_images(soup, self.capture.urls[src], self.docs_dir, src)
        self.ids[src] = {el["id"] for el in soup.find_all(id=True)}
        self.soups[src] = soup

    def resolve(self, src, href):
        path, _, frag = href.partition("#")
        if not path:
            return src, frag
        joined = posixpath.normpath(posixpath.join(self.capture.urls[src], urllib.parse.unquote(path)))
        return self.by_url.get(joined), frag

    def rewrite_links(self, src, soup, present):
        pid = chapter_id(src)
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith(("http://", "https://", "mailto:")):
                self.footnote_url(link, soup)
                continue
            target, frag = self.resolve(src, href)
            if target is None:
                report.add("Unresolved link", f"{src}: {href}")
                link.unwrap()
                continue
            if target not in present:  # only in a partial --only build
                link.unwrap()
                continue
            if frag and frag not in self.ids[target]:
                report.add("Link to a missing anchor (sent to the chapter start)", f"{src}: {href}")
                frag = ""
            link["href"] = f"#{chapter_id(target)}" + (f"--{frag}" if frag else "")
            if target != src:
                link["class"] = (link.get("class") or []) + ["xref"]
        for el in soup.find_all(id=True):
            el["id"] = f"{pid}--{el['id']}"

    @staticmethod
    def footnote_url(link, soup):
        href = link["href"]
        shown = href.removeprefix("mailto:")
        if link.get_text(strip=True).rstrip("/") == shown.rstrip("/"):
            return
        note = soup.new_tag("span", attrs={"class": "ext-url"})
        note.string = shown
        link.insert_after(note)

    def chapter_html(self, entry, part_label, level, present, bands=()):
        src = entry.src
        soup = self.soups[src]
        self.rewrite_links(src, soup, present)
        for heading in soup.find_all(["h1", "h2", "h3"]):
            depth = {"h1": level, "h2": level + 1, "h3": level + 2}[heading.name]
            heading["class"] = (heading.get("class") or []) + [f"bl{min(depth, 5)}"]
        if entry.title in PAGE_TITLE_OVERRIDES.values():  # keep the outline in step with the contents
            soup.find("h1")["style"] = f'bookmark-label: "{entry.title}"'
        for table in soup.find_all("table"):
            first = table.find("tr")
            if first is not None and len(first.find_all(["td", "th"])) >= 5:
                table["class"] = (table.get("class") or []) + ["wide"]
        if src == "reference/index.md":
            wrapper = soup.new_tag("div", attrs={"class": "api-index"})
            for child in list(soup.contents):
                wrapper.append(child.extract())
            soup.append(wrapper)

        classes = ["chapter"]
        if src.startswith("reference/classes/") and estimate_lines(soup) <= COMPACT_LINES:
            classes.append("compact")
        mark = (
            f'<div class="chapter-mark" data-title="{htmllib.escape(entry.title)}" '
            f'data-part="{htmllib.escape(part_label)}"></div>'
        )
        band_html = "".join(bands)
        return (
            f'<section class="{" ".join(classes)}" id="{chapter_id(src)}">'
            f"{mark}{band_html}{soup}</section>\n"
        )


# ---------------------------------------------------------------- book assembly

def toc_item(entry, css=""):
    label = htmllib.escape(entry.title)
    attr = f' class="{css}"' if css else ""
    anchor = f"--{entry.anchor}" if entry.anchor else ""
    return f'<li{attr}><a href="#{chapter_id(entry.src)}{anchor}">{label}</a></li>'


def toc_list(entries, css=""):
    attr = f' class="{css}"' if css else ""
    items = "".join(toc_item(e, "toc-dup" if e.duplicate else "") for e in entries)
    return f"<ul{attr}>{items}</ul>"


def build_toc(front, parts):
    out = ['<nav class="toc"><div class="chapter-mark" data-title="Contents" data-part="Doriax Engine"></div>',
           '<h1 class="bl1">Contents</h1>', '<div class="toc-body">']
    out.append(f'<div class="toc-part"><a href="#{chapter_id(front.src)}">{htmllib.escape(front.title)}</a></div>')
    for number, part in enumerate(parts, 1):
        out.append(f'<div class="toc-part">Part {number} · {htmllib.escape(part.title)}</div>')
        out.append(toc_list(part.entries))
        for group in part.groups:
            out.append(f'<div class="toc-group">{htmllib.escape(group.title)}</div>{toc_list(group.entries)}')
            for sub in group.subgroups:
                out.append(f'<div class="toc-subgroup">{htmllib.escape(sub.title)}</div>{toc_list(sub.entries, "sub")}')
    out.append("</div></nav>")
    return "".join(out)


def part_page(number, part):
    """Divider listing what the part holds: chapters, or groups for Reference."""
    entries = list(part.entries)
    for group in part.groups:
        first = next((e for e in all_entries(group) if not e.duplicate), None)
        if first is not None:
            entries.append(Entry(first.src, group.title))
    items = "".join(toc_item(e) for e in entries if not e.duplicate)
    title = htmllib.escape(part.title)
    return (
        f'<section class="part-page"><div class="chapter-mark" data-title="{title}" data-part="{title}"></div>'
        f'<p class="part-number">Part {number}</p><h1 class="bl1">{title}</h1><ul>{items}</ul></section>\n'
    )


def all_entries(group):
    yield from group.entries
    for sub in group.subgroups:
        yield from all_entries(sub)


def build_body(merger, front, parts, present):
    chunks = []
    if front.src in present:
        chunks.append(merger.chapter_html(front, "Doriax Engine", 1, present))
    for number, part in enumerate(parts, 1):
        chunks.append(part_page(number, part))
        for entry in part.entries:
            if not entry.duplicate:
                chunks.append(merger.chapter_html(entry, part.title, 2, present))
        for group in part.groups:
            group_label = f"{part.title} · {group.title}"
            pending = [f'<div class="group-band bl2">{htmllib.escape(group.title)}</div>']
            for entry in group.entries:
                if not entry.duplicate:
                    chunks.append(merger.chapter_html(entry, group_label, 3, present, pending))
                    pending = []
            for sub in group.subgroups:
                sub_label = f"{group_label} · {sub.title}"
                pending.append(f'<div class="group-band sub bl3">{htmllib.escape(sub.title)}</div>')
                for entry in sub.entries:
                    if not entry.duplicate:
                        chunks.append(merger.chapter_html(entry, sub_label, 4, present, pending))
                        pending = []
    return "".join(chunks)


def prune(parts, present):
    """Drops pages left out by --only."""
    def keep(entries):
        return [e for e in entries if e.src in present]

    for part in parts:
        part.entries = keep(part.entries)
        for group in part.groups:
            group.entries = keep(group.entries)
            for sub in group.subgroups:
                sub.entries = keep(sub.entries)
            group.subgroups = [s for s in group.subgroups if s.entries]
        part.groups = [g for g in part.groups if g.entries or g.subgroups]
    return [p for p in parts if p.entries or p.groups]


def check_pointers(parts, merger):
    """A contents line pointing into a page needs that anchor to exist."""
    for part in parts:
        for group in part.groups:
            for entry in all_entries(group):
                if entry.anchor and entry.anchor not in merger.ids[entry.src]:
                    report.add("API Index anchor not found (sent to the chapter start)", f"{entry.src}#{entry.anchor}")
                    entry.anchor = ""


def build_html(cfg, src, front, parts, body, version, ref, commit, date, css_toc, present):
    logo = (src / "docs" / "assets" / "logo" / "doriax_logo_dark.png").as_uri()
    title = f"Doriax Engine Documentation {version}"
    copyright_text = cfg.copyright or ""
    example_src = "manual/scripting.md"
    example = (
        f'<a class="xref" href="#{chapter_id(example_src)}">Scripting</a>'
        if example_src in present else "Scripting (p. 12)"
    )
    return f"""<!doctype html>
<html lang="en" data-book="{htmllib.escape(title)}">
<head>
<meta charset="utf-8">
<title>{htmllib.escape(title)}</title>
<meta name="author" content="{htmllib.escape(cfg.site_author or '')}">
<meta name="description" content="{htmllib.escape(cfg.site_description or '')}">
<meta name="keywords" content="Doriax, game engine, documentation, Lua, C++">
<meta name="dcterms.modified" content="{datetime.date.today().isoformat()}">
</head>
<body>
<section class="cover">
  <img src="{logo}" alt="Doriax Engine">
  <p class="cover-title">Documentation</p>
  <p class="cover-version">Version {version}</p>
  <p class="cover-date">{date}</p>
</section>
<section class="edition">
  <h2>This edition</h2>
  <p>Doriax Engine Documentation, version {version}. Generated from <code>{ref}</code>
  (commit <code>{commit}</code>, {date}) of
  <code>github.com/doriaxengine/doriax-docs</code>. The current documentation is online
  at <code>{htmllib.escape(cfg.site_url.rstrip("/").removeprefix("https://"))}</code>.</p>
  <h2>Reading on paper</h2>
  <ul>
    <li>Code shown in tabs on the website is printed in full, one language after the other,
    with a <strong>C++</strong> or <strong>Lua</strong> label on each block.</li>
    <li>References to other chapters carry the page they point to, as in
    “{example}”. In a PDF viewer they also work as links.</li>
    <li>Web addresses appear as footnotes.</li>
    <li>The Reference part holds every class page, grouped as in the API Index.</li>
  </ul>
  <h2>License</h2>
  <p>{copyright_text}</p>
</section>
{css_toc}
{body}
</body>
</html>"""


# ---------------------------------------------------------------- checks

def check_layout(document):
    """Reports anything printed outside the text area, and nearly empty pages."""
    overflow = []
    sparse = []
    for number, page in enumerate(document.pages, 1):
        root = page._page_box
        left = root.content_box_x() - 0.5
        right = root.content_box_x() + root.width + 0.5
        texts = 0
        stack = [c for c in root.children if not isinstance(c, boxes.MarginBox)]
        while stack:
            box = stack.pop()
            if isinstance(box, boxes.TextBox):
                texts += 1
            if isinstance(box, (boxes.TextBox, boxes.ReplacedBox)):
                end = box.position_x + box.margin_width()
                if end > right or box.position_x < left:
                    snippet = getattr(box, "text", getattr(box, "element_tag", ""))[:60]
                    overflow.append(f"p.{number}: {max(end - right, left - box.position_x):.0f}px past the edge: {snippet!r}")
            if hasattr(box, "children"):
                stack.extend(box.children)
        if texts <= 2:
            sparse.append(number)
    if overflow:
        for line in overflow:
            report.add("Content outside the text area", line)
    report.add("__pages", len(document.pages))
    if sparse:
        report.add("Pages with almost no text", ", ".join(map(str, sparse)))


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", required=True, help="tag or branch to build, such as v0.8.4 or main")
    parser.add_argument("--repo", type=Path, default=HERE.parent, help="documentation repository (default: this one)")
    parser.add_argument("--out", type=Path, help="default: doriax-docs-<ref>.pdf")
    parser.add_argument("--strict", action="store_true", help="exit with an error if the report shows a defect")
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--keep-html", type=Path, help="also write the merged HTML here, for debugging")
    args = parser.parse_args()

    version = {"main": "unstable"}.get(args.ref, args.ref.removeprefix("v"))
    out = args.out or Path(f"doriax-docs-{args.ref.replace('/', '-')}.pdf")
    with tempfile.TemporaryDirectory(prefix="doriax-print-") as tmp:
        work = Path(tmp)
        src = work / "src"
        src.mkdir()
        commit, date = export_ref(args.repo, args.ref, src)
        print(f"Rendering {args.ref} ({commit}, {date}) with MkDocs")
        cfg, capture = render_docs(src, work)
        print(f"Rendered {len(capture.pages)} pages")

        front, parts = build_book(capture)
        present = set(capture.pages)
        if args.only:
            present = {s for s in present if any(p in s for p in args.only)}
            parts = prune(parts, present)
            if front.src not in present:
                present.add(front.src)

        merger = Merger(capture, src / "docs")
        for page in present:
            merger.prepare(page)
        check_pointers(parts, merger)
        body = build_body(merger, front, parts, present)
        toc = build_toc(front, parts)
        html = build_html(cfg, src, front, parts, body, version, args.ref, commit, date, toc, present)
        if args.keep_html:
            args.keep_html.write_text(html, encoding="utf-8")

        tabs = collections.Counter(report.items.pop("__tabs", []))
        print(f"Merged {len(present)} pages, {len(html) / 1e6:.1f} MB of HTML; printed tabs: {dict(tabs.most_common(4))}")

        print("Laying out the book with WeasyPrint")
        fonts = FontConfiguration()
        document = HTML(string=html, base_url=str(src)).render(
            stylesheets=[CSS(filename=str(HERE / "print.css"), font_config=fonts)],
            font_config=fonts,
        )
        check_layout(document)
        out.parent.mkdir(parents=True, exist_ok=True)
        document.write_pdf(str(out))

    pages = report.items.pop("__pages")[0]
    print(f"\nWrote {out}: {pages} pages, {out.stat().st_size / 1e6:.1f} MB")
    report.show()
    defects = [kind for kind in DEFECTS if kind in report.items]
    if defects and "GITHUB_ACTIONS" in os.environ:
        print(f"::warning::PDF of {args.ref}: {', '.join(defects)}")
    if args.strict and defects:
        sys.exit(f"Failing because of: {', '.join(defects)}")


if __name__ == "__main__":
    main()
