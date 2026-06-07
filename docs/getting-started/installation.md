---
description: How to download the Doriax editor or build it from source on your platform.
---

# Installation

There are two ways to get Doriax Engine: download a prebuilt editor, or build it from
source.

## Download a prebuilt editor

The fastest way to start is to grab a prebuilt build of the editor from the official
website:

[Download Doriax Engine](https://doriax.org/#download){ .dx-btn .dx-btn-primary }

Builds are available for:

| Platform | Requirements |
| --- | --- |
| Windows | Windows 10+ · x64 |
| Linux | Ubuntu 22.04+ · x64 |
| macOS | macOS 12+ · Universal |

!!! warning "Nightly builds"
    The downloadable editor builds are pulled directly from the `main` branch and are
    **not stable releases**. Expect bugs, incomplete features, and breaking changes.
    Use them at your own risk.

## Build from source

Doriax is built with **CMake**. The root project builds the desktop editor target
`doriax-editor`.

### Quick build

```bash
git clone https://github.com/doriaxengine/doriax.git
cd doriax
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

On single-config generators (Ninja, Makefiles) the executable is created under
`build/`. On multi-config generators such as Visual Studio, look under the
configuration subdirectory (for example `build/Release/`).

!!! tip
    Each platform has additional dependencies and tooling. See the
    [Building](../building/overview.md) section for detailed, per-platform
    instructions.

## Repository layout

When working from source, it helps to know how the repository is organized:

| Directory | Contents |
| --- | --- |
| `editor/` | Desktop editor, windows, tools, project generation, and export flow |
| `engine/` | Runtime engine, platform layers, rendering, ECS, and project templates |
| `shadercompiler/` | Shader compilation and translation tools |
| `libs/` | Bundled third-party dependencies |

## Next steps

Once you have the editor running, continue to [Your First Project](first-project.md).
