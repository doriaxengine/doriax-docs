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

The `doriax-editor` executable is created under `build/`.

!!! tip "Using the Xcode generator"
    To work inside Xcode, generate an Xcode project instead:

    ```bash
    cmake -S . -B build -G "Xcode"
    cmake --build build --config Release --target doriax-editor
    ```

    Xcode is a **multi-config** generator, so the build output is placed under a
    configuration subdirectory such as `build/Release/`.

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
