---
layout: default
title: Abstract Classes
parent: Phase 2   Object Oriented Kotlin
nav_order: 6
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Abstract Classes"
parent: "Object-Oriented Kotlin"
nav_order: 6
---

# Abstract Classes

<!-- Content starts here -->

Here are your interview-focused notes for **Abstract Classes**. This is the final topic of Phase 2!

---

### **Topic: Abstract Classes**

#### **What It Is**

An **Abstract Class** is a **"Half-Finished Blueprint."**
It is a class that is not fully built yet. You defined _some_ parts of it (like common logic), but left other parts empty (abstract) because you didn't know how to fill them in yet.

**Crucial Rule:** Because it is half-finished, **you cannot create an object from it directly.** You can't say `val x = AbstractClass()`. You _must_ create a child class that fills in the blanks, and then create an object of that child.

#### **Why It Exists**

1. **Forcing Implementation:** You want to ensure every child class has a specific function (like `calculateArea()`), but you can't write the code in the parent because every shape calculates area differently.
2. **Sharing State:** Unlike Interfaces (which just define rules), Abstract Classes can hold **State** (variables like `color`, `position`, `size`).
3. **The "Is-A" Relationship:** Use this when you want to say "A Dog **IS AN** Animal." (Strong relationship).

#### **How It Works**

1. **`abstract` Keyword:** Use this on the class and any function you want to leave empty.
2. **No Body:** Abstract functions have no curly braces `{ }`.
3. **Inheritance:** Child classes **MUST** override all abstract functions, or the code won't compile.

#### **Example**

```kotlin
fun main() {
    // val shape = Shape()
    // ❌ ERROR: Cannot create an instance of an abstract class.

    val myCircle = Circle(5.0)
    myCircle.displayColor() // Runs shared code from Parent
    myCircle.calculateArea() // Runs specific code from Child
}

// 1. The Half-Finished Blueprint
abstract class Shape(val color: String) {

    // Concrete Method (Fully finished):
    // All shapes share this exact same logic.
    fun displayColor() {
        println("I am $color")
    }

    // Abstract Method (Empty):
    // We know a shape has an area, but we don't know the math yet.
    // The child MUST finish this.
    abstract fun calculateArea()
}

// 2. The Finished Product
class Circle(val radius: Double) : Shape("Red") {

    // We fill in the blank here
    override fun calculateArea() {
        println("Area is ${3.14 * radius * radius}")
    }
}

```

#### **Visual Representation**

```text
       Abstract Class: Shape (The Template)
    +-----------------------------------------+
    |  [State]  Color = "Red"                 |  <-- Can hold data (Unlike Interface)
    |  [Method] displayColor() { Print... }   |  <-- Shared Code
    |  [Method] calculateArea() = ???         |  <-- THE "HOLE" IN THE BLUEPRINT
    +--------------------+--------------------+
                         |
                         v
                Class: Circle (The Fixer)
    +-----------------------------------------+
    |  Inherits Color & displayColor()        |
    |  OVERRIDES calculateArea() { Math... }  |  <-- Fills the hole
    +-----------------------------------------+

```

#### **Interview Keywords**

Abstract vs Interface, Partial Implementation, Cannot Instantiate, Template Method Pattern, Hierarchy, `abstract` keyword.

> **The #1 Interview Question:** _"What is the difference between an Abstract Class and an Interface?"_
>
> - **Abstract Class:** Can hold **State** (variables with values). Can only inherit **one** class. Used for "Is-A" relationships (Dog is an Animal).
> - **Interface:** Cannot hold state. Can implement **many** interfaces. Used for "Can-Do" behaviors (Dog can Move, can Eat).

#### **Interview Speak Paragraph**

"I use Abstract Classes when I have a strong 'Is-A' relationship and need to share **state** (variables) between classes, while still forcing subclasses to implement specific behaviors. For example, a `BaseViewModel` might hold the shared loading state logic, but leave the `fetchData()` function abstract for each specific screen to implement. If I only need to define behavior without sharing state, I prefer Interfaces because they allow for multiple inheritance and are more flexible."

---

### **🎉 Phase 2 Complete!**

You have mastered **Object-Oriented Kotlin**. You know how to structure apps using Classes, handle Inheritance, design Contracts with Interfaces, and secure code with Visibility Modifiers.

**Ready for the "Secret Sauce"?**
Phase 3 is **The Kotlin Way**. This is where we stop writing "Java code in Kotlin" and start using the features that make Kotlin famous (Null Safety, Data Classes, Extensions).

**Shall we start Phase 3 with "Null Safety"?**
