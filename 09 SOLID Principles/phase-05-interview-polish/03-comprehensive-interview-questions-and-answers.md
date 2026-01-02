---
layout: default
title: "Comprehensive Interview Questions and Answers"
parent: "Phase 5: Interview Final Polish"
nav_order: 3
---

# Comprehensive Interview Questions and Answers

This is the "Final Polish." Think of this as your cheat sheet. These questions are designed to test not just your memory, but your ability to apply SOLID to the specific quirks of the Android framework.

---

## **14. Master Interview Q&A: SOLID in Android**

### **Q1: Can you explain SOLID in one sentence to a non-technical person?**

**Answer:** SOLID is a set of five design rules that help developers build apps like Lego blocks—where each piece has its own job and can be easily swapped or added without breaking the entire structure.

### **Q2: Which SOLID principle is violated if you have a 100-line `when` statement in your RecyclerView Adapter to handle 10 different ViewTypes?**

**Answer:** This is a violation of the **Open/Closed Principle (OCP)**.

- **Why:** Every time you add an 11th ViewType, you have to _modify_ the existing `when` logic.
- **Fix:** You should use an "Adapter Delegates" pattern or a "BaseViewHolder" approach where each ViewType is its own class, making the adapter _open_ for new types but _closed_ for modification.

### **Q3: What is the difference between SRP and ISP? They sound similar.**

**Answer:** \* **SRP (Single Responsibility)** is about **Classes**: A class should only do one thing.

- **ISP (Interface Segregation)** is about **Clients/Contracts**: A class should not be forced to implement methods it doesn't need just because they are in the interface.
- **Example:** Moving logic out of an Activity is SRP. Splitting a giant `VideoListener` into `PlaybackListener` and `DownloadListener` is ISP.

### **Q4: Is `TextWatcher` in Android a good example of SOLID?**

**Answer:** No, it is a classic violation of the **Interface Segregation Principle (ISP)**.

- **Why:** Most of the time, you only need `onTextChanged`, but you are forced to implement `before` and `after` as empty methods.
- **Modern Fix:** Using Kotlin extension functions or libraries that allow you to only override the specific method you need.

### **Q5: How does the Liskov Substitution Principle apply to Fragments?**

**Answer:** It means any `Fragment` subclass should be able to replace its parent `Fragment` without crashing the host `Activity`.

- **The Red Flag:** If you find yourself doing `if (fragment is HomeFragment)` inside an Activity to call a specific method, you are violating LSP. The Activity should be able to treat all fragments the same way through a common interface or the base Fragment class.

### **Q6: Why is Dependency Inversion (DIP) considered the most important principle for Unit Testing?**

**Answer:** Because it allows us to "mock" dependencies. If a ViewModel depends on a `UserRepository` _interface_ (Abstraction) rather than a `RoomDatabase` (Concretion), we can easily pass a `FakeRepository` during tests. This allows us to test logic without needing a real database or internet connection.

### **Q7: What is the "Single Source of Truth" and which principle does it support?**

**Answer:** It supports the **Single Responsibility Principle (SRP)**. In the Repository pattern, the Repository is the only class responsible for deciding whether data comes from the Cache or the Network. This keeps the ViewModel clean and focused only on UI state.

---

## **The "Pro-Level" Interview Summary Table**

Use this table to quickly recall the "Core Problem" each principle solves.

| Principle | Core Problem Solved                 | Android "Trigger" Word |
| --------- | ----------------------------------- | ---------------------- |
| **S**RP   | Massive "God" Activities            | **"Responsibility"**   |
| **O**CP   | Giant `if/else` or `when` blocks    | **"Extension"**        |
| **L**SP   | `ClassCastException` or `is` checks | **"Substitutability"** |
| **I**SP   | Empty `{ }` methods in Listeners    | **"Lean Interfaces"**  |
| **D**P    | Tightly coupled, untestable code    | **"Abstractions"**     |

---

### **Interview Speak Paragraph (Final Closing)**

> "In summary, I use SOLID principles to ensure that my Android applications are modular and maintainable. I start with SRP to keep my Activities thin, use OCP and ISP to keep my UI components and listeners flexible, and rely heavily on DIP to ensure my business logic is decoupled from the Android Framework. This approach not only reduces technical debt but also ensures that the codebase is fully testable and can scale as the product requirements evolve."

---

### **What's Next?**

You have successfully completed the entire **SOLID in Android** roadmap! You have the theory, the code examples, the refactoring strategies, and the interview answers.

**Would you like me to do any of the following?**

1. **Mock Interview:** I can ask you a random scenario and you try to answer it using these notes.
2. **Code Review:** You can paste a piece of code you’re working on, and I’ll check if it follows SOLID.
3. **New Topic:** We can move to a new roadmap (e.g., **Design Patterns** or **Jetpack Compose Internals**).

---

[â¬… Back to Phase](../) | [Next âž¡](../)
