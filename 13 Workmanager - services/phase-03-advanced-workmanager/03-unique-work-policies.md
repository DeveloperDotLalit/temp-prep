---
layout: default
title: "Unique Work Policies"
parent: "Phase 3: Advanced WorkManager - Complex Control"
nav_order: 3
---

# Unique Work Policies

---

Here are your expert notes for **Phase 3, Topic 3**.

---

### **Topic: Unique Work Policies (Handling Duplicates)**

#### **What It Is**

**Unique Work** is a feature that allows you to assign a unique **Name (String ID)** to a task or a chain of tasks.
Crucially, it lets you define a **Policy** (Rule) for what happens if you try to schedule a task with the _same name_ while the previous one is still running.

Think of it like a **Single File Line** at a club.

- You name the line "VIP_ENTRY".
- If a new person arrives, the bouncer (WorkManager) checks the policy: "Do I let them in? Do I kick out the current person? Or do I make them wait?"

#### **Why It Exists**

To prevent **duplicate work** and **race conditions**.

- **Scenario:** A user frantically clicks the "Sync Now" button 10 times in 1 second.
- **Without Unique Work:** WorkManager schedules **10 separate sync tasks**. Your server gets hit 10 times. The user's data might get corrupted.
- **With Unique Work:** You name the task "SYNC_DATA". WorkManager sees the first one is running and ignores the other 9 clicks (if you choose `KEEP`).

#### **How It Works (The 4 Policies)**

You use `enqueueUniqueWork()` (for one-time) or `enqueueUniquePeriodicWork()` instead of the standard `enqueue()`.

1. **`ExistingWorkPolicy.KEEP` (The "Ignore New" Rule)**

- **Logic:** If a task with this name is already running (or pending), **ignore the new request completely.**
- **Use Case:** "Sync Now" button. If a sync is already happening, clicking the button again should do nothing.
- _Analogy:_ A bus is already at the stop. You don't call a second bus; you just get on the existing one.

2. **`ExistingWorkPolicy.REPLACE` (The "Restart" Rule)**

- **Logic:** Cancel the current running task immediately (stop it) and start the **new one** from scratch.
- **Use Case:** "Search Autocomplete" or "Photo Filter Preview". If the user types "Hello", we start searching. If they type "Hello World", we cancel the "Hello" search and start the "Hello World" search.
- _Analogy:_ You ordered a coffee. You change your mind and shout "Wait, make it a latte!". The barista throws away the first cup and starts the new one.

3. **`ExistingWorkPolicy.APPEND` (The "Queue" Rule)**

- **Logic:** Let the current task finish. Then run the new task **after** it.
- **Use Case:** "Upload Queue". The user selects Photo A (starts uploading). Then selects Photo B. Photo B waits for A to finish, then starts.
- **Critical Note:** If Task A _fails_, Task B is also cancelled (Chain dependency).

4. **`ExistingWorkPolicy.APPEND_OR_REPLACE`**

- **Logic:** Same as APPEND, but if Task A _failed_ or was cancelled, Task B still runs (creates a new chain).

#### **Example Code: The "Sync Button" Protection**

```kotlin
fun onSyncButtonClicked() {
    val syncRequest = OneTimeWorkRequestBuilder<SyncWorker>().build()

    // PROTECT against button spamming!
    WorkManager.getInstance(context).enqueueUniqueWork(
        "MY_UNIQUE_SYNC_NAME",       // 1. The ID
        ExistingWorkPolicy.KEEP,     // 2. The Policy (Ignore if running)
        syncRequest                  // 3. The Work
    )
}

```

#### **Interview Keywords**

`enqueueUniqueWork`, `ExistingWorkPolicy`, KEEP, REPLACE, APPEND, Idempotency, Race Conditions, Duplicate Requests.

#### **Interview Speak Paragraph**

"To handle duplicate requests—like a user spamming a 'Sync' button—I use `enqueueUniqueWork`. This forces me to assign a unique name to the task and choose a conflict strategy. For a sync operation, I typically use `ExistingWorkPolicy.KEEP`, which simply ignores new requests if one is already running, preventing unnecessary server load. For something like a search query where the latest input matters most, I'd use `REPLACE` to cancel the old task and start the new one. If I need to build a queue, like uploading multiple files sequentially, I use `APPEND` to chain them together."

---

**Would you like to move to the next topic: "Periodic WorkRequests" (Running tasks daily/weekly)?**

---

[â¬… Back to Phase Overview](../)
