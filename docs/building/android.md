---
description: Targeting Android with Doriax.
---

# Building for Android

Doriax can target **Android** for your exported game projects. The runtime supports
Android with an OpenGL ES 3.1 backend through the Android Native Activity path.

## Requirements

- [Android Studio](https://developer.android.com/studio) with the Android SDK and NDK
- Java 17 or newer for Gradle builds
- A configured Android device or emulator for testing

## Workflow

1. Install Android Studio and ensure the **SDK** and **NDK** are installed via the SDK
   Manager.
2. Make sure the `ANDROID_HOME` (SDK) and NDK paths are available to your environment.
3. Fill in **Project Settings → Platforms → Android** — package name, version, SDK
   levels, orientation, architectures, permissions and launcher icons. See
   [Android settings](../editor/project-settings.md#android).
4. Optional: enable **Project Settings → Directories → Native Resource Pack** to ship
   assets and Lua files in one `resources.pak` instead of as loose files.
5. Export your project from the Doriax editor as **Source Code**, with the Android
   preset selected in the Export Window's graphic backends.
6. Open the generated Android workspace in Android Studio, then build and run on a
   device or emulator.

## Project configuration

A Source Code export writes the Android settings into the generated workspace, so the
manifest and Gradle files do not have to be edited by hand:

| Setting | Written to |
| --- | --- |
| Package name, version code / name, min and target SDK, architectures | `app/build.gradle` |
| Permissions, orientation, allow backup | `app/src/main/AndroidManifest.xml` |
| Application name | `app/src/main/res/values/strings.xml` |
| Fullscreen theme | `app/src/main/res/values/styles.xml` and `MainActivity.java` |
| Launcher icon, or the adaptive foreground/background pair | `app/src/main/res/drawable` and `mipmap-anydpi-v26` |

An export with no architecture selected fails rather than producing an APK that cannot
run, so keep at least one ABI ticked.

## Resource packaging

The native resource pack is experimental and disabled by default. When enabled, a
Source Code export writes `project/assets/resources.pak`, removes the loose asset and
Lua contents, and the Android build ships the pack at the APK asset root. Normal engine
loaders, Lua modules, and `Data` continue to resolve asset-relative, `asset://`, and
`lua://` paths.

A direct `File` handle cannot open packed entries, the full pack must remain below 2
GiB, and its bytes are obfuscated rather than encrypted. See [Export Window — Native
resource pack](../editor/export.md#native-resource-pack) for the complete restrictions.

## Command-line build

The engine repository contains an Android Studio workspace template under
`engine/workspaces/androidstudio/`. Exported projects use the same runtime path.

```bash
cd engine/workspaces/androidstudio
./gradlew assembleDebug
```

Android builds link the Android log, EGL/OpenGL ES, OpenSL ES, Game Activity, and Game
Frame Pacing libraries.

!!! note "Tooling is being refreshed"
    Android project export and the associated workspace tooling are being updated under
    the Doriax name. Some paths and steps may still reference the legacy Supernova
    layout while the transition completes. Check the
    [repository](https://github.com/doriaxengine/doriax) for the latest specifics.
