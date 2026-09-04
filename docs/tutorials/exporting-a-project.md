---
description: Export a Doriax project from the editor and prepare it for a target platform build.
---

# Exporting a Project

Exporting turns editor-authored scenes, resources, scripts, and shaders into a
shippable build — either a buildable source project or a compiled binary, depending on
the mode you choose.

## Choose an export mode

**File → Export** opens with three modes:

- **Source Code** — generates a self-contained C++ project (engine included) you build
  yourself with CMake or the platform toolchain. It supports Android, iOS, Web,
  Windows, macOS, and Linux. Pick this for mobile targets, CI pipelines, or when you
  want to customize the build.
- **Desktop** — compiles a ready-to-run executable for the OS the editor runs on and
  copies it with its resources to your destination folder. Resources ship as `assets/`
  and `lua/` by default, or as one `resources.pak` when the experimental project option
  is enabled. Needs CMake and a C++ compiler installed. Choose OpenGL or Vulkan on Linux;
  Direct3D 11, Vulkan, or OpenGL on Windows; and Metal or OpenGL on macOS.
- **Web** — compiles an HTML + JavaScript + WebAssembly build with Emscripten. Needs the
  [Emscripten SDK](https://emscripten.org/) installed (auto-detected, or point the
  window at your `emsdk` folder once) and uses WebGL 2.

Desktop and Web reuse the Source Code pipeline internally, building inside
`.doriax/export/` in your project — the first export compiles the engine and is slow,
later ones are incremental and fast.

## Export checklist

Before exporting, verify:

- All scenes are saved.
- The intended startup scene is selected.
- Resource paths are inside the project or otherwise reachable by the exporter.
- **Project Settings → Build → Native Resource Pack** is configured for the target:
  leave it off for loose files, or enable it for Desktop/Android after checking its
  [runtime limitations](../editor/export.md#native-resource-pack).
- Lua and C++ entry points are configured so only the intended startup path creates the
  main scene.
- Target platform dependencies are installed.
- The output folder is outside the source asset folders you edit by hand.

## What the exporter prepares

The editor export pipeline can prepare:

| Output | Purpose |
| --- | --- |
| Scene code/data | Serialized scene hierarchy, components, bundles, and child scene references |
| Resources | Textures, models, fonts, audio, and other project assets, as loose files or an optional native `resources.pak` |
| Scripts | Lua files and generated C++ glue for script entry points |
| Shaders | Shader data compiled for each selected graphic backend |
| Build files | CMake, Gradle, Xcode, Emscripten, or platform-specific project files |

## Shader output

The exporter supports shader output formats configured by the editor's shader export
settings. Use the default unless you are debugging shader packaging or integrating a
custom build step.

## Build after export

**Desktop** and **Web** mode exports are already built — run the executable from the
destination folder, or serve the web files with any local web server
(`python3 -m http.server`).

**Source Code** exports are built with CMake:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

Android, iOS, macOS, and HTML5 have additional platform requirements. See the
[Export Window](../editor/export.md) section and the target-specific guide.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Scene does not load | Startup scene, scene ID/name, exported scene list |
| Blank window | Active camera, canvas size, render backend, asset paths |
| Missing textures | Resource folder, texture path case, unsupported source format |
| Assets disappear only when packing is enabled | Code that constructs `File` directly; packed read-only resources must use `Data` or an engine loader |
| Export rejects `resources.pak` | Rename the top-level asset; `resources.pak` and `resources.pak.tmp` are reserved export names |
| Script starts twice | `NO_CPP_INIT` / `NO_LUA_INIT` configuration |
| Shader errors | Target backend, shader compiler output, generated shader files |
| Slow or unusually large C++ build | Large inline mesh data; prefer a GLTF or OBJ asset |

## Exporting without the GUI

You can run the same export from a terminal with the `doriax-editor` CLI — handy for
build servers and automated releases:

```bash
doriax-editor export --project ./MyGame --out ./build/MyGame --backend "vulkan,opengles"
```

See [Command-Line Tools](../editor/command-line.md) for all options.

Continue with [Export Window](../editor/export.md) and [Build Options](../reference/build-options.md).
