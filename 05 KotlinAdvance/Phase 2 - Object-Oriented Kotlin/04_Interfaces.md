---
layout: default
title: Interfaces
parent: Phase 2   Object Oriented Kotlin
nav_order: 4
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Interfaces"
parent: "Object-Oriented Kotlin"
nav_order: 4
---

# Interfaces

<!-- Content starts here -->

Here are your interview-focused notes for **Interfaces**.

---

### **Topic: Interfaces**

#### **What It Is**

An **Interface** is a "Contract" or a "Rulebook."
It lists a set of behaviors (functions) but usually doesn't say _how_ they work. It just says, "If you want to be this type of object, you **must** have these functions."

Unlike a Class, an Interface cannot hold state (it can't store value like `val age = 20` directly).

#### **Why It Exists**

1. **Multiple Inheritance (The Main Reason):** In Kotlin (and Java), a class can only have **one** parent (Inheritance). You can't say `class Child : Father, Mother`.

- _But_... a class can implement **many** interfaces. You _can_ say `class SmartPhone : Phone, Camera, MusicPlayer`.

2. **Decoupling:** It lets you write code based on _what something does_ rather than _what it is_.
3. **Default Implementations:** In Kotlin, interfaces are powerful. They can actually contain code (logic) for functions, not just empty definitions. This helps avoid rewriting common code.

#### **How It Works**

1. **Define:** Use the `interface` keyword.
2. **Abstract Methods:** Functions with no body. The class **must** override these.
3. **Default Methods:** Functions _with_ a body. The class **can** override these, or just use the default version.
4. **Implement:** Use the colon `:` (same as inheritance).

#### **Example**

```kotlin
fun main() {
    val myCar = Tesla()
    myCar.startEngine() // Runs code from Tesla class
    myCar.gps()         // Runs default code from Drivable interface
}

// 1. The Contract
interface Drivable {
    // Abstract Method (No body): The class MUST fix this.
    fun startEngine()

    // Default Implementation (Has body): The class CAN use this as is.
    fun gps() {
        println("Locating vehicle...")
    }
}

// 2. The Implementation
// Tesla signs the contract to be "Drivable"
class Tesla : Drivable {

    // We MUST override this because the interface didn't provide code.
    override fun startEngine() {
        println("Silent electric start")
    }

    // We didn't override gps(), so it uses the default one.
}

// 3. Multiple Interfaces (The Superpower)
interface Flyable { fun fly() }

class FlyingCar : Drivable, Flyable {
    override fun startEngine() = println("Engine On")
    override fun fly() = println("Taking off!")
}

```

#### **Visual Representation**

```text
       Interface: Drivable                Interface: Flyable
    +-----------------------+           +--------------------+
    | Needs: startEngine()  |           | Needs: fly()       |
    | Provides: gps()       |           +----------+---------+
    +-----------+-----------+                      |
                |                                  |
                +---------------+------------------+
                                |
                                v
                       Class: FlyingCar
             +-------------------------------------+
             |  MUST write: startEngine()          |
             |  MUST write: fly()                  |
             |  Optional:   gps() (Already exists) |
             +-------------------------------------+

```

#### **Interview Keywords**

Contract, Multiple Inheritance, Default Implementation, Abstract Methods, Decoupling, Polymorphism, State vs Behavior.

#### **Interview Speak Paragraph**

"I use Interfaces to define contracts for behavior. While a class can only inherit from one parent class, it can implement multiple interfaces, which is essential for creating objects with diverse capabilities—like a class being both `Clickable` and `Serializable`. A great feature in Kotlin is that interfaces can have **default implementations**. This allows me to provide standard behavior directly in the interface so implementing classes don't have to rewrite code unless they specifically need to change it."

---

**Would you like to move on to the next topic: Visibility Modifiers?**
