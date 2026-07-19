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
| **Source Code** | A self-contained buildable C++ project (engine source included) for all supported platforms | You want full control of the build, target mobile platforms, or integrate with CI |
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
| **Assets Directory** | Project folder copied as the game's assets |
| **Lua Directory** | Project folder copied as the game's Lua scripts |
| **Start Scene** | Scene loaded when the exported game launches |
| **Shaders** | The shader variants compiled into the build (pre-filled from your scenes; add or remove entries as needed) |

The shader list is populated automatically from every saved scene, including a live scan
of the currently open scenes — so a component added since the last save (for example a
shadow-casting 2D light) is already accounted for. Use **Add** if your game enables a
feature only at runtime from scripts (say, turning on SSR) so its shaders ship too.

## Source Code mode

Exactly the classic export: choose the **platforms** to include (Linux, Windows, macOS,
iOS, Web, Android) — this decides which shader formats are compiled in — and get a
buildable CMake project in the target directory.

### Generated output structure

```
output/
├── CMakeLists.txt       ← build system entry point
├── core/  libs/  platform/  renders/  workspaces/
│                        ← engine runtime source (copied from the editor's SDK)
├── shaders/             ← compiled shader headers for the selected platforms
└── project/
    ├── main.cpp         ← generated startup entry point
    ├── *.cpp            ← generated scene and bundle factory sources
    ├── assets/          ← copied resources
    ├── lua/             ← copied Lua scripts
    └── scripts/         ← your registered C++ scripts
```

Build it afterwards with the appropriate [platform toolchain](#platform-toolchains).

## Desktop mode

Builds a native executable for the operating system the editor is running on, using
CMake and the **compiler kit configured in Project Settings** (or the system default
toolchain when none is selected). The window shows the effective compiler and parallel
job count; change them in **Project Settings → Build**.

The destination folder receives:

```
destination/
├── MyProject            ← the executable (MyProject.exe on Windows)
├── assets/              ← runtime resources
└── lua/                 ← runtime Lua scripts
```

Run the executable from that folder — it resolves `assets/` and `lua/` relative to its
working directory.

!!! note "Requirements"
    Desktop mode needs **CMake** and a C++ compiler installed. The window warns you with
    install instructions when either is missing. On macOS the **Xcode generator** is not
    supported for this mode (it produces an app bundle instead of a plain executable);
    use the default toolchain.

## Web mode

Builds the project with Emscripten and copies `MyProject.html`, `.js`, `.wasm`, and
`.data` (the packed assets) to the destination.

The editor locates the Emscripten SDK automatically from the `EMSDK` environment
variable or `emcmake` on `PATH`. If neither is set, use **Browse** in the settings to
point at your `emsdk` folder once — the path is remembered in the editor settings across
projects. **Auto** returns to automatic detection.

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

- Changing the compiler kit, generator, or Emscripten SDK wipes the cache's build tree
  automatically (CMake cannot switch toolchains in place).
- The cache is safe to delete at any time; the next export simply starts from scratch.
- Keep `.doriax/` out of version control.

## Export phases

| Phase | Output |
| --- | --- |
| Scene serialization | Converts scene YAML to runtime-loadable data |
| Bundle factory generation | Generates C++ factory functions for each bundle |
| Asset packaging | Copies and organizes resource files |
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

The shader builder translates shader source for the selected graphics backend. In
Desktop and Web modes the formats are chosen automatically for the target; in Source
Code mode they follow the selected platforms:

| Backend | Platforms |
| --- | --- |
| OpenGL / GLSL | Windows, Linux, macOS |
| OpenGL ES 3 / ESSL | Android, web |
| Metal / MSL | iOS, macOS |
| Direct3D 11 / HLSL | Windows |
| WebGL / GLSL ES | HTML5 / Emscripten |
| Vulkan / SPIR-V | Windows, Linux |

If shader compilation fails, the Output panel reports the shader name, stage, backend,
and the compiler error. Fix the shader source and re-export.

Custom (forked) shaders are compiled and shipped through this same pipeline — the Header
output embeds them into the build, while the `.sdat`/JSON output writes them to the
project's **Shaders Directory**. See [Custom Shaders — Export and runtime](custom-shaders.md#export-and-runtime).

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
doriax-editor export --project ./MyGame --out ./build/MyGame --platform "linux,web"
```

See [Command-Line Tools](command-line.md) for the full `export` and `shaders` reference.

## Build options

See [Build Options](../reference/build-options.md) for a full list of CMake flags and
compile-time defines you can set to control engine features in the export.

## Tips

- Keep export destinations and the `.doriax/` folder out of version control.
- Test exported builds on actual devices — some graphics, input, and memory behaviors
  differ between the editor's desktop preview and the target platform.
- If a shader is reported missing at runtime, re-export (the scene shader list refreshes
  automatically) or add the named shader manually with **Add** in the Shaders section.
