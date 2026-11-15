---
description: Collider3D API reference — a Body3D or a Character3D, the two sides of the 3D contact events.
---

# Collider3D

## Description

`Collider3D` is what an entity is in the 3D physics world: a [Body3D](body3d.md) or a
[Character3D](character3d.md). It is the base class of both, and the type of the two sides of
the 3D contact events and of `shouldCollide3D`, so one handler serves bodies and characters:
ask the side what it is, then use its own handle.

An entity with both a Body3D and a Character3D counts as its body. The character's inner body
is reported to nobody, so a side always matches the component that touched.

In Lua the sides arrive as the Body3D or the Character3D itself, with all of its own
properties and methods, and `isCharacter3D()` tells them apart.

**Inherits:** [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    void Spring::onContactAdded(Collider3D colliderA, Collider3D colliderB, Contact3D contact){
        Collider3D other = (colliderA.getEntity() == entity) ? colliderB : colliderA;
        if (other.isCharacter3D()){
            other.getCharacter3D().jump(8.0f);
        }else if (other.isBody3D()){
            other.getBody3D().applyImpulse(Vector3(0, 4, 0));
        }
    }
    ```

=== "Lua"

    ```lua
    function Spring:onContactAdded(colliderA, colliderB, contact)
        local other = colliderA.entity == self.entity and colliderB or colliderA
        if other:isCharacter3D() then
            other:jump(8)
        else
            other:applyImpulse(Vector3(0, 4, 0))
        end
    end
    ```

### Properties

| Type | Name | Languages |
| --- | --- | --- |
| Vector3 | [position](#position) | C++ \| Lua |
| Vector3 | [linearVelocity](#linearvelocity) | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| bool | [isBody3D](#isbody3d-ischaracter3d) | C++ \| Lua |
| bool | [isCharacter3D](#isbody3d-ischaracter3d) | C++ \| Lua |
| [Body3D](body3d.md) | [getBody3D](#getbody3d-getcharacter3d) | C++ \| Lua |
| [Character3D](character3d.md) | [getCharacter3D](#getbody3d-getcharacter3d) | C++ \| Lua |
| [Object](object.md) | [getAttachedObject](#getattachedobject) | C++ \| Lua |

## Contact events

| Event | Signature |
| --- | --- |
| `onContactAdded3D` / `onContactPersisted3D` | `void(Collider3D, Collider3D, Contact3D)` |
| `onContactRemoved3D` | `void(Collider3D, Collider3D, unsigned long, unsigned long)` |
| `shouldCollide3D` | `bool(Collider3D, Collider3D, Vector3, CollideShapeResult3D)` |

A character takes part through its inner body, so it reaches these events only with
[Inner Body](character3d.md#contacts-and-the-inner-body) on. `onBodyActivated3D` and
`onBodyDeactivated3D` keep their [Body3D](body3d.md) and skip characters.

In `onContactRemoved3D` Jolt holds both bodies, so use the sides there only to know which
entities parted. Reading a side's position or velocity trips a Jolt assertion in debug builds.
See [What a 3D callback may do](../../manual/physics.md#what-a-3d-callback-may-do).

## Property details

### position

* `Vector3 getPosition()`

Where the body or the character is in the world, as its own `position` reads it. It is
read-only here: move it through [getBody3D](#getbody3d-getcharacter3d) or
[getCharacter3D](#getbody3d-getcharacter3d).

---

### linearVelocity

* `Vector3 getLinearVelocity()`

How fast the body or the character moves, in meters per second, as its own `linearVelocity`
reads it. It is read-only here.

## Method details

### isBody3D / isCharacter3D

* `bool isBody3D()`
* `bool isCharacter3D()`

Which one the entity is. An entity with both components is a body, so at most one of them is
`true`; both are `false` for an entity with neither.

---

### getBody3D / getCharacter3D

* `Body3D getBody3D()`
* `Character3D getCharacter3D()`

The handle of the same entity as a body or as a character. Unlike
[Object](object.md#getbody3d), neither adds a component, so check
[isBody3D or isCharacter3D](#isbody3d-ischaracter3d) first: the methods of a handle whose
component is missing fail.

---

### getAttachedObject

* `Object getAttachedObject()`

Returns the [Object](object.md) that owns the body or the character.
