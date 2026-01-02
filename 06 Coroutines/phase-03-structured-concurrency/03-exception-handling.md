---
layout: default
title: "Exception Handling"
parent: "Phase 3: Structured Concurrency and Error Handling"
nav_order: 3
---

# Exception Handling

Exception handling in Coroutines is one of the most complex parts of the ecosystem because it depends heavily on **how** you started the coroutine (`launch` vs. `async`) and the **hierarchy** (Job vs. SupervisorJob).

---

## **Exception Handling & Propagation**

### **What It Is**

Exception handling is the mechanism used to catch and manage errors that occur during asynchronous execution. In Coroutines, an exception doesn't just stay where it happens—it **propagates** (travels) up the tree to the parent.

### **Why It Exists**

- **The Problem:** In traditional threads, if a background thread crashes, it often just dies silently or crashes the entire app without giving you a chance to recover.
- **The Solution:** Kotlin provides a structured way to catch errors so you can show a "Try Again" button or log the error instead of letting the app disappear.

---

### **How It Works: The Two Main Strategies**

#### **1. The `try-catch` Approach (Local Handling)**

This is the standard way to handle exceptions. You wrap the "scary" code in a `try-catch` block.

- **Best for:** Specific blocks of code inside a coroutine.
- **Behavior:** It catches the error immediately, prevents it from propagating further, and allows the coroutine to continue or finish gracefully.

#### **2. `CoroutineExceptionHandler` (Global/Scope Handling)**

This is a specific element in the `CoroutineContext` that acts as a "Last Resort" catch-all.

- **Best for:** Logging uncaught exceptions or showing a generic "Something went wrong" message.
- **Limitation:** It only works with `launch`. It **cannot** catch exceptions thrown in `async` blocks (because `async` expects you to catch the error when you call `.await()`).

---

### **How Exceptions Propagate (The "Tree" Rule)**

When an exception is not caught locally with `try-catch`:

1. **Child Fails:** It notifies its parent.
2. **Parent Reacts:** \* If the parent is a **Standard Job**, it cancels itself and all other children.

- If the parent is a **SupervisorJob**, it lets the other children keep running.

3. **The End of the Road:** If no one catches the exception, it reaches the "Root" of the scope. If a `CoroutineExceptionHandler` is present there, it handles it. If not, the app crashes.

---

### **The "Big 3" Types of Exception Scenarios**

| Scenario                    | Behavior                                              | How to Handle                                                                      |
| --------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **`launch`**                | Propagates immediately to the parent.                 | Use `try-catch` inside the block OR `CoroutineExceptionHandler` in the context.    |
| **`async`**                 | Encapsulates the exception in the `Deferred` object.  | Wrap the `.await()` call in a `try-catch`.                                         |
| **`CancellationException`** | A special "silent" exception used to stop coroutines. | **Don't catch it!** Or if you do, re-throw it so the system can finish cancelling. |

---

### **Example (The Real-World Code)**

**Case A: Handling `launch` with a Handler**

```kotlin
val handler = CoroutineExceptionHandler { _, exception ->
    println("Caught $exception in Handler!")
}

val scope = CoroutineScope(Job() + handler)

scope.launch {
    throw RuntimeException("Boom!") // Caught by handler
}

```

**Case B: Handling `async` with try-catch**

```kotlin
val deferred = scope.async {
    throw RuntimeException("Async Error!")
}

scope.launch {
    try {
        deferred.await() // Exception is thrown HERE
    } catch (e: Exception) {
        println("Caught in await: ${e.message}")
    }
}

```

**Case C: The SupervisorScope (The "Island" Strategy)**
If you want a specific part of your code to fail without killing the rest of the scope, use `supervisorScope`.

```kotlin
suspend fun loadDashboard() = supervisorScope {
    launch {
        // If this fails, the 'Load News' launch still runs!
        throw Exception("Weather Failed")
    }
    launch {
        println("Load News - Still working!")
    }
}

```

---

### **Summary of Exception Types to Handle**

1. **Regular Exceptions (`RuntimeException`, etc.):** Business logic errors. Handle with `try-catch`.
2. **`CancellationException`:** Thrown when a job is cancelled. Generally, you should ignore this so the coroutine can die peacefully.
3. **`TimeoutCancellationException`:** A subclass of cancellation thrown by `withTimeout`. You might want to catch this specifically to show a "Request Timed Out" message.

---

### **Interview Keywords**

Exception Propagation, `CoroutineExceptionHandler`, `supervisorScope`, `CancellationException`, `Deferred.await()`, Uncaught Exceptions.

### **Interview Speak Paragraph**

> "Exception handling in Coroutines depends on the builder used and the scope's hierarchy. In a `launch` block, exceptions propagate up the job tree and can be caught using a `CoroutineExceptionHandler` at the root or a `try-catch` locally. For `async`, the exception is encapsulated in the `Deferred` object and is only re-thrown when `await()` is called, meaning we must wrap the `await()` call in a `try-catch`. To prevent a single child's failure from cancelling the entire scope, I use a `SupervisorJob` or a `supervisorScope` block, which ensures that exceptions only propagate downwards and don't affect sibling coroutines."

---

**Common Interview Question: "Why doesn't try-catch work around a launch block?"**

- **Answer:** Because `launch` is non-blocking and returns immediately. By the time the code inside `launch` throws an exception, the `try-catch` block that was wrapping the `launch` call has already finished executing. You must put the `try-catch` **inside** the curly braces of the `launch`.

**Would you like to move on to the final topic of Phase 3: WithContext (The best practice for switching threads safely)?**

Would you like me to explain the **"Exception Aggregation"** rule (what happens when multiple children fail at the same time)?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
