---
layout: default
title: "Cheatsheet SOLID Principles"
parent: "SOLID Principles in Android"
nav_order: 6
---

# Cheatsheet SOLID Principles

This is your **Ultimate SOLID Cheatsheet**. I've condensed all five principles into a "quick-glance" format with the core problem, the solution, and the "Interview Script" for each.

---

## 🚀 The SOLID Android Cheatsheet

### **S: Single Responsibility Principle (SRP)**

- **The Problem:** A "God Activity" that fetches data, parses JSON, and updates UI.
- **The Solution:** Move data to a **Repository**, logic to a **ViewModel**, and keep the **Activity** for UI only.
- **The "Why":** Changes in the API shouldn't break your UI code.
- **Interview Speak:** _"A class should have one reason to change. I use ViewModels and Repositories to separate concerns, making the code easier to test and maintain."_

### **O: Open/Closed Principle (OCP)**

- **The Problem:** Using a giant `when` or `if/else` block that you have to edit every time you add a new feature (like a new Payment method).
- **The Solution:** Use **Interfaces** or **Inheritance**. Create a `Payment` interface and add new classes (e.g., `GooglePay`, `Paypal`) instead of editing the old ones.
- **The "Why":** Prevents "Regression Bugs" (breaking old features while adding new ones).
- **Interview Speak:** _"Code should be open for extension but closed for modification. I use Slot APIs in Compose or Interface-based designs to add features without touching tested code."_

### **L: Liskov Substitution Principle (LSP)**

- **The Problem:** A child class that breaks when used in place of its parent (e.g., a `GuestFragment` that throws an error when `getUserId()` is called).
- **The Solution:** If a child can't do what the parent does, it shouldn't be a child. Refactor the hierarchy.
- **The "Why":** Ensures your app doesn't crash with `UnsupportedOperationException` at runtime.
- **Interview Speak:** _"Subclasses must be substitutable for their base classes. I design hierarchies so that any child class follows the 'contract' of its parent without unexpected behavior."_

### **I: Interface Segregation Principle (ISP)**

- **The Problem:** "Fat" interfaces that force you to implement 10 methods when you only need 1 (e.g., a `TextWatcher` where you only need `onTextChanged`).
- **The Solution:** Split big interfaces into many **smaller, specific ones** (e.g., `ClickListener`, `SwipeListener`).
- **The "Why":** Keeps code clean; no more empty `{ }` method overrides.
- **Interview Speak:** _"No client should be forced to depend on methods it doesn't use. I split large interfaces into smaller, modular ones to keep implementations lean."_

### **D: Dependency Inversion Principle (DIP)**

- **The Problem:** Hardcoding a specific class (like `Retrofit`) inside a ViewModel, making it impossible to swap for a "Fake" during testing.
- **The Solution:** Depend on **Interfaces** (Abstractions), not **Classes** (Concretions). Inject them via Hilt/Dagger.
- **The "Why":** The foundation of Unit Testing and Clean Architecture.
- **Interview Speak:** _"High-level modules shouldn't depend on low-level modules; both should depend on abstractions. This decoupling allows me to mock dependencies for unit tests."_

---

### **💡 Pro-Tips for the Interview**

1. **Don't Over-Engineer:** Mention **YAGNI** (You Ain't Gonna Need It). If a project is small, don't create 50 interfaces for 50 classes.
2. **The Goal is Testability:** If they ask "Why SOLID?", your first answer should be: _"To make the code modular, maintainable, and highly testable."_
3. **Code Smells:** Use terms like **"God Object"** (for SRP) and **"Fragile Code"** (for OCP) to show you understand the pain points.

---

### **Quick Comparison Table**

| Principle | Focus          | Common Android Tool/Pattern         |
| --------- | -------------- | ----------------------------------- |
| **SRP**   | Responsibility | ViewModel, Repository, UseCase      |
| **OCP**   | Extension      | Interface, Abstract Class, Slot API |
| **LSP**   | Inheritance    | Custom Views, Base Fragments        |
| **ISP**   | Contracts      | Small Listeners (OnClick, OnScroll) |
| **DIP**   | Abstraction    | Hilt, Dagger, Koin, Testing Mocks   |

---

**Would you like to try a "Stress Test" where I give you a messy code snippet and you tell me which SOLID principle it violates?**
