---
layout: default
title: Inheritance & the open Keyword
parent: Phase 2   Object Oriented Kotlin
nav_order: 3
---

﻿---
layout: default
title: "Inheritance & the open Keyword"
parent: "Object-Oriented Kotlin"
nav_order: 3
---

# Inheritance & the open Keyword

<!-- Content starts here -->

Here are your interview-focused notes for **Inheritance & `open` Keyword**.

---

### **Topic: Inheritance & `open` Keyword**

#### **What It Is**

Inheritance is the mechanism where one class (the **Child** or Subclass) acquires the properties and functions of another class (the **Parent** or Superclass). It allows you to build new things on top of what you’ve already built.

- **The Kotlin Twist:** In Java, all classes are "open" (inheritable) by default. In Kotlin, all classes are **`final`** (locked) by default. You cannot inherit from them unless you explicitly unlock them using the **`open`** keyword.

#### **Why It Exists**

1. **Code Reuse:** If you have a `Vehicle` class with code to "move," you don't want to rewrite that code for `Car`, `Truck`, and `Bike`. You just inherit it.
2. **Why "Final by Default"?** This is a specific design choice to prevent the **"Fragile Base Class"** problem. In huge projects, if anyone can inherit from your class and change how it works, they might break your code without knowing it. Kotlin forces you to make a conscious decision: _"I designed this class specifically to be inherited."_

#### **How It Works**

1. **Unlock the Parent:** Add `open` before `class Parent`.
2. **Unlock the Methods:** If you want the child to be able to change a function's behavior (Overriding), you must also mark the function as `open`.
3. **Inherit:** Use the colon `:` to inherit.
4. **Modify:** Use the `override` keyword in the child class to change behavior.

#### **Example**

```kotlin
fun main() {
    val myDog = Dog()
    myDog.eat()       // Inherited from Animal
    myDog.makeSound() // Modified by Dog
}

// 1. The Parent Class (Must be 'open' to be inherited)
open class Animal {
    // A standard function (Child uses it as is)
    fun eat() {
        println("This animal is eating")
    }

    // A modifiable function (Must be 'open' to be overridden)
    open fun makeSound() {
        println("Generic animal sound")
    }
}

// 2. The Child Class (Uses ':' to inherit)
// Note: We must call the Parent's constructor '()' immediately
class Dog : Animal() {

    // 3. Changing Behavior (Must use 'override')
    override fun makeSound() {
        println("Bark! Bark!")
    }
}

// class Cat : Animal() // ✅ Allowed (Animal is open)

// class Robot : Dog()
// ❌ ERROR: Dog is NOT open. It is final by default.
// You cannot inherit from Dog unless you go back and make Dog 'open'.

```

#### **Visual Representation**

```text
       [ Open Class: Animal ]
       |  - eat()            (Final: Cannot be changed)
       |  - makeSound()      (Open:  Can be changed)
       +---------+----------+
                 |
                 v
       [ Class: Dog ]
       |  - eat()            (Uses Parent's code)
       |  - makeSound()      (OVERRIDES with "Bark")
       +---------+----------+
                 |
                 X  <-- Cannot Inherit (Dog is Final)

```

#### **Interview Keywords**

Inheritance, Open vs Final, Method Overriding, Polymorphism, Superclass, Subclass, Fragile Base Class Problem, Extensibility.

#### **Interview Speak Paragraph**

"In Kotlin, classes are `final` by default, meaning they cannot be inherited from unless explicitly marked with the `open` keyword. This is a deliberate design choice to prevent the 'Fragile Base Class' problem, ensuring that developers only allow inheritance when they have designed the class to support it safely. Similarly, functions are also final by default; we must explicitly mark a function as `open` if we want child classes to override it using the `override` keyword."

---

**Would you like to move on to the next topic: Interfaces?**
