---
description: KeyframeTracks API reference (C++ and Lua).
---

# KeyframeTracks

**Inherits:** [Action](action.md)  
**C++ type:** `KeyframeTracks`

## Description

Base class of the keyframe track actions: [TranslateTracks](translatetracks.md),
[RotateTracks](rotatetracks.md), [ScaleTracks](scaletracks.md) and
[MorphTracks](morphtracks.md). It holds what they share: the key times, the per-segment
easing, looping and relative values. Each subclass adds `setValues` with one value per key.

You typically do not instantiate `KeyframeTracks` directly.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| bool | [loop](#loop) | `false` | C++ \| Lua |
| bool | [relative](#relative) | `false` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setTimes](#settimes) | C++ \| Lua |
| void | [setEasings](#seteasings-seteasing) | C++ \| Lua |
| void | [setEasing](#seteasings-seteasing) | C++ \| Lua |

## Property details

### loop

* *Setter*: void **setLoop**(bool loop)
* *Getter*: bool **isLoop**() const

When `true`, the track starts over after its last key instead of stopping, so a track
loops on its own without an [Animation](animation.md).

---

### relative

* *Setter*: void **setRelative**(bool relative)
* *Getter*: bool **isRelative**() const

When `true`, the values are offsets from the pose the target has when the track starts:
a translation adds to its position, a rotation is applied after its rotation and a scale
multiplies its scale. The track then works wherever the target is placed. A UI element
with anchors moves by its layout offset. Morph tracks ignore it. See
[Relative tracks](../../manual/animation.md#relative-tracks).

---

## Method details

### setTimes

* void **setTimes**(std::vector<float> times)

Sets the key times in seconds, in ascending order. Trims the easing list when the key
count shrinks.

---

### setEasings / setEasing

* void **setEasings**(std::vector<EaseType> easings)
* void **setEasing**(unsigned int segment, EaseType ease)

`setEasing(segment, ease)` sets the easing of a single segment (key `segment` to key
`segment + 1`); `setEasings(list)` replaces the whole per-segment list. Missing entries
mean linear, `STEP` holds each key's value until the next key, and `CUSTOM` is not
storable per segment (treated as linear). See
[Per-segment easing](../../manual/animation.md#per-segment-easing).
