---
description: Vector2 API reference (C++ and Lua).
---

# Vector2

**C++ type:** `Vector2`

## Description

A 2D vector with `float` components `x` and `y`. Used extensively for 2D positions, sizes, UV coordinates, and directions throughout the engine.

All arithmetic operators (`+`, `-`, `*`, `/`) are available for both component-wise vector operations and scalar multiplication/division. Comparison operators (`<`, `>`, `==`) are also supported.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | x | `0.0` | C++ \| Lua |
| float | y | `0.0` | C++ \| Lua |

### Static constants

| Name | Value |
| --- | --- |
| `ZERO` | `(0, 0)` |
| `UNIT_X` | `(1, 0)` |
| `UNIT_Y` | `(0, 1)` |
| `NEGATIVE_UNIT_X` | `(-1, 0)` |
| `NEGATIVE_UNIT_Y` | `(0, -1)` |
| `UNIT_SCALE` | `(1, 1)` |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| float | [length](#length-squaredlength) | C++ \| Lua |
| float | [squaredLength](#length-squaredlength) | C++ \| Lua |
| float | [distance](#distance-squareddistance) | C++ \| Lua |
| float | [squaredDistance](#distance-squareddistance) | C++ \| Lua |
| float | [dotProduct](#dotproduct) | C++ \| Lua |
| float | [crossProduct](#crossproduct) | C++ \| Lua |
| Vector2& | [normalize](#normalize-normalized) | C++ \| Lua |
| Vector2 | [normalized](#normalize-normalized) | C++ \| Lua |
| float | [normalizeL](#normalizel) | C++ \| Lua |
| Vector2 | [midPoint](#midpoint) | C++ \| Lua |
| Vector2 | [perpendicular](#perpendicular) | C++ \| Lua |
| Vector2 | [reflect](#reflect) | C++ \| Lua |
| void | [makeFloor](#makefloor-makeceil) | C++ \| Lua |
| void | [makeCeil](#makefloor-makeceil) | C++ \| Lua |
| bool | [isValid](#isvalid) | C++ \| Lua |
| std::string | [toString](#tostring) | C++ \| Lua |

## Method details

### length / squaredLength

* float **length**() const
* float **squaredLength**() const

`length()` returns the Euclidean magnitude `√(x² + y²)`. `squaredLength()` skips the square root for cheaper comparisons.

---

### distance / squaredDistance

* float **distance**(const Vector2& rhs) const
* float **squaredDistance**(const Vector2& rhs) const

Distance between this vector and `rhs`. `squaredDistance()` is cheaper and useful when you only need to compare distances.

---

### dotProduct

* float **dotProduct**(const Vector2& vec) const

Returns the dot product (`x*vec.x + y*vec.y`). Useful for projections and angle calculations.

---

### crossProduct

* float **crossProduct**(const Vector2& rkVector) const

Returns the 2D cross product (scalar), which equals the signed area of the parallelogram formed by the two vectors. Positive means `rkVector` is to the left of this vector.

---

### normalize / normalized

* Vector2& **normalize**()
* Vector2 **normalized**() const

`normalize()` scales the vector in-place to unit length and returns a reference to `*this`. `normalized()` returns a new normalised copy without modifying the original.

=== "C++"
    ```cpp
    Vector2 dir(3.0f, 4.0f);
    Vector2 unit = dir.normalized();  // (0.6, 0.8)
    ```

=== "Lua"
    ```lua
    local dir = Vector2(3.0, 4.0)
    local unit = dir:normalized()
    ```

---

### normalizeL

* float **normalizeL**()

Normalises in-place and returns the original length. Combines normalisation with a length query in a single pass.

---

### midPoint

* Vector2 **midPoint**(const Vector2& vec) const

Returns the midpoint between this vector and `vec`.

---

### perpendicular

* Vector2 **perpendicular**() const

Returns a vector perpendicular to this one (rotated 90° counter-clockwise).

---

### reflect

* Vector2 **reflect**(const Vector2& normal) const

Reflects this vector about `normal`. `normal` should be a unit vector.

---

### makeFloor / makeCeil

* void **makeFloor**(const Vector2& cmp)
* void **makeCeil**(const Vector2& cmp)

Component-wise minimum (`makeFloor`) or maximum (`makeCeil`) with `cmp`, applied in-place.

---

### isValid

* bool **isValid**() const

Returns `false` if any component is NaN or infinite.

---

### toString

* std::string **toString**() const

Returns a human-readable string representation like `"Vector2(1.000000, 2.000000)"`.
