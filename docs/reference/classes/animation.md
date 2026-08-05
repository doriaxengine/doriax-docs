---
description: Animation API reference (C++ and Lua).
---

# Animation

**Inherits:** [Action](action.md)  
**C++ type:** `Animation`

## Description

A timeline-based animation composed of `ActionFrame` entries. Each frame schedules an [Action](action.md) to run against a target entity at a specific time offset, for a specific duration. Frames can overlap to create parallel tweens, producing complex multi-property animations.

`Animation` objects are automatically created when loading a [Model](model.md) from a GLTF file. You can also build animations entirely in code for procedural sequences.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| bool | [loop](#loop) | `false` | C++ \| Lua |
| bool | [ownedActions](#ownedactions) | `false` | C++ \| Lua |
| std::string | [name](#name) | `""` | C++ \| Lua |
| float | [duration](#duration) | `0.0` | C++ |
| float | [blendWeight](#blendweight) | `1.0` | C++ \| Lua |
| float | [defaultFadeTime](#defaultfadetime) | `0.15` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [fadeIn](#fadein-fadeout) | C++ \| Lua |
| void | [fadeOut](#fadein-fadeout) | C++ \| Lua |
| void | [addActionFrame](#addactionframe) | C++ \| Lua |
| size_t | [getActionFrameSize](#getactionframesize) | C++ \| Lua |
| [ActionFrame](actionframe.md) | [getActionFrame](#getactionframe) | C++ \| Lua |
| void | [setActionFrameStartTime](#setactionframestarttime-setactionframeduration) | C++ \| Lua |
| void | [setActionFrameDuration](#setactionframestarttime-setactionframeduration) | C++ \| Lua |
| void | [setActionFrameEntity](#setactionframeentity) | C++ \| Lua |
| void | [clearActionFrames](#clearactionframes) | C++ |

## Property details

### loop

* *Setter*: void **setLoop**(bool loop)
* *Getter*: bool **isLoop**() const

When `true`, the animation restarts from the beginning after playing to completion.

---

### ownedActions

* *Setter*: void **setOwnedActions**(bool ownedActions)
* *Getter*: bool **isOwnedActions**() const

When `true`, all child [Action](action.md) entities referenced by the animation's frames are destroyed when the animation is destroyed. Useful for animations built entirely in code.

---

### name

*Inherited from:* [EntityHandle](entityhandle.md#name)

* *Setter*: void **setName**(const std::string& name)
* *Getter*: std::string **getName**() const

The animation entity's human-readable name (for example `"Walk"`, `"Attack"`, or
`"Idle"`). The editor displays this name in the Structure panel and animation selectors,
and [Model::findAnimation()](model.md#getanimation-findanimation) and the string overloads
of [Model::playAnimation()](model.md#playanimation-stopanimations) use it for lookup.

Imported GLTF clips initialize their animation entity name from the source clip name.
Renaming the entity also changes the string used to find or play that clip. There is no
separate name stored in `AnimationComponent`.

---

### duration

* *Setter*: void **setDuration**(const float& duration)
* *Getter*: const float& **getDuration**() const

Total length of the animation in **seconds**. When loading a model, this is set
automatically from the GLTF data. The getter and setter are not exposed to Lua;
Lua-created sequences derive their duration from their action frames.

---

### blendWeight

* *Setter*: void **setBlendWeight**(float weight)
* *Getter*: float **getBlendWeight**() const

The clip's current blend weight (`0.0`–`1.0`). When several clips animate the same skeleton, each bone's final pose is the weight-normalized average of the running clips, so weights let you layer or crossfade animations smoothly.

Setting `blendWeight` cancels any in-progress fade and holds the weight at the given value. For time-based transitions prefer [fadeIn / fadeOut](#fadein-fadeout), which animate this value for you. Reading it returns the live weight while a fade is running.

---

### defaultFadeTime

* *Setter*: void **setDefaultFadeTime**(float seconds)
* *Getter*: float **getDefaultFadeTime**() const

The crossfade duration (in **seconds**) used by [Model::playAnimation()](model.md#playanimation-stopanimations) when it is called without an explicit fade time. Authored per-clip and saved with the scene — set it in the **Properties** window (**AnimationComponent → Fade time**) or in code. Defaults to `0.15`.

---

## Method details

### fadeIn / fadeOut

* void **fadeIn**(float duration)
* void **fadeOut**(float duration)

Crossfade primitives that ramp the clip's [blendWeight](#blendweight) over `duration` seconds.

* `fadeIn(duration)` starts the clip (if not already running) and ramps its weight from `0` up to `1`. A `duration` of `0` starts it instantly at full weight.
* `fadeOut(duration)` ramps a running clip's weight down to `0` and stops it when it reaches zero. A `duration` of `0` stops it immediately.

To transition between two clips, fade one out while fading the other in. For clips on the same [Model](model.md), [Model::playAnimation()](model.md#playanimation-stopanimations) does this for you.

=== "C++"
    ```cpp
    // Manual crossfade from run to idle over 0.25s
    runAnim.fadeOut(0.25f);
    idleAnim.fadeIn(0.25f);
    ```

=== "Lua"
    ```lua
    -- Manual crossfade from run to idle over 0.25s
    runAnim:fadeOut(0.25)
    idleAnim:fadeIn(0.25)
    ```

---

### addActionFrame

Several overloads are available:

* void **addActionFrame**(float startTime, float duration, Entity action, Entity target)
* void **addActionFrame**(float startTime, Entity timedAction, Entity target)
* void **addActionFrame**(float startTime, float duration, Entity action)
* void **addActionFrame**(float startTime, Entity timedAction)

Adds a frame to the animation timeline. `startTime` is the offset in seconds from the animation start. `duration` overrides the action's own duration; a `duration` of `0` (or lower) means **auto** — the frame follows the action's own duration. The overloads without a `duration` parameter use auto. When `target` is omitted, the animation's own target is used.

An animation cannot contain itself, directly or through nested animations: a call that would create such a cycle is rejected with an error log.

=== "C++"
    ```cpp
    // Sequence: move right, then move up
    PositionAction moveRight(&scene);
    moveRight.setAction(Vector3(0,0,0), Vector3(5,0,0), 1.0f);

    PositionAction moveUp(&scene);
    moveUp.setAction(Vector3(5,0,0), Vector3(5,5,0), 1.0f);

    Animation seq(&scene);
    seq.setDuration(2.0f);
    seq.addActionFrame(0.0f, moveRight.getEntity(), mySprite.getEntity());
    seq.addActionFrame(1.0f, moveUp.getEntity(), mySprite.getEntity());
    seq.start();
    ```

=== "Lua"
    ```lua
    local moveRight = PositionAction(scene)
    moveRight:setAction(Vector3(0,0,0), Vector3(5,0,0), 1.0)

    local moveUp = PositionAction(scene)
    moveUp:setAction(Vector3(5,0,0), Vector3(5,5,0), 1.0)

    local seq = Animation(scene)
    seq:addActionFrame(0.0, moveRight.entity, mySprite.entity)
    seq:addActionFrame(1.0, moveUp.entity, mySprite.entity)
    seq:start()
    ```

---

### getActionFrameSize

* size_t **getActionFrameSize**() const

Returns the number of frames currently in the timeline.

---

### getActionFrame

* [ActionFrame](actionframe.md)& **getActionFrame**(unsigned int index)

Returns a reference to the [ActionFrame](actionframe.md) at the given zero-based index.

---

### setActionFrameStartTime / setActionFrameDuration

* void **setActionFrameStartTime**(unsigned int index, float startTime)
* void **setActionFrameDuration**(unsigned int index, float duration)

Modify the start time or duration of an existing frame by index. Setting `duration` to `0` (or lower) switches the frame to **auto**: it follows the action's own duration.

---

### setActionFrameEntity

* void **setActionFrameEntity**(unsigned int index, Entity action)

Replace the action entity for a given frame.

---

### clearActionFrames

* void **clearActionFrames**()

Removes all frames from the timeline. This method is not exposed to Lua.
