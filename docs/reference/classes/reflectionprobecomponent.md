---
description: ReflectionProbeComponent API reference (C++ and Lua).
---

# ReflectionProbeComponent

The data behind a [ReflectionProbe](reflectionprobe.md). In Lua, get it with `probe:getReflectionProbeComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `mode` | C++ \| Lua |
| `updateMode` | C++ \| Lua |
| `boxOffset` | C++ \| Lua |
| `boxSize` | C++ \| Lua |
| `blendDistance` | C++ \| Lua |
| `intensity` | C++ \| Lua |
| `priority` | C++ \| Lua |
| `resolution` | C++ \| Lua |
| `nearClip` | C++ \| Lua |
| `farClip` | C++ \| Lua |
| `updateInterval` | C++ \| Lua |
| `includeSky` | C++ \| Lua |
| `texture` | C++ \| Lua (read-only) |
| `needUpdate` | C++ \| Lua |

Set `needUpdate` to capture again. `texture` is the captured cubemap.
