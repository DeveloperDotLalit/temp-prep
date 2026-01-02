---
layout: default
title: "Debugging Questions"
parent: "Phase 6: Final Interview Drill"
nav_order: 3
---

# Debugging Questions

Debugging coroutines is different from debugging standard threads because coroutines are "virtualized" by the Kotlin runtime. You can't always just look at a thread dump and see which coroutine is stuck.

---

## **The Debugging Drill: Finding Leaks & Deadlocks**

### **What It Is**

Debugging in coroutines involves identifying why a task is either **running longer than it should** (Memory Leak) or **waiting forever for a resource** (Deadlock).

- **Memory Leak:** A coroutine that stays "Active" because it was launched in the wrong scope (like `GlobalScope`) or is stuck in an un-cancellable loop, holding onto UI objects (like an Activity or Fragment).
- **Deadlock:** Two or more coroutines waiting on each other to release a resource (like a Mutex or a Channel), resulting in no progress.

### **Why It Exists**

- **The Problem:** Because coroutines are "cheap," developers often launch them and forget them. However, if a coroutine holds a reference to a `ViewModel` or a `Context` and never finishes, that memory can never be reclaimed by the Garbage Collector.
- **The Solution:** We use specific tools and coding patterns to ensure coroutines are "Lifecycle-aware" and "Cancellable."

---

### **How It Works (Detection & Prevention)**

#### **1. Identifying a Memory Leak**

If you suspect a leak, the first step is to check if your coroutines are **Structured**.

- **The "GlobalScope" Trap:** If you see `GlobalScope.launch`, it's a red flag. These tasks don't die when the screen closes.
- **The "Stubborn Loop" Trap:** If a coroutine is in a `while(true)` loop without any `yield()` or `delay()`, calling `job.cancel()` will not stop it. It will leak until the app process dies.

**Tool to use:** **LeakCanary**. It can detect if an Activity is being held in memory by a background coroutine after `onDestroy()`.

#### **2. Using the Debugger (Coroutines Panel)**

Modern IDEs (Android Studio / IntelliJ) have a dedicated **Coroutines Debugger**.

- It shows you a list of all coroutines, their current **State** (Running, Suspended, Created), and their **Stack Trace**.
- **Pro Tip:** Set the system property `kotlinx.coroutines.debug` to `on`. This allows you to see the name of the coroutine in the thread name during logging.

#### **3. Finding Deadlocks with Mutex**

In coroutines, we don't use `synchronized` blocks (which block threads). We use `Mutex`.

- If Coroutine A calls `mutex.lock()` and then suspends forever, Coroutine B will also wait forever at `mutex.lock()`.
- **The Fix:** Always use `mutex.withLock { ... }`. It automatically releases the lock even if an exception is thrown, preventing most deadlocks.

---

### **Example: The "Leaky" Code vs. The "Fixed" Code**

**The Leaky Way:**

```kotlin
class MyActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // LEAK: GlobalScope lives longer than the Activity.
        // If this loop takes 10 minutes, the Activity stays in RAM for 10 minutes.
        GlobalScope.launch {
            while (true) {
                doWork() // If this doesn't suspend, it's also un-cancellable
            }
        }
    }
}

```

**The Safe Way:**

```kotlin
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // SAFE: lifecycleScope cancels automatically in onDestroy()
        lifecycleScope.launch {
            while (isActive) { // Check for cancellation!
                doWork()
                yield() // Give other coroutines a chance and check cancellation
            }
        }
    }
}

```

---

### **Interview Keywords**

`GlobalScope`, `isActive`, `yield()`, LeakCanary, `kotlinx-coroutines-debug`, Mutex Deadlock, Structured Concurrency.

### **Interview Speak Paragraph**

> "Finding memory leaks in coroutines usually comes down to auditing 'Structured Concurrency' and 'Cooperative Cancellation.' I look for coroutines launched in `GlobalScope` or those that don't check the `isActive` flag in long-running loops, as these are the primary causes of 'zombie' tasks that hold onto UI references. To debug these, I use the Android Studio Coroutine Debugger to inspect suspended states and the `kotlinx-coroutines-debug` library to track coroutine names in logs. For deadlocks, I prefer using `Mutex.withLock` over manual lock/unlock calls to ensure that resources are always released, even in the event of an unexpected exception."

---

## **Final Phase Recap (The Interview Drill)**

You have now mastered the high-level engineering questions:

1. **Internals:** You know about the State Machine and CPS.
2. **Comparison:** You can justify choosing Coroutines over RxJava or WorkManager.
3. **Debugging:** You know how to spot leaks and use the debugger.

### **Final Next Step**

We have covered all the phases in your roadmap!

**Would you like me to generate a "Mock Interview" list of 10-15 high-frequency questions based on all the notes we've created, so you can practice your 'Interview Speak'?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
