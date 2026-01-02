---
layout: default
title: "Cancellation"
parent: "Phase 3: Structured Concurrency and Error Handling"
nav_order: 2
---

# Cancellation

One of the most common mistakes in Coroutines is thinking that calling `job.cancel()` is like pulling a plug on a machine. In reality, it’s more like **sending a "Please Stop" request** to a worker. If the worker is wearing noise-canceling headphones, they might never see the request.

---

## **Cancellation: Cooperative Multitasking**

### **What It Is**

Cancellation in Kotlin Coroutines is **cooperative**. This means a coroutine doesn't just "die" the moment you tell it to; it must periodically check if it has been cancelled and then stop its own work gracefully.

### **Why It Exists**

- **The Problem:** If you force-kill a thread (like the old `Thread.stop()`), it might happen while the thread is halfway through writing to a file or a database, leaving your data corrupted.
- **The Solution:** Cooperative cancellation allows the coroutine to reach a "safe point," clean up its resources (like closing a file), and then exit.

### **How It Works**

When you call `job.cancel()`, the coroutine's state changes to "Cancelling." For it to actually stop, it needs to hit a **Suspension Point** that is "cancellation-aware."

1. **Built-in Suspend Functions:** Most standard functions like `delay()`, `withContext()`, or `await()` are already programmed to check for cancellation. If the job is cancelled, they immediately throw a `CancellationException`.
2. **The Exception:** A `CancellationException` is the mechanism that stops the code. It is a "silent" exception—it doesn't crash your app; it just unwinds the coroutine.

#### **What if your code is doing a heavy loop?**

If you are doing a `while(true)` loop with no `delay()`, your coroutine becomes **un-cancellable**! You must manually check the status:

- **`isActive`:** A property that returns `false` the moment the job is cancelled. You should check this in your loops.
- **`yield()`:** A function that pauses the coroutine momentarily to check for cancellation and let other coroutines run.
- **`ensureActive()`:** A quick way to throw an exception if the coroutine is no longer active.

---

### **Example: The "Stubborn" Coroutine**

**The Wrong Way (Un-cancellable):**

```kotlin
val job = launch(Dispatchers.Default) {
    var nextPrintTime = System.currentTimeMillis()
    var i = 0
    while (i < 5) { // This loop doesn't check for cancellation!
        if (System.currentTimeMillis() >= nextPrintTime) {
            println("I'm working... ${i++}")
            nextPrintTime += 500
        }
    }
}
delay(1000)
job.cancel() // This does NOTHING because the loop is busy!
println("Tried to cancel, but worker ignored me.")

```

**The Right Way (Cooperative):**

```kotlin
val job = launch(Dispatchers.Default) {
    var i = 0
    while (i < 5 && isActive) { // 1. Check isActive!
        // OR use yield() here
        println("I'm working... ${i++}")
        delay(500) // 2. delay() is also cancellation-aware
    }
}
delay(1000)
job.cancelAndJoin() // Properly waits for the worker to stop
println("Worker stopped gracefully.")

```

---

### **Cleaning up with `finally**`

Since cancellation throws an exception, you can use a `try-catch-finally` block to clean up resources (like closing a database connection).

> **Note:** If you need to call a `suspend` function inside a `finally` block after cancellation, you must use `withContext(NonCancellable) { ... }`, otherwise the cleanup code will also be cancelled!

---

### **Interview Keywords**

Cooperative Cancellation, `CancellationException`, `isActive`, `yield()`, `cancelAndJoin`, `NonCancellable`.

### **Interview Speak Paragraph**

> "Cancellation in Kotlin is cooperative, meaning a coroutine isn't forcibly killed but must check for a cancellation signal. Most standard suspending functions like `delay` check this automatically. However, for CPU-intensive tasks or long-running loops, we must manually check the `isActive` property or call `yield()`. If we don't, the coroutine will continue to consume resources even after its parent scope has been cancelled. It’s also a best practice to use `try-finally` blocks to ensure resources are released, potentially using `NonCancellable` context if cleanup requires further suspending calls."

---

**Common Interview Question: "What is the difference between `cancel()` and `cancelAndJoin()`?"**

- **Answer:** `cancel()` just sends the request to stop and moves on. `cancelAndJoin()` sends the request and **suspends** the current code until the target coroutine actually finishes its cleanup and dies.

**Would you like to move on to the next topic: Exception Handling (Using CoroutineExceptionHandler vs. try-catch)?**

I can also explain the **"Cancellation is a two-way street"** concept if you'd like to dive deeper into how children notify parents. Shall we?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
