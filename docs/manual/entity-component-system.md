---
description: Understand the data-oriented Entity Component System that powers Doriax Engine.
---

# Entity Component System

Doriax is built on a modern **Entity Component System (ECS)** with data-oriented design
at its core. This architecture is what keeps the engine lightweight and fast.

## The three pieces

| Concept | Role |
| --- | --- |
| **Entity** | A lightweight identifier. Holds no data or behavior on its own. |
| **Component** | A plain block of data attached to an entity (e.g. transform, mesh, physics body). |
| **System** | Logic that processes all entities sharing a given set of components. |

Instead of deep inheritance hierarchies, behavior emerges from **composition**: you
attach the components an entity needs, and systems operate on whatever entities have the
relevant components.

## Why data-oriented?

Traditional object-oriented designs scatter objects across memory, causing frequent
cache misses as the CPU jumps around to process them. Doriax arranges component data
contiguously so that systems iterate over tightly-packed arrays.

This **data-oriented** layout:

- Maximizes CPU cache utilization
- Reduces per-object overhead
- Scales well as the number of entities grows
- Keeps the engine lean and predictable

!!! tip "Mental model"
    Think of components as columns in a table and entities as rows. A system reads the
    columns it cares about, row by row, in a tight loop.

## Working with the ECS

In day-to-day use you usually work through the higher-level objects the engine provides
(sprites, models, cameras, lights). Each of these creates an entity and attaches the
appropriate components for you, so you get the performance benefits of the ECS without
managing components by hand.

```lua
scene = Scene()
sprite = Sprite(scene)   -- entity + transform + mesh/material components

sprite.position = Vector3(100, 100, 0)
```

As your needs grow, you can work with components more directly to build custom behavior
and systems on top of the same foundation.

## Next steps

See [Scripting](scripting.md) to learn how Lua and C++ drive your game logic on top of
the ECS.
