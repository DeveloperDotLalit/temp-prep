---
layout: default
title: Designing API Response Handlers
parent: Phase 7   Interview Scenarios
nav_order: 3
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Designing API Response Handlers"
parent: "Real-World Interview Scenarios"
nav_order: 3
---

# Designing API Response Handlers

<!-- Content starts here -->

Here are your interview-focused notes for the **"Design an API Response Handler"** scenario.

---

### **Scenario: "Design an API Response Handler"**

#### **The Goal**

The interviewer asks: _"How do you handle API responses in your ViewModel? How do you tell the UI to show a spinner, display data, or show an error dialog?"_

They want to see if you use a **Generic Wrapper** with **Sealed Classes** (The industry standard **LCE Pattern**: Loading, Content, Error).

#### **The Checklist (Mental Cheat Sheet)**

1. **Generic Class `<T>`:** Your wrapper must work for _any_ data (User, List of Posts, etc.).
2. **Sealed Class:** To restrict the types of responses to only the ones you define.
3. **Encapsulation:** The UI shouldn't have to check `if (error == null)` manually. The class type itself tells the UI what to do.

---

#### **The Problem (The "Bad" Way)**

Beginners often use separate variables in their ViewModel:

```kotlin
// ⚠️ BAD PRACTICE: Separate variables for one state
val isLoading = MutableLiveData<Boolean>()
val errorMessage = MutableLiveData<String?>()
val userData = MutableLiveData<User?>()

```

**Why this fails:**

- **Inconsistent State:** What if `isLoading` is true, but `errorMessage` is also set? Is it loading or did it fail?
- **Boilerplate:** You have to observe 3 different variables in the Activity.

---

#### **The Solution (The "Sealed" Way)**

We create a single wrapper class `NetworkResult<T>` that represents the **only** possible states.

```kotlin
// 1. The Generic Wrapper (The "Envelope")
sealed class NetworkResult<T> {
    // State 1: Loading (No data needed)
    class Loading<T> : NetworkResult<T>()

    // State 2: Success (Holds the data)
    data class Success<T>(val data: T) : NetworkResult<T>()

    // State 3: Error (Holds the message)
    data class Error<T>(val message: String, val cause: Throwable? = null) : NetworkResult<T>()
}

```

#### **Example Usage**

**In the Repository (The Producer):**

```kotlin
suspend fun getUser(id: String): NetworkResult<User> {
    return try {
        // Assume api.fetchUser() returns a User object
        val user = api.fetchUser(id)
        NetworkResult.Success(user)
    } catch (e: Exception) {
        NetworkResult.Error("Network failed: ${e.message}")
    }
}

```

**In the UI (The Consumer):**

```kotlin
fun updateUI(state: NetworkResult<User>) {
    // 2. The Exhaustive 'when' (Clean & Safe)
    when (state) {
        is NetworkResult.Loading -> {
            progressBar.isVisible = true
            errorText.isVisible = false
        }
        is NetworkResult.Success -> {
            progressBar.isVisible = false
            // Smart Cast: Kotlin knows 'state.data' exists here!
            showUserName(state.data.name)
        }
        is NetworkResult.Error -> {
            progressBar.isVisible = false
            showErrorDialog(state.message)
        }
    }
}

```

#### **Visual Representation**

```text
    [ ViewModel ]
         |
         | (Returns ONE object)
         v
    [ NetworkResult ]
    /       |       \
 [Loading] [Success] [Error]
             |         |
          [Data]    [Message]

```

#### **Interview Keywords**

LCE Pattern (Loading-Content-Error), Generic Wrapper, State Encapsulation, Single Source of Truth, Exhaustive `when`, Smart Casting.

> **Pro Interview Tip:** "How do you handle data persistence?"
> **Answer:** "In a more complex app, `Success` might come from the Database (Cache), and `Error` might still contain stale data to show the user while offline. I might add a field `data: T?` to the Error class so I can display the old data even if the refresh failed."

#### **Interview Speak Paragraph**

"I strictly avoid managing separate boolean flags like `isLoading` or `isError` because they lead to inconsistent states. Instead, I model my API responses using a **Generic Sealed Class**—typically named `NetworkResult<T>`. This allows me to define clear states: `Loading`, `Success` (containing the data), and `Error` (containing the message). This approach forces the UI to handle every scenario explicitly using a `when` expression and creates a single source of truth for the screen's state."

---

**Would you like to move on to the next scenario: "Scenario: Code Review Simulation" (Spotting bad practices)?**
