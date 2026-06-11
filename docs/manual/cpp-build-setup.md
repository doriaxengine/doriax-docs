---
description: Toolchain requirements and troubleshooting for compiling C++ scripts with the Doriax Editor.
---

# C++ Build Setup

Lua scripts run as-is, but **C++ scripts are compiled on your machine** the first time
you press Play (and again whenever a C++ source changes). The editor generates a CMake
project for your scripts, configures it, and builds a shared library that is loaded back
into the editor. This page covers what tools that build step needs and how to fix the
most common failures.

If you only use Lua scripts, no build tools are required.

## Required tools

- **CMake 3.15 or newer**, available on `PATH`.
- A **C++17 compiler** for your platform (see below).

When you press Play in a project that contains C++ scripts, the editor first checks for
these tools and shows a *Missing Build Tools* dialog listing anything it could not find.

=== "Windows"

    Install one of:

    - **Visual Studio 2019/2022** (Community is fine) with the
      **"Desktop development with C++"** workload — the simplest option. The editor
      finds it automatically even when `cl.exe` is not on `PATH`.
    - **LLVM/Clang** (MSVC target, e.g. the `clang+llvm-*-pc-windows-msvc` release) —
      also requires **Ninja** on `PATH` (see the warning below).
    - **MinGW GCC or Clang** — uses the *MinGW Makefiles* generator.

    Install CMake from [cmake.org/download](https://cmake.org/download/) and check
    **"Add CMake to the system PATH"** during setup.

=== "Linux"

    ```bash
    sudo apt install cmake build-essential   # Debian/Ubuntu
    sudo dnf install cmake gcc-c++           # Fedora
    ```

=== "macOS"

    ```bash
    xcode-select --install   # Apple Clang
    brew install cmake
    ```

## Choosing a compiler

Open **Project → Project Settings** and use the **Compiler** dropdown. The editor
detects available compilers (GCC, Clang, MSVC/Visual Studio) and pairs each one with a
compatible CMake generator:

| Compiler (Windows) | CMake generator used |
| --- | --- |
| MSVC / Visual Studio | Visual Studio (CMake default) |
| Clang targeting MSVC (`x86_64-pc-windows-msvc`) | Ninja — **required** |
| MinGW GCC or Clang (`*-mingw*`) | MinGW Makefiles |

**Default** lets CMake pick the platform default toolchain (Visual Studio on Windows,
`cc`/`c++` elsewhere). On Linux and macOS no generator pairing is needed.

!!! warning "Clang on Windows needs Ninja"
    CMake's Visual Studio generator always compiles with MSVC's `cl.exe` — it cannot
    drive a standalone `clang.exe`. A Clang (MSVC target) compiler therefore only works
    with the **Ninja** generator. If Ninja is not installed, the editor lists the Clang
    entry greyed-out with a *"requires Ninja on PATH"* note.

    Install Ninja with `winget install Ninja-build.Ninja`, or download `ninja-win.zip`
    from [ninja-build.org](https://ninja-build.org), unzip it to a folder on `PATH`,
    and verify with `ninja --version` in a new terminal. Restart the editor afterwards
    so it re-detects the compiler list.

    Do **not** use a pip-installed `ninja.exe` copied out of Python's `Scripts` folder —
    it is a wrapper that stops working outside its install location. If Windows blocked
    a downloaded exe, right-click it → **Properties** → **Unblock**.

Switching compilers is safe at any time: the editor detects the change and cleans the
build directory automatically (CMake cannot switch generators or compilers in-place).

## Where build files live

The CMake build tree is generated under **`.doriax/build`** inside your project folder.
It is a disposable cache — deleting it forces a full clean reconfigure and rebuild, which
is a good first step when the build state seems corrupted (for example after moving the
project, or upgrading CMake or the compiler).

## Troubleshooting

All configure and compile output streams into the **Output panel**. The first error line
is almost always the meaningful one.

| Symptom in the Output panel | Likely cause and fix |
| --- | --- |
| `Missing Build Tools` dialog | CMake or a C++ compiler is not installed / not on `PATH`. Install it and restart the editor. |
| `The C compiler ... is not able to compile a simple test program` together with `CMAKE_LINKER-NOTFOUND` or `TRK0005` | A custom compiler (usually Clang) was configured with the Visual Studio generator. Install Ninja and re-select the Clang compiler in Project Settings, or switch to the MSVC compiler. Editor versions before June 2026 allowed this broken combination. |
| `CMake was unable to find a build program corresponding to "Ninja"` | `ninja.exe` is not on `PATH`, or it exists but cannot run (pip wrapper copied out of place, or blocked download). Install the standalone binary and check `ninja --version` works in a fresh terminal. |
| `CMake configuration failed` with **no other output** | Update the editor — older versions dropped the output of commands that failed quickly. Current versions print the full CMake error plus a `Process exited with code N` line. |
| `Compiler kit changed. Cleaning build directory...` | Not an error — the compiler selection changed, so the editor wipes `.doriax/build` and reconfigures from scratch. |
| Errors persist after fixing the toolchain | Delete `.doriax/build` and press Play again to force a clean configure. |

## Next steps

- [Creating Scripts](creating-scripts.md) — script types and editor workflow
- [Code Editor](../editor/code-editor.md) — editing C++ in the editor and reading build output
- [Export Window](../editor/export.md) — building standalone projects outside the editor
