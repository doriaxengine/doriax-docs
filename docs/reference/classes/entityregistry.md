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
| `findEntity` | Look up an existing entity by name |
| `findComponent` / `addComponent` / `removeComponent` | ECS data access |
| `getEntityList` | All entity ids |

User entities start at id 1001; system entities use 1–1000.

## findEntity

```
Entity findEntity(name)
Entity findEntity(name, parent)
```

Returns the first entity whose name (as shown in the editor Structure panel) matches
`name`, or `NULL_ENTITY` when there is no match. The two-argument form restricts the
search to descendants of `parent`, so you can resolve a named child without relying on
globally unique names.

Use it to reference an entity that already exists in the scene — for example a child
model you want to animate — and then wrap it with the matching object handle:

```lua
local modelEntity = self.scene:findEntity("model", self.entity)
if modelEntity ~= NULL_ENTITY then
    local model = Model(self.scene, modelEntity)   -- wraps; does not create
    model:getAnimation(0):start()
end
```

!!! tip "Wrap, don't recreate"
    Pass the found entity to the **two-argument** handle constructor
    (`Model(scene, entity)`). The one-argument form (`Model(scene)`) creates a brand-new
    entity instead of referencing the existing one. See
    [Referencing other entities](../../manual/creating-scripts.md#referencing-other-entities).

The name lookup is linear over the entity list; cache the result in `init()` rather than
calling it every frame.
