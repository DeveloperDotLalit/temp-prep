---
layout: default
title: "Handling Edge Cases"
parent: "Phase 5: Interview Edge"
nav_order: 2
---

Here are your focused notes on **Handling Edge Cases**.

This distinguishes a "Demo App" from a "Production App." A demo app works when everything goes right. A production app works even when the internet dies or the phone runs out of memory.

---

### **Topic: Handling Edge Cases**

#### **What It Is**

Edge cases are the "unhappy paths" where things go wrong.

1. **Network Errors:** The internet cuts out, or the server sends garbage data.
2. **Process Death:** The Android system quietly kills your app in the background to save battery/memory, and the user re-opens it later.
3. **One-Off Events:** Events that should happen only once (like showing a "Success" Toast or Navigating).

#### **Why It Exists (The Problem)**

- **The Crash:** If you don't catch network errors, the app crashes.
- **The "Blank Screen":** If you don't handle Process Death, the user returns to the app and sees an empty screen because your variables were deleted.
- **The "Looping Toast":** If you treat a Toast like normal data (State), rotating the screen might show the Toast again... and again.

#### **How It Works (The Solutions)**

**1. Managing Network Errors (The Wrapper)**
Don't let exceptions fly around. Wrap your data in a `Result` class.

- **Repository:** Catches `try/catch`. Returns `Result.Success(data)` or `Result.Error(exception)`.
- **ViewModel:** Checks the result. If Error, updates `_uiState` to `ErrorState`.

**2. Handling Process Death (The Zombie)**
Standard ViewModels survive rotations, but **die** if the system kills the app.

- **Solution:** Use `SavedStateHandle`. It's a small "backpack" of data that Android saves to the disk for you. When the app restarts (Zombie mode), the ViewModel checks the backpack.

**3. Complex Navigation (One-Off Events)**
Navigation is an "Event," not "State."

- **State:** "I am on the Home Screen." (Persistent)
- **Event:** "Go to Details Screen." (Happens once)
- **Solution:** Use a `Channel` or `SharedFlow` (hot stream) instead of `StateFlow` for navigation commands. This ensures the event is consumed and doesn't re-fire on rotation.

#### **Example (The Robust ViewModel)**

```kotlin
@HiltViewModel
class RobustViewModel @Inject constructor(
    private val repo: MyRepository,
    private val savedState: SavedStateHandle // The Backpack
) : ViewModel() {

    // 1. Handling Process Death
    // If app died, we get the ID back from the "backpack"
    val userId = savedState.get<String>("userId") ?: ""

    // 2. Handling One-Off Events (Navigation/Toasts)
    private val _events = Channel<UiEvent>()
    val events = _events.receiveAsFlow()

    fun loadData() {
        viewModelScope.launch {
            // 3. Handling Network Errors
            try {
                val data = repo.fetchData()
                _state.value = UiState.Success(data)
            } catch (e: IOException) {
                // Map the error to a UI message
                _state.value = UiState.Error("Check internet")
                // Send a one-time event
                _events.send(UiEvent.ShowToast("Connection Failed"))
            }
        }
    }
}

```

#### **Interview Keywords**

SavedStateHandle, Process Death vs. Configuration Change, Result Wrapper, Try-Catch, SharedFlow vs. StateFlow, One-off Events, System-initiated process death.

#### **Interview Speak Paragraph**

> "To build a robust app, I focus heavily on edge cases. For network errors, I never expose raw exceptions to the UI; instead, I use a sealed `Result` class to wrap success or failure in the Repository. For system-initiated process death, I use the `SavedStateHandle` to preserve critical data like user IDs or search queries so the app can restore its state seamlessly. Finally, for navigation and one-time errors, I use `Channels` or `SharedFlow` to ensure these events are consumed once and don't re-trigger when the user rotates the screen."

---

**Would you like to proceed to the final note: "Mapper Classes"?** (This explains how we convert data between layers).
