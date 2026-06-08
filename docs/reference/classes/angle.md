---
description: Angle API reference (C++ and Lua).
---

# Angle

**C++ type:** `Angle` (static utility class)

## Description

A static utility class providing angle conversion functions between degrees, radians, and Doriax's *default* unit, which is controlled by `Engine::useDegrees`.

Because the "default" unit changes depending on the engine configuration, these helpers make it easy to write code that works correctly regardless of how the engine is configured.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static float | [radToDefault](#radtodefault-degtodefault) | C++ \| Lua |
| static float | [degToDefault](#radtodefault-degtodefault) | C++ \| Lua |
| static float | [defaultToRad](#defaulttorad-defaulttodeg) | C++ \| Lua |
| static float | [defaultToDeg](#defaulttorad-defaulttodeg) | C++ \| Lua |
| static float | [radToDeg](#radtodeg-degtorad) | C++ \| Lua |
| static float | [degToRad](#radtodeg-degtorad) | C++ \| Lua |

## Method details

### radToDefault / degToDefault

* static float **radToDefault**(float radians)
* static float **degToDefault**(float degrees)

Convert a value in radians or degrees to the engine's current default angle unit. If `Engine::useDegrees` is `true`, `radToDefault()` converts radians → degrees and `degToDefault()` is a no-op.

=== "C++"
    ```cpp
    // Rotate 45° regardless of engine angle setting
    float angle = Angle::degToDefault(45.0f);
    obj.setRotation(Quaternion(0, angle, 0));
    ```

=== "Lua"
    ```lua
    local angle = Angle.degToDefault(45)
    obj:setRotation(Quaternion(0, angle, 0))
    ```

---

### defaultToRad / defaultToDeg

* static float **defaultToRad**(float angle)
* static float **defaultToDeg**(float angle)

Convert from the engine's default unit to radians or degrees.

=== "C++"
    ```cpp
    float deg = Angle::defaultToDeg(obj.getRotation().getYaw());
    ```

=== "Lua"
    ```lua
    local deg = Angle.defaultToDeg(obj:getRotation():getYaw())
    ```

---

### radToDeg / degToRad

* static float **radToDeg**(float radians)
* static float **degToRad**(float degrees)

Direct conversion between radians and degrees, independent of the engine's `useDegrees` setting.

=== "C++"
    ```cpp
    float rad = Angle::degToRad(180.0f);  // π
    ```

=== "Lua"
    ```lua
    local rad = Angle.degToRad(180)  -- π
    ```
