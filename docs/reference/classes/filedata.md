---
description: FileData API reference (C++ and Lua).
---

# FileData

Abstract streaming interface shared by [File](file.md) and [Data](data.md).

`newFile` constructs the concrete type. Pass `useHandle = true` to request a disk
`File`; omit it or pass `false` for an in-memory `Data` buffer. In a native export with
resource packing enabled, a packed path still returns `Data` even when a handle was
requested, because a packed entry has no filesystem file to open.

## Methods

| Name | Languages |
| --- | --- |
| `newFile` | C++ \| Lua |
| `getBaseDir` | C++ \| Lua |
| `getFilePathExtension` | C++ \| Lua |
| `getSystemPath` | C++ \| Lua |
| `read8` | C++ \| Lua |
| `read16` | C++ \| Lua |
| `read32` | C++ \| Lua |
| `eof` | C++ \| Lua |
| `length` | C++ \| Lua |
| `seek` | C++ \| Lua |
| `pos` | C++ \| Lua |
| `readString` | C++ \| Lua |
| `writeString` | C++ \| Lua |
