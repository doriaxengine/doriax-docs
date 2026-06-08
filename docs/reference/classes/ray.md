---
description: Ray API reference (C++ and Lua).
---

# Ray

**C++ type:** `Ray`

## Description

A ray defined by an origin point and a direction/length vector. Used for raycasting — detecting which objects lie along the ray. Doriax supports raycasts against geometric volumes ([AABB](aabb.md), [OBB](obb.md), [Sphere](sphere.md), [Plane](plane.md)) and against the physics simulation ([Body2D](body2d.md) / [Body3D](body3d.md)).

The direction vector doubles as the *length* of the ray — objects beyond `origin + direction` are not reported as hits.

### Properties

| Type | Name | Langs |
| --- | --- | --- |
| Vector3 | [origin](#origin-direction) | C++ \| Lua |
| Vector3 | [direction](#origin-direction) | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| Vector3 | [getPoint](#getpoint) | C++ \| Lua |
| [RayReturn](rayreturn.md) | [intersects](#intersects) | C++ \| Lua |

## Property details

### origin / direction

* *Setter*: void **setOrigin**(Vector3 point) / void **setDirection**(Vector3 direction)
* *Getter*: Vector3 **getOrigin**() const / Vector3 **getDirection**() const

`origin` is the start of the ray. `direction` is both the normalised direction and the maximum reach (its magnitude = ray length). Use `Camera::screenToRay()` to generate a ray from a screen pixel.

---

## Method details

### getPoint

* Vector3 **getPoint**(float distance) const

Returns the world-space point at `distance` units along the ray: `origin + direction.normalized() * distance`.

---

### intersects

Multiple overloads for different collision targets:

* [RayReturn](rayreturn.md) **intersects**(const Plane& plane) const
* [RayReturn](rayreturn.md) **intersects**(const AABB& box) const
* [RayReturn](rayreturn.md) **intersects**(const OBB& obb) const
* [RayReturn](rayreturn.md) **intersects**(const Sphere& sphere) const
* [RayReturn](rayreturn.md) **intersects**(const Body2D& body) const
* [RayReturn](rayreturn.md) **intersects**(const Body3D& body) const
* [RayReturn](rayreturn.md) **intersects**(Scene* scene, [RayFilter](#rayfilter) raytest) const
* [RayReturn](rayreturn.md) **intersects**(Scene* scene, [RayFilter](#rayfilter) raytest, bool onlyStatic) const
* [RayReturn](rayreturn.md) **intersects**(Scene* scene, [RayFilter](#rayfilter) raytest, uint16_t categoryBits, uint16_t maskBits) const

Returns a [RayReturn](rayreturn.md) struct. Test the result with `if (result)` or `result.hit`.

=== "C++"
    ```cpp
    // Screen-to-world raycast
    Ray ray = camera.screenToRay(mouseX, mouseY);
    RayReturn hit = ray.intersects(&scene, RayFilter::BODY_3D);
    if (hit) {
        Log::print("Hit body at distance: " + std::to_string(hit.distance));
    }
    ```

=== "Lua"
    ```lua
    local ray = camera:screenToRay(mouseX, mouseY)
    local hit = ray:intersects(scene, RayFilter.BODY_3D)
    if hit.hit then
        Log.print("Hit at " .. tostring(hit.distance))
    end
    ```

## Enumerations

### RayFilter

* **BODY_2D** — Test against [Body2D](body2d.md) physics bodies.
* **BODY_3D** — Test against [Body3D](body3d.md) physics bodies.
