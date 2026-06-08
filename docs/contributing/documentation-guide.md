---
description: How to contribute to the Doriax documentation site.
---

# Documentation Guide

The documentation site is built with MkDocs and a custom Doriax theme. Source pages
live under `docs/`; generated site output lives under `site/`.

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve
mkdocs build --strict
```

## Reference documentation

API reference pages live under `docs/reference/classes/`. Each file documents **one
class** with C++ and Lua on the same page ([Supernova-style](https://github.com/supernovaengine/supernova-docs)).

**Do not** use a bulk markdown generator in this repo. Pages are edited by hand.

### Inventory tool

To list every bound class, method, and property, run the engine script (reference only):

```bash
python3 /path/to/doriax/generate_api_suggestions.py \
  engine/core/script/binding /tmp/out.h engine/core
```

Use that output when adding or verifying APIs. Then edit the matching
`docs/reference/classes/<name>.md` file and add descriptions for important methods.

### Priority for descriptions

Expand these first when touching the reference: `Engine`, `Scene`, `Object`, `Input`,
`Camera`, `Body2D`, `Body3D`, `PhysicsSystem`, `Mesh`, `Sprite`, `Action`, `Animation`.

### Page structure

1. Short class description
2. Properties / Methods / Events tables with a **Languages** column (`C++ | Lua`)
3. **Method details** for important APIs (tabbed C++ / Lua examples)
4. Enumerations when relevant

## File organization

| Folder | Purpose |
| --- | --- |
| `getting-started/` | Orientation and first-run |
| `tutorials/` | Step-by-step workflows |
| `editor/` | Editor panels and export |
| `manual/` | Concepts (ECS, scripting, events) |
| `reference/classes/` | Per-class API (hand-maintained) |
| `building/` | Platform build setup |

## Links

Use relative links. Run `mkdocs build --strict` after nav or path changes.
