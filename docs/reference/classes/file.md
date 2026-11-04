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

## Failed opens

`open` returns a `FileErrors` value, and the `File(path, write)` constructor logs an
error when the file can't be opened. A `File` without an open file acts like an empty
one: reads and writes return `0` or an empty string, and `eof` is true. To tell a
missing file from an empty one, check what `open` returns:

=== "Lua"

    ```lua
    local save = File()
    if save:open("data://save.dat") ~= FileErrors.FILEDATA_OK then
        -- no save yet
    end
    ```

=== "C++"

    ```cpp
    File save;
    if (save.open("data://save.dat") != FileErrors::FILEDATA_OK) {
        // no save yet
    }
    ```

`close` is safe to call more than once, and the file closes itself when the object is
destroyed. In C++ a `File` owns its handle, so it can't be copied.
