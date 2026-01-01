---
layout: default
title: Dispatchers
parent: Phase 5   Advanced Topics
nav_order: 5
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Dispatchers"
parent: "Advanced Topics & Coroutines"
nav_order: 5
---

# Dispatchers

<!-- Content starts here -->

Here are your interview-focused notes for **Dispatchers**.

---

### **Topic: Dispatchers (IO, Main, Default)**

#### **What It Is**

**Dispatchers** are like "Task Schedulers" or "Traffic Controllers." They decide **which thread** a coroutine should run on.
When you launch a coroutine, you must tell it where to go.

- **`Dispatchers.Main`:** The **UI Thread**. Use this for drawing to the screen or updating text. (Android specific).
- **`Dispatchers.IO`:** The **Input/Output Thread Pool**. Use this for reading/writing data (Network, Database, Files). It is optimized for "waiting."
- **`Dispatchers.Default`:** The **CPU Calculation Thread Pool**. Use this for heavy math, sorting lists, or processing complex logic. It is optimized for "working."

#### **Why It Exists**

**The "Wrong Thread" Crash:**

- If you do heavy math on the **Main** thread -> The UI freezes (ANR).
- If you try to update a TextView from a **Background** thread -> The app crashes (CalledFromWrongThreadException).

Dispatchers allow you to easily move tasks to the correct lane without managing raw threads manually.

#### **How It Works**

1. **`launch(Dispatchers.IO)`:** Starts the coroutine directly on the IO thread.
2. **`withContext(Dispatchers...)`:** The magic function to **switch** threads in the middle of a coroutine. Ideally, you start on Main, switch to IO for work, and switch back to Main for results.

#### **Example**

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    launch(Dispatchers.Default) { // Start on CPU thread
        // 1. Do Heavy Calculation (CPU)
        val sortedList = sortHugeList()

        // 2. Switch to IO (Network)
        withContext(Dispatchers.IO) {
            saveToDatabase(sortedList)
        }

        // 3. Switch to Main (UI - Simulated here)
        // In Android, this would be: withContext(Dispatchers.Main)
        println("Done! List saved.")
    }
}

fun sortHugeList(): List<Int> {
    println("Sorting on: ${Thread.currentThread().name}") // Prints: DefaultDispatcher-worker-1
    return listOf(1, 2, 3)
}

suspend fun saveToDatabase(list: List<Int>) {
    println("Saving on: ${Thread.currentThread().name}") // Prints: DefaultDispatcher-worker-1 (IO context)
    delay(500)
}

```

#### **Visual Representation**

```text
    [ Dispatchers.Main ]  <-- Only for UI Updates (TextView, Button)
            |
            | (switch using withContext)
            v
    [ Dispatchers.IO ]    <-- Network, Database, File Reading (Wait heavy)
            |
            | (switch)
            v
    [ Dispatchers.Default ] <-- Complex Logic, Sorting, Image Processing (CPU heavy)

```

#### **Interview Keywords**

Thread Pool, Context Switching, UI Thread, Worker Thread, `withContext`, Blocking vs Non-Blocking, CPU-bound vs IO-bound.

> **Pro Interview Tip (IO vs Default):** "Why not just use `Default` for everything?"
> **Answer:** "`Dispatchers.Default` is limited to the number of CPU cores (e.g., 4 or 8 threads). If you block them with network calls, the whole app slows down. `Dispatchers.IO` is designed for blocking tasks and can scale up to **64 threads** (or more) automatically to handle many waiting connections at once."

#### **Interview Speak Paragraph**

"I carefully manage thread safety using Dispatchers. I perform all UI updates on `Dispatchers.Main`. For network requests or database operations, I switch to `Dispatchers.IO`, which is optimized for blocking I/O tasks. For computationally expensive operations like parsing large JSON files or sorting data, I use `Dispatchers.Default` to avoid freezing the UI or clogging the IO pool. I use `withContext` to switch between these dispatchers smoothly within a single coroutine."

---

**Would you like to move on to the next topic: Flow (Basics)?**
