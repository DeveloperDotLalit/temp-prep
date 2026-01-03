---
layout: default
title: "Location Tracking Scenario"
parent: "Phase 6: Real World Interview Scenarios"
nav_order: 4
---

# Location Tracking Scenario

---

Here are your expert notes for **Phase 6, Topic 4**.

---

### **Topic: System Design Scenario – Location Tracking**

#### **The Problem**

**Interviewer:** "Design a feature for (A) a Running Tracker app like Strava, or (B) a Weather app that updates your local temperature."

**Why this is tricky:**

- **Battery Drain:** GPS chips consume a lot of power.
- **Privacy:** Android has become extremely strict about apps knowing where you are when you aren't looking at the screen.
- **The "One Size Fits All" Trap:** You cannot use the same tool for Strava (Real-time) and Weather (Periodic).

#### **The Solution: Two Different Paths**

You must clarify the requirements immediately.

**Path A: Real-Time Tracking (e.g., Uber, Google Maps, Strava)**

- **Requirement:** High accuracy, updates every few seconds.
- **Tool:** **Foreground Service**.
- **Why?** You need the GPS chip to stay awake constantly. WorkManager cannot run every 5 seconds (min is 15 mins). A standard background service will be killed. You _need_ a persistent notification.

**Path B: Periodic Tracking (e.g., Weather App, "Find my parked car")**

- **Requirement:** Low/Medium accuracy, updates every 1-4 hours.
- **Tool:** **WorkManager**.
- **Why?** You don't need to drain the battery constantly. You just need to wake up, grab one location point, and go back to sleep.

#### **Key Technical Challenges**

1. **Permissions (The Interview Minefield):**

- **Android 10 (API 29)+:** You must request `ACCESS_BACKGROUND_LOCATION` if you want location even when the app is minimized.
- **The Flow:** First request "While Using App". _Then_ request "All the Time" (Background). You cannot request Background instantly.
- **Android 14+:** You must declare `<service android:foregroundServiceType="location" ... />` in the Manifest.

2. **FusedLocationProviderClient:**

- Never say "I'll use the GPS class."
- Always say "I'll use **FusedLocationProviderClient**." It intelligently switches between GPS, WiFi, and Cell Towers to save battery.

#### **Example Code: Real-Time Tracking (Foreground Service)**

```kotlin
// The Manifest
// <uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />

class LocationService : Service() {
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    override fun onCreate() {
        super.onCreate()
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // 1. Start Foreground IMMEDIATELY
        startForeground(1, createNotification())

        // 2. Request High Accuracy Updates
        val request = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 5000) // 5 seconds
            .build()

        // 3. Start Listening (Permission check required here)
        fusedLocationClient.requestLocationUpdates(request, locationCallback, Looper.getMainLooper())

        return START_STICKY
    }

    private val locationCallback = object : LocationCallback() {
        override fun onLocationResult(result: LocationResult) {
            val location = result.lastLocation
            // Save to DB or upload to server
        }
    }
}

```

#### **Example Code: Periodic Tracking (WorkManager)**

```kotlin
class WeatherLocWorker(ctx: Context, params: WorkerParameters) : CoroutineWorker(ctx, params) {

    override suspend fun doWork(): Result {
        val fusedClient = LocationServices.getFusedLocationProviderClient(applicationContext)

        return try {
            // 1. Get Single Update (Current Location)
            // Use "PRIORITY_BALANCED_POWER_ACCURACY" (Cell/WiFi) to save battery
            val location = fusedClient.getCurrentLocation(
                Priority.PRIORITY_BALANCED_POWER_ACCURACY,
                CancellationTokenSource().token
            ).await()

            if (location != null) {
                updateWeather(location.latitude, location.longitude)
                Result.success()
            } else {
                Result.retry()
            }
        } catch (e: Exception) {
            Result.failure()
        }
    }
}

```

#### **Interview Keywords**

Foreground Service vs WorkManager, `FusedLocationProviderClient`, `ACCESS_BACKGROUND_LOCATION`, `foregroundServiceType="location"`, Battery Drain, High Accuracy vs Balanced Power.

#### **Interview Speak Paragraph**

"The approach to background location depends entirely on the frequency required. For a running app requiring real-time updates every few seconds, I use a **Foreground Service** with `FusedLocationProviderClient` set to `HIGH_ACCURACY`. This ensures the process isn't killed and the GPS stays active, while the mandatory notification keeps the user informed. For a weather app that only needs an update every few hours, I use **WorkManager** with `PeriodicWorkRequest`. In this case, I use `BALANCED_POWER_ACCURACY` to rely on WiFi/Cell towers rather than GPS to conserve battery. In both cases, handling the `ACCESS_BACKGROUND_LOCATION` permission correctly for Android 10+ is critical."

---

**This concludes Phase 6!** You now have the system design skills to tackle complex real-world problems.

**Ready to start Phase 7: The Final Drill – Interview Q&A?**
(We will cover rapid-fire conceptual questions, tricky scenarios, and code bug spotting.)

---

[â¬… Back to Phase Overview](../)
