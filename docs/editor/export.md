---
description: Export modes (Source Code, Desktop, Web), settings, generated files, shader compilation, and platform builds in the Doriax editor.
---

# Export Window

The **Export Window** turns a Doriax project into something you can ship. It collects
scene data, resources, scripts, generated C++ glue, engine runtime files, and compiled
shaders — and, depending on the mode, also compiles the result into a ready-to-run
build.

![Export window](../assets/screenshots/editor-export-window.png)

## Opening the Export Window

Choose **File → Export** from the menu bar, or press the **Export** button in the
toolbar.

## Export modes

The window opens with three modes to choose from:

| Mode | Output | Use it when |
| --- | --- | --- |
| **Source Code** | A self-contained buildable C++ project (engine source included) for Android, iOS, Web, Windows, macOS, and Linux | You want full control of the build, target mobile platforms, or integrate with CI |
| **Desktop** | A ready-to-run native executable for the machine you are on (Linux, Windows, or macOS) | You want a playable desktop build without touching a compiler |
| **Web** | HTML + JavaScript + WebAssembly via [Emscripten](https://emscripten.org/) | You want a browser build without running `emcmake` yourself |

Selecting a mode opens its settings screen; the **Back** button returns to the mode
selection.

**Desktop** and **Web** run the Source Code pipeline internally: they generate the full
project into a build cache inside your project (`.doriax/export/desktop` or
`.doriax/export/web`), compile it there, and copy only the final artifacts to your
chosen destination folder.

## Common settings

All modes share these settings:

| Setting | Meaning |
| --- | --- |
| **Target / Destination Directory** | Where the output goes. Source Code requires an empty directory; Desktop and Web overwrite existing files in the destination |
| **Start Scene** | Scene loaded when the exported game launches |
| **Shaders** | The shader variants compiled into the build (pre-filled from your scenes; add or remove entries as needed) |

The assets and Lua folders that ship with the build come from
[Project Settings](project-workflow.md#assets-and-lua-directories), not from this window:
stored references are relative to those directories, so exporting a different one would
break every path in the scenes.

The experimental **Native Resource Pack** choice also comes from **Project Settings →
Build**. It is off by default; see [Native resource pack](#native-resource-pack) for its
output and runtime restrictions.

The shader list is populated automatically from every saved scene, including a live scan
of the currently open scenes — so a component added since the last save (for example a
shadow-casting 2D light) is already accounted for. Use **Add** if your game enables a
feature only at runtime from scripts (say, turning on SSR) so its shaders ship too.

## Source Code mode

Exactly the classic export: choose the **graphic backends** to include (OpenGL, OpenGL ES
3, Direct3D 11, Metal for macOS and iOS, Vulkan) — this decides which shader formats are
compiled in — and get a buildable CMake project in the target directory.

The source builds for every supported operating system regardless of this choice; only the
shaders are affected, so include every backend the project may eventually be built with.
The backends your own machine can build are pre-selected. See
[Shader compilation](#shader-compilation) for which target needs which backend.

### Generated output structure

```
output/
├── CMakeLists.txt       ← build system entry point
├── core/  libs/  platform/  renders/  workspaces/
│                        ← engine runtime source (copied from the editor's SDK)
├── shaders/             ← compiled shader headers for the selected backends
└── project/
    ├── main.cpp         ← generated startup entry point
    ├── *.cpp            ← generated scene and bundle factory sources
    ├── assets/          ← contents of the project's assets directory
    │                    ← (or resources.pak only, when packing is enabled)
    ├── lua/             ← contents of the project's Lua directory
    │                    ← (empty directory kept when packing is enabled)
    └── scripts/         ← your registered C++ scripts
```

Those three trees are filtered rather than mirrored, which matters when the assets and Lua
directories are left at their default `<Project root>` and all three come from the same
folder:

- **C++ sources and headers** only ever reach `scripts/`, at their path relative to the
  project root — a script kept in `scripts/CharacterController.cpp` therefore exports as
  `project/scripts/scripts/CharacterController.cpp`, which is the path the generated
  `scene_scripts.cpp` includes it by.
- **Lua sources** only reach `lua/`, the root `lua://` and `require` resolve against; they
  are not copied to `assets/` as well. A Lua file outside the Lua directory has no other
  home, so it still ships as an asset.
- **Data files** a script may read through either prefix (`.json`, `.txt`, `.csv`, `.dat`
  and similar) are copied to both trees.

A folder appears in the export only when a file lands in it, so a folder holding nothing
but scripts leaves no empty directory behind. The exception is a packed Source Code
export, which keeps an empty `project/lua/` directory for the generated Xcode workspace.

Build it afterwards with the appropriate [platform toolchain](#platform-toolchains).

## Native resource pack

Enable **Project → Project Settings → Build → Native Resource Pack** to combine
the exported `assets/` and `lua/` trees into one `resources.pak`. This experimental,
project-wide option is intended for ready-to-run **Desktop** exports and Android builds
made from **Source Code** output. It has no effect on **Web** mode, which continues to
produce Emscripten's `.data` bundle.

The resulting layout depends on the export mode:

| Mode | Resource output when packing is enabled |
| --- | --- |
| **Desktop** | `resources.pak` beside the executable; loose `assets/` and `lua/` directories are removed |
| **Source Code** | `project/assets/resources.pak`; the loose contents are removed, while the empty `project/lua/` directory is retained for generated Xcode workspace compatibility |
| **Web** | Unchanged; Emscripten emits its normal `.data` bundle |

The pack preserves the usual logical names. High-level loaders, Lua `require()`, script
entries, and `Data::open()` can read plain asset-relative paths, `asset://` paths, and
`lua://` paths transparently; external buffers and images referenced by GLTF models work
the same way. Absolute paths, `data://`, and other schemes continue to resolve outside
the pack. Editor Play mode is unaffected: it always reads the project's loose source
files.

!!! warning "Experimental limitations"
    - `File` opens real filesystem files and cannot open a packed entry. Use `Data` (or
      an engine resource loader) for read-only packaged resources. This also means each
      opened entry is read into memory rather than exposed as a streaming file handle.
      `FileData.newFile()` follows the same rule: a packed path returns an in-memory
      `Data` object even when a file handle was requested.
    - A pack must remain below **2 GiB**. Export stops with an error if the combined
      header and resource data exceed that limit.
    - Packing only obfuscates the bytes; it does **not** encrypt or securely protect
      shipped assets.
    - `resources.pak` and `resources.pak.tmp` are reserved, case-insensitive names at
      the top level of the configured assets directory. Rename any file or directory
      with either name before exporting, even when packing is disabled.

If you disable the option and export again, the exporter removes a stale pack and ships
the loose resource directories again. Command-line exports honor the saved project
setting; there is no separate CLI switch.

## Desktop mode

Builds a native executable for the operating system the editor is running on, using
CMake and the **compiler kit configured in Project Settings** (or the system default
toolchain when none is selected). The window shows the effective compiler and parallel
job count; change them in **Project Settings → Build**.

Choose the **Graphic Backend** before exporting. The available choices follow the host
operating system:

| Host | Backends |
| --- | --- |
| **Linux** | OpenGL *(default)*, Vulkan |
| **Windows** | OpenGL *(default)*, Vulkan, Direct3D 11 |
| **macOS** | Metal *(default)*, OpenGL |

The exporter passes the selection to CMake and compiles only the shader format needed
by that backend. Vulkan builds require the Vulkan development files or SDK to be
available to the compiler. macOS has no Vulkan option because its only driver, MoltenVK,
is missing an extension the renderer needs — see
[Vulkan backend](../building/macos.md#vulkan-backend).

The destination folder receives:

```
destination/
├── MyProject            ← the executable (MyProject.exe on Windows)
├── assets/              ← runtime resources (default)
├── lua/                 ← runtime Lua scripts (default)
├── resources.pak        ← replaces assets/ and lua/ when packing is enabled
├── icon.png             ← (Linux, with a project icon set)
└── MyProject.desktop    ← (Linux, with a project icon set)
```

Run the executable from that folder — it resolves the loose `assets/` and `lua/`
directories, or `resources.pak`, relative to its working directory.

### Application icon

Set a **project icon** in **Project Settings → Window → Icon** (square PNG, 256×256 or
larger recommended) and desktop exports use it automatically:

- **Windows** — embedded into the executable (Explorer, taskbar, and window icon).
- **Linux (X11)** — window and taskbar icon at runtime. Executable files on Linux
  cannot carry icons, so the export also ships `icon.png` and a ready-made
  `.desktop` launcher entry; install it with
  `cp MyProject.desktop ~/.local/share/applications/` to get the icon in menus and
  docks — and on **Wayland**, where windows only receive icons through that entry.
- **macOS** — dock icon at runtime.

!!! note "Requirements"
    Desktop mode needs **CMake** and a C++ compiler installed. The window warns you with
    install instructions when either is missing. On macOS the **Xcode generator** is not
    supported for this mode (it produces an app bundle instead of a plain executable);
    use the default toolchain.

## Web mode

Builds the project with Emscripten and copies `MyProject.html`, `.js`, `.wasm`, and
`.data` (the packed assets) to the destination. The Web graphic backend is fixed to
**WebGL 2 (OpenGL ES 3)**.

The editor locates the Emscripten SDK automatically from the `EMSDK` environment
variable or `emcmake` on `PATH`. If neither is set, use **Browse** in the settings to
point at your `emsdk` folder once — the path is remembered in the editor settings across
projects. **Auto** returns to automatic detection. The status icon beside
**Emscripten SDK** shows whether detection succeeded; hover it to see where the SDK was
found or how to resolve a missing SDK.

!!! tip "Testing the build"
    Browsers do not load WebAssembly from `file://`. Serve the destination folder with
    any local web server, for example:

    ```bash
    python3 -m http.server --directory /path/to/destination
    ```

See [Building for HTML5](../building/html5.md) for Emscripten installation and advanced
options such as thread support.

## Build progress and cancellation

While exporting, the window shows each phase, a progress bar (driven by the compiler's
own progress output during Desktop/Web builds), and the last build log line. The full
log streams to the **Output** panel. **Cancel** stops the export and terminates the
running compiler processes.

## The build cache

Desktop and Web modes keep their generated project and CMake build tree inside your
project under `.doriax/export/desktop` and `.doriax/export/web`. The first export
compiles the whole engine and takes a while; subsequent exports only rebuild what
changed — typically just your scenes and scripts, finishing in seconds.

- Changing the graphics backend, compiler kit, generator, or Emscripten SDK wipes the
  cache's build tree automatically (CMake cannot switch these settings in place).
- The cache is safe to delete at any time; the next export simply starts from scratch.
- Keep `.doriax/` out of version control.

## Export phases

| Phase | Output |
| --- | --- |
| Scene factory generation | Generates a C++ factory function for each scene from its YAML |
| Bundle factory generation | Generates C++ factory functions for each bundle |
| Asset packaging | Copies and organizes resource files, then optionally combines native assets and Lua files into `resources.pak` |
| Startup code generation | Generates `main.cpp` / entry point with scene registration |
| Engine template copy | Copies the runtime engine source and CMake/build files |
| Shader compilation | Translates shaders for the selected graphics backends |
| Configure & build *(Desktop/Web)* | Runs CMake and the compiler on the build cache |
| Collect artifacts *(Desktop/Web)* | Copies the executable or web files to the destination |

## Generated scene data

Meshes backed by a model file keep their geometry in the exported asset and load it at
runtime. Terrain meshes with a configured heightmap also rebuild their runtime buffers
from `TerrainComponent` settings and the exported heightmap. Other meshes without a
runtime geometry source, including geometry created directly in the editor, embed their
vertex and index buffers in the generated scene or bundle C++ as read-only static data.
The scene factory copies those bytes into the runtime buffers without placing the full
geometry blob on the thread stack.

Generated factories also construct large fixed-capacity components, such as mesh,
tilemap, and 3D physics body data, in temporary heap storage before inserting them into
the ECS. This prevents those payloads from inflating the scene factory's stack frame.

Large inline meshes still increase the generated source size, executable size, and C++
compile time. Prefer a GLTF or OBJ asset for multi-megabyte geometry that does not need
to be stored directly in the scene.

## Shader compilation

The shader builder translates shader source per graphics API, never per operating system.
Desktop mode compiles only the format its **Graphic Backend** selection needs, Web uses
WebGL 2, and Source Code mode compiles one format per backend you ticked:

| Backend | Shader language | File suffix |
| --- | --- | --- |
| OpenGL | GLSL 4.10 | `glsl410` |
| OpenGL ES 3 | GLSL ES 3.00 (also WebGL 2) | `glsl300es` |
| Direct3D 11 | HLSL 5 | `hlsl5` |
| Metal (macOS) | MSL 2.1 | `msl21macos` |
| Metal (iOS) | MSL 2.1 | `msl21ios` |
| Vulkan | SPIR-V 1.0 | `spirv10` |

Metal is the one backend split by operating system, because the cross-compiler emits
different MSL for macOS and iOS.

### Choosing backends

The runtime loads only the format matching the backend it was compiled with, so pick the
backends by how the exported source will be built:

| Target | Backends to include |
| --- | --- |
| Linux | OpenGL, Vulkan |
| Windows | OpenGL, Direct3D 11, Vulkan |
| macOS | Metal (macOS), OpenGL |
| iOS | Metal (iOS) |
| Android, Web | OpenGL ES 3 |

Including a backend you never build with only costs export time and file size. Leaving one
out that you do build with makes the game report the shaders as missing at startup, with
the `doriax-editor shaders` command needed to generate them.

If shader compilation fails, the Output panel reports the shader name, stage, backend,
and the compiler error. Fix the shader source and re-export.

Custom (forked) shaders are compiled and shipped through this same pipeline, embedded into
the build alongside the built-in ones. See [Custom Shaders — Export and runtime](custom-shaders.md#export-and-runtime).

## Platform toolchains

Source Code exports are built afterwards with the appropriate native toolchain:

| Target platform | Toolchain | Notes |
| --- | --- | --- |
| **Windows** | CMake + MSVC or MinGW | Requires CMake 3.16+, Windows SDK |
| **Linux** | CMake + GCC or Clang | Requires X11 or Wayland dev libraries |
| **macOS** | CMake + Xcode or CLang | Requires Xcode command-line tools |
| **Android** | Gradle + Android NDK | Requires Android Studio or SDK command-line tools |
| **iOS** | Xcode workspace | Requires a Mac with Xcode |
| **HTML5 / Web** | Emscripten | Requires `emcmake cmake` |

Desktop and Web modes run the Linux/Windows/macOS and Emscripten toolchains for you.

## VSync in desktop exports

The project-level **VSync** option is written into exported desktop CMake projects.
With VSync disabled, Linux GLFW, Windows/Linux Sokol OpenGL, and Windows Direct3D 11
builds use swap interval `0`. Vulkan builds prefer Immediate presentation, use Mailbox
when Immediate is unavailable, and fall back to the always-supported FIFO mode when
required by the driver or surface.

macOS Metal currently has no uncapped application-loop path in Doriax. Metal exports
therefore remain synchronized and emit a CMake warning when project VSync is disabled.
See [Project Workflow — VSync](project-workflow.md#vsync) for the full behavior table.

## Window settings in desktop exports

The project-level **Window** settings (mode, size, resizable, title) are written into
exported desktop CMake projects the same way. Linux GLFW builds honor all of them.
Windows and macOS Sokol builds honor the size, title, and fullscreen mode, but have no
maximized or non-resizable window support. Web, Android, and iOS exports ignore window
settings entirely — the game always fills the browser canvas or the device screen. See
[Project Workflow — Window](project-workflow.md#window) for the full behavior table.

## Exporting from the command line

The Source Code pipeline is available headlessly through the `doriax-editor` CLI, which
is ideal for build servers and CI/CD:

```bash
doriax-editor export --project ./MyGame --out ./build/MyGame --backend "vulkan,opengles"
```

See [Command-Line Tools](command-line.md) for the full `export` and `shaders` reference.

## Build options

See [Build Options](../reference/build-options.md) for a full list of CMake flags and
compile-time defines you can set to control engine features in the export. Source Code
export also writes engine capacity macros (`MAX_SUBMESHES`, `MAX_BONES`, and others)
from the largest values used in your scenes — see
[Engine capacity macros](../reference/build-options.md#engine-capacity-macros).

## Tips

- Keep export destinations and the `.doriax/` folder out of version control.
- Test exported builds on actual devices — some graphics, input, and memory behaviors
  differ between the editor's desktop preview and the target platform.
- If a shader is reported missing at runtime, re-export (the scene shader list refreshes
  automatically) or add the named shader manually with **Add** in the Shaders section.
