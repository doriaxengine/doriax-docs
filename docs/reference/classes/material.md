---
description: Material API reference (C++ writable; Lua read-only).
---

# Material

**C++ type:** `Material` (struct)

## Description

A PBR (Physically Based Rendering) material definition that drives how a mesh surface looks under lighting. `Material` is a plain data struct — it holds colour factors, metallic/roughness values, and up to five texture slots that correspond to the standard glTF 2.0 PBR workflow.

Materials are attached to [Mesh](mesh.md) objects (or individual sub-meshes) via `Mesh::setMaterial()`. When loading a [Model](model.md), each sub-mesh automatically receives the material defined in the source file.

!!! note "Lua binding is read-only"
    Lua can read material fields from `mesh:getMaterial()`, but there is no
    `Material()` constructor and fields cannot be assigned from Lua. Create or edit
    materials in C++, or use editor `.material` files and mesh colour helpers like
    `mesh:setColor(...)`.

### Material files (`.material`)

In the editor, materials can be saved as standalone **`.material`** YAML files and
**linked** from multiple mesh submeshes. All linked meshes read from the same file, so
one edit updates every user of that material.

| Task | Editor workflow |
| --- | --- |
| Create a file | Drag the material preview from Properties into the Resources Browser |
| Apply to a mesh | Drag the `.material` file onto a mesh in the Scene view or onto the Material row in Properties |
| Share across meshes | Link each submesh to the same file |
| Break the link | Click the unlink button next to the material name in Properties |

Linked materials reload when the file changes on disk. See
[Resources Browser — Material files](../../editor/resources.md#material-files).

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| Vector4 | [baseColorFactor](#basecolorfactor) | `(1,1,1,1)` | C++ \| Lua (read-only) |
| float | [metallicFactor](#metallicfactor-roughnessfactor) | `1.0` | C++ \| Lua (read-only) |
| float | [roughnessFactor](#metallicfactor-roughnessfactor) | `1.0` | C++ \| Lua (read-only) |
| MaterialAlphaMode | [alphaMode](#alphamode-alphacutoff) | `AUTO` | C++ \| Lua (read-only) |
| float | [alphaCutoff](#alphamode-alphacutoff) | `0.5` | C++ \| Lua (read-only) |
| Vector3 | [emissiveFactor](#emissivefactor) | `(0,0,0)` | C++ \| Lua (read-only) |
| [Texture](texture.md) | [baseColorTexture](#basecolortexture) | empty | C++ \| Lua (read-only) |
| [Texture](texture.md) | [emissiveTexture](#emissivetexture) | empty | C++ \| Lua (read-only) |
| [Texture](texture.md) | [metallicRoughnessTexture](#metallicroughnesstexture) | empty | C++ \| Lua (read-only) |
| [Texture](texture.md) | [occlusionTexture](#occlusiontexture) | empty | C++ \| Lua (read-only) |
| [Texture](texture.md) | [normalTexture](#normaltexture) | empty | C++ \| Lua (read-only) |
| std::string | [name](#name) | `""` | C++ |

## Property details

### baseColorFactor

The base linear-space RGBA colour multiplied with `baseColorTexture`. When no texture is assigned, this is the solid colour of the surface. How the combined alpha is interpreted depends on [alphaMode](#alphamode-alphacutoff).

=== "C++"
    ```cpp
    Material mat;
    mat.baseColorFactor = Vector4(1.0f, 0.0f, 0.0f, 1.0f);  // solid red
    mesh.setMaterial(mat);
    ```

=== "Lua"
    ```lua
    -- Materials cannot be constructed or mutated from Lua yet.
    -- Prefer editor .material files, or tint with mesh:setColor(...).
    mesh:setColor(Vector4(1.0, 0.0, 0.0, 1.0))
    ```

---

### alphaMode / alphaCutoff

`alphaMode` controls how the combined alpha from `baseColorFactor.a` and the base-colour
texture is rendered:

| Mode | Behaviour |
| --- | --- |
| `MaterialAlphaMode::AUTO` | Legacy Doriax behaviour. `autoTransparency` selects the transparent pass when the texture or base-colour factor contains transparency. The submesh's **Texture Shadow** option remains a manual cutout control. |
| `MaterialAlphaMode::ALPHA_OPAQUE` | Ignores material alpha and renders every surviving fragment fully opaque. |
| `MaterialAlphaMode::MASK` | Discards fragments whose combined alpha is below `alphaCutoff`; surviving fragments are fully opaque. |
| `MaterialAlphaMode::BLEND` | Preserves alpha for conventional transparency and selects the transparent pass when `autoTransparency` is enabled. |

`alphaCutoff` is used only by `MASK` and defaults to `0.5`. The same combined-alpha
test is used by the lit pass, shadow/depth pass, and SSR G-buffer, so the visible
surface, its shadow, and screen-space effects keep the same silhouette.

```cpp
Material leaves;
leaves.baseColorTexture = Texture("textures/leaves.png");
leaves.alphaMode = MaterialAlphaMode::MASK;
leaves.alphaCutoff = 0.35f;
mesh.setMaterial(leaves);
```

Alpha-mode materials must be authored in C++ or as editor `.material` files; Lua cannot
construct or mutate `Material` instances.

GLTF/GLB loading maps the source material's `OPAQUE`, `MASK`, or `BLEND` mode directly
onto `MaterialAlphaMode::ALPHA_OPAQUE`, `MASK`, and `BLEND`.
Editor-created materials default to `AUTO` for compatibility with older projects.

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
    -- Read an existing material; assignment is not supported from Lua.
    local mat = mesh:getMaterial()
    Log.print("Base color factor: " .. tostring(mat.baseColorFactor))
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
