---
description: Export a Doriax project from the editor and prepare it for a target platform build.
---

# Exporting a Project

Exporting turns editor-authored scenes, resources, scripts, and shaders into a buildable
runtime project for a target platform.

## Export checklist

Before exporting, verify:

- All scenes are saved.
- The intended startup scene is selected.
- Resource paths are inside the project or otherwise reachable by the exporter.
- Lua and C++ entry points are configured so only the intended startup path creates the
  main scene.
- Target platform dependencies are installed.
- The output folder is outside the source asset folders you edit by hand.

## What the exporter prepares

The editor export pipeline can prepare:

| Output | Purpose |
| --- | --- |
| Scene code/data | Serialized scene hierarchy, components, bundles, and child scene references |
| Resources | Textures, models, fonts, audio, and other project assets |
| Scripts | Lua files and generated C++ glue for script entry points |
| Shaders | Cross-platform shader data for the selected backend |
| Build files | CMake, Gradle, Xcode, Emscripten, or platform-specific project files |

## Shader output

The exporter supports shader output formats configured by the editor's shader export
settings. Use the default unless you are debugging shader packaging or integrating a
custom build step.

## Build after export

Desktop exports are generally built with CMake:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
cmake --install build --config Release
```

Android, iOS, macOS, and HTML5 have additional platform requirements. See the
[Export Window](../editor/export.md) section and the target-specific guide.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Scene does not load | Startup scene, scene ID/name, exported scene list |
| Blank window | Active camera, canvas size, render backend, asset paths |
| Missing textures | Resource folder, texture path case, unsupported source format |
| Script starts twice | `NO_CPP_INIT` / `NO_LUA_INIT` configuration |
| Shader errors | Target backend, shader compiler output, generated shader files |

## Exporting without the GUI

You can run the same export from a terminal with the `doriax-editor` CLI — handy for
build servers and automated releases:

```bash
doriax-editor export --project ./MyGame --out ./build/MyGame --platform "linux,web"
```

See [Command-Line Tools](../editor/command-line.md) for all options.

Continue with [Export Window](../editor/export.md) and [Build Options](../reference/build-options.md).