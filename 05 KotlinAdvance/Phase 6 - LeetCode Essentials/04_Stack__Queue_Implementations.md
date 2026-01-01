---
layout: default
title: Stack & Queue Implementations
parent: Phase 6   Leetcode Essentials
nav_order: 4
---

﻿---
layout: default
title: "Stack & Queue Implementations"
parent: "LeetCode Essentials (Kotlin)"
nav_order: 4
---

# Stack & Queue Implementations

<!-- Content starts here -->

Here are your interview-focused notes for **Stack & Queue Implementations**.

---

### **Topic: Stack & Queue Implementations (`ArrayDeque`)**

#### **What It Is**

- **Stack (LIFO):** Last In, First Out. Like a stack of plates. You put the last plate on top, and you must take that same plate off first.
- **Queue (FIFO):** First In, First Out. Like a line at a movie theater. The first person in line gets served first.
- **`ArrayDeque`:** In Kotlin (and Java), we don't use the old `Stack` class or `LinkedList` for these anymore. We use **`ArrayDeque`** (Double-Ended Queue). It can act as **both** a Stack and a Queue, and it is highly optimized.

#### **Why It Exists**

**The "Old" Way:**

- **`Stack` Class:** This is a legacy Java class. It is "synchronized" (thread-safe), which makes it slow for standard algorithmic problems.
- **`LinkedList`:** Every item is wrapped in a "Node" object with pointers to next/previous. This creates a lot of memory overhead.

**The Solution (`ArrayDeque`):**

- It uses a resizeable array internally (no Node objects).
- It is faster than `Stack` and `LinkedList` for adding/removing from ends.
- It is the industry standard for LeetCode in Kotlin/Java.

#### **How It Works**

- **As a Stack:** Use `addLast()` (push) and `removeLast()` (pop).
- **As a Queue:** Use `addLast()` (enqueue) and `removeFirst()` (dequeue).

#### **Example**

```kotlin
import java.util.ArrayDeque

fun main() {
    // 1. IMPLEMENTING A STACK (LIFO)
    // "Last in, First out"
    val stack = ArrayDeque<Int>()

    stack.addLast(10) // Push
    stack.addLast(20) // Push
    stack.addLast(30) // Push

    // Peek (Look at top without removing)
    println(stack.peekLast()) // Output: 30

    // Pop (Remove from top)
    println(stack.removeLast()) // Output: 30
    println(stack.removeLast()) // Output: 20


    // 2. IMPLEMENTING A QUEUE (FIFO)
    // "First in, First out"
    val queue = ArrayDeque<String>()

    queue.addLast("Alice") // Enqueue
    queue.addLast("Bob")   // Enqueue

    // Peek (Look at front)
    println(queue.peekFirst()) // Output: Alice

    // Dequeue (Remove from front)
    println(queue.removeFirst()) // Output: Alice
    println(queue.removeFirst()) // Output: Bob
}

```

#### **Visual Representation**

```text
    Stack (LIFO) - Vertical
    |  30  |  <-- In / Out (Top)
    |  20  |
    |  10  |
    +------+

    Queue (FIFO) - Horizontal
    (Out) <--- [ Alice ] [ Bob ] [ Charlie ] <--- (In)

```

#### **Interview Keywords**

LIFO, FIFO, Deque (Double Ended Queue), Vector (Legacy), Synchronized Overhead, ArrayDeque vs LinkedList, Thread Safety.

> **Pro Interview Tip:** "Why not use `Stack<T>`?"
> **Answer:** "The `Stack` class in Java is a legacy class based on `Vector`. It is synchronized, which adds unnecessary performance overhead for single-threaded tasks like competitive programming. `ArrayDeque` is faster and more cache-friendly."

#### **Interview Speak Paragraph**

"For both Stack and Queue implementations, I exclusively use **`ArrayDeque`**. It outperforms the legacy `Stack` class because it isn't synchronized, and it beats `LinkedList` because it uses array-based storage, which reduces memory overhead from node pointers. I use `addLast()` and `removeLast()` to use it as a Stack, and `addLast()` with `removeFirst()` to use it as a Queue. It provides amortized constant time () for insertions and deletions at both ends."

---

**Would you like to move on to the next topic: Sorting & Comparators?**
