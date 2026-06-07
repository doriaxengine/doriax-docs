---
description: Targeting Android with Doriax.
---

# Building for Android

Doriax can target **Android** for your exported game projects. The runtime supports
Android with an OpenGL backend.

## Requirements

- [Android Studio](https://developer.android.com/studio) with the Android SDK and NDK
- A configured Android device or emulator for testing

## Workflow

1. Install Android Studio and ensure the **SDK** and **NDK** are installed via the SDK
   Manager.
2. Make sure the `ANDROID_HOME` (SDK) and NDK paths are available to your environment.
3. Open the Android workspace for your exported project in Android Studio, then build
   and run on a device or emulator.

!!! note "Tooling is being refreshed"
    Android project export and the associated workspace tooling are being updated under
    the Doriax name. Some paths and steps may still reference the legacy Supernova
    layout while the transition completes. Check the
    [repository](https://github.com/doriaxengine/doriax) for the latest specifics.
