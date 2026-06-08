---
description: ColorAction API reference (C++ and Lua).
---

# ColorAction

**Inherits:** [TimedAction](timedaction.md)  
**C++ type:** `ColorAction`

## Description

Animates the `color` property of its target object, interpolating from a start colour to an end colour over a fixed duration. Both RGB (`Vector3`) and RGBA (`Vector4`) variants are available.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAction](#setaction) | C++ \| Lua |

## Method details

### setAction

* void **setAction**(Vector3 startColor, Vector3 endColor, float duration, bool loop = false)
* void **setAction**(Vector4 startColor, Vector4 endColor, float duration, bool loop = false)

Configures the tween. The `Vector3` overload interpolates RGB; the `Vector4` overload includes alpha. `duration` is in **seconds**.

=== "C++"
    ```cpp
    ColorAction flash(&scene);
    flash.setTarget(&sprite);
    // Flash from white to original colour in 0.2 s, looping
    flash.setAction(Vector3(1, 1, 1), Vector3(1, 0.3f, 0.3f), 0.2f, true);
    flash.setFunctionType(EaseType::SINE_IN_OUT);
    flash.start();
    ```

=== "Lua"
    ```lua
    local flash = ColorAction(scene)
    flash:setTarget(sprite)
    flash:setAction(Vector3(1, 1, 1), Vector3(1, 0.3, 0.3), 0.2, true)
    flash:setFunctionType(EaseType.SINE_IN_OUT)
    flash:start()
    ```
