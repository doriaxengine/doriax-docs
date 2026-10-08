---
description: Show Google AdMob ads, sell in-app purchases on Google Play and the App Store, and use the SDKs of web game portals (CrazyGames, Poki, GameDistribution, Yandex Games, YouTube Playables) from C++ or Lua.
---

# Monetization

Doriax has three service classes for earning from a game. They are static classes that
any script can call, and each one talks to a platform SDK that an export includes only
when it is enabled in [Project Settings](../editor/project-settings.md#platforms):

| Class | Service | Platforms | Enabled by |
| --- | --- | --- | --- |
| [`AdMob`](../reference/classes/admob.md) | Google Mobile Ads: banner, interstitial, rewarded, rewarded interstitial and app open ads, with Google's consent form | Android, iOS | **Google AdMob**, in the Android and iOS sections |
| [`InAppPurchase`](../reference/classes/inapppurchase.md) | Google Play Billing and the App Store (StoreKit 2): one-time products and subscriptions | Android, iOS | **Google Play Billing** in the Android section, **App Store Purchases** in the iOS section |
| [`WebPortal`](../reference/classes/webportal.md) | The SDK of one web game portal: ads, gameplay and loading events, cloud saves | Web | **Game Portal**, in the Web section |

The classes exist on every platform, so the same scripts build and run everywhere. Where a
service is missing (desktop, the editor's Play, an export with the setting off), calls
that expect an answer report "not available" through their usual event, and the first
call logs a warning naming the setting to turn on.

## How results arrive {#how-results-arrive}

Every result arrives as an event, never as a return value: an ad loaded, a purchase went
through, a portal finished starting. The platform answers on its own thread. The engine
queues each answer and runs the subscribers at the start of the next frame, on the game
thread and before the scenes update, so a handler can use the scene like any other
script code.

Subscribe with the same helpers as any other [event](events.md#service-events):

=== "C++"

    ```cpp
    // Ads.h
    #include "ScriptBase.h"
    #include "AdMob.h"

    class Ads : public doriax::ScriptBase {
    public:
        Ads(doriax::Scene* scene, doriax::Entity entity);
        ~Ads();

        void onAdLoaded(doriax::AdMobFormat format);
    };

    // Ads.cpp
    Ads::Ads(Scene* scene, Entity entity): ScriptBase(scene, entity) {
        REGISTER_EVENT(AdMob::onAdLoaded, onAdLoaded);
    }

    Ads::~Ads() {
        UNREGISTER_EVENT(AdMob::onAdLoaded, onAdLoaded);
    }

    void Ads::onAdLoaded(AdMobFormat format) {
    }
    ```

=== "Lua"

    ```lua
    function Ads:init()
        RegisterEvent(self, AdMob.onAdLoaded, "onAdLoaded")
    end

    function Ads:onAdLoaded(format)
    end
    ```

- A C++ handler takes the parameters exactly as the event declares them, by value
  (`std::string`, not `const std::string&`), or the macro does not compile.
- The Code Editor's [Add event](../editor/code-editor.md#add-events) menu lists these
  events under **AdMob**, **In-App Purchase** and **Web Portal**, and writes the
  registration and the handler for you.
- The events belong to the class, not to a scene, so they keep firing across scene
  changes. A Lua script's `RegisterEvent` subscriptions are removed with the script, and a
  C++ script removes its own with `UNREGISTER_EVENT`. A function assigned straight to an
  event (`AdMob.onAdLoaded = function(format) ... end`) stays until the game shuts down.

### Ads pause the game {#ads-pause-the-game}

While a full-screen ad covers the game, the engine pauses just as when the app goes to
the background: sounds pause, the update loop stops, and
[`Engine::onPause`](../reference/classes/engine.md#onpause) fires.
[`Engine::onResume`](../reference/classes/engine.md#onresume) follows when the ad closes.
The same happens while a banner's click opens a page over the game, and on the web while
a portal ad plays or a portal pauses the game itself.

On Android the whole app pauses while a full-screen ad shows, so the events of that ad
(`onAdShown`, `onAdImpression`, `onUserEarnedReward`, ...) arrive together when it closes.

## AdMob

### Setup {#admob-setup}

1. Create the app and its ad units in the [AdMob console](https://admob.google.com).
2. In **Project Settings → Platforms**, open the **Android** and **iOS** sections, tick
   **Google AdMob**, and paste the **AdMob App ID** (`ca-app-pub-…~…`). Left empty, the
   export uses Google's sample app, which only serves test ads.
3. On Android, declare in the Play Console that the app contains ads and uses the
   advertising ID. Exports raise **Min SDK** to 24 for AdMob.
4. On iOS, fill in **Tracking Description** when your consent message asks for tracking
   permission.
5. Export as **Source Code** and build with Android Studio or Xcode. Ads only run on a
   device, emulator or simulator; the editor has no AdMob.

See [Android](../editor/project-settings.md#android) and
[iOS](../editor/project-settings.md#ios) settings for what each field writes.

### Consent, then initialize {#admob-consent}

Google's policies require a consent message for users in the EEA, the UK and
Switzerland, and privacy messages for some US states. `AdMob` shows both through Google's
User Messaging Platform, so a game asks first and starts Google Mobile Ads after:

1. Call [`requestConsent()`](../reference/classes/admob.md#requestconsent) at every
   launch. It updates the consent information and shows Google's consent form when the
   user still has to answer.
2. [`onConsentUpdated`](../reference/classes/admob.md#events) reports the result
   (`errorCode` 0 on success). When
   [`canRequestAds()`](../reference/classes/admob.md#getconsentstatus-canrequestads) is
   true, call [`initialize()`](../reference/classes/admob.md#initialize-isinitialized).
   Consent given in an earlier launch counts, even if this request failed offline.
3. `onInitialized` fires once Google Mobile Ads is ready. Load the first ads there.

Audience settings such as
[`setAgeRestriction`](../reference/classes/admob.md#request-settings) and
[`setMaxAdContentRating`](../reference/classes/admob.md#request-settings) go before
`requestConsent()`.

=== "C++"

    ```cpp
    // Ads.h
    #include "ScriptBase.h"
    #include "AdMob.h"

    class Ads : public doriax::ScriptBase {
    public:
        Ads(doriax::Scene* scene, doriax::Entity entity);
        ~Ads();

        void showBreak();

        void onConsentUpdated(int errorCode, std::string message);
        void onInitialized();
        void onAdDismissed(doriax::AdMobFormat format);
    };

    // Ads.cpp
    #include "Ads.h"

    using namespace doriax;

    static const char* interstitialId = "ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx";

    Ads::Ads(Scene* scene, Entity entity): ScriptBase(scene, entity) {
        REGISTER_EVENT(AdMob::onConsentUpdated, onConsentUpdated);
        REGISTER_EVENT(AdMob::onInitialized, onInitialized);
        REGISTER_EVENT(AdMob::onAdDismissed, onAdDismissed);

        AdMob::requestConsent();
    }

    Ads::~Ads() {
        UNREGISTER_EVENT(AdMob::onConsentUpdated, onConsentUpdated);
        UNREGISTER_EVENT(AdMob::onInitialized, onInitialized);
        UNREGISTER_EVENT(AdMob::onAdDismissed, onAdDismissed);
    }

    void Ads::onConsentUpdated(int errorCode, std::string message) {
        if (errorCode != 0) {
            Log::warn("Consent: %s", message.c_str());
        }
        if (AdMob::canRequestAds() && !AdMob::isInitialized()) {
            AdMob::initialize();
        }
    }

    void Ads::onInitialized() {
        AdMob::loadInterstitialAd(interstitialId);
    }

    // At a natural break, like the end of a level
    void Ads::showBreak() {
        if (AdMob::isInterstitialAdLoaded()) {
            AdMob::showInterstitialAd();
        }
    }

    // Each ad shows once, so load the next one
    void Ads::onAdDismissed(AdMobFormat format) {
        if (format == AdMobFormat::INTERSTITIAL) {
            AdMob::loadInterstitialAd(interstitialId);
        }
    }
    ```

=== "Lua"

    ```lua
    local Ads = {}

    local INTERSTITIAL_ID = "ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx"

    function Ads:init()
        RegisterEvent(self, AdMob.onConsentUpdated, "onConsentUpdated")
        RegisterEvent(self, AdMob.onInitialized, "onInitialized")
        RegisterEvent(self, AdMob.onAdDismissed, "onAdDismissed")

        AdMob.requestConsent()
    end

    function Ads:onConsentUpdated(errorCode, message)
        if errorCode ~= 0 then
            Log.warn("Consent: " .. message)
        end
        if AdMob.canRequestAds() and not AdMob.isInitialized() then
            AdMob.initialize()
        end
    end

    function Ads:onInitialized()
        AdMob.loadInterstitialAd(INTERSTITIAL_ID)
    end

    -- At a natural break, like the end of a level
    function Ads:showBreak()
        if AdMob.isInterstitialAdLoaded() then
            AdMob.showInterstitialAd()
        end
    end

    -- Each ad shows once, so load the next one
    function Ads:onAdDismissed(format)
        if format == AdMobFormat.INTERSTITIAL then
            AdMob.loadInterstitialAd(INTERSTITIAL_ID)
        end
    end

    return Ads
    ```

When [`isPrivacyOptionsRequired()`](../reference/classes/admob.md#isprivacyoptionsrequired-showprivacyoptionsform)
is true, Google requires a way back to the consent form, such as a **Privacy** button in
the settings menu that calls `showPrivacyOptionsForm()`.

### Full-screen ads {#full-screen-ads}

Interstitial, rewarded, rewarded interstitial and app open ads work the same way:

| Step | Call | Result |
| --- | --- | --- |
| Load | `loadInterstitialAd(adUnitId)`, `loadRewardedAd`, `loadRewardedInterstitialAd`, `loadAppOpenAd` | `onAdLoaded(format)` or `onAdFailedToLoad(format, errorCode, message)` |
| Check | `isInterstitialAdLoaded()`, ... | `true` between `onAdLoaded` and the show |
| Show | `showInterstitialAd()`, ... | `onAdShown`, `onAdImpression`, then `onAdDismissed`; or `onAdFailedToShow` |

- Loading a format again replaces its ad, and only the latest load reports.
- An ad shows once: `is...Loaded()` turns false when it is shown, so load the next one,
  usually in `onAdDismissed`.
- Showing an ad that is not loaded reports `onAdFailedToShow` with
  [`AdMob::errorNotLoaded`](../reference/classes/admob.md#constants).
- A failed load reports Google's error code. Retry after a delay rather than at once:
  Google advises against reloading in a loop.

**Rewarded** and **rewarded interstitial** ads grant their reward through
`onUserEarnedReward(format, type, amount)`, with the type and amount set on the ad unit.
Grant it there, not in `onAdDismissed`: a player who closes the ad early earns nothing.
For rewards checked by your server, call
[`setServerSideVerificationOptions`](../reference/classes/admob.md#setserversideverificationoptions)
before showing.

**App open** ads cover the app at launch or when it returns from the background. Google
stops serving one four hours after it loaded, so `isAppOpenAdLoaded()` turns false by
then, and the ad needs loading again.

!!! warning "`Engine::onResume` also follows every ad"
    Since full-screen ads [pause the game](#ads-pause-the-game), `onResume` fires after
    each of them, and after anything else that briefly covers the app, like Google Play's
    purchase screen. A game that shows an app open ad from `onResume` needs a flag, set
    before showing its other ads, that skips those resumes.

### Banners {#banners}

[`loadBannerAd(adUnitId, size, position)`](../reference/classes/admob.md#loadbannerad)
places a banner over the game, at the bottom by default. It shows as soon as it loads,
replacing any banner already there.

=== "C++"

    ```cpp
    AdMob::loadBannerAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx", AdMobBannerSize::ADAPTIVE, AdMobBannerPosition::TOP);
    ```

=== "Lua"

    ```lua
    AdMob.loadBannerAd("ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx", AdMobBannerSize.ADAPTIVE, AdMobBannerPosition.TOP)
    ```

- `ADAPTIVE`, the default size, takes the screen width when it loads and lets Google pick
  the height. Load it again after the screen rotates.
- `hideBannerAd()` and `showBannerAd()` toggle it, `setBannerAdPosition()` moves it, and
  `removeBannerAd()` destroys it.
- `getBannerAdWidth()` and `getBannerAdHeight()` give its size in screen pixels once
  loaded, to keep game UI clear of it. On Android the banner also stays out of display
  cutouts and visible system bars.
- Banners refresh at the rate set on their ad unit. A refresh that fails reports
  `onAdFailedToLoad(BANNER, ...)`, but the last ad keeps showing.

### Audience and privacy {#admob-audience}

| Call | Use |
| --- | --- |
| `setAgeRestriction(CHILD)` | The game is for children. Requests get Google's child treatment, and `requestConsent()` asks as for a user under the age of consent |
| `setAgeRestriction(TEEN)` | The game is for teens. Requests get Google's teen treatment |
| `setMaxAdContentRating(rating)` | Highest content rating of ads: `GENERAL`, `PARENTAL_GUIDANCE`, `TEEN` or `MATURE_AUDIENCE` |
| `setPersonalization(DISABLED)` | Only non-personalized ads |

These apply to the requests made after them. See
[Request settings](../reference/classes/admob.md#request-settings).

### Testing {#admob-testing}

Clicking live ads from your own devices breaks AdMob's policies, so use test ads while
developing:

- Use Google's demo ad units, listed for
  [Android](https://developers.google.com/admob/android/test-ads) and
  [iOS](https://developers.google.com/admob/ios/test-ads), or
- register your devices with
  [`setTestDeviceIds`](../reference/classes/admob.md#settestdeviceids-gettestdeviceids).
  Google Mobile Ads prints the device's hashed ID to the device log (Logcat or the
  Xcode console) on the first request.

On a test device, `setConsentDebugGeography(AdMobDebugGeography::EEA)` makes the consent
form appear as it would in Europe, and `resetConsent()` forgets the last answer.
`openAdInspector()` opens Google's Ad Inspector on a test device, to check each ad unit's
requests and mediation results.

### Revenue and volume {#admob-revenue}

`onAdPaid(format, valueMicros, currencyCode, precision)` reports what each ad earned, in
millionths of the currency, for your own analytics. `setAppVolume(volume)` and
`setAppMuted(muted)` tell Google how loud video ads should play relative to the game, so
they match a game whose volume is turned down.

## In-app purchases {#in-app-purchases}

`InAppPurchase` sells one-time products and subscriptions through Google Play Billing on
Android and StoreKit 2 on iOS, with one API: products are queried, bought and settled the
same way on both. The [App Store differences](#iap-ios) are listed at the end.

### Setup {#iap-setup}

=== "Android"

    1. Tick **Google Play Billing** in **Project Settings → Platforms → Android**. Exports
       raise **Min SDK** to 23 for it.
    2. In the Play Console, create the products: **one-time products** (consumable or not)
       and **subscriptions** with their base plans and offers.
    3. Upload a build to a testing track (internal testing is enough) with the same package
       name, and add your Google accounts as license testers so their purchases are not
       charged. Google Play only sells the products of an app it knows.

=== "iOS"

    1. Tick **App Store Purchases** in **Project Settings → Platforms → iOS**. Building it
       needs Xcode 16.3 or later.
    2. In App Store Connect, create the in-app purchases (consumable, non-consumable or
       non-renewing subscription) and the auto-renewable subscriptions, which belong to a
       subscription group.
    3. Test with a Sandbox Apple Account, or with a StoreKit configuration file selected in
       the Xcode scheme, which works before anything is set up in App Store Connect.

On every other platform, and in builds without the setting, the calls report
`BillingResponse::BILLING_UNAVAILABLE`.

### The purchase flow {#iap-flow}

1. [`initialize()`](../reference/classes/inapppurchase.md#initialize-isready) connects to
   the store. `onInitialized(response, message)` reports `OK` when it is ready; calls made
   before that fail with `SERVICE_DISCONNECTED`. On Android, a lost connection
   (`onDisconnected`) comes back by itself on the next call.
2. [`queryProducts(ids, type)`](../reference/classes/inapppurchase.md#queryproducts)
   fetches the localized names and prices. After `onProductsQueried`, read them with
   `getProducts()` or `getProduct(id)` to fill the store screen.
3. [`purchase(productId)`](../reference/classes/inapppurchase.md#purchase) opens the
   store's purchase screen for a queried product. The result is
   `onPurchaseUpdated(purchase)`, or `onPurchaseFailed(productId, response, message)` when
   the player cancels (`USER_CANCELED`) or something goes wrong.
4. In `onPurchaseUpdated`, grant the product only when `purchase.state` is `PURCHASED`. A
   `PENDING` purchase waits for something outside the app, like a cash payment at a store
   or a parent approving it with Ask to Buy, and the event fires again when it completes.
5. Settle the purchase:
   [`consumePurchase(token)`](../reference/classes/inapppurchase.md#acknowledgepurchase-consumepurchase)
   for consumables, which can then be bought again, and
   [`acknowledgePurchase(token)`](../reference/classes/inapppurchase.md#acknowledgepurchase-consumepurchase)
   for everything else. Google Play refunds a purchase left unsettled for three days, and
   the App Store delivers it again at every launch.

!!! warning "Grant a consumable before consuming it, once per token"
    The same purchase can be reported more than once: by the purchase screen, by a query,
    again at the next launch. Once consumed, it is never reported again. So grant and save
    a consumable *before* consuming it, and remember its `purchaseToken` so that a second
    report does not grant it twice.

Purchases also complete outside the purchase screen: a pending payment clears, a promo
code is redeemed, the player buys on another device. Call
[`queryPurchases(type)`](../reference/classes/inapppurchase.md#querypurchases) for each
product type at startup and on `Engine::onResume`. It reports every owned purchase through
`onPurchaseUpdated` (with `restored` set), then `onPurchasesQueried`, and drops refunded
and expired ones from `getPurchases()` and
[`isPurchased(productId)`](../reference/classes/inapppurchase.md#getpurchases-ispurchased).

Give the store screen a **Restore Purchases** button too, which calls
[`restorePurchases()`](../reference/classes/inapppurchase.md#restorepurchases): it queries
both types, and on iOS first syncs the player's App Store account, which may ask them to
sign in. Apple's review guidelines ask for a way to restore purchases that can be
restored.

=== "C++"

    ```cpp
    // Store.h (declarations)
    void buyCoins();
    void restore();

    void onStoreReady(doriax::BillingResponse response, std::string message);
    void onResume();
    void onPurchaseUpdated(doriax::PurchaseDetails purchase);
    void onPurchaseFailed(std::string productId, doriax::BillingResponse response, std::string message);

    // Store.cpp
    static const std::string coinsId = "coins_100";    // consumable
    static const std::string noAdsId = "remove_ads";   // bought once

    Store::Store(Scene* scene, Entity entity): ScriptBase(scene, entity) {
        REGISTER_EVENT(InAppPurchase::onInitialized, onStoreReady);
        REGISTER_EVENT(InAppPurchase::onPurchaseUpdated, onPurchaseUpdated);
        REGISTER_EVENT(InAppPurchase::onPurchaseFailed, onPurchaseFailed);
        REGISTER_ENGINE_EVENT(onResume);

        InAppPurchase::initialize();
    }

    void Store::onStoreReady(BillingResponse response, std::string message) {
        if (response != BillingResponse::OK) {
            Log::warn("Store unavailable: %s", message.c_str());
            return;
        }
        InAppPurchase::queryProducts({coinsId, noAdsId}, ProductType::INAPP);
        InAppPurchase::queryPurchases(ProductType::INAPP);
    }

    void Store::onResume() {
        if (InAppPurchase::isReady()) {
            InAppPurchase::queryPurchases(ProductType::INAPP);
        }
    }

    // From a Buy button
    void Store::buyCoins() {
        InAppPurchase::purchase(coinsId);
    }

    // From a Restore Purchases button
    void Store::restore() {
        InAppPurchase::restorePurchases();
    }

    void Store::onPurchaseUpdated(PurchaseDetails purchase) {
        if (purchase.state != PurchaseState::PURCHASED) return;

        if (purchase.productId == coinsId) {
            // Grant and save once per token, then consume
            const std::string granted = "granted_" + purchase.purchaseToken;
            if (!UserSettings::getBoolForKey(granted.c_str(), false)) {
                UserSettings::setIntegerForKey("coins", UserSettings::getIntegerForKey("coins", 0) + 100);
                UserSettings::setBoolForKey(granted.c_str(), true);
            }
            InAppPurchase::consumePurchase(purchase.purchaseToken);
        } else if (!purchase.acknowledged) {
            InAppPurchase::acknowledgePurchase(purchase.purchaseToken);
        }
        // remove_ads is checked with InAppPurchase::isPurchased(noAdsId)
    }

    void Store::onPurchaseFailed(std::string productId, BillingResponse response, std::string message) {
        if (response != BillingResponse::USER_CANCELED) {
            Log::warn("Purchase failed: %s", message.c_str());
        }
    }
    ```

=== "Lua"

    ```lua
    local Store = {}

    local COINS = "coins_100"     -- consumable
    local NO_ADS = "remove_ads"   -- bought once

    function Store:init()
        RegisterEvent(self, InAppPurchase.onInitialized, "onStoreReady")
        RegisterEvent(self, InAppPurchase.onPurchaseUpdated, "onPurchaseUpdated")
        RegisterEvent(self, InAppPurchase.onPurchaseFailed, "onPurchaseFailed")
        RegisterEngineEvent(self, "onResume")

        InAppPurchase.initialize()
    end

    function Store:onStoreReady(response, message)
        if response ~= BillingResponse.OK then
            Log.warn("Store unavailable: " .. message)
            return
        end
        InAppPurchase.queryProducts({COINS, NO_ADS}, ProductType.INAPP)
        InAppPurchase.queryPurchases(ProductType.INAPP)
    end

    function Store:onResume()
        if InAppPurchase.isReady() then
            InAppPurchase.queryPurchases(ProductType.INAPP)
        end
    end

    -- From a Buy button
    function Store:buyCoins()
        InAppPurchase.purchase(COINS)
    end

    -- From a Restore Purchases button
    function Store:restore()
        InAppPurchase.restorePurchases()
    end

    function Store:onPurchaseUpdated(purchase)
        if purchase.state ~= PurchaseState.PURCHASED then
            return
        end
        if purchase.productId == COINS then
            -- Grant and save once per token, then consume
            local granted = "granted_" .. purchase.purchaseToken
            if not UserSettings.getBoolForKey(granted, false) then
                UserSettings.setIntegerForKey("coins", UserSettings.getIntegerForKey("coins", 0) + 100)
                UserSettings.setBoolForKey(granted, true)
            end
            InAppPurchase.consumePurchase(purchase.purchaseToken)
        elseif not purchase.acknowledged then
            InAppPurchase.acknowledgePurchase(purchase.purchaseToken)
        end
        -- remove_ads is checked with InAppPurchase.isPurchased(NO_ADS)
    end

    function Store:onPurchaseFailed(productId, response, message)
        if response ~= BillingResponse.USER_CANCELED then
            Log.warn("Purchase failed: " .. message)
        end
    end

    return Store
    ```

A consumable left unconsumed, because the app closed before the consume finished, comes
back through `queryPurchases` or at the next launch; its saved token keeps it from being
granted twice, and it is consumed then.

### Subscriptions {#subscriptions}

Query subscriptions with `ProductType::SUBS`, both with `queryProducts` and with
`queryPurchases`. On Google Play, each product lists its base plans and offers in
[`offers`](../reference/classes/inapppurchase.md#productoffer), each with an `offerToken`
and its [`pricingPhases`](../reference/classes/inapppurchase.md#pricingphase), such as a
free week followed by a monthly price. `purchase(productId, offerToken)` buys that plan;
without a token it buys the first base plan. An App Store subscription has one plan, so
`offers` holds a single entry, with no token, whose first phase is the introductory offer
when the player is eligible for it.

- Acknowledge a subscription like any non-consumable. `isPurchased(productId)` is true
  while it is active.
- A subscription on hold for a payment problem arrives with `suspended` set, and
  `isPurchased` turns false. `showInAppMessages()` lets Google Play prompt the player to
  fix the payment, which iOS does by itself, and `openSubscriptionManagement(productId)`
  opens the store's subscription management.
- `changeSubscription(productId, offerToken, oldPurchaseToken, mode)` upgrades or
  downgrades an owned subscription. On Google Play, the
  [`SubscriptionReplacementMode`](../reference/classes/inapppurchase.md#subscriptionreplacementmode)
  decides how the time left on the old plan is billed. On the App Store, it buys the new
  product, and the App Store replaces the subscription of the same group.

### Security {#iap-security}

Purchase data comes from the player's device, which they can tamper with. For anything
of value, send the purchase to your server and verify it there before granting: the
`purchaseToken` with the Google Play Developer API, or on iOS the `signature`, which is
the transaction's JWS, with Apple's App Store Server Library or API.
`setObfuscatedAccountId` attaches an id of your own user account to the next purchases,
which helps the store detect fraud and helps your server match a purchase to an account.
Use a hash on Google Play; the App Store takes it only as a UUID.

### App Store differences {#iap-ios}

| | Google Play | App Store |
| --- | --- | --- |
| `purchaseToken` | Google Play's purchase token | The original transaction id, which renewals keep |
| `orderId` | The order id | The transaction id |
| `originalJson`, `signature` | The signed purchase data and its signature | The transaction JSON and its JWS |
| Offers | Base plans and offers, chosen with an `offerToken` | One plan per product. `offerToken` is ignored, and the introductory offer applies by itself |
| Unsettled purchases | Refunded after three days | Delivered again at every launch |
| `changeSubscription` | Applies the replacement mode | Buys the new product; `mode` is ignored |
| `setObfuscatedAccountId` | Any id, ideally a hash | A UUID, kept as the transaction's `appAccountToken`. Anything else is left out with a warning, and the profile id is not used |
| Pending purchases | Payments made outside the app | Ask to Buy: reported as `PENDING` with no `purchaseToken`, then as a new purchase once approved |
| Refunds and expirations | Gone after the next `queryPurchases` | Gone after the next `queryPurchases`. Those StoreKit announces while the game runs also arrive through `onPurchaseUpdated`, with state `UNSPECIFIED` |
| `showInAppMessages()` | Shows Google Play's messages | Does nothing: iOS shows them by itself |
| `openSubscriptionManagement()` | Opens Google Play's subscription center | Shows Apple's subscription sheet over the game, then queries the subscriptions again |
| Non-renewing subscriptions | — | `INAPP` products that the store never expires: work out the end from `purchaseTime` |

## Web portals {#web-portals}

Web game portals pay through ads and expect games to report what the player is doing, so
the portal can choose the moment for an ad. `WebPortal` gives one API for five portals:

| Portal | **Game Portal** value | Notes |
| --- | --- | --- |
| [CrazyGames](https://docs.crazygames.com) | CrazyGames | SDK v3 |
| [Poki](https://sdk.poki.com) | Poki | SDK v2 |
| [GameDistribution](https://gamedistribution.com) | GameDistribution | Needs the **Portal Game ID** from the GameDistribution dashboard |
| [Yandex Games](https://yandex.com/dev/games/doc/en/) | Yandex Games | The SDK only starts inside Yandex Games |
| [YouTube Playables](https://developers.google.com/youtube/gaming/playables) | YouTube Playables | Adds cloud saves and a platform mute |

Each export builds in one portal, chosen with **Game Portal** in
[Project Settings → Platforms → Web](../editor/project-settings.md#web), so a game sent
to several portals needs one export each. `WebPortal::getPortal()` tells which one a
build has.

### Using the portal {#web-portal-flow}

1. Call [`initialize()`](../reference/classes/webportal.md#initialize) once, at startup.
   It loads the portal's SDK, and `onInitialized(environment)` reports where the game
   runs. Calls made after `initialize()` wait for the SDK; calls made before it are
   dropped, and ads and saves report an error.
2. Call `loadingStop()` once the game can be played. Yandex Games and YouTube Playables
   require it. Bracket later loading screens with `loadingStart()` and `loadingStop()`.
3. Call `gameplayStart()` when play starts or resumes, and `gameplayStop()` at every
   break: menus, pauses, the end of a level.
4. Request ads with [`requestAd()`](../reference/classes/webportal.md#requestad):
   `MIDGAME` at natural breaks and `REWARDED` when the player chooses to watch one. The
   result is `onAdStarted` then `onAdFinished`, or `onAdError(type, code, message)`.
5. Call `happytime()` at happy moments, like a level completed.

=== "C++"

    ```cpp
    // Portal.h (declarations)
    void startLevel();
    void levelComplete();
    void watchAdForCoins();

    void onAdFinished(doriax::WebPortalAdType type);
    void onAdError(doriax::WebPortalAdType type, std::string code, std::string message);

    // Portal.cpp
    Portal::Portal(Scene* scene, Entity entity): ScriptBase(scene, entity) {
        REGISTER_EVENT(WebPortal::onAdFinished, onAdFinished);
        REGISTER_EVENT(WebPortal::onAdError, onAdError);

        WebPortal::initialize();
        WebPortal::loadingStop();   // waits for the SDK
    }

    void Portal::startLevel() {
        WebPortal::gameplayStart();
    }

    void Portal::levelComplete() {
        WebPortal::happytime();
        WebPortal::gameplayStop();
        WebPortal::requestAd(WebPortalAdType::MIDGAME);   // the portal may show none
    }

    void Portal::watchAdForCoins() {
        WebPortal::requestAd(WebPortalAdType::REWARDED);
    }

    void Portal::onAdFinished(WebPortalAdType type) {
        if (type == WebPortalAdType::REWARDED) {
            // add the coins
        }
    }

    void Portal::onAdError(WebPortalAdType type, std::string code, std::string message) {
        if (type == WebPortalAdType::REWARDED) {
            // tell the player no ad could be shown
        }
    }
    ```

=== "Lua"

    ```lua
    local Portal = {}

    function Portal:init()
        RegisterEvent(self, WebPortal.onAdFinished, "onAdFinished")
        RegisterEvent(self, WebPortal.onAdError, "onAdError")

        WebPortal.initialize()
        WebPortal.loadingStop()   -- waits for the SDK
    end

    function Portal:startLevel()
        WebPortal.gameplayStart()
    end

    function Portal:levelComplete()
        WebPortal.happytime()
        WebPortal.gameplayStop()
        WebPortal.requestAd(WebPortalAdType.MIDGAME)   -- the portal may show none
    end

    function Portal:watchAdForCoins()
        WebPortal.requestAd(WebPortalAdType.REWARDED)
    end

    function Portal:onAdFinished(adType)
        if adType == WebPortalAdType.REWARDED then
            -- add the coins
        end
    end

    function Portal:onAdError(adType, code, message)
        if adType == WebPortalAdType.REWARDED then
            -- tell the player no ad could be shown
        end
    end

    return Portal
    ```

Portals decide when a midgame ad really plays, so a request often shows none and reports
`onAdError` with the code `unfilled`. The codes are:

| Code | Meaning |
| --- | --- |
| `unfilled` | No ad played: the portal had none, chose not to show one now, or another ad is playing |
| `unavailable` | No portal SDK: a build without a portal, `initialize()` not called, or the portal refused to start here |
| `other` | The ad started but failed, or a rewarded ad was closed before its reward |
| A CrazyGames code | CrazyGames passes its own codes, like `adCooldown` |

A rewarded ad grants its reward only through `onAdFinished`.

### Environments {#web-portal-environments}

`onInitialized` and `getEnvironment()` report a
[`WebPortalEnvironment`](../reference/classes/webportal.md#webportalenvironment):

| Value | Meaning |
| --- | --- |
| `UNINITIALIZED` | `initialize()` has not finished yet |
| `DISABLED` | No portal in this build, its SDK failed to load, or the portal does not run on this host (CrazyGames outside its site, Yandex Games outside its frame, YouTube outside Playables). Calls do nothing, and ads report `unavailable` |
| `LOCAL` | `localhost`, `127.0.0.1` or `[::1]`, where most portals show test ads |
| `PORTAL` | Any other host, normally the portal's |

`isAvailable()` is true for `LOCAL` and `PORTAL`.

### Pauses and mute {#web-portal-pauses}

The engine [pauses](#ads-pause-the-game) while one of its ads plays. GameDistribution,
Yandex Games and YouTube Playables also pause the game themselves: for an ad they start
on their own, a purchase window, or the player switching away. The engine stays paused
until both the ad and the portal let it go, and `Engine::onResume` follows.

YouTube Playables can mute a game from its own interface. The engine follows it: audio
stays silent while YouTube has it off, whatever the game's
[global volume](../reference/classes/audiosystem.md) is.

### Cloud saves {#web-portal-cloud-saves}

YouTube Playables saves progress in the player's account. Call `loadData()` at startup
and read the save in `onDataLoaded(data)`, which is empty when nothing was saved yet.
`saveData(data)` stores one string, like a JSON document, and reports only failures,
through `onDataSaveFailed`. YouTube refuses saves made before a `loadData()`, and its
rules require progress to be saved this way.

Other portals have no cloud save, so `loadData()` reports `onDataLoadFailed`. Save there
with [`UserSettings`](../reference/classes/usersettings.md), which the web stores in the
browser.

### What each portal supports {#web-portal-support}

| Call or event | CrazyGames | Poki | GameDistribution | Yandex Games | YouTube Playables |
| --- | --- | --- | --- | --- | --- |
| `requestAd(MIDGAME)` | Midgame ad | Commercial break | Interstitial | Fullscreen ad | Interstitial |
| `requestAd(REWARDED)` | Yes | Yes | Yes | Yes | Yes |
| `onAdStarted` | Yes | Yes | Yes | Yes | No: YouTube pauses the game instead |
| `gameplayStart` / `gameplayStop` | Yes | Yes | No | Yes | No |
| `loadingStart` | Yes | Yes | No | No | No |
| `loadingStop` | Yes | Yes | No | Required | Required |
| `happytime` | Yes | Yes | No | No | No |
| `loadData` / `saveData` | No | No | No | No | Yes |
| Pauses the game itself | No | No | Yes | Yes | Yes |

A call a portal does not support does nothing.

### Testing on your machine {#web-portal-testing}

Serve the exported folder from `localhost` (see
[Export Window → Web mode](../editor/export.md#web-mode)) and the portal SDKs act as
follows:

- **CrazyGames** shows demo ads on `localhost`. On another host outside CrazyGames, add
  `?useLocalSdk=true` to the URL for the same.
- **Poki** runs in debug mode on `localhost`, with test ads.
- **GameDistribution** needs the **Portal Game ID** even locally. For test ads, set the
  `gd_debug_ex` and `gd_tag` keys of the page's `localStorage` to `true`.
- **Yandex Games** loads its SDK from `/sdk.js`, which Yandex's hosting serves; on other
  hosts the portal is `DISABLED`. Yandex's
  [`@yandex-games/sdk-dev-proxy`](https://www.npmjs.com/package/@yandex-games/sdk-dev-proxy)
  serves a mock SDK with placeholder ads (run it with `--dev-mode=true`).
- **YouTube Playables** runs only inside YouTube, and is `DISABLED` anywhere else. The
  export adds YouTube's SDK `<script>` to the page head, which YouTube requires to load
  before the game. Test it with YouTube's Playables test suite.

## Migrating from the System methods {#migrating}

Earlier versions had AdMob and CrazyGames methods on [`System`](../reference/classes/system.md).
They were replaced by the classes on this page:

| Before | Now |
| --- | --- |
| `System::initializeAdMob(childDirected, underAge)` | `AdMob::setAgeRestriction(AdMobAgeRestriction::CHILD)` for a children's game, then `AdMob::requestConsent()` and `AdMob::initialize()`, as in [Consent, then initialize](#admob-consent) |
| `System::setMaxAdContentRating(AdMobRating::General)` | `AdMob::setMaxAdContentRating(AdMobRating::GENERAL)`. The values are upper case now, with `UNSPECIFIED` added |
| `System::loadInterstitialAd(id)`, `isInterstitialAdLoaded()`, `showInterstitialAd()` | `AdMob::loadInterstitialAd(id)`, `AdMob::isInterstitialAdLoaded()`, `AdMob::showInterstitialAd()` |
| `System::initializeCrazyGamesSDK()` | **Game Portal** set to CrazyGames, then `WebPortal::initialize()` |
| `System::showCrazyGamesAd("midgame")`, `("rewarded")` | `WebPortal::requestAd(WebPortalAdType::MIDGAME)`, `(WebPortalAdType::REWARDED)` |
| `System::happytimeCrazyGames()` | `WebPortal::happytime()` |
| `System::gameplayStartCrazyGames()`, `gameplayStopCrazyGames()` | `WebPortal::gameplayStart()`, `WebPortal::gameplayStop()` |
| `System::loadingStartCrazyGames()`, `loadingStopCrazyGames()` | `WebPortal::loadingStart()`, `WebPortal::loadingStop()` |

Lua scripts make the same change: `System.showInterstitialAd()` becomes
`AdMob.showInterstitialAd()`. Ads now also need **Google AdMob** or **Game Portal** in
the project settings, since exports only include the SDKs that are enabled.

## Reference

- [AdMob](../reference/classes/admob.md)
- [InAppPurchase](../reference/classes/inapppurchase.md)
- [WebPortal](../reference/classes/webportal.md)
- [Project Settings → Platforms](../editor/project-settings.md#platforms)
