---
description: Overview of the Doriax editor — panels, workflows, play mode, and navigation.
---

# Editor Overview

The Doriax editor is the primary authoring environment for your projects. It brings
together scene editing, resource management, scripting, animation, play mode, and
export tooling in one unified window so you can build, test, and ship games without
leaving the editor.

![Doriax Engine editor - 3D scene](../assets/screenshots/editor-3d-scene.png)

## Editor layout

The editor window is divided into a set of resizable panels:

| Panel | Purpose |
| --- | --- |
| **Menu bar** | File, project, scene, and play-mode controls |
| **Scene view** | Main viewport for 2D, 3D, and UI scene editing with gizmos |
| **Structure panel** | Hierarchical tree of scenes and entities |
| **Properties window** | Component list and property fields for the selected entity |
| **Resources Browser** | Project asset manager: import, preview, and organize files |
| **Animation Timeline** | Keyframe editor for object animation, sprite frames, and bones |
| **Code Editor** | Integrated Lua and C++ editor with API completion |
| **Output panel** | Build logs, play-mode diagnostics, and export messages, persisted to [`editor.log`](../about/faq.md#where-can-i-find-the-editor-crash-log) for crash reports |

## Main workflows

| Task | Where it happens |
| --- | --- |
| Create and configure scenes | Project Workflow, Structure panel, scene save dialog |
| Place and transform entities | Scene view gizmos |
| Edit component data | Properties window |
| Import and preview assets | Resources Browser |
| Share PBR materials across meshes | Create `.material` files (Properties → Resources drag), link from Scene view |
| Slice sprite sheets and tilesets | Sprite Slicer, Tileset Slicer |
| Write Lua or C++ scripts | Code Editor and script creation dialog |
| Animate objects and characters | Animation Timeline |
| Test gameplay | Play / Pause / Stop controls |
| Prepare builds | Export Window |

## Scene types

The editor supports three scene workflows:

| Type | Purpose |
| --- | --- |
| **3D scene** | Games with perspective cameras, 3D models, PBR materials, sky/IBL, and lighting |
| **2D scene** | Top-down or side-scrolling games with sprites and tilemaps |
| **UI scene** | Menus, HUDs, overlays, and screen-space controls using the UI system |

All three types share the same ECS foundation, camera, and scripting system. A project
can load multiple scene types simultaneously — for example, a 3D gameplay scene with a
UI scene overlay.

## Play mode

Press **Play** to run the game inside the editor. The editor takes a snapshot of the
current scene state before entering play mode and restores it when you stop, so runtime
mutations do not permanently corrupt your authored data.

Use play mode for quick iteration. For platform-specific validation (mobile input,
web memory limits, native graphics), test with a proper exported build.

## Undo and redo

All edits made in the scene view, Properties window, and hierarchy are recorded in the
command history. Use **Ctrl+Z** / **Ctrl+Y** to step back and forward through changes.
Undo is available across transforms, component edits, hierarchy reparenting, resource
assignments, and cascade deletes (a parent and its children restore together).

## Keyboard shortcuts

| Shortcut | Action |
| --- | --- |
| **Ctrl+Z** | Undo |
| **Ctrl+Y** | Redo |
| **Ctrl+S** | Save current scene |
| **Delete** | Delete selected entity |
| **W** | Translate gizmo |
| **E** | Rotate gizmo |
| **R** | Scale gizmo |
| **F** | Focus viewport on selection |
| **Space** | Play / Stop |

## Detailed pages

- [Project Workflow](project-workflow.md)
- [Structure Panel](structure.md)
- [Scene View](scene-view.md)
- [Properties & Components](properties.md)
- [Resources Browser](resources.md)
- [Sprite Slicer](sprite-slicer.md)
- [Tileset Slicer](tileset-slicer.md)
- [Animation Timeline](animation.md)
- [Code Editor](code-editor.md)
- [Export Window](export.md)
- [Command-Line Tools](command-line.md)
