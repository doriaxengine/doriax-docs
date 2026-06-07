---
description: Targeting the web (HTML5) with Doriax using Emscripten.
---

# Building for HTML5

Doriax can export to the **web** (HTML5) using [Emscripten](https://emscripten.org/),
producing JavaScript and WebAssembly output that runs in the browser.

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
