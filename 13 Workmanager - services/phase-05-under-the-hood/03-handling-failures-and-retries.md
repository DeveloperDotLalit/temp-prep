---
layout: default
title: "Handling Failures and Retries"
parent: "Phase 5: Under the Hood - How WorkManager Works"
nav_order: 3
---

# Handling Failures and Retries

---

Here are your expert notes for **Phase 5, Topic 3**.

---

### **Topic: Handling Failures & Retries (Backoff Policy)**

#### **What It Is**

When a background task runs, things often go wrong. The server might be down, the internet might flicker, or a file might be locked.

- **Failure (`Result.failure()`):** "I failed, and I cannot be fixed. Stop." (e.g., File not found).
- **Retry (`Result.retry()`):** "I failed, but it might work later. Please try again." (e.g., Server timeout).

When you return `Result.retry()`, WorkManager doesn't restart the task immediately. Instead, it uses a **Backoff Policy** to decide _how long to wait_ before the next attempt.

#### **Why It Exists**

To prevent **"Server Hammering."**
Imagine 10,000 users' apps all fail to connect to your server at 12:00 PM because of a glitch.

- **Without Backoff:** All 10,000 apps retry instantly at 12:00:01. The server crashes again. They retry at 12:00:02. The server explodes.
- **With Backoff:**
- User A waits 10 seconds.
- User B waits 20 seconds.
- User C waits 40 seconds.
- The server gets breathing room to recover.

#### **How It Works (Linear vs. Exponential)**

You configure the "Backoff Criteria" when building the `WorkRequest`.

1. **Linear Backoff:** The wait time increases by the _same amount_ each time.

- _Formula:_ `Wait Time = Initial Time * Attempt Number`
- _Example (Initial = 10s):_
- Attempt 1: Wait 10s
- Attempt 2: Wait 20s (10+10)
- Attempt 3: Wait 30s (20+10)

- _Use Case:_ Predictable, short delays.

2. **Exponential Backoff (Recommended):** The wait time _doubles_ each time.

- _Formula:_ `Wait Time = Initial Time * 2^(Attempt Number - 1)`
- _Example (Initial = 10s):_
- Attempt 1: Wait 10s
- Attempt 2: Wait 20s
- Attempt 3: Wait 40s
- Attempt 4: Wait 80s

- _Use Case:_ Network/Server issues. This grows very fast, giving the server maximum time to heal.

#### **Example Code: The "Polite" Uploader**

```kotlin
// In your Worker
override fun doWork(): Result {
    return try {
        uploadFile()
        Result.success()
    } catch (e: Exception) {
        // "I failed, but please try again later!"
        Result.retry()
    }
}

// In your Activity/Repository
val uploadRequest = OneTimeWorkRequestBuilder<UploadWorker>()
    .setBackoffCriteria(
        BackoffPolicy.EXPONENTIAL, // The Strategy (Linear or Exponential)
        10,                        // The Initial Delay
        TimeUnit.SECONDS           // The Unit
    )
    .build()

// Result:
// Retry 1: runs after 10s
// Retry 2: runs after 20s
// Retry 3: runs after 40s

```

#### **Important Limits (Interview Trivia)**

- **Minimum Backoff:** 10 Seconds (You can't set it to 1 second).
- **Maximum Backoff:** WorkManager caps the wait time (usually around 5 hours) so a task doesn't get pushed to next year.

#### **Interview Keywords**

`Result.retry()`, Backoff Policy, Linear, Exponential, Transient Error, Idempotency (Safe to retry), Server Hammering.

#### **Interview Speak Paragraph**

"When a task fails due to a transient issue like network loss, I return `Result.retry()` from the worker. This triggers WorkManager's **Backoff Policy**. I typically configure this as `BackoffPolicy.EXPONENTIAL` rather than `LINEAR`. This ensures that if the server is struggling, we don't hammer it with requests. The wait time doubles with each failure—10 seconds, then 20, then 40—giving the backend time to recover. It's a crucial mechanism for building resilient and 'polite' mobile applications."

---

**This concludes Phase 5!** You now understand the deep internals of WorkManager.

**Ready to start Phase 6: Real-World Interview Scenarios (System Design)?**
(First topic: "Scenario: Image Uploading – Designing a robust photo uploader.")

---

[â¬… Back to Phase Overview](../)
