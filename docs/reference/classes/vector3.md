---
description: Vector3 API reference (C++ and Lua).
---

# Vector3

**C++ type:** `Vector3`

## Description

A 3D vector with `float` components `x`, `y`, and `z`. The primary type for 3D positions, directions, normals, colours (RGB), and velocity in Doriax.

Arithmetic operators `+`, `-`, and `*` support both vector and scalar operands. Division (`/`) is **scalar-only** (`Vector3 / float`). Comparison operators (`==`, `<`) are also available.

!!! note "Lua components are writable"
    Lua can read and assign `x`, `y`, and `z` directly. Engine properties such as
    `obj.position` return vector values, so assign a mutated value back to persist it:
    `local p = obj.position; p.x = p.x + 1; obj.position = p`. Whole-value arithmetic
    such as `obj.position = obj.position + Vector3(1, 0, 0)` also works.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | x | `0.0` | C++ \| Lua |
| float | y | `0.0` | C++ \| Lua |
| float | z | `0.0` | C++ \| Lua |

### Static constants

| Name | Value |
| --- | --- |
| `ZERO` | `(0, 0, 0)` |
| `UNIT_X` | `(1, 0, 0)` |
| `UNIT_Y` | `(0, 1, 0)` |
| `UNIT_Z` | `(0, 0, 1)` |
| `UNIT_SCALE` | `(1, 1, 1)` |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| float | [length](#length-squaredlength) | C++ \| Lua |
| float | [squaredLength](#length-squaredlength) | C++ \| Lua |
| float | [distance](#distance-squareddistance) | C++ \| Lua |
| float | [squaredDistance](#distance-squareddistance) | C++ \| Lua |
| float | [dotProduct](#dotproduct) | C++ \| Lua |
| float | [absDotProduct](#absdotproduct) | C++ \| Lua |
| Vector3 | [crossProduct](#crossproduct) | C++ \| Lua |
| Vector3& | [normalize](#normalize-normalized) | C++ \| Lua |
| Vector3 | [normalized](#normalize-normalized) | C++ \| Lua |
| float | [normalizeL](#normalizel) | C++ \| Lua |
| Vector3 | [midPoint](#midpoint) | C++ \| Lua |
| Vector3 | [moveTowards](#movetowards) | C++ |
| Vector3 | [lerp](#lerp) | C++ |
| Vector3 | [perpendicular](#perpendicular) | C++ \| Lua |
| Vector3 | [reflect](#reflect) | C++ \| Lua |
| void | [makeFloor](#makefloor-makeceil) | C++ \| Lua |
| void | [makeCeil](#makefloor-makeceil) | C++ \| Lua |
| bool | [isValid](#isvalid) | C++ \| Lua |
| std::string | [toString](#tostring) | C++ \| Lua |

## Method details

### length / squaredLength

* float **length**() const
* float **squaredLength**() const

`length()` returns the Euclidean magnitude `√(x² + y² + z²)`. `squaredLength()` omits the square root for cheaper magnitude comparisons.

---

### distance / squaredDistance

* float **distance**(const Vector3& rhs) const
* float **squaredDistance**(const Vector3& rhs) const

Distance between this point and `rhs`. Use `squaredDistance()` when only relative comparisons are needed.

---

### dotProduct

* float **dotProduct**(const Vector3& v) const

Scalar dot product `(x*v.x + y*v.y + z*v.z)`. Returns the cosine of the angle between two unit vectors.

---

### absDotProduct

* float **absDotProduct**(const Vector3& v) const

Returns the absolute value of the dot product. Useful for axis-aligned overlap tests.

---

### crossProduct

* Vector3 **crossProduct**(const Vector3& v) const

Returns the cross product, a vector perpendicular to both `*this` and `v`. The result follows the right-hand rule.

=== "C++"
    ```cpp
    Vector3 right = forward.crossProduct(Vector3::UNIT_Y);
    ```

=== "Lua"
    ```lua
    local right = forward:crossProduct(Vector3.UNIT_Y)
    ```

---

### normalize / normalized

* Vector3& **normalize**()
* Vector3 **normalized**() const

`normalize()` scales the vector in-place to unit length. `normalized()` returns a new unit-length copy.

---

### normalizeL

* float **normalizeL**()

Normalises in-place and returns the original magnitude in a single operation.

---

### midPoint

* Vector3 **midPoint**(const Vector3& v) const

Returns the midpoint between this vector and `v`.

---

### moveTowards

* Vector3 **moveTowards**(const Vector3& target, float maxDistanceDelta) const

Returns a point moved from `*this` toward `target` by at most `maxDistanceDelta`, **never overshooting** — once the remaining distance is within `maxDistanceDelta`, `target` is returned exactly. Pass `speed * deltatime` as `maxDistanceDelta` for frame-rate independent movement. This is the preferred way to move toward a target, since the naïve `direction * speed * deltatime` overshoots when the step is larger than the remaining distance (for example on the first, large [deltatime](engine.md#deltatime) frame). Equivalent to Unity's `Vector3.MoveTowards` and Godot's `Vector3.move_toward`.

`moveTowards` is currently **C++ only** (not bound to Lua).

=== "C++"
    ```cpp
    void MyScript::onUpdate() {
        Object obj(getScene(), getEntity());
        float step = speed * Engine::getDeltatime();
        obj.setPosition(obj.getPosition().moveTowards(targetPosition, step));
    }
    ```

=== "Lua"
    ```lua
    function MyScript:onUpdate()
        local obj = Object(self.scene, self.entity)
        local cur = obj.position
        local to = self.targetPosition
        local step = self.speed * Engine.deltatime
        local diff = to - cur
        local dist = diff:length()
        if dist <= step or dist == 0 then
            obj.position = to
        else
            obj.position = cur + diff * (step / dist)
        end
    end
    ```

---

### lerp

* Vector3 **lerp**(const Vector3& target, float t) const

Linear interpolation from `*this` toward `target` by factor `t`. `t = 0` returns `*this`, `t = 1` returns `target`. Unlike [moveTowards](#movetowards), the step is proportional to the remaining distance (eases as it approaches). Values outside `[0, 1]` extrapolate.

---

### perpendicular

* Vector3 **perpendicular**() const

Returns an arbitrary vector perpendicular to this one. Useful when you need a tangent without a reference direction.

---

### reflect

* Vector3 **reflect**(const Vector3& normal) const

Reflects this vector about `normal` (a unit vector). Equivalent to `v - 2 * dot(v, n) * n`.

---

### makeFloor / makeCeil

* void **makeFloor**(const Vector3& v)
* void **makeCeil**(const Vector3& v)

Component-wise minimum (`makeFloor`) or maximum (`makeCeil`), applied in-place. Useful for AABB calculations.

---

### isValid

* bool **isValid**() const

Returns `false` if any component is NaN or infinite.

---

### toString

* std::string **toString**() const

Returns a human-readable string like `"Vector3(1.000000, 2.000000, 3.000000)"`.
