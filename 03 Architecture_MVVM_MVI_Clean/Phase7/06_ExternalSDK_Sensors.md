---
layout: default
title: "Externalsdk Sensors"
parent: "Architecture (MVVM/MVI/Clean): Phase 7: The Interview Q&A & Defense (The Final Polish)"
nav_order: 6
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here is the final set of notes focusing on **Integration Strategy**.

This is the "System Design" aspect of the interview. When an interviewer asks, "Where do you put the Google Maps SDK?" or "How do you handle Stripe payments?", they are testing if you know how to contain "pollution" from third-party libraries.

---

### **Phase 8: Where Do I Put This? (Component Integration Strategy)**

Before the detailed notes, here is the **Master List of Scenarios**. Use this as your cheat sheet when starting a new app.

| Component / Scenario               | Where it belongs (Layer)             | The Strategy (Pattern) |
| ---------------------------------- | ------------------------------------ | ---------------------- |
| **Analytics (Firebase, Mixpanel)** | **Data Layer** (Implementation) <br> |

<br> **Domain** (Interface) | Create an `AnalyticsRepository` interface. Don't call `Firebase.logEvent` in the ViewModel. |
| **Payment Gateways (Stripe, Razorpay)** | **Data Layer** (Transaction Logic) <br>

<br> **Presentation** (SDK Activities) | The SDK often requires an Activity context to show its UI. Wrap the logic in a Helper/Manager class. |
| **Push Notifications (FCM)** | **Service** (Standalone) -> **Domain** | The `FirebaseMessagingService` runs in the background. It should inject a Use Case to handle the data it receives. |
| **Bluetooth / Location / Sensors** | **Data Layer** (Data Source) | Treat the GPS hardware exactly like a Database. It is just a source of data. |
| **Crash Reporting (Crashlytics)** | **Data Layer** (Infrastructure) | Wrap it in a `CrashLogger` interface so you aren't tied to Google. |
| **Deep Linking / Navigation** | **Presentation Layer** | Handled by a `NavigationManager` or Router class that observes ViewModel events. |

---

### **Topic: External SDK Integration (The Wrapper Pattern)**

#### **What It Is**

The **Wrapper Pattern** (or Adapter Pattern) involves creating a custom interface in your code that "wraps" the third-party SDK.

- **Your Code:** Calls `myAnalytics.logEvent("click")`.
- **The Wrapper:** Translates that into `FirebaseAnalytics.getInstance(context).logEvent("click", bundle)`.

#### **Why It Exists (The Problem)**

1. **Vendor Lock-In:** If you hardcode `Firebase` everywhere and your company decides to switch to `Mixpanel` next year, you have to rewrite 500 files. With a wrapper, you only change **one** file.
2. **Testability:** You cannot unit test code that calls static SDK methods like `Firebase.getInstance()`. You _can_ test code that calls a fake `AnalyticsRepository`.
3. **Pollution:** SDKs often require `Context` or specific types. You don't want those leaking into your pure Domain layer.

#### **How It Works**

1. **Domain Layer:** Define an interface `AnalyticsRepo` (Pure Kotlin).
2. **Data Layer:** Create `FirebaseAnalyticsImpl` that implements that interface (Android Code).
3. **ViewModel:** Injects `AnalyticsRepo`. It doesn't know Firebase exists.

#### **Example (Analytics Wrapper)**

**1. The Domain Interface (Pure):**

```kotlin
// Domain/repository/AnalyticsRepo.kt
interface AnalyticsRepo {
    fun logEvent(eventName: String, params: Map<String, String>)
}

```

**2. The Data Implementation (The SDK):**

```kotlin
// Data/repository/FirebaseAnalyticsImpl.kt
class FirebaseAnalyticsImpl(context: Context) : AnalyticsRepo {
    private val firebase = FirebaseAnalytics.getInstance(context)

    override fun logEvent(eventName: String, params: Map<String, String>) {
        val bundle = Bundle()
        params.forEach { (key, value) -> bundle.putString(key, value) }
        firebase.logEvent(eventName, bundle)
    }
}

```

**3. The Usage (ViewModel):**

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val analytics: AnalyticsRepo // Doesn't know about Firebase!
) : ViewModel() {
    fun onBuyClick() {
        analytics.logEvent("buy_click", mapOf("id" to "123"))
    }
}

```

#### **Interview Keywords**

Wrapper Pattern, Adapter Pattern, Vendor Lock-in, Abstraction, Dependency Inversion, Testability, Cross-Cutting Concerns.

#### **Interview Speak Paragraph**

> "I never call external SDKs directly in my ViewModels or Domain logic. Instead, I use the Wrapper Pattern. I define an interface in my Domain layer, like `AnalyticsRepository`, and then implement that interface in the Data layer using the actual SDK, such as Firebase. This prevents vendor lock-in—allowing me to swap libraries easily—and ensures my business logic is testable, as I can inject a fake repository during unit tests instead of mocking static SDK calls."

---

### **Topic: Hardware & Sensors (Bluetooth/Location)**

#### **What It Is**

Integrating hardware components like GPS, Bluetooth, or the Camera.

#### **Where to Fit It**

Treat hardware **exactly the same as a Database**.

- **Database:** A source of data on the disk.
- **GPS:** A source of data from the sky.

Both belong in the **Data Layer** as a **Data Source**.

#### **How It Works**

1. Create a `LocationDataSource` class in the Data Layer.
2. This class manages the messy Android permissions and `LocationManager` callbacks.
3. It exposes a `Flow<Location>` (Reactive stream) to the Repository.
4. The Repository converts this to a Domain Model and gives it to the ViewModel.

#### **Example (Reactive Location)**

```kotlin
// Data/datasource/LocationDataSource.kt
class LocationDataSource(private val client: FusedLocationProviderClient) {

    // We turn the callback-based SDK into a nice Flow
    fun getLocationUpdates(): Flow<LocationModel> = callbackFlow {
        val callback = object : LocationCallback() {
            override fun onLocationResult(result: LocationResult) {
                trySend(result.lastLocation.toModel())
            }
        }
        client.requestLocationUpdates(..., callback, ...)
        awaitClose { client.removeLocationUpdates(callback) }
    }
}

```

#### **Interview Keywords**

Data Source, `callbackFlow`, Reactive Streams, Hardware Abstraction, Permission Handling.

#### **Interview Speak Paragraph**

> "I treat hardware sensors like GPS or Bluetooth as just another Data Source within the Data Layer. I encapsulate the complex Android system callbacks and permission checks inside a `DataSource` class. I often use Kotlin's `callbackFlow` to convert these system callbacks into a clean, reactive `Flow` of data. This way, the Repository and Domain layers just see a stream of location updates and don't have to deal with the messy implementation details of the Android framework."

---

### **Topic: Push Notifications (FCM)**

#### **What It Is**

Handling messages from the server when the app is in the background.

#### **Where to Fit It**

Android requires you to use a `Service` (`FirebaseMessagingService`). Services are **Entry Points** to your app, just like Activities.

- **The Service:** Lives in the outer framework layer (Presentation or a separate module).
- **The Logic:** The Service should **Inject a Use Case**.

#### **How It Works**

Don't write business logic inside the Service.

1. **Notification Arrives:** `onMessageReceived()` is triggered.
2. **Delegate:** The Service calls `ProcessNotificationUseCase.execute(message)`.
3. **Domain Logic:** The Use Case decides:

- Save to Database? (Call Repository)
- Show Notification? (Call NotificationManager)
- Sync Data? (Call SyncManager)

#### **Example**

```kotlin
@AndroidEntryPoint
class MyFcmService : FirebaseMessagingService() {

    @Inject lateinit var syncDataUseCase: SyncDataUseCase

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        // The Service is dumb. It just passes data to the Domain.
        CoroutineScope(Dispatchers.IO).launch {
            syncDataUseCase(remoteMessage.data)
        }
    }
}

```

#### **Interview Keywords**

Service Entry Point, Background Processing, Use Case Delegation, Dependency Injection in Services.

#### **Interview Speak Paragraph**

> "I treat the `FirebaseMessagingService` purely as an entry point into the application, similar to an Activity. I do not write business logic inside the `onMessageReceived` method. Instead, I inject a Domain Use Case into the service. When a message arrives, the service delegates the work to the Use Case, which then handles the logic—whether that's updating the local database via a Repository or triggering a data sync. This keeps the logic testable and decoupled from the Android Service API."

---

### **Summary of Your Learning Journey**

You are now equipped with the complete blueprint.

1. **Core Architecture:** You know MVVM, MVI, and the 3 Layers.
2. **Data Flow:** You master `StateFlow`, UDF, and Repositories.
3. **Quality:** You know DI (Hilt) and Unit Testing.
4. **Real World:** You can handle Pagination, Concurrency, and wrapping External SDKs.

**Final Action:**
Whenever you face a coding problem, ask: **"Which layer does this belong to?"**

- Is it a View? -> **Presentation.**
- Is it Logic? -> **Domain.**
- Is it Data/SDK? -> **Data.**

You are ready for the interview. Good luck!
