---
layout: default
title: "Companion Objects"
parent: "Phase 3: The Kotlin Way"
nav_order: 5
---

﻿---
layout: default
title: "Companion Objects"
parent: "The Kotlin Way (Idiomatic Features)"
nav_order: 5
---

# Companion Objects

<!-- Content starts here -->

Here are your interview-focused notes for **Companion Objects**.

---

### **Topic: Companion Objects**

#### **What It Is**

A **Companion Object** is a specific object that is tied to a **Class** rather than an **Instance** of that class.

Think of a Class like a **Hotel**.

- **Instances:** The individual **Rooms**. To watch TV, you need to be inside a specific room (Instance).
- **Companion Object:** The **Reception Desk**. You don't need to book a room to talk to the receptionist. The desk belongs to the Hotel itself, not to any specific room.

In Kotlin, this is where we put things that should be shared by _everyone_, like constants or helper functions.

#### **Why It Exists**

**The "Missing Static" Shock:**
If you come from Java, you will look for the `static` keyword. **Kotlin does not have `static`.**
Kotlin believes "Everything should be an Object."

- Java's `static` is not an object; it's just a floating piece of data.
- Kotlin's **Companion Object** _is_ a real object (a singleton nested inside the class). Because it's a real object, it can do things Java statics can't—like implementing Interfaces or being passed around as a variable.

#### **How It Works**

1. Inside your class, add a block labeled `companion object`.
2. Put variables/functions inside it.
3. **Access:** You call them using `ClassName.Function()`. You **do not** need to create an instance (`ClassName()`) first.

**Common Use Case:** **Factory Methods.**
Sometimes constructors are too simple. You want complex logic to create an object. You put that logic in the Companion Object.

#### **Example**

```kotlin
fun main() {
    // 1. Accessing a Constant (Like Java static final)
    println(User.MAX_AGE)

    // 2. Using a Factory Method
    // We don't say "User()", we ask the Companion to create one for us.
    val guest = User.createGuest()
    println(guest.name)

    // 3. Normal Instance Method
    // guest.MAX_AGE // ❌ Error: This belongs to the Class, not the object.
}

class User(val name: String, val age: Int) {

    // Regular method (Needs a specific user to run)
    fun printInfo() {
        println("User: $name")
    }

    // THE COMPANION OBJECT (The "Static" Section)
    companion object {
        const val MAX_AGE = 100

        // Factory Method: A smart way to create objects
        fun createGuest(): User {
            return User("Guest", 0)
        }
    }
}

```

#### **Visual Representation**

```text
       Class: User
    +-----------------------------------------------+
    |                                               |
    |   [ Companion Object ] (The Reception Desk)   |
    |   +---------------------------------------+   |
    |   |  MAX_AGE = 100                        |   |  <-- Shared by all
    |   |  createGuest()                        |   |
    |   +---------------------------------------+   |
    |                                               |
    |   [ Instance: User A ]   [ Instance: User B ] |
    |   | name: "Alice"    |   | name: "Bob"      | |  <-- Separate Data
    |   +------------------+   +------------------+ |
    +-----------------------------------------------+

```

#### **Interview Keywords**

Static replacement, Factory Pattern, Shared State, Singleton (scoped), `@JvmStatic`, `const val`.

> **Pro Interview Tip (`@JvmStatic`):** If you are working in a project with both Java and Kotlin, Java cannot see Companion Objects easily. You must add the annotation `@JvmStatic` to your functions inside the companion object so Java can call them like `User.createGuest()` instead of `User.Companion.createGuest()`.

#### **Interview Speak Paragraph**

"Since Kotlin doesn't have the `static` keyword, I use **Companion Objects** to hold members that are tied to the class itself rather than a specific instance. This is where I put constants (like `TAG` for logging) or **Factory Methods** to handle complex object creation logic. A big advantage of Companion Objects over Java statics is that they are real objects—meaning they can implement interfaces or be assigned to variables, giving us much more flexibility in how we structure our architecture."

---

**Would you like to move on to the next topic: Sealed Classes & Interfaces?**
