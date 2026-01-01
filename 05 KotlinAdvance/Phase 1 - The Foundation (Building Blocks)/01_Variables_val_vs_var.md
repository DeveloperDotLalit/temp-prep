---
layout: default
title: Variables: val vs var
parent: Phase 1   The Foundation (Building Blocks)
nav_order: 1
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Variables: val vs var"
parent: "The Foundation (Building Blocks)"
nav_order: 1
---

# Variables: val vs var

<!-- Content starts here -->

Here are your interview-focused notes for **Phase 1: The Foundation**.

---

### **Topic: Variables (`val` vs `var`)**

#### **What It Is**

In Kotlin, whenever you save data (like a name, number, or list), you have to choose between two keywords:

- **`var` (Variable):** This is a standard variable. You can change its value as many times as you want.
- **`val` (Value):** This is a **read-only** variable. Once you assign a value to it, you **cannot** change it. It is permanent for that scope.

Think of `var` like a **Whiteboard**—you can write something, erase it, and write something new.
Think of `val` like a **Permanent Marker**—once you write it, that’s it. You can't change it later.

#### **Why It Exists**

You might ask, _"Why would I ever want a variable I can't change? Isn't flexibility good?"_

Actually, too much flexibility causes bugs.

1. **Predictability:** If you declare something as `val`, you (and your teammates) know with 100% certainty that its value hasn't been secretly changed by some other part of the code 50 lines later.
2. **Thread Safety:** When multiple parts of an app try to access the same data at the same time (multithreading), mutable data (`var`) crashes apps. Read-only data (`val`) is safe because no one can fight over changing it.

Kotlin prefers `val` to help you write "cleaner" code with fewer accidental errors.

#### **How It Works**

When you use `val`, Kotlin marks that specific reference as final. The compiler will literally throw an error (red line) if you try to reassign it.

**The "Gotcha" (Important for Interviews):**
`val` means the **reference** is locked, not necessarily the data inside the object.

- If you have a `val user = User()`, you cannot say `user = NewUser()`.
- BUT, you _can_ typically change the properties inside it, like `user.name = "John"`, unless the object itself is also designed to be immutable.

#### **Example**

```kotlin
fun main() {
    // VAR example: A bank account balance changes
    var myBalance = 100
    println(myBalance) // Prints 100

    myBalance = 50 // ✅ Allowed: We spent money
    println(myBalance) // Prints 50

    // VAL example: Your Date of Birth never changes
    val dateOfBirth = "1990-01-01"
    println(dateOfBirth)

    // dateOfBirth = "2000-01-01"
    // ❌ ERROR: Val cannot be reassigned. Compiler stops you here.

    // THE GOTCHA Example (Deep Dive):
    val shoppingList = mutableListOf("Apples", "Bananas")

    // shoppingList = mutableListOf("Oranges")
    // ❌ ERROR: You cannot point 'shoppingList' to a NEW list.

    shoppingList.add("Oranges")
    // ✅ ALLOWED: You aren't changing the variable reference,
    // you are just modifying the contents of the object it points to.
}

```

#### **Visual Representation**

```text
       VAR (Mutable)                VAL (Read-Only)
    +-----------------+           +-----------------+
    |   myBalance     |           |   dateOfBirth   |
    |      100        |           |  "1990-01-01"   |
    +--------+--------+           +--------+--------+
             |                             |
             v                             X (Blocked)
    [Can point to 50]             [Cannot point to anything else]

```

#### **Interview Keywords**

Immutability, Mutability, Read-only, Reassignment, Final, Thread Safety, Reference Safety.

#### **Interview Speak Paragraph**

>"In Kotlin, `var` is for mutable data that changes over time, while `val` is for read-only references that are assigned once. I always prefer using `val` by default because it enforces immutability, which makes the code more predictable and easier to debug. It prevents accidental reassignment and is much safer when working in multi-threaded environments. I only switch to `var` if I explicitly need the variable to change states."

---

**Would you like to move on to the next topic: Basic Data Types & Type Inference?**
