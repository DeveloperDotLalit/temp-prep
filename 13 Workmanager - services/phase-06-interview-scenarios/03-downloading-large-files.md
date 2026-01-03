---
layout: default
title: "Downloading Large Files"
parent: "Phase 6: Real World Interview Scenarios"
nav_order: 3
---

# Downloading Large Files

---

Here are your expert notes for **Phase 6, Topic 3**.

---

### **Topic: System Design Scenario – Downloading Large Files**

#### **The Problem**

**Interviewer:** "Design a feature to download a 2GB movie or a large ML model update in the background. If the user quits the app, the download must continue. If the internet drops, it should pause and resume later."

**Why naive solutions fail:**

- **Coroutines:** Die immediately if the user closes the app.
- **Standard WorkManager:** Killed by the OS after ~10 minutes. A 2GB file on a slow connection takes much longer than 10 minutes.

#### **The Solution: WorkManager (Foreground) + Resumable Logic**

To survive longer than 10 minutes, we **must** use a **Foreground Service** (via WorkManager).
To handle network drops efficiently, we must implement **Resumability** (don't start from 0% again).

#### **Architecture Flow**

1. **Configuration:**

- `Constraint`: `NetworkType.UNMETERED` (WiFi only) + `RequiresStorageNotLow`.

2. **Promotion:**

- The Worker starts and immediately calls `setForeground()`.
- It shows a Notification with a progress bar.

3. **The Download Loop (Resumable):**

- Check: "Do I have a partial file on disk?" (e.g., 500MB downloaded).
- **HTTP Range Header:** Tell the server: _"Give me bytes starting from 500MB."_
- Append new bytes to the file.

4. **Completion:**

- Verify file hash (Checksum).
- Remove notification.

#### **Key Technical Decisions**

1. **Foreground Service:** Essential. Without a visible notification, Android treats the download as "low priority" and will kill it to save battery.
2. **HTTP Range Headers:**

- _Scenario:_ Download fails at 99%.
- _Without Range:_ You re-download 2GB. User is furious.
- _With Range:_ You re-download the last 1%. User is happy.

3. **Backoff Policy:**

- If the server is down, return `Result.retry()`. WorkManager handles the exponential wait times.

#### **Example Code: The Resumable Downloader**

```kotlin
class DownloadWorker(ctx: Context, params: WorkerParameters) : CoroutineWorker(ctx, params) {

    override suspend fun doWork(): Result {
        val fileUrl = inputData.getString("URL")!!
        val targetFile = File(applicationContext.filesDir, "movie.mp4")

        // 1. Promote to Foreground (Allow long running)
        setForeground(createForegroundInfo(0))

        return try {
            // 2. Check how much we already have
            val downloadedBytes = if (targetFile.exists()) targetFile.length() else 0L

            // 3. Request ONLY the missing chunk (Resumable)
            val response = api.downloadFile("bytes=$downloadedBytes-", fileUrl)

            if (!response.isSuccessful) return Result.retry()

            // 4. Stream and Save
            response.body()?.byteStream()?.use { input ->
                FileOutputStream(targetFile, true).use { output -> // 'true' = Append mode
                    val buffer = ByteArray(8 * 1024)
                    var bytesRead: Int
                    var totalSaved = downloadedBytes

                    while (input.read(buffer).also { bytesRead = it } != -1) {
                        output.write(buffer, 0, bytesRead)
                        totalSaved += bytesRead

                        // Update Progress Notification
                        // (Limit updates to once per second to avoid lag)
                        setForeground(createForegroundInfo(calculateProgress(totalSaved)))
                    }
                }
            }
            Result.success()
        } catch (e: Exception) {
            // Connection dropped? Retry later (resume from where we left off)
            Result.retry()
        }
    }
}

```

#### **Interview Keywords**

Foreground Service, HTTP Range Header, Partial Content (206), Append Mode, `NetworkType.UNMETERED`, Checksum/Hashing, `DownloadManager` (System alternative).

#### **Interview Speak Paragraph**

"For downloading large files, I use a `CoroutineWorker` configured as a **Long-Running Worker** by calling `setForeground()`. This prevents the OS from killing the task after the standard 10-minute window. To ensure efficiency and robustness, I implement **resumable downloads**. Before starting, I check the size of any partial file on disk and use the **HTTP `Range` header** to request only the remaining bytes from the server. This prevents wasting bandwidth if the connection drops at 90%. I also set a constraint for `NetworkType.UNMETERED` so large downloads only occur on WiFi, respecting the user's data plan."

---

**Would you like to move to the next topic: "Scenario: Location Tracking – The complexities of tracking location in the background"?**

---

[â¬… Back to Phase Overview](../)
