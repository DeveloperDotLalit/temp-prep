---
layout: default
title: "Androidviewmodel Vs Viewmodel"
parent: "Phase 3: Creation & Dependency Injection"
nav_order: 2
---

Here are your detailed notes for the second topic of Phase 3.

---

### **Topic: AndroidViewModel vs. ViewModel**

#### **What It Is**

When creating a ViewModel, you have two class options to extend:

1. **`ViewModel` (Standard):** The default, pure class. It has no knowledge of the Android system (no Context).
2. **`AndroidViewModel` (Specialized):** A subclass that includes a reference to the **Application Context**.

#### **Why It Exists (The Problem)**

In Android, many operations require a `Context`.

- You want to load a string resource: `context.getString(R.string.welcome)`.
- You want to access Shared Preferences: `PreferenceManager.getDefaultSharedPreferences(context)`.
- You want to access a System Service (like Location or Wifi).

If you use a standard `ViewModel`, you don't have a `Context`. You might be tempted to pass your Activity into the ViewModel. **This is a trap.**

`AndroidViewModel` exists to give you a **Safe Context** (the Application Context) to perform these tasks without crashing the app.

#### **How It Works & The Danger**

This is one of the most critical concepts in Android memory management.

**1. The "Activity Context" Trap (DANGER!)**
If you pass an **Activity** to a ViewModel, you cause a massive **Memory Leak**.

- **Scenario:** User rotates the screen.
- **Action:** System destroys Activity A.
- **The Leak:** The ViewModel is _still alive_ (because that's its job!). It is holding onto Activity A.
- **Result:** The Garbage Collector cannot delete Activity A because the ViewModel is gripping it tight. Activity A sits in memory like a "Zombie," wasting RAM.

**2. The "Application Context" Solution (Safe)**
`AndroidViewModel` holds the **Application Context**.

- The Application Context lives as long as the app runs.
- It is **never** destroyed or recreated on rotation.
- Therefore, it is safe for the ViewModel to hold onto it.

**Visualizing the Leak:**

```text
[ SCENARIO: DANGEROUS ]                  [ SCENARIO: SAFE (AndroidViewModel) ]
ViewModel holds ref to Activity          ViewModel holds ref to Application

    [ ViewModel ]                              [ AndroidViewModel ]
          |                                            |
          | (Strong Reference)                         | (Strong Reference)
          v                                            v
[ Activity Instance ]                      [ Application Instance ]
(Attempts to die on Rotate)                (Lives forever while app runs)
          |                                            |
   System: "Delete this!"                       System: "This is fine."
          |
   Memory: "I can't! ViewModel
            is holding it!"
          |
     [ MEMORY LEAK ]

```

#### **Example: When to use which**

**Use `ViewModel` (Recommended):**

- For 90% of cases.
- When you just need to hold data (Strings, Ints, Lists).
- When your architecture passes data sources (Repositories) via the constructor.

**Use `AndroidViewModel`:**

- When you specifically need a Context _inside_ the ViewModel.
- Example: Getting a localized string or accessing a simple file/preference directly.

**Code Comparison:**

```kotlin
// BAD: Don't do this!
class BadViewModel(private val activity: Activity) : ViewModel() {
    // If activity dies, this class keeps it alive -> LEAK!
}

// GOOD: Use AndroidViewModel if you need Context
class MySettingsViewModel(application: Application) : AndroidViewModel(application) {

    fun getSavedSetting() {
        // We can safely use 'getApplication()' here
        val prefs = PreferenceManager.getDefaultSharedPreferences(getApplication())
        // ...
    }
}

```

#### **Interview Keywords**

Memory Leak, Garbage Collection, Context, Application Context vs. Activity Context, WeakReference, Modularization.

#### **Interview Speak Paragraph**

> "The main difference lies in how they handle the Context. Standard `ViewModel` is pure and should not hold any reference to Android framework classes, especially `Views` or `Activities`, to avoid memory leaks. However, sometimes we need a Context for things like System Services or Resources. in those specific cases, we use `AndroidViewModel`, which provides access to the `Application` Context. The Application Context is safe to hold because its lifecycle matches the application's lifespan, unlike an Activity Context, which can be destroyed and recreated on rotation."

---

**Next Step:**
We know how to create them. Now we need to know how to clean them up properly.
Shall we move to **`onCleared()` Method**: The cleanup hook?
