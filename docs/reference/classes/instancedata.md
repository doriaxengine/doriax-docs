---
description: InstanceData API reference (C++ and Lua).
---

# InstanceData

`InstanceData` API exposed to Lua and C++ gameplay code.

## Properties

| Name | Languages |
| --- | --- |
| `position` | C++ \| Lua |
| `rotation` | C++ \| Lua |
| `scale` | C++ \| Lua |
| `color` | C++ \| Lua |
| `textureRect` | C++ \| Lua |
| `custom` | C++ \| Lua |
| `visible` | C++ \| Lua |

`custom` is a `Vector4`, `(0,0,0,0)` by default, that shader files read as `context.instance`; see [Mesh.setInstanceCustom](mesh.md#setinstancecustom-getinstancecustom).
