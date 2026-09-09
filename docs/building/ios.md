---
description: Targeting iOS with Doriax.
---

# Building for iOS

Doriax can target **iOS** for your exported game projects, using the Metal graphics
backend and the native Apple app backend.

## Requirements

- A **Mac** with **Xcode** installed
- An Apple Developer account for deploying to physical devices
- CMake (for building the engine from source)

## Workflow

1. Install Xcode and its Command Line Tools (`xcode-select --install`).
2. Fill in **Project Settings → Platforms → iOS** — bundle identifier, version name and
   build number, icon, and the status bar / home indicator / high refresh rate options.
   See [iOS settings](../editor/project-settings.md#ios).
3. Export the project as **Source Code** with the iOS backend preset selected. The
   exporter writes those settings into the generated `Info.plist` and `AppIcon` asset
   set, so the workspace opens already configured.
4. Open the generated Xcode workspace for your exported project.
5. Select a simulator or a connected device, then build and run from Xcode.

## Command-line build

The engine repository contains Xcode workspace/project templates under
`engine/workspaces/xcode/`. For simulator testing, use Xcode or `xcodebuild`:

```bash
cd engine/workspaces/xcode
xcodebuild build -sdk iphonesimulator -project Doriax.xcodeproj \
    -configuration Debug -scheme "Doriax iOS"
```

iOS runtime builds use Metal and set the deployment target to iOS 13.0 in the engine
configuration.

!!! note "Tooling is being refreshed"
    iOS project export and the Xcode workspace tooling are being updated under the
    Doriax name. Some paths may still reference the legacy Supernova layout while the
    transition completes. Check the
    [repository](https://github.com/doriaxengine/doriax) for current details.
