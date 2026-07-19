---
description: Targeting the web (HTML5) with Doriax using Emscripten.
---

# Building for HTML5

Doriax can export to the **web** (HTML5) using [Emscripten](https://emscripten.org/),
producing JavaScript and WebAssembly output that runs in the browser.

!!! tip "Let the editor build it"
    The Export Window's **Web** mode runs this entire build for you — it locates the
    Emscripten SDK, compiles the project, and copies the `.html`/`.js`/`.wasm`/`.data`
    files to your destination folder. The manual steps below are for Source Code
    exports and custom setups. See [Export Window](../editor/export.md#web-mode).

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
contains `assets/` and `lua/` folders.

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
