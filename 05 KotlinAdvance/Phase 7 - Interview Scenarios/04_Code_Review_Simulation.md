---
layout: default
title: "Code Review Simulation"
parent: "Advanced Kotlin: Phase 7   Interview Scenarios"
nav_order: 4
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Code Review Simulation"
parent: "Real-World Interview Scenarios"
nav_order: 4
---

# Code Review Simulation

<!-- Content starts here -->

Here are your interview-focused notes for the **"Code Review Simulation"** scenario.

---

### **Scenario: "Code Review Simulation"**

#### **The Goal**

The interviewer hands you a piece of code that _technically compiles_ but is **garbage** in terms of quality.
They want to see if you can spot **Bad Practices**, **Memory Leaks**, and **Crash Risks**.
Your job is to be the "Senior Engineer" who politely points out why the code is dangerous and how to fix it.

#### **The Checklist (The "Red Flags")**

1. **The Double Bang (`!!`):** Immediate red flag. Crash risk.
2. **`GlobalScope`:** Uncontrolled coroutine (Leak risk).
3. **Blocking Code (`Thread.sleep`):** Never use this in coroutines. Use `delay()`.
4. **Broken Encapsulation:** Public `var` / `MutableList` that anyone can modify.
5. **Context Issues:** Running heavy tasks on the Main thread (freezing UI).

---

#### **The Challenge (The "Smelly" Code)**

_Spot the 5 errors in this snippet:_

```kotlin
// A standard ViewModel
class UserViewModel : ViewModel() {

    // ERROR 1: Public Mutable List
    // Any screen can say "viewModel.users.clear()" and delete everything!
    var users = mutableListOf<User>()

    fun loadUsers() {
        // ERROR 2: GlobalScope
        // If the user closes the screen, this keeps running. Memory Leak.
        GlobalScope.launch {

            // ERROR 3: Blocking the Thread
            // This freezes the thread (and potentially the UI) for 1 second.
            Thread.sleep(1000)

            val response = api.getUsers()

            // ERROR 4: The '!!' operator
            // If API returns null, the app crashes.
            val list = response.body()!!

            // ERROR 5: Thread Safety / Race Condition
            // We are likely on a background thread here, but updating a list
            // that the Main Thread might be reading -> Crash.
            users.addAll(list)
        }
    }
}

```

---

#### **The Solution (The "Senior" Fix)**

**Step 1: Encapsulate State**
Use a private mutable list and a public immutable list (Backing Property).

**Step 2: Structured Concurrency**
Use `viewModelScope`. It cancels automatically.

**Step 3: Non-Blocking**
Use `delay()` instead of `Thread.sleep()`.

**Step 4: Safety**
Use `?.` safe calls and switch to the correct Dispatcher for updates.

```kotlin
class UserViewModel : ViewModel() {

    // Fix 1: Backing Property (Encapsulation)
    private val _users = mutableListOf<User>()
    val users: List<User> get() = _users // Public is Read-Only

    fun loadUsers() {
        // Fix 2: viewModelScope (Lifecycle Aware)
        viewModelScope.launch {

            // Fix 3: Suspend function (Non-blocking pause)
            delay(1000)

            // Fix 4: Exception Handling (Try-Catch)
            try {
                // Switch to IO for Network
                val response = withContext(Dispatchers.IO) {
                    api.getUsers()
                }

                // Fix 5: Safe Unwrapping & UI Update
                // 'body()' might be null, so we check it safely
                response.body()?.let { userList ->
                    _users.clear()
                    _users.addAll(userList)
                    // (In real apps, we'd post this to LiveData or Flow)
                }
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }
    }
}

```

#### **Visual Representation**

```text
    Bad Encapsulation:
    [ Activity ] ----( Can Delete! )----> [ MutableList ]
                                          (Unsafe)

    Good Encapsulation (Backing Property):
    [ Activity ] ----( Read Only )-----> [ List (Public) ]
                                              ^
                                              | (Get)
                                         [ MutableList (Private) ]
                                         (Only ViewModel can touch)

```

#### **Interview Keywords**

Code Smell, Defensive Programming, Backing Property, Thread Blocking vs Suspending, Race Condition, Encapsulation, Structured Concurrency.

> **Pro Interview Tip (Politeness):** Don't say "This code is trash."
> Say: _"I noticed a few potential stability issues here. For example, using `!!` creates a risk of runtime crashes. I would recommend using safe calls `?.` instead."_

#### **Interview Speak Paragraph**

"In this snippet, I see several critical issues. First, the usage of `GlobalScope` breaks structured concurrency, which could lead to memory leaks if the ViewModel is cleared. I would replace it with `viewModelScope`. Second, `Thread.sleep()` is a blocking call that wastes system resources; it should be replaced with the suspending function `delay()`. Third, the list is exposed as a public `MutableList`, breaking encapsulation. I would refactor this to use a 'Backing Property,' keeping the mutable version private. Finally, the use of `!!` on the API response is a ticking time bomb for NullPointerExceptions."

---

### **🎉 Phase 7 Complete!**

You have faced the **Real World**. You can Refactor Java, Debug Crashes, Design Architectures, and Review Code like a pro.

**Final Stop:**
Phase 8 is **Interview Questions & Answers**. This is the final rehearsal. I will give you the **Top 5 "Rapid Fire" Questions** that catch people off guard, and the **Behavioral Technical Answer** script.

**Shall we start Phase 8 with "Rapid Fire Theory"?**
