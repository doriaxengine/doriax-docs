---
description: ScaleAction API reference (C++ and Lua).
---

# ScaleAction

**Inherits:** [TimedAction](timedaction.md)  
**C++ type:** `ScaleAction`

## Description

Animates the `scale` property of its target object, interpolating between a start scale and an end scale over a fixed duration.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAction](#setaction) | C++ \| Lua |

## Method details

### setAction

* void **setAction**(Vector3 startScale, Vector3 endScale, float duration, bool loop = false)

Configures the tween. `startScale` and `endScale` are scale vectors. `duration` is in **seconds**.

=== "C++"
    ```cpp
    ScaleAction pop(&scene);
    pop.setTarget(&coin);
    pop.setAction(Vector3(0, 0, 0), Vector3(1, 1, 1), 0.3f);
    pop.setFunctionType(EaseType::BACK_OUT);
    pop.start();
    ```

=== "Lua"
    ```lua
    local pop = ScaleAction(scene)
    pop:setTarget(coin)
    pop:setAction(Vector3(0, 0, 0), Vector3(1, 1, 1), 0.3, false)
    pop:setFunctionType(EaseType.BACK_OUT)
    pop:start()
    ```
