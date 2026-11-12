---
description: Lines API reference (C++ and Lua).
---

# Lines

**Inherits:** [Object](object.md)  
**C++ type:** `Lines`

## Description

Renders a collection of 3D line segments. Useful for debug overlays, grids, trajectory paths, and other wireframe visuals. Each line is defined by two endpoints and an optional per-endpoint colour for gradient lines.

The `Lines` object maintains an internal dynamic buffer. Call `updateLines()` after modifying line data to upload changes to the GPU.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| unsigned int | [maxLines](#maxlines) | `100` | C++ \| Lua |
| string | [shader](#shader) | `""` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [load](#load) | C++ |
| void | [addLine](#addline) | C++ \| Lua |
| [LineData](linedata.md) | [getLine](#getline) | C++ \| Lua |
| void | [updateLine](#updateline) | C++ \| Lua |
| void | [removeLine](#removeline) | C++ \| Lua |
| void | [updateLines](#updatelines) | C++ \| Lua |
| size_t | [getNumLines](#getnumlines) | C++ \| Lua |
| void | [clearLines](#clearlines) | C++ \| Lua |
| void | [setShaderUniform](#setshaderuniform) | C++ \| Lua |
| Vector4 | [getShaderUniform](#setshaderuniform) | C++ \| Lua |
| bool | [removeShaderUniform](#setshaderuniform) | C++ \| Lua |
| void | [setShaderTexture](#setshadertexture) | C++ \| Lua |
| Texture | [getShaderTexture](#setshadertexture) | C++ \| Lua |
| [LinesComponent](linescomponent.md) | `getLinesComponent` | Lua |

## Property details

### maxLines

* *Setter*: void **setMaxLines**(unsigned int maxLines)
* *Getter*: unsigned int **getMaxLines**() const

Pre-allocates buffer space for this many lines. Resize before calling `load()` for best performance.

---

## Method details

### load

* bool **load**()

Explicitly initialises the GPU buffer. This method is **C++ only** and is normally
optional because the render system initialises lines automatically.

---

### addLine

Several overloads are available:

* void **addLine**([LineData](linedata.md) line)
* void **addLine**(Vector3 pointA, Vector3 pointB)
* void **addLine**(Vector3 pointA, Vector3 pointB, Vector3 color)
* void **addLine**(Vector3 pointA, Vector3 pointB, Vector4 color)
* void **addLine**(Vector3 pointA, Vector3 pointB, Vector4 colorA, Vector4 colorB)

Adds a new line segment. The last overload lets each endpoint have a different colour.

=== "C++"
    ```cpp
    Lines debug(&scene);
    debug.load();
    debug.addLine(Vector3(0,0,0), Vector3(1,0,0), Vector4(1,0,0,1));  // red X axis
    debug.addLine(Vector3(0,0,0), Vector3(0,1,0), Vector4(0,1,0,1));  // green Y axis
    debug.addLine(Vector3(0,0,0), Vector3(0,0,1), Vector4(0,0,1,1));  // blue Z axis
    debug.updateLines();
    ```

=== "Lua"
    ```lua
    local debug = Lines(scene)
    debug:addLine(Vector3(0,0,0), Vector3(1,0,0), Vector4(1,0,0,1))
    debug:addLine(Vector3(0,0,0), Vector3(0,1,0), Vector4(0,1,0,1))
    debug:addLine(Vector3(0,0,0), Vector3(0,0,1), Vector4(0,0,1,1))
    debug:updateLines()
    ```

---

### getLine

* [LineData](linedata.md)& **getLine**(size_t index)

Returns a reference to the [LineData](linedata.md) at the given index. Modify in-place then call `updateLines()`.

---

### updateLine

* void **updateLine**(size_t index, ...)

Overwrites an existing line's endpoints and/or colour. Multiple overloads mirror `addLine()`. Call `updateLines()` afterwards.

---

### removeLine

* void **removeLine**(size_t index)

Removes the line at `index`. All subsequent indices shift down.

---

### updateLines

* void **updateLines**()

Uploads all pending line changes to the GPU. Must be called after any `addLine`, `updateLine`, or `removeLine` call.

---

### getNumLines

* size_t **getNumLines**()

Returns the current number of line segments.

---

### clearLines

* void **clearLines**()

Removes all line segments.

---

### shader

* *Setter:* `void setShader(const std::string& path)`
* *Getter:* `std::string getShader() const`

Project-relative path of the `lines` [shader file](../../manual/shader-files.md#ui-points-and-lines) (`.glsl`) or [shader graph](../../editor/shader-graphs.md) (`.shader`) the lines draw with, such as `"shaders/laser.glsl"`. Empty (default) uses the scene's [defaultLinesShader](scene.md#defaultlinesshader), or the engine built-in. Changing it reloads the component, and a shader that fails to build draws as the built-in one. See [Custom Shaders](../../editor/custom-shaders.md).

---

### setShaderUniform

* `void setShaderUniform(const std::string& name, const Vector4& value)`
* `void setShaderUniform(const std::string& name, const Vector3& value)`
* `void setShaderUniform(const std::string& name, const Vector2& value)`
* `void setShaderUniform(const std::string& name, float value)`
* `Vector4 getShaderUniform(const std::string& name) const`
* `bool removeShaderUniform(const std::string& name)`

Values of the parameters the [shader](#shader) declares with `#pragma param`, by name. Setting a value only rewrites the uploaded block, so it can run every frame; a parameter with no value reads the scene's value under a [scene default shader](scene.md#setdefaultshaderuniform), else its declared default. Same semantics as [Mesh.setShaderUniform](mesh.md#setshaderuniform); see [Custom Shaders — Shader parameters](../../editor/custom-shaders.md#shader-parameters).

=== "C++"

    ```cpp
    lines.setShader("shaders/laser.glsl");
    lines.setShaderUniform("strength", 0.8f);
    lines.setShaderUniform("glowColor", Vector4(1.0f, 0.8f, 0.2f, 1.0f));
    ```

=== "Lua"

    ```lua
    lines.shader = "shaders/laser.glsl"
    lines:setShaderUniform("strength", 0.8)
    lines:setShaderUniform("glowColor", Vector4(1, 0.8, 0.2, 1))
    ```

---

### setShaderTexture

* `void setShaderTexture(const std::string& name, const Texture& texture)`
* `Texture getShaderTexture(const std::string& name) const`

Sets a texture parameter the [shader](#shader) declares with `#pragma param texture2D` or `textureCube`, by name (see [Textures](../../manual/shader-files.md#textures)). An empty [Texture](texture.md) draws the declared default. Changing it reloads the component. `getShaderTexture` returns the texture set, empty when none.

=== "C++"

    ```cpp
    lines.setShaderTexture("noise", Texture("textures/noise.png"));
    ```

=== "Lua"

    ```lua
    lines:setShaderTexture("noise", Texture("textures/noise.png"))
    ```
