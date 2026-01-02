---
layout: default
title: "MVI Pattern"
parent: "Phase 4: Architectural Patterns"
nav_order: 4
---

# MVI Pattern

### **MVI (Model-View-Intent): The "Cycle" Pattern**

If **MVVM** is a smart dashboard, **MVI** is like a **Video Game**.

- **Intent (The Input):** You press the "Jump" button on your controller.
- **Model (The Game State):** The game engine calculates your new position (X and Y coordinates).
- **View (The Screen):** The screen reflects that you are now in the air.
  The data moves in **one single circle (Unidirectional)**. You can’t skip a step, and the "Game State" is the only thing the screen ever cares about.

---

### **1. What It Is**

**MVI** is the newest architectural pattern in Android, specifically designed for modern, reactive UIs like **Jetpack Compose**. It is based on the idea of **Unidirectional Data Flow (UDF)** and a **Single Source of Truth**.

1. **Intent:** Not an Android `Intent`! It represents the **user’s intention** to do something (e.g., `ClickSearch`, `RefreshPage`).
2. **Model (State):** An immutable object that represents the _entire_ state of the screen at a specific moment.
3. **View:** A passive component that just "renders" whatever the current State object tells it to.

---

### **2. Why It Exists (The Problem it Solves)**

As apps became more complex, even **MVVM** started to struggle:

- **The "Multiple Stream" Problem:** In MVVM, you might have 5 different LiveDatas (`name`, `isLoading`, `error`, `list`, `isButtonEnabled`). If they update at different times, the UI might flicker or show inconsistent data.
- **State Fragmentation:** It's hard to know exactly what the screen looks like at any given second because the "State" is spread across many variables.
- **The Solution:** MVI combines everything into **one single State object**. If the screen is loading, the _whole_ state is "Loading." This makes the UI completely predictable and easy to debug.

---

### **3. How It Works (The Logical Flow)**

The flow is a strict circle:

1. **User** performs an action (**Intent**).
2. **ViewModel** processes the Intent and communicates with the **Model** (Data).
3. **ViewModel** produces a brand new **State**.
4. **View** observes this single State and updates itself.

---

### **4. Example (Practical Android/Kotlin with Compose)**

#### **The State & Intent (Sealed Classes)**

```kotlin
// The Single State Object
data class UserState(
    val isLoading: Boolean = false,
    val user: String = "",
    val error: String? = null
)

// The Intent (User Actions)
sealed class UserIntent {
    object LoadUser : UserIntent()
    data class ChangeName(val newName: String) : UserIntent()
}

```

#### **The ViewModel**

```kotlin
class UserViewModel : ViewModel() {
    // Single source of truth for the UI
    private val _state = MutableStateFlow(UserState())
    val state: StateFlow<UserState> = _state

    fun handleIntent(intent: UserIntent) {
        when (intent) {
            is UserIntent.LoadUser -> {
                // 1. Update state to Loading
                _state.value = _state.value.copy(isLoading = true)

                // 2. Fetch data and update state to Success
                // (Simplified)
                _state.value = _state.value.copy(isLoading = false, user = "John Doe")
            }
        }
    }
}

```

#### **The View (Jetpack Compose)**

```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel) {
    val uiState by viewModel.state.collectAsState()

    if (uiState.isLoading) {
        CircularProgressIndicator()
    } else {
        Text(text = uiState.user)
        Button(onClick = { viewModel.handleIntent(UserIntent.LoadUser) }) {
            Text("Load")
        }
    }
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
       [ View (UI) ]  --- sends --->  [ Intent (Action) ]
             ^                               |
             |                               v
      [ New State ]  <--- updates ---  [ ViewModel / Business Logic ]

```

---

### **6. Interview Keywords**

- **Unidirectional Data Flow (UDF):** Data flows in only one direction (Intent -> State -> View).
- **Immutability:** The State object cannot be changed; you must create a _new_ copy of it.
- **Single Source of Truth:** One state object defines the entire screen.
- **Side Effects:** Actions that don't change state but happen once (like showing a Toast or Navigating).
- **Redux/Cycle.js:** The web patterns that inspired MVI.

---

### **7. Interview Speak Paragraph**

> "MVI, or Model-View-Intent, is a unidirectional data flow architecture that is highly effective for modern Android apps built with Jetpack Compose. Unlike MVVM, where the state is often fragmented across multiple observables, MVI centralizes the entire UI condition into a single, immutable 'State' object. Users interact with the app by sending 'Intents,' which the ViewModel processes to emit a new 'State.' This makes the UI extremely predictable, easier to test, and simplifies debugging since you can track every state change as a snapshot in time."

---

### **Common Interview Question**

**"When should I choose MVI over MVVM?"**

- **Your Answer:** "MVVM is excellent for most standard apps because it is simpler and has less boilerplate. However, **MVI** is better for **complex screens** with many UI elements that depend on each other. It’s also the preferred choice for **Jetpack Compose** because Compose is designed to 'recompose' based on a single state change. If you need a highly predictable UI or want to implement 'Time Travel Debugging' (replaying states), MVI is the way to go."

---

**Awesome! We have finished Phase 4!** You now know the history and evolution from MVC → MVP → MVVM → MVI.

**Next Step:** Are you ready for **Phase 5: Real-World Interview Scenarios**? This is where I give you a problem (like "Design a Chat App") and you tell me which patterns you'd use and why. Would you like to try the first scenario?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
