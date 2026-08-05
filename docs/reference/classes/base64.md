---
description: Base64 API reference (C++ only).
---

# Base64

**C++ type:** `Base64`

## Description

Static helpers for encoding and decoding binary data as base64 strings. Useful for
embedding small payloads in JSON/YAML or for network/save serialization.

`encode` and `decode` are **C++ only** — they are not exposed to Lua yet.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static std::string | encode | C++ |
| static std::vector&lt;unsigned char&gt; | decode | C++ |
