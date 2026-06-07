---
description: Scripting your game in Doriax with Lua or C++.
---

# Scripting

Doriax supports two scripting languages: **Lua** for fast iteration and flexible
scripting, and **C++** for full native performance. You can use either one or combine
both in the same project.

## Lua vs. C++

| | Lua | C++ |
| --- | --- | --- |
| Iteration speed | Very fast — no recompile needed | Requires a build step |
| Runtime performance | High | Maximum (native) |
| Compilation | Interpreted at runtime | Compiled at **build time** |
| Best for | Gameplay logic, prototyping, glue code | Performance-critical systems |

A common workflow is to prototype in Lua, then move hot paths to C++ when you need the
extra performance.

## Entry points

Each project has entry points for both languages:

- **C++** — the engine calls your `init()` function when the game starts.
- **Lua** — the main Lua script runs at startup and can require other Lua files.

=== "Lua"

    ```lua
    -- main.lua
    scene = Scene()
    -- build your scene here
    Engine.setScene(scene)
    ```

=== "C++"

    ```cpp
    // main.cpp
    #include "Doriax.h"
    using namespace Doriax;

    Scene scene;

    void init() {
        // build your scene here
        Engine::setScene(&scene);
    }
    ```

!!! warning "Choosing one entry point"
    If both Lua and C++ call `setScene()`, the C++ call runs last and overrides the Lua
    one. To disable an entry point, build with `NO_CPP_INIT` or `NO_LUA_INIT`:

    - **CMake:** add `-DNO_CPP_INIT=1` (or `-DNO_LUA_INIT=1`) to your configure step.

    See [Building](../building/overview.md) for full details.

## The Engine API

The static `Engine` object is your main entry into the runtime. Common calls include:

```lua
Engine.setCanvasSize(1000, 480)   -- set the rendering canvas size
Engine.setScene(scene)            -- set the active scene
```

The same methods are available in C++ through `Engine::` static methods.

## Next steps

Continue with [2D Graphics](2d-graphics.md) or [3D Graphics](3d-graphics.md) to start
drawing on screen.
