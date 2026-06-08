---
description: Texture API reference (C++ and Lua).
---

# Texture

**C++ type:** `Texture`

## Description

Represents a GPU texture resource. `Texture` supports 2D textures, cube maps, and framebuffer textures, covering the full range from loading a simple PNG file to driving a render-to-texture pipeline.

A `Texture` object is a lightweight handle; the actual GPU resource is managed internally by the texture pool and shared between objects that reference the same file path. Textures are loaded lazily — the GPU upload happens the first time the texture is needed for rendering.

`Texture` is most commonly used as a field in [Material](material.md) or passed to `Mesh::setTexture()`.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [TextureFilter](#texturefilter) | [minFilter](#minfilter-magfilter) | `LINEAR` | C++ \| Lua |
| [TextureFilter](#texturefilter) | [magFilter](#minfilter-magfilter) | `LINEAR` | C++ \| Lua |
| [TextureWrap](#texturewrap) | [wrapU](#wrapu-wrapv) | `REPEAT` | C++ \| Lua |
| [TextureWrap](#texturewrap) | [wrapV](#wrapu-wrapv) | `REPEAT` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setPath](#setpath) | C++ \| Lua |
| void | [setData](#setdata) | C++ \| Lua |
| void | [setId](#setid) | C++ \| Lua |
| void | [setCubeMap](#setcubemap) | C++ \| Lua |
| void | [setCubePaths](#setcubepaths) | C++ \| Lua |
| void | [setCubeDatas](#setcubedatas) | C++ \| Lua |
| [TextureLoadResult](textureloadresult.md) | [load](#load) | C++ \| Lua |
| void | [destroy](#destroy) | C++ \| Lua |
| std::string | [getPath](#getpath) | C++ \| Lua |
| std::string | [getId](#getid) | C++ \| Lua |
| unsigned int | [getWidth](#getwidth-getheight) | C++ \| Lua |
| unsigned int | [getHeight](#getwidth-getheight) | C++ \| Lua |
| bool | [isTransparent](#istransparent) | C++ \| Lua |
| bool | [isCubeMap](#iscubemap) | C++ \| Lua |
| bool | [empty](#empty) | C++ \| Lua |
| bool | [isFramebuffer](#isframebuffer) | C++ \| Lua |
| void | [releaseData](#releasedata) | C++ \| Lua |

## Enumerations

### TextureFilter

Filtering modes applied when the texture is sampled at a scale different from its native resolution.

* **NEAREST** — No interpolation (nearest-neighbour). Produces a pixelated look; useful for pixel art.
* **LINEAR** — Bilinear interpolation between the four nearest texels.
* **NEAREST_MIPMAP_NEAREST** — Nearest-neighbour within the nearest mipmap level.
* **NEAREST_MIPMAP_LINEAR** — Nearest-neighbour, with linear interpolation between mipmap levels.
* **LINEAR_MIPMAP_NEAREST** — Bilinear within the nearest mipmap level.
* **LINEAR_MIPMAP_LINEAR** — Trilinear filtering (bilinear + mipmap interpolation). Best quality for 3D surfaces.

---

### TextureWrap

Controls what happens when UV coordinates fall outside the `[0, 1]` range.

* **REPEAT** — The texture tiles continuously. Default for most use cases.
* **MIRRORED_REPEAT** — The texture tiles but mirrors on every repeat, producing a seamless look.
* **CLAMP_TO_EDGE** — UV values are clamped; the edge pixel is stretched.
* **CLAMP_TO_BORDER** — UV values outside `[0, 1]` sample a fixed border colour.

---

## Property details

### minFilter / magFilter

* *Setter*: void **setMinFilter**([TextureFilter](#texturefilter) filter)
* *Getter*: [TextureFilter](#texturefilter) **getMinFilter**() const
* *Setter*: void **setMagFilter**([TextureFilter](#texturefilter) filter)
* *Getter*: [TextureFilter](#texturefilter) **getMagFilter**() const

`minFilter` applies when the texture is rendered smaller than its native resolution (minification). `magFilter` applies when it is rendered larger (magnification). Only `NEAREST` and `LINEAR` are valid values for `magFilter`.

---

### wrapU / wrapV

* *Setter*: void **setWrapU**([TextureWrap](#texturewrap) wrapU)
* *Getter*: [TextureWrap](#texturewrap) **getWrapU**() const
* *Setter*: void **setWrapV**([TextureWrap](#texturewrap) wrapV)
* *Getter*: [TextureWrap](#texturewrap) **getWrapV**() const

Wrapping mode along the horizontal (U) and vertical (V) texture coordinates.

---

## Method details

### setPath

* void **setPath**(const std::string& path)

Sets the file path for a 2D texture. The file is not loaded immediately; loading is deferred to the first time the texture is needed for rendering.

=== "C++"
    ```cpp
    Texture tex;
    tex.setPath("textures/wall.png");
    material.baseColorTexture = tex;
    ```

=== "Lua"
    ```lua
    local tex = Texture()
    tex:setPath("textures/wall.png")
    material.baseColorTexture = tex
    ```

Alternatively, pass the path directly to the constructor: `Texture("textures/wall.png")`.

---

### setData

* void **setData**(const std::string& id, TextureData data)

Creates a texture from in-memory pixel data ([TextureData](texturedata.md)). The `id` is an arbitrary string used as a cache key; using the same id for identical pixel data avoids uploading duplicates.

=== "C++"
    ```cpp
    TextureData td;
    td.loadTextureData("textures/icon.png");

    Texture tex;
    tex.setData("icon", td);
    ```

=== "Lua"
    ```lua
    local td = TextureData()
    td:loadTextureData("textures/icon.png")

    local tex = Texture()
    tex:setData("icon", td)
    ```

---

### setId

* void **setId**(const std::string& id)

Manually assigns a cache key without providing pixel data. Useful for referencing a texture that is already in the pool from another code path.

---

### setCubeMap

* void **setCubeMap**(const std::string& path)

Convenience overload that treats `path` as a directory containing six face images in the conventional naming format (`front`, `back`, `left`, `right`, `up`, `down`). Exact naming depends on the engine's convention.

---

### setCubePaths

* void **setCubePaths**(const std::string& front, const std::string& back, const std::string& left, const std::string& right, const std::string& up, const std::string& down)

Loads a cube map from six individual image files. Typically used for skyboxes or environment reflections.

=== "C++"
    ```cpp
    Texture sky;
    sky.setCubePaths("sky/px.png", "sky/nx.png",
                     "sky/ny.png", "sky/py.png",
                     "sky/pz.png", "sky/nz.png");
    ```

=== "Lua"
    ```lua
    local sky = Texture()
    sky:setCubePaths("sky/px.png", "sky/nx.png",
                     "sky/ny.png", "sky/py.png",
                     "sky/pz.png", "sky/nz.png")
    ```

---

### setCubeDatas

* void **setCubeDatas**(const std::string& id, TextureData front, TextureData back, TextureData left, TextureData right, TextureData up, TextureData down)

Creates a cube-map texture from six in-memory [TextureData](texturedata.md) faces. The `id` is used as a pool cache key.

---

### load

* [TextureLoadResult](textureloadresult.md) **load**()

Forces an immediate CPU-side load of the texture data from disk. This is normally not required because loading is deferred, but you can call it to pre-warm assets during a loading screen.

---

### destroy

* void **destroy**()

Releases the GPU resource and removes the texture from the pool. After calling this, the texture object is empty.

---

### getPath

* std::string **getPath**(size_t index = 0) const

Returns the file path associated with this texture. For cube maps, `index` selects the face (0 = front, 1 = back, 2 = left, 3 = right, 4 = up, 5 = down).

---

### getId

* std::string **getId**() const

Returns the internal cache key used to identify this texture in the pool.

---

### getWidth / getHeight

* unsigned int **getWidth**() const
* unsigned int **getHeight**() const

Returns the pixel dimensions of the loaded texture. Returns `0` if the texture has not been loaded yet.

---

### isTransparent

* bool **isTransparent**() const

Returns `true` if the texture image contains pixels with alpha below `1.0`. Used internally by the engine to determine whether the owning mesh should be rendered in the transparent pass.

---

### isCubeMap

* bool **isCubeMap**() const

Returns `true` if this texture is a cube map (six faces).

---

### empty

* bool **empty**() const

Returns `true` if no path, data, or framebuffer has been assigned to this texture.

---

### isFramebuffer

* bool **isFramebuffer**() const

Returns `true` if this texture was created from a [Framebuffer](framebuffer.md) (render-to-texture).

---

### releaseData

* void **releaseData**()

Frees the CPU-side pixel data after it has been uploaded to the GPU. Reduces memory usage on platforms with limited RAM. The texture remains valid for rendering.
