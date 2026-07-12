---
description: RotateTracks API reference (C++ and Lua).
---

# RotateTracks

**Inherits:** [Action](action.md)  
**C++ type:** `RotateTracks`

`RotateTracks` API exposed to Lua and C++ gameplay code.

## Methods

| Name | Languages |
| --- | --- |
| `setTimes` | C++ \| Lua |
| `setValues` | C++ \| Lua |
| `setEasings` | C++ \| Lua |
| `setEasing` | C++ \| Lua |

`setEasing(segment, ease)` sets the easing of a single segment (key `segment` to key
`segment + 1`); `setEasings(list)` replaces the whole per-segment list. Missing entries
mean linear, `CUSTOM` is not storable per segment (treated as linear), and `setTimes`
trims the list when the key count shrinks. See
[Per-segment easing](../../manual/animation.md#per-segment-easing).
