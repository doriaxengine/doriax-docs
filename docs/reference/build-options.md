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

On Windows, the build may also provide a console-oriented `doriax-editor-cmd` target
for automation and easier terminal output.

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

## Graphics backend

| Option value | Target |
| --- | --- |
| `glcore` | Desktop OpenGL Core |
| `gles3` | OpenGL ES 3 / WebGL-style targets |
| `d3d11` | Windows Direct3D 11 |
| `metal` | macOS and iOS Metal |
| `vulkan` | Vulkan (Linux and Windows; requires `APP_BACKEND=sokol`) |

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