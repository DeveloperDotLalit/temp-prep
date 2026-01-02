---
layout: default
title: "Mock Interview QnA"
parent: "Phase 6: Final Interview Drill"
nav_order: 3
---

# Mock Interview QnA

This is the final "Boss Level" of your preparation. I have compiled the most frequent and challenging interview questions, categorized by their focus area.

For each question, I’ve provided the **"Core Answer"** (the technical truth) and the **"Interview Speak"** (the polished, senior-level delivery).

---

## **Category 1: The Fundamentals**

### **1. What is the difference between a Thread and a Coroutine?**

- **Core Answer:** Threads are managed by the OS (heavy, 1MB stack); Coroutines are managed by the Kotlin runtime (light, few bytes).
- **Interview Speak:** "A thread is an OS-level resource that is pre-emptive and expensive to switch. Coroutines are 'lightweight threads' that are cooperative. They live in the heap and don't have their own stack, allowing us to run thousands of them on a single thread by using suspension instead of blocking."

### **2. What does the `suspend` keyword actually do?**

- **Core Answer:** It marks a function as capable of being paused and resumed. It adds a `Continuation` parameter at compile time.
- **Interview Speak:** "The `suspend` keyword tells the compiler that a function can pause its execution without blocking the underlying thread. Behind the scenes, the compiler transforms the function into a state machine using Continuation Passing Style (CPS). This allows the thread to be released for other work while the function waits for its result."

---

## **Category 2: Structured Concurrency**

### **3. Why should we avoid `GlobalScope`?**

- **Core Answer:** It has no lifecycle boundary; it leads to memory leaks.
- **Interview Speak:** "We avoid `GlobalScope` because it breaks 'Structured Concurrency.' Coroutines launched in `GlobalScope` are not bound to any job or lifecycle, meaning they can continue running even after the calling component is destroyed. This leads to memory leaks and unpredictable behavior. Instead, we should use lifecycle-aware scopes like `viewModelScope` or `lifecycleScope`."

### **4. What is the difference between `Job` and `SupervisorJob`?**

- **Core Answer:** `Job` cancels all siblings if one fails; `SupervisorJob` does not.
- **Interview Speak:** "The difference lies in exception propagation. In a standard `Job` hierarchy, if one child fails, the exception propagates up and cancels the parent and all other siblings. A `SupervisorJob` ignores child failures, allowing siblings to continue running. It’s ideal for independent tasks, like a dashboard with multiple independent API widgets."

---

## **Category 3: Builders & Dispatchers**

### **5. When would you use `async` over `launch`?**

- **Core Answer:** `async` for a result (`Deferred`); `launch` for fire-and-forget (`Job`).
- **Interview Speak:** "I use `launch` for side effects where I don't need a return value, like logging or database writes. I use `async` when I need a result back from the coroutine. `async` is particularly powerful for parallel decomposition, where I can start multiple tasks and call `awaitAll()` to get the combined results efficiently."

### **6. Difference between `Dispatchers.IO` and `Dispatchers.Default`?**

- **Core Answer:** `IO` is for waiting (Network/Files, many threads); `Default` is for math/logic (CPU-bound, limited threads).
- **Interview Speak:** "`Dispatchers.IO` is optimized for I/O-bound tasks that spend most of their time waiting for the disk or network. It can create many threads to handle high-latency tasks. `Dispatchers.Default` is optimized for CPU-intensive work, like JSON parsing or image filtering, and limits its thread pool to the number of CPU cores to minimize context-switching overhead."

---

## **Category 4: Flow & Channels**

### **7. What makes a Flow "Cold"?**

- **Core Answer:** It doesn't run code until a terminal operator (like `collect`) is called.
- **Interview Speak:** "A Flow is 'cold' because it is a declarative stream—the code inside the `flow { }` block doesn't execute until someone starts collecting. Every new collector triggers a fresh execution of the flow logic, which makes it very resource-efficient compared to 'hot' streams like Channels."

### **8. What is the difference between `StateFlow` and `SharedFlow`?**

- **Core Answer:** `StateFlow` holds a single latest value (State); `SharedFlow` is for events (Toasts, Navigation).
- **Interview Speak:** "`StateFlow` is a state-holder that always maintains its current value and requires an initial state. It is perfect for UI states. `SharedFlow` is designed for events; it doesn't hold a 'current' value and can be configured with a replay buffer. Use `StateFlow` for data that 'is' (like a profile) and `SharedFlow` for data that 'happens' (like a navigation event)."

---

## **Category 5: Error Handling & Performance**

### **9. How do you handle an exception in an `async` block?**

- **Core Answer:** Wrap the `.await()` call in a `try-catch`.
- **Interview Speak:** "Exceptions in `async` are encapsulated within the `Deferred` object. They aren't thrown until we call `.await()`. Therefore, I wrap the `await()` call in a `try-catch` block. If I want to handle it inside the `async` block, I'd use a local `try-catch` there to return a default or error result."

### **10. How do you make a function "Main-Safe"?**

- **Core Answer:** Use `withContext` inside the function to switch threads.
- **Interview Speak:** "A function is Main-Safe if it can be called from the Main thread without blocking it. To achieve this, I use `withContext` inside the function to switch to the appropriate background dispatcher (like `IO` or `Default`). This encapsulates the threading logic, so the UI developer doesn't have to worry about which dispatcher to use."

---

## **Category 6: Senior/Internal Mechanics**

### **11. What is "Cooperative Cancellation"?**

- **Core Answer:** Coroutines must check their own status to stop.
- **Interview Speak:** "Cancellation in Kotlin is cooperative, meaning the coroutine must periodically check if its `Job` is still active. Most standard suspending functions like `delay()` check this automatically. However, for long-running CPU loops, we must manually check the `isActive` property or call `yield()` to ensure the coroutine stops when requested."

### **12. Explain the concept of "Back-pressure" in Coroutines.**

- **Core Answer:** Suspension handles it; producers slow down automatically if the consumer is slow.
- **Interview Speak:** "In Coroutines, back-pressure is handled naturally through suspension. Because the `send()` function in Channels and `emit()` in Flows are suspending, if the consumer is too slow to process the data, the producer is automatically paused by the runtime. This prevents memory overflows without needing complex buffer strategies like those found in RxJava."

---

### **How to use these for practice:**

1. **Record yourself:** Speak the "Interview Speak" paragraph out loud.
2. **Focus on "Why":** If they ask a "How" question, always end your answer with a "Why" (e.g., "I use this because it prevents memory leaks...").
3. **Check your tone:** Stay confident, but keep it conversational—like one expert talking to another.

**This concludes our Kotlin Coroutines Mastery Guide! Would you like me to help you with another topic (like Jetpack Compose or Clean Architecture), or should we wrap this up?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
