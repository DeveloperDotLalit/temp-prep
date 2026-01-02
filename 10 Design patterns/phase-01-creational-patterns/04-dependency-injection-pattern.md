---
layout: default
title: "Dependency Injection Pattern"
parent: "Phase 1: Creational Patterns"
nav_order: 4
---

# Dependency Injection Pattern

### **Dependency Injection (DI): The "DoorDash" Pattern**

In the real world, if you want a burger, you don't go to the farm, raise a cow, harvest wheat, and build a kitchen. You use an app (like DoorDash) to **inject** the burger into your house. You are the "object," and the burger is your "dependency." You don't care _how_ the burger was made; you just need it to do your job (eat).

---

### **1. What It Is**

**Dependency Injection** is a design pattern where an object does not create the other objects it needs (its dependencies). Instead, those dependencies are "injected" into it—usually through a constructor or a property.

- **Dependency:** If Class A uses a method of Class B, then Class A "depends" on Class B.
- **Injection:** Passing Class B into Class A from the outside.

---

### **2. Why It Exists (The Problem it Solves)**

Imagine a `UserRepository` that needs a `Database` and a `NetworkClient`.

- **The Problem (Hard Coding):** If you create the `Database` inside the `UserRepository` constructor, they are "tightly coupled." If you want to change the database for a test or a different version of the app, you have to rewrite the `UserRepository` code. It’s like a house where the fridge is welded to the floor—you can’t swap it out without breaking the kitchen.
- **The Solution:** You pass the `Database` into the `UserRepository`. Now the repository doesn't care _which_ database it gets, as long as it works. This makes your code "loosely coupled" and incredibly easy to test.

**Key Benefits:**

- **Reusability:** You can use the same class with different configurations.
- **Testing:** You can inject a "Fake/Mock" database during unit tests.
- **Scalability:** Managing hundreds of objects becomes easier when a central "Provider" handles their creation.

---

### **3. How It Works**

There are three main ways to inject dependencies:

1. **Constructor Injection:** Passing dependencies through the constructor (Most common and recommended).
2. **Field (Property) Injection:** Setting the dependency directly on a variable (Common in Android Activities where you can't use constructors).
3. **Method Injection:** Passing a dependency as a parameter to a specific function.

---

### **4. Example (Practical Android/Kotlin)**

#### **Without DI (The "Bad" Way)**

The `Car` is responsible for creating its own `Engine`. If we want an `ElectricEngine`, we have to change the `Car` class.

```kotlin
class Engine {
    fun start() = println("Engine started!")
}

class Car {
    private val engine = Engine() // Hardcoded! Tight coupling.

    fun drive() {
        engine.start()
        println("Car is moving")
    }
}

```

#### **With DI (The "Professional" Way)**

The `Car` just asks for _an_ engine. It doesn't care who makes it.

```kotlin
class Engine {
    fun start() = println("Engine started!")
}

// The Car receives its engine from the outside
class Car(private val engine: Engine) {
    fun drive() {
        engine.start()
        println("Car is moving")
    }
}

// --- HOW IT LOOKS IN ACTION ---
fun main() {
    val myEngine = Engine()

    // We "inject" the engine here
    val myCar = Car(myEngine)
    myCar.drive()
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
[ Manual Way ]
Activity --> creates --> ViewModel --> creates --> Repository --> creates --> Retrofit
(If Retrofit changes, you might have to change everything up the chain!)

[ DI Way ]
[ Central Provider/Hilt ]
      |
      +------> gives Retrofit to Repository
      |
      +------> gives Repository to ViewModel
      |
      +------> gives ViewModel to Activity

```

---

### **6. Interview Keywords**

- **Inversion of Control (IoC):** The shift of responsibility for object creation from the class to a container/framework.
- **Tight vs. Loose Coupling:** How much classes depend on each other's internal details.
- **Boilerplate Code:** The "manual" code written to connect objects (which libraries like Hilt reduce).
- **Mocking:** Replacing real dependencies with fake ones for testing.
- **Constructor Injection:** The preferred way to provide dependencies in Kotlin.

---

### **7. Interview Speak Paragraph**

> "Dependency Injection is a design pattern where a class receives its dependencies from an external source rather than creating them internally. This promotes loose coupling and makes the code significantly more maintainable and testable. In Android, while we often use libraries like Hilt or Dagger to automate this, the core concept is simply about 'passing things in.' By injecting dependencies—usually via the constructor—we can easily swap implementations, such as providing a mock database for unit tests or a specific network configuration for different build flavors, without ever touching the logic inside the class itself."

---

### **Interview "Pro-Tip" (The Library Question)**

Interviewer might ask: **"Is Hilt a design pattern?"**

- **Your Answer:** "No, Hilt is a **library** that _implements_ the Dependency Injection pattern. DI is the concept of passing dependencies; Hilt is just a tool that automates that process for us in Android so we don't have to write 'Manual DI' (boilerplate) in every Factory or Activity."

---

**This completes Phase 1: Creational Patterns!** Would you like to move on to **Phase 2: Structural Patterns** (starting with the **Adapter Pattern**), or would you like to do a quick "Phase 1 Review" first?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
