---
layout: default
title: "Image Uploading Scenario"
parent: "Phase 6: Real World Interview Scenarios"
nav_order: 1
---

# Image Uploading Scenario

---

Here are your expert notes for **Phase 6, Topic 1**.

---

### **Topic: System Design Scenario – Robust Image Uploading**

#### **The Problem**

**Interviewer:** "Design a feature where a user selects a photo and it uploads to our server. It must handle poor network conditions, app crashes, and phone restarts. The user must see progress."

**Why naive solutions fail:**

- **Thread/Coroutine:** If the user closes the app, the upload dies.
- **Service:** If the system needs memory, it kills the service. If the phone reboots, the service is forgotten.

#### **The Solution: WorkManager + Foreground Notification**

We choose **WorkManager** because it persists the request (survives reboot) and handles constraints (waits for network). We add **Foreground Support** so the user sees a progress bar and the system doesn't kill us during a long upload.

#### **Architecture Flow**

1. **UI Layer:** User picks an image -> Get `Uri` -> Enqueue `OneTimeWorkRequest`.
2. **Constraint Layer:** "Must have Internet."
3. **Worker Layer:**

- Read file from `Uri`.
- Compress file (optional).
- **Promote to Foreground** (Show Notification).
- Upload Loop (Chunked or Streamed).
- Return `Result.success` or `Result.retry`.

#### **Key Technical Decisions (The "Why")**

1. **Uri Access:** We pass the file `Uri` (e.g., `content://...`) as Input Data.

- _Edge Case:_ What if the user deletes the photo while waiting for WiFi?
- _Fix:_ Inside `doWork()`, check if the file still exists using `ContentResolver`. If not, return `Result.failure()` (don't retry).

2. **Network Strategy:**

- Use `Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED)`.
- If WiFi drops mid-upload, WorkManager stops us. We rely on the library's automatic retry to resume later.

3. **Progress Updates:**

- Use `setProgressAsync()` inside the worker to update the progress bar in the UI.
- Use `setForeground()` to update the Notification progress bar.

#### **Example Code: The Robust Uploader**

```kotlin
class PhotoUploadWorker(ctx: Context, params: WorkerParameters) : CoroutineWorker(ctx, params) {

    override suspend fun doWork(): Result {
        val imageUriString = inputData.getString("URI") ?: return Result.failure()
        val imageUri = Uri.parse(imageUriString)

        // 1. Promote to Foreground (Crucial for long uploads)
        setForeground(createForegroundInfo(0))

        return try {
            // 2. Open Stream safely
            val resolver = applicationContext.contentResolver
            resolver.openInputStream(imageUri)?.use { inputStream ->

                // 3. Simulated Upload with Progress
                // In reality, use Retrofit with a RequestBody that supports progress
                for (progress in 0..100 step 10) {
                    uploadChunk(inputStream, progress)

                    // Update Notification
                    setForeground(createForegroundInfo(progress))
                    // Update App UI
                    setProgress(workDataOf("PROGRESS" to progress))
                }
            }
            Result.success()
        } catch (e: IOException) {
            // Network error? Retry.
            if (isTransientError(e)) Result.retry() else Result.failure()
        } catch (e: SecurityException) {
            // Permission lost or file deleted? Fail permanently.
            Result.failure()
        }
    }

    private fun createForegroundInfo(progress: Int): ForegroundInfo {
        val notification = NotificationCompat.Builder(applicationContext, "UPLOAD_CH")
            .setContentTitle("Uploading Photo")
            .setProgress(100, progress, false)
            .setSmallIcon(R.drawable.ic_upload)
            .build()
        return ForegroundInfo(1, notification)
    }
}

```

#### **Interview Keywords**

ContentResolver, Transient vs. Permanent Error, setProgress, setForeground, Multipart Upload, Constraints, Persistable URI permission.

#### **Interview Speak Paragraph**

"To design a robust photo uploader, I would use **WorkManager** with a `OneTimeWorkRequest`. I'd set a constraint for `NetworkType.CONNECTED` so it waits for the internet. Inside the `CoroutineWorker`, I'd first call `setForeground()` to show a notification, ensuring the system prioritizes the process. I would read the image using `ContentResolver` and stream it to the server. If the upload fails due to a network timeout, I'd return `Result.retry()` to leverage exponential backoff. Crucially, I'd catch permanent errors like `FileNotFoundException` (if the user deleted the image) and return `Result.failure()` to stop retrying. This ensures reliability across reboots and network changes."

---

**Would you like to move to the next scenario: "Scenario: Data Syncing – Designing an offline-first sync engine"?**

---

[â¬… Back to Phase Overview](../)
