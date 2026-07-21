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

See [Switching scenes with SceneManager](#switching-scenes-with-scenemanager) for full
scene transitions and on-demand overlays at runtime.

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
| Shadow quality | PCF filtering level for smoother shadow edges (`NONE` to `HIGH`) |
| Light state | `OFF`, `ON`, or `AUTO` (auto-detects lights in the scene) |
| Global illumination | Ambient light color and intensity |
| Ambient occlusion (SSAO) | Screen-space ambient occlusion — enable plus radius, intensity, and bias — see [Rendering Pipeline](rendering-pipeline.md#ambient-occlusion-ssao) |
| Reflections (SSR) | Screen-space reflections — enable plus distance, thickness, intensity, and glossy blur — see [Rendering Pipeline](rendering-pipeline.md#screen-space-reflections-ssr) |
| Ambient light (2D) | Flat ambient color and intensity for 2D scenes, with its own 2D shadow quality — see [2D lighting](2d-graphics.md#2d-lighting) |
| Physics gravity | Per-world gravity in m/s² — 2D (Box2D) and 3D (Jolt) are independent — see [Physics](physics.md#gravity) |
| Fixed resolution | Render the main scene at a fixed internal size and upscale it to the window — see [Multiple Resolutions](multiple-resolutions.md#fixed-resolution) |
| UI events | Enables/disables UI input processing for the scene |
| Default shaders | Per-type custom shaders (Mesh, UI, Sky, Points, Lines) used by every component of that type without its own custom shader — see [Custom Shaders](../editor/custom-shaders.md#scene-default-shaders) |
| Canvas size | Logical resolution for 2D and UI scenes |

Edit these in the editor by selecting the scene root in the [Structure panel](../editor/structure.md)
with no entity selected; the settings appear in the [Properties window](../editor/properties.md).
Which sections are shown depends on the scene type — 2D and UI scenes hide 3D-only options such
as SSAO and SSR. As with component fields, any setting changed from its default shows a small
**reset arrow** next to its label that restores the default, and every change is saved with the
scene and undoable.

## Scene stacks

When the engine runs, every loaded scene lives in an ordered list of **layers**, and a
group of scenes that are loaded together is called a **scene stack**:

- The **main scene** is always the bottom layer. There is exactly one per stack.
- Each additional scene is a **layer** drawn on top of the layers before it.
- The **last** layer is the topmost — it renders over everything below it.

In the editor, each scene file is the main scene of its own stack, and you attach other
scenes to it as **child scenes**. At export, the editor turns each stack into a factory
that calls `Engine::setScene()` for the main scene and `Engine::addSceneLayer()` for each
child, then registers it with `SceneManager`.

## Child scenes

A **child scene** reference lets one scene load and run another as part of the same stack.
Child scenes share the same engine tick but keep their own entity and component storage,
so they stay cleanly separated. Use them for:

- **Persistent UI** — a HUD or menu scene that stays loaded across gameplay level changes.
- **Shared setup** — a single lighting and skybox scene included in every level.
- **Additive worlds** — large open worlds assembled from independently-authored chunks.
- **Scene streaming** — load and unload sections without a full scene transition.
- **Pop-ups and pause menus** — UI that appears on demand and is removed without
  reloading the level.

### Adding a child scene in the editor

Select the parent scene in the [Structure panel](../editor/structure.md) and either:

- right-click the scene root and choose **Add child scene → _SceneName_**, or
- drag a `.scene` file from the [Resources Browser](../editor/resources.md) onto the
  scene root.

Child scenes are listed **above** the parent's entities. Click the eye icon next to a
child scene to load it *inline*, so you can see and edit its entities in context — this
is an editor convenience and does not change runtime behavior.

### Start active

Each child scene reference has a **Start active** flag (right-click the child scene node →
**Start active**). It controls whether the child scene is added to the engine
automatically when its parent loads:

| Start active | Behavior when the parent loads | Use it for |
| --- | --- | --- |
| **On** (default) | The child scene is created **and** added as a layer. It runs and renders immediately. | HUDs, persistent overlays, shared lighting — anything always present. |
| **Off** | The child scene is still created and prepared (its entities, scripts, and `Scene*` are all ready), but it is **not** added to the engine. | Pause menus, dialogs, level sections — anything you reveal later. |

A child scene that starts inactive is *ready but hidden*. Because it is already built,
showing it later with [`SceneManager.addChildScene`](#switching-scenes-with-scenemanager)
is instant — there is no loading cost at the moment it appears.

### Scene order

The order of the layers follows the order the child scenes are listed under their parent
in the Structure panel, which is the order you added them. The main scene stays at the
bottom; each child scene draws on top of the ones above it in the list. **Put a HUD or
menu scene last so it renders over the gameplay below it.**

To change the order, remove the child scenes and add them back in the sequence you want —
the one added last ends up on top. At runtime, `SceneManager.addChildScene` always adds a
scene **on top** of the current layers, so re-adding is also how you bring a layer to the
front.

## Switching scenes with SceneManager

[`SceneManager`](../reference/classes/scenemanager.md) is the runtime entry point for
moving between scenes. The editor registers every scene stack for you at startup, so from
a script you refer to scenes by their **name** (or numeric ID) and never touch the
factory functions directly. There are two ways to change what is on screen.

### Migrate to another scene

`SceneManager.loadScene` performs a full **transition**: it removes every currently loaded
scene (`Engine::removeAllScenes()` — main *and* all layers), then builds the requested
stack from scratch and runs it. Use it to move between levels, menus, and game-over
screens.

=== "Lua"

    ```lua
    -- Leave the current scene entirely and load another
    SceneManager.loadScene("Level2")

    -- Or by registration ID
    SceneManager.loadScene(2)
    ```

=== "C++"

    ```cpp
    SceneManager::loadScene("Level2");
    SceneManager::loadScene(2);
    ```

!!! warning "One stack at a time"
    `loadScene` clears everything first, so you do **not** call it once per layer. Attach
    persistent layers (a HUD, shared lighting) as **start-active child scenes** of the
    target scene instead — they come up with it in a single `loadScene` call.

### Overlay a scene without leaving the current one

`SceneManager.addChildScene` and `removeChildScene` add or remove a scene **on top** of
what is already running, with no transition. This is how you show a pause menu, dialog, or
HUD toggle over live gameplay. They operate on scenes that are part of the loaded stack —
typically a child scene you marked **Start active → Off** so it is prepared but hidden.

=== "Lua"

    ```lua
    -- Open a pause menu over the running game
    function onPause()
        if SceneManager.addChildScene("PauseMenu") then
            Engine.pauseGameEvents(true)   -- freeze gameplay updates
        end
    end

    -- "Resume" button handler inside the PauseMenu scene
    resumeBtn = Button(scene)
    resumeBtn.label = "Resume"
    local btnComp = resumeBtn:getButtonComponent()
    btnComp.onPress = function()
        SceneManager.removeChildScene("PauseMenu")
        Engine.pauseGameEvents(false)
    end
    ```

=== "C++"

    ```cpp
    // Open a pause menu over the running game
    if (SceneManager::addChildScene("PauseMenu")) {
        Engine::pauseGameEvents(true);
    }

    // "Resume" button handler inside the PauseMenu scene
    resumeBtn.getComponent<ButtonComponent>().onPress = []() {
        SceneManager::removeChildScene("PauseMenu");
        Engine::pauseGameEvents(false);
    };
    ```

Because `addChildScene` puts the scene at the top of the layer list, the overlay always
draws above the gameplay below it. `removeChildScene` takes it back out and leaves the
main scene and other layers untouched.

### Knowing where you are

`SceneManager` also reports the current state, which is handy for transition logic and
save systems:

| Query | Returns |
| --- | --- |
| `SceneManager.getCurrentSceneName()` | Name of the most recently loaded scene |
| `SceneManager.getCurrentSceneId()` | ID of the most recently loaded scene |
| `SceneManager.getSceneNames()` | All registered scene names |
| `SceneManager.getSceneId(name)` | Numeric ID for a name (`0` if unknown) |

See the [SceneManager reference](../reference/classes/scenemanager.md) for the complete
API.

## Creating UIs as scenes

User interfaces fit the child-scene model naturally. The recommended pattern is to author
each interface — HUD, main menu, pause menu, settings — as its own **UI scene**, then
bring it on screen as a layer:

1. Create a [**UI scene**](user-interface.md) and add widgets to it
   ([`Panel`](../reference/classes/panel.md), [`Button`](../reference/classes/button.md),
   [`Text`](../reference/classes/text.md), and so on).
2. Add it as a **child scene** of the gameplay scene it belongs to.
3. Choose its [**Start active**](#start-active) flag:
    - **On** for a permanent HUD that should appear with the level.
    - **Off** for a menu or dialog you open later with `SceneManager.addChildScene`.
4. Keep the UI scene **last** in the child list so its widgets draw above the game.

Because a UI scene is screen-space and self-contained, you can swap menus without touching
gameplay data and load or unload interfaces independently. For widget construction,
anchoring, events, and canvas scaling, see the [User Interface](user-interface.md) manual
and the [First UI Scene](../tutorials/first-ui-scene.md) tutorial.

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

!!! note "There is no direct `.bundle` file loader"
    You don't load a `.bundle` file by path at runtime. Export turns each file into a
    registered factory, and you spawn it by the **bundle name** — the file's path with the
    `.bundle` extension removed and forward slashes (so `bundles/enemies/EnemyShip.bundle`
    is created as `"enemies/EnemyShip"`). Use `BundleManager.getBundleNames()` to list
    everything that is registered.

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
