---
description: Sphere API reference (C++ and Lua).
---

# Sphere

**C++ type:** `Sphere`

## Description

A bounding sphere defined by a `center` point and a `radius`. Used for fast intersection tests and as a coarse culling primitive.

!!! note "Lua properties are read-only"
    In Lua, `center` and `radius` can be read but not assigned. Construct a new sphere instead:
    `local s = Sphere(Vector3(0, 1, 0), 2.5)`.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| Vector3 | center | `(0,0,0)` | C++ \| Lua (read-only) |
| float | radius | `0.0` | C++ \| Lua (read-only) |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [contains](#contains) | C++ \| Lua |
| bool | [intersects](#intersects) | C++ \| Lua |
| void | [merge](#merge) | C++ \| Lua |
| float | [surfaceArea](#surfacearea-volume) | C++ \| Lua |
| float | [volume](#surfacearea-volume) | C++ \| Lua |
| std::string | [toString](#tostring) | C++ \| Lua |

## Method details

### contains

* bool **contains**(const Vector3& point) const

Returns `true` if `point` is inside (or on) the sphere.

---

### intersects

* bool **intersects**(const Sphere& other) const
* bool **intersects**(const AABB& aabb) const
* bool **intersects**(const OBB& obb) const
* bool **intersects**(const Plane& plane) const
* bool **intersects**(const Vector3& v) const

Overlap test against another sphere, AABB, OBB, plane, or a point.

---

### merge

* void **merge**(const Sphere& other)

Expands this sphere to also enclose `other`.

---

### surfaceArea / volume

* float **surfaceArea**() const — returns `4 * π * r²`
* float **volume**() const — returns `(4/3) * π * r³`

---

### toString

* std::string **toString**() const

Returns a human-readable string like `"Sphere(center=(0,0,0), radius=1)"`.
