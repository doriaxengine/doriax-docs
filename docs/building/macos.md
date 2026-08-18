---
description: Build Doriax from source on macOS.
---

# Building for macOS

## 1. Install dependencies

- **Xcode** with the Command Line Tools (`xcode-select --install`)
- **CMake** — install via [the official installer](https://cmake.org/download/) or
  Homebrew:
- Python 3 for generated editor API suggestion files

```bash
brew install cmake ninja
```

## 2. Clone the repository

```bash
git clone https://github.com/doriaxengine/doriax.git
cd doriax
```

## 3. Configure and build

Using Ninja (single-config):

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -G "Ninja"
cmake --build build --config Release --target doriax-editor
```

The build produces `build/Doriax.app`. The executable inside it is
`Doriax.app/Contents/MacOS/Doriax`, the engine runtime sits beside it as
`libdoriax.dylib`, and the engine SDK is copied to `Contents/Resources/engine`.

!!! note "Why the SDK is in `Contents/Resources`"
    `codesign` treats everything under `Contents/MacOS` as code and refuses to sign a
    bundle that has plain files there. The editor resolves the SDK through
    `FileUtils::getEngineDir()`, which checks `Contents/Resources/engine` first and falls
    back to the directory next to the executable on other platforms.

!!! tip "Using the Xcode generator"
    To work inside Xcode, generate an Xcode project instead:

    ```bash
    cmake -S . -B build -G "Xcode"
    cmake --build build --config Release --target doriax-editor
    ```

    Xcode is a **multi-config** generator, so the bundle is placed under a configuration
    subdirectory such as `build/Release/Doriax.app`.

## Runtime project build

macOS runtime builds default to Metal. When using the Xcode generator, the app backend
defaults to the native Apple backend; otherwise it defaults to Sokol.

```bash
cmake -S engine -B build-runtime \
  -DPROJECT_ROOT=/path/to/project \
  -DCMAKE_BUILD_TYPE=Release \
  -G "Ninja"
cmake --build build-runtime --config Release --target doriax-project
```

For Xcode:

```bash
cmake -S engine -B build-xcode -DPROJECT_ROOT=/path/to/project -G "Xcode"
cmake --build build-xcode --config Release --target doriax-project
```

The engine sets the macOS deployment target to 10.15 for runtime builds.

!!! note "VSync"
    The project **VSync** setting applies to editor Play mode and supported desktop
    backends, but macOS Metal runtime builds currently remain synchronized. Configuring
    an exported Metal project with VSync disabled prints a CMake warning instead of
    selecting an unsafe zero swap interval.

## Vulkan backend

macOS has no native Vulkan driver. Vulkan runs through **MoltenVK**, a translation layer
over Metal that ships with the [Vulkan SDK](https://vulkan.lunarg.com/). Passing
`-DGRAPHIC_BACKEND=vulkan` builds the runtime against it, presenting to a `CAMetalLayer`
through `VK_EXT_metal_surface`:

```bash
cmake -S engine -B build-vulkan \
  -DPROJECT_ROOT=/path/to/project \
  -DGRAPHIC_BACKEND=vulkan \
  -DCMAKE_BUILD_TYPE=Release \
  -G "Ninja"
cmake --build build-vulkan --config Release --target doriax-project
```

If `VULKAN_SDK` is not set, the build looks for the SDK where its installer unpacks it
(`~/VulkanSDK/<version>/macOS`), so an editor launched from the Dock — which inherits no
shell environment — still finds it.

!!! warning "Not runnable yet"
    The renderer binds its resources through `VK_EXT_descriptor_buffer`, and MoltenVK does
    not implement that extension. A macOS Vulkan build compiles and links, then exits at
    startup with a message saying so, and the configure step prints a warning up front.
    **Metal is the supported macOS backend**; Vulkan is here for the day a driver provides
    the extension. This is also why Vulkan is not offered in the editor's Desktop export.

Shaders for Vulkan projects are compiled to SPIR-V by the editor's shader builder.
