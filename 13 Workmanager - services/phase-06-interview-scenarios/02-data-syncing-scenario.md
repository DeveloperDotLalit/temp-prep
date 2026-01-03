---
layout: default
title: "Data Syncing Scenario"
parent: "Phase 6: Real World Interview Scenarios"
nav_order: 2
---

# Data Syncing Scenario

---

Here are your expert notes for **Phase 6, Topic 2**.

---

### **Topic: System Design Scenario – Offline-First Sync Engine**

#### **The Problem**

**Interviewer:** "Design a chat app (like WhatsApp) or an email client. The user enters a tunnel (no internet) and sends a message. Later, they regain connectivity. How do you ensure the message is sent without the user having to press 'retry'?"

**Naive Solution:** Just use `Retrofit` in a `ViewModel`.

- _Fail:_ If the network is down, the call fails immediately. The data is lost unless the user stays on that screen.

#### **The Solution: The "Offline-First" Repository Pattern**

In an offline-first app, the **Database (Room)** is the Single Source of Truth for the UI. The UI **never** talks to the Network directly.

1. **UI:** Displays data from Room.
2. **User Action:** Saves data to Room (marked as "unsynced").
3. **WorkManager:** Watches for "unsynced" data and pushes it to the Server.
4. **Sync:** When the Server responds, WorkManager updates Room.

#### **Architecture Flow**

1. **User Clicks Send:**

- Save Message to **Room** with status `is_synced = false`.
- UI updates _immediately_ (Optimistic UI) showing a "clock" icon.

2. **Trigger Sync:**

- Enqueue a `OneTimeWorkRequest` (Unique Work: `KEEP`).
- Constraint: `NetworkType.CONNECTED`.

3. **The Worker:**

- Query Room: "Give me all messages where `is_synced = false`."
- Loop through them and POST to Server.
- **Success:** Update Room item -> `is_synced = true`. UI updates to "check" icon.
- **Failure:** Do nothing (Room still says `false`). Return `Result.retry()`.

#### **Key Technical Decisions**

1. **Unique Work (`KEEP`):**

- We use `enqueueUniqueWork("SEND_MSG", KEEP, request)`.
- _Why?_ If the user sends 5 messages rapidly, we don't need 5 workers. One worker is enough to wake up, read the database, and sync _all_ pending messages in a batch.

2. **Conflict Resolution (The Hard Part):**

- _Scenario:_ User edits a note offline. Server also updates that note.
- _Strategy:_ usually **"Server Wins"** or **"Last Write Wins"** (based on timestamps).

3. **Periodic Fetching:**

- We also need a `PeriodicWorkRequest` (every 15 mins) to _pull_ new messages from the server into Room.

#### **Example Code: The Sync Worker**

```kotlin
class ChatSyncWorker(ctx: Context, params: WorkerParameters) : CoroutineWorker(ctx, params) {

    override suspend fun doWork(): Result {
        val database = MyDatabase.getInstance(applicationContext)
        val api = ApiClient.create()

        return try {
            // 1. READ Pending Messages
            val pendingMessages = database.chatDao().getUnsyncedMessages()

            if (pendingMessages.isEmpty()) return Result.success()

            // 2. PUSH to Server
            for (msg in pendingMessages) {
                val response = api.sendMessage(msg)

                if (response.isSuccessful) {
                    // 3. UPDATE Local DB (Mark as Sent)
                    msg.isSynced = true
                    msg.serverTimestamp = response.body().timestamp
                    database.chatDao().update(msg)
                } else {
                    // Server error? Retry later.
                    return Result.retry()
                }
            }
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}

```

#### **Interview Keywords**

Offline-First, Single Source of Truth, Optimistic UI, Synchronization, Conflict Resolution, Batching, Repository Pattern, Room + WorkManager.

#### **Interview Speak Paragraph**

"For a chat app, I would implement an **Offline-First Architecture**. The UI observes the local Room database, which acts as the single source of truth. When a user sends a message, I immediately save it to Room with a 'pending' status so the UI updates instantly. I then enqueue a unique WorkManager task with a network constraint. This worker queries the database for all pending messages and batches them to the server. On success, it updates the local database status to 'sent.' If the network is unavailable, WorkManager holds the task and retries automatically when connectivity returns, ensuring no messages are lost."

---

**Would you like to move to the next scenario: "Scenario: Downloading Large Files – Handling long-running downloads without being killed"?**

---

[â¬… Back to Phase Overview](../)
