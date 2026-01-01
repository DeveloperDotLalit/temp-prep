---
layout: default
title: Classes & Objects
parent: Advanced Kotlin: Phase 2   Object Oriented Kotlin
nav_order: 1
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Classes & Objects"
parent: "Object-Oriented Kotlin"
nav_order: 1
---

# Classes & Objects

<!-- Content starts here -->

Here are your interview-focused notes for **Phase 2: Object-Oriented Kotlin**, starting with the core concept: **Classes & Objects**.

---

### **Topic: Classes & Objects**

#### **What It Is**

- **Class:** Think of a **Class** as a **Blueprint** or a Template. It describes what something _should_ look like and do, but it doesn't exist in the real world yet.
- **Object:** Think of an **Object** as the **actual thing** built from that blueprint. This is also called an "Instance."

**Analogy:**

- **Class:** The architect's drawing of a house (Paper). You can't live in the drawing.
- **Object:** The actual physical house (Bricks). You can live in it. You can build 50 houses (Objects) from one drawing (Class).

#### **Why It Exists**

In programming, we need to group related data and behavior together.
If you are building a "Music Player" app, you don't want scattered variables like `songName1`, `songDuration1`, `songName2`.
You want a **Song** container that holds `name` and `duration` together. Classes allow you to create these custom containers.

#### **How It Works**

1. **Define:** Use the `class` keyword.
2. **Properties:** Variables inside the class (Data).
3. **Methods:** Functions inside the class (Behavior).
4. **Create (Instantiate):** **Crucial Kotlin Difference:** We **DO NOT** use the `new` keyword (unlike Java/C++). We just call the class name like a function.

#### **Example**

```kotlin
fun main() {
    // 2. Create Objects (Instantiation)
    // Notice: NO 'new' keyword!
    val myCar = Car()
    val yourCar = Car()

    // 3. Use the Objects
    myCar.brand = "Tesla"
    myCar.drive()

    yourCar.brand = "Toyota"
    yourCar.drive()
}

// 1. Define the Class (The Blueprint)
class Car {
    // Properties (State/Data)
    var brand: String = "Unknown"
    var speed: Int = 0

    // Methods (Behavior/Actions)
    fun drive() {
        println("$brand is moving at $speed mph")
    }
}

```

#### **Visual Representation**

```text
       The Class (Blueprint)                 The Objects (Instances)
    +-------------------------+            +-------------------------+
    |      Class Car          |   ---->    |  Object: myCar          |
    |  - brand                |            |  - brand: "Tesla"       |
    |  - speed                |            |  - speed: 0             |
    |  - drive()              |            +-------------------------+
    +-------------------------+
                                           +-------------------------+
                                  ---->    |  Object: yourCar        |
                                           |  - brand: "Toyota"      |
                                           |  - speed: 0             |
                                           +-------------------------+

```

#### **Interview Keywords**

Class, Object, Instance, Instantiation, Properties, Methods, State and Behavior, No `new` keyword.

#### **Interview Speak Paragraph**

"In Kotlin, a Class serves as a blueprint for creating Objects. It encapsulates properties (state) and methods (behavior) into a single unit. A distinct feature of Kotlin compared to Java is that we don't use the `new` keyword to instantiate a class; we simply call the constructor like a regular function. This simplifies the syntax and makes the code cleaner."

---

**Would you like to move on to the next topic: Constructors (Primary vs. Secondary)?**
