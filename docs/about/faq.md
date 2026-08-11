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

## Does Doriax use engine-specific asset formats?

No. Doriax has no equivalent of Godot's `.scn`/`.res` or Unity's imported assets, and no
import step that rewrites your files. The runtime opens standard formats directly —
`.glb`/`.gltf`/`.obj` for models, PNG/JPG/TGA/BMP/HDR/PSD/SVG for textures,
OGG/WAV/MP3/FLAC for audio, and TTF/OTF/TTC for fonts. The file your content tool produces
is the file the game loads.

Scenes, bundles, and materials are the exception. They are authored as YAML for the editor
and converted at export into C++ that is compiled into your game, rather than shipped as
data the runtime parses. See
[Resources & Assets](../manual/resources-and-assets.md#asset-types).

## Can I load assets at runtime?

Yes, for media. Models, textures, sounds, and fonts can be loaded or swapped from any path
at any point during gameplay, with `Engine.asyncLoading = true` moving the work to worker
threads and [`ResourceProgress`](../reference/classes/resourceprogress.md) reporting how
far along it is. Lua scripts also load from disk at runtime through the `lua://` root.

Entity hierarchies work differently, because scenes and bundles are compiled rather than
parsed. Spawning them on demand is fully supported through
[`BundleManager.createBundle`](../reference/classes/bundlemanager.md#createbundle) for any
bundle that existed at build time, but a scene or hierarchy contained in a file the
executable was not built with cannot be loaded. That is a deliberate trade: it keeps entity
setup statically typed, leaves reflection and deserialization out of the runtime, and keeps
startup cost and binary size low on the web and mobile targets. If you need player-supplied
or downloaded content, drive it with runtime media loading plus bundles composed in script.

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
