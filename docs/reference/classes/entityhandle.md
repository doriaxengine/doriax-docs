---
description: EntityHandle API reference (C++ and Lua).
---

# EntityHandle

**C++ type:** `EntityHandle`

## Description

The base class for all high-level Doriax objects that wrap an ECS entity. `EntityHandle` stores a reference to its owning `Scene` and its `Entity` identifier, giving C++ and Lua code a convenient handle to a scene entity without having to interact with the raw ECS API.

Most classes in the Doriax API — [Object](object.md), [Action](action.md), [Sound](sound.md), [Skybox](skybox.md), etc. — inherit from `EntityHandle`.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| std::string | [name](#name) | `""` | C++ \| Lua |
| bool | [entityOwned](#entityowned) | `true` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| Scene* | [getScene](#getscene) | C++ \| Lua |
| Entity | [getEntity](#getentity) | C++ \| Lua |

## Property details

### name

* *Setter*: void **setName**(const std::string& name)
* *Getter*: std::string **getName**() const

Human-readable tag for this entity. Used by the editor to display entities in the scene hierarchy, and can be used in game code for debugging or lookup.

---

### entityOwned

* *Setter*: void **setEntityOwned**(bool entityOwned)
* *Getter*: bool **isEntityOwned**() const

Whether this handle *owns* its entity. When `true`, the entity is destroyed (and any
sub-resources it set up are cleared) when the handle is destroyed. Set it to `false` to
detach the handle from the entity's lifetime.

The value is decided by which constructor you use:

| Constructor | Owns the entity? |
| --- | --- |
| `Type(scene)` | `true` — creates a **new** entity |
| `Type(scene, entity)` | `false` — **wraps** an existing entity |

---

## Ownership and lifetime

`EntityHandle` follows single-owner semantics so an entity is never destroyed twice:

- **Copying** produces a non-owning observer. `Type b = a;` leaves `a` as the sole owner
  (if it was one) and `b` referencing the same entity without owning it.
- **Moving** transfers ownership. `Type b = std::move(a);` makes `b` the owner and leaves
  `a` as a non-owning observer.
- **Wrapping** an existing entity (`Type(scene, entity)`) never owns it, so references you
  pass around — including handles resolved from script properties or
  [`Scene:findEntity`](entityregistry.md#findentity) — are safe to copy and discard.

!!! warning "Keep owning handles alive"
    An owning handle destroys its entity when it is itself destroyed — in Lua that happens
    when the handle is garbage-collected. If you create an entity at runtime with
    `Type(scene)` and want it to persist, store the handle (e.g. in `self`), or call
    `setEntityOwned(false)` to hand the entity's lifetime to the scene.

---

## Method details

### getScene

* Scene* **getScene**() const

Returns a pointer to the owning [Scene](scene.md).

---

### getEntity

* Entity **getEntity**() const

Returns the raw ECS entity identifier. Use this when interfacing with the low-level [EntityManager](entitymanager.md) or [EntityRegistry](entityregistry.md) APIs.
