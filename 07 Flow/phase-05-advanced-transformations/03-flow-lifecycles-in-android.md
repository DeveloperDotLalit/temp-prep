---
layout: default
title: "Flow Lifecycles in Android"
parent: "Phase 5: Advanced Transformations and Composition"
nav_order: 3
---

# Flow Lifecycles in Android

We are concluding **Phase 5** with a topic that is absolute "bread and butter" for Android developers. In an interview, if you don't mention this, the interviewer might worry about your ability to prevent memory leaks and unnecessary battery drain.

---

### **What It Is – Simple explanation for beginners**

**`repeatOnLifecycle`** is a safety mechanism for collecting Flows in Android UI components (like Activities or Fragments).

Think of it as a **Smart Light Switch** for your data stream.

- When you enter a room (the app screen is visible/`STARTED`), the light turns on and data flows.
- When you leave the room (the app goes to the background/`STOPPED`), the light turns off automatically to save electricity (resources).
- When you come back into the room, the light turns back on, and the Flow restarts.

### **Why It Exists – The problem it solves**

- **The Background Waste Problem:** If you collect a Flow using a standard `lifecycleScope.launch`, the Flow keeps running even when the app is in the background. If that Flow is fetching GPS or high-frequency sensor data, it will drain the user's battery for no reason.
- **Illegal State Crashes:** If a Flow tries to update the UI while the app is in the background, it can cause crashes or "Fragment not attached" errors.
- **Memory Leaks:** Collecting indefinitely keeps references to the UI alive longer than necessary.

### **How It Works – Step-by-step logic**

1. **Subscription:** You call `repeatOnLifecycle(Lifecycle.State.STARTED)`.
2. **Activation:** As soon as the Activity/Fragment reaches the `STARTED` state, it launches a new coroutine and starts collecting the Flow.
3. **Automatic Cancellation:** As soon as the Activity/Fragment drops below `STARTED` (goes to the background/`STOPPED`), the coroutine is **cancelled**. The Flow producer stops.
4. **Re-subscription:** When the user returns to the app, the block runs again, and a fresh collection starts.

---

### **Example – Code-based**

```kotlin
class MyFragment : Fragment() {

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Use viewLifecycleOwner.lifecycleScope for Fragments
        viewLifecycleOwner.lifecycleScope.launch {
            // This suspends the coroutine until the lifecycle is at least STARTED
            // It cancels collection when the lifecycle is STOPPED
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.someFlow.collect { data ->
                    // Update UI safely here
                    binding.textView.text = data
                }
            }
        }
    }
}

```

### **Interview Focus: `repeatOnLifecycle` vs `launchWhenStarted**`

A very common question for Senior developers: _"Why shouldn't you use launchWhenStarted anymore?"_

- **The Answer:** `launchWhenStarted` merely **pauses** the collection when the app is in the background, but the Flow producer stays active. `repeatOnLifecycle` actually **cancels** and **restarts** the collection, making it much more resource-efficient.

### **Interview Keywords**

Lifecycle Awareness, Resource Conservation, Battery Optimization, `STARTED` state, Cancellation, Restartable Collection, `repeatOnLifecycle`.

### **Interview Speak Paragraph**

> "In Android, collecting Flows safely requires awareness of the UI lifecycle to prevent memory leaks and unnecessary resource consumption. While `lifecycleScope.launch` is common, the best practice is to use `repeatOnLifecycle`. This API ensures that the Flow collection only happens when the UI is in a specific state, such as `STARTED`. When the app moves to the background, `repeatOnLifecycle` automatically cancels the collection coroutine, stopping the underlying data production. This is superior to older methods like `launchWhenStarted`, which only paused the consumer while allowing the producer to keep wasting resources in the background."

---

**Congratulations! You have completed Phase 5.** You are now fully equipped with the technical knowledge of how Flow works from creation to UI collection.

**Next Step:** We move to **Phase 6: Interview Scenarios & Real-World Use Cases**. This is where we apply everything we've learned to solve specific app problems. Shall we start with the **Search-as-you-type scenario (Debouncing & Distinct Filtering)**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
