---
description: AABB API reference (C++ and Lua).
---

# AABB

**C++ type:** `AABB`

## Description

An **Axis-Aligned Bounding Box** defined by a minimum and maximum [Vector3](vector3.md) corner. All edges are parallel to the world axes, making AABB overlap tests extremely fast. AABBs are used throughout Doriax for mesh bounds queries, frustum culling, and physics broad-phase.

For rotated bounding volumes use [OBB](obb.md).

### Properties

| Type | Name | Langs |
| --- | --- | --- |
| Vector3 | [minimum](#minimum-maximum) | C++ \| Lua |
| Vector3 | [maximum](#minimum-maximum) | C++ \| Lua |

### Static constants

| Name | Description |
| --- | --- |
| `ZERO` | A valid AABB with all extents at zero |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setExtents](#setextents) | C++ \| Lua |
| Vector3 | [getCenter](#getcenter-getsize-gethalfsize) | C++ \| Lua |
| Vector3 | [getSize](#getcenter-getsize-gethalfsize) | C++ \| Lua |
| Vector3 | [getHalfSize](#getcenter-getsize-gethalfsize) | C++ \| Lua |
| AABB& | [merge](#merge) | C++ \| Lua |
| AABB& | [transform](#transform) | C++ \| Lua |
| AABB | [intersection](#intersection) | C++ \| Lua |
| bool | [intersects](#intersects) | C++ \| Lua |
| bool | [contains](#contains) | C++ \| Lua |
| float | [distance](#distance-squareddistance) | C++ \| Lua |
| float | [squaredDistance](#distance-squareddistance) | C++ \| Lua |
| float | [volume](#volume) | C++ \| Lua |
| void | [scale](#scale) | C++ \| Lua |
| [OBB](obb.md) | [getOBB](#getobb) | C++ \| Lua |
| void | [setNull / setInfinite / setFinite](#null-infinite-finite) | C++ \| Lua |
| bool | [isNull / isInfinite / isFinite](#null-infinite-finite) | C++ \| Lua |

## Property details

### minimum / maximum

* *Setter*: void **setMinimum**(const Vector3& vec) / individual axis setters
* *Getter*: const Vector3& **getMinimum**() const
* *Setter*: void **setMaximum**(const Vector3& vec)
* *Getter*: const Vector3& **getMaximum**() const

The two corner points of the box in world space.

---

## Method details

### setExtents

* void **setExtents**(const Vector3& min, const Vector3& max)
* void **setExtents**(float mx, float my, float mz, float Mx, float My, float Mz)

Sets both minimum and maximum in one call.

---

### getCenter / getSize / getHalfSize

* Vector3 **getCenter**() const
* Vector3 **getSize**() const
* Vector3 **getHalfSize**() const

`getCenter()` returns the midpoint. `getSize()` returns `max - min`. `getHalfSize()` returns half the size — convenient for physics and intersection tests.

---

### merge

* AABB& **merge**(const AABB& rhs)
* AABB& **merge**(const Vector3& point)

Expands this AABB to also contain `rhs` or the given `point`.

---

### transform

* AABB& **transform**(const Matrix4& matrix)

Transforms the AABB by `matrix`. Note: an AABB after transformation is re-fitted, which may be larger than the OBB would be.

---

### intersection

* AABB **intersection**(const AABB& b2) const

Returns the AABB formed by the overlap of this box and `b2`. Returns a null AABB if there is no overlap.

---

### intersects

* bool **intersects**(const AABB& b2) const
* bool **intersects**(const [OBB](obb.md)& obb) const
* bool **intersects**(const [Plane](plane.md)& p) const
* bool **intersects**(const [Sphere](sphere.md)& sp) const
* bool **intersects**(const [Vector3](vector3.md)& v) const

Overlap tests against other volumes or a point.

=== "C++"
    ```cpp
    AABB playerBounds = player.getWorldAABB();
    AABB triggerZone(Vector3(-2,-1,-2), Vector3(2,1,2));
    if (playerBounds.intersects(triggerZone)) {
        // player entered trigger
    }
    ```

=== "Lua"
    ```lua
    local playerBounds = player:getWorldAABB()
    local triggerZone = AABB(Vector3(-2,-1,-2), Vector3(2,1,2))
    if playerBounds:intersects(triggerZone) then
        -- player entered trigger
    end
    ```

---

### contains

* bool **contains**(const Vector3& v) const
* bool **contains**(const AABB& other) const

Returns `true` if this AABB fully contains the given point or box.

---

### distance / squaredDistance

* float **distance**(const Vector3& v) const
* float **squaredDistance**(const Vector3& v) const

Distance from a point to the nearest surface of this box. Returns `0` if the point is inside.

---

### volume

* float **volume**() const

Returns the volume `(max.x-min.x) * (max.y-min.y) * (max.z-min.z)`.

---

### scale

* void **scale**(const Vector3& s)

Scales the AABB from its centre by the given factor.

---

### getOBB

* [OBB](obb.md) **getOBB**() const

Converts this AABB to an [OBB](obb.md) with axis-aligned orientation.

---

### null / infinite / finite

* void **setNull**() / bool **isNull**()
* void **setInfinite**() / bool **isInfinite**()
* void **setFinite**() / bool **isFinite**()

An AABB can be in one of three states: *null* (undefined, no extent), *finite* (normal bounding box), or *infinite* (the entire space). Intersection tests respect these states.
