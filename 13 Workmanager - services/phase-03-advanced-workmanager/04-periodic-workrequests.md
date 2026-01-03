---
layout: default
title: "Periodic WorkRequests"
parent: "Phase 3: Advanced WorkManager - Complex Control"
nav_order: 4
---

# Periodic WorkRequests

---

Here are your expert notes for **Phase 3, Topic 4**.

---

### **Topic: Periodic WorkRequests**

#### **What It Is**

A `PeriodicWorkRequest` is a task that runs repeatedly over and over again after a set amount of time.
You set it up once, and it runs indefinitely until you cancel it (or the user uninstalls the app).

Think of it as a **Scheduled Maintenance Crew**.

- "Come clean the office every 24 hours."
- "Backup the database every 6 hours."

#### **Why It Exists**

Apps often need to perform routine checks without user interaction.

- Checking for new emails.
- Uploading analytics logs.
- Deleting old temporary files.

However, Android introduced a strict rule to protect battery life:
**The Minimum Interval is 15 Minutes.**
You **cannot** schedule a Periodic WorkRequest to run every 1 minute or 5 minutes. If you try to set it to 10 minutes, WorkManager will silently upgrade it to 15 minutes automatically.

#### **How It Works**

1. **The Interval:** You define the repeat cycle (e.g., 1 hour).
2. **Inexact Timing:** Periodic Work is **not** an alarm clock. If you set it for 1 hour, it might run at 60 minutes, or 65 minutes, or 70 minutes. Android groups ("batches") your task with other apps' tasks to wake up the radio once and save battery.
3. **Flex Interval (Advanced):** You can define a specific "window" at the end of the interval where the task can run.

- _Example:_ "Repeat every 1 hour, but run specifically in the last 15 minutes of that hour."

**Text-Based Diagram: The 15-Minute Rule**

```text
Attempt:  [ 5 min ] [ 5 min ] [ 5 min ] ...
Result:   [ --------- 15 min ---------] [ --------- 15 min ---------] ...
           (System forces this minimum spacing)

```

#### **Example Code: The "Daily Sync"**

**1. Simple Periodic Request (Every 24 Hours)**

```kotlin
val dailySyncRequest = PeriodicWorkRequestBuilder<SyncWorker>(
        24, TimeUnit.HOURS // Repeat Interval
    )
    .setConstraints(Constraints.Builder().setRequiresCharging(true).build())
    .build()

WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "DAILY_SYNC_TAG",
    ExistingPeriodicWorkPolicy.KEEP, // If already scheduled, don't add another one
    dailySyncRequest
)

```

**2. The Flex Interval (Advanced)**

```kotlin
// Run every 1 hour, but only execute in the last 15 mins of that hour
val smartRequest = PeriodicWorkRequestBuilder<SyncWorker>(
        1, TimeUnit.HOURS,             // Repeat Interval
        15, TimeUnit.MINUTES           // Flex Interval (runs here)
    )
    .build()

```

#### **Interview Keywords**

PeriodicWorkRequest, 15-Minute Minimum, Flex Interval, Battery Optimization, Batching, Inexact Timing.

#### **Interview Speak Paragraph**

"I use `PeriodicWorkRequest` for routine tasks like log uploads or data syncing. The most important constraint to remember is the **15-minute minimum interval** enforced by Android to conserve battery; we cannot schedule periodic work more frequently than that. Also, these tasks are **inexact**—they won't run at the precise millisecond but are batched by the system to run efficiently. If I need a task to run within a specific window at the end of a cycle, I can use the **Flex Interval** feature. For anything needing precise timing (like an alarm), I would switch to `AlarmManager`, but for general background maintenance, PeriodicWork is the standard."

---

**Would you like to move to the next topic: "Observing Work Status (LiveData/Flow)" (Updating the UI)?**

---

[â¬… Back to Phase Overview](../)
