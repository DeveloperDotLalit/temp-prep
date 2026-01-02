---
layout: default
title: "State Pattern"
parent: "Phase 3: Behavioral Patterns"
nav_order: 4
---

# State Pattern

### **State Pattern: The "Traffic Light" Pattern**

Think of the **State Pattern** like a **Traffic Light**. The light itself is one object, but its "behavior" (what it tells drivers to do) changes based on its internal **State**:

- If the state is **Green**, it tells you to "Go."
- If the state is **Yellow**, it tells you to "Slow down."
- If the state is **Red**, it tells you to "Stop."

You don't need a huge `if-else` block inside the light to check the color every second; the light simply behaves according to its current "State Object."

---

### **1. What It Is**

The **State Pattern** is a behavioral design pattern that allows an object to change its behavior when its internal state changes. To the outside world, it looks as if the object has changed its entire class.

In Android, this is the gold standard for managing **UI States** (Loading, Success, Empty, and Error).

---

### **2. Why It Exists (The Problem it Solves)**

Imagine you are building a **News Feed** screen.

- **The Problem (The "Flag" Mess):** You might use booleans to track what's happening: `isLoading = true`, `isError = false`, `dataList = null`.
  Inside your UI code, you end up with:
  `if (isLoading) showSpinner() else if (isError) showError() else showList()`
  As you add more states (like `isRefreshing` or `isEmpty`), your logic becomes a "Spaghetti" mess of conflicting flags. What if `isLoading` and `isError` are both true by accident? The UI breaks.
- **The Solution:** You treat the "State" as a single object. The screen can only be in **one state at a time**. You swap the entire State Object, and the UI automatically reacts to that specific state's rules.

**Key Benefits:**

- **Single Source of Truth:** No more conflicting boolean flags.
- **Organized Logic:** Each state's behavior is encapsulated in its own class.
- **Clean Transitions:** It’s easy to define how to move from "Loading" to "Success."

---

### **3. How It Works**

1. **The Context:** The class that maintains the current state (e.g., your **ViewModel**).
2. **The State Interface:** Defines the common actions all states must handle.
3. **Concrete States:** Each class represents a specific state (e.g., `LoadingState`, `ErrorState`).

---

### **4. Example (Practical Android/Kotlin)**

In modern Android (using **Jetpack Compose** or **LiveData**), we often use `Sealed Classes` to implement the State Pattern beautifully.

#### **The Scenario: Fetching User Profile**

```kotlin
// 1. The State Definition (Using Sealed Class for restricted hierarchy)
sealed class ProfileState {
    object Loading : ProfileState()
    data class Success(val userName: String) : ProfileState()
    data class Error(val message: String) : ProfileState()
}

// 2. The Context (The ViewModel)
class ProfileViewModel {
    private var currentState: ProfileState = ProfileState.Loading

    fun fetchData() {
        // Logic to fetch data...
        // If success:
        currentState = ProfileState.Success("John Doe")
        renderUI()
    }

    fun renderUI() {
        // 3. The Behavior changes based on the state
        when (val state = currentState) {
            is ProfileState.Loading -> println("Displaying Progress Bar... 🔄")
            is ProfileState.Success -> println("Displaying User: ${state.userName} ✅")
            is ProfileState.Error -> println("Displaying Error: ${state.message} ❌")
        }
    }
}

// --- HOW TO USE IT ---
fun main() {
    val viewModel = ProfileViewModel()

    // Initial State
    viewModel.renderUI()

    // After Fetching
    viewModel.fetchData()
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
  [ User Action ]
         |
         v
  [ ViewModel (Context) ] ----> Swaps ----> [ Current State Object ]
                                                   |
         /-------------------------+---------------+-------------------------\
         |                         |                                         |
 [ Loading State ]         [ Success State ]                         [ Error State ]
 (Shows Shimmer)           (Shows List Data)                         (Shows Retry Button)

```

---

### **6. Interview Keywords**

- **Sealed Classes:** The Kotlin way to implement discrete states.
- **Finite State Machine (FSM):** A mathematical model of computation used to design the State pattern.
- **Encapsulation of State:** Keeping state-specific logic inside separate classes/branches.
- **Unidirectional Data Flow (UDF):** Often paired with the State pattern in MVI architecture.
- **Eliminating Conditional Logic:** Removing large `if-else` or `switch` blocks.

---

### **7. Interview Speak Paragraph**

> "The State Pattern is a behavioral pattern that allows an object to alter its behavior when its internal state changes. In Android, we use this extensively to manage UI states by using Kotlin **Sealed Classes**. Instead of managing multiple conflicting boolean flags like `isLoading` or `hasError`, we encapsulate the entire screen's condition into a single State object. This ensures the UI is always in a valid, predictable state and makes our code much easier to debug and test. It is the core principle behind modern architectures like **MVI (Model-View-Intent)**, where the View simply 'renders' the current state provided by the ViewModel."

---

### **Interview "Pro-Tip" (The "Successor" Question)**

An interviewer might ask: **"Why is a Sealed Class better than an Enum for the State Pattern?"**

- **Your Answer:** "Enums are great for simple labels, but **Sealed Classes** allow you to bundle **data** with the state. For example, the `Success` state can carry a list of users, and the `Error` state can carry an exception message. Enums cannot hold unique data for each constant, making Sealed Classes the perfect choice for complex Android UI states."

---

**Congratulations! You have finished Phase 1, 2, and 3!** You now have a solid grasp of Creational, Structural, and Behavioral patterns.

**Next Step:** Are you ready to zoom out and look at the "Big Picture" in **Phase 4: Architectural Patterns** (starting with **MVC vs. MVP vs. MVVM**)? Or would you like to do a quick recap of the patterns we've covered so far?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
