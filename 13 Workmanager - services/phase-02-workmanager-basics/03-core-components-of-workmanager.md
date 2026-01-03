---
layout: default
title: "Core Components of WorkManager"
parent: "Phase 2: Modern Standard - WorkManager Basics"
nav_order: 3
---

# Core Components of WorkManager

---

Here are your expert notes for **Phase 2, Topic 3**.

---

### **Topic: Core Components of WorkManager**

#### **What It Is**

To use WorkManager, you need to understand its three main pillars. Think of this like a **Package Delivery Service**:

1. **The Worker (The "What"):** This is the actual package content. It contains the code you want to run (e.g., "Compress this image").
2. **The WorkRequest (The "How & When"):** This is the shipping label. It defines the rules: "Deliver this only when the recipient is home" (Constraints) or "Deliver this every day" (Periodic).
3. **The WorkManager (The "Who"):** This is the Delivery Company Manager. You hand the package (Worker) with the label (WorkRequest) to him, and he ensures it gets done.

#### **Why It Exists**

Separating these components allows for flexibility.

- You can write one `UploadWorker` (logic) but use it in two different ways: once as a `OneTimeWorkRequest` (upload now) and once as a `PeriodicWorkRequest` (upload every night).
- The `WorkManager` singleton handles the messy scheduling parts so your code stays clean.

#### **How It Works (Step-by-Step)**

**1. The Worker**

- You create a class that extends `Worker` (or `CoroutineWorker` for Kotlin).
- You override the `doWork()` method.
- **Crucial Rule:** You must return a `Result` at the end:
- `Result.success()`: Task finished successfully.
- `Result.failure()`: Task failed permanently (don't try again).
- `Result.retry()`: Task failed (e.g., no server connection), please try again later.

**2. The WorkRequest**

- You wrap your Worker in a Request.
- **Two Types:**
- `OneTimeWorkRequest`: Run this once.
- `PeriodicWorkRequest`: Run this repeatedly (minimum interval is 15 minutes).

- This is where you add **Constraints** (discussed in the next topic).

**3. The WorkManager**

- You get the instance of `WorkManager` and call `.enqueue()`.
- It takes your request, saves it to the database, and schedules it.

#### **Example Code (Putting it all together)**

**Step 1: Define the Worker (The Logic)**

```kotlin
class UploadWorker(context: Context, params: WorkerParameters) : Worker(context, params) {

    override fun doWork(): Result {
        return try {
            // Do the heavy lifting here (Synchronously)
            uploadFiles()

            // Tell WorkManager it's done
            Result.success()
        } catch (e: Exception) {
            // Tell WorkManager to try again later (Backoff policy)
            Result.retry()
        }
    }

    private fun uploadFiles() {
        // Fake upload logic
        Thread.sleep(3000)
    }
}

```

**Step 2 & 3: Create Request & Enqueue (The Scheduling)**

```kotlin
// In your Activity or ViewModel

fun startUpload() {
    // 1. Create the Request (The "Label")
    val uploadRequest = OneTimeWorkRequestBuilder<UploadWorker>()
        .build()

    // 2. Hand it to the Manager
    WorkManager.getInstance(context).enqueue(uploadRequest)
}

```

#### **Interview Keywords**

doWork(), Result.success, Result.retry, OneTimeWorkRequest, PeriodicWorkRequest, Enqueue, Singleton.

#### **Interview Speak Paragraph**

"WorkManager is built on three core components: the **Worker**, the **WorkRequest**, and the **WorkManager** singleton itself. The **Worker** contains the actual business logic we want to execute in the background; we extend the class and override `doWork()`, returning a specific `Result` like success, failure, or retry. The **WorkRequest** wraps this worker and defines _how_ it should run—whether it's a one-time task or periodic, and what constraints (like WiFi) apply. Finally, we pass this request to the **WorkManager**, which enqueues the task, persists it to the database, and ensures execution."

---

**Would you like to move to the next topic: "Constraints" (How to restrict execution to WiFi/Charging)?**

---

[â¬… Back to Phase Overview](../)
