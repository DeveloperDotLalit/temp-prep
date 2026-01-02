---
layout: default
title: "Launch vs Async"
parent: "Phase 2: Core Building Blocks"
nav_order: 5
---

# Launch vs Async

This is the "Decision-Making" part of Phase 2. As an expert, you need to know not just _how_ to start a coroutine, but _which_ tool to pick for the specific job at hand.

---

## **Launch vs. Async: The Intent Difference**

### **What It Is**

Both `launch` and `async` are coroutine builders used to start a new task. However:

- **`launch`** is for **"Fire and Forget"**: You want to start a task and you don't care about getting a result back (e.g., logging, saving to a database).
- **`async`** is for **"Compute and Wait"**: You want to start a task specifically because you need the value it produces (e.g., an API response, a calculated number).

### **Why It Exists**

- **The Problem:** Sometimes you need to run two network calls at the same time and combine their results. If you use `launch`, you have no easy way to get those values back into your main flow.
- **The Solution:** `async` returns a special object called **`Deferred<T>`**, which is like a "IOU" or a "Promise." It says: "I'm working on it, and I'll give you the result whenever you're ready to `await()` it."

### **How It Works (The Mechanics)**

1. **Return Type:**

- `launch` returns a **Job**. You can use it to cancel the task, but you can't get data out of it.
- `async` returns a **Deferred** (which is just a Job with a result).

2. **`await()`:** To get the result from `async`, you call `.await()`. This is a **suspending call**. It pauses the current coroutine until the `async` block finishes and returns the value.
3. **Exception Handling:**

- `launch` throws exceptions immediately (it crashes the parent).
- `async` "holds" the exception inside the `Deferred` object. It only throws the exception when you actually call `.await()`.

### **Example (The Real-World Code)**

**Case A: Launch (Fire and Forget)**

```kotlin
// We just want to log that the user opened the app.
// We don't need to wait for this to finish to show the UI.
scope.launch {
    logger.logEvent("App_Opened")
}

```

**Case B: Async (Parallel Execution)**

```kotlin
scope.launch {
    // Start both requests at the same time
    val deferredUser = async { api.getUser() }
    val deferredPosts = async { api.getPosts() }

    // Wait for both to finish and combine them
    // Total time = time of the SLOWEST request, not both combined!
    val profile = Profile(deferredUser.await(), deferredPosts.await())
    showProfile(profile)
}

```

### **Interview Keywords**

Fire and Forget, Deferred, `await()`, Parallel Decomposition, Future/Promise, Exception Encapsulation.

### **Interview Speak Paragraph**

> "The choice between `launch` and `async` depends on whether a result is required from the coroutine. `launch` returns a `Job` and is used for 'fire-and-forget' tasks where we don't need to return a value to the caller. On the other hand, `async` returns a `Deferred<T>`, allowing us to perform parallel decomposition. By starting multiple `async` blocks and calling `await()` on them, we can execute multiple tasks concurrently and wait for their results, effectively reducing the total execution time to the duration of the longest task."

---

## **Phase 2 Recap (The Core Building Blocks)**

You have now mastered:

1. **Scope:** The boundary and lifecycle manager.
2. **Context:** The configuration dictionary (Name, Dispatcher, Job).
3. **Dispatchers:** The traffic controllers for Main, IO, and Default threads.
4. **Job vs. SupervisorJob:** How to control if a crash kills everyone or just the failing part.
5. **Launch vs. Async:** When to fire a task vs. when to wait for a result.

**Are you ready to move to Phase 3: Structured Concurrency & Error Handling? This is where we learn how to write "Production-Grade" code.**

Would you like me to start with **"Structured Concurrency"** (the philosophy that keeps your code leak-free)?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
