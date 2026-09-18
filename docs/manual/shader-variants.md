---
description: How Doriax keys shader variants, where a project's set is collected, and what to do when an exported build is missing one.
---

# Shader Variants

The engine does not ship a single mesh shader. It compiles one **variant** per feature
combination a scene actually uses — lit or unlit, with or without normals, tangents,
skinning, vertex colors, shadows, instancing — and each variant is a separate compiled
program. A build carries only the variants it was told to compile, so the set has to be
known before the export runs.

## How a variant is identified

A variant is a **shader type** plus a **property mask**. `mesh:Uv1,Puc,Shw,Nor,Tan,Aop`
is the lit, textured, shadowed, opaque mesh shader with tangents; `depth:Ski` is the
skinned depth pass that feeds shadow maps. That spelling is what
[`--shader`](../editor/command-line.md#shader-specs) accepts and what the
[Export Window](../editor/export.md#common-settings) **Shaders** list shows.

A [custom shader](../editor/custom-shaders.md) adds a third dimension: the fork is
compiled per property combination as well, alongside the built-in variant it falls back
to when the fork fails to build.

## Where the set comes from

Each scene keeps its own list in the `shaderKeys` field of its `.scene` file. The editor
refreshes that list when it saves the scene, by walking the renderable components and
reading the variant each one resolved to.

The catch is that a component reports its variant only once **RenderSystem has loaded
it**, and loading needs a live graphics context. The refresh therefore only sees what the
editor has actually drawn. Two consequences:

- Saving **merges** into the stored list instead of replacing it, so a component that has
  not been rendered yet does not lose its variant from the file. Entries accumulate and
  are never pruned automatically — drop stale ones in the Export Window's **Shaders**
  list.
- A headless [`doriax-editor export`](../editor/command-line.md#export-build-a-project-to-a-target)
  has no renderer, so it discovers nothing and exports exactly what the `.scene` files
  already carry.

Opening the project in the editor and playing each scene once is what fills the list in.

## Property reference

A property name is a three-letter abbreviation of the feature it switches on, and its
position in the list below is the bit it occupies in the numeric mask. Both spellings
are accepted by `--shader` (`mesh:Uv1,Nor` and `mesh:0x42` are the same variant), and
the numeric form is what a scene file's `shaderKeys` entries hold.

### `mesh`

| Bit | Name | Feature |
| --- | --- | --- |
| 0 | `Ult` | Unlit material |
| 1 | `Uv1` | Primary UV set |
| 2 | `Uv2` | Secondary UV set |
| 3 | `Puc` | Punctual lights |
| 4 | `Shw` | Shadow maps |
| 6 | `Nor` | Vertex normals |
| 7 | `Nmp` | Normal map |
| 8 | `Tan` | Vertex tangents |
| 9 | `Vc3` | Vertex color, RGB |
| 10 | `Vc4` | Vertex color, RGBA |
| 11 | `Txr` | Texture rect |
| 12 | `Fog` | Fog |
| 13 | `Ski` | Skinning |
| 14 | `Mta` | Morph targets |
| 15 | `Mnr` | Morph normals |
| 16 | `Mtg` | Morph tangents |
| 17 | `Ter` | Terrain |
| 18 | `Ist` | Instancing |
| 19 | `Ibl` | Image-based lighting |
| 20 | `Mir` | Mirror |
| 21 | `Sao` | SSAO |
| 22 | `L2d` | 2D lights |
| 23 | `S2d` | 2D shadows |
| 24 | `Ams` | Alpha mask |
| 25 | `Aop` | Alpha opaque |
| 26 | `Ifd` | Instance distance fade |
| 27 | `Tpb` | Terrain PBR layers |

Bit 5 is reserved: it used to select the PCF shadow filter, which is uniform-driven now
(Scene shadow quality).

### `depth`

| Bit | Name | Feature |
| --- | --- | --- |
| 0 | `Tex` | Texture (alpha-masked shadow casters) |
| 1 | `Ski` | Skinning |
| 2 | `Mta` | Morph targets |
| 3 | `Mnr` | Morph normals |
| 4 | `Mtg` | Morph tangents |
| 5 | `Ter` | Terrain |
| 6 | `Ist` | Instancing |
| 7 | `Ams` | Alpha mask |
| 8 | `Ifd` | Instance distance fade |

### `ui`, `points`, `lines`

| Type | Bit 0 | Bit 1 | Bit 2 | Bit 3 |
| --- | --- | --- | --- | --- |
| `ui` | `Tex` texture | `Ftx` font texture | `Vc3` | `Vc4` |
| `points` | `Tex` texture | `Vc3` | `Vc4` | `Txr` texture rect |
| `lines` | `Vc3` | `Vc4` | - | - |

`sky`, `blit`, `ssao`, `ssaoblur`, `ssr`, `ssrblur`, `composite`, `shadow2d` and
`postprocess` have no properties; name the type on its own.

### Combinations that are easy to miss

Several properties come from the scene or the frame rather than from the model, so a
variant list assembled by hand tends to be short by a factor of two or four:

- **`Sao`** is set on every lit mesh in a scene with SSAO enabled, terrain and water
  included.
- **`Ibl`** is off until the sky's environment maps finish generating, so the same mesh
  needs the variant both with and without it - the first frames are drawn before they
  exist.
- **`Ifd`** is a separate program from `Ist`, and terrain foliage chunks always set both.
- **`Vc4`** turns on for any model whose glTF carries `COLOR_0`, which many scanned
  assets do without it being obvious.
- **`Uv1`** needs a texture, not just UVs: a generated mesh with texture coordinates but
  an untextured material does not set it.

## When a build is missing one

An exported game checks its precompiled set at startup. If a variant it needs is absent,
it prints the missing specs together with the command that generates them, then exits:

```
Doriax is missing precompiled shaders in:
assets/shaders

Missing shaders:
mesh:Uv1,Uv2,Puc,Shw,Nor,Tan,Ski,Aop; mesh:Uv1,Puc,Shw,Nor,Tan,Aop

Bundle precompiled shaders for graphic backend: opengl
To generate them manually with Doriax Editor:

> doriax-editor shaders --out "assets/shaders" --backend opengl --shader "mesh:Uv1,Uv2,Puc,Shw,Nor,Tan,Ski,Aop" --shader "mesh:Uv1,Puc,Shw,Nor,Tan,Aop"
```

The listed specs are authoritative — they are what the running scene asked for. Fix it in
whichever way suits the workflow:

| Situation | Fix |
| --- | --- |
| Exporting from the editor | Play each scene once, then export. The **Shaders** list fills itself |
| Scripted or CI export | Pass the specs with `--shader`, which replaces what the scenes report |
| Scenes generated by a tool | Write the `shaderKeys` entries into the generated `.scene` files |

For a CI pipeline the `--shader` route is the reliable one: it does not depend on whether
a machine with a GPU ever opened the project.

## See also

- [Custom Shaders](../editor/custom-shaders.md) — forking a built-in shader
- [Command-Line Tools](../editor/command-line.md) — `export` and `shaders` subcommands
- [Rendering Pipeline](rendering-pipeline.md#shaders) — what the built-in shaders do
