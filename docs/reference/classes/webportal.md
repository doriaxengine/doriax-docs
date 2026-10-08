---
description: WebPortal API reference (C++ and Lua) — one API for the SDKs of CrazyGames, Poki, GameDistribution, Yandex Games and YouTube Playables in web exports.
---

# WebPortal

**C++ type:** `WebPortal` (static) · **Header:** `WebPortal.h`

## Description

The SDK of a web game portal, behind one API: ads, gameplay and loading events, and cloud
saves. A web export builds in the portal chosen with **Game Portal** in the project's
[Web settings](../../editor/project-settings.md#web): CrazyGames, Poki,
GameDistribution, Yandex Games or YouTube Playables. Without one, and on every other
platform, the calls do nothing and ads and saves report errors.

Results arrive as [events](#events) at the start of a frame. The engine pauses while an
ad plays or the portal pauses the game, and resumes after. See
[Monetization → Web portals](../../manual/monetization.md#web-portals) for the flow,
what each portal supports, and how to test locally.

=== "C++"

    ```cpp
    REGISTER_EVENT(WebPortal::onAdFinished, onAdFinished);
    WebPortal::initialize();
    WebPortal::loadingStop();

    void Game::onAdFinished(WebPortalAdType type) {
        if (type == WebPortalAdType::REWARDED) lives++;
    }
    ```

=== "Lua"

    ```lua
    RegisterEvent(self, WebPortal.onAdFinished, "onAdFinished")
    WebPortal.initialize()
    WebPortal.loadingStop()

    function Game:onAdFinished(adType)
        if adType == WebPortalAdType.REWARDED then
            self.lives = self.lives + 1
        end
    end
    ```

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static [WebPortalType](#webportaltype) | [getPortal](#getportal) | C++ \| Lua |
| static void | [initialize](#initialize) | C++ \| Lua |
| static [WebPortalEnvironment](#webportalenvironment) | [getEnvironment](#getenvironment-isavailable) | C++ \| Lua |
| static bool | [isAvailable](#getenvironment-isavailable) | C++ \| Lua |
| static void | [requestAd](#requestad) | C++ \| Lua |
| static void | [gameplayStart](#gameplaystart-gameplaystop) | C++ \| Lua |
| static void | [gameplayStop](#gameplaystart-gameplaystop) | C++ \| Lua |
| static void | [loadingStart](#loadingstart-loadingstop) | C++ \| Lua |
| static void | [loadingStop](#loadingstart-loadingstop) | C++ \| Lua |
| static void | [happytime](#happytime) | C++ \| Lua |
| static void | [loadData](#loaddata-savedata) | C++ \| Lua |
| static void | [saveData](#loaddata-savedata) | C++ \| Lua |

### Callback events

| Callback | Name | Languages |
| --- | --- | --- |
| void(WebPortalEnvironment) | [onInitialized](#events) | C++ \| Lua |
| void(WebPortalAdType) | [onAdStarted](#events) | C++ \| Lua |
| void(WebPortalAdType) | [onAdFinished](#events) | C++ \| Lua |
| void(WebPortalAdType, std::string, std::string) | [onAdError](#events) | C++ \| Lua |
| void(std::string) | [onDataLoaded](#events) | C++ \| Lua |
| void(std::string) | [onDataLoadFailed](#events) | C++ \| Lua |
| void(std::string) | [onDataSaveFailed](#events) | C++ \| Lua |

## Method details

### getPortal

* static [WebPortalType](#webportaltype) **getPortal**()

The portal this build includes, or `NONE`. It reflects the build, not where the page
runs: see [`getEnvironment()`](#getenvironment-isavailable) for that.

---

### initialize

* static void **initialize**()

Loads the portal's SDK and starts it. Call it once at startup, as some portals pause or
mute the game from the start. [`onInitialized(environment)`](#events) reports where the
game runs.

Calls made after `initialize()` wait for the SDK to start. Calls made before it are
dropped: ads report `unavailable` and saves fail.

---

### getEnvironment / isAvailable {#getenvironment-isavailable}

* static [WebPortalEnvironment](#webportalenvironment) **getEnvironment**()
* static bool **isAvailable**()

Where the game runs, known once `onInitialized` fired. `isAvailable()` is true for
`LOCAL` and `PORTAL`, when the SDK works.

---

### requestAd

* static void **requestAd**([WebPortalAdType](#webportaladtype) type)

Asks the portal for an ad: `MIDGAME` at a natural break, or `REWARDED` when the player
chose to watch one for a reward. `onAdStarted` and `onAdFinished` report an ad that
played, and `onAdError(type, code, message)` one that did not. Grant a reward only in
`onAdFinished`.

Portals decide when a midgame ad really plays, so a request may show none and report
the code `unfilled`. The engine pauses while the ad plays. See
[ad error codes](../../manual/monetization.md#web-portal-flow).

---

### gameplayStart / gameplayStop {#gameplaystart-gameplaystop}

* static void **gameplayStart**()
* static void **gameplayStop**()

Tell the portal when the player is playing: start at play and on resume, stop at every
break, such as menus, pauses, and the end of a level. Portals use it to time their ads.
CrazyGames, Poki and Yandex Games use it; the others ignore it.

---

### loadingStart / loadingStop {#loadingstart-loadingstop}

* static void **loadingStart**()
* static void **loadingStop**()

Bracket loading screens. Call `loadingStop()` once the game can be played: Yandex Games
and YouTube Playables require it. CrazyGames and Poki also use `loadingStart()`.

---

### happytime

* static void **happytime**()

Marks a happy moment, like a level completed or a record beaten. CrazyGames and Poki use
it.

---

### loadData / saveData {#loaddata-savedata}

* static void **loadData**()
* static void **saveData**(const std::string& data)

The cloud save of YouTube Playables, kept in the player's account as one string.
`loadData()` reports `onDataLoaded(data)`, with an empty string when nothing was saved
yet, or `onDataLoadFailed(message)`. `saveData()` reports only failures, through
`onDataSaveFailed(message)`. YouTube refuses saves made before a `loadData()`.

The other portals have no cloud save: `loadData()` and `saveData()` report a failure.

## Events

Each event is a static `FunctionSubscribe` member; subscribe with `REGISTER_EVENT` in C++
or `RegisterEvent` in Lua (see [Events](../../manual/events.md#service-events)). C++
handlers take the parameters by value, exactly as listed.

| Event | Parameters | When |
| --- | --- | --- |
| `onInitialized` | `WebPortalEnvironment environment` | The SDK started, or could not |
| `onAdStarted` | `WebPortalAdType type` | An ad started. The engine pauses until it ends. YouTube Playables gives no start signal, so it never fires there |
| `onAdFinished` | `WebPortalAdType type` | An ad finished; grant the reward of a rewarded ad |
| `onAdError` | `WebPortalAdType type, std::string code, std::string message` | No ad played, or it failed. See the codes below |
| `onDataLoaded` | `std::string data` | The cloud save loaded; saving works from now on |
| `onDataLoadFailed` | `std::string message` | The cloud save could not be loaded |
| `onDataSaveFailed` | `std::string message` | Saving to the cloud failed |

`onAdError` codes:

| Code | Meaning |
| --- | --- |
| `unfilled` | No ad played: the portal had none, chose not to show one now, or another ad is playing |
| `unavailable` | No portal SDK: a build without a portal, `initialize()` not called, or the portal refused to start here |
| `other` | The ad started but failed, or a rewarded ad was closed before its reward |
| A CrazyGames code | CrazyGames passes its own codes, like `adCooldown` |

## Enumerations

### WebPortalType

* **NONE** — No portal in this build.
* **CRAZYGAMES** — CrazyGames, SDK v3.
* **POKI** — Poki, SDK v2.
* **GAMEDISTRIBUTION** — GameDistribution. Needs the **Portal Game ID** project setting.
* **YANDEX** — Yandex Games.
* **YOUTUBE** — YouTube Playables.

---

### WebPortalAdType

* **MIDGAME** — An ad at a break in the game: CrazyGames' midgame ad, Poki's commercial break, an interstitial or fullscreen ad elsewhere.
* **REWARDED** — An ad the player chose to watch for a reward.

---

### WebPortalEnvironment

* **UNINITIALIZED** — `initialize()` has not finished.
* **DISABLED** — No portal in this build, its SDK failed to load, or the portal does not run on this host. Calls do nothing.
* **LOCAL** — `localhost`, `127.0.0.1` or `[::1]`, where most portals show test ads.
* **PORTAL** — Any other host, normally the portal's.

## See also

- [Monetization → Web portals](../../manual/monetization.md#web-portals) — setup, portal differences, and local testing
- [AdMob](admob.md) and [InAppPurchase](inapppurchase.md)
- [Building for HTML5](../../building/html5.md#game-portals)
