---
description: Frequently asked questions about Doriax Engine — license, platforms, scripting, and project status.
---

# Frequently Asked Questions

## What is Doriax Engine?

Doriax is a free, open-source 2D/3D game engine with an integrated desktop editor. You
author scenes visually, script in **Lua** or **C++**, and export buildable native
projects for desktop, mobile, and web. It is the continuation of **Supernova Engine**
under a new identity, keeping its ECS-based, data-oriented runtime.

## How much does it cost? Can I sell my game?

Doriax is released under the **MIT License** — free for personal and commercial use,
with no royalties, revenue share, or seat licenses. Bundled third-party libraries keep
their own (compatible) open-source licenses. See [License & Credits](license.md).

## Which platforms are supported?

| Area | Platforms |
| --- | --- |
| Editor | Windows, Linux, macOS |
| Exported projects | Windows, Linux, macOS, Android, iOS, HTML5 (WebAssembly) |
| Graphics backends | OpenGL, OpenGL ES 3, Metal, Direct3D 11, WebGPU |

## Lua or C++ — which should I use?

Both target the same runtime API. **Lua** gives the fastest iteration (no compile step)
and is the best starting point; **C++** gives native performance for hot paths. Most
projects mix them — see [Scripting](../manual/scripting.md).

## Does exporting produce a finished executable?

Exporting produces a **self-contained, buildable native project** (CMake, Gradle, or
Xcode depending on the target) with your scenes, assets, scripts, and compiled shaders.
You then build it with the platform's standard toolchain — see
[Exporting a Project](../tutorials/exporting-a-project.md) and
[Command-Line Tools](../editor/command-line.md) for automating this in CI.

## Is Doriax production-ready?

Doriax is under active development. The downloadable editor builds track the `main`
branch and are **not stable releases** — expect breaking changes while the engine and
documentation are refreshed under the Doriax name. Pin a commit for serious projects and
follow the repository for release tags.

## How does Doriax differ from Godot, Unity, or Unreal?

Doriax aims to be **lightweight and code-transparent**: a small MIT-licensed C++ runtime
with an ECS core, where exporting gives you a native project you fully own and can read,
modify, and build yourself. It does not try to match the breadth of larger engines'
tooling; it focuses on a compact feature set — 2D, 3D, UI, physics (Box2D / Jolt), audio
(SoLoud), particles, terrain, and skeletal animation — with both Lua and C++ as
first-class languages.

## Where do my old Supernova projects stand?

Supernova `0.5.5` was the last release of the legacy engine. The runtime API carried
over largely intact (with renames such as `SPROPERTY` → `DPROPERTY` and the `doriax`
namespace), but projects should migrate to the Doriax editor workflow. Some internal
folders may still mention the previous name during the transition.

## Where can I get help or report bugs?

- **Discord** — [discord.gg/yXXDyJf3gT](https://discord.gg/yXXDyJf3gT) for questions and
  discussion.
- **GitHub** — [github.com/doriaxengine/doriax](https://github.com/doriaxengine/doriax)
  for issues and contributions.

## How can I contribute?

Code contributions go through pull requests on GitHub. Documentation lives in its own
repository and accepts fixes through the **Edit this page** links — see the
[Documentation Guide](../contributing/documentation-guide.md).
