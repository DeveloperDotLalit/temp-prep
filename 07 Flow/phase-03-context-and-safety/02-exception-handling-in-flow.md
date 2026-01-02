---
layout: default
title: "Exception Handling in Flow"
parent: "Phase 3: Context Execution and Safety"
nav_order: 2
---

# Exception Handling in Flow

Handling errors in a stream is different from handling errors in a standard function because a Flow has many parts (Producer, Intermediaries, and Consumer). If an error happens in the middle of a pipe, you need to know exactly where to "catch" it.

---

### **What It Is**

**Exception Handling** in Flow is the mechanism used to manage crashes or logic errors that occur during the emission or transformation of data.

In Flow, we have two primary ways to handle errors:

1. **`try-catch` blocks:** The traditional way to wrap code.
2. **The `.catch()` operator:** A specific Flow operator designed to catch errors from "upstream" (the code above it).

### **Why It Exists**

- **Exception Transparency:** Flow is designed so that a Producer should not have to worry about how the Consumer handles errors.
- **Preventing App Crashes:** If a network request fails inside a Flow, you don't want the entire app to disappear. You want to catch the error and perhaps show a "Try Again" message.
- **Stream Recovery:** Unlike a standard `try-catch` that just stops, Flow's `.catch()` allows you to **emit a fallback value** (like a cached result) even after an error occurs.

### **How It Works**

The most important rule in Flow is: **The `.catch()` operator only catches exceptions from UPSTREAM.**

1. **Upstream Errors:** If the Producer or a `.map` block throws an error, a `.catch()` placed below them will handle it.
2. **Downstream Errors:** If the error happens inside the `.collect` block (the Consumer), a `.catch()` operator above it **cannot** see it. To catch errors in the Consumer, you must use a traditional `try-catch` around the `collect` call.

### **Example – Code-based**

```kotlin
val riskyFlow = flow {
    emit("Connecting...")
    throw IllegalStateException("Network Failed!") // Producer Error
}

lifecycleScope.launch {
    riskyFlow
        .map { it.uppercase() }
        .catch { e ->
            // 1. Handles the "Network Failed!" error
            println("Caught in operator: ${e.message}")
            emit("Default Cached Data") // You can emit a fallback!
        }
        .collect { value ->
            println("Received: $value")
            // throw RuntimeException("UI Crash") // .catch WON'T see this!
        }
}

// Handling EVERYTHING (Producer + Consumer)
lifecycleScope.launch {
    try {
        riskyFlow.collect { /* ... */ }
    } catch (e: Exception) {
        println("Caught everything here")
    }
}

```

### **Interview Focus: Trade-offs & Comparisons**

- **The "Upstream Only" Rule:** This is the #1 question. Interviewers will ask: _"What happens if an exception is thrown in the collect block but you have a .catch operator?"_ **Answer:** The app will crash. `.catch` only looks at what happened _before_ it in the pipeline.
- **Emitting in Catch:** A unique feature of `.catch` is that it gives you a `FlowCollector`, meaning you can call `emit()` inside the catch block to provide a default value so the UI doesn't stay empty.

### **Interview Keywords**

Exception Transparency, Upstream Exceptions, Downstream Exceptions, Encapsulation, Fallback Emission, `catch` operator.

### **Interview Speak Paragraph**

> "Flow is designed with 'Exception Transparency' in mind, meaning the stream should encapsulate its own errors. We primarily use the `.catch` operator to handle exceptions occurring in the producer or intermediate transformations. It is vital to remember that `.catch` only handles 'upstream' exceptions—any error thrown inside the `collect` block must be handled with a traditional `try-catch`. A major advantage of the `.catch` operator is its ability to emit fallback values, allowing the stream to recover and provide a default state to the UI instead of simply terminating."

---

**Next Step:** Now that we can handle errors, let's look at how to clean up after ourselves. Shall we move to **Flow Completion (`.onCompletion`)**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
