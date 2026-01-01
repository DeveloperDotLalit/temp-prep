---
layout: default
title: Configuration Change Vs Process Death
parent: ViewModel Internals: Phase 4   State Saving & Process Death
nav_order: 1
grand_parent: ViewModel Internals
---

Here are your detailed notes for the first topic of Phase 4.

This is arguably the **most misunderstood** concept in Android interviews. Mastering this distinction sets you apart from junior developers.

---

### **Topic: Configuration Change vs. Process Death**

#### **What It Is**

Both terms describe scenarios where your Activity is destroyed and recreated, but the **severity** of data loss is completely different.

1. **Configuration Change:** A "Soft Restart." The user does something (rotates screen, changes language), and the system restarts the UI to load new resources. The app remains running in memory.
2. **Process Death (System-Initiated):** A "Hard Kill." The user puts the app in the background (e.g., switches to Instagram). Later, the Android System realizes it is running low on RAM and silently **kills your app's entire process**.

#### **Why It Exists (The Problem)**

- **Configuration Change** exists to ensure your UI looks correct (e.g., applying the landscape layout).
- **Process Death** exists to manage limited phone resources. Android prioritizes the _foreground_ app. If the foreground app needs more RAM, Android will murder background apps to free up space.

#### **How It Works (The Comparison)**

The critical difference lies in **what survives**.

| Feature                | Configuration Change (Rotation) | Process Death (Low Memory)                    |
| ---------------------- | ------------------------------- | --------------------------------------------- |
| **Trigger**            | User rotates screen / Dark Mode | System needs RAM / App in background too long |
| **ViewModel**          | **SURVIVES** (Stays in Memory)  | **DIES** (Wiped from Memory)                  |
| **Static Variables**   | **SURVIVE**                     | **DIE** (Wiped from Memory)                   |
| **SavedInstanceState** | Survives (Bundle)               | Survives (Bundle)                             |
| **Restoration**        | Immediate                       | When user re-opens the app                    |

**Visualizing the Impact:**

```text
SCENARIO A: ROTATION (Config Change)       SCENARIO B: PROCESS DEATH
+-----------------------+                  +-----------------------+
|  ViewModel (Memory)   |                  |  ViewModel (Memory)   |
|   var score = 100     |                  |   var score = 100     |
+-----------------------+                  +-----------------------+
           |                                           |
    (Screen Rotates)                           (App goes to Background)
           |                                           |
           v                                 (System Low on Memory)
+-----------------------+                              |
|  ViewModel (Memory)   | <--- ALIVE                   v
|   var score = 100     |                  [ PROCESS KILLED ]  <--- DEAD
+-----------------------+                  (Everything in RAM is gone)
                                                       |
                                            (User returns to App)
                                                       |
                                                       v
                                           +-----------------------+
                                           |  New ViewModel Created|
                                           |   var score = 0       | <--- DATA LOST!
                                           +-----------------------+

```

#### **The "Silent Killer" Trap**

Developers often fail to catch bugs related to Process Death because they only test on high-end phones where memory is plentiful.

- You rotate the phone: "Hey, my ViewModel kept the data! It works!"
- **The Bug:** A user on a budget phone switches apps, comes back, and the form is empty because the ViewModel died, and you didn't save the state to disk or a Bundle.

#### **Example: The "Booking Ticket" Scenario**

1. **Rotation:** You select "Seat 14A". You rotate the phone. The ViewModel survives. "Seat 14A" is still selected.
2. **Process Death:** You select "Seat 14A". You get a phone call (app goes background). You talk for 20 minutes. Android kills your app to save battery/RAM.
3. **Return:** You hang up and return to the app.

- The Activity restarts.
- The ViewModel is created **fresh**.
- "Seat 14A" is **lost** (reset to null).
- _Fix:_ This is why we need `SavedStateHandle` (Next topic).

#### **Interview Keywords**

System-Initiated Process Death, Low Memory Killer (LMK), Persistence, Bundle limits, Transient State, ViewModel Survival Scope.

#### **Interview Speak Paragraph**

> "The critical distinction is that during a Configuration Change, the application process remains alive, and the `ViewModel` is retained in memory, preserving all current state. However, during System-Initiated Process Death, the Android OS kills the entire application process to free up resources. In this scenario, the `ViewModel` and all singleton or static variables are destroyed. The only thing that survives Process Death is the `savedInstanceState` Bundle. Therefore, relying solely on a ViewModel for state is insufficient; we must also use `SavedStateHandle` to bridge the gap across process death."

---

**Next Step:**
Now that we know ViewModels _die_ during process death, how do we fix it?
Shall we move to **SavedStateHandle**: The internal mechanism that allows ViewModels to survive system-initiated process death?
