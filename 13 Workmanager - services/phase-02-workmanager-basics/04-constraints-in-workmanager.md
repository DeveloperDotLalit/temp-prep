---
layout: default
title: "Constraints in WorkManager"
parent: "Phase 2: Modern Standard - WorkManager Basics"
nav_order: 4
---

# Constraints in WorkManager

---

Here are your expert notes for **Phase 2, Topic 4**.

---

### **Topic: Constraints in WorkManager**

#### **What It Is**

**Constraints** are a set of rules or conditions that you attach to a `WorkRequest`.
They tell WorkManager: **"Do NOT run this task unless these specific conditions are met."**

If you don't set any constraints, the task tries to run immediately.
If you do set constraints (e.g., "Must be charging"), the task sits in the queue and waits until the user plugs in the charger.

#### **Why It Exists**

We use constraints to be "good citizens" of the Android ecosystem.

1. **Save User's Data:** You shouldn't upload a 500MB video over the user's expensive 5G/LTE data. You should wait for WiFi.
2. **Save Battery:** Heavy processing (like video compression) drains the battery fast. You should wait until the device is plugged in.
3. **Performance:** Some tasks should only run when the user isn't using the phone (Device Idle) to avoid slowing down the UI.

#### **How It Works**

1. **Builder Pattern:** You use a `Constraints.Builder()` to define your rules.
2. **Attach:** You pass these constraints to your `WorkRequest`.
3. **Monitoring:** WorkManager (via the OS) monitors the device state.
4. **Stop Signal:**

- **Crucial Interview Point:** If a constraint is met, the task starts. **BUT**, if the constraint is suddenly _unmet_ while the task is running (e.g., user pulls the plug or WiFi drops), WorkManager sends a `stop()` signal to your Worker immediately.
- Your Worker gets a chance to save its progress, and it is re-queued to try again later.

#### **Common Constraint Options**

- `setRequiredNetworkType(NetworkType.UNMETERED)`: Requires WiFi (or free data).
- `setRequiresCharging(true)`: Must be plugged in.
- `setRequiresBatteryNotLow(true)`: Battery must be above ~15%.
- `setRequiresDeviceIdle(true)`: The user is not using the phone (screen off/stationary).
- `setRequiresStorageNotLow(true)`: Must have enough disk space.

#### **Example Code**

```kotlin
// 1. Define the Constraints
val myConstraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.UNMETERED) // Only WiFi
    .setRequiresCharging(true)                     // Only when plugged in
    .setRequiresBatteryNotLow(true)                // Don't run if battery is red
    .build()

// 2. Attach to the Request
val syncRequest = OneTimeWorkRequestBuilder<SyncWorker>()
    .setConstraints(myConstraints) // <--- HERE
    .build()

// 3. Enqueue
WorkManager.getInstance(context).enqueue(syncRequest)

```

#### **Interview Keywords**

Constraints, NetworkType.UNMETERED, DeviceIdle, BatteryNotLow, Stop Signal, Pre-conditions.

#### **Interview Speak Paragraph**

"Constraints allow us to define the optimal conditions for a background task to run, ensuring we don't drain the user's battery or data plan. For example, for a large file upload, I would set a constraint requiring `NetworkType.UNMETERED` and `RequiresCharging`. A critical detail is that these constraints are monitored _during_ execution too. If the WiFi drops or the user unplugs the device while the worker is running, WorkManager will stop the worker and re-queue it to run again when conditions are met, ensuring robustness."

---

**Would you like to move to the next topic: "Input and Output Data" (Passing arguments to your Worker)?**

---

[â¬… Back to Phase Overview](../)
