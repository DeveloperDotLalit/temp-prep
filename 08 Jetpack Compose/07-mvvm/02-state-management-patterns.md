---
layout: default
title: State Management Patterns
parent: 7. Clean MVVM with Compose
nav_order: 2
---

# State Management Patterns

Here are your notes for **Topic 7.2**.

---

## **Topic 7.2: State Management Patterns**

### **1. What It Is**

This topic covers the standard tools for managing and observing data streams in a modern Android app.

- **`StateFlow`:** A state-holder observable flow that emits the current and new state updates. It always has a value. (Replacement for `LiveData`).
- **`SharedFlow`:** A hot flow that emits values to all consumers. It does _not_ hold a value by default. (Replacement for `SingleLiveEvent` or EventBus).
- **`collectAsStateWithLifecycle`:** The specific Composable function used to safely convert these flows into Compose State in the UI.

### **2. Why It Exists (The "Hot" Stream Problem)**

- **StateFlow vs. LiveData:** LiveData was tied to Android. `StateFlow` is pure Kotlin, meaning you can use it in Domain/Data layers (even in KMP).
- **SharedFlow vs. StateFlow:** `StateFlow` is for **State** (What is the current text?). `SharedFlow` is for **Events** (Show Toast, Navigate). If you use `StateFlow` for a Toast, the Toast will reappear every time you rotate the screen because `StateFlow` remembers the "Show Toast" state. `SharedFlow` fires and forgets.
- **The Collection Problem:** If you just use `.collect()` or `collectAsState()` in a Composable, the flow keeps running even when the app is in the background (e.g., user pressed Home). This wastes battery and crashes if you try to update the UI when stopped.

### **3. How It Works**

#### **A. StateFlow (The "Box")**

It acts like a box that always contains exactly one item.

- **Write:** `_state.value = NewData`
- **Read:** `state.value`
- **Behavior:** It conflates values. If you update it 100 times in 1ms, the collector only gets the latest one.

#### **B. SharedFlow (The "hose")**

It acts like a water hose. If nobody is watching, the water (events) is lost (unless you configure `replay`).

- **Write:** `_event.emit(Message)`
- **Read:** `.collect { ... }`

#### **C. `collectAsStateWithLifecycle` (The Safe Consumer)**

This function (from `androidx.lifecycle:lifecycle-runtime-compose`) is the **Mandatory** way to consume flows in Compose UI.

- **Under the hood:** It uses `repeatOnLifecycle`.
- **Behavior:**
- App Backgrounded -> Stops collecting (Saves battery).
- App Foregrounded -> Restarts collecting.

### **4. Example: The Complete Pattern**

**The ViewModel (Producer)**

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor() : ViewModel() {

    // 1. STATE (StateFlow): Always has a value (Initial = Loading)
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState = _uiState.asStateFlow()

    // 2. EVENTS (SharedFlow): No initial value. Replay = 0 (Don't resend old events)
    private val _uiEvent = MutableSharedFlow<String>()
    val uiEvent = _uiEvent.asSharedFlow()

    fun saveData() {
        viewModelScope.launch {
            _uiState.value = UiState.Success // Updates State
            _uiEvent.emit("Saved Successfully") // Triggers One-time Event
        }
    }
}

```

**The UI (Consumer)**

```kotlin
@Composable
fun HomeScreen(viewModel: HomeViewModel) {
    // 3. SAFE COLLECTION (State)
    // Automatically pauses when app is minimized
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    // 4. SAFE COLLECTION (Events)
    // We use LaunchedEffect because events are side-effects
    LaunchedEffect(Unit) {
        viewModel.uiEvent.collect { message ->
            // Show Snackbar or Navigate
            Log.d("Event", message)
        }
    }

    // Render UI based on 'state'
    when(state) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Success -> Text("Done!")
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`StateFlow` vs `SharedFlow`, Hot vs Cold Streams, `collectAsStateWithLifecycle`, `repeatOnLifecycle`, `LiveData` deprecation, Conflation, Replay Cache.

**Interview Speak Paragraph**

> "For state management, I strictly use `StateFlow` for UI state because it acts as a predictable source of truth that always holds a value, similar to LiveData but platform-agnostic. For one-off events like navigation or snackbars, I use `SharedFlow` with `replay=0` to prevent the 'event re-firing' bug on screen rotation. Crucially, when observing these flows in Compose, I use `collectAsStateWithLifecycle`. Unlike the older `collectAsState`, this API is lifecycle-aware—it automatically stops flow collection when the app goes to the background, preventing wasted resources and potential crashes."

---

**Next Step:**
We have the architecture and the state. Now, how do we handle user actions like "Click Button -> Load Data"?
Ready for **Topic 7.3: Handling UI Events (MVI concepts)**? This is how we keep the ViewModel clean.

[StateFlow vs SharedFlow in Jetpack Compose | State Management and Event Handling Explained](https://www.youtube.com/watch?v=ByDU1YjCr8E)

This video is relevant because it clearly demonstrates the practical differences between StateFlow and SharedFlow within a Jetpack Compose context, reinforcing the "State vs Event" distinction.

---

## Navigation

â† Previous
Next â†’
