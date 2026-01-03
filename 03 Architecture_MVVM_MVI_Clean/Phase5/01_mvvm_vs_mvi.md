---
layout: default
title: "Mvvm Vs Mvi"
parent: "Phase 5: Interview Edge"
nav_order: 1
---

Here are your focused notes on **MVVM vs. MVI**.

This is a favorite question for Senior Android roles. They want to know if you choose architecture based on _needs_ or just follow the hype.

---

### **Topic: MVVM vs. MVI**

#### **What It Is**

A battle between two ways of managing data flow.

- **MVVM (Model-View-ViewModel):** The industry standard. Flexible, easier to write, but can get messy if not disciplined.
- **MVI (Model-View-Intent):** The strict challenger. extremely predictable and debuggable, but requires writing a lot more code (boilerplate).

#### **Why It Exists (The Trade-off)**

There is no "Best" architecture. There is only a trade-off between **Ease of Coding** (MVVM) and **Ease of Debugging** (MVI).

- **MVVM** focuses on binding data to the UI efficiently.
- **MVI** focuses on ensuring the State is 100% predictable, no matter how complex the app gets.

#### **How It Works (The Comparison)**

| Feature         | MVVM (Standard)                                                                              | MVI (Strict)                                                            |
| --------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Entry Point** | **Multiple:** The View calls `login()`, `loadData()`, `update()` separately.                 | **Single:** The View sends `Intent(Login)`, `Intent(Load)`.             |
| **State**       | **Multiple Streams:** Often has `isLoading`, `userList`, `error` as separate LiveData/Flows. | **Single State Object:** One big `UiState` data class holds everything. |
| **Data Flow**   | Usually Unidirectional, but allows shortcuts.                                                | Strictly Unidirectional (Cyclic).                                       |
| **Boilerplate** | Low to Medium. Quick to setup.                                                               | High. Need Actions, Reducers, Intents for everything.                   |
| **Debugging**   | Harder to trace _sequence_ of events in complex screens.                                     | Easy. You can log every Intent and State change like a history book.    |

#### **Example (The Difference in Code)**

**MVVM Style (Direct & Simple):**

```kotlin
// View calls this directly
fun onAddClick() {
    val current = _count.value ?: 0
    _count.value = current + 1 // We mutate state locally
}

```

**MVI Style (Formal & Strict):**

```kotlin
// 1. View sends an Intent
fun handleIntent(intent: MainIntent) {
    when(intent) {
        is MainIntent.AddNumber -> {
            // 2. Reduce: Create a brand new state object
            val oldState = _state.value
            val newState = oldState.copy(count = oldState.count + 1)
            _state.value = newState
        }
    }
}

```

#### **When to Use Which?**

- **Use MVVM if:** You are building a standard app, a CRUD app (Create, Read, Update, Delete), or working with a team that needs to move fast. It is "good enough" for 95% of apps.
- **Use MVI if:** You are building a complex screen with many states (e.g., a stock trading dashboard, a rich text editor) where "Ghost States" (bugs) are unacceptable.

#### **Interview Keywords**

Boilerplate, Complexity vs. Control, State Reducer, Predictability, Learning Curve, Over-engineering.

#### **Interview Speak Paragraph**

> "I generally start with MVVM because it strikes the best balance between structure and development speed for most Android applications. It's standard, easy for the team to understand, and with `StateFlow` and Unidirectional Data Flow, it solves most state issues. However, for highly complex screens with multiple data sources and intricate state interactions—like a trading dashboard—I prefer MVI. The strict single-direction flow and immutable state of MVI make debugging complex issues much easier, even though it requires writing more boilerplate code."

---

**Would you like to proceed to the next note: "Handling Edge Cases"?** (How to handle process death and network errors gracefully).
