---
description: Light2D API reference (C++ and Lua).
---

# Light2D

**Inherits:** [Object](object.md)  
**C++ type:** `Light2D`

## Description

A point light for 2D scenes. Unlike [Light](light.md), which drives the 3D PBR pipeline, a `Light2D` lives in the scene's XY plane and uses a simple radius falloff designed for the classic 2D look. Light from every `Light2D` is added on top of the scene's 2D ambient light (see [Scene — setAmbientLight2D](scene.md#setambientlight2d)); dim the ambient to make lights visible.

Sprites, tilemaps, and mesh polygons receive 2D light when their Mesh component has **Receive Lights** enabled (the default). UI objects are not affected. Up to `MAX_LIGHTS_2D` (16) lights can be active at once.

Shadows are opt-in per light and are cast by [Occluder2D](occluder2d.md) components using per-light 1D polar shadow maps — see [Rendering Pipeline — 2D lighting](../../manual/rendering-pipeline.md#2d-lighting-and-shadows).

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| Vector3 | [color](#color) | `(1,1,1)` | C++ \| Lua |
| float | [intensity](#intensity) | `1.0` | C++ \| Lua |
| float | [range](#range) | `200.0` | C++ \| Lua |
| float | [falloff](#falloff) | `1.0` | C++ \| Lua |
| float | [height](#height) | `0.0` | C++ \| Lua |
| bool | [shadows](#shadows) | `false` | C++ \| Lua |
| float | [shadowBias](#shadowbias) | `0.01` | C++ \| Lua |
| float | [shadowSoftness](#shadowsoftness) | `2.0` | C++ \| Lua |
| unsigned int | [mapResolution](#mapresolution) | `512` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setColor](#color) | C++ \| Lua |
| Vector3 | [getColor](#color) | C++ \| Lua |
| void | [setIntensity](#intensity) | C++ \| Lua |
| float | [getIntensity](#intensity) | C++ \| Lua |
| void | [setRange](#range) | C++ \| Lua |
| float | [getRange](#range) | C++ \| Lua |
| void | [setFalloff](#falloff) | C++ \| Lua |
| float | [getFalloff](#falloff) | C++ \| Lua |
| void | [setHeight](#height) | C++ \| Lua |
| float | [getHeight](#height) | C++ \| Lua |
| void | [setShadows](#shadows) | C++ \| Lua |
| bool | [isShadows](#shadows) | C++ \| Lua |
| void | [setShadowBias](#shadowbias) | C++ \| Lua |
| float | [getShadowBias](#shadowbias) | C++ \| Lua |
| void | [setShadowSoftness](#shadowsoftness) | C++ \| Lua |
| float | [getShadowSoftness](#shadowsoftness) | C++ \| Lua |
| void | [setMapResolution](#mapresolution) | C++ \| Lua |
| unsigned int | [getMapResolution](#mapresolution) | C++ \| Lua |

---

## Property details

### color

* *Setter*: void **setColor**(Vector3 color)
* *Setter*: void **setColor**(float r, float g, float b)
* *Getter*: Vector3 **getColor**() const

The RGB color of the emitted light. Each channel ranges from `0.0` to `1.0`.

=== "C++"
    ```cpp
    scene.setAmbientLight2D(0.15f); // dark scene so the light is visible

    Light2D torch(&scene);
    torch.setPosition(Vector3(300, 200, 0));
    torch.setColor(1.0f, 0.8f, 0.5f);
    torch.setRange(250);
    ```

=== "Lua"
    ```lua
    scene:setAmbientLight2D(0.15) -- dark scene so the light is visible

    local torch = Light2D(scene)
    torch.position = Vector3(300, 200, 0)
    torch:setColor(1.0, 0.8, 0.5)
    torch:setRange(250)
    ```

---

### intensity

* *Setter*: void **setIntensity**(float intensity)
* *Getter*: float **getIntensity**() const

A multiplier applied to the light's [color](#color). `1.0` is the default. Higher values create a brighter light without altering the hue.

---

### range

* *Setter*: void **setRange**(float range)
* *Getter*: float **getRange**() const

The radius of the light in world units. Nothing beyond this distance receives any light. In the editor, the range is drawn as a circle around the selected light.

---

### falloff

* *Setter*: void **setFalloff**(float falloff)
* *Getter*: float **getFalloff**() const

The attenuation exponent. Brightness fades as `pow(1 - distance/range, falloff)`: `1.0` is a linear fade, higher values concentrate the light near its center, values below `1.0` push light towards the edge of the range.

---

### height

* *Setter*: void **setHeight**(float height)
* *Getter*: float **getHeight**() const

A virtual Z height of the light above the 2D plane. With a height greater than zero, the light has a direction relative to each surface point, so **normal maps** on sprites produce relief shading that shifts as the light moves. With `0.0` (default) the light is purely radial and normals are ignored.

=== "C++"
    ```cpp
    // relief shading on a sprite with a normal texture in its material
    torch.setHeight(80.0f);
    ```

=== "Lua"
    ```lua
    -- relief shading on a sprite with a normal texture in its material
    torch.height = 80.0
    ```

---

### shadows

* *Setter*: void **setShadows**(bool shadows)
* *Getter*: bool **isShadows**() const

Enables shadow casting for this light. Shadows are produced by [Occluder2D](occluder2d.md) components in the scene; the receiver mesh must have `receiveShadows` enabled. Each light's shadow darkens only that light's contribution — the scene's ambient light is never shadowed.

---

### shadowBias

* *Setter*: void **setShadowBias**(float shadowBias)
* *Getter*: float **getShadowBias**() const

Depth bias for the shadow comparison, in normalized units of the light's [range](#range). Increase it if surfaces right at an occluder edge show shadow acne; decrease it if shadows detach from their occluders.

---

### shadowSoftness

* *Setter*: void **setShadowSoftness**(float shadowSoftness)
* *Getter*: float **getShadowSoftness**() const

The penumbra half-width, in shadow-map texels. `0.0` gives hard edges; values around `2.0`–`4.0` give a soft natural edge. If a wide penumbra shows banding, raise the scene-wide filter quality — see [Scene — shadow2DQuality](scene.md#shadow2dquality).

---

### mapResolution

* *Setter*: void **setMapResolution**(unsigned int mapResolution)
* *Getter*: unsigned int **getMapResolution**() const

The width in pixels of this light's 1D polar shadow map. Higher values give more angular precision for distant or thin occluders. The shadow atlas is sized by the largest `mapResolution` among the shadow-casting lights.
