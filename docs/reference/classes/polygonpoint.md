---
description: PolygonPoint API reference (C++ and Lua).
---

# PolygonPoint

A vertex of a [Polygon](polygon.md) or a [MeshPolygon](meshpolygon.md). `PolygonPoint()` creates one in Lua.

## Properties

| Name | Languages |
| --- | --- |
| `position` | C++ \| Lua |
| `color` | C++ \| Lua |

`color` is a linear vertex color, multiplied by the color of the polygon. `addVertex` leaves it
white, so set per-vertex colors through the component's `points` list.
