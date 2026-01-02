---
layout: default
title: "Dispatchers"
parent: "Phase 2: Core Building Blocks"
nav_order: 3
---

# Dispatchers

Now that we know the **Context** is the "ID card," the **Dispatcher** is the most important piece of info on that card. It tells the coroutine: _"Which worker (thread) should actually execute this code?"_

---

## **Dispatchers: The Resource Managers**

### **What It Is**

A **Dispatcher** is an object that sends (dispatches) the coroutine work to a specific thread pool. Think of it as a **Traffic Controller** at an airport. The airplanes (Coroutines) are ready to fly, and the Dispatcher tells them which runway (Thread) to use.

### **Why It Exists**

- **The Problem:** Not all tasks are equal.
- Updating a Button text is fast (UI).
- Downloading a 1GB file is slow (Network/IO).
- Calculating the value of Pi to a million digits is heavy (CPU).

- **The Solution:** If you do heavy math on the UI thread, the app freezes. If you do UI work on a background thread, the app crashes. Dispatchers ensure the **right task** happens on the **right thread**.

### **How It Works (The Big Three)**

There are three main dispatchers you will use 99% of the time:

#### **1. Dispatchers.Main**

- **The Worker:** The Main (UI) Thread.
- **When to use:** For anything the user sees. Updating Text, showing a Spinner, or Navigating between screens.
- **Constraint:** Only one Main thread exists. If you block it, the app freezes (ANR).

#### **2. Dispatchers.IO**

- **The Worker:** A large pool of threads shared for networking and disk access.
- **When to use:** API calls (Retrofit), Database work (Room), Reading/Writing files.
- **Capacity:** It is designed to scale up to many threads because these tasks spend most of their time _waiting_ for a response.

#### **3. Dispatchers.Default**

- **The Worker:** A pool of threads equal to the number of CPU cores (e.g., 4 or 8).
- **When to use:** Intensive "Calculation" work. Sorting a list of 10,000 items, Image processing, JSON parsing.
- **Reasoning:** It's optimized for tasks that keep the CPU busy 100% of the time.

### **Example (The Switcheroo)**

The best practice is to start on `Main`, switch to `IO` for the data, and switch back to `Main` to show it. We use `withContext` to do this elegantly.

```kotlin
fun loadProfile() {
    viewModelScope.launch(Dispatchers.Main) {
        // 1. We are on the UI thread (Show loading)
        showLoading()

        // 2. Switch to IO thread for the network call
        val user = withContext(Dispatchers.IO) {
            api.fetchUser() // This is a suspend function
        }

        // 3. Automatically back on Main thread (Hide loading)
        hideLoading()
        userName.text = user.name
    }
}

```

### **Interview Keywords**

Thread Pool, UI Thread, Offloading, IO-bound, CPU-bound, `withContext`, Main-safety.

### **Interview Speak Paragraph**

> "Dispatchers are the components responsible for determining which thread or thread pool a coroutine executes on. We have three primary types: `Dispatchers.Main` for UI-related tasks, `Dispatchers.IO` for blocking data operations like network or disk access, and `Dispatchers.Default` for CPU-intensive computations. A key best practice I follow is 'Main-safety,' where I use `withContext` to ensure that heavy operations are offloaded to the appropriate background dispatcher, ensuring the UI thread remains responsive at all times."

---

**Common Interview Question: "What is the difference between IO and Default?"**

- **Answer:** `IO` is for "Waiting" tasks (Network/Disk). It can create many threads (up to 64 or more) because threads aren't doing much "thinking." `Default` is for "Thinking" tasks (Math/Logic). It limits threads to the number of CPU cores because having more threads than cores for math actually slows things down due to context switching.

**Would you like to move on to the next topic: Job & SupervisorJob (Controlling the lifecycle and failure)?**

Would you like me to explain how `withContext` is different from `launch` in terms of performance?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
