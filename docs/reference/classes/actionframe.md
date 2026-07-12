---
description: ActionFrame API reference (C++ and Lua).
---

# ActionFrame

`ActionFrame` API exposed to Lua and C++ gameplay code.

## Properties

| Name | Languages |
| --- | --- |
| `startTime` | C++ \| Lua |
| `duration` | C++ \| Lua |
| `action` | C++ \| Lua |

`startTime` is the offset in seconds from the animation start at which `action` runs.

`duration` is how long the frame lasts, in seconds. A value of `0` (the default) means
**auto**: the frame follows the action's own duration — a `SpriteAnimation` lasts as
long as its frame sequence, a `TimedAction` uses its duration, a nested `Animation`
its own total length.
