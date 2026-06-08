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
| float | [duration](#duration) | `0.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [addActionFrame](#addactionframe) | C++ \| Lua |
| size_t | [getActionFrameSize](#getactionframesize) | C++ \| Lua |
| [ActionFrame](actionframe.md) | [getActionFrame](#getactionframe) | C++ \| Lua |
| void | [setActionFrameStartTime](#setactionframestarttime-setactionframeduration) | C++ \| Lua |
| void | [setActionFrameDuration](#setactionframestarttime-setactionframeduration) | C++ \| Lua |
| void | [setActionFrameEntity](#setactionframeentity) | C++ \| Lua |
| void | [clearActionFrames](#clearactionframes) | C++ \| Lua |

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

* *Setter*: void **setName**(const std::string& name)
* *Getter*: const std::string& **getName**() const

Human-readable animation name (e.g. `"Walk"`, `"Attack"`, `"Idle"`). This is the name used by [Model::findAnimation()](model.md#getanimation-findanimation) to look up an animation by string.

---

### duration

* *Setter*: void **setDuration**(const float& duration)
* *Getter*: const float& **getDuration**() const

Total length of the animation in **seconds**. When loading a model, this is set automatically from the GLTF data.

---

## Method details

### addActionFrame

Several overloads are available:

* void **addActionFrame**(float startTime, float duration, Entity action, Entity target)
* void **addActionFrame**(float startTime, Entity timedAction, Entity target)
* void **addActionFrame**(float startTime, float duration, Entity action)
* void **addActionFrame**(float startTime, Entity timedAction)

Adds a frame to the animation timeline. `startTime` is the offset in seconds from the animation start. `duration` overrides the action's own duration. When `target` is omitted, the animation's own target is used.

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
    seq:setDuration(2.0)
    seq:addActionFrame(0.0, moveRight:getEntity(), mySprite:getEntity())
    seq:addActionFrame(1.0, moveUp:getEntity(), mySprite:getEntity())
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

Modify the start time or duration of an existing frame by index.

---

### setActionFrameEntity

* void **setActionFrameEntity**(unsigned int index, Entity action)

Replace the action entity for a given frame.

---

### clearActionFrames

* void **clearActionFrames**()

Removes all frames from the timeline.
