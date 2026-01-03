---
layout: default
title: "Input and Output Data"
parent: "Phase 2: Modern Standard - WorkManager Basics"
nav_order: 5
---

# Input and Output Data

---

Here are your expert notes for **Phase 2, Topic 5**.

---

### **Topic: Input and Output Data**

#### **What It Is**

When you start a background task, you often need to send it information.

- **Input:** "Hey Worker, upload _this specific file_ (ID: 123)."
- **Output:** "Hey App, I finished. The server response code was _200 OK_."

In WorkManager, we don't pass objects directly. Instead, we use a lightweight container called the **`Data`** object. It acts like a `HashMap` or `Bundle` containing simple **Key-Value pairs** (Strings, Integers, Booleans, Arrays).

#### **Why It Exists**

You cannot pass complex objects (like a `Context` or a custom `User` class) into a Worker's constructor because **WorkManager creates the Worker instance for you** via reflection when the app wakes up in the background.

Therefore, the data passed must be:

1. **Serializable:** Simple types that can be saved to the database.
2. **Small:** WorkManager imposes a strict **10KB limit** on data payloads. It is designed for arguments (IDs, URIs, Flags), not for bulky data (like the actual image bytes).

#### **How It Works**

1. **Sending Input:** You create a `Data` object and attach it to the `WorkRequest` using `.setInputData()`.
2. **Reading Input:** Inside the Worker's `doWork()`, you read it using `inputData.getString(...)`.
3. **Returning Output:** When finished, you create a new `Data` object and pass it into `Result.success(outputData)`.
4. **Reading Output:** The Activity/ViewModel observes the WorkInfo to get the final result.

#### **Example Code: The "Image Blur" Worker**

**1. The Worker (Logic)**

```kotlin
class BlurWorker(context: Context, params: WorkerParameters) : Worker(context, params) {

    override fun doWork(): Result {
        // 1. Get Input
        // "IMAGE_URI" is the key we agreed upon
        val resourceUri = inputData.getString("IMAGE_URI")

        return if (resourceUri != null) {
            // ... Simulate processing the image ...
            val outputUri = "file://blurred_image.png"

            // 2. Prepare Output
            val outputData = workDataOf("OUTPUT_URI" to outputUri)

            // 3. Return Success with Data
            Result.success(outputData)
        } else {
            Result.failure()
        }
    }
}

```

**2. The Request (Sending Data)**

```kotlin
// Define the data (Key-Value)
val myInputData = workDataOf("IMAGE_URI" to "file://original_image.png")

val blurRequest = OneTimeWorkRequestBuilder<BlurWorker>()
    .setInputData(myInputData) // <--- Attach here
    .build()

WorkManager.getInstance(context).enqueue(blurRequest)

```

**3. Observing Result (Receiving Data)**

```kotlin
// In Activity/Fragment
WorkManager.getInstance(context)
    .getWorkInfoByIdLiveData(blurRequest.id)
    .observe(this) { workInfo ->
        if (workInfo.state == WorkInfo.State.SUCCEEDED) {
            // Get the output!
            val resultUri = workInfo.outputData.getString("OUTPUT_URI")
            showImage(resultUri)
        }
    }

```

#### **Interview Keywords**

Data object, Key-Value pairs, 10KB Limit, `workDataOf`, `setInputData`, `inputData`, Serialization, `Result.success(data)`.

#### **Interview Speak Paragraph**

"To pass arguments into a Worker, we use the `Data` object, which is a lightweight key-value container similar to a Bundle. We attach it to the request using `setInputData()`. Inside the Worker, we access these values via the `inputData` property. Once the task is complete, we can return results by passing a `Data` object into `Result.success()`. A crucial limitation to remember is the **10KB size limit** for this data; it is intended for small primitives like IDs, URIs, or flags, not for passing large objects or file content directly."

---

**Congratulations! You have completed Phase 2 (The Basics).**

You now know how to set up a standard WorkRequest. But real apps are complex.
**Ready to start Phase 3: Advanced WorkManager – Complex Control?**
(First topic: "Chaining Work Requests – Running Task A -> Task B -> Task C.")

---

[â¬… Back to Phase Overview](../)
