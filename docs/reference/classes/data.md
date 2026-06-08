---
description: Data API reference (C++ and Lua).
---

# Data

**Inherits:** FileData  
**C++ type:** `Data`

## Description

An in-memory byte buffer that implements the `FileData` streaming interface. It can be loaded from a file path, from a raw byte pointer, or from another [File](file.md) object. Once loaded, it supports sequential read/write operations and random seek access.

`Data` is used by the engine for audio sample loading, asset bundling, and anywhere that in-memory file-like access is needed.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| unsigned int | [open](#open) | C++ \| Lua |
| int | [eof](#eof) | C++ \| Lua |
| unsigned int | [read](#read-write) | C++ \| Lua |
| unsigned int | [write](#read-write) | C++ \| Lua |
| unsigned int | [length](#length) | C++ \| Lua |
| void | [seek](#seek) | C++ \| Lua |
| unsigned int | [pos](#pos) | C++ \| Lua |

## Method details

### open

* unsigned int **open**(unsigned char* aData, unsigned int aDataLength, bool aCopy = false, bool aTakeOwnership = true)
* unsigned int **open**(const char* aFilename)
* unsigned int **open**(File* aFile)

Loads data from a raw byte pointer, a file path, or a [File](file.md) object. When `aCopy` is `true`, the data is duplicated into an internal buffer; when `aTakeOwnership` is `true`, the `Data` object takes ownership of the provided pointer.

---

### eof

* int **eof**()

Returns non-zero if the read cursor is at or past the end of the buffer.

---

### read / write

* unsigned int **read**(unsigned char* aDst, unsigned int aBytes)
* unsigned int **write**(unsigned char* aSrc, unsigned int aBytes)

Read or write `aBytes` bytes at the current cursor position. Returns the number of bytes actually transferred.

---

### length

* unsigned int **length**()

Returns the total size of the buffer in bytes.

---

### seek

* void **seek**(int aOffset)

Moves the read/write cursor to `aOffset` bytes from the beginning.

---

### pos

* unsigned int **pos**()

Returns the current cursor position.
