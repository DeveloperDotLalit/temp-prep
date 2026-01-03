---
layout: default
title: "Cheatsheet Workmanager - Services"
parent: "WorkManager and Services in Android"
nav_order: 8
---

# Cheatsheet Workmanager - Services

Here is your **Ultimate WorkManager Cheat Sheet & Mind Map**. This summarizes the entire masterclass into a single, printable reference guide for your interview preparation.

---

### **1. The Master Mind Map**

```text
ANDROID BACKGROUND PROCESSING
│
├── 1. THE FOUNDATION (Why we are here)
│   ├── Main Thread (UI) vs. Background Thread (Worker)
│   ├── The "Sin": Blocking UI (ANR - Application Not Responding)
│   ├── Service: A component with no UI (Runs on Main Thread by default!)
│   └── The "Killers": Doze Mode & App Standby (Why old Services failed)
│
├── 2. WORKMANAGER BASICS (The Solution)
│   ├── Purpose: Deferrable + Guaranteed Execution
│   ├── Components: Worker (Code) + Request (Rules) + Manager (Scheduler)
│   ├── Constraints: Requires Charging, WiFi, Device Idle
│   └── Data: Input/Output Data (Max 10KB limit)
│
├── 3. ADVANCED CONTROL
│   ├── Chaining: .beginWith(A).then(B) (Sequential)
│   ├── Parallel: .beginWith(listOf(A, B)).then(C) (Fan-Out/Fan-In)
│   ├── Unique Work: .enqueueUniqueWork() (Handle duplicates)
│   │   ├── KEEP: Ignore new if running
│   │   ├── REPLACE: Cancel old, start new
│   │   └── APPEND: Run after current finishes
│   └── Periodic: Min 15 Minutes interval (Battery optimization)
│
├── 4. KOTLIN POWER
│   ├── CoroutineWorker: suspend doWork() (The standard for Kotlin)
│   ├── Threading: Defaults to Dispatchers.Default (CPU)
│   │   └── Use withContext(Dispatchers.IO) for Network/DB
│   └── Long-Running: setForeground() (Promote to Notification)
│
├── 5. UNDER THE HOOD
│   ├── Architecture: Uses local Room DB to persist requests (Survives Reboot)
│   ├── Scheduler:
│   │   ├── API 23+: JobScheduler (Native)
│   │   └── API <23: AlarmManager + BroadcastReceiver
│   └── Backoff Policy: Exponential vs Linear (For retries)
│
└── 6. SYSTEM DESIGN SCENARIOS
    ├── Offline Sync: Room (Truth) + WorkManager (Sync Agent)
    ├── Large Download: Foreground Service + HTTP Range Headers (Resumable)
    └── Location:
        ├── Real-time (Run): Foreground Service
        └── Periodic (Weather): WorkManager

```

---

### **2. Quick-Reference Cheat Sheet**

#### **Phase 1: The Old World (Services)**

- **Main Thread:** Handles UI updates (16ms per frame). Blocking it causes ANRs.
- **Service:** Runs on **Main Thread**. NOT a separate thread.
- **Started Service:** Fire-and-forget.
- **Bound Service:** Client-server (communicates with Activity).
- **Foreground Service:** Has a persistent Notification. Immune to low-memory kills.
- **Doze Mode:** System creates "maintenance windows" to save battery, killing standard background services.

#### **Phase 2: WorkManager Basics**

- **Definition:** Library for **deferrable, guaranteed** background work.
- **Decision Tree:**
- Exact Time? -> `AlarmManager`
- User Interaction? -> `Coroutines`
- Immediate/Long? -> `Foreground Service`
- Deferrable/Guaranteed? -> `WorkManager`

- **Input/Output:** Use `Data` object (Key-Value pairs). Max **10KB**.

#### **Phase 3: Advanced Features**

- **Chaining:** Pass Output of A as Input to B automatically. Fails gracefully (if A fails, B is cancelled).
- **Parallel:** Use `InputMerger` (like `ArrayCreatingInputMerger`) to combine results from multiple parallel workers.
- **Unique Work Policies:**
- `KEEP`: Good for "Sync" buttons (don't spam server).
- `REPLACE`: Good for Search/Autocomplete.
- `APPEND`: Good for Upload Queues.

#### **Phase 4: Kotlin & Threading**

- **CoroutineWorker:** The correct choice for Kotlin. Allows `suspend` functions.
- **Cancellation:** If constraints fail (e.g., WiFi drops), the `CoroutineScope` is cancelled. Handle `try-catch` or `finally` to clean up.
- **Expedited Work:** `setExpedited(true)` for high-priority tasks (replaces deprecated GCM/FirebaseDispatcher).

#### **Phase 5: Internals (The "Why it works")**

- **Persistence:** Requests are serialized into a **Room Database**. This is why tasks survive app kills and reboots.
- **Boot Receiver:** WorkManager listens for `BOOT_COMPLETED` to re-load pending tasks from the DB.
- **JobScheduler:** The underlying API used on 95% of devices (API 23+).

#### **Phase 6: Key Design Patterns**

- **Offline-First:** UI talks to Room. WorkManager talks to Server. WorkManager updates Room.
- **Resumable Downloads:** Check file size on disk -> Request `bytes=X-` -> Append to file.
- **Location:** Use `FusedLocationProviderClient`. Background permission requires a specific flow (While in Use -> All the time).

#### **Phase 7: Interview Defense**

- **Force Stop:** Kills everything. Task will NOT run until user manually opens the app.
- **Swipe Away:** Task still runs (handled by System JobScheduler).
- **IntentService:** Deprecated. No persistence. No constraints. Don't use it.
- **Retry:** Always use `Result.retry()` with **Exponential Backoff** for network errors.

---

### **Final Interview Tip**

When asked **"How do you handle X?"**, do not jump straight to code.

1. **Define the constraints:** "Does it need to survive a reboot? Is it immediate?"
2. **Select the tool:** "Based on that, I'd use WorkManager..."
3. **Explain the architecture:** "...configured with a CoroutineWorker and a 'Connected' constraint..."
4. **Mention the edge case:** "...and I'd handle the 'Force Stop' scenario by managing user expectations."

You are now fully equipped. Good luck with your preparation!
