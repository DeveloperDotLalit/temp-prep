---
layout: default
title: "Constructors: Primary vs Secondary"
parent: "Advanced Kotlin: Phase 2   Object Oriented Kotlin"
nav_order: 2
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Constructors: Primary vs Secondary"
parent: "Object-Oriented Kotlin"
nav_order: 2
---

# Constructors: Primary vs Secondary

<!-- Content starts here -->

Here are your interview-focused notes for **Constructors (Primary vs. Secondary)**.

---

### **Topic: Constructors (Primary vs. Secondary) & `init` Blocks**

#### **What It Is**

A **Constructor** is the specific function that runs the moment you create an object. It’s like the setup wizard that runs when you install software—it gets everything ready before you start using it.

Kotlin has two types:

1. **Primary Constructor:** The main, concise way to initialize a class. It lives right in the class header (next to the class name).
2. **Secondary Constructor:** Alternative ways to initialize a class (like the "old Java way"). They live inside the class body.
3. **`init` Block:** Since the Primary Constructor is just a header (no body), you can't put code logic like `print()` or `if()` there. The `init` block is where you put that startup logic.

#### **Why It Exists**

**The Problem (Java):**
In Java, defining a class and assigning variables was repetitive.

```java
// Java bloat
class User {
    String name;
    User(String name) { // Constructor
        this.name = name; // Repetitive assignment
    }
}

```

**The Kotlin Solution:**
Kotlin wants to reduce boilerplate.

1. **Primary:** Allows you to declare variables and assign them in **one line**.
2. **Secondary:** Exists mostly for compatibility with Java or specific complex setup scenarios, but honestly? **We rarely use them.** We usually use _Default Arguments_ instead (from Phase 1).

#### **How It Works**

1. **Primary Constructor:** Defined in the class signature: `class User(val name: String)`. This automatically creates a property `name` and assigns the value passed in.
2. **`init` Block:** Runs immediately after the Primary Constructor. Used for validation (e.g., checking if the name is not empty).
3. **Secondary Constructor:** Uses the keyword `constructor`. **Rule:** If you have a Primary constructor, every Secondary constructor **must** call the Primary one (using `: this(...)`).

#### **Example**

```kotlin
fun main() {
    // Uses Primary Constructor
    val user1 = User("Alice")

    // Uses Secondary Constructor
    val user2 = User("Bob", 25)
}

// 1. PRIMARY CONSTRUCTOR (In the header)
// This effectively says: "I have a property 'name', please set it."
class User(val name: String) {

    var age: Int = 0

    // 2. INIT BLOCK (Startup Logic)
    // The primary constructor has no body, so we do checks here.
    init {
        println("New user created: $name")
        if (name.isBlank()) {
            throw IllegalArgumentException("Name cannot be empty!")
        }
    }

    // 3. SECONDARY CONSTRUCTOR (The Alternative)
    // Needs 'constructor' keyword.
    // MUST call the primary constructor using ": this(name)"
    constructor(name: String, age: Int) : this(name) {
        this.age = age
        println("Secondary constructor used. Age set to $age")
    }
}

```

#### **Visual Representation**

```text
       Class Definition
    +------------------------------------------------+
    | class Robot(val name: String)                  | <-- Primary (The VIP Entrance)
    |   ^                                            |
    |   |--[Variables Created Here]                  |
    |                                                |
    | {                                              |
    |    init {                                      |
    |       // Logic runs here (Checking oil...)     | <-- Init Block (The Engine Start)
    |    }                                           |
    |                                                |
    |    constructor(name, color) : this(name) {     | <-- Secondary (The Side Door)
    |       // Extra logic                           |     (Must knock on VIP door first)
    |    }                                           |
    +------------------------------------------------+

```

#### **Interview Keywords**

Primary Constructor, Secondary Constructor, Init Block, Initializer, Delegation (`this`), Boilerplate reduction, Property Declaration.

#### **Interview Speak Paragraph**

"In Kotlin, I almost always use the **Primary Constructor** because it allows me to declare and initialize properties in a single line, keeping the code clean. If I need to run validation logic during initialization—like checking if a string is empty—I put that code inside an **`init` block**, since the primary constructor acts as a header. While Kotlin supports **Secondary Constructors**, I rarely use them. Instead, I prefer using **Default Arguments** in the primary constructor to handle different initialization scenarios, as it's more idiomatic and readable."

---

**Would you like to move on to the next topic: Inheritance & `open` keyword?**
