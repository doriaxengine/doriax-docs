---
description: Character3D API reference — a walking 3D character on Jolt Physics' CharacterVirtual, with steps, ramps and ground detection.
---

# Character3D

## Description

`Character3D` moves a 3D character over the physics world: it walks along the ground, climbs
steps, walks up ramps that are not too steep, slides down the ones that are, keeps to the ground
going down, rides moving platforms, pushes dynamic bodies and falls with gravity. It is built on
**Jolt Physics' CharacterVirtual**, so it is not a rigid body: it never tips over, never bounces
and never slides on its own when it stands still.

The character is a [Character3DComponent](character3dcomponent.md) on the entity, added in the
Properties window with **New component → 3D Character**. Its capsule stands on the entity
origin, so a model whose origin is at its feet needs no offset. The entity needs no
[Body3D](body3d.md); a static Body3D under it is the ground.

Get the handle with `Character3D(scene, entity)`, or with
[getCharacter3D](object.md#getcharacter3d) of an [Object](object.md), which also adds the
component to an entity that has none, as one a script creates. A script sets where it wants to walk with
[moveVelocity](#movevelocity) and jumps with [jump](#jump); each fixed step the physics system
applies gravity, moves the character and writes its position to the entity's transform. The
rotation stays where scripts put it.

**Inherits:** [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    Character3D character(scene, entity);

    character.setMoveVelocity(direction * 4.0f);
    if (character.isOnGround() && Input::isKeyPressed(D_KEY_SPACE)){
        character.jump(5.0f);
    }
    ```

=== "Lua"

    ```lua
    local character = Character3D(self.scene, self.entity)

    character.moveVelocity = direction * 4
    if character:isOnGround() and Input.isKeyPressed(Input.KEY_SPACE) then
        character:jump(5)
    end
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| Vector3 | [moveVelocity](#movevelocity) | `(0,0,0)` | C++ \| Lua |
| Vector3 | [linearVelocity](#linearvelocity) | `(0,0,0)` | C++ \| Lua |
| Vector3 | [position](#position) | — | C++ \| Lua |
| float | [maxSlopeAngle](#maxslopeangle) | `45` | C++ \| Lua |
| float | [stepUp](#stepup-stepdown) | `0.4` | C++ \| Lua |
| float | [stepDown](#stepup-stepdown) | `0.5` | C++ \| Lua |
| float | [mass](#mass-maxstrength) | `70` | C++ \| Lua |
| float | [maxStrength](#mass-maxstrength) | `100` | C++ \| Lua |
| float | [gravityFactor](#gravityfactor) | `1` | C++ \| Lua |
| float | [airControl](#aircontrol) | `1` | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [jump](#jump) | C++ \| Lua |
| [Character3DGroundState](#character3dgroundstate) | [getGroundState](#ground-detection) | C++ \| Lua |
| bool | [isOnGround](#ground-detection) | C++ \| Lua |
| bool | [isSupported](#ground-detection) | C++ \| Lua |
| Vector3 | [getGroundPosition](#ground-detection) | C++ \| Lua |
| Vector3 | [getGroundNormal](#ground-detection) | C++ \| Lua |
| Vector3 | [getGroundVelocity](#ground-detection) | C++ \| Lua |
| Entity | [getGroundEntity](#ground-detection) | C++ \| Lua |
| bool | [isSlopeTooSteep](#ground-detection) | C++ \| Lua |
| bool | [setShape](#setshape) | C++ \| Lua |
| float | getHeight | C++ \| Lua |
| float | getRadius | C++ \| Lua |
| void | [load](#load) | C++ \| Lua |
| Object | getAttachedObject | C++ \| Lua |
| JPH::CharacterVirtual* | getJoltCharacter | C++ |
| [Character3DComponent](character3dcomponent.md) | getCharacter3DComponent | Lua |

## Enumerations

### Character3DGroundState

* **ON_GROUND** — Standing on something it can walk on.
* **ON_STEEP_GROUND** — Touching a slope steeper than [maxSlopeAngle](#maxslopeangle). It
  slides down and cannot walk up it.
* **NOT_SUPPORTED** — Touching something that does not hold it up, like the side of a wall
  while falling.
* **IN_AIR** — Touching nothing.

## Property details

### moveVelocity

* *Setter:* `void setMoveVelocity(Vector3)`
* *Getter:* `Vector3 getMoveVelocity() const`

The velocity the character walks with, in world units per second. Only its horizontal part is
used, so a direction from the camera can be passed as it is. It is kept until changed: set it
every frame from input, and set it to zero to stop.

On the ground the character walks at this velocity plus the velocity of what it stands on, so
it rides moving platforms. Up a ramp it is slower, the steeper the more: Jolt's
CharacterVirtual takes out the part of the velocity that points into the slope, which leaves
about 85% of the speed on a 20 degree ramp. Down a ramp it keeps the speed. Walking into a step no higher than [stepUp](#stepup-stepdown) climbs
it; walking into a wall or a slope that is too steep slides along it. In the air,
[airControl](#aircontrol) sets how much of it applies.

---

### linearVelocity

* *Setter:* `void setLinearVelocity(Vector3)`
* *Getter:* `Vector3 getLinearVelocity() const`

The velocity the last step moved the character with, gravity, jumps and the ground's velocity
included. Walls and the ground stop the character without changing it: standing, it reads a
small downward speed, and against a wall the full walking speed. Use the
[ground state](#ground-detection) to tell standing from falling.

Setting an upward velocity launches the character, like a jump pad. The horizontal part comes
from [moveVelocity](#movevelocity) on the ground, and in the air [airControl](#aircontrol)
sets how much of it stays.

---

### position

* *Setter:* `void setPosition(Vector3)`
* *Getter:* `Vector3 getPosition() const`

The feet of the character, in world space. Setting it teleports the character and the entity's
transform at once and finds its contacts again, so `isOnGround` is right before the next step.
Called from a physics callback, such as a sensor's `onContactAdded3D`, the teleport waits for
the next step.

Moving the entity's [Object](object.md) transform from a script or an animation also teleports
the character at the next step.

---

### maxSlopeAngle

The steepest ground, in degrees, that the character walks on. Steeper ground reports
`ON_STEEP_GROUND`: the character slides down it and walking into it does not climb it.

---

### stepUp / stepDown

`stepUp` is the highest step, in world units, that the character climbs while walking. The
rounded bottom of the capsule rides over a low edge by itself, up to about
`radius * (1 - cos(maxSlopeAngle))` (0.09 m for the default capsule), and that height adds to
`stepUp` on a sharp edge. `0` leaves only what the rounded bottom climbs.

`stepDown` is how far the character follows the ground down when it walks off a step or down a
ramp. Without it the character would leave the ground and fall a short way at every step.
`0` turns it off. Keep it larger than the steps it walks down.

---

### mass / maxStrength

`mass` (kg) is the weight the character puts on dynamic bodies it stands on. `maxStrength` (N)
is the force it pushes dynamic bodies with when it walks into them: a body heavier than that
force can move against its friction stays where it is.

---

### gravityFactor

Scales the scene's 3D gravity for this character. `0` makes it fly where
[moveVelocity](#movevelocity) and [linearVelocity](#linearvelocity) take it.

---

### airControl

How much the character steers in the air, from `0` to `1`. `1` moves it in the air as on the
ground. `0` keeps the horizontal velocity it had when it left the ground, so a jump follows its
arc whatever the input. Values in between steer from that velocity towards
[moveVelocity](#movevelocity) at every fixed step.

## Method details

### jump

* `void jump(float speed)`

At the next fixed step the character leaves with this upward speed, added to the velocity of
the ground it stands on. It does not check the ground itself: call it when
[isOnGround](#ground-detection) is true, or count jumps for a double jump. A ceiling stops the
rise at once.

The height of a jump is about `speed * speed / (2 * gravity)`: `5` reaches about 1.25 m with the
default gravity.

---

### Ground detection

* `Character3DGroundState getGroundState() const`
* `bool isOnGround() const` — `ON_GROUND`
* `bool isSupported() const` — `ON_GROUND` or `ON_STEEP_GROUND`
* `Vector3 getGroundPosition() const` — contact point, world space
* `Vector3 getGroundNormal() const`
* `Vector3 getGroundVelocity() const` — of the ground at the contact point
* `Entity getGroundEntity() const` — the body or character it stands on or leans against, `NULL_ENTITY` when it touches nothing
* `bool isSlopeTooSteep(Vector3 normal) const`

The state of the last fixed step. Use `isOnGround` to allow a jump and `isSupported` to choose
between a walking and a falling animation, so the character does not play its falling clip
while it slides down a steep slope.

=== "Lua"

    ```lua
    local clip = "Idle"
    if not character:isSupported() then
        clip = "Fall"
    elseif moving then
        clip = "Walk"
    end
    ```

---

### setShape

* `bool setShape(float height, float radius)`

Changes the capsule while the character keeps playing, for example to crouch. It returns
`false` and keeps the old capsule when the new one would not fit where the character stands,
so a crouching character cannot stand up under a low ceiling. Like the component values, the
sizes are scaled by the entity's scale. It cannot be called from a physics callback.

=== "Lua"

    ```lua
    if Input.isKeyPressed(Input.KEY_C) then
        character:setShape(1.0, 0.35)
    elseif not character:setShape(2.0, 0.35) then
        -- still under something low, stays crouched
    end
    ```

---

### load

* `void load()`

Rebuilds the character from its [Character3DComponent](character3dcomponent.md). Call it after
changing a component value that only applies when the character is built: `height`, `radius`,
`padding` or `innerBody`. The physics system builds the character on its own when the scene
loads, and the methods that read or move the character build it when a script's `init` runs
first.

## Contacts and the inner body

With **Inner Body** on (the default), the character carries a kinematic body inside its
capsule. Rays, sensors and contact callbacks find the character through it: a ray from
[Ray](ray.md)`::intersects` returns the character's entity, and a sensor's
`onContactAdded3D` receives it. That entity has no Body3D, so compare it with
`getEntity()` (`entity` in Lua) rather than calling body methods on it. `onBodyActivated3D` and
`onBodyDeactivated3D` are for Body3D only and skip it. Other characters do not collide with
inner bodies; characters block each other directly.

Sensors never block the character.
