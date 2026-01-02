---
layout: default
title: "Scenario Based Refactoring Challenges"
parent: "Phase 5: Interview Final Polish"
nav_order: 1
---

# Scenario Based Refactoring Challenges

This is the "Senior Developer" question. Interviewers use this to see if you have a systematic approach to technical debt. They aren't looking for a "rewrite everything" answer; they are looking for how you surgically improve a mess without breaking the app.

---

## **12. Scenario: Refactoring a 2000-line "God Activity"**

### **What It Is**

A **2000-line Activity** is the ultimate SOLID violator. It likely handles networking, database, business logic, permissions, UI state, and navigation. Refactoring it means breaking these responsibilities into smaller, testable, and interchangeable pieces.

### **Why It Exists**

- **The Problem:** Legacy code usually starts small, but as features (Analytics, Validation, API calls) are added over years, the Activity becomes the "dumping ground" for everything.
- **The Goal:** Move from a **Monolithic** structure to a **Clean Architecture** structure where the Activity is "dumb" and only handles UI.

---

### **How It Works (The 4-Step Refactor Strategy)**

#### **Step 1: The "Low Hanging Fruit" (Extraction)**

Don't touch the logic yet. Start by moving code that doesn't belong in an Activity at all.

- **Mappers:** Move code that converts API models to UI strings (e.g., `if(status == 1) "Active"`) into a `Mapper` class.
- **Validators:** Move email/password regex checks into a `Validator` class.
- **Constants:** Move hardcoded strings or IDs into appropriate config files.

#### **Step 2: The Data Layer (SRP & DIP)**

Identify all `Retrofit` calls or `SharedPreferences` logic.

- Create a `Repository` interface.
- Move the actual networking code into a `RepositoryImpl`.
- **Result:** The Activity no longer knows _where_ the data comes from.

#### **Step 3: The Logic Layer (ViewModel)**

Move the "State" out of the Activity.

- Create a `ViewModel`.
- Move variables like `isLoading`, `userList`, and `errorMessage` into `LiveData` or `StateFlow` inside the ViewModel.
- **Result:** If the screen rotates, the data isn't lost, and the Activity only "observes" the state.

#### **Step 4: The "Brain" (Use Cases/Interactors)**

If there is complex business logic (e.g., "If user is premium AND has expired subscription, show discount"), move that into a `UseCase`.

- **Result:** This logic can now be Unit Tested with plain JUnit.

---

### **Example: Before & After Logic**

**Before (The 2000-line Mess):**

```kotlin
// Inside Activity
fun onLoginClicked() {
    showProgress()
    // 1. Networking code inside UI
    apiService.login(email, pass).enqueue(object : Callback {
        // 2. Business logic & Navigation inside UI
        if (response.isSuccessful) {
             startActivity(Intent(this, Home::class.java))
        }
    })
}

```

**After (The SOLID way):**

```kotlin
// Inside Activity (Passive UI)
fun onLoginClicked() {
    viewModel.login(email, pass) // Just tells the VM what happened
}

// Inside ViewModel (State & Coordination)
fun login(email, pass) {
    viewModelScope.launch {
        val result = loginUseCase(email, pass) // Delegates to logic
        _viewState.value = result
    }
}

```

---

### **Interview Keywords**

Technical Debt, Incremental Refactoring, Separation of Concerns, State Hoisting, Testability, Passive View.

### **Interview Speak Paragraph**

> "When refactoring a 2,000-line Activity, my priority is to reduce the 'Single Responsibility' violations incrementally. I start by extracting non-UI logic—like data mapping and validation—into utility classes. Next, I introduce a Repository layer to abstract the data source and a ViewModel to manage the UI state. This allows the Activity to become a 'Passive View' that only observes state changes. Finally, I move complex business rules into Use Cases. This systematic approach ensures that each piece of logic becomes independently testable and the Activity is reduced to its primary job: rendering UI and capturing user input."

---

### **Common Interview Question/Angle**

**Q: "How do you ensure you don't break the app during this massive refactor?"**
**A:** "I use the **'Boy Scout Rule'**—leave the code cleaner than you found it, but do it in small, manageable PRs. Before refactoring a specific logic block, I try to write an **Integration Test** or a **UI Test** (Espresso) to capture the current behavior. Once I extract the logic into a new class, I write a **Unit Test** for it. If the tests pass before and after the move, I have confidence that I haven't introduced regressions."

---

**Excellent! We have covered the major scenarios.** The very last step is the **Master Q&A List**. This will be a "Cheat Sheet" of the most common, tricky SOLID questions you might face, summarized for quick recall.

**Would you like me to generate the Master Interview Q&A List now?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
