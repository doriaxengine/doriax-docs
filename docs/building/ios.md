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
   build number, icon, the status bar / home indicator / high refresh rate options, and
   the Google AdMob and App Store Purchases services. See
   [iOS settings](../editor/project-settings.md#ios).
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

iOS runtime builds use Metal and set the deployment target to iOS 15.0 in the engine
configuration. CMake builds copy the project's `assets/` and `lua/` folders into the app
bundle after each build, since iOS reads them from inside the app.

## Google Mobile Ads

The [`AdMob`](../reference/classes/admob.md) class runs on Google Mobile Ads SDK 13.11.0
and the User Messaging Platform, vendored as static xcframeworks under
`engine/platform/apple/GoogleMobileAdsSdkiOS-13.11.0`. The Xcode template links them and
compiles the AdMob adapter, `AdMobAdapter.m`, behind the `DORIAX_ADMOB` define.

A Source Code export with **Google AdMob** off in the iOS settings unlinks both
frameworks, drops the define, and removes the `GADApplicationIdentifier` and
`NSUserTrackingUsageDescription` keys from `Info.plist`. With it on, the export writes
the **AdMob App ID** and the **Tracking Description** into those keys.

CMake builds follow the [`DORIAX_ADMOB`](../reference/build-options.md#runtime-project-options)
option, on by default. With CMake 3.28 or newer the xcframeworks are linked whole, and
Xcode picks the device or simulator slice; older CMake links the simulator slice only.
The SDK also needs the Swift runtime libraries, which a placeholder Swift source in that
folder makes Xcode link.

## App Store purchases

The [`InAppPurchase`](../reference/classes/inapppurchase.md) class runs on StoreKit 2
through `StoreKitAdapter.swift`, which implements the Objective-C interface declared in
`StoreKitAdapter.h`, the target's bridging header. That Swift feature needs Swift 6.1, so
building with App Store purchases takes Xcode 16.3 or later. The engine uses the adapter
when built with the `DORIAX_STOREKIT` define.

A Source Code export with **App Store Purchases** off in the iOS settings removes the
adapter, the bridging header setting and the define. CMake builds follow the
[`DORIAX_STOREKIT`](../reference/build-options.md#runtime-project-options) option, on by
default.

!!! note "Tooling is being refreshed"
    iOS project export and the Xcode workspace tooling are being updated under the
    Doriax name. Some paths may still reference the legacy Supernova layout while the
    transition completes. Check the
    [repository](https://github.com/doriaxengine/doriax) for current details.
