---
layout: default
title: "StateFlow and SharedFlow"
parent: "Phase 4: Advanced Data Streams"
nav_order: 3
---

# StateFlow and SharedFlow

While **Flow** is inherently "Cold," modern application development (especially in Android) often needs a "Hot" version of Flow to keep the UI in sync with data. This is where **StateFlow** and **SharedFlow** come in. Think of these as the modern, Coroutine-powered replacements for `LiveData`.

---

## **StateFlow & SharedFlow**

### **What It Is**

Both are **Hot Flows**, meaning they exist and emit values even if no one is collecting from them.

- **StateFlow:** A state-holder observable flow that emits the **current** and new state updates to its collectors. It always has a "current value."
- **SharedFlow:** A highly configurable flow that can emit events (like a Snackbar message or a Navigation command) to multiple collectors.

### **Why It Exists**

- **The Problem with Cold Flow:** If you use a regular `Flow` for UI state, every time the screen rotates and the Activity restarts, the Flow starts from scratch (re-fetching data from the DB/Network). This is wasteful and causes flickering.
- **The Solution:** StateFlow keeps the latest data in memory. When a new UI element starts collecting, it immediately gets the **last known value**.

### **How It Works (Comparison)**

#### **1. StateFlow (The State Holder)**

- **Always has a value:** You must provide an initial value (e.g., `Loading`).
- **State Conflation:** If you push the same value twice (e.g., `Success` followed by `Success`), it won't emit the second one. It only cares about _distinct_ state changes.
- **Latest Value:** New collectors immediately receive the current state.
- **Analogy:** A **Thermostat**. It always has a current temperature. If you walk into the room, you can see what it is right now.

#### **2. SharedFlow (The Event Bus)**

- **No initial value:** It starts empty.
- **Configurable Replay:** You can decide how many previous values a new collector should get (default is 0).
- **Great for Events:** Use this for "one-time" actions like showing a Toast, playing a sound, or navigating.
- **Analogy:** A **Radio Broadcast**. If you turn on the radio halfway through a song, you missed the beginning.

---

### **Example: Real-World Implementation**

```kotlin
class MyViewModel : ViewModel() {

    // 1. StateFlow: For the UI State (Loading, Success, Error)
    private val _uiState = MutableStateFlow<String>("Initial State")
    val uiState: StateFlow<String> = _uiState.asStateFlow()

    // 2. SharedFlow: For one-time events (Navigation)
    private val _navigateToDetails = MutableSharedFlow<Int>()
    val navigateToDetails: SharedFlow<Int> = _navigateToDetails.asSharedFlow()

    fun updateState() {
        _uiState.value = "New UI Data" // Simple value assignment
    }

    suspend fun triggerNavigation(id: Int) {
        _navigateToDetails.emit(id) // Use emit for SharedFlow
    }
}

```

### **Technical Comparison Table**

| Feature           | StateFlow                      | SharedFlow                     |
| ----------------- | ------------------------------ | ------------------------------ |
| **Initial Value** | Mandatory                      | None                           |
| **Latest Value**  | Accessible via `.value`        | Not accessible directly        |
| **Conflation**    | Yes (ignores duplicate states) | No (emits everything)          |
| **Use Case**      | UI State (User Profile, List)  | UI Events (Toasts, Navigation) |

### **Interview Keywords**

Hot Flow, State Conflation, Replay Buffer, `asStateFlow`, `asSharedFlow`, LiveData replacement, One-time events.

### **Interview Speak Paragraph**

> "StateFlow and SharedFlow are 'Hot' flows used primarily for state management and event handling. StateFlow is a state-holder that always maintains its latest value and conflates identical consecutive updates, making it ideal for representing UI states like data lists or loading indicators. SharedFlow, on the other hand, is designed for events; it doesn't require an initial value and can be configured with a 'replay' buffer to send a specific number of previous emissions to new collectors. In modern Android development, these have largely replaced LiveData because they are part of the Kotlin Coroutines ecosystem and provide much more powerful transformation operators."

---

**Common Interview Question: "Why use StateFlow over LiveData?"**

- **Answer:** 1. **Kotlin-first:** StateFlow is part of Kotlin, so it works in Multiplatform (KMP) projects, whereas LiveData is tied to Android.

2.  **Operators:** You can use all Flow operators (`map`, `filter`, `combine`, `zip`) which are much more powerful than LiveData's transformations.
3.  **Thread Control:** You can easily change dispatchers using `flowOn`.

**Would you like to move on to Flow Operators: Transforming data using `map`, `filter`, `collect`, and `combine`?**

Would you like me to explain how to collect these safely in the Android UI using `repeatOnLifecycle`? (Crucial for preventing background crashes).

---

[â¬… Back to Phase](../) | [Next âž¡](../)
