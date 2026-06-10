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

Running `doriax-editor` with **no subcommand** launches the normal graphical editor.

!!! note "Same binary, no GUI"
    There is no separate command-line build. The subcommands run before the window
    backend starts, so they work on headless machines. On Windows the GUI binary
    re-attaches to the parent console so output appears in your terminal.

## `export` — build a project to a target

Serializes scenes, generates the C++ glue and bundle factories, compiles shaders, copies
assets and the engine runtime, and writes a self-contained, buildable project directory —
the same output as the [Export Window](export.md), but scriptable.

```bash
doriax-editor export --project ./MyGame --out ./build/MyGame --platform linux
```

### Options

| Option | Description |
| --- | --- |
| `-p`, `--project <path>` | **Required.** Project directory or a `project.yaml` file. |
| `-o`, `--out <path>` | **Required** (unless `--list-scenes`). Destination directory. Must be empty. |
| `--assets <path>` | Asset directory, relative to the project or absolute. Defaults to the project's asset directory. |
| `--lua <path>` | Lua directory, relative to the project or absolute. Defaults to the project's Lua directory. |
| `--start-scene <id\|name>` | Override the start scene by numeric ID, scene name, or file stem. |
| `--platform <list>` | Target platform(s). Repeatable, or a list (see below). Defaults to **all** supported platforms. |
| `--shader <spec>` | Shader(s) to compile. Repeatable (see [Shader specs](#shader-specs)). If omitted, shaders discovered while regenerating scenes are exported. |
| `--list-scenes` | Print the project's scenes (`id`, `name`, `path`) and exit. |
| `-h`, `--help` | Show usage for this subcommand. |

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
doriax-editor shaders --out ./shaders --shader mesh:Uv1,Nor --platform web
```

### Options

| Option | Description |
| --- | --- |
| `-o`, `--out <path>` | **Required.** Destination directory for the generated shader files. |
| `--format <format>` | Output format: `binary` (default, also `sdat`), `header`, or `json`. |
| `--platform <list>` | Target platform(s). Repeatable or a list. Defaults to **all** supported platforms. |
| `--shader <spec>` | **Required.** Shader(s) to generate. Repeatable (see [Shader specs](#shader-specs)). |
| `-h`, `--help` | Show usage for this subcommand. |

## Platforms

Both subcommands accept these platform names (case-insensitive), with aliases:

| Value | Aliases |
| --- | --- |
| `linux` | |
| `windows` | `win` |
| `macos` | `mac` |
| `ios` | |
| `android` | |
| `web` | `wasm`, `emscripten` |
| `all` | selects every supported platform |

Pass `--platform` multiple times, or give a single list separated by `,`, `+`, `|`, or
`;`:

```bash
doriax-editor export -p ./MyGame -o ./build --platform windows --platform linux
doriax-editor export -p ./MyGame -o ./build --platform "windows,linux,web"
```

## Shader specs

A `--shader` value is a **shader type** with optional **properties**, separated by a
colon:

```
<type>[:<properties>]
```

- **Type** (case-insensitive): `points`, `lines`, `mesh`, `sky` (or `skybox`), `depth`,
  `ui`.
- **Properties** are either:
    - a comma-separated list of property names, e.g. `mesh:Uv1,Nor`, or
    - a numeric bitmask, e.g. `mesh:0x3` or `mesh:12`.

Property names come from the engine's shader system for that shader type; an unknown
property or type is reported as an error. Omit the properties to generate the base
variant of a type (e.g. `--shader depth`).

```bash
# Base mesh shader plus a UV+normal variant, for web and Windows
doriax-editor shaders --out ./shaders \
  --shader mesh \
  --shader mesh:Uv1,Nor \
  --platform web --platform windows
```

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success. |
| `1` | Runtime failure (project failed to load, export/shader build error). The error is printed to `stderr`. |
| `2` | Invalid arguments. Usage is printed to `stderr`. |

## Use in CI/CD

Because the commands are headless and return meaningful exit codes, they drop straight
into a pipeline. Example GitHub Actions step:

```yaml
- name: Export game (Linux + Web)
  run: |
    doriax-editor export \
      --project ./MyGame \
      --out ./build/MyGame \
      --platform "linux,web"
```

The exported directory still needs its native toolchain to produce final binaries — see
[Platform toolchains](export.md#platform-toolchains) and
[Building from Source](../building/overview.md).

## See also

- [Export Window](export.md) — the graphical equivalent and full export pipeline.
- [Build Options](../reference/build-options.md) — CMake flags for the generated project.
