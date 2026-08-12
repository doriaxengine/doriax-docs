---
description: CMake options, generated artifacts, backends, and build configuration reference for Doriax.
---

# Build Options

Doriax uses CMake for desktop editor/runtime builds and platform tooling for mobile,
Apple, and web exports.

## Common requirements

| Requirement | Notes |
| --- | --- |
| CMake | 3.20 or newer |
| C++ compiler | C++17-capable MSVC, GCC, Clang, or equivalent |
| Python 3 | Used by code generation scripts |
| Platform SDK | Required for Android, iOS, macOS, and web builds |

## Editor build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --target doriax-editor
cmake --install build --config Release --strip
```

On Windows the build also provides `doriax-editor-cmd`, the same editor linked as a
console application for automation and terminal output. It is excluded from the default
build, so request it by name:

```bash
cmake --build build --config Release --target doriax-editor-cmd
```

See [Command-Line Tools](../editor/command-line.md).

## Runtime build

```bash
cmake -S engine -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --config Debug
```

## Scripting entry options

| Option | Effect |
| --- | --- |
| `NO_CPP_INIT` | Disable the C++ startup entry point |
| `NO_LUA_INIT` | Disable the Lua startup entry point |

## Engine/library options

| Option | Effect |
| --- | --- |
| `DORIAX_SHARED` | Build the engine as a shared library when enabled |
| `ENABLE_OPT` | Enable SPIR-V optimizer support when available |
| `EMSCRIPTEN_THREAD_SUPPORT` | Enable pthread support for Emscripten builds |

## Runtime project options

| Option | Default | Effect |
| --- | --- | --- |
| `DORIAX_VSYNC_ENABLED` | `ON` | Synchronize supported desktop presentation backends to the display refresh rate. Set to `OFF` to request an uncapped build. macOS Metal remains synchronized. |
| `DORIAX_WINDOW_WIDTH` | `960` | Initial window width in pixels for desktop builds |
| `DORIAX_WINDOW_HEIGHT` | `540` | Initial window height in pixels for desktop builds |
| `DORIAX_WINDOW_MODE` | `0` | Initial window state: `0` windowed, `1` maximized, `2` fullscreen. The Sokol app backend has no maximized support and treats `1` as windowed. |
| `DORIAX_WINDOW_RESIZABLE` | `ON` | Allow resizing the window. Ignored by the Sokol app backend, whose windows are always resizable. |
| `DORIAX_WINDOW_TITLE` | `"Doriax"` | Window title-bar text |

The editor writes these options into exported CMake projects from **Project
Settings** (VSync and the Window settings). For a manually configured standalone
runtime, override them at configure time:

```bash
cmake -S engine -B build-runtime \
  -DPROJECT_ROOT=/path/to/project \
  -DDORIAX_VSYNC_ENABLED=OFF \
  -DDORIAX_WINDOW_MODE=2 \
  -DDORIAX_WINDOW_TITLE="My Game"
```

Vulkan treats `OFF` as a request for Immediate presentation, with Mailbox and then FIFO
as fallbacks according to surface support.

## Graphics backend

Set `GRAPHIC_BACKEND` when configuring a standalone runtime project. The editor's
Desktop export selector passes the corresponding value automatically; Web exports use
`gles3`.

| Option value | Target |
| --- | --- |
| `glcore` | Desktop OpenGL Core |
| `gles3` | OpenGL ES 3 / WebGL-style targets |
| `d3d11` | Windows Direct3D 11 |
| `metal` | macOS and iOS Metal |
| `vulkan` | Vulkan (Linux and Windows; requires `APP_BACKEND=sokol`) |

On macOS, `vulkan` builds through MoltenVK but cannot run yet — see
[Vulkan backend](../building/macos.md#vulkan-backend).

## App backend

| Backend | Target |
| --- | --- |
| `glfw` | Desktop editor/windowing |
| `sdl` | Desktop alternative when configured |
| `sokol` | Standalone desktop runtime path |
| `apple` | Native Apple/Xcode path |
| `android` | Android Native Activity |
| `emscripten` | HTML5/web builds |

## Generated artifacts

| Artifact | Generated from |
| --- | --- |
| `shaders.h` | Shader sources processed by CMake shader generation |
| `engine_api_suggestions.h` | Lua binding files parsed by `generate_api_suggestions.py` |
| Copied engine directory | Editor export/build support |

## Platform guides

See [Building Overview](../building/overview.md), then use the guide for your target
platform.
