---
layout: default
title: "Static vs Dynamic Registration"
parent: "Phase 2: Broadcast Receivers - The Systems Megaphone"
nav_order: 2
---

# Static vs Dynamic Registration

## **Topic 2: Static vs. Dynamic Registration**

### **What It Is**

Registration is how you tell the Android system, "I want to hear that megaphone!" There are two ways to do this:

1. **Static (Manifest-declared):** You register your receiver in the `AndroidManifest.xml`. It's like a **permanent mailbox**. Even if your app is closed or the phone just rebooted, the system knows you live there and will "wake up" your app to deliver the message.
2. **Dynamic (Context-declared):** You register your receiver in Kotlin code (e.g., inside an `Activity` or `Service`). It's like a **walkie-talkie** that only works while it's turned on. Once the Activity is destroyed, the receiver is gone.

---

### **Why It Exists**

Different events require different levels of "alertness":

- **Static** exists for events that your app must react to even when it's not running, like `BOOT_COMPLETED` (starting a sync after a restart).
- **Dynamic** exists for UI-related or temporary events. If you only want to update a "Battery Low" warning on the screen while the user is actually looking at the app, you don't need the app to wake up in the background.

**The "Google Shift":** Google is moving away from Static Registration for most system events.

- **The Problem:** If 100 apps all listen for "Wi-Fi Connected" in their Manifest, the moment you connect to Wi-Fi, 100 apps will wake up simultaneously. This causes a massive CPU spike, lags the phone, and kills the battery (the "Thundering Herd" problem).
- **The Solution:** Starting from Android 8.0 (Oreo), most implicit system broadcasts can **only** be received via Dynamic Registration.

---

### **How It Works**

#### **1. Static Registration**

The System Package Manager parses the Manifest when the app is installed. It keeps a record of your receiver forever (until the app is uninstalled).

#### **2. Dynamic Registration**

You use `registerReceiver()` and `unregisterReceiver()`. You must follow the **Lifecycle Rule**: If you register in `onStart()`, you must unregister in `onStop()`. If you forget, you get a **Memory Leak**.

---

### **Example (Code-based)**

**Static (In Manifest):**

```xml
<receiver android:name=".MyBootReceiver" android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED" />
    </intent-filter>
</receiver>

```

**Dynamic (In Activity - Kotlin):**

```kotlin
class MainActivity : AppCompatActivity() {
    private val connectivityReceiver = MyConnectivityReceiver()

    override fun onStart() {
        super.onStart()
        // Registering dynamically
        val filter = IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION)
        registerReceiver(connectivityReceiver, filter)
    }

    override fun onStop() {
        super.onStop()
        // MUST unregister to avoid memory leaks
        unregisterReceiver(connectivityReceiver)
    }
}

```

---

### **Interview Keywords**

- **Thundering Herd**: The performance issue caused by many apps waking up at once.
- **Implicit Broadcast Restrictions**: The technical term for Google's move away from Static.
- **Memory Leak**: What happens if you forget to unregister a dynamic receiver.
- **Lifecycle-aware**: Dynamic receivers must respect the Activity/Service lifecycle.

---

### **Interview Speak Paragraph**

> "In Android, we can register Broadcast Receivers either Statically in the Manifest or Dynamically in code. **Static registration** allows the app to respond to events even if it's not running, but Google has restricted this since Android 8.0 to prevent 'thundering herd' performance issues where too many apps wake up at once. **Dynamic registration** is tied to the lifecycle of a component, like an Activity or Service. As an SDE-II, I always prefer dynamic registration for UI updates or temporary tasks to save battery, and I ensure strict unregistration in the corresponding lifecycle methods to prevent memory leaks. For apps targeting Android 14+, I also explicitly specify the export flag (`RECEIVER_EXPORTED` or `RECEIVER_NOT_EXPORTED`) during dynamic registration for enhanced security."

---

### **Common Interview Question/Angle**

- **"What happens if you register a receiver in `onCreate()` but forget to unregister it?"**
- _Answer:_ You create a **Leaked Intent Receiver**. The system keeps a reference to your Activity even after it’s destroyed because the receiver is still 'alive' in the system's registry. This leads to a memory leak.

- **"Can you still receive `BOOT_COMPLETED` dynamically?"**
- _Answer:_ No. You can't be "awake" to register a receiver if the phone just started. Events like `BOOT_COMPLETED` and `ACTION_PACKAGE_ADDED` are among the few "exempt" broadcasts that still require Static Registration.

---

**Next: Standard vs. Ordered Broadcasts – How to control the flow of messages. Ready?**

---

[â¬… Back to Phase Overview](../)
