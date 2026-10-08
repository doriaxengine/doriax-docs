---
description: AdMob API reference (C++ and Lua) — Google Mobile Ads on Android and iOS, with consent, banners, and full-screen ads.
---

# AdMob

**C++ type:** `AdMob` (static) · **Header:** `AdMob.h`

## Description

Google Mobile Ads on Android and iOS: banner, interstitial, rewarded, rewarded
interstitial and app open ads, plus Google's consent form (User Messaging Platform).
Exports include the SDK only when **Google AdMob** is enabled in the project's
[Android](../../editor/project-settings.md#android) or
[iOS](../../editor/project-settings.md#ios) settings. Everywhere else the calls still
compile and run, and report `errorNotAvailable` through their events.

Results arrive as [events](#events) at the start of a frame, never as return values.
Loading a format again replaces its ad. See [Monetization](../../manual/monetization.md#admob)
for the setup and the full flow.

=== "C++"

    ```cpp
    REGISTER_EVENT(AdMob::onUserEarnedReward, onUserEarnedReward);
    AdMob::loadRewardedAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx");

    void Shop::onUserEarnedReward(AdMobFormat format, std::string type, int amount) {
        coins += amount;
    }
    ```

=== "Lua"

    ```lua
    RegisterEvent(self, AdMob.onUserEarnedReward, "onUserEarnedReward")
    AdMob.loadRewardedAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx")

    function Shop:onUserEarnedReward(format, rewardType, amount)
        self.coins = self.coins + amount
    end
    ```

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static void | [initialize](#initialize-isinitialized) | C++ \| Lua |
| static bool | [isInitialized](#initialize-isinitialized) | C++ \| Lua |
| static void | [setMaxAdContentRating](#request-settings) | C++ \| Lua |
| static [AdMobRating](#admobrating) | [getMaxAdContentRating](#request-settings) | C++ \| Lua |
| static void | [setAgeRestriction](#request-settings) | C++ \| Lua |
| static [AdMobAgeRestriction](#admobagerestriction) | [getAgeRestriction](#request-settings) | C++ \| Lua |
| static void | [setPersonalization](#request-settings) | C++ \| Lua |
| static [AdMobPersonalization](#admobpersonalization) | [getPersonalization](#request-settings) | C++ \| Lua |
| static void | [setTestDeviceIds](#settestdeviceids-gettestdeviceids) | C++ \| Lua |
| static std::vector\<std::string\> | [getTestDeviceIds](#settestdeviceids-gettestdeviceids) | C++ \| Lua |
| static void | [requestConsent](#requestconsent) | C++ \| Lua |
| static void | [setConsentDebugGeography](#setconsentdebuggeography-getconsentdebuggeography) | C++ \| Lua |
| static [AdMobDebugGeography](#admobdebuggeography) | [getConsentDebugGeography](#setconsentdebuggeography-getconsentdebuggeography) | C++ \| Lua |
| static [AdMobConsentStatus](#admobconsentstatus) | [getConsentStatus](#getconsentstatus-canrequestads) | C++ \| Lua |
| static bool | [canRequestAds](#getconsentstatus-canrequestads) | C++ \| Lua |
| static bool | [isPrivacyOptionsRequired](#isprivacyoptionsrequired-showprivacyoptionsform) | C++ \| Lua |
| static void | [showPrivacyOptionsForm](#isprivacyoptionsrequired-showprivacyoptionsform) | C++ \| Lua |
| static void | [resetConsent](#resetconsent) | C++ \| Lua |
| static void | [loadBannerAd](#loadbannerad) | C++ \| Lua |
| static bool | [isBannerAdLoaded](#banner-control) | C++ \| Lua |
| static void | [showBannerAd](#banner-control) | C++ \| Lua |
| static void | [hideBannerAd](#banner-control) | C++ \| Lua |
| static bool | [isBannerAdVisible](#banner-control) | C++ \| Lua |
| static void | [setBannerAdPosition](#banner-control) | C++ \| Lua |
| static [AdMobBannerPosition](#admobbannerposition) | [getBannerAdPosition](#banner-control) | C++ \| Lua |
| static void | [removeBannerAd](#banner-control) | C++ \| Lua |
| static int | [getBannerAdWidth](#banner-control) | C++ \| Lua |
| static int | [getBannerAdHeight](#banner-control) | C++ \| Lua |
| static void | [loadInterstitialAd](#full-screen-ads) | C++ \| Lua |
| static bool | [isInterstitialAdLoaded](#full-screen-ads) | C++ \| Lua |
| static void | [showInterstitialAd](#full-screen-ads) | C++ \| Lua |
| static void | [loadRewardedAd](#full-screen-ads) | C++ \| Lua |
| static bool | [isRewardedAdLoaded](#full-screen-ads) | C++ \| Lua |
| static void | [showRewardedAd](#full-screen-ads) | C++ \| Lua |
| static void | [loadRewardedInterstitialAd](#full-screen-ads) | C++ \| Lua |
| static bool | [isRewardedInterstitialAdLoaded](#full-screen-ads) | C++ \| Lua |
| static void | [showRewardedInterstitialAd](#full-screen-ads) | C++ \| Lua |
| static void | [loadAppOpenAd](#full-screen-ads) | C++ \| Lua |
| static bool | [isAppOpenAdLoaded](#full-screen-ads) | C++ \| Lua |
| static void | [showAppOpenAd](#full-screen-ads) | C++ \| Lua |
| static void | [setServerSideVerificationOptions](#setserversideverificationoptions) | C++ \| Lua |
| static void | [setAppVolume](#setappvolume-setappmuted) | C++ \| Lua |
| static void | [setAppMuted](#setappvolume-setappmuted) | C++ \| Lua |
| static void | [openAdInspector](#openadinspector) | C++ \| Lua |

### Callback events

| Callback | Name | Languages |
| --- | --- | --- |
| void() | [onInitialized](#events) | C++ \| Lua |
| void(int, std::string) | [onConsentUpdated](#events) | C++ \| Lua |
| void(AdMobFormat) | [onAdLoaded](#events) | C++ \| Lua |
| void(AdMobFormat, int, std::string) | [onAdFailedToLoad](#events) | C++ \| Lua |
| void(AdMobFormat) | [onAdShown](#events) | C++ \| Lua |
| void(AdMobFormat, int, std::string) | [onAdFailedToShow](#events) | C++ \| Lua |
| void(AdMobFormat) | [onAdDismissed](#events) | C++ \| Lua |
| void(AdMobFormat) | [onAdClicked](#events) | C++ \| Lua |
| void(AdMobFormat) | [onAdImpression](#events) | C++ \| Lua |
| void(AdMobFormat, std::string, int) | [onUserEarnedReward](#events) | C++ \| Lua |
| void(AdMobFormat, long long, std::string, AdMobPrecision) | [onAdPaid](#events) | C++ \| Lua |
| void(int, std::string) | [onAdInspectorClosed](#events) | C++ \| Lua |

## Method details

### initialize / isInitialized {#initialize-isinitialized}

* static void **initialize**()
* static bool **isInitialized**()

Starts Google Mobile Ads with the [request settings](#request-settings) made so far.
[`onInitialized`](#events) fires when it is ready, and `isInitialized()` is true from
then on. Call it once [consent](#requestconsent) allows ad requests
([`canRequestAds()`](#getconsentstatus-canrequestads)), and load the first ads in
`onInitialized`.

---

### Request settings {#request-settings}

* static void **setMaxAdContentRating**([AdMobRating](#admobrating) rating)
* static [AdMobRating](#admobrating) **getMaxAdContentRating**()
* static void **setAgeRestriction**([AdMobAgeRestriction](#admobagerestriction) restriction)
* static [AdMobAgeRestriction](#admobagerestriction) **getAgeRestriction**()
* static void **setPersonalization**([AdMobPersonalization](#admobpersonalization) personalization)
* static [AdMobPersonalization](#admobpersonalization) **getPersonalization**()

Settings for the ad requests made after them. Set them before
[`requestConsent()`](#requestconsent) and `initialize()`; settings made earlier reach the
first requests too. All default to `UNSPECIFIED` or `DEFAULT`.

- **Max ad content rating** — the highest content rating of the ads served.
- **Age restriction** — `CHILD` for a game directed at children and `TEEN` for one
  directed at teens. `CHILD` also makes `requestConsent()` ask as for a user under the
  age of consent.
- **Personalization** — `DISABLED` asks for non-personalized ads only.

=== "C++"

    ```cpp
    AdMob::setAgeRestriction(AdMobAgeRestriction::CHILD);
    AdMob::setMaxAdContentRating(AdMobRating::GENERAL);
    AdMob::requestConsent();
    ```

=== "Lua"

    ```lua
    AdMob.setAgeRestriction(AdMobAgeRestriction.CHILD)
    AdMob.setMaxAdContentRating(AdMobRating.GENERAL)
    AdMob.requestConsent()
    ```

---

### setTestDeviceIds / getTestDeviceIds {#settestdeviceids-gettestdeviceids}

* static void **setTestDeviceIds**(const std::vector\<std::string\>& ids)
* static std::vector\<std::string\> **getTestDeviceIds**()

Devices that get test ads, by the hashed ID Google Mobile Ads prints to the device log
(Logcat or the Xcode console). The consent debug settings also apply only to these
devices. In Lua, pass a table of strings.

=== "Lua"

    ```lua
    AdMob.setTestDeviceIds({ "33BE2250B43518CCDA7DE426D04EE231" })
    ```

---

### requestConsent

* static void **requestConsent**()

Updates the user's consent information and shows Google's consent form when the user
still has to answer, as Google's policies require in the EEA, the UK, Switzerland and
some US states. Call it at every launch, before `initialize()`.
[`onConsentUpdated(errorCode, message)`](#events) reports the result, with `errorCode` 0
on success. Without AdMob in the build it reports `errorNotAvailable`.

---

### setConsentDebugGeography / getConsentDebugGeography {#setconsentdebuggeography-getconsentdebuggeography}

* static void **setConsentDebugGeography**([AdMobDebugGeography](#admobdebuggeography) geography)
* static [AdMobDebugGeography](#admobdebuggeography) **getConsentDebugGeography**()

Makes the next `requestConsent()` on a [test device](#settestdeviceids-gettestdeviceids)
act as if the user were in that region, to see the consent form from anywhere. Defaults
to `DISABLED`.

---

### getConsentStatus / canRequestAds {#getconsentstatus-canrequestads}

* static [AdMobConsentStatus](#admobconsentstatus) **getConsentStatus**()
* static bool **canRequestAds**()

The consent state Google has stored. `canRequestAds()` is true once the consent allows ad
requests, including consent from an earlier launch. Without AdMob in the build they
return `UNKNOWN` and `false`.

---

### isPrivacyOptionsRequired / showPrivacyOptionsForm {#isprivacyoptionsrequired-showprivacyoptionsform}

* static bool **isPrivacyOptionsRequired**()
* static void **showPrivacyOptionsForm**()

When `isPrivacyOptionsRequired()` is true, the game must offer a way back to the consent
form, such as a **Privacy** button in its settings, which calls
`showPrivacyOptionsForm()`. Closing the form reports through `onConsentUpdated`.

---

### resetConsent

* static void **resetConsent**()

Forgets the stored consent, so the next `requestConsent()` asks again. Meant for testing.

---

### loadBannerAd

* static void **loadBannerAd**(const std::string& adUnitId, [AdMobBannerSize](#admobbannersize) size = ADAPTIVE, [AdMobBannerPosition](#admobbannerposition) position = BOTTOM)

Loads a banner and shows it over the game as soon as it loads, replacing any banner
already there. `onAdLoaded(BANNER)` or `onAdFailedToLoad(BANNER, ...)` reports the
result. An `ADAPTIVE` banner takes the screen width when it loads, so load it again after
the screen rotates.

Banners refresh at the rate set on their ad unit. A refresh that fails reports
`onAdFailedToLoad(BANNER, ...)` while the last ad keeps showing, and
`isBannerAdLoaded()` stays true.

=== "C++"

    ```cpp
    AdMob::loadBannerAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx");
    AdMob::loadBannerAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx", AdMobBannerSize::BANNER, AdMobBannerPosition::TOP);
    ```

=== "Lua"

    ```lua
    AdMob.loadBannerAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx")
    AdMob.loadBannerAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx", AdMobBannerSize.BANNER, AdMobBannerPosition.TOP)
    ```

---

### Banner control {#banner-control}

* static bool **isBannerAdLoaded**()
* static void **showBannerAd**()
* static void **hideBannerAd**()
* static bool **isBannerAdVisible**()
* static void **setBannerAdPosition**([AdMobBannerPosition](#admobbannerposition) position)
* static [AdMobBannerPosition](#admobbannerposition) **getBannerAdPosition**()
* static void **removeBannerAd**()
* static int **getBannerAdWidth**()
* static int **getBannerAdHeight**()

`hideBannerAd()` and `showBannerAd()` toggle the banner without reloading it, and
`isBannerAdVisible()` is true when it is loaded and not hidden. `setBannerAdPosition()`
moves it. `removeBannerAd()` destroys it; results of its load still on their way are
dropped.

`getBannerAdWidth()` and `getBannerAdHeight()` give the loaded banner's size in screen
pixels, as [`System::getScreenWidth`](system.md#getscreenwidth-getscreenheight) counts
them, and are 0 until it loads. On Android the banner also stays clear of display
cutouts and visible system bars.

---

### Full-screen ads {#full-screen-ads}

* static void **loadInterstitialAd**(const std::string& adUnitId)
* static bool **isInterstitialAdLoaded**()
* static void **showInterstitialAd**()
* static void **loadRewardedAd**(const std::string& adUnitId)
* static bool **isRewardedAdLoaded**()
* static void **showRewardedAd**()
* static void **loadRewardedInterstitialAd**(const std::string& adUnitId)
* static bool **isRewardedInterstitialAdLoaded**()
* static void **showRewardedInterstitialAd**()
* static void **loadAppOpenAd**(const std::string& adUnitId)
* static bool **isAppOpenAdLoaded**()
* static void **showAppOpenAd**()

Each format holds one ad. `load...()` loads it, replacing a loaded one, and
`onAdLoaded(format)` or `onAdFailedToLoad(format, errorCode, message)` reports the
result; only the latest load of a format reports. `is...Loaded()` is true from
`onAdLoaded` until the ad is shown.

`show...()` shows the ad once: `onAdShown`, `onAdImpression` and `onAdDismissed` follow,
and the format needs loading again. Showing a format that is not loaded reports
`onAdFailedToShow(format, errorNotLoaded, message)`. While the ad covers the game, the
engine [pauses](../../manual/monetization.md#ads-pause-the-game).

- **Rewarded** and **rewarded interstitial** ads report the reward through
  `onUserEarnedReward(format, type, amount)`. A player who closes the ad early gets no
  such event.
- **App open** ads expire four hours after loading, as Google stops serving them then:
  `isAppOpenAdLoaded()` turns false, and showing one reports "The ad expired, load it
  again".

---

### setServerSideVerificationOptions

* static void **setServerSideVerificationOptions**(const std::string& userId, const std::string& customData = "")

Data passed to the server-side verification callback of rewarded ads, which lets your
server confirm a reward before granting it. It applies to the rewarded and rewarded
interstitial ads shown after the call.

---

### setAppVolume / setAppMuted {#setappvolume-setappmuted}

* static void **setAppVolume**(float volume)
* static void **setAppMuted**(bool muted)

Volume of video ads relative to the game, from 0 to 1, and whether they play muted.
Match them to the game's own volume settings.

---

### openAdInspector

* static void **openAdInspector**()

Opens Google's Ad Inspector, which shows the requests and mediation results of each ad
unit. It only opens on a [test device](#settestdeviceids-gettestdeviceids).
`onAdInspectorClosed(errorCode, message)` fires when it closes.

## Events

Each event is a static `FunctionSubscribe` member; subscribe with `REGISTER_EVENT` in C++
or `RegisterEvent` in Lua (see [Events](../../manual/events.md#service-events)). C++
handlers take the parameters by value, exactly as listed.

| Event | Parameters | When |
| --- | --- | --- |
| `onInitialized` | — | Google Mobile Ads is ready to load ads |
| `onConsentUpdated` | `int errorCode, std::string message` | `requestConsent()` or the privacy options form finished. `errorCode` is 0 on success |
| `onAdLoaded` | `AdMobFormat format` | An ad loaded and can be shown |
| `onAdFailedToLoad` | `AdMobFormat format, int errorCode, std::string message` | An ad failed to load, with Google's error code |
| `onAdShown` | `AdMobFormat format` | A full-screen ad opened, or a banner opened an overlay after a click |
| `onAdFailedToShow` | `AdMobFormat format, int errorCode, std::string message` | A full-screen ad could not be shown |
| `onAdDismissed` | `AdMobFormat format` | A full-screen ad, or a banner's overlay, closed |
| `onAdClicked` | `AdMobFormat format` | An ad was clicked |
| `onAdImpression` | `AdMobFormat format` | An ad recorded an impression |
| `onUserEarnedReward` | `AdMobFormat format, std::string type, int amount` | The player earned the reward of a rewarded ad. Type and amount come from the ad unit |
| `onAdPaid` | `AdMobFormat format, long long valueMicros, std::string currencyCode, AdMobPrecision precision` | An ad earned revenue, in millionths of the currency |
| `onAdInspectorClosed` | `int errorCode, std::string message` | The Ad Inspector closed |

On Android, the events of a full-screen ad arrive when it closes, since the whole app
pauses while it shows.

## Constants

Error codes the engine reports in place of Google's:

| Name | Value | Meaning |
| --- | --- | --- |
| `errorNotAvailable` | `-1` | The platform or the build has no AdMob |
| `errorNotLoaded` | `-2` | The ad shown was not loaded, or has expired |

## Enumerations

### AdMobFormat

* **BANNER**
* **INTERSTITIAL**
* **REWARDED**
* **REWARDED_INTERSTITIAL**
* **APP_OPEN**

---

### AdMobBannerSize

Fixed sizes are in Google's units: dp on Android, points on iOS.

* **ADAPTIVE** — Anchored adaptive banner: the screen width, with a height Google picks.
* **BANNER** — 320×50.
* **LARGE_BANNER** — 320×100.
* **MEDIUM_RECTANGLE** — 300×250.
* **FULL_BANNER** — 468×60.
* **LEADERBOARD** — 728×90.

---

### AdMobBannerPosition

`TOP`, `BOTTOM`, `TOP_LEFT`, `TOP_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_RIGHT`, `CENTER`

---

### AdMobRating

* **UNSPECIFIED** — No limit set.
* **GENERAL** — Content for general audiences.
* **PARENTAL_GUIDANCE** — Content for most audiences, with parental guidance.
* **TEEN** — Content for teen and older audiences.
* **MATURE_AUDIENCE** — Content only for mature audiences.

---

### AdMobAgeRestriction

* **UNSPECIFIED** — No age treatment.
* **CHILD** — Directed at children; also asks for consent as for a user under the age of consent.
* **TEEN** — Directed at teens.

---

### AdMobPersonalization

* **DEFAULT** — Google decides.
* **ENABLED** — Personalized ads allowed.
* **DISABLED** — Non-personalized ads only.

---

### AdMobConsentStatus

* **UNKNOWN** — Not known yet, or no AdMob in the build.
* **REQUIRED** — The user has to answer the consent form.
* **NOT_REQUIRED** — No consent needed, as outside the regulated regions.
* **OBTAINED** — The user answered.

---

### AdMobDebugGeography

`DISABLED`, `EEA`, `REGULATED_US_STATE`, `OTHER`

---

### AdMobPrecision

How exact an [`onAdPaid`](#events) value is.

* **UNKNOWN**
* **ESTIMATED** — Estimated from aggregated data.
* **PUBLISHER_PROVIDED** — From the CPM set in a mediation network.
* **PRECISE** — The value paid for this ad.

## See also

- [Monetization](../../manual/monetization.md) — setup, consent, and testing
- [InAppPurchase](inapppurchase.md) and [WebPortal](webportal.md)
