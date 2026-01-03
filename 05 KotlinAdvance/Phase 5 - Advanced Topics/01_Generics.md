---
layout: default
title: "Generics"
parent: "Phase 5: Advanced Topics & Asynchronous Programming"
nav_order: 1
---

﻿---
layout: default
title: "Generics"
parent: "Advanced Topics & Coroutines"
nav_order: 1
---

# Generics

<!-- Content starts here -->

Here are your interview-focused notes for **Phase 5: Advanced Topics**, starting with **Generics**.

---

### **Topic: Generics (`<T>`, `in`, `out`)**

#### **What It Is**

**Generics** allow you to write a class or function that can handle **any** data type, rather than being stuck with just one.

Instead of writing `IntBox`, `StringBox`, and `UserBox`, you write one **`Box<T>`**.

- **`<T>`**: Is a placeholder. It stands for "Type." When you use the code, you replace `T` with the actual type (like `String` or `Int`).

#### **Why It Exists**

1. **Code Reuse:** You write the logic once, and it works for everything. (Imagine if you had to write a different `ArrayList` for every single data type!)
2. **Type Safety:** In old Java, we used `Object` to hold anything. But when you took data out, you had to "cast" it manually (`(String) obj`). If you made a mistake, the app crashed.

- Generics fix this by checking the type at **compile time**. If you put an `Int` into a `Box<String>`, the compiler stops you.

#### **How It Works**

1. **Definition:** Add `<T>` after the class or function name.
2. **Usage:** `val box = Box<String>("Hello")`. Now `T` is `String` forever for that specific object.

**The Advanced Part: Variance (`in` and `out`)**

- **`out` (Producer):** Use this when your class **only returns** data (Produces).
- _Rule:_ If `Dog` is an `Animal`, then `List<Dog>` is a `List<Animal>`. (Covariant).

- **`in` (Consumer):** Use this when your class **only takes in** data (Consumes).
- _Rule:_ Opposite direction. (Contravariant).

#### **Example**

```kotlin
fun main() {
    // 1. Basic Generic Class
    val intBox = Box(10)       // T is Int
    val strBox = Box("Hello")  // T is String

    // 2. Generic Function
    printItem(500)
    printItem("World")

    // 3. Variance (out) - "Producer"
    // Because List is defined as List<out T>, we can do this:
    val dogs: List<Dog> = listOf(Dog(), Dog())
    val animals: List<Animal> = dogs
    // ✅ Safe! A list of dogs IS a list of animals (for reading).
}

// A Class that can hold ANYTHING
class Box<T>(val content: T) {
    fun get(): T = content
}

// A Function that can print ANYTHING
fun <T> printItem(item: T) {
    println("Item: $item")
}

open class Animal
class Dog : Animal()

```

#### **Visual Representation**

```text
       Without Generics            With Generics (<T>)
    +------------------+         +-------------------+
    |  IntList         |         |    List<T>        |
    |  StringList      |   --->  |                   |
    |  UserList        |         |  (T becomes Int   |
    +------------------+         |   or String later)|
                                 +-------------------+

    Variance Rule (The "out" keyword):
    If Dog --is--> Animal

    Then:
    List<Dog> --is--> List<Animal>  ( ✅ YES, if using 'out' / Read-Only)
    MutableList<Dog> -/-> MutableList<Animal> ( ❌ NO, dangerous for Writing)

```

#### **Interview Keywords**

Type Parameter, Compile-time Safety, Casting, Variance, Covariance (`out`), Contravariance (`in`), Type Erasure, Reified.

> **Pro Interview Tip (Reified):** "What is Type Erasure?"
> **Answer:** "At runtime, the JVM usually forgets the specific type `T` (it becomes just `Object`). This is called Type Erasure. If I explicitly need to know the type at runtime (e.g., `T::class.java`), I must use an **`inline` function with `reified T**`. This forces the compiler to copy the actual type into the bytecode."

#### **Interview Speak Paragraph**

"I use **Generics** to create reusable, type-safe components. Instead of relying on raw `Object` types and risky casting, Generics allow the compiler to enforce type checks. For example, creating a generic `NetworkResponse<T>` class allows me to wrap any data model. When dealing with inheritance in collections, I pay attention to variance: I use **`out`** (Covariance) when I only need to read data (Producer), which allows a `List<Dog>` to be treated as a `List<Animal>`. I use **`in`** (Contravariance) when I am only consuming data."

---

**Would you like to move on to the next topic: Delegation (`by lazy`, `Observable`)?**
