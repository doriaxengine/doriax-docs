---
description: SubSystem API reference (C++ and Lua), the base class of the scene systems.
---

# SubSystem

Base class of the systems each [Scene](scene.md) runs: [ActionSystem](actionsystem.md),
[AudioSystem](audiosystem.md), [MeshSystem](meshsystem.md), [PhysicsSystem](physicssystem.md),
[RenderSystem](rendersystem.md), and [UISystem](uisystem.md).

## Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| bool | paused | `false` | C++ \| Lua |

While `paused` is `true` the system skips its update, so what it drives stops changing in
that scene; the scene is still drawn. A paused AudioSystem also pauses the scene's playing
sounds. In C++ the property is `setPaused(bool)` / `isPaused()`.

Pausing Play in the editor sets it on the physics, action, and audio systems, and resuming
clears it.

=== "Lua"

    ```lua
    scene:getPhysicsSystem().paused = true
    ```

=== "C++"

    ```cpp
    scene->getSystem<PhysicsSystem>()->setPaused(true);
    ```
