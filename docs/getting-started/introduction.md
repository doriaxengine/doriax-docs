---
description: An overview of Doriax Engine — its architecture, features, and what you can build with it.
---

# Introduction

**Doriax Engine** is a free, open-source 2D/3D game engine with an integrated editor
for building cross-platform games and interactive projects. It combines a lightweight,
data-oriented runtime with a modern desktop editor, so you can author scenes visually,
script in Lua or C++, and export to multiple platforms from a single environment.

Doriax is the continuation of **Supernova Engine** under a new identity and a broader
workflow focused on visual editing, shader generation, and project export.

## Design philosophy

Doriax is built around a few core principles:

- **Lightweight and efficient** — no heavy GUI overhead or unnecessary processing. The
  engine stays lean and produces small output.
- **Data-oriented design** — an Entity Component System (ECS) arranges data to take
  advantage of CPU caching, avoiding the performance pitfalls of traditional
  object-oriented designs.
- **Two languages, one workflow** — use **Lua** for rapid iteration and flexible
  scripting, or **C++** for full native performance. C++ scripts are compiled at build
  time, not runtime.
- **Write once, deploy everywhere** — a single project can target six platforms with
  native graphics backends.

## Documentation structure

This documentation follows a broad structure similar to large engine manuals:

| Section | Use it for |
| --- | --- |
| Getting Started | Install Doriax, understand the editor, and create a first project |
| Tutorials | Step-by-step 2D, 3D, and export walkthroughs |
| Editor | Panels, project workflow, assets, code editing, animation, and export tools |
| Manual | Engine concepts and subsystem guides |
| Reference | API maps, components, Lua bindings, and build options |
| Building | Platform-specific toolchain setup |

## What you can build

| Capability | Description |
| --- | --- |
| 2D games | Sprites, tilemaps, sprite slicing, and 2D physics |
| 3D games | GLTF/OBJ models, PBR materials, dynamic shadows, fog, and sky |
| Animation | Skeletal animation, morph targets, and a timeline editor |
| UI | A built-in UI system for menus, HUDs, and overlays |
| Physics | Integrated 2D and 3D physics via Box2D and Jolt Physics |
| Audio | 3D positional audio |

## Engine features

- 2D and 3D scenes with a shared ECS foundation
- GLTF and OBJ model loading
- Skeletal animation and morph targets
- PBR materials, dynamic shadows, fog, and sky
- Particle systems, UI, terrain LOD, and instancing
- Scene serialization, texture and shader pools, and multithreading
- 3D audio

!!! tip "Custom shaders"
    Fork, edit, and customize the built-in shaders for Mesh, UI, Points, Lines, and Sky
    components directly in the editor — see [Custom Shaders](../editor/custom-shaders.md).

## Platforms

| Area | Support |
| --- | --- |
| Editor downloads | Windows, Linux, macOS |
| Project targets | Windows, Linux, macOS, Android, iOS, HTML5 |
| Graphics APIs | OpenGL, Metal, DirectX |
| Scripting | Lua, C++ |

## Next steps

<div class="dx-cards" markdown>

<a class="dx-card" href="../installation/">
<p class="dx-card-title">Installation →</p>
<p class="dx-card-desc">Download the editor or build Doriax from source.</p>
</a>

<a class="dx-card" href="../first-project/">
<p class="dx-card-title">Your First Project →</p>
<p class="dx-card-desc">Build and run your first Doriax scene.</p>
</a>

<a class="dx-card" href="../../manual/architecture/">
<p class="dx-card-title">Architecture →</p>
<p class="dx-card-desc">Learn how the runtime is organized internally.</p>
</a>

</div>
