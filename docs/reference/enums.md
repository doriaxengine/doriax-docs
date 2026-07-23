---
description: Doriax API enumerations exposed to C++ and Lua.
---

# Enumerations

Most enums are exposed as Lua namespaces (`Scaling.FITWIDTH`) and C++ `enum class`
types. C++-only enums are noted below. See [Engine](classes/engine.md) for `Scaling`,
`Platform`, and `GraphicBackend`.

| Enum | Typical use |
| --- | --- |
| `Scaling` | Canvas scaling mode |
| `TextureStrategy` | Non-power-of-two texture handling |
| `Platform` | Runtime OS |
| `GraphicBackend` | Graphics API |
| `BodyType` | `STATIC`, `KINEMATIC`, `DYNAMIC` |
| `CameraType` | UI, orthographic, perspective |
| `LightType` | Directional, point, spot |
| `Occluder2DShape` | 2D shadow occluder outline (`AUTO_QUAD`, `POLYGON`) |
| `ShadowQuality` | Shadow PCF filter, 3D and 2D (`NONE`, `LOW`, `MEDIUM`, `HIGH`) |
| `Shape2DType` / `Shape3DType` | Physics shapes |
| `Joint2DType` / `Joint3DType` | Constraints |
| `AnchorPreset` / `PivotPreset` | UI layout |
| `EaseType` | Animation easing |
| `SoundState` / `SoundAttenuation` | Audio |
| `ActionState` | Action playback |
| `FogType` | Fog mode |
| `ReflectionProbeMode` | Reflection probe source (`STATIC`, `DYNAMIC`) |
| `ReflectionProbeUpdateMode` | Dynamic probe capture policy (`ON_LOAD`, `ON_MOVE`, `INTERVAL`, `MANUAL`) |
| `LightState` / `UIEventState` | Scene flags |
| `PrimitiveType` / `CullingMode` / `WindingOrder` | Rendering |
| `MaterialAlphaMode` | Material alpha handling (`AUTO`, `OPAQUE`, `MASK`, `BLEND`) |
| `TextureFilter` / `TextureWrap` / `TextureType` | Textures |
| `CursorType` | Mouse cursor |
| `ResourceLoadState` | Async loading |

Run `doriax/generate_api_suggestions.py` against the engine binding folder for the
authoritative member list when documenting new enum values.
