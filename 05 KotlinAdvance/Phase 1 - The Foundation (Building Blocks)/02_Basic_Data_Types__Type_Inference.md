---
layout: default
title: Basic Data Types & Type Inference
parent: Phase 1   The Foundation (Building Blocks)
nav_order: 2
---

﻿---
layout: default
title: "Basic Data Types & Type Inference"
parent: "The Foundation (Building Blocks)"
nav_order: 2
---

# Basic Data Types & Type Inference

<!-- Content starts here -->

Here are your interview-focused notes for **Basic Data Types & Type Inference**.

---

### **Topic: Basic Data Types & Type Inference**

#### **What It Is**

In programming, every piece of data needs a category (a "Type").

- **Basic Types:** Kotlin uses standard types like `Int` (numbers), `String` (text), `Boolean` (true/false), `Double` (decimals), and `Char` (single characters).
- **Type Inference:** This is Kotlin's "Smart Guessing" ability. You don't always have to tell Kotlin what type a variable is. If you give it a value, Kotlin looks at the value and automatically decides the type for you.

#### **Why It Exists**

In older languages (like Java), you had to be very repetitive:
`String name = "John";` -> You said "String" twice!

Kotlin fixes two things:

1. **Reduces Noise:** It removes the need to state the obvious. If I assign `"John"` to a variable, it is obviously a String.
2. **Uniformity:** In Java, there was a confusing split between "primitives" (`int`, `boolean` - fast but dumb) and "wrappers" (`Integer`, `Boolean` - slow but powerful). In Kotlin, **everything is an object**. You can call methods on numbers (e.g., `10.toString()`).

#### **How It Works**

When you compile your code, Kotlin analyzes the right side of the equals sign (`=`).

- If it sees a number without decimals (e.g., `5`), it assumes `Int`.
- If it sees quotes (e.g., `"Hello"`), it assumes `String`.
- If it sees `true` or `false`, it assumes `Boolean`.

**Crucial Interview Note:** Even though "Everything is an object" in Kotlin code, the compiler secretly converts them back to "primitives" (like raw `int` or `double`) when running on the machine (JVM) whenever possible. This gives you the _convenience_ of objects with the _speed_ of primitives.

#### **Example**

```kotlin
fun main() {
    // 1. Explicit Typing (The "Old School" way)
    // You specifically tell Kotlin: "This is an Integer"
    val age: Int = 25
    val salary: Double = 1000.50
    val isEmployed: Boolean = true

    // 2. Type Inference (The "Kotlin" way)
    // Kotlin looks at "John" and knows it's a String.
    val name = "John"

    // Kotlin looks at 99 and knows it's an Int.
    val score = 99

    // 3. The Limitation (When Inference fails)
    // If you don't give a value immediately, you MUST specify the type.
    // val city // ❌ Error: Type must be specified or assigned.
    val city: String
    city = "New York" // ✅ Allowed because we promised it would be a String later.
}

```

#### **Visual Representation**

```text
    Programmer writes:        Kotlin Compiler sees:
    ------------------        ---------------------
    val x = 10         --->   "10 is an integer, so x is Int"
    val y = "Hi"       --->   "Quotes mean text, so y is String"
    val z = 5.5        --->   "Decimal point means Double"

```

#### **Interview Keywords**

Type Inference, Statically Typed, Everything is an Object, Primitives vs. Wrappers, JVM Bytecode Optimization, Explicit vs. Implicit Typing.

#### **Interview Speak Paragraph**

"Kotlin is a statically typed language, which means types are checked at compile time. However, it uses **Type Inference** to reduce boilerplate code. This allows the compiler to automatically detect the type of a variable based on the value assigned to it, keeping the code clean. Another key feature is that in Kotlin, everything is an object—we don't distinguish between primitives and wrappers in the source code. However, for performance, the Kotlin compiler optimizes these into primitives at the bytecode level whenever possible."

---

**Would you like to move on to the next topic: String Templates?**
