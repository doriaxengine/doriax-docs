---
description: Configure and build an exported Doriax project with one command using the doriax.py build script.
---

# Build Script (doriax.py)

`doriax.py` runs the CMake configure and build steps for a Doriax project in one command.
Every [Source Code export](../editor/export.md#source-code-mode) puts it in the export
root, next to `CMakeLists.txt`. The engine repository has it at `engine/doriax.py`,
where it builds `engine/project` by default.

!!! tip "Desktop and Web exports are already built"
    The Export Window's **Desktop** and **Web** modes compile the game for you. The
    script is for **Source Code** exports.

## Requirements

- Python 3.9 or newer
- [CMake](https://cmake.org/download/) 3.20 or newer, on `PATH`
- The toolchain of the target platform, see the [platform guides](overview.md#per-platform-guides)
- Optional: [Ninja](https://ninja-build.org/), used for Linux, macOS, and Web builds when
  it is on `PATH`

## Usage

From the export folder:

```bash
python3 doriax.py              # Release build for this computer
python3 doriax.py --debug      # Debug build
python3 doriax.py -g vulkan    # choose the graphics backend
python3 doriax.py -p web       # Emscripten build
```

On Windows, run it with `python` or `py`.

## Platforms

| `--platform` | Builds on | Generator | Output |
| --- | --- | --- | --- |
| `linux` | Linux | Ninja if installed | `build/linux/<App>` |
| `windows` | Windows | Newest Visual Studio | `build/windows/Release/<App>.exe` |
| `macos` | macOS | Ninja if installed | `build/macos/<App>` |
| `macos-xcode` | macOS | Xcode | `build/macos-xcode/Release/<App>.app` |
| `ios-xcode` | macOS | Xcode | `build/ios-xcode/Release-iphonesimulator/<App>.app` |
| `web` | Any | Ninja if installed | `build/web/<App>.html` |

The default is the computer's own platform. Desktop platforms build only on their own
operating system. `<App>` is the project name the export wrote into `CMakeLists.txt`, and
Debug builds use `Debug` instead of `Release` in the paths.

Android builds go through Gradle. Open the exported Android Studio workspace instead,
see [Building for Android](android.md).

## Options

| Option | Default | Effect |
| --- | --- | --- |
| `-p`, `--platform` | This computer | Target platform |
| `-d`, `--debug` / `--no-debug` | Release | Build type |
| `-b`, `--build` / `--no-build` | Build | `--no-build` only configures, for example to open the Xcode or Visual Studio project |
| `-g`, `--graphic-backend` | Platform default | `glcore`, `gles3`, `metal`, `d3d11`, or `vulkan`, see [Graphics backend](../reference/build-options.md#graphics-backend) |
| `-G`, `--generator` | See [Platforms](#platforms) | CMake generator |
| `-j`, `--jobs` | CPU cores | Parallel build jobs |
| `-D`, `--define` | | Extra CMake definition, repeatable: `-DEMSCRIPTEN_THREAD_SUPPORT=ON` |
| `-o`, `--output` | `build/<platform>` | Build directory |
| `-a`, `--appname` | From `CMakeLists.txt` | Executable name (`APP_NAME`) |
| `-s`, `--project` | `project/` | Project root (`PROJECT_ROOT`) |
| `-e`, `--doriax` | Script folder | Engine root with the engine `CMakeLists.txt` |
| `--no-cpp-init` / `--no-lua-init` | | Define `NO_CPP_INIT` / `NO_LUA_INIT`, see [Scripting entry options](../reference/build-options.md#scripting-entry-options) |
| `--em-shell-file` | | Emscripten `--shell-file` template for `web` |

The build directory keeps its generator and CMake cache between runs, including
`--graphic-backend`, `--appname`, and `-D` values. To start over, delete the build
directory.

## Web builds

The script finds `emcmake` in the `EMSDK`, `EMSCRIPTEN_ROOT`, or `EMSCRIPTEN` folder, or on
`PATH`. Running `emsdk_env` sets `EMSDK`.

An exported project also gets `<App>.export.html`, the page with the
[Web settings](../editor/project-settings.md#web) applied. Publish it (renamed to
`index.html` if you like) with `<App>.js`, `<App>.wasm`, and, when present, `<App>.data`
and `favicon.png`. Serve the files over HTTP as in [Building for HTML5](html5.md#3-run-it).

## Xcode builds

`macos-xcode` and `ios-xcode` generate `build/<platform>/<App>.xcodeproj`. CMake doesn't
put `assets/` and `lua/` into the app bundle, so the script adds them to the project's
resources after each configure. macOS `glcore` and `vulkan` builds are plain executables,
not bundles, so they skip this step.

`ios-xcode` builds for the iOS Simulator. For devices, see [Building for iOS](ios.md).
