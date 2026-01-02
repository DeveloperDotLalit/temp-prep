---
layout: default
title: "Design Patterns in Android"
nav_order: 11
has_children: true
---

# Design Patterns in Android

An interview-focused guide to **writing architecturally sound Android applications**  
using proven **Design Patterns** with Kotlin and modern Android APIs.

Hello! It’s great to meet you. I'm excited to act as your personal thought partner and mentor for mastering **Design Patterns in Android**.

Since you are an experienced Kotlin developer, we’re going to bridge the gap between "writing code that works" and "writing code that is architecturally sound." We will break these patterns down so you can explain not just _how_ to use them, but _why_ they are the better choice during a high-stakes interview.

Here is your comprehensive, phase-wise roadmap to becoming an expert in Android Design Patterns.

---

## **Phase 1: The Creational Patterns (The "How to Build It" Phase)**

_Focus: Managing object creation to make your code flexible and reusable._

- **Singleton Pattern:** Ensures a class has only one instance (e.g., Database or Network clients) and provides a global point of access.
- **Factory Pattern:** Hides the complexity of object creation by using a specialized "factory" class to decide which object to instantiate.
- **Builder Pattern:** A step-by-step approach to creating complex objects (like building a `Notification` or a `Retrofit` instance) without messy constructors.
- **Dependency Injection (DI):** Not just a library (Hilt/Dagger), but a pattern where objects receive their dependencies rather than creating them.

## **Phase 2: The Structural Patterns (The "How to Organize It" Phase)**

_Focus: How classes and objects compose together to form larger structures._

- **Adapter Pattern:** Acts as a bridge between two incompatible interfaces (crucial for `RecyclerView` and `ViewHolders`).
- **Facade Pattern:** Providing a simplified interface to a complex subsystem (e.g., a `Repository` hiding the complexity of local DB and remote API).
- **Proxy Pattern:** Using a placeholder object to control access to another object (common in heavy resource loading).
- **Composite Pattern:** Treating a group of objects the same way as a single instance (how the Android `View` and `ViewGroup` hierarchy works).

## **Phase 3: The Behavioral Patterns (The "How They Talk" Phase)**

_Focus: Improving communication between different parts of your app._

- **Observer Pattern:** The backbone of "Reactive" programming where one object notifies many others about state changes (e.g., `LiveData`, `Flow`).
- **Strategy Pattern:** Swapping out an algorithm or behavior at runtime (e.g., switching between different payment methods or sorting logic).
- **Command Pattern:** Encapsulating a request as an object, letting you parameterize actions (useful for "Undo" functionality or WorkManager tasks).
- **State Pattern:** Allowing an object to change its behavior when its internal state changes (perfect for managing UI Loading/Success/Error states).

## **Phase 4: Architectural Patterns (The "Big Picture" Phase)**

_Focus: High-level organization of the entire application._

- **MVC (Model-View-Controller):** Understanding the classic approach and why it often leads to "God Activities" in Android.
- **MVP (Model-View-Presenter):** Decoupling the UI from the logic using interfaces (the predecessor to modern standards).
- **MVVM (Model-View-ViewModel):** The current Android standard, focusing on data binding and surviving configuration changes.
- **MVI (Model-View-Intent):** A unidirectional data flow (UDF) approach popular in modern Compose-based apps.

## **Phase 5: Real-World Interview Scenarios**

_Focus: Applying patterns to solve actual problems asked in interviews._

- **Scenario: Designing a Network Layer:** Which patterns (Singleton, Facade, Factory) would you combine to build a robust API client?
- **Scenario: Managing Global State:** How do you handle user session data across multiple screens using patterns?
- **Scenario: Image Loading Library:** If you had to build a simple `Glide`, which patterns would you use (Proxy, Observer, Builder)?
- **Scenario: Clean Architecture:** How do patterns like Facade and Dependency Injection fit into the "Domain" and "Data" layers?

## **Phase 6: The Interview "Closing" (Q&A)**

_Focus: Nailing the common questions and technical trade-offs._

- **Common Questions:** "When would you choose MVP over MVVM?" or "Is Singleton always a good idea?"
- **Trade-offs:** Discussing "Boilerplate vs. Flexibility" and "Over-engineering vs. Scalability."
- **Anti-patterns:** Identifying common mistakes (e.g., Massive ViewModels, tight coupling).

---

**How would you like to proceed? We can start with Phase 1: Creational Patterns, or if you have a specific pattern you're curious about right now, we can jump straight to that!**
