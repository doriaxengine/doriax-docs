---
description: RayReturn API reference (C++ and Lua).
---

# RayReturn

Result of a ray cast (hit point, normal, distance).

## Properties

!!! note "Read-only from Lua"
    A raycast result: the systems fill it in, scripts read it.

| Name | Languages |
| --- | --- |
| `hit` | C++ \| Lua (read-only) |
| `distance` | C++ \| Lua (read-only) |
| `point` | C++ \| Lua (read-only) |
| `normal` | C++ \| Lua (read-only) |
| `body` | C++ \| Lua (read-only) |
| `shapeIndex` | C++ \| Lua (read-only) |

`distance` is where the hit lies along the ray, as a fraction from 0 at its origin to 1 at
`origin + direction`. `point` is the hit position in world space.
