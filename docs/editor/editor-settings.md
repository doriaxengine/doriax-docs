---
description: The Editor Settings dialog — build toolchain, Emscripten SDK, default export directory, and other machine-local editor preferences.
---

# Editor Settings

**Edit → Editor Settings** holds the settings that belong to *this machine* rather than
to the project: where your compiler and SDKs are, where exports go by default, and how
the editor itself renders. They are saved to the editor's `settings.yaml`, never to
`project.yaml`, so they are not shared through version control and a teammate opening
the same project keeps their own toolchain.

Anything the game itself carries — application identity, canvas, window, directories,
per-platform settings — is in [Project Settings](project-settings.md) instead.

The dialog is a modal with four tabs and an **OK** / **Cancel** footer.

## General

| Setting | Default | Effect |
| --- | --- | --- |
| **Default Export Directory** | Not set | Pre-fills the output folder in the Export Window for projects that have no remembered export directory yet |
| **Editor VSync** | Enabled | VSync for the editor's own frames |

The default export directory is only a starting point: once you export a project, the
folder you actually used is remembered per project *and per export mode*, and that
remembered value wins the next time you open the Export Window.

**Editor VSync** covers editing frames only. While a scene is running, frames follow the
project's own [VSync](project-settings.md#window) setting instead, so the two never apply
at once. Toggling takes effect on the next frame with no restart, and an idle editor
waits on the window system either way, so disabling it does not make the editor spin.

## Desktop

The C++ toolchain used both when **playing** a scene with C++ scripts and when running a
**Desktop** export.

| Setting | Default | Effect |
| --- | --- | --- |
| **CMake** | Auto-detect | Path to the `cmake` executable. **Browse** validates the pick by running it, and reports a folder with no working CMake instead of storing it. **Auto** returns to looking it up on `PATH` |
| **Compiler** | Default | The compiler kit used to build C++ scripts |

The **Compiler** dropdown lists the kits the editor detected (GCC, Clang, MSVC/Visual
Studio), each paired with a compatible CMake generator, and shows the resolved C and C++
compiler paths under the selection. Kits that cannot work are listed greyed out — hover
one to read why. **Default** leaves the toolchain to CMake on Linux and macOS; on Windows
it resolves to the best ABI-compatible detected kit, because a bare `cmake` there can
pick a toolchain that cannot link the editor's engine.

If the kit stored for a project is no longer detected — a compiler that was uninstalled,
or a project that came from another machine — the dropdown falls back to **Default** and
warns that builds still use the stored kit until you press OK.

!!! note "The compiler is stored per project, and remembered for new ones"
    Each project keeps its own kit, so a project that needs MSVC and one that needs
    MinGW can coexist. The kit you last chose also becomes the default for projects
    opened afterwards that have none, so in practice you set it once.

See [C++ Build Setup](../manual/cpp-build-setup.md) for what each toolchain requires, the
Windows ABI rules, and how to read a failing build.

## Web

| Setting | Default | Effect |
| --- | --- | --- |
| **Emscripten SDK** | Auto-detect | Root of your `emsdk` installation, used by **Web** exports. **Auto** returns to detecting it from the `EMSDK` environment variable or `emcmake` on `PATH` |
| **Status** | — | Whether the SDK was found, and where |

The status line updates as soon as you pick a folder, so you can confirm the SDK before
leaving the dialog. See [Building for HTML5](../building/html5.md) for installing the SDK.

## Advanced

**Clear Shader Cache** deletes the compiled-shader cache shared by every project on this
editor version. Shaders are rebuilt on demand afterwards, so the only cost is the next
build being slower. The button is disabled while a scene is playing.

## Where the values are stored

All of it goes to the editor's `settings.yaml`, beside `editor.log` — the
[FAQ](../about/faq.md#where-can-i-find-the-editor-crash-log) lists the per-platform path.

| Key | Holds |
| --- | --- |
| `cmake.path` | The CMake executable override |
| `emsdk.path` | The Emscripten SDK override |
| `export.default_dir` | The default export directory |
| `project_builds` | Per project: compiler kit and parallel build jobs, keyed by the absolute path of its `project.yaml` |
| `project_exports` | Per project and export mode: the last output directory used |

The per-project entries are keyed by path, so moving a project through **Save Project
As** re-keys them and your toolchain choice follows the project on this machine.

!!! note "Build jobs are edited in the Export Window"
    The parallel job count lives in the same `project_builds` entry as the compiler, but
    it is edited in the Export Window's **Desktop** mode as **Build Jobs**. The value
    applies to Play builds too. See
    [Parallel builds](../manual/cpp-build-setup.md#parallel-builds).

## Migrating from older projects

Editors before this dialog kept the compiler kit and job count in `project.yaml` as
`cmakeCCompiler`, `cmakeCxxCompiler`, `cmakeGenerator` and `cmakeBuildJobs`. Opening such
a project copies those values into `project_builds` once, and never over an entry this
machine already has. The keys stay in the old file until the project is saved again, so
an older editor can still read it.

## See also

- [Project Settings](project-settings.md) — the per-project counterpart
- [C++ Build Setup](../manual/cpp-build-setup.md) — toolchain requirements and troubleshooting
- [Export Window](export.md) — where the SDK and toolchain settings are used
