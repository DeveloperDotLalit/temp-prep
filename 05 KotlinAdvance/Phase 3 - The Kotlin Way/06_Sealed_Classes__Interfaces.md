---
layout: default
title: "Sealed Classes & Interfaces"
parent: "Advanced Kotlin: Phase 3   The Kotlin Way"
nav_order: 6
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Sealed Classes & Interfaces"
parent: "The Kotlin Way (Idiomatic Features)"
nav_order: 6
---

# Sealed Classes & Interfaces

<!-- Content starts here -->

Here are your interview-focused notes for **Sealed Classes & Interfaces**. This is the final (and perhaps most important) topic of Phase 3!

---

### **Topic: Sealed Classes & Interfaces**

#### **What It Is**

A **Sealed Class** is like a "Super-Powered Enum."
It allows you to define a **Restricted Hierarchy**. This means you (the parent class) know exactly who your children are, and **no one else** is allowed to join the family.

- **Enum:** A list of constants. (e.g., `Color.RED`, `Color.BLUE`). All look the same.
- **Sealed Class:** A list of _types_. One child can be a simple object, another can be a complex data class with variables.

#### **Why It Exists**

**The Problem:**
In standard inheritance (using `open`), anyone, anywhere can inherit from your class. The compiler never knows if it has seen _all_ the subclasses.
When you check types using `when`, you always have to add an `else` branch to cover the "unknowns," which is unsafe.

**The Solution:**
With Sealed Classes, the compiler knows **exactly** how many subclasses exist (e.g., 3 specific states).

1. **Safety:** If you handle those 3 states, you **don't need an `else` branch**.
2. **Alerts:** If you add a 4th state later (e.g., "Loading"), the compiler will **break your build** and force you to handle it in your `when` statement. This prevents bugs where you forget to update your UI.

#### **How It Works**

1. Use `sealed class` or `sealed interface`.
2. Define subclasses (usually in the same file).
3. Use a `when` expression to check the state. It will be "Exhaustive" (must cover all cases).

#### **Example: Modern UI State Management (The #1 Use Case)**

This is the standard pattern for Android ViewModels (MVVM/MVI).

```kotlin
fun main() {
    val currentState: UiState = UiState.Success("Data Loaded!")

    renderScreen(currentState)
}

// 1. The Restricted Hierarchy
sealed class UiState {
    // State 1: Simple Object (No data needed)
    object Loading : UiState()

    // State 2: Data Class (Holds the actual data)
    data class Success(val data: String) : UiState()

    // State 3: Data Class (Holds the error info)
    data class Error(val message: String) : UiState()
}

// 2. The Usage
fun renderScreen(state: UiState) {
    // Notice: NO 'else' branch is needed!
    // The compiler knows these are the ONLY 3 possibilities.
    when (state) {
        is UiState.Loading -> showProgressBar()
        is UiState.Success -> showText(state.data)
        is UiState.Error -> showErrorMessage(state.message)
    }
}

fun showProgressBar() = println("Loading...")
fun showText(text: String) = println(text)
fun showErrorMessage(msg: String) = println("Error: $msg")

```

#### **Visual Representation**

```text
       Regular Class (Open)             Sealed Class (Restricted)
    +-----------------------+         +----------------------------+
    |       Animal          |         |         UiState            |
    +----------+------------+         +-------------+--------------+
               |                                    |
      [Dog] [Cat] [Bird] ...              [Loading] [Success] [Error]
               |                                    |
      (Anyone can add [Fish]              (The Gate is CLOSED)
       from another file!)                (No one else enters)

```

#### **Interview Keywords**

Restricted Hierarchy, Exhaustive `when`, State Management, LCE Pattern (Loading-Content-Error), Type Safety, Compile-time check, Enums with State.

> **Pro Interview Tip:** "What is the difference between `Enum` and `Sealed Class`?"
>
> - **Enum:** Each option is a **Constant**. `Color.RED` is just a name. It cannot hold unique data per instance.
> - **Sealed Class:** Each option is a **Class**. `Success(data)` can hold a list, `Error(msg)` can hold a string. They can hold dynamic data.

#### **Interview Speak Paragraph**

"I use **Sealed Classes** extensively for State Management, specifically to model UI states like Loading, Success, and Error. The biggest advantage is that they make `when` expressions **exhaustive**. If I add a new state later, the compiler immediately flags every place in the code where I forgot to handle that new state, which prevents bugs. It's essentially a more powerful version of an Enum that allows each state to hold its own specific data."

---

### **🎉 Phase 3 Complete!**

You have mastered **The Kotlin Way**. You now understand Null Safety, Data Classes, Extensions, Singletons, and Sealed Classes.

**Ready for the "Brain Expanders"?**
Phase 4 is **Functional Programming**. This is where code gets _really_ short and smart. We will cover Lambdas, High-Order Functions, and the 5 Scope Functions (`let`, `apply`, etc.) that confuse everyone.

**Shall we start Phase 4 with "Lambdas & High-Order Functions"?**
