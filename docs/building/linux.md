---
description: Build Doriax from source on Linux.
---

# Building for Linux

## 1. Install dependencies

On Debian/Ubuntu-based distributions, install the development packages:

```bash
sudo apt update
sudo apt install -y \
  build-essential cmake ninja-build python3 \
  libglfw3-dev libxi-dev libxcursor-dev libxrandr-dev libxinerama-dev \
  libwayland-dev libxkbcommon-dev wayland-protocols extra-cmake-modules \
  libgl1-mesa-dev libdbus-1-dev
```

| Package | Purpose |
| --- | --- |
| `build-essential` | C/C++ compiler and toolchain |
| `cmake`, `ninja-build` | Build system |
| `python3` | Generated editor API suggestion files |
| `libglfw3-dev` | Windowing / input |
| `libxi-dev`, `libxcursor-dev`, `libxrandr-dev`, `libxinerama-dev` | X11 input, cursor, and display support |
| `libwayland-dev`, `libxkbcommon-dev`, `wayland-protocols` | Wayland support through GLFW/native dialogs |
| `libgl1-mesa-dev` | OpenGL headers |
| `libdbus-1-dev` | Native file dialog / portal support |

## 2. Clone the repository

```bash
git clone https://github.com/doriaxengine/doriax.git
cd doriax
```

## 3. Configure and build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -G "Ninja"
cmake --build build --config Release --target doriax-editor
```

Ninja is a **single-config** generator, so the `doriax-editor` executable is created
directly under `build/`.

## Runtime project build

Linux runtime builds default to OpenGL Core and the GLFW app backend.

```bash
cmake -S engine -B build-runtime \
  -DPROJECT_ROOT=/path/to/project \
  -DCMAKE_BUILD_TYPE=Release \
  -G "Ninja"
cmake --build build-runtime --config Release --target doriax-project
```

Assets and Lua files are copied next to the build output when the project contains
`assets/` and `lua/` folders.

## Vulkan backend

To build a Linux runtime with the Vulkan backend, install the Vulkan SDK development
packages and pass `-DGRAPHIC_BACKEND=vulkan` at configure time. The Vulkan backend
requires the sokol app backend, which is selected automatically:

```bash
sudo apt install -y libvulkan-dev vulkan-tools
cmake -S engine -B build-vulkan \
  -DPROJECT_ROOT=/path/to/project \
  -DGRAPHIC_BACKEND=vulkan \
  -DCMAKE_BUILD_TYPE=Release \
  -G "Ninja"
cmake --build build-vulkan --config Release --target doriax-project
```

Shaders for exported Vulkan projects are compiled to SPIR-V by the editor's shader
builder.
