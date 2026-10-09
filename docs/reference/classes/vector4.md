---
description: Vector4 API reference (C++ and Lua).
---

# Vector4

**C++ type:** `Vector4`

## Description

A 4D vector with `float` components `x`, `y`, `z`, and `w`. Used for RGBA colours, homogeneous coordinates, and quaternion-adjacent math inside the engine.

`+` and `-` work on two vectors. `*` and `/` take a number or another vector, which multiplies or divides per component, and the number can also come first in a multiplication (`2 * v`).

!!! note "Lua components are writable"
    Lua can read and assign `x`, `y`, `z`, and `w` directly. When a vector comes from
    an engine property, mutate a local value and assign it back to persist the change.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | x | `0.0` | C++ \| Lua |
| float | y | `0.0` | C++ \| Lua |
| float | z | `0.0` | C++ \| Lua |
| float | w | `0.0` | C++ \| Lua |

### Static constants

| Name | Value |
| --- | --- |
| `ZERO` | `(0, 0, 0, 0)` |
| `UNIT_X` | `(1, 0, 0, 0)` |
| `UNIT_Y` | `(0, 1, 0, 0)` |
| `UNIT_Z` | `(0, 0, 1, 0)` |
| `UNIT_W` | `(0, 0, 0, 1)` |
| `UNIT_SCALE` | `(1, 1, 1, 1)` |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| float | [dotProduct](#dotproduct) | C++ \| Lua |
| void | [divideByW](#dividebyw) | C++ \| Lua |
| Vector4 | [moveTowards](#movetowards) | C++ \| Lua |
| Vector4 | [lerp](#lerp) | C++ \| Lua |
| bool | [isNaN](#isnan) | C++ \| Lua |
| bool | [isValid](#isvalid) | C++ \| Lua |
| std::string | [toString](#tostring) | C++ \| Lua |

## Method details

### dotProduct

* float **dotProduct**(const Vector4& vec) const

Returns the 4D dot product `(x*vec.x + y*vec.y + z*vec.z + w*vec.w)`.

---

### divideByW

* void **divideByW**()

Divides `x`, `y`, and `z` by `w` in place, the perspective divide that turns homogeneous clip-space coordinates into NDC. `w` keeps its value.

---

### moveTowards

* Vector4 **moveTowards**(const Vector4& target, float maxDistanceDelta) const

Returns `*this` moved toward `target` by at most `maxDistanceDelta`, never past it. See [Vector3 moveTowards](vector3.md#movetowards). On a colour it gives a fade at a steady rate:

=== "C++"
    ```cpp
    // Fully transparent after half a second
    Sprite sprite(getScene(), getEntity());
    Vector4 c = sprite.getColor();
    sprite.setColor(c.moveTowards(Vector4(c.x, c.y, c.z, 0.0f), 2.0f * Engine::getDeltatime()));
    ```

=== "Lua"
    ```lua
    -- Fully transparent after half a second
    local sprite = Sprite(self.scene, self.entity)
    local c = sprite.color
    sprite.color = c:moveTowards(Vector4(c.x, c.y, c.z, 0), 2 * Engine.deltatime)
    ```

---

### lerp

* Vector4 **lerp**(const Vector4& target, float t) const

Linear interpolation from `*this` toward `target` by factor `t`. `t = 0` returns `*this`, `t = 1` returns `target`, and values outside `[0, 1]` extrapolate. Blends two colours, for example `red:lerp(blue, 0.5)`.

---

### isNaN

* bool **isNaN**() const

Returns `true` if any component is NaN.

---

### isValid

* bool **isValid**() const

Returns `false` if any component is NaN or infinite.

---

### toString

* std::string **toString**() const

Returns a human-readable string like `"Vector4(1.0, 0.0, 0.0, 1.0)"`.
