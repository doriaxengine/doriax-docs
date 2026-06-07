---
description: Build Doriax from source on macOS.
---

# Building for macOS

## 1. Install dependencies

- **Xcode** with the Command Line Tools (`xcode-select --install`)
- **CMake** — install via [the official installer](https://cmake.org/download/) or
  Homebrew:

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
cmake --build build --config Release
```

The `doriax-editor` executable is created under `build/`.

!!! tip "Using the Xcode generator"
    To work inside Xcode, generate an Xcode project instead:

    ```bash
    cmake -S . -B build -G "Xcode"
    cmake --build build --config Release
    ```

    Xcode is a **multi-config** generator, so the build output is placed under a
    configuration subdirectory such as `build/Release/`.
