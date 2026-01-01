---
layout: default
title: "Singleton Pattern (object)"
parent: "Advanced Kotlin: Phase 3   The Kotlin Way"
nav_order: 4
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Singleton Pattern (object)"
parent: "The Kotlin Way (Idiomatic Features)"
nav_order: 4
---

# Singleton Pattern (object)

<!-- Content starts here -->

Here are your interview-focused notes for the **Singleton Pattern (`object`)**.

---

### **Topic: Singleton Pattern (`object`)**

#### **What It Is**

A **Singleton** is a class that can have **only one instance** (object) in the entire application. No matter how many times you try to access it, you always get the exact same object.

In Kotlin, you create this using the **`object`** keyword instead of `class`.

- **Class:** A blueprint to make many houses.
- **Object:** The "White House." There is only one. You don't build a new White House every time you want to visit it; you go to the existing one.

#### **Why It Exists**

1. **Shared Resources:** Perfect for things that need to be shared across the whole app, like a **Database Connection**, a **Network Client**, or a **Configuration Manager**.
2. **Memory Efficiency:** Since you only create it once, you save memory.
3. **The Java Headache:** In Java, creating a thread-safe Singleton was a nightmare. You had to write "Double-Checked Locking" logic, private constructors, and static blocks. It was complex and easy to mess up.

- **Kotlin's Fix:** Kotlin handles all that complex thread-safety logic automatically. You just write `object`, and you are done.

#### **How It Works**

1. Replace `class` with `object`.
2. **No Constructors:** You cannot have a constructor `()` because _you_ are not allowed to create it. Kotlin creates it for you the first time you access it.
3. **Direct Access:** You call methods directly on the object name (like a static class).

#### **Example**

```kotlin
fun main() {
    // Usage: We don't say "val db = DatabaseConnection()"
    // We just use the object name directly.

    DatabaseConnection.connect()

    // Accessing properties
    println(DatabaseConnection.url)

    // Changing data
    DatabaseConnection.isConnected = true

    // Proving it's a Singleton:
    // If we access it somewhere else, 'isConnected' will still be true.
    checkStatus()
}

fun checkStatus() {
    println("Status in other function: ${DatabaseConnection.isConnected}")
    // Output: true (Because it's the SAME object)
}

// THE SINGLETON DEFINITION
object DatabaseConnection {
    val url = "https://mydb.com"
    var isConnected = false

    fun connect() {
        println("Connecting to $url...")
    }
}

```

#### **Visual Representation**

```text
       Class (Standard)                  Object (Singleton)
    +-------------------+               +--------------------+
    |      User         |               |  NetworkManager    |
    +-------------------+               +--------------------+
             |                                     ^
       Creates New Copies                          |
      /      |       \                   All parts of the App
   [User1] [User2] [User3]               point to the SAME box
                                         (Screen A) --|
                                         (Screen B) --|

```

#### **Interview Keywords**

Singleton, Global State, Thread Safety, Lazy Initialization, `object` keyword, No Constructor, Static replacement.

> **Pro Interview Tip:** "Is the Kotlin object thread-safe?"
> **Answer:** "Yes! The initialization of an `object` in Kotlin is thread-safe by default. It is created the first time it is accessed (lazily), and the compiler ensures that even if two threads try to access it at the exact same millisecond, only one instance is created."

#### **Interview Speak Paragraph**

"I use the `object` keyword whenever I need a Singleton—a class that should only have a single instance throughout the app's lifecycle, like a `NetworkManager` or `DatabaseHolder`. In Java, implementing a thread-safe singleton required complex boilerplate like double-checked locking. Kotlin simplifies this completely: by using `object`, the compiler guarantees thread safety and lazy initialization automatically. It’s also worth noting that because it’s a singleton, it cannot have a constructor since we don't instantiate it manually."

---

**Would you like to move on to the next topic: Companion Objects?**
