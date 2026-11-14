---
description: WaterComponent API reference (C++ and Lua).
---

# WaterComponent

The data behind [Water](water.md). In Lua, get it with `water:getWaterComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `loaded` | C++ \| Lua (read-only) |
| `aabb` | C++ \| Lua (read-only) |
| `worldAABB` | C++ \| Lua (read-only) |
| `shader` | C++ \| Lua |
| `shaderUniforms` | C++ |
| `shaderTextures` | C++ |
| `size` | C++ \| Lua |
| `subdivisions` | C++ \| Lua |
| `shallowColor` | C++ \| Lua |
| `deepColor` | C++ \| Lua |
| `depthFade` | C++ \| Lua |
| `waveHeight` | C++ \| Lua |
| `waveLength` | C++ \| Lua |
| `waveSpeed` | C++ \| Lua |
| `waveDirection` | C++ \| Lua |
| `waveSteepness` | C++ \| Lua |
| `normalTexture` | C++ \| Lua |
| `normalScale` | C++ \| Lua |
| `normalStrength` | C++ \| Lua |
| `rippleSpeed` | C++ \| Lua |
| `reflectivity` | C++ \| Lua |
| `specularIntensity` | C++ \| Lua |
| `roughness` | C++ \| Lua |
| `foamColor` | C++ \| Lua |
| `shoreFoam` | C++ \| Lua |
| `crestFoam` | C++ \| Lua |
| `receiveShadows` | C++ \| Lua |
| `depthEffects` | C++ \| Lua |
| `planarReflection` | C++ \| Lua |
| `reflectionDistortion` | C++ \| Lua |
| `refraction` | C++ \| Lua |
| `refractionDistortion` | C++ \| Lua |
| `caustics` | C++ \| Lua |
| `causticsScale` | C++ \| Lua |
| `underwater` | C++ \| Lua |
| `buoyancy` | C++ \| Lua |
| `buoyancyDepth` | C++ \| Lua |
| `wakeArea` | C++ \| Lua |
| `wakeFade` | C++ \| Lua |
| `needUpdateTexture` | C++ \| Lua |
| `needReload` | C++ \| Lua |

The colors are linear here, while the [Water](water.md) setters take sRGB. Set `needReload` after changing `size`, `subdivisions`, or `shader`, and `needUpdateTexture` after replacing `normalTexture`. `shader` is the water's [shader file](water.md#shader), the scene default when empty; `shaderUniforms` and `shaderTextures` hold its parameter values and textures by name; [setShaderUniform](water.md#setshaderuniform) and [setShaderTexture](water.md#setshadertexture) set them, also from Lua.
