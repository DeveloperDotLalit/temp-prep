---
layout: default
title: Debugging Crashes
parent: Phase 7   Interview Scenarios
nav_order: 2
---

﻿---
layout: default
title: "Debugging Crashes"
parent: "Real-World Interview Scenarios"
nav_order: 2
---

# Debugging Crashes

<!-- Content starts here -->

Here are your interview-focused notes for the **"Debug this crash"** scenario.

---

### **Scenario: "Debug this crash"**

#### **The Goal**

The interviewer shows you a block of code that _looks_ fine but causes the app to crash or freeze in production.
Your job is to spot the **"Silent Killers"**: logic that compiles correctly but fails at runtime.
The two biggest culprits in Kotlin Android interviews are **Hidden NPEs** and **Coroutine Leaks**.

#### **The Checklist (Mental Cheat Sheet)**

1. **The "Bang-Bang" (`!!`):** Are they forcing a null value?
2. **Platform Types (Java Interop):** Are they calling a Java function that returns `null` into a Kotlin non-null variable?
3. **Lateinit Vars:** Is `lateinit var` accessed before initialization?
4. **The Zombie Coroutine:** Is a task running on `GlobalScope` or a custom scope without cancellation? If the screen closes, does the task keep running and try to update a dead view?

---

#### **The Challenge (Broken Code)**

_Spot the bugs:_

```kotlin
class UserActivity : AppCompatActivity() {

    // BUG 1: Lateinit might not be ready
    private lateinit var userSettings: Settings

    fun onCreate() {
        // BUG 2: GlobalScope lives forever (Memory Leak / Crash)
        GlobalScope.launch(Dispatchers.Main) {
            val data = fetchData()

            // BUG 3: The '!!' Assertion (NPE risk)
            // If fetchData returns null, the app crashes immediately.
            updateUI(data!!)

            // BUG 4: Updating UI after Activity might be destroyed
            // If user closes app during fetchData(), this line crashes.
            userSettings.save(data)
        }
    }
}

```

---

#### **The Solution (The Fix)**

**Step 1: Fix the NPEs (`?` over `!!`)**
Never trust the API. Use `?.let` or `?: return`.

**Step 2: Fix the Leak (Structured Concurrency)**
Replace `GlobalScope` with `lifecycleScope` (Activity) or `viewModelScope` (ViewModel). These scopes automatically cancel the job when the screen is destroyed.

**Step 3: Safe Initialization**
Check `::userSettings.isInitialized` or, better yet, don't use `lateinit` if you can avoid it.

```kotlin
class UserActivity : AppCompatActivity() {

    // Fix 1: Make it nullable or lazy to avoid uninitialized crashes
    private var userSettings: Settings? = null

    fun onCreate() {
        // Fix 2: Use lifecycleScope (Automatically cancels if Activity dies)
        lifecycleScope.launch {
            val data = fetchData()

            // Fix 3: Handle null safely (Elvis operator)
            if (data == null) {
                showError()
                return@launch // Stop here
            }

            // Fix 4: Safe update
            updateUI(data) // 'data' is smart-cast to Non-Null here

            userSettings?.save(data)
        }
    }
}

```

#### **Visual Representation**

```text
    The Leak (GlobalScope):
    [ Activity Opens ] --> [ GlobalScope Task Starts ]
           |
    [ Activity Closes ]    (Task keeps running...)
                           (Task finishes)
                           (Task tries to find Activity) -> 💥 CRASH!

    The Fix (lifecycleScope):
    [ Activity Opens ] --> [ Scope Task Starts ]
           |
    [ Activity Closes ] -> [ Scope CANCELS Task ]
                           (Task stops safely) -> ✅ NO CRASH

```

#### **Interview Keywords**

Memory Leak, Structured Concurrency, Lifecycle-Aware, `GlobalScope` (Anti-pattern), `!!` operator, Platform Types, `isInitialized`, Race Condition.

> **Pro Interview Tip (Platform Types):** "If you call a Java method `String getName()` from Kotlin, Kotlin sees it as `String!`. This is a **Platform Type**. It means 'I don't know if this is nullable or not.' If you treat it as non-null (`val s: String = javaObj.getName()`) and it returns null, you get an NPE. **Always** treat Java calls as nullable (`val s: String?`) unless the Java code has `@NonNull` annotations."

#### **Interview Speak Paragraph**

"In the provided snippet, I see two major issues. First, the use of the `!!` operator on the API response is unsafe; if the network call returns null, the app will crash with an NPE. I would replace this with a safe call `?.let` or an Elvis operator check. Second, using `GlobalScope` creates a potential memory leak and crash risk. If the user closes the Activity before `fetchData` completes, the coroutine continues running and attempts to update a destroyed view. I would refactor this to use `lifecycleScope` or `viewModelScope` to ensure **Structured Concurrency**, guaranteeing the task is cancelled automatically when the lifecycle ends."

---

**Would you like to move on to the next scenario: "Scenario: Design an API Response Handler"?**
