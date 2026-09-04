---
description: File API reference (C++ and Lua).
---

# File

**Inherits:** [FileData](filedata.md)  
**C++ type:** `File`

Disk file access. `File` requires a real filesystem entry and cannot open assets or Lua
files stored in an exported `resources.pak`; use [Data](data.md) or an engine resource
loader for packed read-only resources.

## Methods

| Name | Languages |
| --- | --- |
| `open` | C++ \| Lua |
| `flush` | C++ \| Lua |
| `close` | C++ \| Lua |
