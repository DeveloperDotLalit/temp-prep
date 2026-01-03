---
layout: default
title: "Parallel Execution"
parent: "Phase 3: Advanced WorkManager - Complex Control"
nav_order: 2
---

# Parallel Execution

---

Here are your expert notes for **Phase 3, Topic 2**.

---

### **Topic: Parallel Execution (Fan-Out / Fan-In)**

#### **What It Is**

Parallel Execution allows you to run multiple independent tasks **simultaneously** (at the same time) and then wait for **all** of them to finish before starting the next step.

In Computer Science, this is often called the **"Fan-Out / Fan-In"** pattern.

- **Fan-Out:** Start 3 tasks at once (A, B, C).
- **Fan-In:** Wait for A, B, AND C to finish, then run Task D.

#### **Why It Exists**

**Speed and Efficiency.**
Imagine you need to download 3 separate images to create a collage.

- **Sequential (Chaining):** Download 1 (5s) -> Download 2 (5s) -> Download 3 (5s) -> Create Collage. **Total Time: 15s.**
- **Parallel:** Download 1, 2, and 3 all at once. Since they run together, the total time is roughly equal to the slowest download (approx 5s) -> Create Collage. **Total Time: ~5s.**

If tasks don't depend on each other, always run them in parallel.

#### **How It Works**

1. **The List:** Instead of passing a single request to `beginWith()` or `.then()`, you pass a **List** of requests.
2. **The Barrier:** WorkManager creates an invisible "barrier." The next task in the chain will **not start** until **every single task** in the parallel list has reported `Result.success()`.
3. **The Data Problem:** If Task A returns `{"id": 1}` and Task B returns `{"id": 2}`, what does Task D receive?

- _Default Behavior:_ Keys overwrite each other. Task D sees only `{"id": 2}` (or whichever finished last).
- _The Fix:_ Use an **`InputMerger`**.

#### **Example Code: The "Collage Maker"**

**Scenario:** We download 3 images in parallel. Once _all_ are done, we run the `CollageWorker`.

```kotlin
// 1. Create Independent Requests
val downloadImg1 = OneTimeWorkRequestBuilder<DownloadWorker>()
    .setInputData(workDataOf("URL" to "url_1"))
    .build()

val downloadImg2 = OneTimeWorkRequestBuilder<DownloadWorker>()
    .setInputData(workDataOf("URL" to "url_2"))
    .build()

val downloadImg3 = OneTimeWorkRequestBuilder<DownloadWorker>()
    .setInputData(workDataOf("URL" to "url_3"))
    .build()

// 2. Create the Final Request
val createCollage = OneTimeWorkRequestBuilder<CollageWorker>()
    .setInputMerger(ArrayCreatingInputMerger::class.java) // <--- CRITICAL PRO TIP
    .build()

// 3. Execute in Parallel
WorkManager.getInstance(context)
    .beginWith(listOf(downloadImg1, downloadImg2, downloadImg3)) // Pass a List!
    .then(createCollage) // Runs only when ALL 3 are done
    .enqueue()

```

#### **Pro Tip: InputMergers (For Interviews)**

If you are passing data from parallel tasks to the final task, you must mention **`ArrayCreatingInputMerger`**.

- **Without it:** If all 3 workers return a key "IMAGE_PATH", the final worker only gets the _last_ one.
- **With it:** The final worker gets an **Array** of values: `["path1", "path2", "path3"]`.

#### **Interview Keywords**

Parallel Execution, Fan-Out Fan-In, `beginWith(List)`, `ArrayCreatingInputMerger`, Synchronization Barrier, Multi-threading.

#### **Interview Speak Paragraph**

"WorkManager supports parallel execution, allowing us to run multiple independent tasks simultaneously to save time. We achieve this by passing a **list** of WorkRequests to `beginWith()` or `.then()`. WorkManager handles the synchronization, ensuring that the subsequent task in the chain only starts once **all** parallel tasks have successfully completed. A common challenge here is data conflicts—if multiple parallel workers return output with the same key, they overwrite each other. To solve this, we define an `ArrayCreatingInputMerger` on the final request, which merges the outputs into an array so the final worker receives all the results."

---

**Would you like to move to the next topic: "Unique Work Policies" (Handling duplicates like double-clicks)?**

---

[â¬… Back to Phase Overview](../)
