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

The Windows download contains two executables: run `doriax-editor.exe` to open the
editor, and use `doriax-editor-cmd.exe` for scripting and CI. See
[Command-Line Tools](../editor/command-line.md).

The Linux download is an **AppImage**: unzip it, mark it executable with `chmod +x`, and
run the file directly — there is nothing to install. A plain folder of the same build is
offered next to it if you would rather have the binaries loose.

!!! tip "Adding Doriax to your application menu"
    An AppImage is a single self-contained file, so nothing registers it with your desktop
    on its own — which is why it has no menu entry or icon until you integrate it. Tools
    such as [Gear Lever](https://github.com/mijorus/gearlever) or `appimaged` read the
    desktop entry and icons bundled inside the AppImage and register them for you.

The macOS download is a disk image holding `Doriax.app`. Open the `.dmg` and drag the app
onto the **Applications** shortcut inside it.

!!! warning "macOS blocks the first launch"
    Doriax is signed, but not notarized by Apple — notarization requires a paid Apple
    Developer membership. macOS therefore reports that it cannot verify the app the first
    time you open it.

    To allow it, open **System Settings → Privacy & Security**, scroll to the security
    section near the bottom, and click **Open Anyway**. You only do this once per version.

    Before macOS Sequoia you could Control-click the app and choose **Open** instead. That
    shortcut was removed.

    Downloading from a terminal skips the prompt altogether, because the quarantine flag
    is set by the browser rather than by macOS:

    ```bash
    curl -L -o doriax_macos_dmg.zip \
      https://nightly.link/doriaxengine/doriax/workflows/cmake.yml/main/doriax_macos_dmg.zip
    ```

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
    Each platform has additional dependencies and tooling. See
    [Building from Source](../building/overview.md) for detailed, per-platform
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
