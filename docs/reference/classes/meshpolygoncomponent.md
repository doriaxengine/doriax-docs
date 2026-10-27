---
description: MeshPolygonComponent API reference (C++ and Lua).
---

# MeshPolygonComponent

The data behind a [MeshPolygon](meshpolygon.md). In Lua, get it with `polygon:getMeshPolygonComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `width` | C++ \| Lua (read-only) |
| `height` | C++ \| Lua (read-only) |
| `automaticFlipY` | C++ \| Lua |
| `flipY` | C++ \| Lua |
| `points` | C++ \| Lua |
| `needUpdatePolygon` | C++ \| Lua |

`points` is a list of [PolygonPoint](polygonpoint.md). Set `needUpdatePolygon` after assigning it. `width` and `height` are measured from the points. In Lua, lists are copies: assign the changed table back.
