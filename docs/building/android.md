---
description: Targeting Android with Doriax.
---

# Building for Android

Doriax can target **Android** for your exported game projects. The runtime supports
Android with an OpenGL ES 3 backend through the Android Native Activity path.

## Requirements

- [Android Studio](https://developer.android.com/studio) with the Android SDK and NDK
- Java 17 or newer for Gradle builds
- A configured Android device or emulator for testing

## Workflow

1. Install Android Studio and ensure the **SDK** and **NDK** are installed via the SDK
   Manager.
2. Make sure the `ANDROID_HOME` (SDK) and NDK paths are available to your environment.
3. Export your project from the Doriax editor with Android selected.
4. Open the generated Android workspace in Android Studio, then build and run on a
   device or emulator.

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
