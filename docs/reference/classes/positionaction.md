---
description: PositionAction API reference (C++ and Lua).
---

# PositionAction

**Inherits:** [TimedAction](timedaction.md)  
**C++ type:** `PositionAction`

## Description

Animates the `position` property of its target object, moving it from a start position to an end position over a fixed duration. Works in both 2D and 3D scenes.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAction](#setaction) | C++ \| Lua |

## Method details

### setAction

* void **setAction**(Vector3 startPosition, Vector3 endPosition, float duration, bool loop = false)

Configures the tween. `startPosition` and `endPosition` are world-space coordinates. `duration` is in **seconds**.

=== "C++"
    ```cpp
    PositionAction move(&scene);
    move.setTarget(&platform);
    move.setAction(Vector3(0, 0, 0), Vector3(5, 0, 0), 2.0f, true);
    move.setFunctionType(EaseType::SINE_IN_OUT);
    move.start();
    ```

=== "Lua"
    ```lua
    local move = PositionAction(scene)
    move:setTarget(platform)
    move:setAction(Vector3(0, 0, 0), Vector3(5, 0, 0), 2.0, true)
    move:setFunctionType(EaseType.SINE_IN_OUT)
    move:start()
    ```
