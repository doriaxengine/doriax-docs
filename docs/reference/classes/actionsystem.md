---
description: ActionSystem API reference (C++ and Lua).
---

# ActionSystem

**Inherits:** [SubSystem](subsystem.md)

Updates actions, animations, and particles.

## Methods

| Name | Languages |
| --- | --- |
| `actionStart` | C++ \| Lua |
| `actionStop` | C++ \| Lua |
| `actionPause` | C++ \| Lua |
| `particleActionReset` | C++ \| Lua |
| `getDuration` | C++ \| Lua |
| `getFrameDuration` | C++ \| Lua |

`actionStart(entity, newRun)` resumes a paused action. With `newRun` true, the default, a
stopped action starts over from its `startOffset`, or from a random point with `randomStart`.

`getDuration(entity)` returns an action's length in seconds, and `getFrameDuration(frame)`
the length of one [ActionFrame](actionframe.md) of an animation. `particleActionReset(entity)`
stops a particle action and clears its particles.
