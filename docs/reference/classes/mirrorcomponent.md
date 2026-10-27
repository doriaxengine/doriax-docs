---
description: MirrorComponent API reference (C++ and Lua).
---

# MirrorComponent

The data behind a [Mirror](mirror.md). In Lua, get it with `mirror:getMirrorComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `normal` | C++ \| Lua |

`normal` is the local normal of the reflecting surface. The default, +Z, matches a wall mesh.
