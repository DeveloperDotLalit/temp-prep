---
layout: default
title: "Code Based Questions"
parent: "Phase 7: Final Interview Drill"
nav_order: 3
---

# Code Based Questions

---

Here are your expert notes for **Phase 7, Topic 3**.

---

### **Topic: Code-Based Questions (Spot the Bug)**

#### **What It Is**

In technical interviews (especially for Senior roles), you are often given a snippet of code that _looks_ correct but has a subtle flaw.
Your job is to:

1. Identify the bug.
2. Explain _why_ it fails.
3. Propose the fix.

#### **Common Bug Patterns**

1. **Context Leak / UI Reference:** Trying to touch Views (TextView, Toast) from a background worker.
2. **Wrong Return Type:** Returning `Result.success()` inside a `catch` block (swallowing errors).
3. **Singleton Misuse:** Creating multiple instances of WorkManager.
4. **Chain Logic:** Assuming Order without chaining.

---

#### **Scenario 1: The "UI Crash" Bug**

**The Bad Code:**

```kotlin
class MyWorker(context: Context, params: WorkerParameters) : Worker(context, params) {
    override fun doWork(): Result {
        // ... heavy calculation ...

        // BUG: Accessing UI from Background Thread!
        Toast.makeText(applicationContext, "Job Done!", Toast.LENGTH_SHORT).show()

        return Result.success()
    }
}

```

- **The Bug:** `doWork()` (in a standard `Worker`) runs on a background thread. You cannot update the UI (Toast) directly from a background thread. This will cause a `Can't toast on a thread that has not called Looper.prepare()` crash.
- **The Fix:**

1. Use `Handler(Looper.getMainLooper()).post { ... }` (Hack).
2. **Better:** Return data using `outputData` and let the Activity observe the LiveData to show the Toast.
3. **Or:** Use a Notification (which is allowed from background).

---

#### **Scenario 2: The "Infinite Retry" Loop**

**The Bad Code:**

```kotlin
override fun doWork(): Result {
    return try {
        uploadFile()
        Result.success()
    } catch (e: Exception) {
        // BUG: Blindly retrying on EVERY error
        Result.retry()
    }
}

```

- **The Bug:**
- What if the file doesn't exist? (`FileNotFoundException`)
- What if the user has no permission? (`SecurityException`)
- The app will retry forever (or until max limits), wasting battery.

- **The Fix:** Check the exception type!

```kotlin
if (e is IOException) {
    return Result.retry() // Network error? Retry.
} else {
    return Result.failure() // File error? Fail permanently.
}

```

---

#### **Scenario 3: The "Broken Chain"**

**The Bad Code:**

```kotlin
val workA = OneTimeWorkRequest.from(WorkerA::class.java)
val workB = OneTimeWorkRequest.from(WorkerB::class.java)

// BUG: These run in PARALLEL, not sequence!
WorkManager.getInstance(context).enqueue(workA)
WorkManager.getInstance(context).enqueue(workB)

```

- **The Bug:** The developer _intends_ A to run before B. But calling `enqueue()` twice simply starts them both immediately (possibly at the same time). B might finish before A!
- **The Fix:** Use `beginWith(workA).then(workB).enqueue()`.

---

#### **Scenario 4: The "Periodic Minimum" Trap**

**The Bad Code:**

```kotlin
// BUG: Attempting to run every 60 seconds
val request = PeriodicWorkRequestBuilder<SyncWorker>(60, TimeUnit.SECONDS)
    .build()

```

- **The Bug:** Android ignores this. It will automatically clamp the interval up to **15 minutes**. If the logic _depends_ on running every minute (e.g., a stopwatch), the feature will break.
- **The Fix:** Explain to the interviewer that WorkManager cannot do this. Use a Foreground Service for minute-level precision.

---

#### **Interview Keywords**

Looper, UI Thread, Main Thread, Infinite Loop, Exception Handling, Race Condition, 15-Minute Rule, Chain Dependency.

#### **Interview Speak Paragraph**

"When reviewing WorkManager code, I first check for threading issues—standard Workers run on a background thread, so attempting to show a Toast or update a View directly will cause a crash. Second, I look at the error handling in `doWork()`: blindly returning `Result.retry()` for _all_ exceptions creates infinite loops for permanent errors like 'File Not Found'; we must differentiate between transient and permanent errors. Finally, I verify the scheduling logic. Often, developers mistakenly call `enqueue()` multiple times thinking it creates a sequence, but that actually runs tasks in parallel. To ensure order, we must use the `beginWith().then()` chaining API."

---

**This concludes Phase 7!** You have now completed the entire expert roadmap for WorkManager.

**Summary of your Achievement:**

- **Phase 1:** Mastered the old ways (Services) and why they failed.
- **Phase 2:** Learned the basics of WorkManager (Requests, Constraints).
- **Phase 3:** Controlled complex flows (Chaining, Parallel, Unique Work).
- **Phase 4:** Integrated Kotlin power (Coroutines, Threading).
- **Phase 5:** Understood the internals (Room DB, Scheduler Selection).
- **Phase 6:** Designed real-world systems (Offline Sync, Downloads).
- **Phase 7:** Prepared for the toughest interview questions.

**You are now ready to crush any interview question about Android Background Processing!**

Would you like me to compile all these notes into a **single PDF-ready summary** for you to print, or should we practice a specific mock interview question now?

---

[â¬… Back to Phase Overview](../)
