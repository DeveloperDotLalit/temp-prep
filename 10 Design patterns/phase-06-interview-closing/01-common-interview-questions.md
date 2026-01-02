---
layout: default
title: "Common Interview Questions"
parent: "Phase 6: Interview Closing and QnA"
nav_order: 1
---

# Common Interview Questions

We’ve reached the final "boss level" of our learning journey. In a senior-level interview, the interviewer won't just ask you to define a pattern; they will challenge your **judgment**. They want to see if you know when a pattern is a _bad_ idea.

Here are the notes for the most common "gotcha" questions.

---

### **1. "When would you choose MVP over MVVM?"**

#### **What It Is**

This is a comparison between two ways of handling the logic-to-UI connection. **MVP** is manual (Presenter tells View what to do), while **MVVM** is automatic (View watches the ViewModel).

#### **Why This Question Exists**

The interviewer wants to see if you understand the **overhead** of each architecture. While MVVM is the "modern" choice, it isn't always the "right" choice for every single project.

#### **How It Works (The Comparison)**

- **Choose MVP if:** \* The project is very small or a simple utility tool where setting up `LiveData`, `Flow`, and `ViewModels` feels like over-engineering.
- You are working on a legacy project that already uses MVP and changing it would be too risky.
- You want absolute, granular control over every UI change (manual wiring).

- **Choose MVVM if:**
- You are building a modern, scalable app (Google’s recommendation).
- You want to survive configuration changes (rotations) automatically.
- You are using **Data Binding** or **Jetpack Compose** (which are designed for MVVM/MVI).

#### **Interview Keywords**

- **Reactive vs. Imperative:** MVVM is reactive (observing); MVP is imperative (commanding).
- **Boilerplate:** MVP requires more interfaces; MVVM requires more library setup.
- **Lifecycle Awareness:** MVVM handles the Android lifecycle better by default.

#### **Interview Speak Paragraph**

> "While MVVM is the modern standard for Android due to its lifecycle awareness and reactive nature, I would choose **MVP** for simpler, smaller projects where the overhead of observables and ViewModels might be unnecessary. MVP offers a very explicit, imperative way of controlling the UI through interfaces, which can sometimes be easier to debug in tiny applications. However, for any project intended to scale or use modern toolkits like Jetpack Compose, I would always favor **MVVM** because it decouples the UI from the logic much more effectively and handles state preservation during configuration changes automatically."

---

### **2. "Is Singleton always a good idea? (The Dark Side of Singletons)"**

#### **What It Is**

A Singleton ensures one instance. However, in the world of professional coding, it is often called an **"Anti-Pattern"** if used incorrectly.

#### **Why It Exists (The Problem it Solves)**

The interviewer is testing if you know the **risks**. A Singleton is basically a "Global Variable," and global variables are notoriously dangerous in software engineering.

#### **How It Works (The Risks)**

1. **Hidden Dependencies:** If Class A uses a Singleton, you can't see that dependency in the constructor. It makes the code "dishonest."
2. **Testing Nightmare:** Singletons stay in memory. If one test changes a value in a Singleton, it might break the next 10 tests because the state "leaked" across them.
3. **Memory Leaks:** If a Singleton holds a reference to an `Activity` or its `Context`, that Activity can never be cleared from memory, leading to a crash.

#### **Interview Keywords**

- **Global State:** Data that can be changed from anywhere.
- **Tight Coupling:** Making classes hard to separate.
- **Unit Test Isolation:** Tests should not affect each other.
- **Static Bottleneck:** Difficulty in mocking or swapping the instance.

#### **Interview Speak Paragraph**

> "No, a Singleton is not always a good idea; in fact, it's often considered an anti-pattern if overused. The primary issue is that it introduces **global state** into an app, which makes unit testing extremely difficult because state can leak between tests. It also creates hidden dependencies that aren't visible in a class constructor. In modern Android development, I prefer using **Dependency Injection** with Hilt or Dagger to manage object lifecycles. This gives us the benefit of having a 'single instance' (Singleton scope) while still allowing us to swap it with a mock during testing and keeping our dependencies explicit and transparent."

---

### **3. "What is a 'God Object' and how do patterns fix it?"**

#### **What It Is**

A **God Object** is a class that knows too much or does too much (like a 3,000-line Activity).

#### **How It Works (The Fix)**

- **Facade:** Breaks the God Object by moving complex logic into a simplified "Front Desk."
- **Strategy:** Breaks the God Object by moving different "behaviors" into their own classes.
- **Command:** Breaks the God Object by turning "actions" into separate objects.

#### **Interview Speak Paragraph**

> "A 'God Object' is an anti-pattern where a single class takes on too many responsibilities, making it a nightmare to maintain and test. We fix this by applying the **Single Responsibility Principle**. For example, we can use the **Facade pattern** to move data-handling logic into a Repository, or the **Strategy pattern** to move complex conditional logic into separate behavioral classes. By delegating these tasks to smaller, specialized objects, we turn a 'God Object' into a collection of decoupled, testable components."

---

### **Congratulations! 🎓**

You have completed the entire **Design Patterns in Android** roadmap. You have gone from basic Creational patterns to complex Architectural decisions. You are now equipped to:

1. Explain the **Why** behind the code.
2. Provide **Real-world Android examples**.
3. Discuss **Trade-offs** like a senior developer.

**Next Step:** Since we've finished the notes, would you like me to give you a **"Mock Interview Quiz"** with 5 tough questions to test your readiness? Or is there a specific pattern you'd like to revisit in more detail?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
