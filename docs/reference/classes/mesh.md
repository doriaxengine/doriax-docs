---
description: Mesh API reference — geometry, materials, shadows, transparency, and GPU instancing.
---

# Mesh

## Description

`Mesh` is the base class for all renderable 3D objects. It exposes the material system (color, texture, PBR material), shadow casting and receiving, transparency control, face culling, and GPU instancing for drawing thousands of objects in a single draw call.

**Inherits:** [Object](object.md) → [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Mesh mesh(&scene);
    mesh.setTexture("textures/crate.png");
    mesh.setColor(1.0f, 1.0f, 1.0f, 1.0f);
    mesh.setCastShadows(true);
    ```

=== "Lua"

    ```lua
    local mesh = Mesh(scene)
    mesh:setTexture("textures/crate.png")
    mesh:setColor(1, 1, 1, 1)
    mesh.castShadows = true
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| Vector4 | [color](#color) | `(1,1,1,1)` | C++ \| Lua |
| float | [alpha](#alpha) | `1.0` | C++ \| Lua |
| Material | [material](#material) | default | C++ \| Lua |
| [PrimitiveType](#primitivetype) | [primitiveType](#primitivetype_1) | `TRIANGLES` | C++ \| Lua |
| bool | [faceCulling](#faceculling) | `true` | C++ \| Lua |
| [CullingMode](#cullingmode) | cullingMode | `BACK` | C++ \| Lua |
| [WindingOrder](#windingorder) | windingOrder | `CCW` | C++ \| Lua |
| bool | receiveLights | `true` | C++ \| Lua |
| bool | receiveIBL | `false` | Editor / scene |
| bool | [castShadows](#castshadows-receiveshadows) | `false` | C++ \| Lua |
| bool | [receiveShadows](#castshadows-receiveshadows) | `false` | C++ \| Lua |
| bool | shadowsBillboard | `false` | C++ \| Lua |
| bool | castShadowsWithTexture | `false` | C++ \| Lua |
| bool | [transparent](#transparent-autotransparency) | `false` | C++ \| Lua |
| bool | [autoTransparency](#transparent-autotransparency) | `true` | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| bool | [load](#load) | C++ \| Lua |
| void | [setTexture](#settexture) | C++ \| Lua |
| void | [setColor](#color) | C++ \| Lua |
| Vector4 | [getColor](#color) | C++ \| Lua |
| void | [setAlpha](#alpha) | C++ \| Lua |
| float | [getAlpha](#alpha) | C++ \| Lua |
| void | [setMaterial](#material) | C++ \| Lua |
| Material | [getMaterial](#material) | C++ \| Lua |
| void | [setPrimitiveType](#primitivetype_1) | C++ \| Lua |
| PrimitiveType | [getPrimitiveType](#primitivetype_1) | C++ \| Lua |
| void | [setFaceCulling](#faceculling) | C++ \| Lua |
| bool | [isFaceCulling](#faceculling) | C++ \| Lua |
| void | setCullingMode | C++ \| Lua |
| CullingMode | getCullingMode | C++ \| Lua |
| void | setWindingOrder | C++ \| Lua |
| WindingOrder | getWindingOrder | C++ \| Lua |
| AABB | [getAABB](#getaabb-getverticesaabb-getworldaabb) | C++ \| Lua |
| AABB | [getVerticesAABB](#getaabb-getverticesaabb-getworldaabb) | C++ \| Lua |
| AABB | [getWorldAABB](#getaabb-getverticesaabb-getworldaabb) | C++ \| Lua |
| unsigned int | [getNumSubmeshes](#getnumsubmeshes) | C++ \| Lua |
| void | setReceiveLights | C++ \| Lua |
| bool | isReceiveLights | C++ \| Lua |
| void | [setCastShadows](#castshadows-receiveshadows) | C++ \| Lua |
| bool | [isCastShadows](#castshadows-receiveshadows) | C++ \| Lua |
| void | [setReceiveShadows](#castshadows-receiveshadows) | C++ \| Lua |
| bool | [isReceiveShadows](#castshadows-receiveshadows) | C++ \| Lua |
| void | setShadowsBillboard | C++ \| Lua |
| bool | isShadowsBillboard | C++ \| Lua |
| void | setCastShadowsWithTexture | C++ \| Lua |
| bool | isCastShadowsWithTexture | C++ \| Lua |
| void | [setTransparent](#transparent-autotransparency) | C++ \| Lua |
| bool | [isTransparent](#transparent-autotransparency) | C++ \| Lua |
| void | [setAutoTransparency](#transparent-autotransparency) | C++ \| Lua |
| bool | [isAutoTransparency](#transparent-autotransparency) | C++ \| Lua |
| void | [setAsMirror](#setasmirror-removemirror-ismirror) | C++ \| Lua |
| void | [removeMirror](#setasmirror-removemirror-ismirror) | C++ \| Lua |
| bool | [isMirror](#setasmirror-removemirror-ismirror) | C++ \| Lua |
| void | [createInstancedMesh](#createinstancedmesh) | C++ \| Lua |
| void | [removeInstancedMesh](#createinstancedmesh) | C++ \| Lua |
| bool | [hasInstancedMesh](#createinstancedmesh) | C++ \| Lua |
| void | [addInstance](#addinstance) | C++ \| Lua |
| InstanceData& | [getInstance](#addinstance) | C++ \| Lua |
| void | [updateInstance](#updateinstance) | C++ \| Lua |
| void | [removeInstance](#addinstance) | C++ \| Lua |
| bool | isInstanceVisible | C++ \| Lua |
| void | setInstanceVisible | C++ \| Lua |
| void | [updateInstances](#updateinstances) | C++ \| Lua |
| size_t | [getNumInstances](#createinstancedmesh) | C++ \| Lua |
| void | [clearInstances](#clearinstances) | C++ \| Lua |
| void | [setInstancedBillboard](#createinstancedmesh) | C++ \| Lua |
| bool | [isInstancedBillboard](#createinstancedmesh) | C++ \| Lua |
| void | [setInstancedCylindricalBillboard](#createinstancedmesh) | C++ \| Lua |
| bool | [isInstancedCylindricalBillboard](#createinstancedmesh) | C++ \| Lua |
| void | [setMaxInstances](#createinstancedmesh) | C++ \| Lua |
| unsigned int | [getMaxInstances](#createinstancedmesh) | C++ \| Lua |

## Enumerations

### PrimitiveType

* **TRIANGLES** — Solid triangle meshes (default).
* **TRIANGLE_STRIP** — Triangle strip.
* **POINTS** — Renders each vertex as a point.
* **LINES** — Renders edges as lines.

---

### CullingMode

* **BACK** — Culls back faces (default, outward-facing normals).
* **FRONT** — Culls front faces (useful for inside-out rendering).

---

### WindingOrder

* **CCW** — Counter-clockwise winding defines the front face (OpenGL convention, default).
* **CW** — Clockwise winding defines the front face.

## Property details

### color

* *Setter:* `void setColor(Vector4 color)`
* *Setter:* `void setColor(float red, float green, float blue, float alpha)`
* *Setter:* `void setColor(float red, float green, float blue)`
* *Getter:* `Vector4 getColor() const`

Tint color multiplied with the material texture. `(1,1,1,1)` means no tint.

---

### alpha

* *Setter:* `void setAlpha(float alpha)`
* *Getter:* `float getAlpha() const`

Shorthand for the alpha channel of [color](#color). Values below 1.0 require [transparent]( #transparent-autotransparency) to be enabled for correct rendering order.

---

### material

* *Setter:* `void setMaterial(const Material& material)` *(all submeshes)*
* *Setter:* `void setMaterial(unsigned int submesh, const Material& material)` *(per submesh)*
* *Getter:* `Material getMaterial() const`
* *Getter:* `Material getMaterial(unsigned int submesh) const`

PBR material descriptor. Contains base color, metallic/roughness factors, normal map, emissive settings, and shader overrides.

---

### primitiveType

* *Setter:* `void setPrimitiveType(PrimitiveType primitiveType)`
* *Getter:* `PrimitiveType getPrimitiveType() const`

GPU draw mode. Overloads are available per submesh.

---

### faceCulling

* *Setter:* `void setFaceCulling(bool faceCulling)`
* *Getter:* `bool isFaceCulling() const`

Enables or disables back-face culling globally for this mesh. Disable for double-sided geometry (e.g. leaves, cards).

---

### castShadows / receiveShadows

* *Setter:* `void setCastShadows(bool castShadows)` / `void setReceiveShadows(bool receiveShadows)`
* *Getter:* `bool isCastShadows() const` / `bool isReceiveShadows() const`

Shadow participation flags. Enabling both adds depth-map cost; disable on distant or small objects for performance.

---

### receiveIBL

When `true`, the mesh samples the scene's Sky environment for image-based lighting:
diffuse irradiance plus specular reflections on top of punctual lights. Requires a Sky
entity with a cubemap texture, **Receive Lights** enabled, and surface normals.

Set this in the editor on the Mesh component (**Receive IBL**). The flag is serialized
with the scene. Metallic, low-roughness materials show the strongest reflections.

---

### transparent / autoTransparency

* *transparent Setter:* `void setTransparent(bool transparent)`
* *autoTransparency Setter:* `void setAutoTransparency(bool autoTransparency)`

`transparent` marks the mesh for the transparent render pass (sorted back-to-front). `autoTransparency` detects transparency from the material and enables the transparent pass automatically.

## Method details

### load

* `bool load()`

Uploads geometry and material resources to the GPU. Must be called after building or modifying geometry programmatically. Subclasses like `Sprite` call this internally when needed.

---

### setTexture

* `void setTexture(const std::string& path)`
* `void setTexture(const std::string& id, TextureData data)`
* `void setTexture(Framebuffer* framebuffer)`

Assigns the diffuse/base-color texture. Accepts a file path, raw `TextureData`, or a framebuffer render target.

=== "C++"

    ```cpp
    mesh.setTexture("textures/stone.png");
    // or use a render-to-texture framebuffer:
    Camera cam(&scene);
    cam.setRenderToTexture(true);
    mesh.setTexture(cam.getFramebuffer());
    ```

=== "Lua"

    ```lua
    mesh:setTexture("textures/stone.png")
    ```

---

### setAsMirror / removeMirror / isMirror

* `void setAsMirror()` — turn this flat mesh into a planar reflection surface, using the default `+Z` normal (matching a [Wall](shape.md)).
* `void setAsMirror(Vector3 normal)` — same, with an explicit surface normal in local space (e.g. `Vector3(0, 1, 0)` for a `createPlane` floor).
* `void removeMirror()` — stop being a mirror.
* `bool isMirror() const` — whether this mesh is currently a mirror.

The engine creates and drives the reflection camera internally and feeds its render
target to the mesh's base texture — no camera setup is required. Set `receiveLights` to
`false` for a reflection shown without surface shading. See
[Rendering Pipeline — Mirrors](../../manual/rendering-pipeline.md#mirrors-and-planar-reflections).

=== "C++"

    ```cpp
    Shape mirror(&scene);
    mirror.createWall(10.0f, 10.0f);
    mirror.setAsMirror();
    mirror.setReceiveLights(false);
    ```

=== "Lua"

    ```lua
    mirror:createWall(10.0, 10.0)
    mirror:setAsMirror()
    mirror.receiveLights = false
    ```

---

### getAABB / getVerticesAABB / getWorldAABB

* `AABB getAABB() const` — Axis-aligned bounding box of the mesh in local space.
* `AABB getVerticesAABB() const` — AABB computed from raw vertex positions, ignoring the transform.
* `AABB getWorldAABB() const` — AABB in world space after applying the full transform chain.

Useful for frustum culling, click picking, and physics proxy fitting.

---

### getNumSubmeshes

* `unsigned int getNumSubmeshes() const`

Returns the number of submeshes. Each submesh can have its own material, primitive type, and culling settings.

---

### createInstancedMesh

* `void createInstancedMesh()`

Enables GPU instancing for this mesh. After calling this, use [addInstance](#addinstance) / [updateInstance](#updateinstance) to populate the instance list, then [updateInstances](#updateinstances) to flush changes to the GPU.

=== "C++"

    ```cpp
    Mesh tree(&scene);
    tree.setTexture("textures/tree.png");
    tree.createInstancedMesh();
    tree.setMaxInstances(500);

    for (int i = 0; i < 500; i++) {
        tree.addInstance(Vector3(i * 2.0f, 0.0f, 0.0f));
    }
    tree.updateInstances();
    ```

=== "Lua"

    ```lua
    local tree = Mesh(scene)
    tree:setTexture("textures/tree.png")
    tree:createInstancedMesh()
    tree:setMaxInstances(500)

    for i = 0, 499 do
        tree:addInstance(Vector3(i * 2, 0, 0))
    end
    tree:updateInstances()
    ```

---

### addInstance

* `void addInstance(InstanceData instance)`
* `void addInstance(Vector3 position)`
* `void addInstance(float x, float y, float z)`
* `void addInstance(Vector3 position, Quaternion rotation, Vector3 scale)`
* `void addInstance(Vector3 position, Quaternion rotation, Vector3 scale, Vector4 color)`
* `void addInstance(Vector3 position, Quaternion rotation, Vector3 scale, Vector4 color, Rect textureRect)`

Appends a new instance with the specified transform. Requires [createInstancedMesh](#createinstancedmesh) to have been called first.

---

### updateInstance

* `void updateInstance(size_t index, InstanceData instance)` *(and overloads)*

Replaces the data for an existing instance at `index`. Call [updateInstances](#updateinstances) afterwards to sync changes to the GPU.

---

### updateInstances

* `void updateInstances()`

Uploads all pending instance data changes to the GPU vertex buffer. Must be called after any [addInstance](#addinstance) or [updateInstance](#updateinstance) calls.

---

### clearInstances

* `void clearInstances()`

Removes all instances from the instance list. The mesh geometry is preserved; call [updateInstances](#updateinstances) afterwards.
