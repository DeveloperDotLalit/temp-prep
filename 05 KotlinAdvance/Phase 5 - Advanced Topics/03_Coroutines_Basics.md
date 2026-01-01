---
layout: default
title: Coroutines Basics
parent: Phase 5   Advanced Topics
nav_order: 3
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Coroutines Basics"
parent: "Advanced Topics & Coroutines"
nav_order: 3
---

# Coroutines Basics

<!-- Content starts here -->

Here are your interview-focused notes for **Coroutines Basics**. This is arguably the most critical topic for modern Android/Kotlin interviews.

---

### **Topic: Coroutines Basics (Scope, Context, Builders)**

#### **What It Is**

- **Coroutines:** Think of them as **"Lightweight Threads."** They are tasks that can pause and resume.
- **Scope:** The **"Lifetime Manager."** It determines how long the coroutine lives. If the Scope dies (e.g., a screen closes), all coroutines inside it are cancelled automatically.
- **Context:** The **"Configuration."** It tells the coroutine _where_ to run (which thread) and what its name is.
- **Builders:** The functions used to **start** a new coroutine (mainly `launch` and `async`).

#### **Why It Exists**

**The Problem (Threads are Expensive):**

- **Memory:** Creating a standard Java Thread costs about **1MB of RAM**. If you try to spawn 10,000 threads, your app crashes (Out of Memory).
- **CPU:** Switching between threads ("Context Switching") is heavy work for the CPU.

**The Solution (Coroutines are Lightweight):**

- Coroutines do **not** equal Threads.
- You can run **100,000 coroutines** on a _single_ thread.
- When a coroutine pauses (e.g., waiting for API), it **releases** the underlying thread so another coroutine can use it. It recycles threads efficiently.

#### **How It Works**

1. **Select a Scope:** e.g., `GlobalScope` (Bad, lives forever) or `viewModelScope` (Good, lives with the screen).
2. **Select a Builder:**

- **`launch`**: "Fire and Forget." You start it and don't care about the return value. Returns a `Job`.
- **`async`**: "Perform and Return." You expect a result back (like a number or JSON). Returns a `Deferred` (which is like a "Future" promise).

3. **Suspend:** The magic happens here. The function pauses execution without blocking the thread.

#### **Example**

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking { // runBlocking is a bridge (mostly for testing)

    // 1. LAUNCH (Fire and Forget)
    // "I want to print something, I don't need a result back."
    val job = launch {
        delay(1000L) // Pauses for 1 sec WITHOUT blocking the thread
        println("Task 1 Completed")
    }

    // 2. ASYNC (Compute and Return)
    // "I need to calculate a number."
    val deferredResult = async {
        delay(1000L)
        return@async 42
    }

    println("Waiting...")

    // 3. AWAIT
    // We wait for the async result to be ready
    val result = deferredResult.await()
    println("Result received: $result")
}

```

#### **Visual Representation**

```text
    Traditional Threads (Blocking):
    [Thread 1] ----(Waiting 2s)----> [Work]
                   (Thread is Useless/Frozen here)

    Coroutines (Suspending):
    [Thread 1] --(Start Task A)--> (Pause A, Save State)
                                   (Start Task B on SAME Thread) -->
                                   (Resume Task A) -->

```

#### **Interview Keywords**

Structured Concurrency, Suspending vs Blocking, `launch` vs `async`, `Job` vs `Deferred`, Context Switching, Lightweight, `runBlocking`.

> **The "Gotcha" (Structured Concurrency):** Interviewers love to ask: _"What is Structured Concurrency?"_ > **Answer:** "It is the principle that **no coroutine should get lost.** Every coroutine must start within a specific **Scope**. This ensures that when the parent scope is cancelled (e.g., user navigates away), all child jobs are automatically cancelled, preventing memory leaks."

#### **Interview Speak Paragraph**

"I use Coroutines for all asynchronous programming because they are far more memory-efficient than traditional threads. A key distinction is that threads are expensive resources managed by the OS, while coroutines are lightweight user-level tasks. I always adhere to **Structured Concurrency** by launching coroutines within a specific lifecycle-aware scope, like `viewModelScope`. I typically use `launch` for operations that don't return a value, and `async` when I need to perform parallel calculations and `await` a result."

---

**Would you like to move on to the next topic: Suspend Functions?**
