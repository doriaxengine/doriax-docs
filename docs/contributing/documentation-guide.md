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

## Versioned documentation

The published site carries one build per release series plus the in-development
docs from `main`:

| URL | Contents |
| --- | --- |
| `docs.doriax.org/` | Latest stable release (canonical URLs) |
| `docs.doriax.org/0.7/` | Newest tag of the 0.7 series |
| `docs.doriax.org/unstable/` | Current `main` branch |

`main` is always the unstable docs. Changes land there and reach the stable URLs
only when a release is tagged, so a page describing an unreleased feature does not
have to be held back.

`scripts/build-versions.sh` assembles the whole tree — it builds each series from
its highest patch tag (`v0.7.0`, `v0.7.1` → `0.7`, built from `v0.7.1`), ignores
pre-release tags, mirrors the newest series at the root, and writes
`versions.json`, which drives the version picker in the header. Old builds read
that file at runtime, so they pick up newer releases without being rebuilt.

`mkdocs serve` builds only the unstable version, and the picker stays hidden
because there is no `versions.json` to read. To preview the full versioned site:

```bash
scripts/build-versions.sh site
python3 -m http.server -d site
```

### Releasing a version

Tag the documentation repository when the matching engine release goes out:

```bash
git tag v0.7.1
git push origin v0.7.1
```

The tag push rebuilds and redeploys every version. Only a tagged commit's own
content is published for that version, so the tag must point at the commit whose
docs describe the release.
