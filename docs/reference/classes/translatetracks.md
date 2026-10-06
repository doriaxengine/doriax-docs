---
description: TranslateTracks API reference (C++ and Lua).
---

# TranslateTracks

**Inherits:** [KeyframeTracks](keyframetracks.md)  
**C++ type:** `TranslateTracks`

`TranslateTracks` API exposed to Lua and C++ gameplay code.

## Constructors

Available in C++ and Lua:

* `TranslateTracks(Scene* scene)` — creates a new entity.
* `TranslateTracks(Scene* scene, Entity entity)` — wraps an existing entity without taking ownership.
* `TranslateTracks(Scene* scene, std::vector<float> times, std::vector<Vector3> values)` — creates a track initialized with key times and values.

In Lua, use `TranslateTracks(scene, entity)` to access an existing action. The entity must
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
