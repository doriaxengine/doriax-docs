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
| [`customShader`](#customshader) | C++ \| Lua |

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

## Method details

---

### customShader

* *Setter:* `void setCustomShader(const std::string& path)`
* *Getter:* `std::string getCustomShader() const`

Project-relative base path of a forked shader (`"shaders/glow"` resolves to `shaders/glow.vert` and `shaders/glow.frag`, or `"a.vert|b.frag"` names the files separately). Empty (default) uses the scene default shader for this type, or the engine built-in. Changing it reloads the component. Same semantics as [Mesh.customShader](mesh.md#customshader); see [Custom Shaders](../../editor/custom-shaders.md).

---

### setShaderUniform

* `void setShaderUniform(const std::string& name, const Vector4& value)`
* `void setShaderUniform(const std::string& name, const Vector3& value)`
* `void setShaderUniform(const std::string& name, const Vector2& value)`
* `void setShaderUniform(const std::string& name, float value)`
* `Vector4 getShaderUniform(const std::string& name) const`
* `bool removeShaderUniform(const std::string& name)`

Values for the members of the custom shader's `u_vs_customParams` / `u_fs_customParams` blocks, by member name. Setting a value only rewrites the uploaded block, so it can run every frame; a member with no value reads zero, and `time` (seconds since startup) and `resolution` (render target size) are reserved for the engine. Same semantics as [Mesh.setShaderUniform](mesh.md#setshaderuniform); see [Custom Shaders — Shader uniforms](../../editor/custom-shaders.md#shader-uniforms).

=== "C++"

    ```cpp
    polygon.setCustomShader("shaders/glow");
    polygon.setShaderUniform("strength", 0.8f);
    polygon.setShaderUniform("glowColor", Vector4(1.0f, 0.8f, 0.2f, 1.0f));
    ```

=== "Lua"

    ```lua
    polygon.customShader = "shaders/glow"
    polygon:setShaderUniform("strength", 0.8)
    polygon:setShaderUniform("glowColor", Vector4(1, 0.8, 0.2, 1))
    ```
