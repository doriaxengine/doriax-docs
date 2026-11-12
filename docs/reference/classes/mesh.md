---
description: Mesh API reference — geometry, materials, shader files, shadows, transparency, and GPU instancing.
---

# Mesh

## Description

`Mesh` is the base class for all renderable 3D objects. It exposes the material system (color, texture, PBR material, [shader file](#shader)), shadow casting and receiving, transparency control, face culling, automatic detail levels, and GPU instancing (including distance fade and per-view instance culling) for drawing thousands of objects in a single draw call.

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

### Constructors

Available in C++ and Lua:

* `Mesh(Scene* scene)` — creates a new entity.
* `Mesh(Scene* scene, Entity entity)` — wraps an existing entity without taking ownership.

In Lua, use `Mesh(scene, entity)` to access an existing mesh. The entity must
already have the components required by this type; wrapping does not add them.
See [EntityHandle ownership](entityhandle.md#ownership-and-lifetime).

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
| bool | [receiveIBL](#receiveibl) | `false` | C++ \| Lua |
| bool | [castShadows](#castshadows-receiveshadows) | `true` | C++ \| Lua |
| bool | [receiveShadows](#castshadows-receiveshadows) | `true` | C++ \| Lua |
| bool | [lodEnabled](#lodenabled-lodbias) | `true` | C++ \| Lua |
| float | [lodBias](#lodenabled-lodbias) | `1.0` | C++ \| Lua |
| bool | shadowsBillboard | `true` | C++ \| Lua |
| bool | [renderInReflectionProbes](#renderinreflectionprobes) | `true` | C++ \| Lua |
| bool | castShadowsWithTexture | `false` | C++ \| Lua |
| bool | [transparent](#transparent-autotransparency) | `false` | C++ \| Lua |
| bool | [autoTransparency](#transparent-autotransparency) | `true` | C++ \| Lua |
| string | [shader](#shader) | `""` | C++ \| Lua |
| float | [vertexOffsetMax](#vertexoffsetmax) | `0` | C++ \| Lua |
| unsigned int | [maxInstances](#maxinstances) | `100` | C++ \| Lua |
| bool | [instancedBillboard](#instancedbillboard-instancedcylindricalbillboard) | `false` | C++ \| Lua |
| bool | [instancedCylindricalBillboard](#instancedbillboard-instancedcylindricalbillboard) | `false` | C++ \| Lua |
| bool | [distanceFade](#distancefade-fadestart-fadeend) | `false` | C++ \| Lua |
| float | [fadeStart](#distancefade-fadestart-fadeend) | `0` | C++ \| Lua |
| float | [fadeEnd](#distancefade-fadestart-fadeend) | `0` | C++ \| Lua |
| bool | [cullInstances](#cullinstances) | `true` | C++ \| Lua |
| float | [cullDistance](#culldistance) | `0` | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| bool | [load](#load) | C++ |
| void | [setTexture](#settexture) | C++ \| Lua |
| void | [setColor](#color) | C++ \| Lua |
| Vector4 | [getColor](#color) | C++ |
| void | [setAlpha](#alpha) | C++ |
| float | [getAlpha](#alpha) | C++ |
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
| void | [setCastShadows](#castshadows-receiveshadows) | C++ |
| bool | [isCastShadows](#castshadows-receiveshadows) | C++ |
| void | [setReceiveShadows](#castshadows-receiveshadows) | C++ |
| bool | [isReceiveShadows](#castshadows-receiveshadows) | C++ |
| void | [setLodEnabled](#lodenabled-lodbias) | C++ |
| bool | [isLodEnabled](#lodenabled-lodbias) | C++ |
| void | [setLodBias](#lodenabled-lodbias) | C++ |
| float | [getLodBias](#lodenabled-lodbias) | C++ |
| void | setShadowsBillboard | C++ \| Lua |
| bool | isShadowsBillboard | C++ \| Lua |
| void | setCastShadowsWithTexture | C++ \| Lua |
| bool | isCastShadowsWithTexture | C++ \| Lua |
| void | [setTransparent](#transparent-autotransparency) | C++ |
| bool | [isTransparent](#transparent-autotransparency) | C++ |
| void | [setAutoTransparency](#transparent-autotransparency) | C++ |
| bool | [isAutoTransparency](#transparent-autotransparency) | C++ |
| void | [setShader](#shader) | C++ \| Lua |
| string | [getShader](#shader) | C++ \| Lua |
| void | [setVertexOffsetMax](#vertexoffsetmax) | C++ |
| float | [getVertexOffsetMax](#vertexoffsetmax) | C++ |
| void | [setShaderUniform](#setshaderuniform) | C++ \| Lua |
| Vector4 | [getShaderUniform](#setshaderuniform) | C++ \| Lua |
| bool | [removeShaderUniform](#setshaderuniform) | C++ \| Lua |
| void | [setShaderTexture](#setshadertexture) | C++ \| Lua |
| Texture | [getShaderTexture](#setshadertexture) | C++ \| Lua |
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
| Vector4 | [getInstanceCustom](#setinstancecustom-getinstancecustom) | C++ \| Lua |
| void | [setInstanceCustom](#setinstancecustom-getinstancecustom) | C++ \| Lua |
| void | [updateInstances](#updateinstances) | C++ \| Lua |
| size_t | [getNumInstances](#createinstancedmesh) | C++ \| Lua |
| void | [clearInstances](#clearinstances) | C++ \| Lua |
| void | [setInstancedBillboard](#createinstancedmesh) | C++ \| Lua |
| bool | [isInstancedBillboard](#createinstancedmesh) | C++ |
| void | [setInstancedCylindricalBillboard](#createinstancedmesh) | C++ |
| bool | [isInstancedCylindricalBillboard](#createinstancedmesh) | C++ |
| void | [setMaxInstances](#createinstancedmesh) | C++ |
| unsigned int | [getMaxInstances](#createinstancedmesh) | C++ |
| void | [setDistanceFade](#distancefade-fadestart-fadeend) | C++ |
| bool | [isDistanceFade](#distancefade-fadestart-fadeend) | C++ |
| void | [setFadeRange](#distancefade-fadestart-fadeend) | C++ \| Lua |
| void | [setFadeStart](#distancefade-fadestart-fadeend) | C++ |
| float | [getFadeStart](#distancefade-fadestart-fadeend) | C++ |
| void | [setFadeEnd](#distancefade-fadestart-fadeend) | C++ |
| float | [getFadeEnd](#distancefade-fadestart-fadeend) | C++ |
| void | [setCullInstances](#cullinstances) | C++ |
| bool | [isCullInstances](#cullinstances) | C++ |
| void | [setCullDistance](#culldistance) | C++ |
| float | [getCullDistance](#culldistance) | C++ |
| [MeshComponent](meshcomponent.md) | `getMeshComponent` | Lua |
| [InstancedMeshComponent](instancedmeshcomponent.md) | `getInstancedMeshComponent` | Lua |

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

* *Setter:* `void setMaterial(const Material& material)` *(first submesh)*
* *Setter:* `void setMaterial(unsigned int submesh, const Material& material)` *(per submesh)*
* *Getter:* `Material getMaterial() const`
* *Getter:* `Material getMaterial(unsigned int submesh) const`

PBR material descriptor. Contains base color, metallic/roughness factors, normal map, emissive settings, and the [shader](#shader) with its parameter values.

---

### primitiveType

* *Setter:* `void setPrimitiveType(PrimitiveType primitiveType)`
* *Getter:* `PrimitiveType getPrimitiveType() const`

GPU draw mode. Overloads are available per submesh.

---

### faceCulling

* *Setter:* `void setFaceCulling(bool faceCulling)`
* *Getter:* `bool isFaceCulling() const`

Enables or disables back-face culling globally for this mesh. Disable for double-sided geometry (e.g. leaves, cards): back faces are then lit with their normal flipped toward the viewer, as glTF double-sided materials are.

---

### castShadows / receiveShadows

* *Setter:* `void setCastShadows(bool castShadows)` / `void setReceiveShadows(bool receiveShadows)`
* *Getter:* `bool isCastShadows() const` / `bool isReceiveShadows() const`

Shadow participation flags. Enabling both adds depth-map cost; disable on distant or small objects for performance.

---

### lodEnabled / lodBias

* *lodEnabled Setter:* `void setLodEnabled(bool lodEnabled)`
* *lodEnabled Getter:* `bool isLodEnabled() const`
* *lodBias Setter:* `void setLodBias(float lodBias)`
* *lodBias Getter:* `float getLodBias() const`

[Mesh detail levels](../../manual/rendering-pipeline.md#mesh-detail-lod). `lodEnabled` (default `true`) lets this mesh follow the scene's detail levels; turn it off to keep it at full detail, for example a hero asset whose silhouette must never change. Toggling it reloads the mesh. `lodBias` (default `1`) scales how far detail is kept: above 1 keeps the source longer, below 1 drops to a coarser level sooner.

Nothing happens until the scene has [meshLodEnabled](scene.md#meshlodenabled-meshlodthreshold) on, which is off by default. Terrain and tilemaps ignore these flags and keep their own LOD.

=== "C++"

    ```cpp
    mesh.setLodBias(1.5f);       // keep detail longer than the scene threshold
    statue.setLodEnabled(false); // always full detail
    ```

=== "Lua"

    ```lua
    mesh.lodBias = 1.5         -- keep detail longer than the scene threshold
    statue.lodEnabled = false  -- always full detail
    ```

---

### renderInReflectionProbes

* *Setter:* `void setRenderInReflectionProbes(bool renderInReflectionProbes)`
* *Getter:* `bool isRenderInReflectionProbes() const`

Whether the mesh is drawn into [ReflectionProbe](reflectionprobe.md) captures. Turn it off
when an object surrounds or sits on a probe and would otherwise show up inside its own
reflection. Normal rendering is unaffected — this only controls the capture pass.

Changing it re-captures every probe in the scene: a probe that already baked its cubemap
keeps the old contents until it captures again.

---

### receiveIBL

* *Setter:* `void setReceiveIBL(bool receiveIBL)`
* *Getter:* `bool isReceiveIBL() const`

When `true`, the mesh samples image-based lighting: diffuse irradiance plus specular
reflections on top of punctual lights. The source is the scene's Sky environment, a
[Reflection Probe](reflectionprobe.md) whose volume covers the mesh, or both. Sky
lighting needs a Sky entity with a cubemap texture; probes need none. Also requires
**Receive Lights** enabled and surface normals.

Also settable in the editor on the Mesh component (**Receive IBL**); the flag is
serialized with the scene. Metallic, low-roughness materials show the strongest
reflections.

Beyond reflective materials, this is what keeps *unlit* sides of an object from going
flat. A surface no light reaches falls back to the scene's global illumination, which is
a single flat colour — with a bright white ambient it washes out to a pale grey. With
`receiveIBL` the same surface takes its colour from the sky instead. This shows up most
in [mirrors](../../manual/rendering-pipeline.md#mirrors-and-planar-reflections), which
show the side of an object facing the mirror — usually the side the key light misses.

---

### transparent / autoTransparency

* *transparent Setter:* `void setTransparent(bool transparent)`
* *autoTransparency Setter:* `void setAutoTransparency(bool autoTransparency)`

`transparent` marks the mesh for the transparent render pass (sorted back-to-front). `autoTransparency` detects blending from the material (`BLEND`, or `AUTO` when the texture or factor is translucent) and enables the transparent pass automatically. A blended submesh keeps depth testing but disables depth writes in the colour pass so overlapping translucent surfaces composite correctly.

---

### shader

* *Setter:* `void setShader(const std::string& path)` *(all submeshes)*
* *Setter:* `void setShader(unsigned int submesh, const std::string& path)` *(per submesh)*
* *Getter:* `std::string getShader() const` *(first submesh)*
* *Getter:* `std::string getShader(unsigned int submesh) const`

The [shader file](../../manual/shader-files.md) (`.glsl`) or [shader graph](../../editor/shader-graphs.md) (`.shader`) the mesh draws with, as a project-relative path such as `"shaders/wave.glsl"`, or one of [the engine's](../../manual/shader-files.md#the-engines-shader-files) such as `"shaders/wind.glsl"`. It must be a `mesh` shader. The path is stored on the [material](material.md#shader-shaderuniforms-shadertextures) of each submesh, so submeshes can draw with different shaders. Its hooks also run in the depth, shadow and G-buffer passes, so shadows, SSAO and reflections follow what it draws; see [Mesh hooks](../../manual/shader-files.md#mesh-hooks).

Empty (default) uses the scene's [defaultMeshShader](scene.md#defaultmeshshader), or the engine built-in when the scene has none. Changing it reloads the mesh, and a shader that fails to build draws as the built-in one. [Terrain](terrain.md) ignores it. On a [Model](model.md) whose meshes are child entities, the setters change every part and a submesh index counts across them. The engine loads the compiled shader; the sources are only needed by the editor, and a shader given only at runtime must be added to the [export](../../manual/shader-files.md#export). See [Custom Shaders](../../editor/custom-shaders.md).

=== "C++"

    ```cpp
    mesh.setShader("shaders/wave.glsl");     // every submesh
    mesh.setShader(1, "shaders/glass.glsl"); // the second submesh only
    ```

=== "Lua"

    ```lua
    mesh.shader = "shaders/wave.glsl"
    mesh:setShader(1, "shaders/glass.glsl")
    ```

---

### vertexOffsetMax

* *Setter:* `void setVertexOffsetMax(float vertexOffsetMax)`
* *Getter:* `float getVertexOffsetMax() const`

The longest distance, in world units, the shader's [vertex offset](../../manual/shader-files.md#vertex-offsets) moves a vertex. Longer offsets are clamped to it, and culling widens the mesh bounds and each instance's sphere by it, so moved geometry is not culled at the screen edge or out of a shadow cascade. `0` (default) clamps nothing and keeps the bounds of the mesh data. It belongs to the mesh, not to a material, so one value covers every submesh.

=== "C++"

    ```cpp
    grass.setShader("shaders/wind.glsl");
    grass.setShaderUniform("windSway", 0.3f);
    grass.setVertexOffsetMax(0.8f);
    ```

=== "Lua"

    ```lua
    grass.shader = "shaders/wind.glsl"
    grass:setShaderUniform("windSway", 0.3)
    grass.vertexOffsetMax = 0.8
    ```

---

### maxInstances

* *Setter:* `void setMaxInstances(unsigned int maxInstances)`
* *Getter:* `unsigned int getMaxInstances() const`

Slots in the GPU instance buffer, `100` by default. Drawing clamps to it, but [addInstance](#addinstance) grows the cap as the list outgrows it — reloading the mesh each time — so the clamp only bites when the instance list is filled without going through `addInstance`. Set the capacity up front when the count is already known, to skip those reloads. Unlike the billboard setters, this one logs an error if the mesh is not instanced yet — call [createInstancedMesh](#createinstancedmesh) first.

---

### instancedBillboard / instancedCylindricalBillboard

* *Setter:* `void setInstancedBillboard(bool billboard)`
* *Setter:* `void setInstancedBillboard(bool billboard, bool cylindrical)`
* *Getters:* `bool isInstancedBillboard() const`, `bool isInstancedCylindricalBillboard() const`

Turns every instance to face the camera, the per-instance counterpart of [Object.billboard](object.md#billboard). Both default to `false`, and `instancedCylindricalBillboard` only matters while `instancedBillboard` is on. The setters create the instanced mesh if it does not exist yet.

!!! warning "Cylindrical is not Y-only yet"
    The instanced path builds its rotation from the inverse view matrix whichever flag is set, so instanced cylindrical facing currently matches the spherical one. [Object.cylindricalBillboard](object.md#billboard) does constrain to Y.

=== "C++"

    ```cpp
    grass.setInstancedBillboard(true, true);
    ```

=== "Lua"

    ```lua
    grass.instancedBillboard = true
    grass.instancedCylindricalBillboard = true
    ```

---

### distanceFade / fadeStart / fadeEnd

* *distanceFade Setter:* `void setDistanceFade(bool distanceFade)`
* *distanceFade Getter:* `bool isDistanceFade() const`
* *Setter:* `void setFadeRange(float fadeStart, float fadeEnd)`
* *fadeStart Setter / Getter:* `void setFadeStart(float fadeStart)` / `float getFadeStart() const`
* *fadeEnd Setter / Getter:* `void setFadeEnd(float fadeEnd)` / `float getFadeEnd() const`

Instanced-mesh [distance fade](../../manual/rendering-pipeline.md#distance-fade). When `distanceFade` is on, instances shrink toward their base between `fadeStart` and `fadeEnd`, both model-space distances from the camera. Toggling the flag reloads the mesh (shader variant `Ifd`); the two distances are uniforms and can change without a reload. `Fade End` must be greater than `Fade Start`. Logs an error if the mesh is not instanced yet.

On triangle meshes, instances past `fadeEnd` are also omitted from the draw, unless SSR is on: its G-buffer has no fade, so they are still submitted and rely on the vertex scale.

=== "C++"

    ```cpp
    trees.createInstancedMesh();
    trees.setDistanceFade(true);
    trees.setFadeRange(40.0f, 60.0f);
    ```

=== "Lua"

    ```lua
    trees:createInstancedMesh()
    trees.distanceFade = true
    trees:setFadeRange(40, 60)
    ```

---

### cullInstances

* *Setter:* `void setCullInstances(bool cullInstances)`
* *Getter:* `bool isCullInstances() const`

When `true` (default), instances outside the main camera or a shadow atlas slot are left out of that view. Turn it off when a shader moves instances away from the bounds the CPU computed; the whole entity then skips frustum culling too. Logs an error if the mesh is not instanced yet. See [Culling granularity](../../manual/rendering-pipeline.md#culling-granularity).

---

### cullDistance

* *Setter:* `void setCullDistance(float distance)`
* *Getter:* `float getCullDistance() const`

World-space distance from the main camera past which instances are dropped from the culled views (main camera and shadow slots). `0` (default) means unlimited; negative or non-finite values are ignored. A hard cut, unlike [distanceFade](#distancefade-fadestart-fadeend): instances keep their size until they vanish, and it applies with custom shaders and SSR too, so hide it with fog. Requires [cullInstances](#cullinstances). Logs an error if the mesh is not instanced yet.

=== "C++"

    ```cpp
    trees.createInstancedMesh();
    trees.setCullDistance(150.0f);
    ```

=== "Lua"

    ```lua
    trees:createInstancedMesh()
    trees.cullDistance = 150
    ```

---

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

Use these to make an existing mesh reflective. To create a mirror outright, the
[Mirror](mirror.md) class does both steps at once and exposes the surface normal as a
property.

---

### setShaderUniform

* `void setShaderUniform(const std::string& name, const Vector4& value)`
* `void setShaderUniform(const std::string& name, const Vector3& value)`
* `void setShaderUniform(const std::string& name, const Vector2& value)`
* `void setShaderUniform(const std::string& name, float value)`
* `void setShaderUniform(unsigned int submesh, const std::string& name, const Vector4& value)`
* `Vector4 getShaderUniform(const std::string& name) const`
* `Vector4 getShaderUniform(unsigned int submesh, const std::string& name) const`
* `bool removeShaderUniform(const std::string& name)`

Values of the parameters the mesh's [shader](#shader) declares with `#pragma param`, by
name (see [Declaring parameters](../../manual/shader-files.md#declaring-parameters)). They
are stored on the materials: without a submesh a value goes to every submesh, and with one,
as a `Vector4`, only to that submesh, so two submeshes can give the same shader different
values. A
narrower value leaves the remaining components at zero, and an `int` parameter takes the
truncated value. Setting a value only rewrites the uploaded block, so it can be called
every frame. Names the shader does not declare are kept but unused, and a parameter with
no value reads the scene's value while the material inherits the
[scene default shader](scene.md#setdefaultshaderuniform), else its declared default.

`getShaderUniform` returns the stored value of the first submesh, or of `submesh`, zero
when unset. It reads the material's own values, not the uploaded block or the scene's, so
an `int` parameter set to `3.7` reads back `3.7` while the shader sees `3`.
`removeShaderUniform` drops the value from every submesh and returns whether one existed;
the parameter reads its inherited or declared default again.

=== "C++"

    ```cpp
    mesh.setShader("shaders/wave.glsl");
    mesh.setShaderUniform("amplitude", 0.3f);
    mesh.setShaderUniform("direction", Vector2(1.0f, 0.0f));
    mesh.setShaderUniform(1, "tint", Vector4(0.2f, 0.5f, 1.0f, 0.5f)); // second submesh only

    Vector4 tint = mesh.getShaderUniform(1, "tint");
    ```

=== "Lua"

    ```lua
    mesh.shader = "shaders/wave.glsl"
    mesh:setShaderUniform("amplitude", 0.3)
    mesh:setShaderUniform("direction", Vector2(1, 0))
    mesh:setShaderUniform(1, "tint", Vector4(0.2, 0.5, 1.0, 0.5))

    local tint = mesh:getShaderUniform(1, "tint")
    ```

---

### setShaderTexture

* `void setShaderTexture(const std::string& name, const Texture& texture)`
* `void setShaderTexture(unsigned int submesh, const std::string& name, const Texture& texture)`
* `Texture getShaderTexture(const std::string& name) const`
* `Texture getShaderTexture(unsigned int submesh, const std::string& name) const`

Sets a texture parameter the shader declares with `#pragma param texture2D` or
`textureCube` (see [Textures](../../manual/shader-files.md#textures)), on the material of
every submesh or of one. The [Texture](texture.md) can be a file, pixel data or a camera's
render target, and an empty one draws the declared default. The texture is bound again
without rebuilding the shader. `getShaderTexture` returns the texture set on the material
of `submesh`, the first without one, empty when none.

=== "C++"

    ```cpp
    rock.setShader("shaders/detail.glsl");
    rock.setShaderTexture("detail", Texture("textures/rock_detail.png"));
    ```

=== "Lua"

    ```lua
    rock.shader = "shaders/detail.glsl"
    rock:setShaderTexture("detail", Texture("textures/rock_detail.png"))
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

Instancing draws geometry on this entity only. Multi-node GLTF models that keep child mesh entities need [static merge](../../manual/3d-graphics.md#merging-static-model-meshes) first (or use a single-mesh / procedural mesh).

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
    tree.maxInstances = 500

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

Appends a new instance with the specified transform, creating the instanced mesh if the entity does not have one yet. Growing past [maxInstances](#maxinstances) doubles the capacity and reloads the mesh.

---

### updateInstance

* `void updateInstance(size_t index, InstanceData instance)` *(and overloads)*

Replaces the data for an existing instance at `index`. Call [updateInstances](#updateinstances) afterwards to sync changes to the GPU.

---

### setInstanceCustom / getInstanceCustom

* `void setInstanceCustom(size_t index, Vector4 custom) const`
* `Vector4 getInstanceCustom(size_t index)`

A `Vector4` of the instance at `index` that shader files read as `context.instance`, for a color, a growth stage or a random seed per instance (see [Per-instance values](../../manual/shader-files.md#per-instance-values)). It is the `custom` field of [InstanceData](instancedata.md), `(0,0,0,0)` by default. The setter marks the instances for upload, so no [updateInstances](#updateinstances) call is needed. It logs an error if the mesh is not instanced, and the getter then returns zero.

=== "C++"

    ```cpp
    trees.setInstanceCustom(0, Vector4(0.5f, 0.0f, 0.0f, 0.0f));
    ```

=== "Lua"

    ```lua
    trees:setInstanceCustom(0, Vector4(0.5, 0, 0, 0))
    ```

---

### updateInstances

* `void updateInstances()`

Uploads all pending instance data changes to the GPU vertex buffer. Must be called after any [addInstance](#addinstance) or [updateInstance](#updateinstance) calls.

---

### clearInstances

* `void clearInstances()`

Removes all instances from the instance list. The mesh geometry is preserved; call [updateInstances](#updateinstances) afterwards.
