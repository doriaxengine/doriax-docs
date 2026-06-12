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

## See also

- [Mesh — receiveIBL](mesh.md#receiveibl)
- [Texture — cube maps](texture.md)
- [Properties — Sky component](../../editor/properties.md#sky-component)
