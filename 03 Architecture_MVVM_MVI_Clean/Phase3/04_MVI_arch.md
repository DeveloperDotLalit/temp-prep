---
layout: default
title: Mvi Arch
parent: Phase3
nav_order: 4
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Introduction to MVI (Model-View-Intent)**.

This is the "Advanced" architecture pattern often asked about in Senior interviews.

---

### **Topic: Introduction to MVI (Model-View-Intent)**

#### **What It Is**

MVI stands for **Model-View-Intent**. It is very similar to MVVM, but it is much stricter.

- **Model:** Represents the State (just like we learned in UI State Modeling).
- **View:** The UI (Activity/Compose).
- **Intent:** This is **NOT** the `android.content.Intent` used to start Activities. In MVI, "Intent" simply means **"Intention"** or "User Action." It is a label for something the user wants to do (e.g., `LoadData`, `ClickButton`, `TypeSearch`).

#### **Why It Exists (The Problem)**

In standard MVVM, your ViewModel often becomes a mess of functions:

- `fun login()`
- `fun loadUser()`
- `fun updateProfile()`
- `fun deleteAccount()`

The View calls these randomly. It’s hard to track _what_ caused a state change. Did the user click "Login"? Or did the system auto-login? Or did a background timer do it?

**MVI fixes this by forcing a Single Entry Point.**
The View can only do **one thing**: Send an `Intent`.
The ViewModel processes that Intent and produces a new State.

#### **How It Works (The Cycle)**

MVI follows a strict circle called **Unidirectional Data Flow**:

1. **The View** fires an **Intent** (e.g., `UserIntent.Refresh`).
2. **The ViewModel** captures this Intent.
3. **The Processor** handles the logic (fetches data).
4. **The Reducer** creates a **New State** based on the result.
5. **The View** renders the new State.

_Think of it like a Vending Machine:_

- **MVVM:** You can reach inside and spin the motors manually (calling functions).
- **MVI:** You can only press buttons on the front panel (Sending Intents). The machine handles the rest internally.

#### **Example (The Single Entry Point)**

**MVVM Approach (Multiple Functions):**

```kotlin
class MainViewModel : ViewModel() {
    fun loadData() { ... }
    fun onBookmarkClick(id: Int) { ... }
    fun onSearch(query: String) { ... }
}

```

**MVI Approach (One Function to Rule Them All):**

```kotlin
// 1. Define all possible User Actions
sealed class MainIntent {
    object LoadData : MainIntent()
    data class Bookmark(val id: Int) : MainIntent()
    data class Search(val query: String) : MainIntent()
}

class MainViewModel : ViewModel() {

    // 2. The Single Entry Point
    fun handleIntent(intent: MainIntent) {
        when(intent) {
            is MainIntent.LoadData -> fetchNews()
            is MainIntent.Bookmark -> saveBookmark(intent.id)
            is MainIntent.Search -> performSearch(intent.query)
        }
    }
}

```

#### **Interview Keywords**

Unidirectional Data Flow, Immutable State, Intent (User Action), Reducer, Single Entry Point, Cyclic Flow, Thread Safety.

#### **Interview Speak Paragraph**

> "MVI (Model-View-Intent) is an architectural pattern that enforces strict unidirectional data flow. Unlike MVVM, where the View might call multiple different functions in the ViewModel, MVI treats every user interaction as a distinct 'Intent' or object. These Intents are passed to a single entry point in the ViewModel. This makes the app state extremely predictable and easy to debug, because we can trace the exact sequence of Intents that led to the current state."

---

### **Phase 3 Complete!**

You now master the flow of data: **UDF**, **Observables**, **UI State**, and **MVI**.

**Would you like to move to Phase 4: "The Glue & The Safety Net – DI & Testing"?** (This covers Hilt/Koin and how to test your code).
