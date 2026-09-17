---
description: ResourceBuildInfo API reference (C++ and Lua).
---

# ResourceBuildInfo

`ResourceBuildInfo` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Read-only from Lua"
    A progress snapshot: the build threads fill it in, scripts read it.

| Name | Languages |
| --- | --- |
| `type` | C++ \| Lua (read-only) |
| `name` | C++ \| Lua (read-only) |
| `progress` | C++ \| Lua (read-only) |
| `isActive` | C++ \| Lua (read-only) |
| `startTime` | C++ \| Lua (read-only) |
