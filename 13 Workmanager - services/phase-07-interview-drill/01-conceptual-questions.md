---
layout: default
title: "Conceptual Questions"
parent: "Phase 7: Final Interview Drill"
nav_order: 1
---

# Conceptual Questions

---

Here are your expert notes for **Phase 7, Topic 1**.

---

### **Topic: IntentService (Deprecated) vs. WorkManager**

#### **What It Is**

This is a classic "History Lesson" question. Even though `IntentService` is deprecated, interviewers ask this to see if you understand **how Android has evolved**.

- **IntentService (The Old Guard):** It was a helper class that created a background thread, processed a queue of requests (Intents) one by one, and then stopped itself automatically. It was simple but fragile.
- **WorkManager (The New Standard):** It is a robust library that guarantees execution even if the app or device restarts. It respects system health (battery/data) using constraints.

#### **Why It Exists (The Evolution)**

`IntentService` was great in 2012. But as Android evolved:

1. **Reliability:** If you force-closed the app while `IntentService` was running, the task was **lost forever**.
2. **Battery:** `IntentService` tried to run _immediately_. If 10 apps did this at once, the phone overheated.
3. **Deprecation:** Starting with Android 8 (Oreo), background services were banned from running freely. `IntentService` became unusable for many tasks, leading to its deprecation in Android 11.

**WorkManager replaced it** to solve the "Guaranteed Execution" problem and to comply with modern battery saving rules (Doze Mode).

#### **How It Works (The Comparison)**

| Feature         | IntentService (Deprecated)                               | WorkManager (Modern)                                    |
| --------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| **Execution**   | Runs **Immediately** (Fire-and-forget).                  | Runs when **Constraints are met** (Deferrable).         |
| **Persistence** | **None.** If the app crashes/restarts, the task is gone. | **High.** Saves request to a Room DB. Survives reboots. |
| **Thread**      | Creates a single worker thread (HandlerThread).          | Uses `Executor` (Java) or `Coroutines` (Kotlin).        |
| **Constraints** | None. (Runs even if battery is low).                     | Yes. (Can wait for WiFi/Charging).                      |
| **Status**      | Deprecated (API 30+).                                    | Recommended.                                            |

#### **Example: The "Upload" Scenario**

- **Using IntentService (Old Way):**
- You start the service.
- The phone reboots 2 seconds later.
- **Result:** Upload failed. The app has no idea it failed. The user thinks it worked.

- **Using WorkManager (New Way):**
- You enqueue the work.
- WorkManager saves "Upload Task" to its database.
- The phone reboots.
- **Result:** Phone turns on. WorkManager sees the pending task in the DB. It restarts the upload automatically.

#### **Interview Keywords**

Deprecated, HandlerThread, Fire-and-Forget, Guaranteed Execution, Persistence, Background Limits, Immediate vs. Deferrable.

#### **Interview Speak Paragraph**

"`IntentService` was the traditional way to handle background tasks sequentially on a worker thread, but it had no persistence—if the app crashed or the device rebooted, the task was lost. It also struggled with modern Android background restrictions introduced in Oreo. `WorkManager` replaces it by offering **guaranteed execution**. Unlike IntentService, WorkManager persists the task to a local database, ensuring it survives system kills and reboots. It also respects system constraints like battery and network availability, making it the correct choice for deferrable, reliable work, whereas IntentService is now deprecated."

---

**Would you like to move to the next topic: "Tricky Scenario Questions" ("What happens if I force stop the app?")?**

---

[â¬… Back to Phase Overview](../)
