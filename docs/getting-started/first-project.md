---
description: Create your first Doriax scene and run it, using either Lua or C++.
---

# Your First Project

This walkthrough creates a simple scene and runs it. The same approach works on every
platform Doriax targets.

## Create a project

Open the Doriax editor and create a new project. The editor scaffolds the project
structure for you, including a scene, an assets folder, and entry-point scripts for
Lua and C++.

A typical project contains:

- 📁 **assets** — textures, models, audio, and other resources
- 📁 **scripts** — your Lua and/or C++ game code
- 📄 a **scene** file that the editor edits visually

## Add an entity

In the editor's **Scene** panel, create a new entity and give it a visual component —
for example a sprite (2D) or a box/model (3D). Use the **Inspector** to set its
position, rotation, scale, and other properties.

You can do the same thing in code. The examples below create a colored triangle.

=== "Lua"

    ```lua
    -- main.lua
    scene = Scene()
    triangle = Polygon(scene)

    triangle:addVertex(0, -100)
    triangle:addVertex(-50, 50)
    triangle:addVertex(50, 50)

    triangle.position = Vector3(300, 300, 0)
    triangle:setColor(0.6, 0.2, 0.6, 1)

    Engine.setCanvasSize(1000, 480)
    Engine.setScene(scene)
    ```

=== "C++"

    ```cpp
    // main.cpp
    #include "Doriax.h"
    using namespace Doriax;

    #include "Polygon.h"

    Scene scene;
    Polygon triangle(&scene);

    void init() {
        triangle.addVertex(0, -100);
        triangle.addVertex(-50, 50);
        triangle.addVertex(50, 50);

        triangle.setPosition(Vector3(300, 300, 0));
        triangle.setColor(0.6, 0.2, 0.6, 1);

        Engine::setCanvasSize(1000, 480);
        Engine::setScene(&scene);
    }
    ```

In C++, the engine calls your `init()` function when the game starts. In Lua, the main
script runs at startup and can require other Lua files.

!!! warning "Mixing Lua and C++ entry points"
    If both Lua and C++ call `Engine.setScene()` / `Engine::setScene()`, the C++ call
    runs last and the Lua scene will not be used. Use the `NO_CPP_INIT` or
    `NO_LUA_INIT` build option to disable the entry point you don't want. See
    [Building](../building/overview.md) for details.

## Run the project

Press **Play** in the editor to run the scene immediately. You should see your
triangle (or entity) rendered on screen.

When building from source instead of using the editor's play mode, build and install
the project first, then run the produced executable from the install directory's
`bin/` folder. After changing code, build and install again.

## Next steps

<div class="dx-cards" markdown>

<a class="dx-card" href="../the-editor/">
<p class="dx-card-title">The Editor →</p>
<p class="dx-card-desc">Tour the editor's panels and tools.</p>
</a>

<a class="dx-card" href="../../manual/scenes-and-entities/">
<p class="dx-card-title">Scenes &amp; Entities →</p>
<p class="dx-card-desc">Learn how scenes and entities are structured.</p>
</a>

</div>
