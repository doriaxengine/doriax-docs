#!/usr/bin/env python3
"""Writes the class and member descriptions of the API reference as JSON.

The editor build takes them into its Lua stubs and the engine headers it copies
to projects, so hovers in an IDE show them:

    python3 scripts/api-docs.py ../doriax/editor/resources/docs/api-docs.json
"""
import json
import os
import re
import sys

SITE = "https://docs.doriax.org/reference/classes/"
CLASSES = os.path.join(os.path.dirname(__file__), "..", "docs", "reference", "classes")


def plain(text):
    """Markdown of one paragraph as plain text, keeping code spans."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def first_paragraph(lines):
    """The first paragraph of prose, past signatures, code, tabs, tables and notes."""
    paragraph = []
    fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if not stripped:
            if paragraph:
                break
            continue
        # signature bullets, tables, notes, tabs and rules
        if line.startswith((" ", "\t")) or stripped.startswith(("* ", "- ", "+ ", "|", "!!!", "???", "===", "---", "#", "<")):
            if paragraph:
                break
            continue
        paragraph.append(stripped)
    return plain(" ".join(paragraph))


def parse_page(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    lines = text.split("\n")

    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "")
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", title):
        return None, None

    sections = {}
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    entry = {"url": SITE + os.path.splitext(os.path.basename(path))[0] + "/", "members": {}}
    description = first_paragraph(sections.get("Description", []))
    if description:
        entry["description"] = description

    for section, body in sections.items():
        if not section.endswith("details"):
            continue
        heading = None
        start = 0
        for i, line in enumerate(body + ["### "]):
            if not line.startswith("### "):
                continue
            if heading:
                paragraph = first_paragraph(body[start:i])
                for name in heading.split("/"):
                    name = re.sub(r"[`()]", "", name).strip()
                    if paragraph and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
                        entry["members"].setdefault(name, paragraph)
            heading = line[4:].strip()
            start = i + 1

    return title, entry


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    docs = {}
    for name in sorted(os.listdir(CLASSES)):
        if name.endswith(".md"):
            title, entry = parse_page(os.path.join(CLASSES, name))
            if title and (entry.get("description") or entry["members"]):
                docs[title] = entry

    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    members = sum(len(entry["members"]) for entry in docs.values())
    print(f"{len(docs)} classes, {members} members")


if __name__ == "__main__":
    main()
