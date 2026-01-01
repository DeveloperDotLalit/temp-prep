---
layout: default
title: "Concurrency & Race Conditions"
parent: "Architecture (MVVM/MVI/Clean): Phase 6: with the topic: \"Refactoring Bloated ViewModels\"?"
nav_order: 3
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Concurrency & Race Conditions**.

This distinguishes a "Junior" developer (whose app crashes when you tap quickly) from a "Senior" developer (whose app handles chaos gracefully).

---

### **Topic: Concurrency & Race Conditions**

#### **What It Is**

Concurrency means multiple tasks running at overlapping times. A **Race Condition** is a bug that happens when the **timing** of these tasks messes up the result.

- **The "Double Click" Bug:** The user taps "Pay" twice in 100ms. The app sends _two_ payment requests because the first one didn't finish before the second one started.
- **The "Outdated Search" Bug:** You type "A", then "AB". The "A" request takes 5 seconds, "AB" takes 1 second. The screen shows result for "AB", then suddenly overwrites it with "A" (the old, slow request).

#### **Why It Exists (The Problem)**

Android is asynchronous. Network calls take time.
If you don't manage the order of operations, the "Last" request might not be the "Last" one to finish. The app enters an inconsistent state because it processed events in the wrong order or processed duplicates.

#### **How It Works (The Solutions)**

**1. Solving Double Clicks (State Guarding)**
We use the **State** to block the second click.

- User Clicks -> Check `if (isLoading) return`.
- Set `isLoading = true`.
- Start work.
- Any other clicks are ignored because `isLoading` is true.

**2. Solving Outdated Calls (Job Cancellation)**
We use **Coroutine Jobs** to kill the old work.

- User types "A". Start **Job 1**.
- User types "AB".
- **Cancel Job 1** immediately (Stop wasting data!).
- Start **Job 2**.
- Only the latest job is allowed to finish and update the UI.

#### **Example (The Auto-Canceling Search)**

**❌ Bad Code (The Race Condition):**

```kotlin
fun onSearchQuery(query: String) {
    // If "A" takes 10s and "AB" takes 1s, "A" will return LAST
    // and overwrite the correct results.
    viewModelScope.launch {
        val result = repository.search(query)
        _results.value = result
    }
}

```

**✅ Good Code (Job Cancellation & Debounce):**

```kotlin
private var searchJob: Job? = null // Keep track of the running work

fun onSearchQuery(query: String) {
    // 1. Kill the previous search immediately
    searchJob?.cancel()

    // 2. Start the new search
    searchJob = viewModelScope.launch {
        delay(300) // Optional: Debounce (wait for user to stop typing)

        // 3. If the user types again during this delay, this line never runs!
        val result = repository.search(query)
        _results.value = result
    }
}

```

#### **Interview Keywords**

Race Condition, Concurrency, Thread Safety, Job Cancellation, Debounce, Throttling, Structured Concurrency, Idempotency.

#### **Interview Speak Paragraph**

> "I handle concurrency issues by leveraging Kotlin Coroutines' structured concurrency. For scenarios like a search bar, I prevent race conditions by holding a reference to the current search `Job` and canceling it whenever the input changes. This ensures that only the latest network call updates the UI, preventing 'ghost' results from outdated queries. For UI interactions like double-clicks, I guard the action by checking the current `UiState`—ignoring inputs if an operation is already in progress (`isLoading`)—to ensure the action is performed only once."

---

**Would you like to proceed to the next note: "Handling Complex Lists (Heterogeneous Views)"?**
