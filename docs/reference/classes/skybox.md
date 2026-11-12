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
| [`shader`](#shader) | C++ \| Lua |

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
| [`setShaderTexture`](#setshadertexture) | C++ \| Lua |
| [`getShaderTexture`](#setshadertexture) | C++ \| Lua |
| `getSkyComponent` ([SkyComponent](skycomponent.md)) | Lua |

## Example

=== "C++"

    ```cpp
    SkyBox sky(&scene);
    // faces in +X, -X, +Y, -Y, +Z, -Z order
    sky.setTextures(
        "sky/px.png", "sky/nx.png",
        "sky/py.png", "sky/ny.png",
        "sky/pz.png", "sky/nz.png");
    sky.setRotation(15.0f);
    ```

=== "Lua"

    ```lua
    local sky = SkyBox(scene)
    -- faces in +X, -X, +Y, -Y, +Z, -Z order
    sky:setTextures(
        "sky/px.png", "sky/nx.png",
        "sky/py.png", "sky/ny.png",
        "sky/pz.png", "sky/nz.png")
    sky.rotation = 15
    ```

Enable **Receive IBL** on meshes that should reflect this environment. See
[Rendering Pipeline — IBL](../../manual/rendering-pipeline.md#image-based-lighting-ibl).

## Method details

---

### shader

* *Setter:* `void setShader(const std::string& path)`
* *Getter:* `std::string getShader() const`

Project-relative path of the `sky` [shader file](../../manual/shader-files.md#sky) (`.glsl`) or [shader graph](../../editor/shader-graphs.md) (`.shader`) the sky draws with, such as `"shaders/dayNight.glsl"`. Its `getColor` hook receives the cube map sample times the sky's color and returns the color drawn. Empty (default) uses the scene's [defaultSkyShader](scene.md#defaultskyshader), or the engine built-in. Changing it reloads the component, and a shader that fails to build draws as the built-in one. See [Custom Shaders](../../editor/custom-shaders.md).

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
    sky.setShader("shaders/dayNight.glsl");
    sky.setShaderUniform("strength", 0.8f);
    sky.setShaderUniform("glowColor", Vector4(1.0f, 0.8f, 0.2f, 1.0f));
    ```

=== "Lua"

    ```lua
    sky.shader = "shaders/dayNight.glsl"
    sky:setShaderUniform("strength", 0.8)
    sky:setShaderUniform("glowColor", Vector4(1, 0.8, 0.2, 1))
    ```

---

### setShaderTexture

* `void setShaderTexture(const std::string& name, const Texture& texture)`
* `Texture getShaderTexture(const std::string& name) const`

Sets a texture parameter the [shader](#shader) declares with `#pragma param texture2D` or `textureCube`, by name (see [Textures](../../manual/shader-files.md#textures)). An empty [Texture](texture.md) draws the declared default. Changing it reloads the component. `getShaderTexture` returns the texture set, empty when none.

=== "C++"

    ```cpp
    sky.setShaderTexture("clouds", Texture("textures/clouds.png"));
    ```

=== "Lua"

    ```lua
    sky:setShaderTexture("clouds", Texture("textures/clouds.png"))
    ```

## See also

- [Shader Files — Sky](../../manual/shader-files.md#sky)
- [Custom Shaders — Shader parameters](../../editor/custom-shaders.md#shader-parameters)
- [Mesh — receiveIBL](mesh.md#receiveibl)
- [Texture — cube maps](texture.md)
- [Properties — Sky component](../../editor/properties.md#sky-component)
