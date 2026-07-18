---
description: System API reference — screen dimensions, paths, virtual keyboard, fullscreen, user preferences, and ad SDKs.
---

# System

## Description

`System` is a virtual platform-abstraction layer. It provides screen dimensions, file-system paths, virtual keyboard control, fullscreen management, persistent key-value storage, and optional SDK integrations (AdMob, CrazyGames). You access it via `System::instance()` in C++ or the global `System` table in Lua.

Each target platform provides its own concrete `System` subclass; the engine injects the correct implementation at startup.

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    int screenW = System::instance().getScreenWidth();
    int screenH = System::instance().getScreenHeight();
    Log::print("Screen: %dx%d", screenW, screenH);
    ```

=== "Lua"

    ```lua
    local w = System.getScreenWidth()
    local h = System.getScreenHeight()
    Log.print("Screen: " .. w .. "x" .. h)
    ```

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| int | [getScreenWidth](#getscreenwidth-getscreenheight) | C++ \| Lua |
| int | [getScreenHeight](#getscreenwidth-getscreenheight) | C++ \| Lua |
| int | [getSampleCount](#getsamplecount) | C++ \| Lua |
| void | [showVirtualKeyboard](#showvirtualkeyboard) | C++ \| Lua |
| void | [hideVirtualKeyboard](#showvirtualkeyboard) | C++ \| Lua |
| bool | [isFullscreen](#isfullscreen-requestfullscreen-exitfullscreen) | C++ \| Lua |
| void | [requestFullscreen](#isfullscreen-requestfullscreen-exitfullscreen) | C++ \| Lua |
| void | [exitFullscreen](#isfullscreen-requestfullscreen-exitfullscreen) | C++ \| Lua |
| bool | [isWindowMaximized](#window-control) | C++ \| Lua |
| void | [maximizeWindow](#window-control) | C++ \| Lua |
| void | [restoreWindow](#window-control) | C++ \| Lua |
| void | [setWindowSize](#window-control) | C++ \| Lua |
| bool | [isWindowResizable](#window-control) | C++ \| Lua |
| void | [setWindowResizable](#window-control) | C++ \| Lua |
| void | [setWindowTitle](#window-control) | C++ \| Lua |
| char | [getDirSeparator](#getdirseparator) | C++ \| Lua |
| std::string | [getAssetPath](#getassetpath) | C++ \| Lua |
| std::string | [getUserDataPath](#getuserdatapath) | C++ \| Lua |
| std::string | [getLuaPath](#getluapath) | C++ \| Lua |
| std::string | [getShaderPath](#getshaderpath) | C++ \| Lua |
| bool | [getBoolForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| int | [getIntegerForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| long | [getLongForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| float | [getFloatForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| double | [getDoubleForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| std::string | [getStringForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| void | [setBoolForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| void | [setIntegerForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| void | [setLongForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| void | [setFloatForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| void | [setDoubleForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| void | [setStringForKey](#persistent-keyvalue-storage) | C++ \| Lua |
| void | [removeKey](#persistent-keyvalue-storage) | C++ \| Lua |

## Method details

### getScreenWidth / getScreenHeight {#getscreenwidth-getscreenheight}

* `virtual int getScreenWidth() = 0`
* `virtual int getScreenHeight() = 0`

Physical screen (window) dimensions in pixels. These may differ from [Engine::canvasWidth / canvasHeight](engine.md#canvaswidth-canvasheight) when a scaling mode other than `NATIVE` is active.

=== "C++"

    ```cpp
    int w = System::instance().getScreenWidth();
    int h = System::instance().getScreenHeight();
    ```

=== "Lua"

    ```lua
    local w = System.getScreenWidth()
    local h = System.getScreenHeight()
    ```

---

### getSampleCount

* `virtual int getSampleCount()`

Returns the MSAA sample count configured for the current graphics backend (e.g. 1, 2, or 4). Useful when creating render targets that must match the main framebuffer.

---

### showVirtualKeyboard

* `virtual void showVirtualKeyboard(std::wstring text = L"")`

Displays the platform's on-screen keyboard with `text` as the initial input buffer. Has no effect on desktop platforms. On iOS/Android, raises the software keyboard and fires `Engine::onCharInput` for each key typed.

=== "C++"

    ```cpp
    System::instance().showVirtualKeyboard(L"Enter name");
    ```

=== "Lua"

    ```lua
    System.showVirtualKeyboard("Enter name")
    ```

---

### hideVirtualKeyboard

* `virtual void hideVirtualKeyboard()`

Dismisses the on-screen keyboard.

---

### isFullscreen / requestFullscreen / exitFullscreen {#isfullscreen-requestfullscreen-exitfullscreen}

* `virtual bool isFullscreen()`
* `virtual void requestFullscreen()`
* `virtual void exitFullscreen()`

Query and control fullscreen mode. On desktop platforms, `requestFullscreen()` typically toggles borderless fullscreen; on web, it requests the Fullscreen API. Has no effect on mobile (always fullscreen).

Whether a desktop build *starts* fullscreen is a project setting (see [Project Workflow — Window](../../editor/project-workflow.md#window)); `exitFullscreen()` restores the window size configured there.

=== "C++"

    ```cpp
    if (!System::instance().isFullscreen()) {
        System::instance().requestFullscreen();
    }
    ```

=== "Lua"

    ```lua
    if not System.isFullscreen() then
        System.requestFullscreen()
    end
    ```

---

### Window control {#window-control}

* `virtual bool isWindowMaximized()`
* `virtual void maximizeWindow()`
* `virtual void restoreWindow()`
* `virtual void setWindowSize(int width, int height)`
* `virtual bool isWindowResizable()`
* `virtual void setWindowResizable(bool resizable)`
* `virtual void setWindowTitle(const std::string& title)`

Control the OS window of desktop builds at runtime. `maximizeWindow()`/`restoreWindow()` toggle the maximized state, `setWindowSize()` resizes the window in screen coordinates (while fullscreen it instead updates the size restored by `exitFullscreen()`), and `setWindowTitle()` changes the title-bar text. The initial values come from the project's [Window settings](../../editor/project-workflow.md#window).

Note that `setWindowSize()` takes *window* coordinates while [getScreenWidth/getScreenHeight](#getscreenwidth-getscreenheight) report *framebuffer* pixels — on HiDPI/scaled displays these differ by the content scale, so the two do not round-trip 1:1.

Platform support: fully implemented on GLFW-based desktop builds (generated desktop projects and Linux exports). Windows/macOS Sokol exports support only `setWindowTitle()` — the other calls are no-ops there. On web, `setWindowTitle()` sets the browser tab title and the rest are no-ops. All are no-ops on mobile.

=== "C++"

    ```cpp
    System::instance().setWindowTitle("My Game — Level 2");
    System::instance().setWindowSize(1600, 900);
    if (!System::instance().isWindowMaximized()) {
        System::instance().maximizeWindow();
    }
    ```

=== "Lua"

    ```lua
    System.setWindowTitle("My Game — Level 2")
    System.setWindowSize(1600, 900)
    if not System.isWindowMaximized() then
        System.maximizeWindow()
    end
    ```

---

### getDirSeparator

* `virtual char getDirSeparator()`

Returns the platform path directory separator: `'/'` on Unix/macOS/iOS/Android/Web, `'\\'` on Windows.

---

### getAssetPath

* `virtual std::string getAssetPath()`

Returns the root path for read-only assets bundled with the project. Prepend this to asset file names when opening files directly from C++. In Lua and the high-level C++ loaders (`setTexture`, etc.), paths are automatically resolved relative to the asset root.

=== "C++"

    ```cpp
    std::string path = System::instance().getAssetPath() + "textures/sprite.png";
    ```

---

### getUserDataPath

* `virtual std::string getUserDataPath()`

Returns a writable per-user data directory (Documents on iOS, internal storage on Android, `%AppData%` on Windows, `~/.local/share` on Linux). Use for save files and configuration.

=== "C++"

    ```cpp
    std::string savePath = System::instance().getUserDataPath() + "save.dat";
    ```

---

### getLuaPath

* `virtual std::string getLuaPath()`

Returns the base path prepended when Lua `require()` looks for script modules.

---

### getShaderPath

* `virtual std::string getShaderPath()`

Returns the path where compiled shader binaries are expected. Relevant for custom shader loading.

---

### Persistent key–value storage

The system exposes a simple cross-platform persistent store backed by `NSUserDefaults` (iOS/macOS), `SharedPreferences` (Android), `localStorage` (Web), and a JSON file (desktop/Linux/Windows).

**Getters** return the stored value or `defaultValue` if the key does not exist:

| Method | Type |
| --- | --- |
| `getBoolForKey(key, defaultValue)` | bool |
| `getIntegerForKey(key, defaultValue)` | int |
| `getLongForKey(key, defaultValue)` | long |
| `getFloatForKey(key, defaultValue)` | float |
| `getDoubleForKey(key, defaultValue)` | double |
| `getStringForKey(key, defaultValue)` | string |

**Setters** write or update a value:

| Method | Type |
| --- | --- |
| `setBoolForKey(key, value)` | bool |
| `setIntegerForKey(key, value)` | int |
| `setLongForKey(key, value)` | long |
| `setFloatForKey(key, value)` | float |
| `setDoubleForKey(key, value)` | double |
| `setStringForKey(key, value)` | string |

**removeKey** deletes a stored entry:

* `virtual void removeKey(const char* key)`

=== "C++"

    ```cpp
    System& sys = System::instance();

    // Save high score
    sys.setIntegerForKey("highScore", score);

    // Load with default 0
    int best = sys.getIntegerForKey("highScore", 0);
    ```

=== "Lua"

    ```lua
    System.setIntegerForKey("highScore", score)
    local best = System.getIntegerForKey("highScore", 0)
    ```

## AdMob integration

The following methods are available on Android and iOS when the Google AdMob SDK is linked. They are no-ops on other platforms.

| Method | Description |
| --- | --- |
| `initializeAdMob(childDirected, underAge)` | Initialize the AdMob SDK. |
| `setMaxAdContentRating(AdMobRating rating)` | Set COPPA-compliant content rating. |
| `loadInterstitialAd(adUnitID)` | Pre-load an interstitial ad. |
| `isInterstitialAdLoaded()` | Returns `true` when the ad is ready to show. |
| `showInterstitialAd()` | Display the loaded interstitial ad. |

### AdMobRating

* **General** — Suitable for all audiences.
* **ParentalGuidance** — Parental guidance suggested.
* **Teen** — Suitable for teens.
* **MatureAudience** — Mature content.

## CrazyGames integration

Methods for the CrazyGames web SDK. Only active on HTML5 builds.

| Method | Description |
| --- | --- |
| `initializeCrazyGamesSDK()` | Load and initialize the CrazyGames SDK. |
| `showCrazyGamesAd(type)` | Show a mid-game or rewarded ad. |
| `happytimeCrazyGames()` | Signal a positive gameplay moment. |
| `gameplayStartCrazyGames()` | Notify the SDK that gameplay started. |
| `gameplayStopCrazyGames()` | Notify the SDK that gameplay stopped. |
| `loadingStartCrazyGames()` | Notify the SDK that loading started. |
| `loadingStopCrazyGames()` | Notify the SDK that loading finished. |
