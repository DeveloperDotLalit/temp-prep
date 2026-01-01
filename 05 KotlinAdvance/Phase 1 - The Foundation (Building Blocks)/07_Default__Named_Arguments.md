---
layout: default
title: Default & Named Arguments
parent: Phase 1   The Foundation (Building Blocks)
nav_order: 7
---

﻿---
layout: default
title: "Default & Named Arguments"
parent: "The Foundation (Building Blocks)"
nav_order: 7
---

# Default & Named Arguments

<!-- Content starts here -->

Here are your interview-focused notes for **Default & Named Arguments**. This is the final topic of Phase 1!

---

### **Topic: Default & Named Arguments**

#### **What It Is**

- **Default Arguments:** You can give a function parameter a "backup plan." If the caller doesn't provide a value for that parameter, the function uses the default one you set.
- **Named Arguments:** When calling a function, you can explicitly say which parameter is which by name (e.g., `width = 10`), rather than just hoping you put the numbers in the correct order.

#### **Why It Exists**

**The Problem (Java's "Overloading Hell"):**
In older languages, if you wanted a function to be flexible (e.g., creating a user with just a name, OR a name + age, OR a name + age + phone), you had to write **three different functions**.
This is called the **"Telescoping Constructor"** pattern, and it creates a lot of messy, repetitive code.

**The Solution:**
Kotlin lets you write **one single function** that handles all those scenarios.
Plus, Named Arguments solve the "Mystery Number" problem.

- _Bad code:_ `resize(100, 200, true)` -> What do these numbers mean? Width? Height? Or X, Y?
- _Good code:_ `resize(width = 100, height = 200, animate = true)` -> Crystal clear.

#### **How It Works**

1. **Define Defaults:** Use `=` after the type in the function definition.
2. **Call with Names:** Use `parameterName = value` when calling the function. You can even change the order of arguments!

#### **Example**

```kotlin
fun main() {
    // 1. Using Defaults
    // We only pass the name. 'isPremium' defaults to false.
    createUser("Alice")

    // 2. Overriding Defaults
    // We pass both, so the default is ignored.
    createUser("Bob", true)

    // 3. Named Arguments (Clarity & Skipping)
    // We want to set the age, but keep 'isPremium' as default.
    // We MUST use names here to skip the middle parameter.
    createUser("Charlie", age = 30)

    // 4. Mixing Order (Chaos Mode - but allowed!)
    createUser(age = 25, isPremium = true, name = "Dave")
}

// One function replaces 3 or 4 Java Overloads
fun createUser(
    name: String,
    isPremium: Boolean = false, // Default value
    age: Int = 18               // Default value
) {
    println("User: $name, Premium: $isPremium, Age: $age")
}

```

#### **Visual Representation**

```text
    Java Way (Telescoping):
    -----------------------
    func(A) { ... }
    func(A, B) { ... }
    func(A, B, C) { ... }  <-- So much duplicate code!

    Kotlin Way (Defaults):
    ----------------------
    func(A, B=Default, C=Default) { ... }

    // Usage:
    func(A)       -> Uses defaults for B & C
    func(A, B)    -> Uses default for C
    func(A, C=5)  -> Uses default for B, sets C manually

```

#### **Interview Keywords**

Method Overloading, Boilerplate, Telescoping Constructor Pattern, Readability, Builder Pattern alternative, `@JvmOverloads`.

> **Pro Interview Tip (`@JvmOverloads`):** If an interviewer asks "How do you use Kotlin default arguments in Java?", the answer is: "Java doesn't understand Kotlin defaults. We must annotate the Kotlin function with `@JvmOverloads`, which tells the compiler to secretly generate all those multiple Java overload methods for us."

#### **Interview Speak Paragraph**

"I love Default Arguments because they eliminate the need for 'Method Overloading' or the 'Builder Pattern' for simple objects. Instead of writing five different constructors, I write one with default values. I also use Named Arguments heavily in code reviews. It makes the code self-documenting—seeing `resize(width = 100, height = 200)` is infinitely safer and clearer than just seeing `resize(100, 200)`, where you might accidentally swap the values."

---

### **🎉 Phase 1 Complete!**

You have mastered the **Foundation**. You now understand immutability, type inference, templates, control flow, loops, and flexible functions.

**Ready for the big shift?**
Phase 2 is **Object-Oriented Kotlin**. This is where we learn how Kotlin structures code differently from Java (Classes, Inheritance, and Interfaces).

**Shall we start Phase 2 with "Classes & Objects"?**
