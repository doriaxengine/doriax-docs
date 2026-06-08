---
description: Material API reference (C++ and Lua).
---

# Material

**C++ type:** `Material` (struct)

## Description

A PBR (Physically Based Rendering) material definition that drives how a mesh surface looks under lighting. `Material` is a plain data struct — it holds colour factors, metallic/roughness values, and up to five texture slots that correspond to the standard glTF 2.0 PBR workflow.

Materials are attached to [Mesh](mesh.md) objects (or individual sub-meshes) via `Mesh::setMaterial()`. When loading a [Model](model.md), each sub-mesh automatically receives the material defined in the source file.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| Vector4 | [baseColorFactor](#basecolorfactor) | `(1,1,1,1)` | C++ \| Lua |
| float | [metallicFactor](#metallicfactor-roughnessfactor) | `1.0` | C++ \| Lua |
| float | [roughnessFactor](#metallicfactor-roughnessfactor) | `1.0` | C++ \| Lua |
| Vector3 | [emissiveFactor](#emissivefactor) | `(0,0,0)` | C++ \| Lua |
| [Texture](texture.md) | [baseColorTexture](#basecolortexture) | empty | C++ \| Lua |
| [Texture](texture.md) | [emissiveTexture](#emissivetexture) | empty | C++ \| Lua |
| [Texture](texture.md) | [metallicRoughnessTexture](#metallicroughnesstexture) | empty | C++ \| Lua |
| [Texture](texture.md) | [occlusionTexture](#occlusiontexture) | empty | C++ \| Lua |
| [Texture](texture.md) | [normalTexture](#normaltexture) | empty | C++ \| Lua |
| std::string | [name](#name) | `""` | C++ \| Lua |

## Property details

### baseColorFactor

The base linear-space RGBA colour multiplied with `baseColorTexture`. When no texture is assigned, this is the solid colour of the surface. Alpha below `1.0` makes the surface semi-transparent (requires [transparent](mesh.md#transparent-autotransparency) on the mesh).

=== "C++"
    ```cpp
    Material mat;
    mat.baseColorFactor = Vector4(1.0f, 0.0f, 0.0f, 1.0f);  // solid red
    mesh.setMaterial(mat);
    ```

=== "Lua"
    ```lua
    local mat = Material()
    mat.baseColorFactor = Vector4(1.0, 0.0, 0.0, 1.0)
    mesh:setMaterial(mat)
    ```

---

### metallicFactor / roughnessFactor

Controls the PBR metallic-roughness workflow:

* **metallicFactor** (`0.0`–`1.0`) — `1.0` is a fully metallic surface (like polished steel), `0.0` is dielectric (like plastic or wood). Multiplied with the blue channel of `metallicRoughnessTexture`.
* **roughnessFactor** (`0.0`–`1.0`) — `0.0` is a mirror-like glossy surface, `1.0` is fully diffuse. Multiplied with the green channel of `metallicRoughnessTexture`.

---

### emissiveFactor

An additive linear-space RGB glow colour. The surface emits light of this colour independent of external lighting. Multiplied with `emissiveTexture` when present. Keep all channels at `0` (the default) to disable emission.

---

### baseColorTexture

A [Texture](texture.md) that modulates the `baseColorFactor`. The texture's RGBA channels are multiplied component-wise with `baseColorFactor`. Supports 2D textures loaded from file or created from pixel data.

=== "C++"
    ```cpp
    Material mat;
    mat.baseColorTexture = Texture("textures/ground_albedo.png");
    mesh.setMaterial(mat);
    ```

=== "Lua"
    ```lua
    local mat = Material()
    mat.baseColorTexture = Texture("textures/ground_albedo.png")
    mesh:setMaterial(mat)
    ```

---

### emissiveTexture

A [Texture](texture.md) whose RGB channels are multiplied with `emissiveFactor` to produce surface emission. Useful for glowing screens, neon signs, or lava surfaces.

---

### metallicRoughnessTexture

A [Texture](texture.md) encoding metallic information in the **blue channel** and roughness in the **green channel** (following the glTF 2.0 specification). The red channel is unused.

---

### occlusionTexture

A [Texture](texture.md) used for baked ambient-occlusion. The red channel is sampled to darken areas that receive less indirect light (crevices, seams). Scale is fixed at `1.0`.

---

### normalTexture

A tangent-space normal map [Texture](texture.md). Perturbs the surface normal per-pixel to simulate fine geometric detail without additional polygons.

---

### name

An optional human-readable identifier for the material, usually set automatically when loading a [Model](model.md) from a GLTF file. Can be used to look up or display material information at runtime.
