#!/usr/bin/env python3
"""Writes docs/reference/shader-nodes.md from the editor's node catalogue.

    doriax-editor shader-nodes > nodes.json
    python3 scripts/shader-nodes.py nodes.json docs/reference/shader-nodes.md
"""
import json
import sys

CATEGORIES = ["Output", "Input", "Scene", "Parameter", "Math", "Vector", "Color", "UV", "Texture", "Noise", "Logic", "Effect", "Utility"]
TYPES = ["mesh", "ui", "points", "lines", "sky", "water", "postprocess"]

HEADER = """---
description: Every node of Doriax shader graphs, with its pins, settings, the shader types it fits and the stage it runs in.
---

# Shader Graph Nodes

The nodes a [shader graph](../editor/shader-graphs.md) is built from, generated from the
editor's catalogue (`doriax-editor shader-nodes`). The MCP tool `list_graph_node_types`
answers from the same catalogue.

Pin types:

| Type | Holds |
| --- | --- |
| `float`, `vec2`, `vec3`, `vec4` | Numbers. A float fills every component of a vector, a vector feeds a shorter one with its first components, and a `vec3` feeds a `vec4` with w 0. Other pairs, such as a vector into a float, go through Split or Combine |
| `color` | A `vec4`; a `vec3` feeding it gets alpha 1 |
| `int`, `bool` | An int takes a float, cut to an integer. A bool takes only a bool, which Compare makes |
| `texture2D`, `textureCube` | A texture parameter, named by a node's Texture setting rather than linked |
| `dynamic` | A float or vector that takes the smallest vector linked into the node's dynamic inputs, as Multiply does |

An input that nothing feeds takes its constant, set in the inspector, or its default. A
default such as `uv1` reads that field of the hook's context, as the matching Input node
would. Where a node runs: *any* runs in the stage that reads it; *vertex* and *fragment*
nodes only in that stage. A vertex value read by fragment nodes reaches them through a
varying the graph adds.
"""


def value(item):
    v = item.get("default")
    if v is None:
        return ""
    if isinstance(v, str):
        return v[1:] if v.startswith("@") else v
    if isinstance(v, list):
        return ", ".join(number(n) for n in v)
    return number(v)


def number(n):
    return str(int(n)) if float(n).is_integer() else str(n)


def fits(node):
    types = node.get("shaderTypes") or []
    if not types or set(types) == set(TYPES):
        return "every type"
    return ", ".join(types)


def node_section(node):
    lines = [f"### {node['name']}", ""]
    stage = "" if node["id"].startswith("output/") else f" · {node['stage']} stage"
    lines.append(f"`{node['id']}`{stage} · {fits(node)}")
    lines.append("")
    lines.append(node["description"])
    lines.append("")
    inputs = node.get("inputs", [])
    if inputs:
        output_node = node["id"].startswith("output/")
        if output_node:
            lines += ["| Input | Type | Fills |", "| --- | --- | --- |"]
            for pin in inputs:
                fills = pin.get("fills", {})
                target = f"`{fills['target']}`" if fills.get("target") else "its return value"
                lines.append(f"| {pin['label']} (`{pin['name']}`) | {pin['type']} | `{fills.get('hook', '')}`, {target} |")
        else:
            lines += ["| Input | Type | Default |", "| --- | --- | --- |"]
            for pin in inputs:
                lines.append(f"| {pin['label']} (`{pin['name']}`) | {pin['type']} | {value(pin)} |")
        lines.append("")
    outputs = node.get("outputs", [])
    if outputs:
        lines += ["| Output | Type |", "| --- | --- |"]
        for pin in outputs:
            kind = {"parameter": "the parameter's", "mask": "as long as the mask"}.get(pin["type"], pin["type"])
            lines.append(f"| {pin['label']} (`{pin['name']}`) | {kind} |")
        lines.append("")
    settings = node.get("settings", [])
    if settings:
        lines += ["| Setting | Takes | Default |", "| --- | --- | --- |"]
        for setting in settings:
            options = setting.get("options") or []
            if setting["type"] == "choice":
                takes = "one of " + ", ".join(f"`{o}`" for o in options)
            elif setting["type"] == "parameter":
                takes = "a " + " or ".join(f"`{o}`" for o in options) + " parameter" if options else "a parameter"
            elif setting["type"] == "number":
                takes = "a number"
            else:
                takes = "text"
            lines.append(f"| {setting['label']} (`{setting['name']}`) | {takes} | {value(setting)} |")
        lines.append("")
    return lines


def main():
    nodes = json.load(open(sys.argv[1]))
    out = [HEADER]
    for category in CATEGORIES + sorted({n["category"] for n in nodes} - set(CATEGORIES)):
        members = [n for n in nodes if n["category"] == category]
        if not members:
            continue
        out.append(f"## {category}")
        out.append("")
        for node in members:
            out += node_section(node)
    open(sys.argv[2], "w").write("\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    main()
