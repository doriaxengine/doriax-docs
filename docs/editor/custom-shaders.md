---
description: Fork, edit, and customize the built-in shaders for Mesh, UI, Points, Lines, and Sky — per component or as scene-wide defaults — directly in the Doriax editor.
---

# Custom Shaders

Doriax ships built-in shaders for each renderable type (Mesh, UI, Points, Lines, Sky).
The editor lets you **fork** any of them into your project, edit the GLSL in the
[Code Editor](code-editor.md), and see the result in the viewport — without leaving the
editor. Forked shaders are compiled and shipped with your project just like the built-in
ones.

## How customization works

A custom shader is a **fork** of a built-in shader. The editor copies the built-in
entry-point files (for example `mesh.vert` and `mesh.frag`) into your project's shader
sources folder; you edit the shading code while the rest of the rendering contract stays
intact:

- The **variant system** is unchanged — the engine still injects the same feature
  defines (skinning, normal maps, shadows, IBL, fog, instancing, …) based on the mesh,
  so your edited shader keeps working across all of those cases.
- The **depth, shadow, and G-buffer passes** keep using the built-in shaders, so shadow
  casting and screen-space effects continue to work.
- `#include` directives still resolve against the engine's shader library, so you only
  need the top-level `.vert`/`.frag` — not the whole include tree.

This means you customize the *surface/shading logic* while the engine continues to drive
lighting, passes, and built-in inputs.

## The Shader row

Open the **Properties** window for a Mesh, UI, Points, Lines, or Sky entity. Each of
these components has a **Shader** row:

| Control | Action |
| --- | --- |
| **Built-in** label | Shown when the component uses the default engine shader. |
| **Customize** | Forks the built-in shader into your project's shader sources folder, assigns it to the component, and opens the new `.vert` and `.frag` in the Code Editor. |
| **Edit** | Re-opens the assigned shader's `.vert` and `.frag` in the Code Editor. |
| **Reset to Built-in** | Clears the custom shader and returns to the engine default. |
| Drag-and-drop | Drop an existing `.vert`/`.frag` from the [Resources Browser](resources.md) onto the row to assign it. |

The Shader row is shown for a single selected entity (the path is per-entity). Assigning,
editing, or resetting a custom shader is undoable.

## Scene default shaders

Besides per-component shaders, each scene can set a **default custom shader per type**.
Select the scene (no entity) in the **Structure panel** and look for the **Default
Shaders** section at the bottom of the scene settings in the Properties window. It shows
one row per applicable type — 3D scenes list Mesh, Sky, UI, Points, and Lines; 2D scenes
omit Sky; UI scenes list only UI.

Each row offers the same controls as the component Shader row (fork, edit files, open
`.vert`/`.frag`, reset, drag-and-drop), and every change is undoable.

The shader used by a component is resolved with this priority:

1. **Component shader** — a custom shader assigned on the component always wins.
2. **Scene default shader** — used by every component of that type whose Shader row
   still shows **Built-in**.
3. **Engine built-in** — used when neither is set.

A component with no custom shader *inherits* the scene default; resetting a component's
shader returns it to the scene default (or the built-in if the scene has none). To keep a
single component on stock shading while a scene default is active, fork the built-in
shader for that component and leave it unedited.

Scene default shaders are saved with the scene, applied in play mode, and exported like
any other custom shader — components that inherit them compile and ship the right shader
variants automatically. They are also scriptable via the `Scene` properties
`defaultMeshShader`, `defaultUIShader`, `defaultSkyShader`, `defaultPointsShader`, and
`defaultLinesShader` (see the [Scene reference](../reference/classes/scene.md)).

## Editing and live updates

Forked shaders open in the [Code Editor](code-editor.md) with GLSL syntax highlighting
(`.vert`, `.frag`, and `.glsl` files). When you **save** a shader source file, the editor
recompiles the affected forked shaders and refreshes the viewport — no rebuild or replay
needed.

!!! tip "Iterate fast"
    Saving a `.vert`, `.frag`, or `.glsl` file under the shader sources folder triggers a
    recompile of every forked shader. Keep the file open, tweak, **Ctrl+S**, and watch the
    viewport update.

## Includes

Your project's shader sources folder mirrors the engine shader library, so any `.glsl`
file there is includable from a fork by its path relative to that folder:

- **Use an engine include** — `#include "includes/pbr.glsl"` resolves to the engine's
  copy automatically; you do not need to copy it.
- **Override an engine include** — place a file at the same relative path (for example
  `includes/pbr.glsl`) inside your shader sources folder. Your project's forked shaders
  use your copy; built-in shaders keep the engine's.
- **Add your own include** — drop a new `.glsl` anywhere under the sources folder (for
  example `lib/noise.glsl`) and `#include "lib/noise.glsl"` from a fork.

Include overrides apply only to your forked shaders — they never change the engine's
built-in rendering. Editing any `.glsl` under the sources folder rebuilds the forks that
might use it.

## Project settings

Two directories are configurable in **Project Settings** (both default to `shaders`):

| Setting | Role |
| --- | --- |
| **Shaders Directory** | Where compiled `.sdat` shaders are written/loaded. This is the engine/build-facing location. |
| **Shader Sources Directory** | Where forked shader sources (`.vert`/`.frag`/`.glsl`) live. **Editor-only** — the engine never reads it; it only consumes compiled `.sdat`. |

Keeping them separate lets the source files (which you edit) live alongside — or apart
from — the compiled output the runtime loads.

## Export and runtime

Forked shaders flow through the same export pipeline as the built-in ones (see
[Export Window — Shader compilation](export.md#shader-compilation)):

- With the default **Header** output, every used shader — including your forks — is
  compiled and embedded into the build for the target backends. The shader *sources* are
  not needed at runtime.
- With **`.sdat`/JSON** output, the compiled files are written to the project's **Shaders
  Directory** and loaded at runtime.

At runtime the engine identifies a component's shader from the value saved on it and loads
the matching compiled `.sdat` — it never reads the source files. Because the engine only
cares about the compiled output, your shader sources can be organized however you like.

!!! note "Compiled vs. source location"
    The standalone runtime loads compiled shaders from the assets' `shaders` folder. For a
    loose `.sdat` export, keep the **Shaders Directory** at `shaders` so the runtime finds
    them. The default **Header** export embeds shaders into the build and does not read a
    shader directory at runtime.
