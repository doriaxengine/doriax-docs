---
description: Overview of building Doriax from source and exporting projects to each platform.
---

# Building — Overview

There are two things you might "build" with Doriax:

1. **The editor itself**, from source, using CMake.
2. **Your game project**, exported from the editor to a target platform.

This section focuses on building from source and the per-platform requirements.

!!! note "Transition in progress"
    Doriax is the continuation of Supernova Engine. Some platform tooling and folder
    names are still being refreshed under the Doriax name, so a few steps may reference
    legacy paths. When in doubt, the CMake commands below are the source of truth.

## Building the editor from source

Doriax uses **CMake**. The root project builds the desktop editor target
`doriax-editor`.

```bash
git clone https://github.com/doriaxengine/doriax.git
cd doriax
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

- On **single-config** generators (Ninja, Makefiles) the executable is created under
  `build/`.
- On **multi-config** generators (Visual Studio, Xcode) it is created under a
  configuration subdirectory such as `build/Release/`.

## Per-platform guides

| Target | Guide |
| --- | --- |
| Windows | [Building for Windows](windows.md) |
| Linux | [Building for Linux](linux.md) |
| macOS | [Building for macOS](macos.md) |
| Android | [Building for Android](android.md) |
| iOS | [Building for iOS](ios.md) |
| HTML5 | [Building for HTML5](html5.md) |

## Build options

Doriax exposes CMake options to control how a project is built. Two common ones control
the scripting entry point:

| Option | Effect |
| --- | --- |
| `NO_CPP_INIT` | Disable the C++ `init()` entry point |
| `NO_LUA_INIT` | Disable the Lua entry point |

Pass them at configure time, for example:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DNO_CPP_INIT=1
```

This is useful when a project mixes Lua and C++ and you want only one to drive scene
setup. See [Scripting](../manual/scripting.md) for the rationale.
