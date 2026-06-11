---
description: Build Doriax from source on Windows.
---

# Building for Windows

## 1. Install dependencies

- [CMake](https://cmake.org/download/) 3.20 or newer, added to `PATH`
- **Visual Studio 2022** with Desktop development with C++
- [GLFW](https://www.glfw.org/) 3.4 development package, or SDL2 if building with `-DAPI_BACKEND=sdl`
- Python 3 for generated editor API suggestion files

## 2. Clone the repository

```bash
git clone https://github.com/doriaxengine/doriax.git
cd doriax
```

## 3. Configure and build

Using the Visual Studio generator:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -G "Visual Studio 17 2022"
cmake --build build --config Release --target doriax-editor
```

Visual Studio is a **multi-config** generator, so the resulting `doriax-editor`
executable is placed under a configuration subdirectory such as `build/Release/`.

The Windows runtime defaults to Direct3D 11 for standalone projects. You can request
OpenGL Core instead with `-DGRAPHIC_BACKEND=glcore` when configuring a runtime build.

!!! tip "Faster builds with Ninja"
    If you have Ninja installed you can use it instead of the Visual Studio generator:

    ```bash
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -G "Ninja"
    cmake --build build --config Release --target doriax-editor
    ```

    With Ninja the executable is created directly under `build/`.

## Runtime project build

For an exported or standalone runtime project, configure the engine directory and pass
the project root if it is not the default `engine/project` folder:

```bash
cmake -S engine -B build-runtime -DPROJECT_ROOT="C:/path/to/project" -DCMAKE_BUILD_TYPE=Release
cmake --build build-runtime --config Release --target doriax-project
```

Use the generated executable from the selected configuration folder.

## Vulkan backend

To build a Windows runtime with the Vulkan backend, install the
[Vulkan SDK](https://vulkan.lunarg.com/) and set the `VULKAN_SDK` environment variable
to your SDK path. Pass `-DGRAPHIC_BACKEND=vulkan` at configure time:

```bash
cmake -S engine -B build-vulkan ^
  -DPROJECT_ROOT="C:/path/to/project" ^
  -DGRAPHIC_BACKEND=vulkan ^
  -DCMAKE_BUILD_TYPE=Release ^
  -G "Ninja"
cmake --build build-vulkan --config Release --target doriax-project
```

Shaders for exported Vulkan projects are compiled to SPIR-V by the editor's shader
builder.
