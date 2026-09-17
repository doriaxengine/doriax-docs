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
