---
hide_title: true
description: Official documentation for the Doriax game engine — a free, lightweight, open-source engine for building 2D and 3D games with Lua or C++.
---

<div class="dx-hero" markdown>

<span class="dx-hero-badge">Open Source &amp; Free</span>

# Lightweight engine <span class="dx-text-gradient">for 2D &amp; 3D games</span> { .dx-hero-title }

Welcome to the official documentation for **Doriax Engine** — a free, lightweight,
and efficient open-source game engine with an integrated editor for creating 2D and
3D games. Script in **Lua** or **C++**, design scenes visually, and deploy to six platforms.

<div class="dx-hero-actions" markdown>
[Get Started](getting-started/introduction.md){ .dx-btn .dx-btn-primary }
[Download the Editor](https://doriax.org/#download){ .dx-btn .dx-btn-outline }
</div>

</div>

!!! note "Documentation status"
    This documentation covers the editor workflow, runtime architecture, core
    subsystems, build targets, and the current public API surface exposed by the
    Doriax source tree. Doriax is moving quickly, so the reference pages are written
    to be practical guides rather than frozen ABI guarantees.

## Start here

<div class="dx-cards" markdown>

<a class="dx-card" href="getting-started/introduction/">
<p class="dx-card-title">Introduction</p>
<p class="dx-card-desc">What Doriax is, its architecture, and what you can build with it.</p>
</a>

<a class="dx-card" href="getting-started/installation/">
<p class="dx-card-title">Installation</p>
<p class="dx-card-desc">Download a prebuilt editor or build Doriax from source.</p>
</a>

<a class="dx-card" href="getting-started/first-project/">
<p class="dx-card-title">Your First Project</p>
<p class="dx-card-desc">Create a scene, add an entity, and run your first game.</p>
</a>

<a class="dx-card" href="manual/entity-component-system/">
<p class="dx-card-title">Entity Component System</p>
<p class="dx-card-desc">Understand the data-oriented ECS at the core of the engine.</p>
</a>

<a class="dx-card" href="reference/index/">
<p class="dx-card-title">API Reference</p>
<p class="dx-card-desc">Complete class reference with C++ and Lua on every page.</p>
</a>

</div>

## Why Doriax

<div class="dx-feature-grid" markdown>

<div class="dx-feature" markdown>
**2D &amp; 3D Engine**
<p>Full support for both 2D and 3D development — sprites, tilemaps, 3D models, skeletal animation, and more in one lean workflow.</p>
</div>

<div class="dx-feature" markdown>
**Built-in Editor**
<p>Scene hierarchy, properties inspector, animation timeline, integrated code editor, and resource management — all in one place.</p>
</div>

<div class="dx-feature" markdown>
**Lua &amp; C++**
<p>Prototype quickly in Lua or compile C++ at build time for maximum native performance. Combine both seamlessly.</p>
</div>

<div class="dx-feature" markdown>
**Entity Component System**
<p>A modern, data-driven ECS that maximizes CPU cache performance while keeping the engine lightweight and efficient.</p>
</div>

<div class="dx-feature" markdown>
**Cross-Platform**
<p>Deploy to Windows, Linux, macOS, Android, iOS, and HTML5 with OpenGL, Vulkan, Metal, and DirectX backends.</p>
</div>

<div class="dx-feature" markdown>
**PBR Rendering**
<p>Physically-based rendering with dynamic shadows, fog, sky system, and advanced materials for photorealistic visuals.</p>
</div>

<div class="dx-feature" markdown>
**Editor Export Pipeline**
<p>Scene serialization, script generation, shader compilation, and platform-specific project generation live in the editor.</p>
</div>

</div>

## The editor

![Doriax Engine Editor — 3D scene](assets/screenshots/editor-3d-scene.png)

Doriax ships with a complete visual editor: design scenes, edit 2D tilemaps, animate
characters, write code, and test your game in play mode — all from one unified
environment. Learn more in [The Editor](editor/index.md).

---

!!! tip "Coming from Supernova?"
    Doriax Engine is the continuation of **Supernova Engine** under a new identity.
    Version `0.5.5` was the last legacy Supernova release. The core ECS and
    data-oriented runtime remain, now wrapped in a full editor and export pipeline.
