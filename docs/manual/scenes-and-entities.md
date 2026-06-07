---
description: How scenes and entities are structured in Doriax Engine.
---

# Scenes &amp; Entities

A **scene** is the container for everything that exists in a part of your game: the
objects, cameras, lights, and the systems that update them. A game is made up of one or
more scenes that you switch between at runtime.

## Scenes

A scene owns a collection of entities and drives their updates each frame. You create a
scene, populate it with entities, and tell the engine to run it.

=== "Lua"

    ```lua
    scene = Scene()

    -- ... add entities to the scene ...

    Engine.setScene(scene)
    ```

=== "C++"

    ```cpp
    Scene scene;

    // ... add entities to the scene ...

    Engine::setScene(&scene);
    ```

You can have multiple scenes loaded — for example, a gameplay scene and a separate UI
overlay scene — and control which one is active.

## Entities

An **entity** is a lightweight identifier that lives in a scene. By itself an entity
holds no behavior or data; it gains both by having **components** attached to it. This
is the foundation of the [Entity Component System](entity-component-system.md).

Higher-level objects in Doriax — such as a `Polygon`, a sprite, or a 3D model — are
convenience wrappers that create an entity and attach the components it needs.

```lua
scene = Scene()
triangle = Polygon(scene)   -- creates an entity in the scene with the right components

triangle.position = Vector3(300, 300, 0)
triangle:setColor(0.6, 0.2, 0.6, 1)
```

## Transforms

Most visible entities have a transform that defines their **position**, **rotation**,
and **scale** in space. Transforms can be parented to build hierarchies — moving a
parent moves its children with it.

```lua
entity.position = Vector3(300, 300, 0)
entity.rotation = Quaternion(0, 0, 0)
entity.scale = Vector3(1, 1, 1)
```

## Next steps

Continue to the [Entity Component System](entity-component-system.md) to understand how
data and behavior are organized under the hood.
