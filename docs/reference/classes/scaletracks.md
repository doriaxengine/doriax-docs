---
description: ScaleTracks API reference (C++ and Lua).
---

# ScaleTracks

**Inherits:** [Action](action.md)  
**C++ type:** `ScaleTracks`

`ScaleTracks` API exposed to Lua and C++ gameplay code.

## Constructors

Available in C++ and Lua:

* `ScaleTracks(Scene* scene)` — creates a new entity.
* `ScaleTracks(Scene* scene, Entity entity)` — wraps an existing entity without taking ownership.
* `ScaleTracks(Scene* scene, std::vector<float> times, std::vector<Vector3> values)` — creates a track initialized with key times and values.

In Lua, use `ScaleTracks(scene, entity)` to access an existing action. The entity must
already have the components required by this type; wrapping does not add them.
See [EntityHandle ownership](entityhandle.md#ownership-and-lifetime).

## Methods

| Name | Languages |
| --- | --- |
| `setTimes` | C++ \| Lua |
| `setValues` | C++ \| Lua |
| `setEasings` | C++ \| Lua |
| `setEasing` | C++ \| Lua |

`setEasing(segment, ease)` sets the easing of a single segment (key `segment` to key
`segment + 1`); `setEasings(list)` replaces the whole per-segment list. Missing entries
mean linear, `STEP` holds each key's value until the next key, `CUSTOM` is not storable
per segment (treated as linear), and `setTimes` trims the list when the key count
shrinks. Tracks imported from GLTF `CUBICSPLINE` clips carry per-key Hermite tangents
and interpolate from them instead; `setValues` keeps existing tangent arrays sized to
the new values. See
[Per-segment easing](../../manual/animation.md#per-segment-easing) and
[Interpolation modes](../../manual/animation.md#interpolation-modes).
