---
description: Project organization, scene types, bundles, settings, and save/load behavior in the Doriax editor.
---

# Project Workflow

A Doriax project is the editable source for a game. It organizes scenes, resources,
scripts, bundles, and export configuration into a single directory that the editor
understands. The editor keeps visual authoring, code, and build settings clearly
separated so teams can iterate and collaborate effectively.

## Creating a project

Launch the editor and choose **New Project** from the startup dialog. Select a project
template (empty, 2D, 3D, or UI) and pick an empty folder. The editor creates the
initial folder structure and a default scene file.

## Project anatomy

| Area | Purpose |
| --- | --- |
| `assets/` (or `resources/`) | Textures, models, fonts, sounds, materials, and other imported files |
| `scenes/` | YAML scene files edited by the visual editor |
| `scripts/` | Lua scripts and C++ source files |
| `bundles/` | Reusable entity hierarchy files |
| `settings/` | Scene startup references, build target settings, and export configuration |

Folder names may differ by template. The structure is a convention, not a strict
requirement — you can reorganize asset folders and update resource paths accordingly.

## Scene files

Scene files are serialized as YAML. They store the full scene hierarchy: entities,
component data, transform values, camera settings, child scene references, and editor
viewport state.

Keep scene files focused. For large games, split gameplay areas into separate scenes
and compose them with child scene references. This keeps individual YAML files small
and merge-friendly in version control.

## Scene types

The editor offers three scene workflows:

| Type | Editor defaults | Typical content |
| --- | --- | --- |
| **3D** | Perspective editor camera, 3D gizmos, lighting panel | Models, lights, camera, terrain, physics bodies |
| **2D** | Orthographic camera, 2D canvas gizmos | Sprites, tilemaps, polygon shapes, 2D physics |
| **UI** | Screen-space canvas, anchor gizmos | Buttons, text, images, panels, scrollbars |

All three share the same `Scene` class at runtime — the type mainly affects editor
defaults and authoring tools. A 3D scene can contain UI entities, and a UI scene can
reference 2D or 3D child scenes.

## Child scenes

Child scenes let one scene reference and load another. This is useful for:

- **Persistent UI layers** — load a HUD scene as a child of the gameplay scene.
- **Shared environment** — a common lighting rig or skybox loaded by all levels.
- **Level assembly** — large worlds assembled from smaller room or chunk scenes.
- **Streaming** — load and unload sections independently at runtime.

To add a child scene reference, use the Structure panel's **Add Child Scene** option and
point it to a saved scene file.

## Bundles

**Bundles** are prefab-like reusable entity hierarchies. A bundle can represent an
enemy, an interactive prop, a UI card, or any repeated arrangement of entities and
components. They are defined visually in the editor and stored as YAML bundle files.

### Why bundles?

| Advantage | Detail |
| --- | --- |
| **Shared across scenes** | The same bundle can be placed in any number of scenes without duplicating data |
| **Single source of truth** | Changing a bundle updates every instance in every scene that references it |
| **Runtime factory** | During export, bundles become factory functions; `BundleManager` creates and destroys instances at runtime |
| **No coupling** | Bundles are independent of the scenes that use them — they can be loaded on demand |

### Creating a bundle

1. Build the entity hierarchy you want to reuse in any scene.
2. Select the root entity in the Structure panel.
3. Choose **Save as Bundle** from the context menu.
4. Name the bundle and save to the `bundles/` folder.

### Placing bundles

Drag a bundle file from the Resources Browser into the scene, or reference it in the
Structure panel with **Add Bundle Instance**.

### Runtime bundle usage

Bundle registration is generated automatically by the export step. At runtime you call
`createBundle` (bundle **name first, then scene**) and `destroyBundle`:

=== "Lua"

    ```lua
    -- Create a bundle instance at runtime
    local root = BundleManager.createBundle("enemy_grunt", scene)

    -- Destroy it later
    BundleManager.destroyBundle(scene, root)
    ```

=== "C++"

    ```cpp
    // Registration is normally emitted by export:
    BundleManager::registerBundle(1, "enemy_grunt", [](Scene* scene, Entity parent) {
        // bundle factory body
    });

    // Create an instance
    Entity root = BundleManager::createBundle("enemy_grunt", &scene);
    ```

See [BundleManager](../reference/classes/bundlemanager.md) for the complete API.

## Settings

| Settings area | What it stores |
| --- | --- |
| **Editor settings** | Window size, maximized state, recent projects, Resources Browser preferences |
| **Project settings** | Startup scene reference, canvas size, export targets |
| **Export settings** | Platform targets, shader backend, output folder, included asset folders |

## Save strategy

- Save scenes after structural edits (**Ctrl+S**).
- Save project settings after changing export configuration.
- Keep generated export output outside the source project folder.
- Commit human-authored files (scenes, scripts, assets) to version control;
  ignore local build folders and generated C++ glue.
