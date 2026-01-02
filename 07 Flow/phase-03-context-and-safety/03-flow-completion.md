---
layout: default
title: "Flow Completion"
parent: "Phase 3: Context Execution and Safety"
nav_order: 3
---

# Flow Completion

We are finishing up the "Context & Safety" portion of **Phase 3**. Just like a `try-finally` block in standard Java or Kotlin, `Flow` needs a way to signal that the stream is over—whether it finished successfully or crashed.

---

### **What It Is – Simple explanation for beginners**

**`.onCompletion()`** is an intermediate operator that executes its code block when the Flow finishes.

Think of it as the **"Clean-up Crew."** Whether a party ends because the clock struck midnight (normal completion) or because the fire alarm went off (an exception), the clean-up crew still comes in to sweep the floor and turn off the lights.

### **Why It Exists – The problem it solves**

- **Resource Management:** If you opened a database connection or a file stream inside your Flow, you must close it when the Flow stops to avoid memory leaks.
- **UI Feedback:** You might want to hide a "Loading Spinner" or show a "Finished" toast message as soon as the data stops flowing.
- **Observing Failure:** Unlike `.catch()`, which _handles_ errors, `.onCompletion()` allows you to _see_ if the flow ended due to an error without actually catching it.

### **How It Works – Step-by-step logic**

1. **Normal Completion:** When the Producer finishes emitting all values, `.onCompletion()` is triggered with a `null` cause.
2. **Cancellation:** If the Coroutine scope is cancelled (e.g., the user leaves the screen), the Flow stops and `.onCompletion()` is triggered.
3. **Exception:** If an exception is thrown upstream, `.onCompletion()` triggers _first_ (allowing you to see the error), and then the error continues moving down to the `.catch()` operator.

### **Example – Code-based**

```kotlin
val simpleFlow = flow {
    emit(1)
    emit(2)
    // throw RuntimeException("Something went wrong!") // Uncomment to see error handling
}

lifecycleScope.launch {
    simpleFlow
        .onStart { println("Show Loading Spinner") } // Bonus: Runs before the first emission
        .onCompletion { cause ->
            // 'cause' is null if finished normally
            if (cause != null) {
                println("Flow finished with error: $cause")
            } else {
                println("Flow finished successfully")
            }
            println("Hide Loading Spinner") // Cleanup UI
        }
        .collect { value ->
            println("Received: $value")
        }
}

```

### **Interview Focus: Trade-offs & Scenarios**

- **onCompletion vs. catch:** This is a common interview question. **Answer:** `.catch()` is for _handling_ an error (and optionally providing a fallback). `.onCompletion()` is for _cleanup_ and observing the end-state. Crucially, `.onCompletion()` does not "consume" the error; it still propagates downstream.
- **Order of Operations:** If an error occurs, the order is: `onCompletion` `catch`.

### **Interview Keywords**

Cleanup, Finally block, Termination, Resource Release, Throwable cause, Stream Lifecycle.

### **Interview Speak Paragraph**

> "The `.onCompletion` operator acts similarly to a 'finally' block in traditional programming; it is triggered whenever a Flow terminates, whether it finishes normally, is cancelled, or fails due to an exception. It provides a nullable `Throwable` parameter, which is useful for determining if the flow closed successfully or with an error. In Android development, this is the ideal place to perform cleanup tasks, such as closing database cursors or hiding progress bars in the UI, ensuring that the app's state remains consistent regardless of how the stream ended."

---

**Next Step:** We are ready for the most advanced part of Phase 3. Shall we tackle **Backpressure & Buffering** (solving the "Fast Producer vs. Slow Consumer" problem)? This is where senior-level understanding really shines! Would you like me to proceed with that?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
