---
description: InAppPurchase API reference (C++ and Lua) — one-time products and subscriptions through Google Play Billing on Android and StoreKit 2 on iOS.
---

# InAppPurchase

**C++ type:** `InAppPurchase` (static) · **Header:** `InAppPurchase.h`

## Description

One-time products, consumable or not, and subscriptions, through Google Play Billing on
Android and StoreKit 2 on iOS. Exports include it only when **Google Play Billing** is
enabled in the project's [Android settings](../../editor/project-settings.md#android), or
**App Store Purchases** in its [iOS settings](../../editor/project-settings.md#ios). On
every other platform the calls report `BILLING_UNAVAILABLE` through their events.

Results arrive as [events](#events) at the start of a frame. A purchase must be
acknowledged or consumed: Google Play refunds one left unsettled for three days, and the
App Store delivers it again at every launch. See
[Monetization → In-app purchases](../../manual/monetization.md#in-app-purchases) for the
setup, a complete store script, and the
[App Store differences](../../manual/monetization.md#iap-ios).

=== "C++"

    ```cpp
    REGISTER_EVENT(InAppPurchase::onPurchaseUpdated, onPurchaseUpdated);
    InAppPurchase::purchase("remove_ads");

    void Store::onPurchaseUpdated(PurchaseDetails purchase) {
        if (purchase.state == PurchaseState::PURCHASED && !purchase.acknowledged) {
            InAppPurchase::acknowledgePurchase(purchase.purchaseToken);
        }
    }
    ```

=== "Lua"

    ```lua
    RegisterEvent(self, InAppPurchase.onPurchaseUpdated, "onPurchaseUpdated")
    InAppPurchase.purchase("remove_ads")

    function Store:onPurchaseUpdated(purchase)
        if purchase.state == PurchaseState.PURCHASED and not purchase.acknowledged then
            InAppPurchase.acknowledgePurchase(purchase.purchaseToken)
        end
    end
    ```

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static void | [initialize](#initialize-isready) | C++ \| Lua |
| static bool | [isReady](#initialize-isready) | C++ \| Lua |
| static void | [queryProducts](#queryproducts) | C++ \| Lua |
| static bool | [hasProduct](#hasproduct-getproduct-getproducts) | C++ \| Lua |
| static [ProductDetails](#productdetails) | [getProduct](#hasproduct-getproduct-getproducts) | C++ \| Lua |
| static std::vector\<[ProductDetails](#productdetails)\> | [getProducts](#hasproduct-getproduct-getproducts) | C++ \| Lua |
| static void | [purchase](#purchase) | C++ \| Lua |
| static void | [changeSubscription](#changesubscription) | C++ \| Lua |
| static void | [acknowledgePurchase](#acknowledgepurchase-consumepurchase) | C++ \| Lua |
| static void | [consumePurchase](#acknowledgepurchase-consumepurchase) | C++ \| Lua |
| static void | [queryPurchases](#querypurchases) | C++ \| Lua |
| static void | [restorePurchases](#restorepurchases) | C++ \| Lua |
| static std::vector\<[PurchaseDetails](#purchasedetails)\> | [getPurchases](#getpurchases-ispurchased) | C++ \| Lua |
| static bool | [isPurchased](#getpurchases-ispurchased) | C++ \| Lua |
| static void | [setObfuscatedAccountId](#setobfuscatedaccountid-setobfuscatedprofileid) | C++ \| Lua |
| static void | [setObfuscatedProfileId](#setobfuscatedaccountid-setobfuscatedprofileid) | C++ \| Lua |
| static void | [openSubscriptionManagement](#opensubscriptionmanagement) | C++ \| Lua |
| static void | [showInAppMessages](#showinappmessages) | C++ \| Lua |

### Callback events

| Callback | Name | Languages |
| --- | --- | --- |
| void(BillingResponse, std::string) | [onInitialized](#events) | C++ \| Lua |
| void() | [onDisconnected](#events) | C++ \| Lua |
| void(BillingResponse, std::string) | [onProductsQueried](#events) | C++ \| Lua |
| void(PurchaseDetails) | [onPurchaseUpdated](#events) | C++ \| Lua |
| void(std::string, BillingResponse, std::string) | [onPurchaseFailed](#events) | C++ \| Lua |
| void(ProductType, BillingResponse, std::string) | [onPurchasesQueried](#events) | C++ \| Lua |
| void(std::string, BillingResponse, std::string) | [onPurchaseAcknowledged](#events) | C++ \| Lua |
| void(std::string, BillingResponse, std::string) | [onPurchaseConsumed](#events) | C++ \| Lua |

## Method details

### initialize / isReady {#initialize-isready}

* static void **initialize**()
* static bool **isReady**()

Connects to the store. [`onInitialized(response, message)`](#events) reports `OK` once
it is ready, and every call before that fails with `SERVICE_DISCONNECTED`. Calling
`initialize()` again while connected reports `OK` again.

On Android, `isReady()` is true while connected to Google Play. When the connection
drops, `onDisconnected` fires and the next call connects again by itself. On iOS,
`initialize()` reports `OK` at once and starts listening for App Store transactions,
which delivers the ones left unsettled in earlier launches through `onPurchaseUpdated`.

---

### queryProducts

* static void **queryProducts**(const std::vector\<std::string\>& productIds, [ProductType](#producttype) type)

Fetches the details of these products, which must all be of `type`: their localized
names, descriptions, prices and, for subscriptions, plans and offers.
[`onProductsQueried(response, message)`](#events) reports when they are stored, and
products the store does not know are left out. On iOS so are products of the other
type, and the message names both kinds. An empty list reports `DEVELOPER_ERROR`. In Lua,
pass a table of strings.

=== "C++"

    ```cpp
    InAppPurchase::queryProducts({"coins_100", "remove_ads"}, ProductType::INAPP);
    InAppPurchase::queryProducts({"premium"}, ProductType::SUBS);
    ```

=== "Lua"

    ```lua
    InAppPurchase.queryProducts({ "coins_100", "remove_ads" }, ProductType.INAPP)
    InAppPurchase.queryProducts({ "premium" }, ProductType.SUBS)
    ```

---

### hasProduct / getProduct / getProducts {#hasproduct-getproduct-getproducts}

* static bool **hasProduct**(const std::string& productId)
* static [ProductDetails](#productdetails) **getProduct**(const std::string& productId)
* static std::vector\<[ProductDetails](#productdetails)\> **getProducts**()

The products queried so far. `getProduct()` returns an empty `ProductDetails` for a
product that was not queried, so check `hasProduct()` first.

=== "Lua"

    ```lua
    for _, product in ipairs(InAppPurchase.getProducts()) do
        Log.print(product.name .. " " .. product.price)
    end
    ```

---

### purchase

* static void **purchase**(const std::string& productId, const std::string& offerToken = "")

Opens the store's purchase screen for a [queried](#queryproducts) product. The result
is [`onPurchaseUpdated`](#events) for a completed or pending purchase, or
`onPurchaseFailed(productId, response, message)`, for example with `USER_CANCELED`,
`ITEM_ALREADY_OWNED`, or `ITEM_UNAVAILABLE` for a product that was not queried.

On Google Play, `offerToken` picks a subscription plan from the product's
[`offers`](#productoffer). Left empty, a subscription buys its first base plan (or its
first offer when it has no base plan), and a one-time product its default purchase
option. The App Store ignores it: a product has one plan, and its introductory offer
applies by itself.

On iOS, a device not allowed to make payments reports `BILLING_UNAVAILABLE`, and a
purchase waiting for a parent's approval (Ask to Buy) is reported as `PENDING` with no
`purchaseToken`; once approved, it arrives as a new purchase.

The purchases include the ids set with
[`setObfuscatedAccountId` and `setObfuscatedProfileId`](#setobfuscatedaccountid-setobfuscatedprofileid).

---

### changeSubscription

* static void **changeSubscription**(const std::string& productId, const std::string& offerToken, const std::string& oldPurchaseToken, [SubscriptionReplacementMode](#subscriptionreplacementmode) mode = WITH_TIME_PRORATION)

Replaces an owned subscription with another plan or product, an upgrade or a downgrade.
`oldPurchaseToken` must belong to a purchase in [`getPurchases()`](#getpurchases-ispurchased),
so query `SUBS` purchases first; otherwise `onPurchaseFailed` reports `DEVELOPER_ERROR`.
`mode` decides how the time left on the old plan is billed. `KEEP_EXISTING` keeps the old
plan's payment schedule and ignores `offerToken`.

On iOS it buys `productId` like [`purchase()`](#purchase), and the App Store replaces
the subscription of the same group; `offerToken` and `mode` are ignored.

---

### acknowledgePurchase / consumePurchase {#acknowledgepurchase-consumepurchase}

* static void **acknowledgePurchase**(const std::string& purchaseToken)
* static void **consumePurchase**(const std::string& purchaseToken)

Settle a `PURCHASED` purchase. Google Play refunds one left unsettled for three days,
and the App Store delivers it again at every launch. On iOS, settling finishes the
purchase's transactions.

- **Acknowledge** products bought once and subscriptions.
  `onPurchaseAcknowledged(purchaseToken, response, message)` reports it, and the stored
  purchase's `acknowledged` turns true.
- **Consume** consumables, like coins. Consuming also acknowledges, removes the purchase
  from `getPurchases()`, and lets the player buy the product again.
  `onPurchaseConsumed(purchaseToken, response, message)` reports it.

Grant and save a consumable *before* consuming it, once per `purchaseToken`: the same
purchase can be reported twice, and a consumed one is never reported again. On iOS,
consuming a product that is not a consumable in App Store Connect reports
`DEVELOPER_ERROR`, and consuming one twice reports `ITEM_NOT_OWNED`. Never settle a
`PENDING` purchase.

---

### queryPurchases

* static void **queryPurchases**([ProductType](#producttype) type)

Asks the store for the player's purchases of `type`: active subscriptions, products
bought once, and consumables not consumed yet. Each one is reported through
`onPurchaseUpdated` with [`restored`](#purchasedetails) set, then
`onPurchasesQueried(type, response, message)` fires. With `OK`, the result replaces the
stored purchases of that type, so refunded and expired ones go away.

Call it for each type at startup and on [`Engine::onResume`](engine.md#onresume):
purchases also complete outside the app, through pending payments, promo codes or another
device.

---

### restorePurchases

* static void **restorePurchases**()

For a **Restore Purchases** button: queries the purchases of both types, as two
[`queryPurchases`](#querypurchases) calls do. On iOS it first syncs the player's App
Store account, which may ask them to sign in; a failed sync reports its error through
both `onPurchasesQueried` events. Apple's review guidelines ask apps to offer a way to
restore purchases that can be restored.

---

### getPurchases / isPurchased {#getpurchases-ispurchased}

* static std::vector\<[PurchaseDetails](#purchasedetails)\> **getPurchases**()
* static bool **isPurchased**(const std::string& productId)

The purchases known in this session, from purchase screens and
[`queryPurchases`](#querypurchases), less the consumed ones. `isPurchased()` is true when
one of them includes the product, is `PURCHASED`, and is not `suspended`. It does not
check acknowledgment.

---

### setObfuscatedAccountId / setObfuscatedProfileId {#setobfuscatedaccountid-setobfuscatedprofileid}

* static void **setObfuscatedAccountId**(const std::string& accountId)
* static void **setObfuscatedProfileId**(const std::string& profileId)

A hashed id of the player's account in your game, and of a profile within it, attached to
the next purchases. Google Play uses them against fraud, and they come back in
[`PurchaseDetails`](#purchasedetails) for your server. Never pass plain personal data.

The App Store takes the account id only as a UUID, which it keeps as the transaction's
`appAccountToken`; any other value is left out with a warning. It has no profile id.

---

### openSubscriptionManagement

* static void **openSubscriptionManagement**(const std::string& productId = "")

Opens the store's subscription management, on one subscription or on all of them, where
the player can cancel or fix a payment. On Android it opens Google Play's subscription
center. On iOS it shows Apple's subscription sheet over the game, on the product's
subscription group from iOS 17, and queries the subscriptions again when it closes.

---

### showInAppMessages

* static void **showInAppMessages**()

Lets Google Play show its messages about subscription payment problems, such as a
declined card. When the player fixes the payment, subscription purchases are queried
again, and `onPurchaseUpdated` reports the subscription without `suspended`. It does
nothing on iOS, which shows these messages by itself.

## Events

Each event is a static `FunctionSubscribe` member; subscribe with `REGISTER_EVENT` in C++
or `RegisterEvent` in Lua (see [Events](../../manual/events.md#service-events)). C++
handlers take the parameters by value, exactly as listed.

| Event | Parameters | When |
| --- | --- | --- |
| `onInitialized` | `BillingResponse response, std::string message` | The store connection was set up, or failed |
| `onDisconnected` | — | Android: the store connection was lost; the next call reconnects |
| `onProductsQueried` | `BillingResponse response, std::string message` | Product details arrived; read them with `getProducts()` |
| `onPurchaseUpdated` | `PurchaseDetails purchase` | A purchase is new, changed, or reported by `queryPurchases`. Grant it when `PURCHASED`. On iOS, a refund or an ended subscription also arrives here, with state `UNSPECIFIED` |
| `onPurchaseFailed` | `std::string productId, BillingResponse response, std::string message` | A purchase screen failed or was canceled. `productId` is empty when unknown |
| `onPurchasesQueried` | `ProductType productType, BillingResponse response, std::string message` | `queryPurchases`, or one type of `restorePurchases`, finished after its `onPurchaseUpdated` events |
| `onPurchaseAcknowledged` | `std::string purchaseToken, BillingResponse response, std::string message` | A purchase was acknowledged |
| `onPurchaseConsumed` | `std::string purchaseToken, BillingResponse response, std::string message` | A purchase was consumed and can be bought again |

## Types

These structs are also Lua classes with the same fields. Lists are Lua tables.

### ProductDetails

A product as the store describes it, from [`queryProducts`](#queryproducts).

| Field | Type | Meaning |
| --- | --- | --- |
| `productId` | std::string | The product's id in the Play Console or App Store Connect |
| `type` | [ProductType](#producttype) | `INAPP` or `SUBS` |
| `title` | std::string | Title as Google Play shows it, which may include the app name. On iOS, the display name |
| `name` | std::string | The product's name, for a store screen. On iOS, the display name |
| `description` | std::string | Description |
| `price` | std::string | Formatted price with its currency symbol. For a subscription, the recurring price of the plan `purchase()` buys without an offer token |
| `priceMicros` | long long | The price in millionths of the currency |
| `currencyCode` | std::string | ISO 4217 currency code |
| `offers` | std::vector\<[ProductOffer](#productoffer)\> | Subscription plans and offers, or the purchase options of a one-time product. On iOS, one entry with no token, holding the pricing phases |

---

### ProductOffer

A subscription's base plan or offer, or a one-time product's purchase option.

| Field | Type | Meaning |
| --- | --- | --- |
| `offerToken` | std::string | What [`purchase()`](#purchase) takes to buy this plan or offer |
| `offerId` | std::string | The offer's id; empty for a base plan |
| `basePlanId` | std::string | The base plan's id, or the purchase option's id of a one-time product |
| `tags` | std::vector\<std::string\> | Tags set in the Play Console |
| `pricingPhases` | std::vector\<[PricingPhase](#pricingphase)\> | The phases a buyer goes through, like a free trial and then the regular price |

---

### PricingPhase

| Field | Type | Meaning |
| --- | --- | --- |
| `price` | std::string | Formatted price with its currency symbol |
| `priceMicros` | long long | The price in millionths of the currency |
| `currencyCode` | std::string | ISO 4217 currency code |
| `billingPeriod` | std::string | ISO 8601 period, like `P1M` for a month. Empty for one-time products |
| `billingCycleCount` | int | Cycles a `FINITE_RECURRING` phase lasts |
| `recurrenceMode` | [RecurrenceMode](#recurrencemode) | How the phase repeats |

---

### PurchaseDetails

| Field | Type | Meaning |
| --- | --- | --- |
| `orderId` | std::string | Google Play's order id. On iOS, the transaction id |
| `productId` | std::string | The first product of the purchase |
| `productIds` | std::vector\<std::string\> | Every product of the purchase |
| `productType` | [ProductType](#producttype) | `INAPP` or `SUBS` |
| `purchaseToken` | std::string | Identifies the purchase; what acknowledging, consuming and server checks take. On iOS, the original transaction id, which renewals keep. Empty for a purchase waiting for Ask to Buy |
| `purchaseTime` | long long | When it was bought, in milliseconds since the epoch |
| `state` | [PurchaseState](#purchasestate) | Grant only when `PURCHASED` |
| `quantity` | int | Units bought at once, for products that allow several |
| `acknowledged` | bool | Already acknowledged or consumed. On iOS, its transaction is finished |
| `autoRenewing` | bool | A subscription that renews; false once canceled |
| `suspended` | bool | A subscription on hold for a payment problem. Do not grant it |
| `restored` | bool | Reported by [`queryPurchases`](#querypurchases), not by a purchase screen |
| `packageName` | std::string | The app's package name, or bundle identifier on iOS |
| `obfuscatedAccountId` | std::string | The id set with `setObfuscatedAccountId`. On iOS, the `appAccountToken` UUID, in lower case |
| `obfuscatedProfileId` | std::string | The id set with `setObfuscatedProfileId`. Empty on iOS |
| `originalJson` | std::string | The purchase data Google Play signed, to verify on a server. On iOS, the transaction JSON |
| `signature` | std::string | Its signature. On iOS, the transaction's JWS, which a server verifies with Apple's App Store Server Library or API |

## Enumerations

### ProductType

* **INAPP** — A one-time product, consumable or not. Also an iOS non-renewing subscription, which the store never expires: work out its end from `purchaseTime`.
* **SUBS** — An auto-renewing subscription.

---

### PurchaseState

* **UNSPECIFIED** — Unknown state. On iOS, also a refunded purchase or an ended subscription.
* **PURCHASED** — Paid. Grant it and settle it.
* **PENDING** — Waiting for a payment or an approval made outside the app, like Ask to Buy on iOS. Do not grant it yet.

---

### BillingResponse

Google Play Billing's response codes, with the same values. iOS maps StoreKit's errors
to them.

| Value | Code | Meaning |
| --- | --- | --- |
| `SERVICE_TIMEOUT` | -3 | Google Play took too long to answer |
| `FEATURE_NOT_SUPPORTED` | -2 | The device's Google Play does not support the request |
| `SERVICE_DISCONNECTED` | -1 | Not connected: call `initialize()` first, or try again |
| `OK` | 0 | Success |
| `USER_CANCELED` | 1 | The player closed the purchase screen |
| `SERVICE_UNAVAILABLE` | 2 | Google Play cannot be reached for now, often for lack of network |
| `BILLING_UNAVAILABLE` | 3 | No billing here: another platform, a build without it, or an unsupported Play account |
| `ITEM_UNAVAILABLE` | 4 | The product cannot be bought, or was not queried |
| `DEVELOPER_ERROR` | 5 | Invalid arguments |
| `FATAL_ERROR` | 6 | Google Play's `ERROR`: an internal failure |
| `ITEM_ALREADY_OWNED` | 7 | The player owns it already; query purchases to restore it |
| `ITEM_NOT_OWNED` | 8 | The player does not own it |
| `NETWORK_ERROR` | 12 | A network failure during the operation |

---

### RecurrenceMode

* **INFINITE_RECURRING** — Repeats until the subscription is canceled.
* **FINITE_RECURRING** — Repeats `billingCycleCount` times.
* **NON_RECURRING** — Charged once.

---

### SubscriptionReplacementMode

How [`changeSubscription`](#changesubscription) bills the time left on the old plan.

* **WITH_TIME_PRORATION** — The change applies now, and the time left is credited toward the new plan.
* **CHARGE_PRORATED_PRICE** — The change applies now and the billing date stays; the price difference for the time left is charged. Upgrades only.
* **WITHOUT_PRORATION** — The change applies now, and the new price is charged from the next billing date.
* **CHARGE_FULL_PRICE** — The change applies now, the new plan is charged in full, and the time left is credited.
* **DEFERRED** — The change applies when the old plan renews.
* **KEEP_EXISTING** — The old plan's payment schedule carries over. `offerToken` is ignored.

## See also

- [Monetization](../../manual/monetization.md#in-app-purchases) — setup, testing, and a complete store script
- [AdMob](admob.md) and [WebPortal](webportal.md)
