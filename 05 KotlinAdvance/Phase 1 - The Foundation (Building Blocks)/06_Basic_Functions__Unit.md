---
layout: default
title: "Basic Functions & Unit"
parent: "Phase 1: The Foundation"
nav_order: 6
---

﻿---
layout: default
title: "Basic Functions & Unit"
parent: "The Foundation (Building Blocks)"
nav_order: 6
---

# Basic Functions & Unit

<!-- Content starts here -->

Here are your interview-focused notes for **Basic Functions**.

---

### **Topic: Basic Functions**

#### **What It Is**

A function is a reusable block of code that performs a specific task. You give it a name, feed it some data (parameters), and it gives you back a result (return value).

- **`fun` keyword:** Used to define a function in Kotlin.
- **`Unit`:** This is Kotlin’s version of `void`. It means "this function does something (like printing text) but doesn't calculate and return a useful data value."

#### **Why It Exists**

1. **DRY Principle (Don't Repeat Yourself):** If you copy-paste the same code 10 times, and then find a bug, you have to fix it in 10 places. With functions, you write it once and call it 10 times. If it breaks, you fix it in one place.
2. **The "Unit" Mystery:** In Java, `void` meant "nothingness." It wasn't a real type. This caused issues in advanced programming (Generics). In Kotlin, `Unit` is an actual real object (a singleton). This makes the language mathematically consistent.

#### **How It Works**

1. Start with `fun`.
2. Name the function (camelCase).
3. Define inputs inside `( )`.
4. Define the output type after a colon `:`. (If you don't write one, Kotlin assumes `: Unit`).

**The Kotlin Special (Single-Expression Functions):**
If your function only has **one line** of code that returns a result, you can delete the `{ }` and the `return` keyword and just use `=`. This is a favorite among Kotlin developers.

#### **Example**

```kotlin
fun main() {
    val result = addNumbers(5, 10)
    println(result) // Prints 15

    greetUser("Alex")
}

// 1. Standard Function (The "Classic" way)
// Takes two Ints, Returns an Int
fun addNumbers(a: Int, b: Int): Int {
    return a + b
}

// 2. Single-Expression Function (The "Pro" way)
// Kotlin infers the return type is Int automatically!
fun multiplyNumbers(a: Int, b: Int) = a * b

// 3. Unit Function (The "Void" way)
// We don't return data, we just DO something (Print)
// ": Unit" is optional here, usually we just leave it out.
fun greetUser(name: String): Unit {
    println("Hello, $name!")
}

```

#### **Visual Representation**

```text
       Input (Parameters)        The Function Machine          Output (Return Type)
    +---------------------+    +----------------------+    +-----------------------+
    |  Eggs, Flour, Milk  | -> |  makePancakes()      | -> |      Pancake          |
    +---------------------+    +----------------------+    +-----------------------+


       Input (Parameters)        The "Unit" Machine            Output (Side Effect)
    +---------------------+    +----------------------+    +-----------------------+
    |     "Hello"         | -> |  printMessage()      | -> |  (Standard Output)    |
    +---------------------+    +----------------------+    |  Returns: Unit Object |
                                                           +-----------------------+

```

#### **Interview Keywords**

DRY Principle, Single Expression Syntax, Unit vs Void, Type Inference, Parameters, Arguments, Return Type.

#### **Interview Speak Paragraph**

"In Kotlin, functions are defined using the `fun` keyword. What I really like is the **Single-Expression Syntax**—if a function just calculates one thing, I can remove the curly braces and `return` keyword to make it a one-liner. Also, Kotlin uses `Unit` instead of `void`. Unlike `void`, `Unit` is a real object, which allows functions that return 'nothing' to still be treated consistently when working with generics or advanced functional programming patterns."

---

**Would you like to move on to the next topic: Default & Named Arguments?**
