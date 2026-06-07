---
description: A tour of the Doriax editor — scene editing, inspector, animation, code editor, and play mode.
---

# The Editor

Doriax ships with a complete visual editor built for creators. Design scenes, write
code, animate characters, and test your game — all from one unified environment.

![Doriax Engine editor — 3D scene](../assets/screenshots/editor-3d-scene.png)

## Core panels

| Panel | Purpose |
| --- | --- |
| Scene view | Viewport for editing 2D and 3D scenes with gizmos and cameras |
| Scene hierarchy | The tree of entities in the current scene |
| Inspector | View and edit the components and properties of the selected entity |
| Resources | Manage textures, models, audio, and other project assets |
| Code editor | Integrated editor for Lua and C++ scripts |

## 3D scenes

Edit 3D scenes with cameras, lighting, models, and play mode. Position entities with
gizmos, set up PBR materials, and preview shadows, fog, and the sky system directly in
the viewport.

## 2D &amp; tilemaps

![2D tilemap editor](../assets/screenshots/editor-2d-tilemap.png)

Build 2D scenes with sprites and tilemaps. The **sprite slicer** and **tileset slicer**
tools let you cut sprite sheets and tilesets into usable frames and tiles.

## Animation

![Animation timeline](../assets/screenshots/editor-animation.png)

Animate characters and objects with the timeline editor, and work with skeletons using
the bone tools for skeletal animation.

## Code editor

![Integrated code editor](../assets/screenshots/editor-code.png)

Write Lua and C++ scripts in the integrated code editor without leaving the
environment. Lua iterates quickly at runtime, while C++ is compiled at build time for
native performance.

## Play mode

Press **Play** to run your game inside the editor. Test gameplay, UI overlays, and
physics interactively, then return to editing.

## Export pipeline

The editor includes a shader-aware export pipeline that prepares scenes, assets,
scripts, engine files, and compiled shaders for your target platform. See
[Building](../building/overview.md) for platform-specific output.

!!! note "Editor coverage"
    Terrain authoring, particle editing, audio tooling, and direct shader manipulation
    are not fully integrated into the editor yet — these features are currently
    available at the engine/runtime level.
