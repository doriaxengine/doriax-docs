---
description: PolygonComponent API reference (C++ and Lua).
---

# PolygonComponent

The data behind a UI [Polygon](polygon.md). In Lua, get it with `polygon:getPolygonComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `points` | C++ \| Lua |
| `needUpdatePolygon` | C++ \| Lua |

`points` is a list of [PolygonPoint](polygonpoint.md). Set `needUpdatePolygon` after assigning it. In Lua, lists are copies: assign the changed table back.
