---
layout: default
title: "Coroutine Cheat Sheet"
parent: "Kotlin Coroutines Mastery Roadmap"
nav_order: 2
---

This cheat sheet is designed for quick reference before an interview or while coding. It condenses all our phases into a single, high-density guide.

---

# **Kotlin Coroutines Cheat Sheet**

## **1. The Fundamentals**

| Concept          | Description                                                    | Key Takeaway                                                |
| ---------------- | -------------------------------------------------------------- | ----------------------------------------------------------- |
| **Coroutine**    | Lightweight "virtual thread" managed by the Kotlin runtime.    | Thousands of coroutines can run on one thread.              |
| **Suspend**      | Pauses execution without blocking the thread.                  | Frees the CPU; implemented via a **State Machine**.         |
| **Continuation** | A hidden object that stores the "bookmark" of where to resume. | Every `suspend` function has a hidden `Continuation` param. |

---

## **2. Builders: How to Start**

- **`launch`**: Returns a `Job`. Fire-and-forget. Throws exceptions immediately.
- **`async`**: Returns a `Deferred<T>`. Compute-and-wait. Use `.await()` to get the result.
- **`runBlocking`**: Bridges regular code to coroutines. Blocks the current thread (use only in `main` or tests).
- **`withContext`**: Switches the dispatcher and returns the result. **Best practice for Main-safety.**

---

## **3. Dispatchers: Where to Run**

- **`Dispatchers.Main`**: UI operations (Android Main thread).
- **`Dispatchers.IO`**: Disk and Network. Optimized for "waiting" (64+ threads).
- **`Dispatchers.Default`**: CPU-intensive work (Sorting, JSON parsing). Optimized for "math" (Threads = CPU Cores).
- **`Dispatchers.Unconfined`**: Runs on the current thread until the first suspension. (Rarely used).

---

## **4. Structured Concurrency & Scopes**

> **Rule:** Every coroutine must have a parent. When the parent dies, children die.

- **`viewModelScope`**: Tied to the Android ViewModel lifecycle.
- **`lifecycleScope`**: Tied to the Activity/Fragment lifecycle.
- **`coroutineScope`**: Creates a temporary scope; fails if any child fails.
- **`supervisorScope`**: Creates a temporary scope; child failures don't kill siblings.

---

## **5. Jobs & Cancellation**

- **`Job`**: A handle to the coroutine lifecycle (`join()`, `cancel()`).
- **`SupervisorJob`**: Isolates failures (child crash doesn't kill parent).
- **Cooperative Cancellation**: Check `isActive` or call `yield()` in long-running loops.
- **`NonCancellable`**: Use for cleanup code in `finally` blocks that _must_ run even if cancelled.

---

## **6. Flow & Channels**

### **Channel (Hot)**

- Think: **Walkie-Talkie**.
- Starts sending immediately. Data is consumed once.
- Great for: **Communication between coroutines.**

### **Flow (Cold)**

- Think: **Netflix Stream**.
- Starts only when `.collect()` is called.
- Great for: **Reactive data (Database updates, Search results).**

### **StateFlow vs. SharedFlow**

- **`StateFlow`**: Always has a value. Conflates data. (Use for: **UI State**).
- **`SharedFlow`**: No initial value. No conflation. (Use for: **One-time events/Toasts**).

---

## **7. Error Handling Strategy**

1. **Local Error?** Use `try-catch` inside the coroutine.
2. **`async` Error?** Wrap the `.await()` call in `try-catch`.
3. **Global Safety?** Add a `CoroutineExceptionHandler` to the scope.
4. **Isolate Failure?** Use `SupervisorJob` or `supervisorScope`.

---

## **8. Testing & Debugging**

- **`runTest`**: Skips `delay()` calls instantly using Virtual Time.
- **`advanceTimeBy(ms)`**: Moves the virtual clock.
- **`kotlinx-coroutines-debug`**: Enable to see coroutine names in logs.

---

## **9. The "Senior" Pro-Tips**

- **Main-Safety:** Every repository/network function should be `suspend` and use `withContext(Dispatchers.IO)` so it can be called from the Main thread safely.
- **Avoid GlobalScope:** Always use a specific, lifecycle-bound scope.
- **Avoid `Job()` in Scopes:** If you pass a `Job()` to a `CoroutineScope`, manual cancellation is required. Use built-in scopes whenever possible.

---

**Would you like me to convert this cheat sheet into a downloadable Markdown file, or perhaps move on to a new topic like Jetpack Compose or Kotlin Flow Operators in more depth?**
