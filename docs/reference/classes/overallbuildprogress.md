---
description: OverallBuildProgress API reference (C++ and Lua).
---

# OverallBuildProgress

`OverallBuildProgress` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Read-only from Lua"
    A progress snapshot: the build threads fill it in, scripts read it.

| Name | Languages |
| --- | --- |
| `totalProgress` | C++ \| Lua (read-only) |
| `totalBuilds` | C++ \| Lua (read-only) |
| `completedBuilds` | C++ \| Lua (read-only) |
| `currentBuildName` | C++ \| Lua (read-only) |
| `currentBuildType` | C++ \| Lua (read-only) |
| `hasActiveBuilds` | C++ \| Lua (read-only) |
