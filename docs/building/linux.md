---
description: Build Doriax from source on Linux.
---

# Building for Linux

## 1. Install dependencies

On Debian/Ubuntu-based distributions, install the development packages:

```bash
sudo apt update
sudo apt install -y \
  build-essential cmake ninja-build \
  libglfw3-dev libxi-dev libxcursor-dev libgl1-mesa-dev
```

| Package | Purpose |
| --- | --- |
| `build-essential` | C/C++ compiler and toolchain |
| `cmake`, `ninja-build` | Build system |
| `libglfw3-dev` | Windowing / input |
| `libxi-dev`, `libxcursor-dev` | X11 input and cursor support |
| `libgl1-mesa-dev` | OpenGL headers |

## 2. Clone the repository

```bash
git clone https://github.com/doriaxengine/doriax.git
cd doriax
```

## 3. Configure and build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -G "Ninja"
cmake --build build --config Release
```

Ninja is a **single-config** generator, so the `doriax-editor` executable is created
directly under `build/`.
