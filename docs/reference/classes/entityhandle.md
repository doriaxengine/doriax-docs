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

When `true` (default), the entity is destroyed when the `EntityHandle` is destroyed. Set to `false` to keep the underlying entity alive after the handle goes out of scope — useful when you pass ownership to another system.

---

## Method details

### getScene

* Scene* **getScene**() const

Returns a pointer to the owning [Scene](scene.md).

---

### getEntity

* Entity **getEntity**() const

Returns the raw ECS entity identifier. Use this when interfacing with the low-level [EntityManager](entitymanager.md) or [EntityRegistry](entityregistry.md) APIs.
