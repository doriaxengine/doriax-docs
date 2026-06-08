---
description: EntityRegistry API reference — ECS entity and component API (C++ and Lua).
---

# EntityRegistry

Base of [Scene](scene.md). Entity/component CRUD and hierarchy.

## Methods

| Name | Description |
| --- | --- |
| `createEntity` / `createUserEntity` / `createSystemEntity` | Allocate ids |
| `destroyEntity` | Remove entity and components |
| `addEntityChild` | Parent/child link |
| `setEntityName` / `getEntityName` | Debug/editor names |
| `findComponent` / `addComponent` / `removeComponent` | ECS data access |
| `getEntityList` | All entity ids |

User entities start at id 1001; system entities use 1–1000.
