---
description: Mirror API reference (C++ and Lua).
---

# Mirror

**Inherits:** [Shape](shape.md)  
**C++ type:** `Mirror`

## Description

A flat mesh that reflects the scene — a true planar reflection, used for mirrors, still
water, and polished floors. Constructing a `Mirror` attaches a `MirrorComponent` to the
entity; the engine creates and drives the reflection camera internally, so no camera or
texture wiring is required.

`Mirror` inherits [Shape](shape.md), so it builds its own surface. Use
[createWall](shape.md) — its `+Z` normal matches the default [normal](#normal), so an
upright mirror needs no rotation.

See [Rendering Pipeline — Mirrors and planar reflections](../../manual/rendering-pipeline.md#mirrors-and-planar-reflections)
for how the reflection is rendered and what it costs.

=== "C++"

    ```cpp
    Mirror mirror(&scene);
    mirror.createWall(10.0f, 10.0f);
    mirror.setReceiveLights(false);   // reflection shown unshaded
    ```

=== "Lua"

    ```lua
    local mirror = Mirror(scene)
    mirror:createWall(10.0, 10.0)
    mirror.receiveLights = false
    ```

To make an existing mesh reflective instead — a floor, a model surface — use
[Mesh::setAsMirror](mesh.md#setasmirror-removemirror-ismirror), which attaches the same
component without replacing the geometry.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [Vector3](vector3.md) | [normal](#normal) | `Vector3(0, 0, 1)` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setNormal](#normal) | C++ \| Lua |
| Vector3 | [getNormal](#normal) | C++ \| Lua |

---

## Property details

### normal

* *Setter*: void **setNormal**([Vector3](vector3.md) normal)
* *Setter*: void **setNormal**(const float x, const float y, const float z)
* *Getter*: [Vector3](vector3.md) **getNormal**() const

The reflecting surface direction in the mesh's local space. It is transformed by the
entity's world rotation to build the mirror plane, so rotating the entity orients the
reflection automatically.

The default `+Z` matches a [Wall](shape.md). Pass `Vector3(0, 1, 0)` for a horizontal
surface such as a `createPlane` floor.

!!! tip "If the reflection looks wrong"
    The reflection image is the same whichever way the normal points, but the
    behind-the-mirror clipping depends on its sign. If the reflection is clipped on the
    wrong side, flip the sign of the normal.
