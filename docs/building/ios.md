---
description: Targeting iOS with Doriax.
---

# Building for iOS

Doriax can target **iOS** for your exported game projects, using the Metal graphics
backend.

## Requirements

- A **Mac** with **Xcode** installed
- An Apple Developer account for deploying to physical devices
- CMake (for building the engine from source)

## Workflow

1. Install Xcode and its Command Line Tools (`xcode-select --install`).
2. Open the generated Xcode workspace for your exported project.
3. Select a simulator or a connected device, then build and run from Xcode.

!!! note "Tooling is being refreshed"
    iOS project export and the Xcode workspace tooling are being updated under the
    Doriax name. Some paths may still reference the legacy Supernova layout while the
    transition completes. Check the
    [repository](https://github.com/doriaxengine/doriax) for current details.
