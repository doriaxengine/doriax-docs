---
description: Targeting the web (HTML5) with Doriax using Emscripten.
---

# Building for HTML5

Doriax can export to the **web** (HTML5) using [Emscripten](https://emscripten.org/),
producing JavaScript and WebAssembly output that runs in the browser.

!!! tip "Let the editor build it"
    The Export Window's **Web** mode runs this entire build for you — it locates the
    Emscripten SDK, compiles the project, and copies `index.html` and the
    `.js`/`.wasm`/`.data` files to your destination folder, ready to upload. The manual
    steps below are for Source Code exports and custom setups. See
    [Export Window](../editor/export.md#web-mode).

    If the SDK is not on `PATH`, point the editor at your `emsdk` folder once in
    **Edit → [Editor Settings](../editor/editor-settings.md#web) → Web**.

## Page customization

The generated page is not fixed. **Project Settings → Platforms → Web** sets the page
title, a favicon, extra `<head>` markup, whether the canvas follows the browser window,
whether Emscripten's default logo, status line and console are hidden, and how many
pixels HiDPI screens draw. For full control, supply a **Custom HTML Shell**: any HTML
file containing a `{{DORIAX_DEFAULT_HTML}}` marker, which the build replaces with the
page Emscripten generated. See [Web settings](../editor/project-settings.md#web).

## Game portals

To publish on a web game portal, pick it under **Project Settings → Platforms → Web →
Game Portal**: CrazyGames, Poki, GameDistribution, Yandex Games or YouTube Playables.
The export builds that portal's SDK in for the
[`WebPortal`](../reference/classes/webportal.md) class, so each portal needs its own
export. A build configured by hand takes the same choice as
[`-DDORIAX_WEB_PORTAL=poki`](../reference/build-options.md#runtime-project-options),
plus `-DDORIAX_WEB_PORTAL_GAME_ID=<id>` for GameDistribution. See
[Monetization → Web portals](../manual/monetization.md#web-portals) for the API and for
testing each portal on `localhost`.

## Screen density

On phones and HiDPI monitors one CSS pixel covers several device pixels. The game draws
at the device's resolution, up to the **Max Pixel Ratio** of the
[Web settings](../editor/project-settings.md#web), which is 2 by default. A canvas that
is 800×360 on the page of a phone with three device pixels per CSS pixel is drawn at
1600×720. Input coordinates and
[`System::getScreenWidth`](../reference/classes/system.md#getscreenwidth-getscreenheight)
follow that size, so canvas scaling works as on any other screen. Lower the setting when
a GPU-heavy game runs slowly on such screens. A build configured by hand takes it as
[`-DDORIAX_WEB_MAX_PIXEL_RATIO=1.5`](../reference/build-options.md#runtime-project-options).

The drawing size follows the size the canvas has on the page, so a custom shell only
needs to style the canvas with CSS. With **Resize Canvas To Window** off and no CSS of
your own, the canvas has the project's window size.

## Hidden pages

The game pauses while its page is hidden: another tab in front, the browser minimized,
or the phone locked. Sounds pause with it and
[`Engine::onPause`](../reference/classes/engine.md#onpause) fires.
[`Engine::onResume`](../reference/classes/engine.md#onresume) follows when the page
shows again. A YouTube Playables export leaves this to YouTube, which pauses the game
itself.

## 1. Install Emscripten

Download and install the Emscripten SDK by following the official
[installation instructions](https://emscripten.org/docs/getting_started/downloads.html).

After installation, make the SDK available in your environment:

=== "Linux / macOS"

    ```bash
    source <path-to-emsdk>/emsdk_env.sh
    ```

=== "Windows"

    Install [CMake](https://cmake.org/download/) and a compatible toolchain, and ensure
    both `cmake` and the Emscripten tools are on your `PATH`. Test with:

    ```bat
    cmake --version
    emcc --version
    ```

    Emscripten builds on Windows with Ninja, not with Visual Studio. The editor and
    `doriax.py` take Ninja from `PATH`, or else the one the **C++ CMake tools for Windows**
    component of Visual Studio installs. Without it, install
    [Ninja](https://ninja-build.org) and add it to `PATH`.

## 2. Build the web target

Configure and build using the Emscripten toolchain. The output is a set of `.js`,
`.wasm`, and `.html` files for your project.

```bash
emcmake cmake -S engine -B build-web -G "Ninja" \
    -DPROJECT_ROOT=/path/to/project \
    -DCMAKE_BUILD_TYPE=Release
cmake --build build-web --config Release --target doriax-project
```

The runtime selects the `gles3` graphics backend and Emscripten app backend for web
builds. Assets and Lua files are preloaded into the virtual filesystem when the project
contains `assets/` and `lua/` folders. The experimental Native Resource Pack setting does
not apply to Web mode — Emscripten still emits its `.data` bundle from the loose folders.
Leave packing off if you export Source Code and then run this Emscripten build yourself.

In a Source Code export, `python3 doriax.py -p web` finds the SDK and runs both commands.
See [Build Script — Web builds](build-script.md#web-builds).

## Thread support

Thread support is disabled by default for Emscripten builds. Enable it only when your
hosting environment supports the required cross-origin isolation headers:

```bash
emcmake cmake -S engine -B build-web -G "Ninja" \
    -DPROJECT_ROOT=/path/to/project \
    -DEMSCRIPTEN_THREAD_SUPPORT=ON
```

Web builds use memory growth and start with a 256 MB initial memory configuration.

## 3. Run it

Opening the generated `.html` file directly from the filesystem can trigger browser
security errors. Serve it over HTTP instead:

```bash
python3 -m http.server
```

Then open <http://127.0.0.1:8000> in your browser.

!!! note "Tooling is being refreshed"
    The web export pipeline is being updated under the Doriax name. Some steps may still
    reference the legacy Supernova layout while the transition completes. Check the
    [repository](https://github.com/doriaxengine/doriax) for the latest workflow.
