---
description: Polygon API reference (C++ and Lua).
---

# Polygon

**Inherits:** [UILayout](uilayout.md)  
**C++ type:** `Polygon`

`Polygon` API exposed to Lua and C++ gameplay code.

## Properties

| Name | Languages |
| --- | --- |
| `color` | C++ \| Lua |
| `alpha` | C++ \| Lua |
| `flipY` | C++ \| Lua |
| [`shader`](#shader) | C++ \| Lua |

## Methods

| Name | Languages |
| --- | --- |
| `addVertex` | C++ \| Lua |
| `setColor` | C++ \| Lua |
| `setTexture` | C++ \| Lua |
| `getAABB` | C++ \| Lua |
| `getWorldAABB` | C++ \| Lua |
| [`setShaderUniform`](#setshaderuniform) | C++ \| Lua |
| [`getShaderUniform`](#setshaderuniform) | C++ \| Lua |
| [`removeShaderUniform`](#setshaderuniform) | C++ \| Lua |
| [`setShaderTexture`](#setshadertexture) | C++ \| Lua |
| [`getShaderTexture`](#setshadertexture) | C++ \| Lua |
| `getPolygonComponent` ([PolygonComponent](polygoncomponent.md)) | Lua |
| `getUIComponent` ([UIComponent](uicomponent.md)) | Lua |

## Method details

---

### shader

* *Setter:* `void setShader(const std::string& path)`
* *Getter:* `std::string getShader() const`

Project-relative path of the `ui` [shader file](../../manual/shader-files.md#ui-points-and-lines) (`.glsl`) or [shader graph](../../editor/shader-graphs.md) (`.shader`) the polygon draws with, such as `"shaders/glow.glsl"`. Empty (default) uses the scene's [defaultUIShader](scene.md#defaultuishader), or the engine built-in. Changing it reloads the component, and a shader that fails to build draws as the built-in one. It is the `shader` field of [UIComponent](uicomponent.md#shader); see [Custom Shaders](../../editor/custom-shaders.md).

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
    polygon.setShader("shaders/glow.glsl");
    polygon.setShaderUniform("strength", 0.8f);
    polygon.setShaderUniform("glowColor", Vector4(1.0f, 0.8f, 0.2f, 1.0f));
    ```

=== "Lua"

    ```lua
    polygon.shader = "shaders/glow.glsl"
    polygon:setShaderUniform("strength", 0.8)
    polygon:setShaderUniform("glowColor", Vector4(1, 0.8, 0.2, 1))
    ```

---

### setShaderTexture

* `void setShaderTexture(const std::string& name, const Texture& texture)`
* `Texture getShaderTexture(const std::string& name) const`

Sets a texture parameter the [shader](#shader) declares with `#pragma param texture2D` or `textureCube`, by name (see [Textures](../../manual/shader-files.md#textures)). An empty [Texture](texture.md) draws the declared default. Changing it reloads the component. `getShaderTexture` returns the texture set, empty when none.

=== "C++"

    ```cpp
    polygon.setShaderTexture("noise", Texture("textures/noise.png"));
    ```

=== "Lua"

    ```lua
    polygon:setShaderTexture("noise", Texture("textures/noise.png"))
    ```
