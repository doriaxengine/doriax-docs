---
description: Vector4 API reference (C++ and Lua).
---

# Vector4

**C++ type:** `Vector4`

## Description

A 4D vector with `float` components `x`, `y`, `z`, and `w`. Used for RGBA colours, homogeneous coordinates, and quaternion-adjacent math inside the engine. Provides full arithmetic operator support for both vector and scalar operations.

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

Performs perspective divide by `w` in-place: `x/=w; y/=w; z/=w; w=1`. Used to convert homogeneous clip-space coordinates to NDC.

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
