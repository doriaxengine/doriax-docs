---
description: OBB API reference (C++ and Lua).
---

# OBB

**C++ type:** `OBB`

## Description

An **Oriented Bounding Box** — a box whose axes can be rotated arbitrarily in world space. OBBs provide tighter fit than [AABB](aabb.md)s for non-axis-aligned objects at the cost of more complex intersection tests.

### Properties

| Type | Name | Langs |
| --- | --- | --- |
| Vector3 | [center](#center-halfextents) | C++ \| Lua |
| Vector3 | [halfExtents](#center-halfextents) | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAxes](#setaxes) | C++ \| Lua |
| void | [setOrientation](#setorientation-getorientation) | C++ \| Lua |
| Quaternion | [getOrientation](#setorientation-getorientation) | C++ \| Lua |
| void | [transform](#transform) | C++ \| Lua |
| AABB | [toAABB](#toaabb) | C++ \| Lua |
| bool | [intersects](#intersects) | C++ \| Lua |
| bool | [contains](#contains) | C++ \| Lua |
| float | [distance](#distance-squareddistance) | C++ \| Lua |
| float | [squaredDistance](#distance-squareddistance) | C++ \| Lua |
| Vector3 | [closestPoint](#closestpoint) | C++ \| Lua |
| float | [volume](#volume) | C++ \| Lua |
| void | [enclose](#enclose) | C++ \| Lua |
| std::string | [toString](#tostring) | C++ \| Lua |

## Property details

### center / halfExtents

* *Setter/Getter*: **setCenter** / **getCenter**, **setHalfExtents** / **getHalfExtents**

The box centre and the half-extents along each local axis.

---

## Method details

### setAxes

* void **setAxes**(const Vector3& axisX, const Vector3& axisY, const Vector3& axisZ)
* void **setAxes**(const Quaternion& orientation)

Sets the three orthonormal local axes of the OBB. Can also be specified as a quaternion.

---

### setOrientation / getOrientation

* void **setOrientation**(const Quaternion& orientation)
* Quaternion **getOrientation**() const

The rotation of the box as a quaternion.

---

### transform

* void **transform**(const Matrix4& matrix)
* void **transform**(const Vector3& translate, const Quaternion& rotate, const Vector3& scale)

Applies a transformation to the OBB.

---

### toAABB

* [AABB](aabb.md) **toAABB**() const

Returns the axis-aligned bounding box that fully encloses this OBB.

---

### intersects

* bool **intersects**(const OBB& other) const
* bool **intersects**(const AABB& aabb) const
* bool **intersects**(const Sphere& sphere) const
* bool **intersects**(const Plane& plane) const
* bool **intersects**(const Vector3& point) const

Intersection tests using the Separating Axis Theorem (SAT).

---

### contains

* bool **contains**(const Vector3& point) const
* bool **contains**(const OBB& other) const

Returns `true` if this OBB fully contains the given point or box.

---

### distance / squaredDistance

* float **distance**(const Vector3& point) const
* float **squaredDistance**(const Vector3& point) const

Distance from a point to the nearest surface of this OBB.

---

### closestPoint

* Vector3 **closestPoint**(const Vector3& point) const

Returns the point on or inside the OBB closest to `point`.

---

### volume

* float **volume**() const

Returns `8 * halfExtents.x * halfExtents.y * halfExtents.z`.

---

### enclose

* void **enclose**(const OBB& other)
* void **enclose**(const Vector3& point)

Expands the OBB to also contain another OBB or a point.

---

### toString

* std::string **toString**() const

Returns a human-readable description of the OBB.
