---
description: Water API reference (C++ and Lua) — a water surface with Gerstner waves, ripples, reflections, refraction, foam, an underwater view, and height queries.
---

# Water

**Inherits:** [Object](object.md)  
**C++ type:** `Water`

## Description

A water surface: a flat grid at the entity's height, displaced by Gerstner waves and
shaded with scrolling ripples, sky or planar reflections, refraction of the scene behind
it, shore and crest foam, and a fade seen from below the surface. Constructing a `Water`
attaches a `WaterComponent` to the entity. Water has its own render path, so it is not a
[Mesh](mesh.md) and needs no material, texture, or camera wiring.

The waves are computed in world space, so moving, rotating, or scaling the entity changes
the area the water covers but never stretches the waves. The surface always stays level at
the entity's world height, even when the entity is tilted.

See [Rendering Pipeline — Water](../../manual/rendering-pipeline.md#water) for how the
surface is drawn and what each feature costs.

=== "C++"

    ```cpp
    Water water(&scene);
    water.setPosition(0.0f, -0.5f, 0.0f);
    water.setSize(80.0f, 80.0f);
    water.setWaveHeight(0.4f);
    water.setWaveDirection(30.0f);
    water.setPlanarReflection(true);
    ```

=== "Lua"

    ```lua
    local water = Water(scene)
    water:setPosition(0, -0.5, 0)
    water:setSize(80, 80)
    water.waveHeight = 0.4
    water.waveDirection = 30
    water.planarReflection = true
    ```

A dynamic [Body3D](body3d.md#buoyancy) with a **buoyancy** above `0` floats on the waves
without any script; see [Physics — Buoyancy](../../manual/physics.md#buoyancy).

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [Vector2](vector2.md) | [size](#size-subdivisions) | `Vector2(50, 50)` | C++ \| Lua |
| unsigned int | [subdivisions](#size-subdivisions) | `128` | C++ \| Lua |
| [Vector3](vector3.md) | [shallowColor](#shallowcolor-deepcolor-depthfade) | `Vector3(0.20, 0.62, 0.62)` | C++ \| Lua |
| [Vector3](vector3.md) | [deepColor](#shallowcolor-deepcolor-depthfade) | `Vector3(0.02, 0.13, 0.22)` | C++ \| Lua |
| float | [depthFade](#shallowcolor-deepcolor-depthfade) | `3.0` | C++ \| Lua |
| float | [waveHeight](#waves) | `0.2` | C++ \| Lua |
| float | [waveLength](#waves) | `6.0` | C++ \| Lua |
| float | [waveSpeed](#waves) | `1.0` | C++ \| Lua |
| float | [waveDirection](#waves) | `0.0` | C++ \| Lua |
| float | [waveSteepness](#waves) | `0.6` | C++ \| Lua |
| float | [normalScale](#ripples) | `4.0` | C++ \| Lua |
| float | [normalStrength](#ripples) | `0.4` | C++ \| Lua |
| float | [rippleSpeed](#ripples) | `0.3` | C++ \| Lua |
| float | [reflectivity](#reflectivity-specularintensity-roughness) | `1.0` | C++ \| Lua |
| float | [specularIntensity](#reflectivity-specularintensity-roughness) | `1.0` | C++ \| Lua |
| float | [roughness](#reflectivity-specularintensity-roughness) | `0.06` | C++ \| Lua |
| bool | [receiveShadows](#receiveshadows) | `true` | C++ \| Lua |
| bool | [planarReflection](#planarreflection-reflectiondistortion) | `false` | C++ \| Lua |
| float | [reflectionDistortion](#planarreflection-reflectiondistortion) | `0.04` | C++ \| Lua |
| bool | [refraction](#refraction-refractiondistortion) | `true` | C++ \| Lua |
| float | [refractionDistortion](#refraction-refractiondistortion) | `0.03` | C++ \| Lua |
| bool | [underwater](#underwater) | `true` | C++ \| Lua |
| bool | [depthEffects](#deptheffects) | `true` | C++ \| Lua |
| [Vector3](vector3.md) | [foamColor](#foamcolor-shorefoam-crestfoam) | `Vector3(1, 1, 1)` | C++ \| Lua |
| float | [shoreFoam](#foamcolor-shorefoam-crestfoam) | `0.4` | C++ \| Lua |
| float | [crestFoam](#foamcolor-shorefoam-crestfoam) | `0.15` | C++ \| Lua |
| string | [customShader](#customshader-customunderwatershader) | `""` | C++ \| Lua |
| string | [customUnderwaterShader](#customshader-customunderwatershader) | `""` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [load](#load) | C++ \| Lua |
| void | [setSize](#size-subdivisions) | C++ \| Lua |
| void | [setShallowColor](#shallowcolor-deepcolor-depthfade) | C++ \| Lua |
| void | [setDeepColor](#shallowcolor-deepcolor-depthfade) | C++ \| Lua |
| void | [setFoamColor](#foamcolor-shorefoam-crestfoam) | C++ \| Lua |
| void | [setNormalTexture](#ripples) | C++ \| Lua |
| void | [setShaderUniform](#setshaderuniform) | C++ \| Lua |
| Vector4 | [getShaderUniform](#setshaderuniform) | C++ \| Lua |
| bool | [removeShaderUniform](#setshaderuniform) | C++ \| Lua |
| float | [getHeight](#getheight-getnormal) | C++ \| Lua |
| Vector3 | [getNormal](#getheight-getnormal) | C++ \| Lua |

---

## Property details

### size / subdivisions

* *Setter*: void **setSize**([Vector2](vector2.md) size)
* *Setter*: void **setSize**(const float width, const float depth)
* *Getter*: [Vector2](vector2.md) **getSize**() const
* *Setter*: void **setSubdivisions**(unsigned int subdivisions)
* *Getter*: unsigned int **getSubdivisions**() const

`size` is the width (X) and depth (Z) of the surface, centered on the entity and scaled by
its transform. `subdivisions` is the number of grid cells along each side, capped at
`512`. Short waves need more cells to keep their shape; the grid has
`(subdivisions + 1)²` vertices, so raise it only as far as the waves need. Changing either
rebuilds the grid.

---

### shallowColor / deepColor / depthFade

* *Setter*: void **setShallowColor**(Vector3 color)
* *Setter*: void **setShallowColor**(const float r, const float g, const float b)
* *Getter*: Vector3 **getShallowColor**() const
* *Setter*: void **setDeepColor**(Vector3 color)
* *Setter*: void **setDeepColor**(const float r, const float g, const float b)
* *Getter*: Vector3 **getDeepColor**() const
* *Setter*: void **setDepthFade**(float depthFade)
* *Getter*: float **getDepthFade**() const

The water colour, in sRGB (stored linear, so the value read back is the sRGB form of the
stored one). Shallow water takes `shallowColor` and turns to `deepColor` as it deepens;
`depthFade` is the depth in world units where the deep colour takes over. Shallower water
is lighter and clearer.

With [refraction](#refraction-refractiondistortion) or the [underwater](#underwater) view,
`shallowColor` is also the tint of the scene seen through the water: its clearest channel
fades out over `depthFade`, and the other channels fade faster, while `deepColor` fills
in the light scattered by the water.

---

### waves

* *Setter*: void **setWaveHeight**(float waveHeight)
* *Setter*: void **setWaveLength**(float waveLength)
* *Setter*: void **setWaveSpeed**(float waveSpeed)
* *Setter*: void **setWaveDirection**(float waveDirection)
* *Setter*: void **setWaveSteepness**(float waveSteepness)
* *Getters*: **getWaveHeight**(), **getWaveLength**(), **getWaveSpeed**(), **getWaveDirection**(), **getWaveSteepness**()

The surface is the sum of four Gerstner waves derived from these values:

| Property | Meaning |
| --- | --- |
| `waveHeight` | How far the crests rise above the water level, in world units. |
| `waveLength` | Length of the longest wave. The other three are shorter and turned a little away from it. Longer waves also travel faster, as on deep water. |
| `waveSpeed` | Multiplier on the wave travel speed. `0` freezes the waves; a negative value runs them backwards. |
| `waveDirection` | Angle around Y the waves travel toward, `0` = `+X`. Degrees, or radians when [Engine::useDegrees](engine.md#usedegrees) is off. |
| `waveSteepness` | `0` gives round waves, `1` sharp crests. It is lowered automatically where the waves would fold over. |

Wave changes take effect on the next frame without a reload.

---

### ripples

* void **setNormalTexture**(const std::string& path)
* *Setter*: void **setNormalScale**(float normalScale)
* *Setter*: void **setNormalStrength**(float normalStrength)
* *Setter*: void **setRippleSpeed**(float rippleSpeed)
* *Getters*: **getNormalScale**(), **getNormalStrength**(), **getRippleSpeed**()

Small ripples come from a tiling normal map, sampled twice in two layers that drift across
each other. An empty path restores the built-in ripple map. Give a custom map a
mipmap filter so distant ripples do not shimmer.

`normalScale` is the world size of one tile, `normalStrength` how much the ripples bend
the lighting and reflections, and `rippleSpeed` how fast the layers drift (world units per
second).

---

### reflectivity / specularIntensity / roughness

* *Setter*: void **setReflectivity**(float reflectivity)
* *Setter*: void **setSpecularIntensity**(float specularIntensity)
* *Setter*: void **setRoughness**(float roughness)
* *Getters*: **getReflectivity**(), **getSpecularIntensity**(), **getRoughness**()

`reflectivity` scales the reflection (sky, or the scene with
[planarReflection](#planarreflection-reflectiondistortion)), `specularIntensity` scales
the sun glints, and `roughness` (`0`–`1`) spreads the highlight: low values give sharp
glints.

Without planar reflection the water reflects the scene's [Sky](skybox.md) (its texture,
colour, and rotation), or the background colour when the scene has no sky, and takes its
ambient light from the sky's environment when IBL is available.

---

### receiveShadows

* *Setter*: void **setReceiveShadows**(bool receiveShadows)
* *Getter*: bool **isReceiveShadows**() const

Shadows of the scene lights darken the sun glints and the light under the surface. Takes
effect only when the scene has a shadow-casting light. Deep, clear water shows shadows
only faintly, because most of its colour is reflected sky.

---

### planarReflection / reflectionDistortion

* *Setter*: void **setPlanarReflection**(bool planarReflection)
* *Getter*: bool **isPlanarReflection**() const
* *Setter*: void **setReflectionDistortion**(float reflectionDistortion)
* *Getter*: float **getReflectionDistortion**() const

Reflects the scene, not only the sky, like a [Mirror](mirror.md): the scene is drawn a
second time, at half resolution, from a camera reflected across the water plane.
`reflectionDistortion` is how much the ripples bend the reflection.

Only the scene's main camera sees the planar reflection; render-to-texture cameras,
mirrors, and other waters' reflection passes see the water reflect the sky.

---

### refraction / refractionDistortion

* *Setter*: void **setRefraction**(bool refraction)
* *Getter*: bool **isRefraction**() const
* *Setter*: void **setRefractionDistortion**(float refractionDistortion)
* *Getter*: float **getRefractionDistortion**() const

Shows the scene behind the water, bent by the ripples and tinted by the water it crosses
(see [shallowColor](#shallowcolor-deepcolor-depthfade)). The engine copies the scene once
per frame for it. `refractionDistortion` is how much the ripples bend what is seen
through.

Refraction is drawn for the main camera. Other cameras show the water alpha-blended over
the scene instead, as does a water with refraction off.

---

### underwater

* *Setter*: void **setUnderwater**(bool underwater)
* *Getter*: bool **isUnderwater**() const

When the main camera goes below the surface, inside the water's area, the scene fades into
the water with distance, using the same [colours and depth fade](#shallowcolor-deepcolor-depthfade).
With [depthEffects](#deptheffects) off the fade is even, as if everything were
`depthFade` away.

---

### depthEffects

* *Setter*: void **setDepthEffects**(bool depthEffects)
* *Getter*: bool **isDepthEffects**() const

Uses the scene depth for shore foam, soft edges where the water meets geometry, and the
shallow-to-deep tint. The depth comes from SSR or SSAO when the scene already has one of
them on; otherwise the engine adds a depth pre-pass for the water. Only the main camera
has the scene depth.

---

### foamColor / shoreFoam / crestFoam

* *Setter*: void **setFoamColor**(Vector3 color)
* *Setter*: void **setFoamColor**(const float r, const float g, const float b)
* *Getter*: Vector3 **getFoamColor**() const
* *Setter*: void **setShoreFoam**(float shoreFoam)
* *Setter*: void **setCrestFoam**(float crestFoam)
* *Getters*: **getShoreFoam**(), **getCrestFoam**()

`foamColor` is in sRGB. `shoreFoam` is the water depth the shore foam covers (needs
[depthEffects](#deptheffects)); `crestFoam` (`0`–`1`) is the share of the highest crests
that turn to foam.

---

### customShader / customUnderwaterShader

* *Setter*: void **setCustomShader**(const std::string& path)
* *Getter*: std::string **getCustomShader**() const
* *Setter*: void **setCustomUnderwaterShader**(const std::string& path)
* *Getter*: std::string **getCustomUnderwaterShader**() const

Base paths (no extension) of forked shaders. `customShader` replaces the water surface
shader (`water.vert` / `water.frag`); `customUnderwaterShader` replaces the fullscreen
fade of the [underwater](#underwater) view (`fullscreen.vert` / `underwater.frag`). An
empty path uses the scene's [default water shader](scene.md#defaultwatershader) for
`customShader`, then the built-in. See
[Custom Shaders — Water shaders](../../editor/custom-shaders.md#water-shaders).

---

## Method details

### load

* bool **load**()

Builds the grid and loads the shaders now instead of on the next frame. Not needed in
normal use: the render system loads a water the first time it updates.

---

### setShaderUniform

* `void setShaderUniform(const std::string& name, const Vector4& value)`
* `void setShaderUniform(const std::string& name, const Vector3& value)`
* `void setShaderUniform(const std::string& name, const Vector2& value)`
* `void setShaderUniform(const std::string& name, float value)`
* `Vector4 getShaderUniform(const std::string& name) const`
* `bool removeShaderUniform(const std::string& name)`

Values for the members of the forks' `u_vs_customParams` / `u_fs_customParams` blocks, by
member name. The water fork and the underwater fork read the same values. Setting a value
only rewrites the uploaded block, so it can run every frame; `time` and `resolution` are
reserved for the engine. Same semantics as [Mesh.setShaderUniform](mesh.md#setshaderuniform);
see [Custom Shaders — Shader uniforms](../../editor/custom-shaders.md#shader-uniforms).

---

### getHeight / getNormal

* float **getHeight**(float x, float z) const
* Vector3 **getNormal**(float x, float z) const

The world height and the unit normal of the surface over the world point `(x, z)`, waves
included. The result matches the surface the next frame draws, so calling it in
`onUpdate` keeps a buoy, a boat without physics, or a camera on the waves:

=== "C++"

    ```cpp
    Vector3 pos = buoy.getPosition();
    pos.y = water.getHeight(pos.x, pos.z);
    buoy.setPosition(pos);
    ```

=== "Lua"

    ```lua
    local pos = buoy:getPosition()
    pos.y = water:getHeight(pos.x, pos.z)
    buoy:setPosition(pos)
    ```

Neither call checks the water's area: a point outside it gets the waves as if the water
went on. Both follow the built-in wave math, so a [custom shader](#customshader-customunderwatershader)
that moves the vertices differently no longer matches them.
