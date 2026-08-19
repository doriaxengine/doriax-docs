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
    - **MinGW GCC or Clang** — uses the *MinGW Makefiles* generator. Only works with a
      **MinGW build of the editor**, *not* the official MSVC download — see the ABI note
      under [Choosing a compiler](#choosing-a-compiler).

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

| Compiler (Windows) | CMake generator | C++ ABI | Official (MSVC) build |
| --- | --- | --- | --- |
| MSVC / Visual Studio | Visual Studio (CMake default) | MSVC | Yes |
| Clang targeting MSVC (`x86_64-pc-windows-msvc`) | Ninja — **required** | MSVC | Yes |
| MinGW GCC or Clang (`*-mingw*`) | MinGW Makefiles | GNU | No — needs a MinGW editor build |

**Default** lets CMake pick the platform default toolchain (Visual Studio on Windows,
`cc`/`c++` elsewhere). On Linux and macOS no generator pairing is needed.

Your selection is **remembered across sessions and projects** — newly created projects
inherit the compiler you last chose, so you only need to set it once (rather than having
each new project silently fall back to **Default**).

!!! danger "Your compiler must match the editor's own C++ ABI"
    C++ scripts are compiled into a shared library that is loaded **into the running
    editor and shares its engine instance** — so the plugin must use the same C++ ABI as
    the editor was built with. MSVC and MinGW (GCC) are **not** ABI-compatible: they
    disagree on name mangling, class layout, RTTI, exception handling and STL types. A
    MinGW plugin therefore cannot link against an MSVC-built engine — you get a wall of
    `undefined reference` errors — and the reverse fails just as badly.

    The **official Windows download is built with MSVC**, so with it you must use **MSVC**
    or **Clang targeting MSVC** (both free — see [Required tools](#required-tools)). To
    build plugins with **MinGW GCC**, you need a MinGW build of the editor (see
    [Building from Source → Windows](../building/windows.md)). The two never mix: one
    editor download supports one ABI.

    The editor knows which toolchain it was built with and **greys out incompatible
    compilers** in the **Compiler** dropdown — hover one to read why. This is a
    Windows-only concern; Linux and macOS each have a single system C++ ABI, so GCC and
    Clang interoperate there.

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

!!! info "Clang also needs the Windows SDK"
    A standalone Clang compiles your code with its own toolchain but still **links
    against the Windows SDK and the MSVC C runtime** (`kernel32.lib`, `msvcrtd`, …).
    Those ship with Visual Studio's "Desktop development with C++" workload. The editor
    loads the Visual Studio environment automatically before building with Ninja, so you
    do **not** need to launch it from a Developer Command Prompt. If linking fails with
    `lld-link: error: could not open 'kernel32.lib'`, the Windows SDK is either not
    installed or could not be located — install it via the Visual Studio Installer.

Switching compilers is safe at any time: the editor detects the change and cleans the
build directory automatically (CMake cannot switch generators or compilers in-place).

## Parallel builds

C++ scripts compile in parallel: by default the editor runs **one build job per
detected logical CPU thread**. That is dramatically faster on multi-core machines but
raises peak memory use, since every concurrent compiler process needs its own working
memory.

Open **Project → Project Settings** and use **Parallel Jobs** (below the **Compiler**
dropdown) to tune this:

| Value | Effect |
| --- | --- |
| `0` (default) | Automatic — one job per logical CPU thread of the machine running the build |
| `1` | Serial build — slowest, but minimal memory use |
| Any other number | At most that many concurrent jobs |

Lower the value if builds fail with out-of-memory errors or make the system
unresponsive — each concurrent C++ compile can use hundreds of MB of RAM, more with
heavy template use.

The value is saved as `cmakeBuildJobs` in `project.yaml` (omitted when automatic) and
travels with the project. It is safe to share between machines of different sizes: the
stored number is a *request*, and each machine caps it independently at build time (at
4× its logical CPU count, up to 65536) without rewriting the saved setting — a limit
chosen on a 32-core workstation is not lost when a teammate opens the project on a
4-core laptop.

!!! note "MSVC rebuilds scripts when the value changes"
    With the MSVC compiler the limit is applied through the compiler's `/MP` flag,
    because MSBuild alone cannot throttle per-file compilation within a single target.
    Since that changes compile flags, changing **Parallel Jobs** triggers a full script
    rebuild on the next Play. Ninja and Make apply the limit at the build-tool level,
    so changing it there only affects new compilations.

## Script directories

By default the editor compiles only the C++ scripts a scene actually uses — the files
referenced by a Script component. A helper class that no entity mentions is never built,
and every header is included by its full path from the project root.

**Project → Project Settings → Directories → Script Directories** changes that. Add any
folder inside your project and it becomes two things at once:

| Role | Effect |
| --- | --- |
| **Include root** | Headers under it are included by the path *below* the folder, so the full path from the project root is no longer needed |
| **Compile root** | Every `.cpp` under it is compiled, even when no entity references it |

Only the folders you add behave this way — the rest of the project is untouched, and a
project with no script directories builds exactly as before.

This lets you lay out code in modules and include across them by short path. With
`Source/Public` added as a root, a header at `Source/Public/Player/Script.h` becomes:

```cpp
#include "Player/Script.h"   // instead of "Source/Public/Player/Script.h"
```

Add as many roots as you need; they are searched in the order listed. Both roles apply to
Play builds and to [exported projects](../editor/export.md) alike.

!!! note "Keep roots inside the project"
    A folder outside the project compiles in the editor but **cannot be exported** — the
    export copies the project tree only, and warns that the directory was skipped. Use a
    folder inside the project for anything you intend to ship.

The list is saved as `scriptDirs` in `project.yaml` and travels with the project.

## Customizing the build

The `CMakeLists.txt` at your project root is generated: Play and Save overwrite it, so
edits to it are lost. To add your own CMake — linking a third-party library, extra
compile definitions, platform flags — create **`ProjectBuild.cmake`** next to it. The
editor never creates, reads or overwrites that file, and both the editor build and
exported builds include it when it exists.

```cmake
target_link_libraries(${DORIAX_TARGET} PRIVATE mylib)
target_include_directories(${DORIAX_TARGET} PRIVATE ${DORIAX_SCRIPTS_DIR}/ThirdParty/include)
```

Two variables are set for you, with the same meaning in both builds:

| Variable | Value |
| --- | --- |
| `DORIAX_TARGET` | The target to attach to |
| `DORIAX_SCRIPTS_DIR` | The root your `.h`/`.cpp` paths are relative to |

!!! warning "Attach through `${DORIAX_TARGET}`, not the target name"
    The target is named after your project in editor builds and after the application
    name in exported ones, so a hard-coded name works in one and breaks in the other —
    and breaks again if you rename the project.

For include paths alone you do not need this file: [Script
directories](#script-directories) covers that case from the editor.

## Where build files live

Play and Save rewrite the generated C++ glue: `CMakeLists.txt` at the **project root**,
`scene_scripts.cpp` under **`.doriax`**, and `main.cpp` plus the scene and bundle
factories under **`.doriax/generated`**. Together they cover every C++ script and
`.bundle` file that still exists on disk. Do **not** edit those files by hand — the next
Play or Save overwrites them. Put your own build settings in
[`ProjectBuild.cmake`](#customizing-the-build) instead, which is never overwritten.

The CMake build tree is generated under **`.doriax/build`**. It is a disposable cache —
deleting it forces a full clean reconfigure and rebuild, which is a good first step when
the build state seems corrupted (for example after moving the project, or upgrading CMake
or the compiler).

## Troubleshooting

All configure and compile output streams into the **Output panel**. The first error line
is almost always the meaningful one.

| Symptom in the Output panel | Likely cause and fix |
| --- | --- |
| `Missing Build Tools` dialog | CMake or a C++ compiler is not installed / not on `PATH`. Install it and restart the editor. |
| `The C compiler ... is not able to compile a simple test program` together with `CMAKE_LINKER-NOTFOUND` or `TRK0005` | A custom compiler (usually Clang) was configured with the Visual Studio generator. Install Ninja and re-select the Clang compiler in Project Settings, or switch to the MSVC compiler. Editor versions before June 2026 allowed this broken combination. |
| `CMake was unable to find a build program corresponding to "Ninja"` | `ninja.exe` is not on `PATH`, or it exists but cannot run (pip wrapper copied out of place, or blocked download). Install the standalone binary and check `ninja --version` works in a fresh terminal. |
| `undefined reference to` **every** engine symbol (`doriax::Vector3::Vector3`, `doriax::Engine::onUpdate`, …) at the **link** step | The selected compiler's C++ ABI does not match the editor's — typically MinGW GCC against the official MSVC build. Use MSVC or Clang-targeting-MSVC on the MSVC build (or a MinGW editor for MinGW). Current editors grey out incompatible compilers, so this mainly appears in older versions or when building outside the editor. See [Choosing a compiler](#choosing-a-compiler). |
| `lld-link: error: could not open 'kernel32.lib'` (or other `*.lib`) | Clang cannot find the Windows SDK libraries. Install the Windows SDK through the Visual Studio Installer ("Desktop development with C++"). The editor loads the MSVC environment automatically; if it can't find Visual Studio it warns and you can instead launch the editor from a Developer Command Prompt. |
| `No CMAKE_C_COMPILER could be found` (with `Building for: Visual Studio 17 2022`) | The build is using the **Default** toolchain and CMake's Visual Studio auto-detection found no usable compiler. Pick an explicit compiler in **Project Settings → Compiler** (MSVC, or Clang). The choice is remembered across projects, so you only set it once. If even MSVC fails here, your Visual Studio C++ toolset is incomplete — repair "Desktop development with C++" in the Visual Studio Installer. |
| `internal compiler error: Killed` (GCC/Clang) or `fatal error C1060: compiler is out of heap space` (MSVC) | The parallel build ran out of memory. Lower **Project Settings → Parallel Jobs** (try `1` or `2`) — see [Parallel builds](#parallel-builds). |
| `Does not match the generator used previously` | The build directory holds a cache from a different generator. The editor normally cleans it automatically when you switch compilers; if it reports the directory is **locked**, close anything using `.doriax/build` (notably the VS Code *CMake Tools* extension) or delete the folder manually, then try again. |
| `CMake configuration failed` with **no other output** | Update the editor — older versions dropped the output of commands that failed quickly. Current versions print the full CMake error plus a `Process exited with code N` line. |
| `CMake Error: File ... does not exist.` (or similar) for a script or `.bundle` you already deleted | Generated sources still listed a missing file. Current editors skip files that are gone from disk; press Play or Save once to regenerate. Do not patch the generated `CMakeLists.txt` — it is overwritten. If a closed scene still shows the old ScriptComponent entry, open that scene, remove the leftover, and save. |
| `Unknown type SomeClass` | A leftover C++ script class name is still registered. Remove that ScriptComponent entry from every scene and bundle that still lists it, then Play or Save. Recreating a script with the same class name also recovers a project that was already broken. |
| `Compiler kit changed. Cleaning build directory...` | Not an error — the compiler selection changed, so the editor wipes `.doriax/build` and reconfigures from scratch. |
| Errors persist after fixing the toolchain | Delete `.doriax/build` and press Play again to force a clean configure. |

## Next steps

- [Creating Scripts](creating-scripts.md) — script types and editor workflow
- [Code Editor](../editor/code-editor.md) — editing C++ in the editor and reading build output
- [Export Window](../editor/export.md) — building standalone projects outside the editor
