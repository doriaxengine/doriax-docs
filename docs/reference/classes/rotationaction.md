---
description: RotationAction API reference (C++ and Lua).
---

# RotationAction

**Inherits:** [TimedAction](timedaction.md)  
**C++ type:** `RotationAction`

## Description

Animates the `rotation` property of its target object using quaternion spherical linear interpolation (slerp) between a start and end rotation. A slerp takes the short way between two rotations, so it never turns more than half a turn; [setSpinAction](#setspinaction) turns by any angle instead, for full spins.

### Constructors

Available in C++ and Lua:

* `RotationAction(Scene* scene)` — creates a new entity.
* `RotationAction(Scene* scene, Entity entity)` — wraps an existing entity without taking ownership.

In Lua, use `RotationAction(scene, entity)` to access an existing action. The entity must
already have the components required by this type; wrapping does not add them.
See [EntityHandle ownership](entityhandle.md#ownership-and-lifetime).

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAction](#setaction) | C++ \| Lua |
| void | [setSpinAction](#setspinaction) | C++ \| Lua |

## Method details

### setAction

* void **setAction**(Quaternion startRotation, Quaternion endRotation, float duration, bool loop = false)

Configures the tween. `startRotation` and `endRotation` are quaternion values. `duration` is in **seconds**.

=== "C++"
    ```cpp
    RotationAction spin(&scene);
    spin.setTarget(&wheel);
    spin.setAction(
        Quaternion(0.0f, 0.0f, 0.0f),
        Quaternion(0.0f, 360.0f, 0.0f),
        2.0f, true
    );
    spin.start();
    ```

=== "Lua"
    ```lua
    local spin = RotationAction(scene)
    spin:setTarget(wheel)
    spin:setAction(
        Quaternion(0, 0, 0),
        Quaternion(0, 360, 0),
        2.0, true
    )
    spin:start()
    ```

---

### setSpinAction

* void **setSpinAction**(Quaternion startRotation, Vector3 axis, float angle, float duration, bool loop = false)

Turns `startRotation` by `angle` around `axis` over `duration` seconds. The angle can be
any size, so `360` is a full turn and `720` two turns, and the axis is in the frame of
`startRotation`. The angle uses the engine's angle unit (degrees by default). In the
editor, check **Spin** in the RotationAction component and set its **Axis** and
**Angle**.

=== "C++"
    ```cpp
    RotationAction spin(&scene);
    spin.setTarget(&coin);
    spin.setSpinAction(Quaternion(), Vector3(0, 1, 0), 360.0f, 2.0f, true);
    spin.start();
    ```

=== "Lua"
    ```lua
    local spin = RotationAction(scene)
    spin:setTarget(coin)
    spin:setSpinAction(Quaternion(), Vector3(0, 1, 0), 360, 2.0, true)
    spin:start()
    ```
