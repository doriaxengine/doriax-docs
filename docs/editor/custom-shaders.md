---
description: Fork, edit, and customize the built-in shaders for Mesh, UI, Points, Lines, and Sky — per component or as scene-wide defaults — and add custom post-process passes, directly in the Doriax editor.
---

# Custom Shaders

Doriax ships built-in shaders for each renderable type (Mesh, UI, Points, Lines, Sky).
The editor lets you **fork** any of them into your project, edit the GLSL in the
[Code Editor](code-editor.md), and see the result in the viewport — without leaving the
editor. Forked shaders are compiled and shipped with your project just like the built-in
ones.

The same fork mechanism drives [post-process passes](#post-process-passes) — fullscreen
shaders a scene runs over the finished image.

## How customization works

A custom shader is a **fork** of a built-in shader. The editor copies the built-in
entry-point files (for example `mesh.vert` and `mesh.frag`) into a folder you pick in your
project; you edit the shading code while the rest of the rendering contract stays intact:

- The **variant system** is unchanged — the engine still injects the same feature
  defines (skinning, normal maps, shadows, IBL, fog, instancing, …) based on the mesh,
  so your edited shader keeps working across all of those cases.
- Skinned forks that `#include "includes/skinning.glsl"` bind bone matrices through a
  storage buffer, or through a bone texture when the editor compiles for OpenGL / OpenGL
  ES (`SKINNING_TEXTURE`). Re-fork that include if you copied an older `skinning.glsl`
  that still declared `mat4 bonesMatrix[MAX_BONES]` in a uniform block.
- The **depth, shadow, and G-buffer passes** keep using the built-in shaders, so shadow
  casting and screen-space effects continue to work.
- `#include` directives still resolve against the engine's shader library, so you only
  need the top-level `.vert`/`.frag` — not the whole include tree. If you want to edit the
  includes as well, the fork dialog can copy them for you (see [Includes](#includes)).

This means you customize the *surface/shading logic* while the engine continues to drive
lighting, passes, and built-in inputs.

## The Shader row

Open the **Properties** window for a Mesh, UI, Points, Lines, or Sky entity. Each of
these components has a **Shader** row:

| Control | Action |
| --- | --- |
| **Built-in** label | Shown when the component uses the default engine shader. |
| **Fork** | Opens the [Fork Shader dialog](#the-fork-shader-dialog) to choose where the fork is created and what it is called. On confirm it writes the files, assigns them to the component, and opens them in the Code Editor. |
| **Edit shader files** | Picks the `.vert` and `.frag` independently, so entry points that do not share a base name can be assigned. Changes apply as soon as both slots are set (or both cleared). |
| **Open vertex** / **Open fragment** | Re-opens the assigned file in the Code Editor. |
| **Reset to Built-in** | Clears the custom shader and returns to the engine default. |
| Drag-and-drop | Drop an existing `.vert`/`.frag` from the [Resources Browser](resources.md) onto the row to assign it. |

**Fork** is available only while the row shows **Built-in** — reset the shader first to
fork it again, so an existing fork is never orphaned by accident.

The Shader row is shown for a single selected entity (the path is per-entity). Assigning,
editing, or resetting a custom shader is undoable.

## The Fork Shader dialog

Forking asks where the new shader goes before writing anything:

| Field | Meaning |
| --- | --- |
| **Destination folder** | A tree of the folders in your project. Defaults to `shaders` when it exists, otherwise the project root. |
| **Shader Name** | The file name stem, without an extension. Letters, digits, and underscores only; other characters become `_` as you type. |
| **Also fork shader includes** | Copies the engine `.glsl` files this shader actually uses so you can edit them too. See [Includes](#includes). |
| **Will create** | The exact files that will be written, project-relative. |

The name is pre-filled from the entity (or the scene and shader type, for a scene default)
and gets a numeric suffix if that name is already taken. **Create** stays disabled while a
target already exists — forks never overwrite files, because undoing one deletes what it
wrote.

The layout depends on whether you fork the includes:

| Option | Files created |
| --- | --- |
| Off | `<folder>/<name>.vert` and `<folder>/<name>.frag` |
| On | `<folder>/<name>/` containing `<name>.vert`, `<name>.frag`, and an `includes/` copy |

Forking includes gives the shader a folder of its own so your edited copies apply to that
shader alone. Creating the fork is a single undoable step — undo removes the files it
wrote and restores the previous shader.

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

## Post-process passes

A scene can run an ordered chain of **fullscreen passes** over its finished image:
sharpen, tint, vignette, colour grading, and so on. Each pass is a forked shader, and
unlike the component shaders above the chain belongs to the scene, not to any entity.

Select the scene (no entity) in the **Structure panel** and open the **Post-processing**
section of the scene settings in the Properties window.

| Control | Action |
| --- | --- |
| **Add Pass** | Appends a pass. A new pass starts on the built-in passthrough, which copies the image unchanged. |
| Checkbox | Enables or disables the pass without removing it. |
| **↑** / **↓** | Moves the pass in the chain. Passes run top to bottom. |
| **🗑** | Removes the pass. |
| **Shader** row | The same controls as any other shader row — fork, pick files, open, reset, drag-and-drop. |

Every change is undoable, and the chain is saved with the scene.

The chain runs on the scene's **active camera**, after the opaque, transparent, UI, and
SSR passes, and before the fixed-resolution upscale. Secondary cameras — minimaps,
mirrors, portals — do not run it; if the active camera itself renders to a texture, the
chain writes into that texture. A scene drawn as a layer skips its chain, because a
fullscreen pass would overwrite the scene below it.

### Writing a pass

Forking a post-process pass copies `fullscreen.vert` and `postprocess.frag` into your
project. The vertex shader draws a fullscreen triangle and normally needs no edits — all
the work happens in the fragment shader.

A pass may declare any subset of the inputs below; only the ones it actually uses are
bound:

| Sampler | Contents |
| --- | --- |
| `u_sceneColorTexture` | The previous pass's output, or the scene colour for the first pass. |
| `u_depthTexture` | Camera-space packed depth. The engine runs a depth pre-pass for the chain when SSR and SSAO are both off, so this is always available. |
| `u_gbufferTexture` | View-space normal, roughness, and metallic. Only produced while **SSR** is enabled; reads black otherwise. |
| `u_ssaoTexture` | Blurred ambient occlusion. Reads white while SSAO is off. |

!!! warning "Depth orientation"
    Depth and the G-buffer keep the logical orientation of the depth pre-pass, so flip
    `v_texcoord.y` when sampling them on the OpenGL backends. The built-in `ssr.frag` shows
    the pattern.

### Pass uniforms

Declaring a `u_fs_postParams` block makes every member an editable row in the
**Post-processing** list — no extra declaration file, and no editor change needed:

```glsl
uniform u_fs_postParams {
    vec4 resolution;
    float amount;
    float threshold;
    vec4 tintColor;
} postParams;
```

Add a member, save the file, and a row appears for it. Values are stored **by name**, so
reordering members keeps them, and renaming or deleting one simply drops its saved value.
A member with no saved value is zero — GLSL uniform blocks have no initializers, so there
is no shader-side default to read.

Two names are **reserved** and written by the engine every frame instead of being edited.
They show in the list as *Set by the engine*:

| Name | Contents |
| --- | --- |
| `resolution` | `xy` = width and height of the pass target, `zw` = `1 / width` and `1 / height`. |
| `time` | Seconds elapsed since startup. |

Use `resolution` for anything that depends on target size — a texel offset written as a
literal breaks the moment the window resizes. Rename the uniform if you want to drive that
value yourself.

!!! warning "Do not mix int and float members"
    The OpenGL backends flatten a uniform block into a single upload typed after its first
    member, so a block holding both `int` and `float` members uploads incorrectly there.
    Keep one block to one scalar kind.

Members are edited as drag fields; matrix members are not editable and show no row.

### Export

Every pass ships its forked shader, including disabled ones — the generated scene carries
the whole chain, and the enable flag is a runtime value. A pass whose shader fails to
compile falls back to the passthrough, so the scene keeps rendering; the list marks it
**Shader failed to build** and the compiler output goes to the Output panel.

## Editing and live updates

Forked shaders open in the [Code Editor](code-editor.md) with GLSL syntax highlighting
(`.vert`, `.frag`, and `.glsl` files). When you **save** a shader source file, the editor
recompiles the affected forked shaders and refreshes the viewport — no rebuild or replay
needed.

Only shaders that actually reach the edited file through `#include` are rebuilt: the
editor tracks each fork's real dependency graph rather than assuming everything in a
folder is related. Editing a shader in an external editor works too — the change is picked
up when the Code Editor reloads the file.

!!! tip "Iterate fast"
    Keep the file open, tweak, **Ctrl+S**, and watch the viewport update.

## Includes

Shaders include by a fixed key — `#include "includes/pbr.glsl"` — and a fork resolves each
key in this order, taking the first that exists:

| Order | Location | Scope |
| --- | --- | --- |
| 1 | The fork's **own folder** | That fork only |
| 2 | The **project root** | Every fork in the project |
| 3 | The **engine shader library** | The default for everything |

A fork's folder mirrors the engine shader library, so a key keeps its shape:
`includes/pbr.glsl` is looked up at `<fork folder>/includes/pbr.glsl`.

- **Use an engine include** — `#include "includes/pbr.glsl"` resolves to the engine's copy
  automatically; you do not need to copy anything.
- **Override an include for one shader** — tick **Also fork shader includes** when you
  fork. The copies land in the fork's own folder and win for that shader alone.
- **Override an include for the whole project** — put the file at the same key under the
  project root, for example `<project>/includes/pbr.glsl`.
- **Add your own include** — drop a `.glsl` next to the fork and include it by its path
  relative to the fork folder (`#include "lib/noise.glsl"`), or put it anywhere in the
  project and include it relative to the project root
  (`#include "shaders/lib/noise.glsl"`).

Overrides never change the engine's built-in rendering — a built-in shader always uses the
engine library. A fork stored loose in a folder shares whatever `includes/` that folder
holds, which is why forking includes moves the shader into a folder of its own.

!!! note "Moving a fork"
    Nothing about the fork is recorded anywhere but its file paths, so you can move,
    rename, or copy it freely — including by hand — and its includes follow. Moving a fork
    into a folder with a different `includes/` changes what it resolves to, which is what
    makes overrides opt-in per location.

## Shader locations

Shaders have no directory settings. Sources live wherever you fork them — each fork
chooses its own location in the [Fork Shader dialog](#the-fork-shader-dialog) — and the
engine never reads them anyway. It only consumes compiled `.sdat`.

Compiled `.sdat` output goes to the project's `shaders` folder, the fixed location the
engine reads through `System::getShaderPath()`.

## Export and runtime

Forked shaders flow through the same export pipeline as the built-in ones (see
[Export Window — Shader compilation](export.md#shader-compilation)):

- Every used shader — including your forks — is compiled and embedded into the build for
  the target backends. The shader *sources* are not needed at runtime.
- To get loose `.sdat` or JSON files instead, use the
  [`shaders` CLI command](command-line.md#shaders-generate-shader-files-standalone), which
  writes them straight into its `--out` directory.

At runtime the engine identifies a component's shader (or a post-process pass's shader)
from the value saved on it and loads the matching compiled `.sdat` — it never reads the
source files. Because the engine only
cares about the compiled output, your shader sources can be organized however you like.

!!! note "Compiled vs. source location"
    The standalone runtime loads compiled shaders from the assets' `shaders` folder, and
    never reads shader sources. An export embeds them into the build instead, so it reads
    no shader directory at runtime.
