---
description: Log API reference — console output and log levels (C++ and Lua).
---

# Log

## Description

`Log` provides static methods for writing messages to the platform console or log sink. Output goes to the IDE console during editor play mode, and to `stdout`/`logcat`/Xcode console on each platform. All methods accept `printf`-style format strings.

In Lua, the global `print()` function is also available as an alias for `Log.print`.

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Log::print("Player health: %d", health);
    Log::warn("Physics body not loaded yet!");
    ```

=== "Lua"

    ```lua
    Log.print("Player health: " .. health)
    Log.warn("Physics body not loaded yet!")
    -- or use the Lua global:
    print("Hello from script")
    ```

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| static void | [print](#print) | C++ \| Lua |
| static void | [verbose](#verbose) | C++ \| Lua |
| static void | [debug](#debug) | C++ \| Lua |
| static void | [warn](#warn) | C++ \| Lua |
| static void | [error](#error) | C++ \| Lua |

## Log levels

The engine filters messages based on the build configuration (defined in `System.h`):

| Macro | Level | Description |
| --- | --- | --- |
| `S_LOG_VERBOSE` | 1 | Detailed trace information; typically disabled in release builds. |
| `S_LOG_DEBUG` | 2 | Debug-level messages useful during development. |
| `S_LOG_WARN` | 3 | Non-fatal warnings that may indicate incorrect usage. |
| `S_LOG_ERROR` | 4 | Errors that require attention; may terminate the operation. |

## Method details

### print

* `static void print(const char* text, ...)`

Writes a plain message to the log with no severity prefix. Use for general informational output and debugging.

=== "C++"

    ```cpp
    Log::print("Score: %d  Time: %.2f", score, elapsed);
    ```

=== "Lua"

    ```lua
    Log.print("Score: " .. score .. "  Time: " .. string.format("%.2f", elapsed))
    -- or:
    print("Score:", score)
    ```

---

### verbose

* `static void verbose(const char* text, ...)`

Logs a `VERBOSE`-level message. Typically compiled out in release; use for high-frequency trace output such as per-frame diagnostics.

=== "C++"

    ```cpp
    Log::verbose("Frame %d: entity count = %zu", frame, scene.getEntityCount());
    ```

=== "Lua"

    ```lua
    Log.verbose("Frame " .. frame .. ": entity count = " .. count)
    ```

---

### debug

* `static void debug(const char* text, ...)`

Logs a `DEBUG`-level message. Use for state dumps, object creation, and lifecycle tracking during active development.

=== "C++"

    ```cpp
    Log::debug("Enemy spawned at (%.1f, %.1f)", x, y);
    ```

=== "Lua"

    ```lua
    Log.debug("Enemy spawned at " .. x .. ", " .. y)
    ```

---

### warn

* `static void warn(const char* text, ...)`

Logs a `WARN`-level message. Use for recoverable issues: missing optional resources, fallback paths taken, or unexpected but non-fatal conditions.

=== "C++"

    ```cpp
    if (!body.isEnabled()) {
        Log::warn("Trying to apply force to a disabled body (entity %u)", entity);
    }
    ```

=== "Lua"

    ```lua
    if not body:isEnabled() then
        Log.warn("Trying to apply force to a disabled body")
    end
    ```

---

### error

* `static void error(const char* text, ...)`

Logs an `ERROR`-level message. Use for critical failures that prevent correct execution.

=== "C++"

    ```cpp
    if (!mesh.load()) {
        Log::error("Failed to load mesh for entity %u", entity);
    }
    ```

=== "Lua"

    ```lua
    if not mesh:load() then
        Log.error("Failed to load mesh")
    end
    ```
