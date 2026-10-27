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
| `customShader` | C++ \| Lua |
| `customUnderwaterShader` | C++ \| Lua |
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
| `needUpdateTexture` | C++ \| Lua |
| `needReload` | C++ \| Lua |

The colors are linear here, while the [Water](water.md) setters take sRGB. Set `needReload` after changing `size`, `subdivisions`, or a custom shader, and `needUpdateTexture` after replacing `normalTexture`.
