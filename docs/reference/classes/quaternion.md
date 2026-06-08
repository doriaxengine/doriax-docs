---
description: Quaternion API reference (C++ and Lua).
---

# Quaternion

**C++ type:** `Quaternion`

## Description

Represents a rotation in 3D space using the quaternion formalism. Quaternions avoid gimbal lock, support smooth slerp interpolation, and are more numerically stable than Euler-angle representations for concatenated rotations.

In Doriax, all [Object](object.md) rotations are stored as quaternions. Euler angles, axis-angle, and matrix forms can be converted to/from quaternions using the provided static and instance methods.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | w | `1.0` | C++ \| Lua |
| float | x | `0.0` | C++ \| Lua |
| float | y | `0.0` | C++ \| Lua |
| float | z | `0.0` | C++ \| Lua |

### Static constants

| Name | Value |
| --- | --- |
| `IDENTITY` | `(1, 0, 0, 0)` — no rotation |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [fromEulerAngles](#fromeuler) | C++ \| Lua |
| void | [fromAngleAxis](#fromangleaxis) | C++ \| Lua |
| void | [fromAngle](#fromangle) | C++ \| Lua |
| void | [fromAxes](#fromaxes) | C++ \| Lua |
| Matrix4 | [getRotationMatrix](#getrotationmatrix) | C++ \| Lua |
| Vector3 | [getEulerAngles](#geteuler) | C++ \| Lua |
| Vector3 | [xAxis / yAxis / zAxis](#xaxis-yaxis-zaxis) | C++ \| Lua |
| float | [dot](#dot) | C++ \| Lua |
| float | [norm](#norm) | C++ \| Lua |
| Quaternion | [inverse](#inverse-unitinverse) | C++ \| Lua |
| Quaternion | [unitInverse](#inverse-unitinverse) | C++ \| Lua |
| Quaternion& | [normalize](#normalize-normalized) | C++ \| Lua |
| Quaternion | [normalized](#normalize-normalized) | C++ \| Lua |
| float | [normalizeL](#normalizel) | C++ \| Lua |
| float | [getRoll / getPitch / getYaw](#getroll-getpitch-getyaw) | C++ \| Lua |
| static Quaternion | [slerp](#slerp) | C++ \| Lua |
| static Quaternion | [nlerp](#nlerp) | C++ \| Lua |
| static Quaternion | [squad](#squad) | C++ \| Lua |
| std::string | [toString](#tostring) | C++ \| Lua |

## Enumerations

### RotationOrder

Controls the order in which Euler-angle rotations are applied when constructing a quaternion:

* **XYZ** — Roll, then Pitch, then Yaw
* **XZY**, **YXZ**, **YZX**, **ZXY**, **ZYX** — Other standard combinations

The most common order in Doriax is **XYZ**.

---

## Method details

### fromEuler

* void **fromEulerAngles**(float xAngle, float yAngle, float zAngle, const [RotationOrder](#rotationorder)& order)

Constructs the quaternion from Euler angles. Angles are in degrees if `Engine::useDegrees` is `true`.

=== "C++"
    ```cpp
    Quaternion q;
    q.fromEulerAngles(0.0f, 45.0f, 0.0f, RotationOrder::XYZ);
    obj.setRotation(q);
    ```

=== "Lua"
    ```lua
    local q = Quaternion()
    q:fromEulerAngles(0, 45, 0, RotationOrder.XYZ)
    obj:setRotation(q)
    ```

There is also a shorthand constructor:

=== "C++"
    ```cpp
    Quaternion q(0.0f, 45.0f, 0.0f);  // XYZ order, useDegrees aware
    ```

=== "Lua"
    ```lua
    local q = Quaternion(0, 45, 0)
    ```

---

### fromAngleAxis

* void **fromAngleAxis**(float angle, const Vector3& rkAxis)

Constructs the quaternion from an angle-axis representation. Useful for arbitrary-axis rotations.

=== "C++"
    ```cpp
    Quaternion q;
    q.fromAngleAxis(90.0f, Vector3::UNIT_Y);  // 90° around Y
    ```

=== "Lua"
    ```lua
    local q = Quaternion()
    q:fromAngleAxis(90, Vector3.UNIT_Y)
    ```

---

### fromAngle

* void **fromAngle**(float angle)

Constructs a 2D-style rotation around the Z axis. Convenience for 2D scenes.

---

### fromAxes

* void **fromAxes**(const Vector3& xaxis, const Vector3& yaxis, const Vector3& zaxis)

Builds the quaternion from an orthonormal basis of three axes.

---

### getRotationMatrix

* Matrix4 **getRotationMatrix**() const

Converts this quaternion to a `Matrix4` rotation matrix.

---

### getEuler

* Vector3 **getEulerAngles**(const [RotationOrder](#rotationorder)& order) const

Extracts Euler angles from this quaternion in the specified rotation order.

---

### xAxis / yAxis / zAxis

* Vector3 **xAxis**() const
* Vector3 **yAxis**() const
* Vector3 **zAxis**() const

Returns the local X, Y, or Z axis expressed in world space — equivalent to rotating the corresponding unit vector by this quaternion.

---

### dot

* float **dot**(const Quaternion& rkQ) const

Returns the dot product between two quaternions. Values near `1` indicate similar orientations; near `-1` indicate opposite orientations.

---

### norm

* float **norm**() const

Returns the squared length of the quaternion. A normalised quaternion has `norm()` = `1`.

---

### inverse / unitInverse

* Quaternion **inverse**() const
* Quaternion **unitInverse**() const

`inverse()` returns the inverse (safe for any non-zero quaternion). `unitInverse()` is faster but only correct for unit quaternions.

---

### normalize / normalized

* Quaternion& **normalize**()
* Quaternion **normalized**() const

`normalize()` scales the quaternion in-place to unit length. `normalized()` returns a new unit-length copy.

---

### normalizeL

* float **normalizeL**()

Normalises in-place and returns the original norm.

---

### getRoll / getPitch / getYaw

* float **getRoll**() const
* float **getPitch**() const
* float **getYaw**() const

Extracts the roll (Z), pitch (X), or yaw (Y) angle component.

---

### slerp

* static Quaternion **slerp**(float t, const Quaternion& q1, const Quaternion& q2)
* static Quaternion **slerp**(float t, const Quaternion& q1, const Quaternion& q2, bool shortestPath)

Spherical linear interpolation. `t=0` returns `q1`, `t=1` returns `q2`. When `shortestPath` is `true`, the interpolation always takes the shorter arc.

=== "C++"
    ```cpp
    Quaternion smoothRot = Quaternion::slerp(0.5f, startRot, endRot, true);
    ```

=== "Lua"
    ```lua
    local smoothRot = Quaternion.slerp(0.5, startRot, endRot, true)
    ```

---

### nlerp

* static Quaternion **nlerp**(float fT, const Quaternion& rkP, const Quaternion& rkQ)
* static Quaternion **nlerp**(float fT, const Quaternion& rkP, const Quaternion& rkQ, bool shortestPath)

Normalised linear interpolation. Cheaper than `slerp()` but not constant-speed; suitable for small angular differences or when speed uniformity is not critical.

---

### squad

* static Quaternion **squad**(float fT, const Quaternion& rkP, const Quaternion& rkA, const Quaternion& rkB, const Quaternion& rkQ)

Spherical cubic (SQUAD) interpolation between two quaternions `rkP` and `rkQ` with inner control points `rkA` and `rkB`. Used for smooth keyframe animation.

---

### toString

* std::string **toString**() const

Returns a string like `"Quaternion(1.000000, 0.000000, 0.000000, 0.000000)"`.
