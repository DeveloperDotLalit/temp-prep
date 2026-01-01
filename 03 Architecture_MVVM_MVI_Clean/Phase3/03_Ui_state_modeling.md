---
layout: default
title: Ui State Modeling
parent: Phase3
nav_order: 3
---

Here are your focused notes on **UI State Modeling**.

This is one of the most effective ways to prevent bugs in your UI code.

---

### **Topic: UI State Modeling**

#### **What It Is**

UI State Modeling means defining a **Single Object** that represents the entire state of your screen at any given moment.

Instead of having separate variables floating around, you group everything into one strict "State" class using a Kotlin **Sealed Class**.
Common states are:

1. **Loading:** The spinner is spinning.
2. **Success:** The data is here (and contains the List of items).
3. **Error:** Something went wrong (and contains the error message).

#### **Why It Exists (The Problem)**

The "Old Way" was to use separate variables.

- `var isLoading: Boolean`
- `var userList: List<User>`
- `var errorMessage: String`

**The Bug:** What happens if `isLoading = true` AND `errorMessage = "No Internet"` at the same time?

- Does the app show the spinner? Or the error text? Or both overlapping each other?
- This is called an **"Illegal State."** It shouldn't be possible, but bugs happen.

UI State Modeling fixes this. Just like a traffic light can't be Red and Green at the same time, your app shouldn't be "Loading" and "Error" at the same time.

#### **How It Works (The Sealed Class)**

We use a **Sealed Class** (or Interface) in Kotlin. A sealed class allows us to define a fixed set of possibilities. The View _must_ handle every possibility.

1. **Define:** Create a `sealed class UiState`.
2. **Emit:** The ViewModel pushes strictly _one_ of these states at a time.
3. **Render:** The View checks "Which state is this?" and draws _only_ that state.

#### **Example (The Traffic Light)**

**❌ The Bad Way (Separate Variables):**

```kotlin
// In ViewModel
val isLoading = MutableLiveData<Boolean>()
val data = MutableLiveData<String>()
val error = MutableLiveData<String>()

// In Activity: You have to manually toggle visibility for EVERYTHING
if (loading) {
    progressBar.visibility = View.VISIBLE
    errorText.visibility = View.GONE // If you forget this, they overlap!
    dataView.visibility = View.GONE
}

```

**✅ The Good Way (UI State):**

```kotlin
// 1. Define the specific states
sealed class ScreenState {
    object Loading : ScreenState()
    data class Success(val data: String) : ScreenState()
    data class Error(val message: String) : ScreenState()
}

// 2. In Activity: clearer and safer
fun render(state: ScreenState) {
    // Kotlin 'when' forces us to handle all cases
    when (state) {
        is ScreenState.Loading -> {
            progressBar.isVisible = true
            errorText.isVisible = false
            dataView.isVisible = false
        }
        is ScreenState.Success -> {
            progressBar.isVisible = false
            dataView.text = state.data // Data only exists in Success state!
            dataView.isVisible = true
        }
        is ScreenState.Error -> {
            progressBar.isVisible = false
            errorText.text = state.message
            errorText.isVisible = true
        }
    }
}

```

#### **Interview Keywords**

Sealed Class, UI State, Illegal States, Deterministic UI, Single Source of Truth, Exhaustive When.

#### **Interview Speak Paragraph**

> "I model my UI state using Kotlin Sealed Classes rather than managing multiple boolean flags like `isLoading` or `isError`. This eliminates 'illegal states'—for example, it prevents the app from accidentally showing a loading spinner and an error message at the same time. By defining specific states like `Loading`, `Success`, and `Error`, the UI code becomes deterministic: it simply takes the current state object and renders exactly what is needed, reducing bugs and complexity."

---

**Would you like to proceed to the next note: "Introduction to MVI (Model-View-Intent)"?** (This is the final topic of Phase 3).
