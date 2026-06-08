---
description: Plane API reference (C++ and Lua).
---

# Plane

**C++ type:** `Plane`

## Description

An infinite plane in 3D space represented in the form `n·x + d = 0`, where `n` is the unit normal vector and `d` is the signed distance from the origin.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| Vector3 | normal | `(0,0,0)` | C++ \| Lua |
| float | d | `0.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| Side | [getSide](#getside) | C++ \| Lua |
| float | [getDistance](#getdistance) | C++ \| Lua |
| void | [redefine](#redefine) | C++ \| Lua |
| Vector3 | [projectVector](#projectvector) | C++ \| Lua |
| Plane& | [normalize](#normalize-normalized) | C++ \| Lua |
| Plane | [normalized](#normalize-normalized) | C++ \| Lua |

## Enumerations

### Side

Classifies the relative position of a point or volume:

* **NO_SIDE** — The object is on or spans both sides.
* **POSITIVE_SIDE** — The object is in front of the plane (same direction as `normal`).
* **NEGATIVE_SIDE** — The object is behind the plane.
* **BOTH_SIDE** — The object spans both sides.

---

## Method details

### getSide

* [Side](#side) **getSide**(const Vector3& rkPoint) const
* [Side](#side) **getSide**(const Vector3& centre, const Vector3& halfSize) const
* [Side](#side) **getSide**(const AABB& rkBox) const
* [Side](#side) **getSide**(const OBB& obb) const

Determines which side of the plane a point or volume is on. Useful for frustum culling and portal rendering.

---

### getDistance

* float **getDistance**(const Vector3& rkPoint) const

Returns the signed distance from `rkPoint` to the plane. Positive values are on the `normal` side.

---

### redefine

* void **redefine**(const Vector3& rkPoint0, const Vector3& rkPoint1, const Vector3& rkPoint2)
* void **redefine**(const Vector3& rkNormal, const Vector3& rkPoint)

Recomputes the plane from three non-collinear points or from a normal and a point.

---

### projectVector

* Vector3 **projectVector**(const Vector3& v) const

Projects `v` onto the plane, returning the component of `v` tangent to the plane.

---

### normalize / normalized

* Plane& **normalize**()
* Plane **normalized**() const

Normalises the plane equation so that `normal` has unit length.
