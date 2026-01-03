---
layout: default
title: "Chaining Work Requests"
parent: "Phase 3: Advanced WorkManager - Complex Control"
nav_order: 1
---

# Chaining Work Requests

---

Here are your expert notes for **Phase 3, Topic 1**.

---

### **Topic: Chaining Work Requests (Sequential Execution)**

#### **What It Is**

Chaining is the ability to link multiple WorkRequests together so they run in a specific **order**.
Instead of just saying "Run Task A", you can say:
**"Run Task A. When it finishes successfully, run Task B. Then run Task C."**

It creates a dependency chain: `A -> B -> C`.

#### **Why It Exists**

Real-world tasks often have **prerequisites**. You cannot perform step 2 before step 1 is finished.

- **Example:** You cannot _Compress_ an image before you have _Downloaded_ it.
- **Example:** You cannot _Sync Data_ before you have _Logged In_.

Without chaining, you would have to write messy code inside the `onSuccess` callback of Task A to manually start Task B. WorkManager handles this orchestration natively and cleanly.

#### **How It Works**

1. **Sequence:** You use the `beginWith()` and `.then()` methods.
2. **Data Passing:** The **Output Data** of the first worker automatically becomes the **Input Data** of the next worker.

- Worker A returns `["image_path": "/sdcard/img.jpg"]`.
- Worker B receives `["image_path": "/sdcard/img.jpg"]` as input.

3. **Failure Logic:** The chain is **strict**.

- If Task A **fails**, Task B and Task C are **CANCELLED** automatically. They will not run.

**Text-Based Diagram: The Chain**

```text
[ Worker A: Download ]
       | (Success + Output Data)
       v
[ Worker B: Compress ]
       | (Success + Output Data)
       v
[ Worker C: Upload ]

```

#### **Example Code: The "Image Pipeline"**

**Scenario:**

1. `DownloadWorker`: Downloads a file.
2. `FilterWorker`: Applies a sepia filter.
3. `UploadWorker`: Uploads the result to the server.

```kotlin
// 1. Create the Requests
val downloadReq = OneTimeWorkRequestBuilder<DownloadWorker>().build()
val filterReq = OneTimeWorkRequestBuilder<FilterWorker>().build()
val uploadReq = OneTimeWorkRequestBuilder<UploadWorker>().build()

// 2. Build the Chain
WorkManager.getInstance(context)
    .beginWith(downloadReq) // Start here
    .then(filterReq)        // Wait for download, then filter
    .then(uploadReq)        // Wait for filter, then upload
    .enqueue()              // GO!

```

**Advanced Note (InputMergers):**
If you run two tasks in parallel and _then_ merge them into one (A and B -> C), you might need an `InputMerger` to handle data collisions. But for simple linear chains (A -> B -> C), the default `OverwritingInputMerger` works fine.

#### **Interview Keywords**

Chaining, Sequential Execution, `beginWith`, `.then()`, Dependency Graph, InputMerger, Data Pipelining.

#### **Interview Speak Paragraph**

"WorkManager allows us to orchestrate complex task flows using **Chaining**. We can define a sequence of dependencies where Task B only starts after Task A completes successfully. This is done using `beginWith()` followed by `.then()`. A key feature of chaining is that the output data from one worker is automatically passed as input to the next, creating a data pipeline. Additionally, the chain handles failure gracefully: if any worker in the sequence fails, all subsequent dependent workers are automatically blocked or cancelled, ensuring we don't perform operations on invalid data."

---

**Would you like to move to the next topic: "Parallel Execution" (Running multiple tasks at once)?**

---

[â¬… Back to Phase Overview](../)
