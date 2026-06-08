---
description: Action API reference (C++ and Lua).
---

# Action

**Inherits:** [EntityHandle](entityhandle.md)  
**C++ type:** `Action`

## Description

Base class for all time-driven actions in Doriax. Actions are managed by [ActionSystem](actionsystem.md), which advances them each frame. You typically do not instantiate `Action` directly; instead you use concrete subclasses:

* [TimedAction](timedaction.md) — a single tween with start/end values and duration
* [Animation](animation.md) — a sequenced timeline of `ActionFrame` entries
* [Particles](particles.md) — a particle emitter driven by the action clock

An action operates on a *target* object. When started, the action applies its effect to the target each frame until it completes, is paused, or is stopped.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | [speed](#speed) | `1.0` | C++ \| Lua |
| bool | [ownedTarget](#ownedtarget) | `false` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [start](#start-pause-stop) | C++ \| Lua |
| void | [pause](#start-pause-stop) | C++ \| Lua |
| void | [stop](#start-pause-stop) | C++ \| Lua |
| void | [setTarget](#settarget) | C++ \| Lua |
| Entity | [getTarget](#settarget) | C++ \| Lua |
| bool | [isRunning](#isrunning-ispaused-isstopped) | C++ \| Lua |
| bool | [isPaused](#isrunning-ispaused-isstopped) | C++ \| Lua |
| bool | [isStopped](#isrunning-ispaused-isstopped) | C++ \| Lua |
| float | [getTimeCount](#gettimecount) | C++ \| Lua |

## Property details

### speed

* *Setter*: void **setSpeed**(float speed)
* *Getter*: float **getSpeed**() const

Playback speed multiplier. `1.0` is normal speed, `2.0` plays twice as fast, `0.5` in slow motion. Negative values play the action in reverse (where supported by the subclass).

---

### ownedTarget

* *Setter*: void **setOwnedTarget**(bool ownedTarget)
* *Getter*: bool **getOwnedTarget**() const

When `true`, the action takes ownership of its target entity — the target is automatically destroyed when the action is destroyed. Useful for fire-and-forget effects where both the action and the visual entity should be cleaned up together.

---

## Method details

### start / pause / stop

* void **start**()
* void **pause**()
* void **stop**()

Control playback:

* `start()` — begins or resumes the action. If the action was stopped, it restarts from the beginning.
* `pause()` — freezes time at the current position; `start()` resumes from here.
* `stop()` — halts and resets the time counter to zero.

=== "C++"
    ```cpp
    AlphaAction fadeOut(&scene);
    fadeOut.setTarget(&mySprite);
    fadeOut.setAction(1.0f, 0.0f, 1.0f);
    fadeOut.start();
    ```

=== "Lua"
    ```lua
    local fadeOut = AlphaAction(scene)
    fadeOut:setTarget(mySprite)
    fadeOut:setAction(1.0, 0.0, 1.0)
    fadeOut:start()
    ```

---

### setTarget

* void **setTarget**(Object* target)
* void **setTarget**(Entity target)
* Entity **getTarget**() const

Assigns the [Object](object.md) or entity that this action modifies. Most actions require a target to be set before `start()` is called.

---

### isRunning / isPaused / isStopped

* bool **isRunning**() const
* bool **isPaused**() const
* bool **isStopped**() const

Query the current playback state. An action is *running* if it has been started and has not yet completed, been paused, or been stopped.

---

### getTimeCount

* float **getTimeCount**() const

Returns the action's internal time counter in seconds, from `0` at the start to the action's total duration at completion.
