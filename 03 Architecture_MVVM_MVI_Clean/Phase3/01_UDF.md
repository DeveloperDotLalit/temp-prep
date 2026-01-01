---
layout: default
title: Udf
parent: Architecture (MVVM/MVI/Clean): Phase3
nav_order: 1
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Unidirectional Data Flow (UDF)**.

This is the traffic law of modern Android apps.

---

### **Topic: Unidirectional Data Flow (UDF)**

#### **What It Is**

Unidirectional Data Flow (UDF) is a design pattern where data and events travel in a **single, one-way loop**.

Think of it like a river. It only flows downstream. You cannot swim upstream.

1. **State (Data)** flows **DOWN** from the ViewModel to the UI.
2. **Events (Actions)** flow **UP** from the UI to the ViewModel.

The UI never changes the data directly. It only _requests_ a change by sending an event.

#### **Why It Exists (The Problem)**

In older Android code, we often had **Bidirectional Flow**.

- The generic `EditText` changes the variable.
- The variable changes the `EditText`.
- **The Conflict:** If both change at the same time (e.g., a network refresh happens while the user is typing), who wins?
- **The Bug:** You end up with "Ghost States"—the UI says one thing (e.g., "Liked"), but the database says another (e.g., "Not Liked").

UDF solves this by ensuring there is only **one** source of truth (the ViewModel).

#### **How It Works (The Loop)**

The cycle always follows these 3 steps:

1. **State:** The ViewModel holds the current state (e.g., `count = 0`). The UI displays it.
2. **Event:** The User clicks a button. The UI sends an event to the ViewModel (`onIncrementClicked()`).
3. **Update:** The ViewModel processes the logic (`count + 1`) and pushes a **new** state (`count = 1`).
4. **Render:** The UI observes the new state and redraws itself.

_Crucially: The UI simply mirrors the ViewModel. It doesn't "think."_

#### **Example (The "Like" Button)**

**The Wrong Way (Bidirectional/Old School):**
The UI toggles the heart icon _immediately_ when clicked, then tells the server.

- _Risk:_ If the server fails, the UI still shows "Liked." The user is lied to.

**The UDF Way:**

1. **UI:** User clicks the "Like" button.

- _Action:_ Calls `viewModel.toggleLike()`. (The UI does NOT change the icon yet).

2. **ViewModel:**

- Receives the event.
- Calls API.
- If successful, updates `_state.value = Liked`.

3. **UI:**

- Observes the state change.
- "Oh, the state is now 'Liked'. I will turn the heart red."

```kotlin
// 1. The State (Data Down)
data class UiState(val isLiked: Boolean = false)

class PostViewModel : ViewModel() {
    private val _state = MutableStateFlow(UiState())
    val state = _state.asStateFlow()

    // 2. The Event (Events Up)
    fun onLikeClicked() {
        // Logic happens here, not in the UI
        val newLikeStatus = !_state.value.isLiked
        _state.value = _state.value.copy(isLiked = newLikeStatus)
    }
}

// 3. The UI (Compose or XML)
@Composable
fun PostScreen(viewModel: PostViewModel) {
    // Collect State
    val state by viewModel.state.collectAsState()

    // Pass Event
    Button(onClick = { viewModel.onLikeClicked() }) {
        Text(if (state.isLiked) "Unlike" else "Like")
    }
}

```

#### **Interview Keywords**

State, Event, Single Source of Truth, Predictability, Consistency, State Hoisting, Debuggability, Immutable State.

#### **Interview Speak Paragraph**

> "I strictly follow Unidirectional Data Flow (UDF) in my apps. This means data always flows down from the ViewModel to the UI, and user events flow up from the UI to the ViewModel. This eliminates inconsistent states because the UI never modifies data itself; it simply reflects the current state of the ViewModel. It makes the app predictable and much easier to debug because I can trace exactly where and why a state change occurred."

---

**Would you like to proceed to the next note: "Observables (StateFlow / LiveData)"?**
