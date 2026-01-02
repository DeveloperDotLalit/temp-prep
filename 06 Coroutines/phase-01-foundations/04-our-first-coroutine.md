---
layout: default
title: "Our First Coroutine"
parent: "Phase 1: The Foundations"
nav_order: 4
---

# Our First Coroutine

Now that we understand the "why," it's time to actually write some code. To start a coroutine, we can't just call a `suspend` function from a regular function; we need a "bridge" or a "builder" to get things started.

---

## **Our First Coroutine: The Basic Launch**

### **What It Is**

A **Coroutine Builder** is a function that creates and starts a coroutine. The most common one is `launch`. Think of it as the "Start" button on a machine. You put your code inside the curly braces of a builder, and Kotlin takes care of running it in the background.

### **Why It Exists**

- **The Bridge:** Regular functions (like `main` or `onCreate`) live in the "blocking world." Suspend functions live in the "coroutine world." You need a builder to bridge these two worlds.
- **Fire and Forget:** Sometimes you just want to start a task (like logging an event or saving a draft) and don't need to wait for a result. `launch` is perfect for this.

### **How It Works (Step-by-Step)**

1. **Dependency Setup:** First, you must add the `kotlinx-coroutines-core` library to your `build.gradle` file.
2. **Choosing a Scope:** You need a `CoroutineScope` (we will deep-dive into this in Phase 2). For a simple "Hello World," we often use `GlobalScope` or `runBlocking`.
3. **The Builder (`launch`):** You call `launch { ... }`. This starts the coroutine. It returns a **Job**, which is like a handle you can use to cancel the task later if you want.
4. **Non-Blocking Delay:** Inside the coroutine, we use `delay()`. This is the suspend version of `Thread.sleep()`. It pauses the coroutine but **does not freeze the app.**

### **Example (The Code)**

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking { // 1. Creates a bridge to the coroutine world
    println("Main program starts on: ${Thread.currentThread().name}")

    launch { // 2. Starts a new coroutine (Fire and Forget)
        println("Coroutine starts on: ${Thread.currentThread().name}")
        delay(1000) // 3. Suspends for 1 second (Non-blocking!)
        println("Coroutine finished!")
    }

    println("Main program continues... I didn't wait for the delay!") // 4. This runs immediately
}

```

**What happens here?**

- `runBlocking` waits for everything inside it to finish (used mostly in `main` functions or tests).
- `launch` starts a task on a background thread (usually).
- The "Main program continues" line prints **before** "Coroutine finished" because `delay` didn't stop the rest of the code from running.

### **Interview Keywords**

Coroutine Builder, `launch`, `runBlocking`, Job, Non-blocking delay.

### **Interview Speak Paragraph**

> "To start our first coroutine, we use a 'Coroutine Builder' like `launch`. While `runBlocking` is typically used to bridge regular blocking code to the coroutine world in main functions or tests, `launch` is the standard 'fire-and-forget' builder used for background tasks. It returns a `Job` object, which allows us to manage the coroutine's lifecycle. The key takeaway is that when we call a suspending function like `delay()` inside a `launch` block, it pauses that specific coroutine without blocking the thread it's running on, allowing other code to continue execution."

---

### **Phase 1 Recap**

You now know:

1. **Concurrency** is about doing more with less.
2. **Suspend** is a state-machine "bookmark" that frees up threads.
3. **Coroutines** are light-weight objects (~bytes) compared to heavy-weight Threads (~1MB).
4. **Launch** is the basic builder to get a coroutine running.

**Are you ready to move to Phase 2: The Core Building Blocks (Scope, Context, and Dispatchers)?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
