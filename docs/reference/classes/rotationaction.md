---
description: RotationAction API reference (C++ and Lua).
---

# RotationAction

**Inherits:** [TimedAction](timedaction.md)  
**C++ type:** `RotationAction`

## Description

Animates the `rotation` property of its target object using quaternion spherical linear interpolation (slerp) between a start and end rotation.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAction](#setaction) | C++ \| Lua |

## Method details

### setAction

* void **setAction**(Quaternion startRotation, Quaternion endRotation, float duration, bool loop = false)

Configures the tween. `startRotation` and `endRotation` are quaternion values. `duration` is in **seconds**.

=== "C++"
    ```cpp
    RotationAction spin(&scene);
    spin.setTarget(&wheel);
    spin.setAction(
        Quaternion::fromEuler(0, 0, 0),
        Quaternion::fromEuler(0, 360, 0),
        2.0f, true
    );
    spin.start();
    ```

=== "Lua"
    ```lua
    local spin = RotationAction(scene)
    spin:setTarget(wheel)
    spin:setAction(
        Quaternion.fromEuler(0, 0, 0),
        Quaternion.fromEuler(0, 360, 0),
        2.0, true
    )
    spin:start()
    ```
