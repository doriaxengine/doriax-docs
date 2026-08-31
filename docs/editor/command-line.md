---
description: Run Doriax exports and shader generation from the command line for automation and CI/CD.
---

# Command-Line Tools

The `doriax-editor` executable doubles as a **headless command-line tool**. When the
first argument is a known subcommand, the editor runs that command and exits without ever
opening a window — ideal for build servers, scripted releases, and CI/CD pipelines.

```bash
doriax-editor export   --project <path> --out <dir> [options]
doriax-editor shaders  --out <dir> --shader <spec> [options]
```

Running `doriax-editor` with **no arguments** launches the normal graphical editor.
`--help`, `-h` or `help` print the top-level usage. Anything else is reported as an
unrecognized argument and exits with code `2`, so a mistyped subcommand fails instead of
opening a window.

!!! note "Windows: two executables"
    Windows builds ship both. `doriax-editor.exe` is a GUI application — it re-attaches
    to the parent console so subcommand output still appears in your terminal, but `cmd`
    and PowerShell do not wait for a GUI application, so the prompt returns before the
    command finishes and its exit code never reaches you. `doriax-editor-cmd.exe` is the
    same program linked as a console application: use it for scripting and CI. Both
    accept the same subcommands, and both open the editor when given no arguments.

On Linux and macOS there is a single binary, and the subcommands run before the window
backend starts, so they work on headless machines.

!!! note "macOS: the binary is inside the app bundle"
    The editor ships as `Doriax.app`, so the command-line entry point is
    `Doriax.app/Contents/MacOS/Doriax`:

    ```bash
    /Applications/Doriax.app/Contents/MacOS/Doriax export \
      --project ./MyGame --out ./build/MyGame
    ```

    Alias it or add that directory to your `PATH` if you use it often.

## `export` — build a project to a target

Serializes scenes, generates the C++ glue and bundle factories, compiles shaders, copies
assets and the engine runtime, and writes a self-contained, buildable project directory —
the same output as the [Export Window](export.md), but scriptable.

```bash
doriax-editor export --project ./MyGame --out ./build/MyGame --backend vulkan
```

### Options

| Option | Description |
| --- | --- |
| `-p`, `--project <path>` | **Required.** Project directory or a `project.yaml` file. |
| `-o`, `--out <path>` | **Required** (unless `--list-scenes`). Destination directory. Must be empty. |
| `--assets <path>` | Asset directory, relative to the project or absolute. Defaults to the project's asset directory. |
| `--lua <path>` | Lua directory, relative to the project or absolute. Defaults to the project's Lua directory. |
| `--start-scene <id\|name>` | Override the start scene by numeric ID, scene name, or file stem. |
| `--backend <list>` | Graphic backend(s) to compile shaders for. Repeatable, or a list (see below). Defaults to **all** supported backends. |
| `--shader <spec>` | Shader(s) to compile. Repeatable (see [Shader specs](#shader-specs)). If omitted, shaders discovered while regenerating scenes are exported. |
| `--list-scenes` | Print the project's scenes (`id`, `name`, `path`) and exit. |
| `-h`, `--help` | Show usage for this subcommand. |

Asset references are stored relative to the directories configured in the project, so
`--assets` and `--lua` only make sense when they point at those same folders. Exporting a
different root ships files the stored paths do not resolve against.

### List a project's scenes

Useful for discovering a start-scene ID before exporting:

```bash
doriax-editor export --project ./MyGame --list-scenes
# 1   MainMenu   scenes/main_menu.scene
# 2   Level01    scenes/level_01.scene
```

## `shaders` — generate shader files standalone

Compiles shader variants directly to an output directory, without exporting a whole
project. Use it to pre-bake a shader cache or produce shader data for custom tooling.

```bash
doriax-editor shaders --out ./shaders --shader mesh:Uv1,Nor --backend opengles
```

### Options

| Option | Description |
| --- | --- |
| `-o`, `--out <path>` | **Required.** Destination directory for the generated shader files. |
| `--format <format>` | Output format: `binary` (default, also `sdat`), `header`, or `json`. |
| `--backend <list>` | Graphic backend(s) to compile for. Repeatable or a list. Defaults to **all** supported backends. |
| `--shader <spec>` | **Required.** Shader(s) to generate. Repeatable (see [Shader specs](#shader-specs)). |
| `-h`, `--help` | Show usage for this subcommand. |

## Graphic backends

A shader is compiled for a **graphics API**, not for an operating system — a Windows build
needs GLSL, HLSL, or SPIR-V depending only on how it was configured. Both subcommands
accept these backend names (case-insensitive):

| Value | Alias | Shader format |
| --- | --- | --- |
| `opengl` | `glcore` | `glsl410` |
| `opengles` | `gles3` | `glsl300es` |
| `d3d11` | | `hlsl5` |
| `metal-macos` | `metal` | `msl21macos` |
| `metal-ios` | | `msl21ios` |
| `vulkan` | | `spirv10` |
| `all` | | selects every supported backend |

One file is written per shader and backend, named `<shader>_<format>`. At startup the
runtime loads the format matching the backend it was built with, so an export must include
every backend the final binary may use — see
[Choosing backends](export.md#choosing-backends).

Pass `--backend` multiple times, or give a single list separated by `,`, `+`, `|`, or
`;`:

```bash
doriax-editor export -p ./MyGame -o ./build --backend vulkan --backend opengl
doriax-editor export -p ./MyGame -o ./build --backend "vulkan,opengl,opengles"
```

## Shader specs

A `--shader` value is a **shader type** with optional **properties**, separated by a
colon:

```
<type>[:<properties>]
```

- **Type** (case-insensitive): `points`, `lines`, `mesh`, `sky` (or `skybox`), `depth`,
  `ui`, `postprocess` (or `post`).
- **Properties** are either:
    - a comma-separated list of property names, e.g. `mesh:Uv1,Nor`, or
    - a numeric bitmask, e.g. `mesh:0x3` or `mesh:12`.

Property names come from the engine's shader system for that shader type; an unknown
property or type is reported as an error. Omit the properties to generate the base
variant of a type (e.g. `--shader depth`).

```bash
# Base mesh shader plus a UV+normal variant, for WebGL 2 and Direct3D 11
doriax-editor shaders --out ./shaders \
  --shader mesh \
  --shader mesh:Uv1,Nor \
  --backend opengles --backend d3d11
```

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success. |
| `1` | Runtime failure (project failed to load, export/shader build error). The error is printed to `stderr`. |
| `2` | Invalid or unrecognized arguments. The error is printed to `stderr`, usage to `stdout`. |

## Use in CI/CD

Because the commands are headless and return meaningful exit codes, they drop straight
into a pipeline. On Windows runners call `doriax-editor-cmd`: the default PowerShell
shell does not wait for the GUI binary, so the step can pass even when the export
failed. Example GitHub Actions step:

```yaml
- name: Export game (Vulkan + WebGL 2)
  run: |
    doriax-editor export \
      --project ./MyGame \
      --out ./build/MyGame \
      --backend "vulkan,opengles"
```

The exported directory still needs its native toolchain to produce final binaries — see
[Platform toolchains](export.md#platform-toolchains) and
[Building from Source](../building/overview.md).

## See also

- [Export Window](export.md) — the graphical equivalent and full export pipeline.
- [Build Options](../reference/build-options.md) — CMake flags for the generated project.
