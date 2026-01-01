---
layout: default
title: "Visibility Modifiers"
parent: "Advanced Kotlin: Phase 2   Object Oriented Kotlin"
nav_order: 5
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Visibility Modifiers"
parent: "Object-Oriented Kotlin"
nav_order: 5
---

# Visibility Modifiers

<!-- Content starts here -->

Here are your interview-focused notes for **Visibility Modifiers**.

---

### **Topic: Visibility Modifiers**

#### **What It Is**

Visibility Modifiers are like **Security Clearances** for your code. They determine who is allowed to see and use your variables, functions, or classes.

Kotlin has four levels of security:

1. **`private`**: Top Secret. Only visible inside the specific file or class where it is defined.
2. **`protected`**: Family Only. Visible inside the class and its subclasses (children).
3. **`internal`**: Team Only. Visible anywhere inside the same **Module** (e.g., your specific Gradle project).
4. **`public`**: Open to the World. Visible everywhere. (This is the default if you don't write anything).

#### **Why It Exists**

**Encapsulation (Safety).**
Imagine you are building a `Bank Account` class.

- If you make the `balance` variable **`public`**, any random code in the app can set `balance = 0` or `balance = -1000000`. That's a disaster.
- By making it **`private`**, you force other code to use safe methods (like `deposit()` or `withdraw()`) that check rules before changing the money.
- It hides the "messy details" so other developers only see the clean tools they are supposed to use.

#### **How It Works**

You simply place the keyword before the declaration.

- **`private`**: Restricted to the scope `{ }` it is in.
- **`protected`**: Like private, but children classes can see it too. **Note:** In Kotlin, `protected` does NOT make it visible to the whole package (unlike Java).
- **`internal`**: This is special to Kotlin. It means "Everything in this compiled `.jar` or module can see it." Great for library developers who want to share code between files but hide it from the user of the library.

#### **Example**

```kotlin
open class SuperCar {
    // 1. PUBLIC: Everyone can see the brand
    public val brand = "Ferrari"

    // 2. PRIVATE: Only THIS class knows the engine secret code
    private val engineSecret = "V12-Turbo-X"

    // 3. PROTECTED: Only this class and Subclasses (kids) can use the gearbox
    protected val gearboxType = "Manual"

    // 4. INTERNAL: Only files in this Module (App) can see this
    internal val assemblyLineNumber = 404

    fun testAccess() {
        println(engineSecret) // ✅ Allowed (Inside same class)
    }
}

class BabyFerrari : SuperCar() {
    fun drive() {
        println(brand)       // ✅ Allowed (Public)
        println(gearboxType) // ✅ Allowed (Protected - I am a child)

        // println(engineSecret)
        // ❌ ERROR: Private is for the parent class ONLY.
    }
}

fun mechanic() {
    val car = SuperCar()
    println(car.brand)

    // println(car.gearboxType)
    // ❌ ERROR: Mechanic is not a subclass (Child), so no access.
}

```

#### **Visual Representation**

```text
    Modifier       |  Same Class  |  Subclass  |  Same Module  |  Everywhere
    ---------------|--------------|------------|---------------|------------
    private        |      ✅      |     ❌     |      ❌       |     ❌
    protected      |      ✅      |     ✅     |      ❌       |     ❌
    internal       |      ✅      |     ✅     |      ✅       |     ❌
    public         |      ✅      |     ✅     |      ✅       |     ✅

```

#### **Interview Keywords**

Encapsulation, Access Control, Module-level visibility, Information Hiding, Package-private (doesn't exist in Kotlin).

> **Pro Interview Tip:** If asked "What is the difference between Java's package-private and Kotlin's `internal`?", answer: "Java's default is package-private (visible to the same package). Kotlin doesn't have that. Kotlin uses `internal`, which is visible to the entire **Module**. This is better for modern modularized development."

#### **Interview Speak Paragraph**

"I strictly use visibility modifiers to enforce Encapsulation. My default is always `private` to lock down state as much as possible. I only open things up if absolutely necessary. I frequently use `internal` in multi-module projects to share logic between files within a specific feature module without exposing those implementation details to the rest of the application. I avoid `public` mutable variables to prevent external classes from corrupting the state."

---

**Would you like to move on to the next topic: Abstract Classes?**
