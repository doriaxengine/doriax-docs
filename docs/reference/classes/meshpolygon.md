---
description: MeshPolygon API reference (C++ and Lua).
---

# MeshPolygon

**Inherits:** [Mesh](mesh.md)  
**C++ type:** `MeshPolygon`

`MeshPolygon` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "`width` and `height` are derived"
    They come from the vertex list, so neither language has a setter. `addVertex` marks the polygon dirty and `MeshSystem` recomputes them on the next update, so they lag a frame behind the vertices.

| Name | Languages |
| --- | --- |
| `width` | C++ \| Lua (read-only) |
| `height` | C++ \| Lua (read-only) |
| `flipY` | C++ \| Lua |

## Methods

| Name | Languages |
| --- | --- |
| `addVertex` | C++ \| Lua |
