---
layout: default
title: "Single Responsibility Principle"
parent: "Phase 1: The Foundation (S and O)"
nav_order: 1
---

# Single Responsibility Principle

Starting with **Phase 1**, let’s dive into the first and arguably most important pillar of SOLID. In the Android world, this is the primary "cure" for the dreaded "God Activity" (that 3000-line file we’ve all seen).

---

## **1. Single Responsibility Principle (SRP)**

### **What It Is**

At its simplest, SRP says: **"A class should do one thing, and do it well."** In technical terms, it means a class should have only **one reason to change**. If you find yourself editing the same file because the API logic changed, AND because the UI design changed, AND because the database schema changed—that class is doing too much.

### **Why It Exists**

- **The Problem:** In Android, beginners often put everything into an `Activity` or `Fragment` (API calls, data parsing, UI logic, string formatting). This is called a **"God Object."**
- **The Consequence:** When you change one small thing, the whole class breaks. It becomes impossible to write Unit Tests because you can't isolate the logic.
- **The Goal:** By splitting responsibilities, your code becomes modular, easier to read, and much simpler to test.

### **How It Works**

1. **Identify Responsibilities:** Look at your class. Is it handling UI? Is it fetching data? Is it calculating math?
2. **Extract:** Move logic that doesn't belong to a new class.
3. **Delegate:** The original class now just "calls" the new class to get the work done.

### **Example (The Android Way)**

#### **❌ The Wrong Way (Violating SRP)**

This `UserActivity` is doing everything: fetching data, parsing it, and showing it.

```kotlin
class UserActivity : AppCompatActivity() {
    // VIOLATION: Activity is fetching data, parsing logic, and UI
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1. Networking Logic
        val userJson = api.getUser(123)

        // 2. Parsing/Business Logic
        val name = userJson.split(":")[1]

        // 3. UI Logic
        findViewById<TextView>(R.id.nameTv).text = name
    }
}

```

#### **✅ The SRP Way (Refactored)**

We split the responsibilities into three distinct parts.

1. **UserRepository:** Handles only data fetching.
2. **UserViewModel:** Handles only the "logic" of preparing data for the UI.
3. **UserActivity:** Handles only displaying things on the screen.

```kotlin
// Responsibility: Data Fetching
class UserRepository {
    fun fetchUser(id: Int) = api.getUser(id)
}

// Responsibility: Preparing data for UI
class UserViewModel(val repo: UserRepository) : ViewModel() {
    fun getFormattedName(id: Int): String {
        val rawData = repo.fetchUser(id)
        return rawData.split(":")[1] // Parsing logic lives here
    }
}

// Responsibility: Displaying UI
class UserActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val name = viewModel.getFormattedName(123)
        findViewById<TextView>(R.id.nameTv).text = name
    }
}

```

### **Interview Keywords**

One reason to change, God Object, Cohesion, Separation of Concerns, Decoupling, Modularization.

### **Interview Speak Paragraph**

> "The Single Responsibility Principle states that a class should have only one reason to change. In Android, we commonly apply this by moving business logic out of Activities and Fragments and into ViewModels or UseCases. By ensuring a class handles only one specific functionality—like data fetching or UI rendering—we avoid 'God Objects,' making the codebase much easier to unit test, maintain, and debug."

---

### **Common Interview Question/Angle**

**Q: "If I have a small app, isn't SRP just creating too many files for no reason?"**
**A:** "While it creates more files, it reduces the **cognitive load** per file. It’s easier to debug a 50-line class that does one thing than a 500-line class that does five things. It's an investment in 'Scalability'—as the app grows, SRP prevents the code from becoming a tangled mess."

**Would you like to move on to the next topic in Phase 1: The Open/Closed Principle (OCP)?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
