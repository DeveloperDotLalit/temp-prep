---
layout: default
title: Refactoring Bloated Viewmodels
parent: Phase6
nav_order: 1
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Refactoring Bloated ViewModels**.

This is a very common scenario in "Take Home Assignments" or code reviews during interviews. They want to see if you can clean up a mess.

---

### **Topic: Refactoring Bloated ViewModels**

#### **What It Is**

A **"Bloated ViewModel"** (or Fat ViewModel) is a class that has grown too large. It knows too much and does too much.
Instead of just holding state, it starts handling:

- Formatting strings (UI logic).
- Calculating math (Business logic).
- Parsing errors (Data logic).
- Managing overly complex flows.

**Refactoring** is the process of cutting this fat and moving logic to where it truly belongs (Use Cases, Mappers, or Utility classes).

#### **Why It Exists (The Problem)**

1. **The "Kitchen Sink" Effect:** Since the ViewModel is the connector between UI and Data, it's the easiest place to dump code. "I'll just put this check here for now" turns into a 1000-line file.
2. **Violation of SRP:** It violates the Single Responsibility Principle. A ViewModel should manage **State**, not calculate tax rules or format dates.
3. **Unreadable & Untestable:** A giant file is hard to read. Testing it requires mocking 15 different dependencies, which is a nightmare.

#### **How It Works (The Cleanup Strategy)**

We use **Delegation**. The ViewModel should act like a **Traffic Cop**, directing traffic, not driving the cars.

**Technique 1: Extract Business Logic -> Use Cases**

- _Bad:_ `if (password.length > 5 && password.hasUpper())` inside ViewModel.
- _Good:_ Call `validatePasswordUseCase(password)`.

**Technique 2: Extract Formatting -> Mappers / UI Models**

- _Bad:_ `val dateString = SimpleDateFormat...` inside ViewModel.
- _Good:_ The ViewModel receives a raw Date. The **Mapper** converts it to a String before the View sees it.

**Technique 3: Composition (Breaking it down)**

- If a ViewModel manages 3 different features (e.g., User Profile, Settings, and Friends), break it into smaller, specific ViewModels or use "Delegates" to handle chunks of logic.

#### **Example (The Diet Plan)**

**❌ Before (The Bloated Mess):**

```kotlin
class SignUpViewModel(private val api: Api) : ViewModel() {

    fun onSignUpClick(email: String, pass: String) {
        // 1. Validation Logic (Should be Domain)
        if (!email.contains("@")) {
            _error.value = "Invalid Email"
            return
        }

        // 2. Formatting Logic (Should be Mapper)
        val cleanEmail = email.trim().lowercase()

        // 3. Network Logic (Should be Repository)
        viewModelScope.launch {
            try {
                api.signUp(cleanEmail, pass)
                _state.value = Success
            } catch (e: Exception) {
                // 4. Error Parsing (Should be generic handler)
                _error.value = e.message
            }
        }
    }
}

```

**✅ After (The Lean Traffic Cop):**

```kotlin
class SignUpViewModel(
    private val signUpUseCase: SignUpUseCase, // 1. Logic moved here
    private val errorMapper: ErrorMapper      // 2. Parsing moved here
) : ViewModel() {

    fun onSignUpClick(email: String, pass: String) {
        viewModelScope.launch {
            // The ViewModel just calls "Execute" and handles the result
            val result = signUpUseCase(email, pass)

            when(result) {
                is Result.Success -> _state.value = SignUpState.Success
                is Result.Error -> _state.value = errorMapper.map(result.error)
            }
        }
    }
}

```

#### **Interview Keywords**

Refactoring, Single Responsibility Principle (SRP), Delegation, Composition, Spaghetti Code, Fat ViewModel, Use Case Extraction.

#### **Interview Speak Paragraph**

> "I strictly keep my ViewModels lean. Their only responsibility should be managing the UI state and handling user intents. If I see a ViewModel performing data validation, string formatting, or complex business math, I consider it a 'code smell.' I refactor this by extracting business rules into reusable Use Cases and moving data formatting into Mapper classes. The ViewModel should act as a coordinator—delegating tasks to these specialized classes—rather than doing the heavy lifting itself."

---

**Would you like to proceed to the next note: "Shared ViewModels (Fragment Communication)"?**
