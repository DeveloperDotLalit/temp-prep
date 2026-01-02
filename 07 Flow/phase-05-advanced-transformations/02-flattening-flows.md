---
layout: default
title: "Flattening Flows"
parent: "Phase 5: Advanced Transformations and Composition"
nav_order: 2
---

# Flattening Flows

This is a "Level 2" topic. In intermediate Flow usage, you often run into a situation where you have a value (like a User ID) and you want to use that value to call _another_ Flow (like a "Fetch Orders" flow). This creates a **Flow of Flows** (`Flow<Flow<T>>`).

**Flattening** is the act of squashing that nested Flow into a single, usable stream.

---

### **What It Is – Simple explanation for beginners**

Flattening operators decide how to handle the "Inner Flow" when the "Outer Flow" sends a new value.

- **`flatMapConcat`:** The **Wait-Your-Turn** operator. It finishes the first inner flow completely before starting the next one.
- **`flatMapMerge`:** The **Everyone-At-Once** operator. It starts all inner flows immediately and merges their results as they arrive.
- **`flatMapLatest`:** The **New-Is-Better** operator. As soon as a new outer value arrives, it **kills** the previous inner flow and starts the new one.

### **Why It Exists – The problem it solves**

Imagine you are building a search feature:

1. The user types "A". You start a Flow to fetch results for "A".
2. Before "A" is finished, the user types "AB".
3. **The Conflict:** Do you wait for "A" to finish? Do you run both "A" and "AB" together? Or do you stop "A" because "AB" is the only thing that matters now?

Flattening operators give you the logic to handle these specific scenarios.

---

### **How It Works – Comparison & Logic**

#### **1. `flatMapConcat` (Sequential)**

It ensures order. If Flow A is running, and Flow B arrives, Flow B stays in a queue.

#### **2. `flatMapMerge` (Concurrent)**

It runs everything in parallel. You can set a `concurrency` limit to decide how many inner flows can run at once.

#### **3. `flatMapLatest` (Cancellation)**

It is the most common for UI. It ensures that if the input changes, we don't waste time on old data.

---

### **Example – Code-based**

```kotlin
val userIdFlow = flowOf(1, 2, 3) // Outer Flow

fun getOrders(id: Int): Flow<String> = flow {
    emit("Order for $id started")
    delay(1000) // Simulate network
    emit("Order for $id finished")
}

// 1. flatMapConcat: Total time ~3 seconds
// Results: 1-start, 1-finish, 2-start, 2-finish, 3-start, 3-finish
userIdFlow.flatMapConcat { id -> getOrders(id) }

// 2. flatMapMerge: Total time ~1 second (runs in parallel)
// Results: 1-start, 2-start, 3-start ... (all finish together)
userIdFlow.flatMapMerge { id -> getOrders(id) }

// 3. flatMapLatest:
// If 1, 2, and 3 are emitted rapidly, 1 and 2 get CANCELLED.
// Results: 1-start (cancelled), 2-start (cancelled), 3-start, 3-finish
userIdFlow.flatMapLatest { id -> getOrders(id) }

```

### **Interview Focus: The "Search" Scenario**

An interviewer will ask: _"Which flatMap operator would you use for a search-as-you-type feature?"_
**The Answer:** `flatMapLatest`. Because if the user types a new character, the previous network request is no longer relevant. We should cancel the old one to save bandwidth and prevent "flickering" where old results pop up after new ones.

### **Interview Keywords**

Sequential, Concurrent, Cancellation, Flow of Flows, Flattening, `flatMapLatest`, `flatMapConcat`.

### **Interview Speak Paragraph**

> "Flattening operators are used when we have a 'Flow of Flows' and need to manage how inner streams are collected. `flatMapConcat` processes inner flows sequentially, ensuring order but taking more time. `flatMapMerge` allows for concurrent execution, which is great for parallel tasks. However, in Android development, `flatMapLatest` is often the most useful; it cancels the previous inner flow as soon as a new value is emitted by the outer flow, ensuring that the UI always displays data corresponding to the most recent input and avoiding unnecessary background work."

---

**Next Step:** We are finishing Phase 5! To wrap up advanced composition, we need to talk about **Flow Lifecycles in Android**. Shall we learn how to use **`repeatOnLifecycle`** to collect flows safely in UI components? This is a "must-know" for memory leak prevention.

---

[â¬… Back to Phase](../) | [Next âž¡](../)
