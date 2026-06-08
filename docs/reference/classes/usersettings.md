---
description: UserSettings API reference (C++ and Lua).
---

# UserSettings

**C++ type:** `UserSettings` (static)

## Description

A cross-platform key-value store for persistent user preferences. Values survive app restarts and are stored in a platform-appropriate location (e.g. `SharedPreferences` on Android, `NSUserDefaults` on iOS, a settings file on desktop platforms).

Supported value types: `bool`, `int`, `long`, `float`, `double`, `std::string`, and `Data`.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static bool | [getBoolForKey](#get-methods) | C++ \| Lua |
| static int | [getIntegerForKey](#get-methods) | C++ \| Lua |
| static long | [getLongForKey](#get-methods) | C++ \| Lua |
| static float | [getFloatForKey](#get-methods) | C++ \| Lua |
| static double | [getDoubleForKey](#get-methods) | C++ \| Lua |
| static std::string | [getStringForKey](#get-methods) | C++ \| Lua |
| static [Data](data.md) | [getDataForKey](#get-methods) | C++ \| Lua |
| static void | [setBoolForKey](#set-methods) | C++ \| Lua |
| static void | [setIntegerForKey](#set-methods) | C++ \| Lua |
| static void | [setLongForKey](#set-methods) | C++ \| Lua |
| static void | [setFloatForKey](#set-methods) | C++ \| Lua |
| static void | [setDoubleForKey](#set-methods) | C++ \| Lua |
| static void | [setStringForKey](#set-methods) | C++ \| Lua |
| static void | [setDataForKey](#set-methods) | C++ \| Lua |
| static void | [removeKey](#removekey) | C++ \| Lua |

## Method details

### get methods

* static T **get\<Type\>ForKey**(const char* key)
* static T **get\<Type\>ForKey**(const char* key, T defaultValue)

Retrieve a stored value by key. If the key does not exist and no `defaultValue` is given, the zero/empty value for the type is returned.

=== "C++"
    ```cpp
    int volume = UserSettings::getIntegerForKey("volume", 80);
    bool musicEnabled = UserSettings::getBoolForKey("music", true);
    std::string playerName = UserSettings::getStringForKey("name", "Player1");
    ```

=== "Lua"
    ```lua
    local volume = UserSettings.getIntegerForKey("volume", 80)
    local musicEnabled = UserSettings.getBoolForKey("music", true)
    local playerName = UserSettings.getStringForKey("name", "Player1")
    ```

---

### set methods

* static void **set\<Type\>ForKey**(const char* key, T value)

Store a value. Creates the key if it does not exist, or overwrites the previous value.

=== "C++"
    ```cpp
    UserSettings::setIntegerForKey("highScore", 9999);
    UserSettings::setBoolForKey("tutorialDone", true);
    ```

=== "Lua"
    ```lua
    UserSettings.setIntegerForKey("highScore", 9999)
    UserSettings.setBoolForKey("tutorialDone", true)
    ```

---

### removeKey

* static void **removeKey**(const char* key)

Deletes a key and its associated value from persistent storage.
