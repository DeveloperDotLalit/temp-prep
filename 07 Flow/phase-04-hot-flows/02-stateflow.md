---
layout: default
title: "StateFlow"
parent: "Phase 4: Hot Flows StateFlow and SharedFlow"
nav_order: 2
---

# StateFlow

In the Android world, **StateFlow** has become the gold standard for state management in ViewModels. It is essentially the Kotlin Coroutines version of `LiveData`, but with more power and a stricter focus on "State."

---

### **What It Is – Simple explanation for beginners**

**StateFlow** is a "Hot" Flow that always holds a single, current value.

Think of it like a **Digital Scoreboard** at a stadium.

- It always shows a score (even if it's 0-0).
- If you look at it right now, you see the current score immediately.
- When the score changes, the board updates instantly for everyone watching.
- It doesn't matter when you arrived at the stadium; the scoreboard always tells you the latest "state" of the game.

### **Why It Exists – The problem it solves**

Before StateFlow, we used `LiveData`. However, `LiveData` had limitations:

- **Thread Dependency:** `LiveData` is tied to the Main Thread. StateFlow can work on any thread.
- **Coroutines Integration:** Since StateFlow is a Flow, you can use all the operators we learned (like `.map`, `.filter`, `.zip`) directly on it.
- **Clean Architecture:** `LiveData` is an Android-specific library. If you want your Domain Layer (Pure Kotlin) to handle state, you can't use `LiveData`. You **can** use StateFlow.

### **How It Works – Step-by-step logic**

1. **Initial Value:** Unlike a regular Flow, a StateFlow **must** have an initial value (e.g., `MutableStateFlow(0)`).
2. **State Retention:** It always stores the last emitted value. When a new collector joins, it immediately receives that last value.
3. **Distinct Until Changed:** StateFlow is smart. If you try to update it with the exact same value it already has (e.g., updating score from `1` to `1`), it won't emit anything. This prevents unnecessary UI refreshes.
4. **Read-Only Pattern:** We usually have a `MutableStateFlow` (private) that we can change, and a `StateFlow` (public) that the UI can only read.

---

### **Example – Code-based**

```kotlin
class MyViewModel : ViewModel() {
    // 1. The "Mutable" version is private - only the ViewModel can change it.
    private val _uiState = MutableStateFlow(UiState.Loading)

    // 2. The "Read-Only" version is public - the Fragment/Activity observes this.
    val uiState: StateFlow<UiState> = _uiState

    fun fetchData() {
        viewModelScope.launch {
            // 3. Updating the state
            _uiState.value = UiState.Success(data = "New Data")
        }
    }
}

// UI Side (Fragment)
lifecycleScope.launch {
    // 4. Collect the state safely
    viewModel.uiState.collect { state ->
        when(state) {
            is UiState.Loading -> showSpinner()
            is UiState.Success -> updateList(state.data)
        }
    }
}

```

### **Comparison: StateFlow vs. LiveData**

| Feature                 | StateFlow                                 | LiveData                               |
| ----------------------- | ----------------------------------------- | -------------------------------------- |
| **Initial Value**       | **Required**.                             | Optional.                              |
| **Lifecycle Awareness** | Use `repeatOnLifecycle` to make it aware. | Native-built lifecycle awareness.      |
| **Default Filtering**   | Always filters out duplicate values.      | Does not filter duplicates by default. |
| **Threading**           | Works on any dispatcher.                  | Main thread only for updates.          |

### **Interview Keywords**

Stateful, Hot Flow, Initial Value, `MutableStateFlow`, Conflation, Value-based Filtering, Thread-independent.

### **Interview Speak Paragraph**

> "StateFlow is a state-holder observable flow that emits the current and new state updates to its collectors. Unlike standard Flows, it is hot, meaning it remains active in memory independently of collectors, and it always requires an initial value. In Android, it is the modern alternative to LiveData because it is part of the Kotlin library, making it testable in non-Android modules. It also features built-in conflation, meaning it only emits when the value actually changes, which optimizes UI performance by preventing redundant updates."

---

**Next Step:** StateFlow is great for "State," but what about "Events" like Toasts or Navigation? Shall we move to **SharedFlow: Handling one-time events or broadcasts**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
