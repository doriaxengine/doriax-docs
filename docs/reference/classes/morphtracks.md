---
description: MorphTracks API reference (C++ and Lua).
---

# MorphTracks

**Inherits:** [Action](action.md)  
**C++ type:** `MorphTracks`

`MorphTracks` API exposed to Lua and C++ gameplay code.

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
