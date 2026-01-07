---
layout: default
title: Handling UI Events (MVI concepts)
parent: 7. Clean MVVM with Compose
nav_order: 3
---

# Handling UI Events (MVI concepts)

Here are your notes for **Topic 7.3**.

---

## **Topic 7.3: Handling UI Events (MVI concepts)**

### **1. What It Is**

This topic covers how the UI talks to the ViewModel.
Instead of the UI calling 20 different functions like `viewModel.login()`, `viewModel.typeEmail()`, `viewModel.reset()`, we use **MVI (Model-View-Intent)** concepts.

- **Intents (User Actions):** We define a `Sealed Class` that represents **every possible thing** the user can do on that screen.
- **The Processor:** The ViewModel has a **single public function** (usually named `onEvent` or `onAction`) that takes this sealed class and decides what to do.

### **2. Why It Exists (The "Spaghetti" Fix)**

- **Decoupling:** The UI is dumb. It shouldn't know _how_ to log in. It should just announce "The Login Button was clicked."
- **Traceability:** If a bug occurs, you can log every single `UserEvent` that entered the ViewModel. You get a perfect history of what the user did: `[TypeEmail, TypePassword, ClickLogin]`.
- **Scalability:** Adding a new button just means adding one line to the Sealed Class and one branch to the `when` statement.

### **3. How It Works**

#### **A. Modeling Actions (The Sealed Class)**

Define interaction as data, not functions.

```kotlin
// The "Menu" of all possible actions
sealed interface LoginUiEvent {
    data class EmailChanged(val value: String): LoginUiEvent
    data class PasswordChanged(val value: String): LoginUiEvent
    data object LoginClicked: LoginUiEvent
}

```

#### **B. Processing Actions (The ViewModel)**

One entry point to rule them all.

```kotlin
fun onEvent(event: LoginUiEvent) {
    when(event) {
        is LoginUiEvent.EmailChanged -> { _state.value = _state.value.copy(email = event.value) }
        is LoginUiEvent.LoginClicked -> { performLogin() }
    }
}

```

#### **C. State vs. One-Time Events (Crucial Distinction)**

- **UI State (StateFlow):** Persistent. "The loading spinner is visible." If you rotate the phone, it is **still** visible.
- **One-Time Events (Channel/SharedFlow):** Transient. "Show a Toast", "Navigate to Home". If you rotate the phone, the Toast should **not** show again. (Covered in Topic 7.2).

### **4. Example: The MVI Loop**

**The ViewModel**

```kotlin
@HiltViewModel
class LoginViewModel @Inject constructor() : ViewModel() {

    // Single Entry Point
    fun onEvent(event: LoginEvent) {
        when(event) {
            is LoginEvent.OnEmailChange -> { /* update state */ }
            is LoginEvent.OnSubmit -> {
                // Trigger One-Time Event (Navigation)
                viewModelScope.launch { _uiEvent.send(UiEvent.NavigateHome) }
            }
        }
    }
}

```

**The UI (Composable)**

```kotlin
@Composable
fun LoginScreen(viewModel: LoginViewModel) {
    // UI just passes data objects. It calls NO logic functions.
    TextField(
        value = state.email,
        onValueChange = { text ->
            viewModel.onEvent(LoginEvent.OnEmailChange(text))
        }
    )

    Button(
        onClick = {
            viewModel.onEvent(LoginEvent.OnSubmit)
        }
    ) { Text("Login") }
}

```

### **5. Interview Prep**

**Interview Keywords**
MVI (Model-View-Intent), Sealed Interface, Single Entry Point, User Intent, `onEvent`, Separation of Logic, Event vs. State.

**Interview Speak Paragraph**

> "I prefer managing user interactions using the MVI pattern. Instead of exposing multiple functions in the ViewModel like `updateName()` or `submitForm()`, I define a single sealed interface called `UiEvent` or `UserIntent` that represents all user actions. The ViewModel exposes a single `onEvent(event: UiEvent)` function. This makes the data flow unidirectional and highly traceable. It separates 'What happened' (the Event) from 'How to handle it' (the Logic), making the codebase cleaner and easier to debug."

---

**Next Step:**
We have a clean architecture. Now, how do we glue the ViewModel into the Screen?
Ready for **Topic 7.4: Dependency Injection (Hilt/Koin)**? This explains `@HiltViewModel`.

---

## Navigation

â† Previous
Next â†’
