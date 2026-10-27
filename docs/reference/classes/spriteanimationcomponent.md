---
description: SpriteAnimationComponent API reference (C++ and Lua).
---

# SpriteAnimationComponent

`SpriteAnimationComponent` holds the frame sequence and playback state for a
[SpriteAnimation](spriteanimation.md) action. Configure it through
[`SpriteAnimation::setAnimation`](spriteanimation.md#setanimation) or in the editor
**Properties** window (**Sprite Animation**). In Lua, get it with
`animation:getSpriteAnimationComponent()`.

## Properties

| Name | Languages |
| --- | --- |
| `loop` | C++ \| Lua |
| `frames` | C++ |
| `framesSize` | C++ \| Lua (read-only) |
| `framesTime` | C++ |
| `framesTimeSize` | C++ \| Lua (read-only) |
| `frameIndex` | C++ \| Lua (read-only) |
| `frameTimeIndex` | C++ \| Lua (read-only) |
| `spriteFrameCount` | C++ \| Lua (read-only) |

From Lua, change the frames with [`SpriteAnimation:setAnimation`](spriteanimation.md#setanimation).

`SpriteAnimationComponent` does not store a separate name. Sprite animations are
entities, so their display and lookup name comes from the inherited
[`SpriteAnimation` / entity name](spriteanimation.md#name) (`EntityHandle::name`).
Rename the entity in the Structure panel (or call `setName`) when you need a searchable
label — for example with [`Scene::findEntity`](entityregistry.md#findentity).

`frames` is a list of sprite atlas **frame indices**; `framesTime` is the matching list
of per-frame durations in **milliseconds**. `loop` restarts the sequence when it
finishes. Without it, playback stops on the last frame. `frameIndex`, `frameTimeIndex`,
and `spriteFrameCount` are runtime playback state (shown read-only in the editor).
