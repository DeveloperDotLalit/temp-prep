---
layout: default
title: "Combining Flows"
parent: "Phase 5: Advanced Transformations and Composition"
nav_order: 1
---

# Combining Flows

In an Android app, you rarely have just one data source. You might have one Flow for "User Profile" and another for "User Posts." To show a complete screen, you need to wait for both. This is where **Flow Composition** comes in.

---

### **What It Is – Simple explanation for beginners**

Combining flows is the process of taking two or more separate streams and merging them into one.

- **`zip`:** Like a **zipper** on a jacket. To move the zipper up, the left teeth and the right teeth must meet. If one side is missing a tooth, the zipper stops and waits. It pairs items 1-to-1.
- **`combine`:** Like a **live dashboard**. If you have a "Total Price" display that depends on "Quantity" and "Unit Price," the dashboard updates whenever _either_ of those values changes, using the latest known value of the other.
- **`flattenMerge`:** Like **multiple lanes merging into one highway**. It takes multiple flows and just shoves all their emissions into a single stream as fast as they arrive.

### **Why It Exists – The problem it solves**

- **Synchronization:** You need to wait for two independent API calls to finish before showing a UI state (`zip`).
- **Dynamic UI:** You want to filter a list of "Products" based on a "Search Query" typed by the user. Every time the search query _or_ the product list changes, the UI should update (`combine`).
- **Concurrency:** You have 5 separate fetch tasks and you want them all to run at the same time and show results as they come in (`flattenMerge`).

---

### **How It Works – Comparison & Logic**

#### **1. `zip` (The Pairer)**

It waits for both Flows to emit an item before sending the result. If Flow A emits 3 items and Flow B emits 2, the result Flow only emits 2 items and then stops.

#### **2. `combine` (The Most Recent)**

It doesn't wait for a pair. Once both flows have emitted at least _once_, any new emission from _either_ flow triggers a new result using the most recent value from the other.

#### **3. `flattenMerge` (The Merger)**

This is used when you have a "Flow of Flows." It flattens them into one. It doesn't care about pairing; it just emits everything as it happens.

---

### **Example – Code-based**

```kotlin
val flowA = flowOf("A1", "A2").onEach { delay(1000) }
val flowB = flowOf("B1", "B2", "B3").onEach { delay(500) }

// ZIP Example: Pairs them up
// Result: (A1, B1), (A2, B2) -> Total 2 emissions
flowA.zip(flowB) { a, b -> "$a + $b" }

// COMBINE Example: Uses latest
// Result: (A1, B1), (A1, B2), (A2, B2), (A2, B3) -> Total 4 emissions
flowA.combine(flowB) { a, b -> "$a + $b" }

// FLATTENMERGE Example: Concurrent execution
val flowOfFlows = flowOf(flowA, flowB)
flowOfFlows.flattenMerge() // Emits B1, A1, B2, B3, A2 (order depends on timing)

```

### **Interview Focus: When to use which?**

- **Question:** "What is the main difference between zip and combine?"
- **Answer:** `zip` is strictly 1-to-1; it waits for both sides to provide a new value. `combine` uses the latest available values and triggers whenever _either_ side updates. In Android UI development, `combine` is much more common (e.g., combining UserState and PermissionsState).

### **Interview Keywords**

Synchronization, Pairwise, Latest Emission, Concurrency, Flattening, 1-to-1 vs Many-to-Many.

### **Interview Speak Paragraph**

> "In Kotlin Flow, we use `zip` and `combine` to merge multiple data streams. `zip` is used when you need to pair emissions 1-to-1 from two flows, waiting for both to produce a value before emitting a result. On the other hand, `combine` is more common in Android UI logic; it triggers whenever either upstream flow emits a new value, using the most recent emission from the other. For handling multiple flows simultaneously without pairing, `flattenMerge` allows us to collect from multiple streams concurrently, merging them into a single, flattened output."

---

**Next Step:** Now that we can combine flows, we need to handle the "Flow of Flows" situation more gracefully. Shall we move to **Flattening Flows: Understanding `flatMapConcat`, `flatMapMerge`, and `flatMapLatest**`?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
