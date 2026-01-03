---
layout: default
title: "Delegation"
parent: "Phase 5: Advanced Topics & Asynchronous Programming"
nav_order: 2
---

﻿---
layout: default
title: "Delegation"
parent: "Advanced Topics & Coroutines"
nav_order: 2
---

# Delegation

<!-- Content starts here -->

Here are your interview-focused notes for **Delegation**.

---

### **Topic: Delegation (`by lazy`, `Observable`)**

#### **What It Is**

**Delegation** is the act of handing off a task to someone else.
In Kotlin, **Property Delegation** means: "I (the variable) do not want to store or calculate my own value. Instead, I will ask a helper object (the Delegate) to handle all `get()` and `set()` logic for me."

You recognize it by the keyword **`by`**.

#### **Why It Exists**

1. **Reduce Boilerplate:** Many properties need similar logic (e.g., "Calculate this only when needed" or "Tell me when this changes"). Instead of writing that logic 100 times, you write it once in a Delegate and reuse it.
2. **Memory Efficiency:** Loading heavy objects (like a Database or huge Image) immediately when the app starts slows everything down. Delegation lets us load them **lazily** (only when asked).

#### **How It Works**

- **`by lazy`**: The most common delegate. It runs the code block **only the first time** you access the variable. It remembers the result and gives you the same result forever after. (Great for heavy initialization).
- **`Delegates.observable`**: Watcher mode. It lets you run code every time a variable's value changes (like a listener).

#### **Example**

```kotlin
import kotlin.properties.Delegates

class User {
    // 1. LAZY DELEGATION (The "Procrastinator")
    // The "heavy" code block is NOT run when User is created.
    // It runs only when I first say "user.database".
    val database: String by lazy {
        println("Connecting to heavy DB...") // Prints once
        "SQL_DB_INSTANCE"
    }

    // 2. OBSERVABLE DELEGATION (The "Watcher")
    // Every time 'status' changes, the block runs automatically.
    var status: String by Delegates.observable("Offline") { prop, old, new ->
        println("Status changed from $old to $new")
    }
}

fun main() {
    val user = User()

    println("App Started")
    // DB code hasn't run yet!

    println(user.database) // First access: Prints "Connecting...", then "SQL..."
    println(user.database) // Second access: Just prints "SQL..." (Cached)

    user.status = "Online" // Output: Status changed from Offline to Online
}

```

#### **Visual Representation**

```text
    Standard Variable:
    [ Variable ] ---> [ Value ] (Holds data directly)

    Delegated Variable (by ...):
    [ Variable ] --(asks)--> [ Delegate Helper ]
                                    |
                                    |-- Logic: "Is this the first time?"
                                    |-- Logic: "Alert listeners!"
                                    |
                             [ Value ] (Managed by Helper)

```

#### **Interview Keywords**

Delegation Pattern, `by` keyword, Lazy Initialization, Thread Safety (Lazy is thread-safe by default), Observer Pattern, Boilerplate reduction.

> **Pro Interview Tip:** "Is `by lazy` thread-safe?"
> **Answer:** "Yes! By default, `lazy` uses `LazyThreadSafetyMode.SYNCHRONIZED`, meaning it is safe to use in a multi-threaded environment. Only one thread can initialize it. If you are sure you are on a single thread (like the Main Thread) and want extra speed, you can turn safety off using `lazy(LazyThreadSafetyMode.NONE)`."

#### **Interview Speak Paragraph**

"I use Kotlin's **Delegation** features to keep my code clean and efficient. My most used delegate is **`by lazy`**, which allows me to defer the initialization of heavy objects (like database instances or complex lists) until they are actually accessed. This improves the app's startup time significantly. I also use **`Delegates.observable`** for simple state monitoring where I need to trigger a log or a UI update immediately after a variable changes, without the overhead of setting up a full reactive stream."

---

**Would you like to move on to the next topic: Coroutines Basics (Scope, Context, Builders)?**
