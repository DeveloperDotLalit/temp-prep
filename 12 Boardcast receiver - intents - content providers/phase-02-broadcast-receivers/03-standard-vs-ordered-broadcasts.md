---
layout: default
title: "Standard vs Ordered Broadcasts"
parent: "Phase 2: Broadcast Receivers - The Systems Megaphone"
nav_order: 3
---

# Standard vs Ordered Broadcasts

## **Topic 3: Standard vs. Ordered Broadcasts**

### **What It Is**

When the "megaphone" (the System) shouts a message, there are two ways the listeners can hear it:

1. **Standard Broadcast (Normal):** It’s like a public announcement in a stadium. Everyone hears it at the exact same time. There is no order, and no one can stop the message from reaching others.
2. **Ordered Broadcast:** It’s like a **game of telephone** or a **chain of command**. The message is delivered to one receiver at a time, based on a specific "priority." Each person in the chain can read the message, change the message, or simply "abort" it so the next person never hears it.

---

### **Why It Exists**

- **Standard Broadcasts** are for efficiency. Most system events (like "Battery Low") don't need an order. The system just wants everyone to know as fast as possible.
- **Ordered Broadcasts** are for **coordination**.
- _The Problem:_ Imagine two apps want to handle an SMS. If they both handle it simultaneously, you might get two notifications.
- _The Solution:_ With an Ordered Broadcast, the app with the "Highest Priority" gets the message first. It can process the SMS and then tell the system, "I'm done, don't show this to anyone else."

---

### **How It Works**

1. **Priority:** You set a priority (an integer) in your Intent Filter. Higher numbers go first.
2. **Sequential Delivery:** The Android System sorts all matching receivers by priority.
3. **Result Data:** Each receiver can pass data to the _next_ receiver in the chain using `setResultData()`.
4. **Aborting:** A receiver can call `abortBroadcast()` to kill the message.

---

### **Example (Practical Scenario)**

Imagine you have a **Security App**. You want to intercept an incoming SMS if it contains a "Remote Wipe" command, so the default Messaging app never sees it.

1. **Your Security App:** Priority 100.
2. **Default SMS App:** Priority 1.

When the SMS arrives:

- **Security App** hears it first. It checks the text. If it’s a wipe command, it calls `abortBroadcast()`.
- **Default SMS App** never receives the Intent, and the user never sees a notification.

**Kotlin Code for sending an Ordered Broadcast:**

```kotlin
val intent = Intent("com.example.MY_ORDERED_SIGNAL")
// Nulls are for optional: resultReceiver, scheduler, initialCode, initialData, initialExtras
sendOrderedBroadcast(intent, null)

```

**In Manifest (Setting Priority):**

```xml
<receiver android:name=".HighPriorityReceiver">
    <intent-filter android:priority="100">
        <action android:name="com.example.MY_ORDERED_SIGNAL" />
    </intent-filter>
</receiver>

```

---

### **Interview Keywords**

- **Asynchronous vs. Synchronous**: Standard is async (parallel), Ordered is sync (one-by-one).
- **Priority Attribute**: The `android:priority` tag in the Manifest.
- **abortBroadcast()**: The specific method used to stop the chain.
- **setResultData()**: Passing information down the line.

---

### **Interview Speak Paragraph**

> "In Android, **Standard Broadcasts** are sent asynchronously, meaning all receivers catch the intent at roughly the same time in an undefined order. They are very efficient but cannot be cancelled. Conversely, **Ordered Broadcasts** are delivered synchronously based on a defined priority. This allows each receiver to process the intent, potentially modify the result data, or even terminate the broadcast using `abortBroadcast()` to prevent lower-priority receivers from seeing it. This is particularly useful for system-level events where one app needs to intercept or validate an action before it reaches the rest of the system."

---

### **Common Interview Question/Angle**

- **"Can a Standard Broadcast be aborted?"**
- _Answer:_ No. Because they are sent to everyone simultaneously, there is no 'chain' to break. `abortBroadcast()` will throw an exception if called in a normal broadcast.

- **"What happens if two receivers have the same priority in an Ordered Broadcast?"**
- _Answer:_ If the priorities are equal, the order of delivery is undefined (it's up to the system's internal logic).

- **"Where do you define the priority?"**
- _Answer:_ You define it in the `intent-filter` within the `AndroidManifest.xml` or when creating an `IntentFilter` object for dynamic registration.

---

**Next up: LocalBroadcastManager vs. Flow/Bus – Why the old way is dead and what we use now in modern Kotlin apps. Ready?**

---

[â¬… Back to Phase Overview](../)
