---
description: RotateTracks API reference (C++ and Lua).
---

# RotateTracks

**Inherits:** [KeyframeTracks](keyframetracks.md)  
**C++ type:** `RotateTracks`

`RotateTracks` API exposed to Lua and C++ gameplay code.

## Constructors

Available in C++ and Lua:

* `RotateTracks(Scene* scene)` — creates a new entity.
* `RotateTracks(Scene* scene, Entity entity)` — wraps an existing entity without taking ownership.
* `RotateTracks(Scene* scene, std::vector<float> times, std::vector<Quaternion> values)` — creates a track initialized with key times and values.

In Lua, use `RotateTracks(scene, entity)` to access an existing action. The entity must
already have the components required by this type; wrapping does not add them.
See [EntityHandle ownership](entityhandle.md#ownership-and-lifetime).

## Methods

| Name | Languages |
| --- | --- |
| `setValues` | C++ \| Lua |

The key times, easing, `loop` and `relative` come from [KeyframeTracks](keyframetracks.md).
Tracks imported from GLTF `CUBICSPLINE` clips carry per-key Hermite tangents and
interpolate from them instead; `setValues` keeps existing tangent arrays sized to the
new values. See [Interpolation modes](../../manual/animation.md#interpolation-modes).
