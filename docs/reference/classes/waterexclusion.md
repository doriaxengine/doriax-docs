---
description: WaterExclusion API reference (C++ and Lua) — a volume that keeps water out, like a boat: no water surface, underwater fade, or buoyancy inside it.
---

# WaterExclusion

**Inherits:** [Object](object.md)  
**C++ type:** `WaterExclusion`

## Description

A volume that keeps [Water](water.md) out, like the inside of a boat. Inside it the water
surface is not drawn, a camera sees no [underwater](water.md#underwater) fade, and dynamic
bodies get no [buoyancy](body3d.md#buoyancy), so cargo rests on the floor of a boat instead
of floating on the sea outside. Constructing a `WaterExclusion` attaches a
`WaterExclusionComponent` to the entity, and the volume moves, rotates, and scales with it.

The default **HULL** shape wraps the convex hull of the entity's meshes, or of its model's
mesh nodes, and is rebuilt when they change. On a boat it is the outer hull closed over the
top at the gunwale, so the component goes on the boat itself. **BOX** and **SPHERE** fill a
volume of their own, for a cabin, a cave, or a diving bell.

=== "C++"

    ```cpp
    // keeps the water out of a boat
    boat.addComponent<WaterExclusionComponent>();

    // a dry room below the sea
    WaterExclusion room(&scene);
    room.setShape(WaterExclusionShape::BOX);
    room.setPosition(0.0f, -3.0f, 0.0f);
    room.setSize(6.0f, 3.0f, 4.0f);
    ```

=== "Lua"

    ```lua
    -- a dry room below the sea
    local room = WaterExclusion(scene)
    room.shape = WaterExclusionShape.BOX
    room:setPosition(0, -3, 0)
    room:setSize(6, 3, 4)
    ```

A body that owns the volume, on its own entity or on a child of it, still floats: the boat
keeps its buoyancy while what it carries loses it. See
[Rendering Pipeline — Water exclusions](../../manual/rendering-pipeline.md#water-exclusions)
for how the surface is cut.

Hidden, on its own entity or through an ancestor, the volume no longer cuts the surface,
stops the underwater fade or leaves a wake, and its wake starts afresh when it shows again.
Bodies inside it still lose their buoyancy, as hiding leaves physics running.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [WaterExclusionShape](#waterexclusionshape) | [shape](#shape) | `HULL` | C++ \| Lua |
| [Vector3](vector3.md) | [center](#center-size) | `Vector3(0, 0, 0)` | C++ \| Lua |
| [Vector3](vector3.md) | [size](#center-size) | `Vector3(1, 1, 1)` | C++ \| Lua |
| float | [wakeFoam](#wakefoam-wakewaves) | `0.0` | C++ \| Lua |
| float | [wakeWaves](#wakefoam-wakewaves) | `0.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setCenter](#center-size) | C++ \| Lua |
| void | [setSize](#center-size) | C++ \| Lua |
| bool | [contains](#contains) | C++ \| Lua |
| [WaterExclusionComponent](waterexclusioncomponent.md) | `getWaterExclusionComponent` | Lua |

## Enumerations

### WaterExclusionShape

* **BOX** — A box of [size](#center-size) around [center](#center-size).
* **SPHERE** — An ellipsoid of [size](#center-size) around [center](#center-size).
* **HULL** — The convex hull of the entity's meshes.

---

## Property details

### shape

* *Setter*: void **setShape**([WaterExclusionShape](#waterexclusionshape) shape)
* *Getter*: [WaterExclusionShape](#waterexclusionshape) **getShape**() const

A hull is convex, so a boat with a dip in its outline, like a catamaran, takes one volume
per hull, each on its own mesh. Building a hull needs 3D physics, which projects have
unless they turn `DORIAX_PHYSICS_3D` off (see [Build Options](../build-options.md#enginelibrary-options)).

---

### center / size

* *Setter*: void **setCenter**([Vector3](vector3.md) center)
* *Setter*: void **setCenter**(const float x, const float y, const float z)
* *Getter*: [Vector3](vector3.md) **getCenter**() const
* *Setter*: void **setSize**([Vector3](vector3.md) size)
* *Setter*: void **setSize**(const float x, const float y, const float z)
* *Getter*: [Vector3](vector3.md) **getSize**() const

The box or sphere in the entity's local space: `size` is its width, height, and depth,
centred on `center`. A hull ignores them.

---

### wakeFoam / wakeWaves

* *Setter*: void **setWakeFoam**(float wakeFoam)
* *Getter*: float **getWakeFoam**() const
* *Setter*: void **setWakeWaves**(float wakeWaves)
* *Getter*: float **getWakeWaves**() const

What the volume leaves on a [Water](water.md) while it moves across its surface, from `0`
(nothing, the default) to `2`. The wake follows the motion of the entity, whatever moves
it — physics, a script or an animation — so a boat only needs these set:

- **Foam** stays where it forms and fades there: churned behind the stern and, closer to
  hull speed, along the sides and at the bow, where the bow waves of a fast hull break.
- **Waves** spread from where the bow passed, at the Kelvin angle of 19.5° on each side,
  narrowing past a length Froude number of about 0.5, with the transverse waves crossing
  between them. They bend the surface, so they show in its light and reflections.

Both grow with the speed relative to the hull speed of the volume's length, so a small
boat drifting leaves almost nothing and one near its hull speed a full wake. The water
keeps the wakes in a square around the camera and fades them over its
[wakeFade](water.md#wakearea-wakefade). Waves stay on the water they were made on, even
after the volume leaves it. The waterline is taken as an ellipse inside the volume's
bounds, facing the motion.

=== "C++"

    ```cpp
    WaterExclusion hull(&scene, boat);
    hull.setWakeFoam(1.0f);
    hull.setWakeWaves(1.0f);
    ```

=== "Lua"

    ```lua
    local hull = WaterExclusion(self.scene, self.entity)
    hull.wakeFoam = 1
    hull.wakeWaves = 1
    ```

The wake is drawn by the built-in water shader; a fork of an older version draws none until
it is forked again.

---

## Method details

### contains

* bool **contains**([Vector3](vector3.md) point) const

Whether the world point is inside the volume, tested as buoyancy tests it. Gameplay that
should agree with the water, like the air of a diver, can use it:

=== "Lua"

    ```lua
    local cabin = WaterExclusion(self.scene, self.entity)
    if cabin:contains(diver:getWorldPosition()) then
        oxygen = maxOxygen -- breathing in the dry cabin
    end
    ```

The volume is placed by the render update, so a new one contains nothing until the next
frame.
