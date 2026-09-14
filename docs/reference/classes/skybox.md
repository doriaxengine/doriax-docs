---
description: SkyBox API reference (C++ and Lua).
---

# SkyBox

**Inherits:** [EntityHandle](entityhandle.md)  
**C++ type:** `SkyBox`

Cubemap sky rendering and the source environment for **image-based lighting (IBL)**.

When a Sky entity has a valid cubemap texture, the engine generates irradiance and
prefiltered specular environment maps from it. Meshes with **Receive IBL** enabled on
their Mesh component use those maps for reflections and indirect diffuse lighting.

## Editor-only component fields

These are edited on the **Sky** component in the Properties window and serialized with
the scene (not yet exposed on the `SkyBox` script class):

| Field | Default | Purpose |
| --- | --- | --- |
| **visible** | `true` | Draw the sky background. When `false`, the sky is hidden but IBL maps are still built from the texture. |
| **texture** | — | Cubemap source (six faces or single file). |
| **color** | white | Linear RGBA tint. |
| **rotation** | `0` | Y-axis rotation in degrees. |

Use **Visible = false** for invisible HDR environments that only drive reflections.

## Properties

| Name | Languages |
| --- | --- |
| `color` | C++ \| Lua |
| `alpha` | C++ \| Lua |
| `rotation` | C++ \| Lua |
| [`customShader`](#customshader) | C++ \| Lua |

## Methods

| Name | Languages |
| --- | --- |
| `setTextures` | C++ \| Lua |
| `setTexture` | C++ \| Lua |
| `setTexturePositiveX` | C++ \| Lua |
| `setTextureNegativeX` | C++ \| Lua |
| `setTexturePositiveY` | C++ \| Lua |
| `setTextureNegativeY` | C++ \| Lua |
| `setTexturePositiveZ` | C++ \| Lua |
| `setTextureNegativeZ` | C++ \| Lua |
| `setColor` | C++ \| Lua |
| [`setShaderUniform`](#setshaderuniform) | C++ \| Lua |
| [`getShaderUniform`](#setshaderuniform) | C++ \| Lua |
| [`removeShaderUniform`](#setshaderuniform) | C++ \| Lua |

## Example

=== "C++"

    ```cpp
    SkyBox sky(&scene);
    sky.setTextures("outdoor",
        "sky/px.png", "sky/nx.png",
        "sky/py.png", "sky/ny.png",
        "sky/pz.png", "sky/nz.png");
    sky.setRotation(15.0f);
    ```

=== "Lua"

    ```lua
    local sky = SkyBox(scene)
    sky:setTextures("outdoor",
        "sky/px.png", "sky/nx.png",
        "sky/py.png", "sky/ny.png",
        "sky/pz.png", "sky/nz.png")
    sky.rotation = 15
    ```

Enable **Receive IBL** on meshes that should reflect this environment. See
[Rendering Pipeline — IBL](../../manual/rendering-pipeline.md#image-based-lighting-ibl).

## Method details

---

### customShader

* *Setter:* `void setCustomShader(const std::string& path)`
* *Getter:* `std::string getCustomShader() const`

Project-relative base path of a forked shader (`"shaders/dayNight"` resolves to `shaders/dayNight.vert` and `shaders/dayNight.frag`, or `"a.vert|b.frag"` names the files separately). Empty (default) uses the scene default shader for this type, or the engine built-in. Changing it reloads the component. Same semantics as [Mesh.customShader](mesh.md#customshader); see [Custom Shaders](../../editor/custom-shaders.md).

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
    sky.setCustomShader("shaders/dayNight");
    sky.setShaderUniform("strength", 0.8f);
    sky.setShaderUniform("glowColor", Vector4(1.0f, 0.8f, 0.2f, 1.0f));
    ```

=== "Lua"

    ```lua
    sky.customShader = "shaders/dayNight"
    sky:setShaderUniform("strength", 0.8)
    sky:setShaderUniform("glowColor", Vector4(1, 0.8, 0.2, 1))
    ```

## See also

- [Custom Shaders — Shader uniforms](../../editor/custom-shaders.md#shader-uniforms)
- [Mesh — receiveIBL](mesh.md#receiveibl)
- [Texture — cube maps](texture.md)
- [Properties — Sky component](../../editor/properties.md#sky-component)
