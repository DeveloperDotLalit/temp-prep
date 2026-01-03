---
layout: default
title: "Flow Basics"
parent: "Phase 5: Advanced Topics & Asynchronous Programming"
nav_order: 6
---

﻿---
layout: default
title: "Flow Basics"
parent: "Advanced Topics & Coroutines"
nav_order: 6
---

# Flow Basics

<!-- Content starts here -->

Here are your interview-focused notes for **Flow (Basics)**. This is the final topic of Phase 5!

---

### **Topic: Flow (Basics)**

#### **What It Is**

**Flow** is a stream of data that comes in **asynchronously** over time.
Think of it like a **Pipe of Water**.

- **Suspend Function:** A "Package Delivery." You wait, and eventually, you get **one** box. Then it's over.
- **Flow:** A "Faucet." You turn it on, and a stream of water (data) flows out continuously. You might get one drop now, another drop in 5 seconds, and a bucketful in 1 minute.

#### **Why It Exists**

**The Limitation of Suspend Functions:**
A `suspend` function can only return **one single value**.
`suspend fun getUser(): User` -> Returns User -> Done.

**The Solution:**
But what if you need to receive:

- Live GPS updates (every second)?
- Download progress (1%, 10%, 50%, 100%)?
- Real-time chat messages?

You need something that can `emit` multiple values over time without blocking the app. That is **Flow**.

#### **How It Works**

Flow has three parts (The Pipe Analogy):

1. **The Producer (`flow { }`):** This creates the pipe and puts data into it using **`emit(value)`**.
2. **The Intermediaries (`map`, `filter`):** You can modify the water while it's in the pipe (e.g., filter out dirty water).
3. **The Consumer (`collect { }`):** The bucket at the end. The water (data) doesn't start moving until someone starts **collecting** it.

**Crucial Concept: Cold Stream**
Flow is **"Cold."** This means the code inside `flow { ... }` does **NOT** run until you call `collect()`. If nobody is listening, the Flow does nothing.

#### **Example**

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun main() = runBlocking {
    println("App Started")

    // 1. CREATE THE FLOW (The Pipe)
    // This code does NOT run yet.
    val countdownFlow = flow {
        for (i in 5 downTo 1) {
            delay(1000) // Pretend we are doing work
            emit(i)     // Put a number in the pipe
        }
    }

    println("Flow created, but waiting...")

    // 2. COLLECT THE FLOW (Turn on the tap)
    // Now the code above starts running.
    countdownFlow.collect { value ->
        println("Countdown: $value")
    }

    println("Liftoff!")
}

```

#### **Visual Representation**

```text
    Suspend Function:
    [ Start ] ------------(Wait)-------------> [ Result ] (One Value)

    Flow:
    [ Start ] --(Wait)--> [ 1 ] --(Wait)--> [ 2 ] --(Wait)--> [ 3 ] ... (Stream)
                          (emit)            (emit)            (emit)

```

#### **Interview Keywords**

Stream, Cold Stream, Emit, Collect, Asynchronous Sequence, Reactive Programming, Backpressure (handled automatically).

> **Pro Interview Tip:** "What is the difference between a `List` and a `Flow`?"
> **Answer:** "A `List` holds all values in memory at once and is calculated immediately. A `Flow` calculates values **lazily** (one by one) and **asynchronously**. A Flow can technically be infinite (like a stock ticker), whereas a List must have a fixed size."

#### **Interview Speak Paragraph**

"I use **Flow** whenever I need to handle a stream of data rather than a single value—for example, tracking download percentages or listening to real-time database updates from Room. Unlike a `suspend` function which returns once, Flow can `emit` multiple values over time. It is a **Cold Stream**, meaning it doesn't consume resources or execute code until a subscriber actually starts `collecting` the data. This makes it extremely efficient for resource management."

---

### **🎉 Phase 5 Complete!**

You have mastered **Advanced Topics**. You know Generics, Delegation, and the Async Trinity (Coroutines, Dispatchers, Flow).

**Ready for the Algorithm Grind?**
Phase 6 is **LeetCode Essentials**. We are going to take your Kotlin knowledge and apply it to solving coding problems efficiently. We will cover Strings, HashMaps, and Windows.

**Shall we start Phase 6 with "Array & String Manipulation"?**
