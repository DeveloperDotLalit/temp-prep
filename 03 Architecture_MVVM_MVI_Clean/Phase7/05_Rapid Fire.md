---
layout: default
title: Rapid Fire
parent: Architecture (MVVM/MVI/Clean): Phase 7: The Interview Q&A & Defense (The Final Polish)
nav_order: 5
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Mock Interview Rapid Fire**.

These are the "Elevator Pitch" definitions. In an interview, if you stumble on these basics, the interviewer will assume you don't know the advanced stuff either. You must memorize these to answer instantly.

---

### **Topic: Mock Interview Rapid Fire (10 Essentials)**

**1. What is a Memory Leak?**

> "It happens when an object (like an Activity) is no longer needed but cannot be deleted by the Garbage Collector because some other object (like a background thread or static variable) is still holding a reference to it. This eventually causes an `OutOfMemoryError`."

**2. What is a Race Condition?**

> "A bug that occurs when the software's behavior depends on the uncontrollable timing of events, like two threads trying to update the same variable at the exact same time, leading to unpredictable results."

**3. What is Dependency Injection (DI)?**

> "A design pattern where a class receives its dependencies (objects it needs) from the outside—usually via the constructor—rather than creating them itself. This makes the code loosely coupled and easily testable."

**4. What is the difference between `val` and `const val`?**

> "`val` is a read-only variable whose value is determined at **runtime** (when the code runs). `const val` is a compile-time constant, meaning its value is hardcoded and known when you build the app (like `3.14`)."

**5. What is the difference between `LiveData` and `StateFlow`?**

> "`LiveData` is Android-lifecycle aware but requires the main thread. `StateFlow` is part of Kotlin Coroutines, is not tied to Android (platform-agnostic), and offers more powerful operators, making it the modern standard."

**6. What is the Single Responsibility Principle (SRP)?**

> "The 'S' in SOLID. It states that a class should have only one reason to change, meaning it should perform only one specific job. For example, a ViewModel should manage state, not format Date strings."

**7. What is a Coroutine?**

> "A lightweight thread management framework in Kotlin. It allows us to write asynchronous code (like network calls) in a sequential, readable way without blocking the main thread."

**8. What is `ViewModelScope`?**

> "A predefined Coroutine Scope tied to the ViewModel's lifecycle. Any coroutine launched in this scope is automatically canceled when the ViewModel is cleared, preventing memory leaks."

**9. What is the role of the Repository?**

> "It acts as a Single Source of Truth for data. It mediates between different data sources—like a local database and a network API—and decides where to fetch data from to provide it to the ViewModel."

**10. Why do we use `DiffUtil` in RecyclerView?**

> "It's a utility class that calculates the difference between two lists (old vs. new) on a background thread. It updates only the specific items that changed, rather than refreshing the entire list, which improves performance significantly."

---

### **🎉 COURSE COMPLETE!**

You have officially finished the entire **Android Architecture Clean MVVM/MVI Masterclass**.

You started with "Why we need architecture" and finished with "How to survive a rapid-fire interview."

**What is your next move?**

1. **Start a Mock Interview:** I can simulate a strict interviewer right now. I'll ask one question, you answer, and I'll grade you.
2. **Generate a Cheat Sheet:** I can condense all 7 Phases into a single-page PDF-style summary.
3. **End Session:** You can take these notes and start studying on your own.

**Just let me know!**
