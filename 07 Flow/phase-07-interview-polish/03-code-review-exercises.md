---
layout: default
title: "Code Review Exercises"
parent: "Phase 7: Final Interview Polish"
nav_order: 3
---

# Code Review Exercises

We have reached the final technical hurdle of **Phase 7**. In many senior interviews, you won't just be asked to write code—you'll be asked to **Review** it. This exercises your ability to spot "silent killers": code that works but drains battery, leaks memory, or causes race conditions.

---

### **What It Is – Simple explanation for beginners**

Code Review for Flows is like being a **Home Inspector**. The house might look beautiful from the outside, but you are looking for the leaky pipes behind the walls and the loose wiring in the attic.

In Flow, "bad code" usually falls into three categories:

1. **Thread Violations:** Trying to change threads the wrong way.
2. **Resource Leaks:** Forgetting to stop a flow when the user leaves.
3. **Performance Bottlenecks:** Doing heavy work multiple times or blocking the UI.

### **Why It Exists – The problem it solves**

- **Battery Drain:** A flow that keeps polling in the background is a top cause of user uninstalls.
- **Janky UI:** If a transformation (like `map`) is too heavy and runs on the Main Thread, the app will stutter.
- **Crashes:** Improper exception handling leads to "Uncaught Exception" crashes that are hard to trace.

---

### **How It Works – The "Red Flag" Checklist**

#### **Red Flag 1: The `withContext` Trap**

**The Mistake:** Using `withContext` inside a flow builder to change threads.
**The Fix:** Use `.flowOn(Dispatchers.IO)`.

#### **Red Flag 2: Collecting in the wrong Scope**

**The Mistake:** Using `GlobalScope` or `lifecycleScope.launch` without lifecycle awareness.
**The Fix:** Use `repeatOnLifecycle(Lifecycle.State.STARTED)`.

#### **Red Flag 3: The "Multiple Collection" Waste**

**The Mistake:** Collecting a Cold Flow in two different places (Fragment A and Fragment B), causing two network calls.
**The Fix:** Use `.stateIn()` or `.sharedIn()` to "hot-load" and share the result.

---

### **Example – The "Spot the Bug" Exercise**

Look at this common "Junior" implementation. Can you see the 3 major issues?

```kotlin
// ❌ BAD CODE
class UserViewModel(val repo: UserRepository) : ViewModel() {
    val users = flow {
        // Issue 1: Breaking Context Preservation
        withContext(Dispatchers.IO) {
            val list = repo.getUsers()
            emit(list)
        }
    }
}

// In Activity
lifecycleScope.launch {
    // Issue 2: Background Waste
    // This keeps running even if the user minimizes the app!
    viewModel.users.collect { data ->
        binding.recyclerView.adapter = UserAdapter(data)
    }
}

```

**✅ THE CODE REVIEW FIX:**

```kotlin
class UserViewModel(val repo: UserRepository) : ViewModel() {
    // Fix 1: Use flowOn and share the flow (Hot Flow)
    val users = flow {
        val list = repo.getUsers()
        emit(list)
    }.flowOn(Dispatchers.IO)
     .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
}

// In Activity
viewLifecycleOwner.lifecycleScope.launch {
    // Fix 2: Lifecycle aware collection
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.users.collect { data ->
            binding.recyclerView.adapter = UserAdapter(data)
        }
    }
}

```

---

### **Interview Focus: Performance Optimization**

- **The "Conflation" Tip:** If your UI is getting too many updates (e.g., a high-frequency sensor), remind the interviewer that using `.conflate()` can save CPU by dropping intermediate values that the UI can't keep up with anyway.
- **The "SharedFlow" Replay:** If a user navigates back and forth and sees a "Toast" message every time, check if the `SharedFlow` has a `replay > 0`. It should usually be `0` for one-time events.

### **Interview Keywords**

Resource Leak, Context Preservation, `flowOn`, `repeatOnLifecycle`, `stateIn`, Conflation, Structured Concurrency.

### **Interview Speak Paragraph**

> "When reviewing Kotlin Flow code, I look for three critical performance and safety indicators. First, I ensure 'Context Preservation' is respected by checking that thread switching is handled via `flowOn` rather than `withContext`. Second, I verify that UI collection is lifecycle-aware using `repeatOnLifecycle` to prevent background resource leaks. Finally, I look for opportunities to multicast cold flows using `stateIn` or `sharedIn`, which prevents redundant and expensive operations—like network calls—when multiple components are observing the same data source."

---

**CONGRATULATIONS!** You have finished all seven phases of the Kotlin Flows roadmap. You have the knowledge of a senior-level Android developer.

**Final Step:** We have reached the **End Phase for Interview Questions and Answers**.

Would you like me to generate a **Master List of High-Frequency Interview Questions** (from basic to architectural) so you can practice your "Interview Speak" for all of them at once?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
