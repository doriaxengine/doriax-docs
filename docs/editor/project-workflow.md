---
description: Project organization, scene types, bundles, settings, and save/load behavior in the Doriax editor.
---

# Project Workflow

A Doriax project is the editable source for a game. It organizes scenes, resources,
scripts, bundles, and export configuration into a single directory that the editor
understands. The editor keeps visual authoring, code, and build settings clearly
separated so teams can iterate and collaborate effectively.

## Creating a project

Doriax does not display a startup dialog. When the editor launches, it reopens the
last saved project if that project is still available. Otherwise, it opens a temporary
project named `MyDoriaxProject` with a new 3D scene so you can begin editing
immediately. **File → New Project** also replaces the current project with a fresh
temporary project.

To keep a temporary project:

1. Choose **File → Save Project**.
2. Enter the project name, click **Browse**, and select an empty directory.
3. Click **Save**. The editor moves the temporary project into that directory and
   writes its `project.yaml` file.
4. Save the initial scene separately with **File → Save** or **Ctrl+S**, choosing a
   location inside the project directory.

Temporary projects are stored in the operating system's temporary directory. Save the
project to another directory before relying on it as permanent work.

New projects begin with a 3D scene. To add a different scene type, choose
**File → New Scene → 2D Scene** or **File → New Scene → UI Scene**. Doriax does not
use project templates.

## Project anatomy

| Area | Purpose |
| --- | --- |
| `assets/` (or `resources/`) | Textures, models, fonts, sounds, materials, and other imported files. The folder chosen as the [assets directory](#assets-and-lua-directories) is the root every asset reference is stored against |
| `scenes/` | YAML scene files edited by the visual editor |
| `scripts/` | Lua scripts and C++ source files |
| `shaders/` | Default location for forked shader sources (`.vert`/`.frag`/`.glsl`), and where compiled `.sdat` output goes — see [Custom Shaders](custom-shaders.md) |
| `bundles/` | Reusable entity hierarchy files |
| `settings/` | Scene startup references, build target settings, and export configuration |

Folder names may differ by project. The structure is a convention, not a strict
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
| **Project settings** | Startup scene reference, canvas size, scaling, VSync, window mode/size/title, compiler, parallel build jobs, and asset/Lua/shader directories |
| **Export settings** | Platform targets, shader backend, output folder, included asset folders |

Project settings include the **Shader Binaries Directory** (default `shaders`) for
compiled `.sdat` output. Shader *sources* have no setting — each fork picks its own
location when you create it. See [Custom Shaders](custom-shaders.md#project-settings).

### Assets and Lua directories

**Project → Project Settings → Directories** picks the two folders the running game reads
from. Both default to `<Project root>`, which keeps the whole project as the root.

| Setting | Root for | Resolved at runtime through |
| --- | --- | --- |
| **Assets Directory** | Textures, models, sounds, fonts | `asset://`, and every plain relative path |
| **Lua Directory** | Lua script entries and the data files they read | `lua://` |

References are stored **relative to these roots**, not to the project. With the assets
directory set to `assets`, a texture in `assets/textures/hero.png` is stored as
`textures/hero.png`, which is exactly what the exported game finds next to its executable.

Changing either directory migrates the project in one step:

- referenced files that would fall outside the new root are **moved into it**, keeping
  their folder layout so a model still finds its `.bin` and textures;
- every reference is rewritten in scenes, bundles and `.material` files — scenes that are
  not open are loaded for the rewrite and closed again;
- if any file cannot be moved, every move is undone and the directories are left
  unchanged, so the project is never half-migrated.

Because a reference cannot leave its root, the editor only accepts assets from inside the
assets directory: dropping a file from elsewhere previews it but shows a warning instead of
assigning it. Maps painted in the Terrain editor and assets downloaded by the AI assistant
are created under the assets root for the same reason. Moving a referenced file out of the
assets directory clears the references to it, exactly like deleting it.

### VSync

Open **Project → Project Settings** and use **VSync** to choose whether Play mode and
supported desktop builds synchronize frames to the display refresh rate. It is enabled
by default. Disable it when profiling the maximum frame rate; leave it enabled for
normal use to avoid tearing and unnecessary GPU load.

The value is saved as `vsync` in `project.yaml` and travels with the project. Older
projects without the field default to enabled.

| Runtime path | VSync off behavior |
| --- | --- |
| Editor Play mode | Uncaps the editor render loop while a scene is running; normal editing remains synchronized |
| Generated standalone GLFW build | Uses swap interval `0` |
| Exported Linux GLFW, Windows/Linux Sokol OpenGL, or Windows Direct3D 11 build | Uses swap interval `0` |
| Exported Vulkan build | Prefers Immediate presentation, then Mailbox; falls back to FIFO if neither is supported by the system |
| Exported macOS Metal build | Remains synchronized; the generated CMake project prints a warning |

!!! note "Platform control"
    A graphics driver, compositor, or window system may still impose presentation
    limits after VSync is disabled. Compare a standalone build when collecting final
    performance numbers because the editor adds its own rendering overhead.

### Window

Open **Project → Project Settings** to control the OS window that desktop builds
create at startup:

| Setting | Default | Effect |
| --- | --- | --- |
| **Window Mode** | Windowed | Initial window state: `Windowed`, `Maximized`, or `Fullscreen` |
| **Window Width / Height** | Canvas size | Initial window size in pixels, and the size restored when leaving fullscreen |
| **Window Resizable** | Enabled | Whether the player can resize the window |
| **Window Title** | Project name | Title-bar text; leave empty to use the project name |

The values are saved as `windowMode`, `windowWidth`, `windowHeight`,
`windowResizable`, and `windowTitle` in `project.yaml` and travel with the project.
Projects saved before these fields existed start windowed at their canvas size.

`Fullscreen` starts the game on the primary monitor at the current desktop video mode
(borderless-style, no display mode switch) and falls back to windowed when no monitor
is available. Scripts can still toggle fullscreen at runtime with
[`requestFullscreen` / `exitFullscreen`](../reference/classes/system.md#isfullscreen-requestfullscreen-exitfullscreen);
leaving fullscreen restores the configured window size.

| Runtime path | Behavior |
| --- | --- |
| Editor Play mode | Not affected — Play renders inside the editor viewport |
| Generated standalone GLFW build | All settings honored |
| Exported Linux GLFW build | All settings honored |
| Exported Windows/macOS Sokol build | Size, title, and fullscreen honored; `Maximized` falls back to windowed and the window is always resizable |
| Exported macOS Xcode (apple backend) build | Uses the storyboard-defined window; project window settings are not applied |
| Web, Android, iOS | Ignored — the game always fills the browser canvas or the device screen |

## Save strategy

- Save scenes after structural edits (**Ctrl+S**).
- Save project settings after changing export configuration.
- Keep generated export output outside the source project folder.
- Commit human-authored files (scenes, scripts, assets) to version control;
  ignore local build folders and generated C++ glue.
