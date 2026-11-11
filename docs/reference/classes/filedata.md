---
description: FileData API reference (C++ and Lua).
---

# FileData

Abstract streaming interface shared by [File](file.md) and [Data](data.md).

`newFile` constructs the concrete type. Pass `useHandle = true` to request a disk
`File`; omit it or pass `false` for an in-memory `Data` buffer. In a native export with
resource packing enabled, a packed path still returns `Data` even when a handle was
requested, because a packed entry has no filesystem file to open.

In Lua, the object is released when it is collected, which also closes a file, and it
comes back as a `FileData`: the methods of this page work on it, the ones only `File` or
`Data` have don't. In C++ you own the returned pointer and must `delete` it.

`seek` and `eof` work the same on both types: a negative offset counts back from the
end, and `eof` is true right after the last byte. Only a `File` can move past the end,
to write after a gap. On a pipe or FIFO, `eof` never waits for data, so it only turns
true after a read has hit the end.

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
