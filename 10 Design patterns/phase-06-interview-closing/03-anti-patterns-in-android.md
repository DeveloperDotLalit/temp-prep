---
layout: default
title: "Anti Patterns in Android"
parent: "Phase 6: Interview Closing and QnA"
nav_order: 3
---

# Anti Patterns in Android

### **Anti-patterns: The "What NOT To Do" Guide**

In medicine, an "anti-pattern" is like a symptom of an underlying disease. In Android, an anti-pattern is a common response to a problem that usually creates **more** problems down the road. Identifying these in an interview shows you have the "scars" of an experienced developer and know how to avoid "technical debt."

---

### **1. Massive ViewModel (The Modern "God Object")**

#### **What It Is**

As we moved away from "Massive Activities" in MVC, many developers simply shifted all that junk into the **ViewModel**. The ViewModel ends up handling networking, database logic, string formatting, and navigation.

- **The Problem:** If a ViewModel is 1,000 lines long, it is just as hard to test and maintain as a God Activity.
- **The Fix:** Use the **Domain Layer (UseCases)**. Move specific business logic into small, reusable classes. A ViewModel should only be a "Coordinator" that holds state and calls UseCases.

---

### **2. Tight Coupling (The "Tangled Headphones" Problem)**

#### **What It Is**

Tight coupling happens when one class knows way too much about the internal details of another class. For example, an `Activity` directly instantiating a `Retrofit` service.

- **The Problem:** If you want to change the API, you have to change the Activity. If you want to test the Activity, you are forced to make real network calls.
- **The Fix:** Use **Dependency Injection (DI)** and **Interfaces**. Talk to "abstractions," not "concrete implementations."

---

### **3. The "Fragile Base Class" (Inheritance Abuse)**

#### **What It Is**

Creating a `BaseActivity` or `BaseViewModel` that contains _everything_ (Analytics, Loading logic, Permissions, Logging).

- **The Problem:** Eventually, you’ll have a screen that _doesn't_ need analytics, but it's forced to inherit it anyway. Changing the Base class risks breaking every single screen in your app.
- **The Fix:** Use **Composition over Inheritance**. Instead of a Base class, create small "Helper" or "Utility" classes and inject them only where they are needed.

---

### **4. Hardcoding Dependencies (Manual Creation)**

#### **What It Is**

Using the `new` keyword (or calling a constructor) inside a class to create its dependencies: `val repo = UserRepository()`.

- **The Problem:** You cannot swap `UserRepository` with a `MockUserRepository` during a unit test. Your code is now "locked" into that specific implementation.
- **The Fix:** Use **Dependency Injection**. Let an external tool (like Hilt) provide the instance.

---

### **5. Context Leaking**

#### **What It Is**

Passing an `Activity Context` into a Singleton, a ViewModel, or a background thread.

- **The Problem:** The Activity is destroyed (e.g., rotation), but the Singleton still holds a reference to it. The Garbage Collector cannot delete the Activity, leading to a **Memory Leak**.
- **The Fix:** Always use `applicationContext` for long-lived objects. Never store a `View` or an `Activity` reference inside a ViewModel.

---

### **6. Logical Flow (Text Diagram)**

```text
[ ANTI-PATTERN ]                      [ THE FIX ]
----------------                      -----------
God Activity/ViewModel  --->  UseCases / Clean Architecture
Tight Coupling          --->  Dependency Injection (Hilt/Dagger)
Deep Inheritance        --->  Composition (Delegates/Helpers)
Hardcoded Data Logic    --->  Repository Pattern (Facade)
Fragmented State        --->  Single Source of Truth (MVI/State)

```

---

### **7. Interview Keywords**

- **Technical Debt:** Code that is easy to write now but expensive to fix later.
- **Spaghetti Code:** Logic that is so tangled it's impossible to follow.
- **Separation of Concerns:** The "cure" for most anti-patterns.
- **Mockability:** The ability to replace a real object with a fake one for testing.
- **Circular Dependency:** When Class A needs Class B, and Class B needs Class A (a sign of poor design).

---

### **8. Interview Speak Paragraph**

> "Identifying anti-patterns is a crucial part of maintaining a healthy Android codebase. One of the most common issues I see today is the **Massive ViewModel**, where the ViewModel takes on too many responsibilities like data fetching and business logic. I address this by applying **Clean Architecture** principles, moving that logic into specialized **UseCases**. Another critical mistake is **Tight Coupling**, which I avoid by using **Dependency Injection** to ensure that my classes depend on abstractions rather than concrete implementations. This not only prevents 'God Objects' but also ensures the app remains highly testable and scalable as the project grows."

---

### **Common Interview "Follow-up" Questions**

**1. "Is a 'BaseActivity' always an anti-pattern?"**

- **Answer:** "Not always. It's okay for very generic UI setup, like setting a Theme or a Toolbar. It becomes an anti-pattern when you start putting **Business Logic** or unrelated features (like GPS tracking) into it. If it does more than one thing, it's starting to become a God Object."

**2. "How do you detect Memory Leaks caused by Context leaking?"**

- **Answer:** "I use tools like **LeakCanary** during development. It monitors the heap and alerts me if an Activity is being held in memory after it should have been destroyed. I also follow the best practice of never passing View or Activity references to ViewModels."

---

### **CONGRATULATIONS! 🎉**

You have officially completed **every single topic** in our comprehensive roadmap!

1. **Phase 1-3:** Creational, Structural, and Behavioral Patterns.
2. **Phase 4:** Architectural Patterns (MVC to MVI).
3. **Phase 5:** Real-world Scenarios.
4. **Phase 6:** Interview Trade-offs and Anti-patterns.

**Final Step:** You are ready for the real deal. Would you like me to generate a **Final Summary Cheat Sheet** that lists every pattern and its "One-Sentence Interview Pitch"? Or would you like to celebrate and finish here?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
