---
description: AlphaAction API reference (C++ and Lua).
---

# AlphaAction

**Inherits:** [TimedAction](timedaction.md)  
**C++ type:** `AlphaAction`

## Description

Animates the `alpha` (opacity) property of its target object from a start value to an end value over a fixed duration.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAction](#setaction) | C++ \| Lua |

## Method details

### setAction

* void **setAction**(float startAlpha, float endAlpha, float duration, bool loop = false)

Configures the tween. `startAlpha` and `endAlpha` are opacity values in `[0, 1]`. `duration` is in **seconds**.

=== "C++"
    ```cpp
    AlphaAction fadeOut(&scene);
    fadeOut.setTarget(&sprite);
    fadeOut.setAction(1.0f, 0.0f, 0.5f);  // fade out in 0.5 s
    fadeOut.start();
    ```

=== "Lua"
    ```lua
    local fadeOut = AlphaAction(scene)
    fadeOut:setTarget(sprite)
    fadeOut:setAction(1.0, 0.0, 0.5)
    fadeOut:start()
    ```

Set `loop = true` to create a continuous pulsing effect.
