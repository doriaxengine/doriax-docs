---
description: Scenes, entities, transforms, scene types, child scenes, and bundles in Doriax Engine.
---

# Scenes & Entities

A **scene** is the container for everything that exists in a part of your game:
entities, cameras, lights, physics, scripts, and the systems that update them each
frame. A game is typically made of one or more scenes that you create, configure, and
switch between at runtime.

## Scenes

A scene owns a collection of entities and drives their updates. Internally, `Scene`
extends `EntityRegistry`, so it owns entity allocation, component storage, and subsystem
registration. You create a scene, populate it with entities, and tell the engine to run
it.

=== "Lua"

    ```lua
    scene = Scene()
    -- ... add entities ...
    Engine.setScene(scene)
    ```

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Scene scene;
    // ... add entities ...
    Engine::setScene(&scene);
    ```

You can have several scenes loaded at the same time. The most common pattern is one
main scene for gameplay with additional scene layers for overlays, menus, or transition
effects.

| Operation | C++ API |
| --- | --- |
| Set the main scene | `Engine::setScene(scene)` |
| Add an overlay/layer | `Engine::addSceneLayer(scene)` |
| Execute once and discard | `Engine::executeSceneOnce(scene)` |
| Remove one layer | `Engine::removeScene(scene)` |
| Clear all scenes | `Engine::removeAllScenes()` |

For project-level scene switching, use `SceneManager` to register scene factories and
load scenes by name or numeric ID:

=== "C++"

    ```cpp
    SceneManager::registerScene(1, "Level1", []() {
        static Scene level;
        Engine::setScene(&level);
    });

    SceneManager::loadScene("Level1");
    ```

## Scene types

All scenes use the same `Scene` class and ECS foundation at runtime. The **scene type**
is an authoring concept that tells the editor which defaults, camera setup, and tools to
use.

| Type | Editor defaults | Typical use |
| --- | --- | --- |
| **3D** | Perspective camera, 3D gizmos, lighting setup | Open-world levels, first/third-person games, 3D platformers |
| **2D** | Orthographic camera, canvas gizmos, 2D tools | Top-down games, side-scrollers, puzzle games, tilemaps |
| **UI** | Screen-space canvas, anchor gizmos | Menus, HUDs, settings screens, overlays |

A 3D scene can contain UI entities, and a UI scene can reference 2D or 3D child scenes.
This compositing model is the foundation for in-game HUDs: create a separate **UI
scene** and add it as a scene layer on top of the gameplay scene.

```lua
-- Load a HUD scene on top of the main gameplay scene
Engine.setScene(gameplayScene)
Engine.addSceneLayer(hudScene)
```

## Entities

An **entity** is a lightweight integer identifier that lives in a scene. By itself it
holds no behavior or data; it gains both by having **components** attached to it. This
is the core of the [Entity Component System](entity-component-system.md).

Higher-level objects in Doriax — `Sprite`, `Model`, `Camera`, `Button`, etc. — are
convenience wrappers. They create or reference an entity and manipulate the components
it needs for you.

```lua
scene = Scene()
triangle = Polygon(scene)
triangle.position = Vector3(300, 300, 0)
triangle:setColor(0.6, 0.2, 0.6, 1)
```

## Transforms

Most visible entities have a **Transform** component that defines their **position**,
**rotation**, and **scale** in space. Transforms can be parented to build hierarchies —
moving a parent moves all its children with it.

```lua
entity.position = Vector3(300, 300, 0)
entity.rotation = Quaternion(0, 0, 0)
entity.scale    = Vector3(1, 1, 1)
```

When an entity has a parent, its world transform is derived from the full parent chain.
Local transforms are relative to the parent; world transforms are absolute.

## Entities without transforms

Not every entity needs a Transform. Non-transform entities are useful for:

- Logic-only scripts and global state
- Non-spatial (2D panned) audio
- Scene environment components like Fog or Skybox
- Physics joints that link two body entities
- Actions and animations targeting another entity

In the editor's [Structure Panel](../editor/structure.md), these entities appear in a
separate area above the transform hierarchy. They can be selected and edited but cannot
be parented until a Transform is added.

## Scene settings

Every scene owns rendering and interaction state that affects all entities within it:

| Setting | Purpose |
| --- | --- |
| Active camera | The `Camera` entity used for rendering |
| Background color | Clear color for the scene |
| Shadows PCF | Percentage-closer filtering for smoother shadow edges |
| Light state | `OFF`, `ON`, or `AUTO` (auto-detects lights in the scene) |
| Global illumination | Ambient light color and intensity |
| UI events | Enables/disables UI input processing for the scene |
| Canvas size | Logical resolution for 2D and UI scenes |

## Child scenes

A **child scene** reference lets one scene load and run another. Child scenes share the
same engine tick but maintain their own entity and component storage. Use them for:

- **Persistent UI** — a HUD scene that stays loaded across gameplay level changes.
- **Shared setup** — a single lighting and skybox scene included in every level.
- **Additive worlds** — large open worlds assembled from independently-authored chunks.
- **Scene streaming** — load and unload sections without a full scene transition.

In the editor, add a child scene reference from the Structure panel's **Add Child
Scene** option.

## Bundles

**Bundles** are reusable entity hierarchy templates — similar to prefabs in other
engines. They let you define a configured group of entities once and place the same
hierarchy in any number of scenes.

### How bundles work

A bundle is authored visually in the editor (or defined in script) and saved as a YAML
file. During export, the bundle is converted into a **factory function** registered with
`BundleManager`. At runtime, calling `createBundle` runs the factory and returns the
root entity of the new hierarchy.

Unlike simple duplication, bundles:

- Are a **single source of truth** — editing the bundle definition updates every scene
  that references it.
- Are **shared across scenes** — the same bundle can be instantiated in many scenes
  without duplicating authored data.
- **Can be created and destroyed at runtime** — useful for enemies, projectiles, UI
  cards, and any pooled or on-demand hierarchy.

### Creating a bundle in the editor

1. Build the entity hierarchy you want to reuse.
2. Select the root entity in the Structure panel.
3. Right-click and choose **Save as Bundle**.
4. Name the bundle and save to the `bundles/` folder.

### Using a bundle at runtime

Bundle **registration** is generated automatically by the export step (it emits a C++
`registerBundle` call that wires the factory to the bundle name/ID). At runtime you
mainly call `createBundle` and `destroyBundle`. Note that `createBundle` takes the bundle
**name first, then the scene**, and returns the root `Entity`.

=== "Lua"

    ```lua
    -- Create an instance (name first, then scene)
    local root = BundleManager.createBundle("enemy_grunt", scene)

    -- Destroy it later (scene first, then root entity)
    BundleManager.destroyBundle(scene, root)
    ```

=== "C++"

    ```cpp
    // Registration is normally emitted by export, e.g.:
    BundleManager::registerBundle(1, "enemy_grunt",
        [](Scene* scene, Entity parent) {
            // factory body
        });

    Entity root = BundleManager::createBundle("enemy_grunt", &scene);

    // Destroy when done
    BundleManager::destroyBundle(&scene, root);
    ```

See [BundleManager](../reference/classes/bundlemanager.md) for the full API reference.

## Next steps

- [Entity Component System](entity-component-system.md) — how data and behavior are
  organized under the hood.
- [Scripting](scripting.md) — add gameplay logic to entities.
- [Project Workflow](../editor/project-workflow.md) — how to manage scenes and bundles
  in the editor.
