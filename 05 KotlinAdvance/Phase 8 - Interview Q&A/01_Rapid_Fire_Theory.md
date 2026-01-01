---
layout: default
title: Rapid Fire Theory
parent: Advanced Kotlin: Phase 8   Interview Q&A
nav_order: 1
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Rapid Fire Theory"
parent: "Interview Questions & Answers"
nav_order: 1
---

# Rapid Fire Theory

<!-- Content starts here -->

Here are your interview-focused notes for **Phase 8: Interview Questions & Answers**, starting with **Rapid Fire Theory**.

These are designed for the "First 5 Minutes" of the interview. The interviewer will shoot simple questions to check your confidence. **Speed and Clarity** are key here.

---

### **Topic: Rapid Fire Theory (One-Liners)**

#### **What It Is**

A cheat sheet of the most common "What is X?" and "Difference between X and Y?" questions.
**Rule of Thumb:** Do not give a 5-minute speech. Give a 1-sentence definition. Stop. Wait for the next question.

#### **Category 1: Variables & Initialization**

- **`val` vs `var`?**
- "`val` is **read-only** (assigned once), while `var` is **mutable** (can be changed)."

- **`const val` vs `val`?**
- "`const val` is a **compile-time** constant (hardcoded), whereas `val` is calculated at **runtime**."

- **`lateinit` vs `lazy`?**
- "`lateinit` is for **`var`** properties we promise to initialize later (e.g., in `onCreate`). `by lazy` is for **`val`** properties that initialize only when first accessed (memory saving)."

- **Can `lateinit` be used with Int/Boolean?**
- "No, `lateinit` only works with **Reference types** (Objects), not Primitives."

#### **Category 2: Object-Oriented Kotlin**

- **Data Class vs Regular Class?**
- "A Data Class automatically generates `equals()`, `hashCode()`, `toString()`, and `copy()` to reduce boilerplate, while a regular class does not."

- **Open vs Final?**
- "All classes in Kotlin are **Final** (closed) by default. We use the `open` keyword to allow them to be inherited."

- **Abstract Class vs Interface?**
- "Abstract classes can hold **state** (fields with values), while Interfaces cannot hold state (only behavior contracts)."

- **What is a Companion Object?**
- "It is a singleton object inside a class used to hold **static** members (shared by all instances), like constants or factory methods."

#### **Category 3: Functions & Scoping**

- **Extension Function?**
- "It allows us to add new functions to an existing class (like `String` or `View`) without modifying its source code."

- **Higher-Order Function?**
- "A function that accepts another function as a parameter or returns a function."

- **Inline Function?**
- "It instructs the compiler to **copy-paste** the function's code directly to the call site to avoid the memory overhead of creating objects for lambdas."

#### **Category 4: Coroutines & Async**

- **Thread vs Coroutine?**
- "A Thread is an expensive OS resource (1MB RAM), while a Coroutine is a lightweight, user-level task; you can run thousands of coroutines on a single thread."

- **`launch` vs `async`?**
- "`launch` is **'fire-and-forget'** (returns a Job), while `async` performs a computation and **returns a result** (returns a Deferred)."

- **`dispatchers.IO` vs `dispatchers.Default`?**
- "`IO` is optimized for **waiting** (Network/DB), while `Default` is optimized for **CPU work** (Sorting/Math)."

---

#### **Visual Cheat Sheet (Comparison Table)**

| Concept A      | Concept B           | The One-Word Difference |
| -------------- | ------------------- | ----------------------- |
| **`val`**      | **`var`**           | Mutability              |
| **`lateinit`** | **`by lazy`**       | Var vs Val              |
| **`Array`**    | **`List`**          | Fixed vs Flexible       |
| **`==`**       | **`===`**           | Content vs Reference    |
| **`String`**   | **`StringBuilder`** | Immutable vs Mutable    |
| **`Enum`**     | **`Sealed Class`**  | Constant vs State       |

---

#### **Interview Speak Paragraph (How to handle the round)**

"When answering rapid-fire questions, I focus on the **primary differentiator**. For example, if asked about `lateinit` vs `lazy`, I immediately highlight that `lateinit` is for mutable variables initialized later, while `lazy` is for read-only variables initialized on demand. I keep my answers to one or two sentences to demonstrate clear understanding without fluff."

---

**Would you like to move on to the next topic: Deep Dive Explanations (Behavioral + Technical)?**
