---
description: Shape API reference (C++ and Lua).
---

# Shape

**Inherits:** [Mesh](mesh.md)  
**C++ type:** `Shape`

Procedural mesh factory (box, sphere, etc.). Each `create*` call replaces the mesh
geometry; call it once after constructing the `Shape`.

## Methods

| Name | Languages | Geometry |
| --- | --- | --- |
| `createPlane` | C++ \| Lua | Flat quad in the XZ plane, normal `+Y` (lies down, like a floor) |
| `createWall` | C++ \| Lua | Upright quad in the XY plane, normal `+Z` (stands up, faces the camera) |
| `createBox` | C++ \| Lua | Box centred on the origin |
| `createSphere` | C++ \| Lua | UV sphere |
| `createCylinder` | C++ \| Lua | Cylinder or cone (separate base/top radii) |
| `createCapsule` | C++ \| Lua | Capsule (cylinder with hemispherical caps) |
| `createTorus` | C++ \| Lua | Torus / ring |

```cpp
Shape floor(&scene);
floor.createPlane(20.0f, 20.0f);     // width, depth — horizontal

Shape wall(&scene);
wall.createWall(10.0f, 10.0f);       // width, height — vertical
```

A **Wall** is the natural surface for a [mirror](../../manual/rendering-pipeline.md#mirrors-and-planar-reflections):
its `+Z` normal matches the default `MirrorComponent` normal, so it reflects without any
rotation.
