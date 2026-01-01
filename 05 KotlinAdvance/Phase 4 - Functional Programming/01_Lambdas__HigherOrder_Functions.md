---
layout: default
title: Lambdas & Higher-Order Functions
parent: Phase 4   Functional Programming
nav_order: 1
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Lambdas & Higher-Order Functions"
parent: "Functional Programming & Scoping"
nav_order: 1
---

# Lambdas & Higher-Order Functions

<!-- Content starts here -->

Here are your interview-focused notes for **Phase 4: Functional Programming & Scoping**, starting with the foundation: **Lambdas & High-Order Functions**.

---

### **Topic: Lambdas & High-Order Functions**

#### **What It Is**

- **Lambda:** A "Function with no name." It's a block of code that you can pass around like a variable. Think of it as a sticky note with instructions written on it.
- **High-Order Function:** A function that is the "Manager." It either **takes** a function as a parameter or **returns** a function.

#### **Why It Exists**

**The Problem (Java's "Callback Hell"):**
In older Java (Android), if you wanted to handle a button click, you had to create an entire anonymous class (new `OnClickListener...`). It was verbose and ugly.

**The Kotlin Solution:**
Kotlin treats functions as **"First-Class Citizens."** This means functions are just like numbers or strings. You can store them in variables, pass them into other functions, or return them.
This allows for powerful shortcuts, like running a loop and filtering a list in one line (`list.filter { it > 5 }`).

#### **How It Works**

1. **Lambda Syntax:** `{ inputs -> body }`.
2. **Function Type:** You must tell Kotlin what kind of function you expect. e.g., `(String) -> Unit` means "A function that takes a String and returns nothing."
3. **The "Trailing Lambda" Rule:** If a function is the _last_ parameter, you can move the curly braces `{ }` **outside** the parentheses `( )`. This makes the code look like a native language block (this is the magic behind Jetpack Compose).

#### **Example**

```kotlin
fun main() {
    // 1. Storing a Lambda in a variable
    // Type: Takes Int, Returns Int
    val square: (Int) -> Int = { number -> number * number }

    println(square(5)) // Prints 25

    // 2. High-Order Function
    // We pass our calculator logic INTO the function
    calculate(10, 5, { a, b -> a + b }) // Addition logic
    calculate(10, 5, { a, b -> a * b }) // Multiplication logic

    // 3. Trailing Lambda Syntax (The "Kotlin Style")
    // Because the lambda is the LAST argument, we can remove the ()
    calculate(20, 10) { a, b ->
        a - b
    }
}

// DEFINITION: A function that takes another function as a parameter
// operation: (Int, Int) -> Int
fun calculate(x: Int, y: Int, operation: (Int, Int) -> Int) {
    val result = operation(x, y)
    println("Result is: $result")
}

```

#### **Visual Representation**

```text
    Standard Function Call:
    [ Main ] --(Data: 5)--> [ Function ]

    High-Order Function Call:
    [ Main ] --(Data: 5)------------+
                                    |--> [ Function ]
             --(Logic: x * 2)-------+      |
                                           | executes logic
                                           v
                                        Result: 10

```

#### **Interview Keywords**

Functional Programming, First-Class Citizens, Anonymous Function, Callback, Trailing Lambda Syntax, `it` keyword, Function Type.

> **Pro Interview Tip (The `it` keyword):** If a lambda has **only one parameter**, you don't need to name it (e.g., `name ->`). You can just use the keyword **`it`**.
>
> - `list.filter { name -> name.length > 5 }`
> - `list.filter { it.length > 5 }` (Cleaner!)

#### **Interview Speak Paragraph**

"I use **Lambdas** effectively to write concise code, especially for callbacks and collection operations. Since Kotlin treats functions as first-class citizens, I can pass logic directly into **High-Order Functions**. My favorite feature is the **Trailing Lambda Syntax**—if the last parameter is a function, I can write the lambda block outside the parentheses. This is heavily used in modern frameworks like **Jetpack Compose** and makes the code read much more like natural language."

---

**Would you like to move on to the next topic: Scope Functions (`let`, `run`, `with`, `apply`, `also`)?**
