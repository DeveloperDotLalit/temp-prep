---
layout: default
title: "Data Classes"
parent: "Advanced Kotlin: Phase 3   The Kotlin Way"
nav_order: 2
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Data Classes"
parent: "The Kotlin Way (Idiomatic Features)"
nav_order: 2
---

# Data Classes

<!-- Content starts here -->

Here are your interview-focused notes for **Data Classes**.

---

### **Topic: Data Classes**

#### **What It Is**

A **Data Class** is a class whose _main purpose_ is just to hold data.
You declare it by adding the keyword `data` before `class`.

- **Standard Class:** "I am an object that does things."
- **Data Class:** "I am a box that holds information (like a name, ID, or email)."

#### **Why It Exists**

**The Problem (Java Boilerplate):**
In Java, if you wanted a simple `User` class to store a name and age, you had to write 50+ lines of code:

1. Getters and Setters.
2. `toString()` (to print it nicely).
3. `equals()` (to compare if two users are the same).
4. `hashCode()` (to store it in HashMaps).
5. `copy()` (to duplicate it).

**The Kotlin Solution:**
Kotlin says: "If this is just data, why write all that?"
By adding the word `data`, the compiler **automatically generates** all those standard functions for you in the background. It turns 50 lines of Java into 1 line of Kotlin.

#### **How It Works**

1. Write `data class Name(val params...)`.
2. **Constraint:** The Primary Constructor needs at least one parameter.
3. **Constraint:** Parameters must be `val` or `var`.
4. **Bonus Feature:** You get a powerful `copy()` function for free.

#### **Example**

```kotlin
fun main() {
    // 1. Automatic toString()
    val user1 = User("Alice", 25)
    println(user1)
    // Output: User(name=Alice, age=25)
    // (Standard classes would print confusing memory addresses like User@548c4f57)

    // 2. Automatic equals()
    val user2 = User("Alice", 25)
    println(user1 == user2)
    // Output: true
    // (Standard classes would say false because they are different objects in memory)

    // 3. The COPY function (Super useful)
    // "Give me a copy of Alice, but change the age to 26"
    val olderAlice = user1.copy(age = 26)
    println(olderAlice)
}

// THE ONE-LINER MAGIC
data class User(val name: String, val age: Int)

```

#### **Visual Representation**

```text
    Java POJO (Plain Old Java Object)      Kotlin Data Class
    ---------------------------------      -----------------
    - Class definition                     - data class User(...)
    - Constructor
    - Getter()
    - Setter()                             (ALL Generated Automatically)
    - equals()
    - hashCode()
    - toString()
    ---------------------------------
    50 Lines of Code                       1 Line of Code

```

#### **Interview Keywords**

Boilerplate, POJO (Plain Old Java Object), `equals()` and `hashCode()`, `toString()`, `copy()`, ComponentN functions (Destructuring), Immutability.

> **Pro Interview Tip:** If asked "Can a Data Class be abstract or open?", the answer is **No**. Data classes are final. They are meant to be simple data containers, not part of a complex inheritance hierarchy.

#### **Interview Speak Paragraph**

"I exclusively use **Data Classes** for model objects (like API responses or database entities). They save massive amounts of boilerplate code because Kotlin automatically generates `equals()`, `hashCode()`, and `toString()` for me. My favorite feature is the `copy()` method. Since I prefer immutable data (`val`), `copy()` allows me to create a modified version of an object safely without changing the original instance, which is perfect for state management patterns like MVVM or MVI."

---

**Would you like to move on to the next topic: Extension Functions?**
