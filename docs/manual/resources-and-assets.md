---
description: Resource loading, asset formats, runtime pools, file I/O, and user settings in Doriax.
---

# Resources & Assets

Doriax projects combine editor-managed resources with runtime pools and file helpers.
Assets are authored or imported in the editor, copied and transformed during export,
then loaded on demand by the runtime as needed.

## Asset types

| Asset type | Formats | Loaded by |
| --- | --- | --- |
| **Textures** | PNG, JPG, TGA, BMP, PSD, HDR, SVG | `Texture`, texture pools |
| **3D Models** | GLTF, GLB, OBJ | `Model`, `MeshSystem` |
| **Materials** | Engine `.material` files (YAML) | `Material` struct, linked from mesh submeshes |
| **Audio** | OGG, WAV, MP3, FLAC | `SoundPool`, `Sound` |
| **Fonts** | TTF, OTF, TTC | Font pool, `Text` components |
| **Shaders** | Shader data (engine format) | `ShaderPool`, `RenderSystem` |
| **Scenes** | YAML scene files | `SceneManager` |
| **Bundles** | YAML bundle files | `BundleManager` |

## Path roots

A path handed to the engine is resolved against a root, chosen by its scheme:

| Scheme | Root | Holds |
| --- | --- | --- |
| `asset://`, or no scheme | Assets directory | Textures, models, sounds, fonts |
| `lua://` | Lua directory | Lua modules and script entries |
| `shader://` | Compiled shader directory | `.sdat` shader data |
| `data://` | Writable user data directory | Saves and settings |

Both project directories are set in
[Project Settings](../editor/project-workflow.md#assets-and-lua-directories) and default to
the project root. Paths are stored relative to their root, so `sprites/hero.png` means
`<assets directory>/sprites/hero.png` in the editor and `assets/sprites/hero.png` next to
an exported executable. Absolute paths are used as given.

A leading `..` never escapes a root: it is dropped while the path is normalized, so keep
every referenced file inside the assets directory.

## Loading assets at runtime

Most high-level objects accept a file path and load the resource automatically:

=== "Lua"

    ```lua
    -- Texture loaded by a Sprite
    sprite = Sprite(scene)
    sprite:setTexture("sprites/hero.png")

    -- Model loaded from GLTF
    model = Model(scene)
    model:loadGLTF("models/hero.gltf")

    -- Sound loaded by Sound object
    sfx = Sound(scene)
    sfx:loadSound("audio/jump.ogg")
    ```

=== "C++"

    ```cpp
    Sprite sprite(&scene);
    sprite.setTexture("sprites/hero.png");

    Model model(&scene);
    model.loadGLTF("models/hero.gltf");

    Sound sfx(&scene);
    sfx.loadSound("audio/jump.ogg");
    ```

## Vector images (SVG)

`.svg` files are treated as textures: they are **rasterized to RGBA when loaded**, so they
work anywhere a raster texture does — sprites, UI images, and material maps. Only the
features of the bundled rasterizer are drawn (basic shapes, paths, solid and gradient fills,
and strokes); there is no text or filter/effect support, so convert text to paths when
authoring.

By default an SVG is rasterized at its intrinsic size (the `width`/`height` or `viewBox` in
the file). Because a vector is resolution-independent, you can rasterize it larger for crisp
results on high-DPI displays or when the image is drawn bigger than its native size. The
rasterization scale is set per texture (`2.0` = twice the intrinsic resolution) and has no
effect on raster images:

=== "Lua"

    ```lua
    local data = TextureData()
    data.svgScale = 4
    data:loadTextureFromFile("ui/icon.svg")  -- a 24x24 SVG -> 96x96 texture
    ```

=== "C++"

    ```cpp
    TextureData data;
    data.setSVGScale(4.0f);
    data.loadTextureFromFile("ui/icon.svg");  // a 24x24 SVG -> 96x96 texture
    ```

The scale can also be set directly on a `Texture` reference — `svgScale` in Lua,
`setSvgScale()` in C++ (see [Texture](../reference/classes/texture.md#svgscale)):

=== "Lua"

    ```lua
    local icon = Texture("ui/icon.svg")
    icon.svgScale = 4  -- a 24x24 SVG -> 96x96 texture
    ```

=== "C++"

    ```cpp
    Texture icon("ui/icon.svg");
    icon.setSvgScale(4.0f);  // a 24x24 SVG -> 96x96 texture
    ```

The property is saved with the scene and applied in exported projects, and because the
scale is part of the texture's identity, different slots can use the same SVG at different
resolutions. This is what the editor's per-slot **SVG Scale** control edits; see
[Properties — texture fields](../editor/properties.md). The legacy path form
`"ui/icon.svg?svgScale=4"` is still accepted and absorbed into the property when the path
is set. The rasterized size is capped to a GPU-friendly limit, so very large scales are
rejected rather than allocated.

## Material files

`.material` files store PBR parameters outside scene YAML so many meshes can reference
one definition. Each file lists colour factors, metallic/roughness scalars, and relative
texture paths — the same fields as the [Material](../reference/classes/material.md)
struct.

In the editor, drag a material preview from **Properties** into the **Resources Browser**
to create a file, or drag an existing `.material` from the browser onto a mesh to link
it. Linked materials reload when the file changes. See
[Resources Browser — Material files](../editor/resources.md#material-files).

At runtime, linked materials are resolved when the scene loads; exported games bundle
the referenced textures and material data like any other asset.

## Runtime pools

Pools avoid loading the same resource data twice and centralize ownership. Objects that
use the same file path share the underlying data.

| Pool | Managed resource |
| --- | --- |
| `TextureDataPool` | Raw decoded texture data (pixels) |
| `TexturePool` | GPU-side texture handles |
| `ModelPool` | Parsed 3D model and skeleton data |
| `ShaderPool` | Compiled shader programs |
| `SoundPool` | Loaded audio data |
| `FontPool` | Parsed font data |

Pools are managed internally. You normally interact with them through high-level objects
(`Sprite`, `Model`, `Sound`), but you can query pool state or pre-warm a pool
for level loading.

For C++ teardown code, `Engine::clearUnusedPools()` releases entries that are owned
only by their pool and preserves resources still referenced by active scenes or engine
objects. `Engine::clearPools()` empties every pool and destroys pooled GPU textures and
shaders, so reserve it for engine or graphics-view shutdown. If asynchronous model
loads may still be running, call `MeshSystem::cancelAllAsyncModelLoads()` before either
cleanup operation; cancellation waits for the active worker tasks to finish before it
returns.

The editor performs the safe sequence automatically when you switch projects: it
quiesces project-specific background work, destroys the old scenes, and then clears
unreferenced pool entries.

See [Engine](../reference/classes/engine.md#clearunusedpools) and
[MeshSystem](../reference/classes/meshsystem.md#asynchronous-model-load-control) for the
complete C++ API.

## File I/O

`FileData` is the abstract base for byte-level access; `File` reads and writes files on
disk and `Data` wraps an in-memory buffer. All three share `readString`, `writeString`,
`read8/16/32`, `seek`, `pos`, `length`, and `eof`.

=== "Lua"

    ```lua
    -- Read a file into memory (second argument: open for writing)
    local f = File("saves/player.dat", false)
    local contents = f:readString()
    f:close()

    -- Write
    local out = File("saves/player.dat", true)
    out:writeString(contents)
    out:flush()
    out:close()
    ```

=== "C++"

    ```cpp
    File file("saves/player.dat", false);
    std::string contents = file.readString();
    file.close();
    ```

File paths follow the same roots as the rest of the engine: a relative path resolves
against the assets directory, and absolute paths are used as given. On mobile and web,
write-accessible directories are separate from read-only resource paths — use
`System.getUserDataPath()` (`data://`) for player save data, and `System.getAssetPath()`
for read-only bundled assets.

## User settings

`UserSettings` persists key/value pairs using each platform's native preferences
storage. It is suited for player preferences, audio/video settings, and small game
state. The API is typed — use the matching `set…ForKey` / `get…ForKey` pair for `Bool`,
`Integer`, `Long`, `Float`, `Double`, `String`, or `Data`:

=== "Lua"

    ```lua
    UserSettings.setFloatForKey("volume", 0.8)
    UserSettings.setBoolForKey("fullscreen", true)

    local vol = UserSettings.getFloatForKey("volume", 1.0)  -- second arg is the default
    UserSettings.removeKey("obsoleteSetting")
    ```

=== "C++"

    ```cpp
    UserSettings::setFloatForKey("volume", 0.8f);
    UserSettings::setBoolForKey("fullscreen", true);

    float vol = UserSettings::getFloatForKey("volume", 1.0f);
    ```

Keep heavy save data (inventory, world state) in custom binary or JSON files. Reserve
`UserSettings` for small configuration.

## Asset path best practices

| Guideline | Reason |
| --- | --- |
| Use lowercase file names | Avoids case-sensitivity issues on Linux and Android |
| No spaces in paths | Prevents build and script path parsing issues |
| Keep source and generated output separate | Generated export data should not be committed to version control |
| Use relative paths from the assets directory | Paths remain valid across machines and in exported builds |
| Keep referenced files inside the assets directory | A path outside it cannot be stored or shipped |
| Prefer GLTF for animated 3D assets | Carries mesh, materials, skeleton, animations, and morph targets |
| Compress textures for mobile and web | Keeps bundle sizes manageable |

## Export and asset packaging

At export time the editor copies the **contents** of the assets and Lua directories into
the `assets` and `lua` folders of the output, which is what the runtime reads relative to
the executable. Shaders are compiled for the target platform. The source project folder is
not modified.

See [Export Window](../editor/export.md) for details on the export pipeline.

## See also

- [Texture](../reference/classes/texture.md)
- [Model](../reference/classes/model.md)
- [Sound](../reference/classes/sound.md)
- [Data](../reference/classes/data.md)
- [UserSettings](../reference/classes/usersettings.md)
- [BundleManager](../reference/classes/bundlemanager.md)
- [Resources Browser](../editor/resources.md)
