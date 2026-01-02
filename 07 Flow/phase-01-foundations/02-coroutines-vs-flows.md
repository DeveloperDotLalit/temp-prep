---
layout: default
title: "Coroutines vs Flows"
parent: "Phase 1: Foundations and Core Concepts"
nav_order: 2
---

# Coroutines vs Flows

This is a crucial distinction. In Kotlin, people often get confused because both Coroutines and Flows involve "background work," but they serve very different structural purposes.

---

### **What It Is**

- **Coroutines** are about **"Doing"**: It is a framework for managing a single task that might take time. You start it, it suspends (pauses) while waiting for a result, and it returns **one thing**.
- **Flows** are about **"Observing"**: It is a framework built _on top_ of Coroutines to manage a sequence of many tasks. It is a stream that can return **multiple things** over time.

Think of a Coroutine as a **Function** that can pause. Think of a Flow as a **Pipe** that uses Coroutines to move data.

### **Why It Exists**

- **The Limitation of `suspend`:** A standard `suspend` function can only return one value. If you need to return a progress update (10%, 20%, 30%) or a list of items that are loading one by one, a `suspend` function isn't enough because it "returns and dies."
- **The Need for Reactivity:** In Android, we want our UI to "react" to data changes. If a Coroutine just fetches data once, the UI won't update when the database changes. Flows stay "alive" to keep pushing new data.

### **How It Works**

Flows use Coroutines under the hood. You cannot have a Flow without a Coroutine because a Flow must be "collected" (started) inside a Coroutine scope.

1. **Coroutine (One-Shot):** You call `fetchUser()`. The thread is freed. The network returns the user. The function resumes and returns the object. Done.
2. **Flow (Continuous):** You call `observeUser()`. The Flow starts a Coroutine. Every time the user’s name changes in the database, the Flow **emits** a new value. The Coroutine stays active as long as you are listening.

### **Example: A Single Photo vs. A Video Stream**

- **Coroutine (The Single Photo):** You click a button to take a picture. The camera processes (suspends) and gives you **one image file**.
- **Flow (The Video Stream):** You turn on your camera's "Video Preview." The camera is now a **Flow**. It is continuously emitting "frames" (images) to your screen. It doesn't stop after the first frame; it keeps going until you turn the camera off.

```kotlin
// Coroutine: Single Value
suspend fun fetchPrice(): Int {
    delay(1000) // Simulate work
    return 100
}

// Flow: Multiple Values over time
fun trackPrice(): Flow<Int> = flow {
    for (i in 1..5) {
        delay(1000) // Simulate work
        emit(100 + i) // Sending multiple values
    }
}

```

### **Interview Keywords**

One-shot operation, Suspend function, Emitting, Multiple values, Asynchronous Stream, Collection Scope.

### **Interview Speak Paragraph**

> "The main difference is that a Coroutine is designed for a single asynchronous task that returns a single result, whereas a Flow is designed to handle a stream of multiple values emitted over time. Structurally, Flow is built on top of Coroutines; you need a Coroutine to collect a Flow, but the Flow allows you to keep the communication channel open to receive continuous updates, which a standard suspend function cannot do."

---

**Next Step:** Would you like to explore **The Problem with Iterables/Sequences** (why we don't just use a standard `List` for this), or move straight into **Flow Anatomy**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
