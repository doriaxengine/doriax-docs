---
description: AnimationComponent API reference (C++ and Lua).
---

# AnimationComponent

`AnimationComponent` API exposed to Lua and C++ gameplay code.

## Properties

| Name | Languages |
| --- | --- |
| `actions` | C++ \| Lua |
| `ownedActions` | C++ \| Lua |
| `loop` | C++ \| Lua |
| `duration` | C++ \| Lua |
| `defaultFadeTime` | C++ \| Lua |

`AnimationComponent` does not store a separate name. Animations are entities, so their
display and lookup name comes from the inherited
[`Animation::name`](animation.md#name) entity property.

`defaultFadeTime` is the crossfade duration (seconds) used by
[Model::playAnimation()](model.md#playanimation-stopanimations) when no explicit fade
time is passed. Edit it in the **Properties** window as **Fade time**, or on an
[Animation](animation.md) object via `defaultFadeTime`.
