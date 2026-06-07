---
description: Build Doriax from source on Windows.
---

# Building for Windows

## 1. Install dependencies

- [CMake](https://cmake.org/download/) 3.x or newer (added to your `PATH`)
- A C++ toolchain — **Visual Studio 2022** (Desktop development with C++) is recommended

## 2. Clone the repository

```bash
git clone https://github.com/doriaxengine/doriax.git
cd doriax
```

## 3. Configure and build

Using the Visual Studio generator:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -G "Visual Studio 17 2022"
cmake --build build --config Release
```

Visual Studio is a **multi-config** generator, so the resulting `doriax-editor`
executable is placed under a configuration subdirectory such as `build/Release/`.

!!! tip "Faster builds with Ninja"
    If you have Ninja installed you can use it instead of the Visual Studio generator:

    ```bash
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -G "Ninja"
    cmake --build build --config Release
    ```

    With Ninja the executable is created directly under `build/`.
