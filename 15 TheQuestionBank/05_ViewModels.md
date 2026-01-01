---
layout: default
title: ViewModels
parent: The Question Bank
nav_order: 5
---

# ViewModels Internals

## Do you know about the viewmodel? Do you know how the viewmodel works internally?

That's a core question regarding modern Android Architecture Components. A strong understanding of the **ViewModel** is essential for any experienced developer.

| Role/Category                         | Question                                                                                                                                |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Android Architecture/Jetpack**      | **Can you explain what the Android ViewModel is, the problem it solves, and how it works internally to survive configuration changes?** |
| **What the Interviewer is Expecting** | \* The core concept: A **lifecycle-aware** data holder for the UI.                                                                      |
|                                       | \* The problem solved: **Surviving configuration changes** (e.g., screen rotation) and preventing memory leaks.                         |
|                                       | \* Internal mechanism: How it's associated with a **`ViewModelStoreOwner`** and retained across Activity/Fragment re-creations.         |
|                                       | \* Distinction from the View (separation of concerns).                                                                                  |

> **Proper Answer:**
> "The Android `ViewModel` is a critical component of the Android Architecture Components, designed to hold and manage UI-related data in a **lifecycle-aware** way.
>
> ### **The Problem it Solves**
>
> The traditional pain point in Android was **configuration changes**, such as screen rotation. When an Activity is destroyed and re-created due to rotation, any data held within the Activity itself (like network results or user input) is lost.
> The `ViewModel` solves this by **retaining its state** across these re-creations, ensuring the user experience is seamless and that we avoid redundant network calls or database fetches.
>
> ### **Core Principles**
>
> 1. **Data Holder:** Its primary responsibility is to hold the data the UI needs (the _state_) and expose methods to fetch or update that data.
> 2. **No Direct View References:** Crucially, a `ViewModel` **must never hold a reference** to the View (Activity, Fragment, or any Android context-bound object) to prevent severe **memory leaks**.
> 3. **Lifecycle Awareness:** It's designed to live longer than the specific Activity/Fragment instance.
>
> ### **Internal Working: How it Survives**
>
> The magic behind `ViewModel` survival lies in a separate class called the **`ViewModelStore`**, which is managed by a **`ViewModelStoreOwner`**.
>
> 1. **`ViewModelStoreOwner`:** This is the interface implemented by Activities, Fragments, and other lifecycle owners. It owns the **`ViewModelStore`**.
> 2. **`ViewModelStore`:** This is a simple container class (essentially a `HashMap`) that stores the actual `ViewModel` instances. It lives _outside_ the Activity's standard lifecycle destruction path during a configuration change.
> 3. **The Process:**
>
> - **First Creation:** When you call `ViewModelProvider(this).get(MyViewModel::class.java)`, the system checks the `ViewModelStore` (which belongs to the current `ViewModelStoreOwner`). If the `ViewModel` is not found, it creates a new one and stores it.
> - **Configuration Change (Rotation):** The Activity is destroyed, but the system marks the associated `ViewModelStore` as **retained**—it is _not_ destroyed.
> - **Re-creation:** When the Activity is re-created, the `ViewModelProvider` uses the same `ViewModelStoreOwner` instance. It checks the store, finds the existing `ViewModel` instance, and returns it to the new Activity instance.
> - **Final Destruction:** The `ViewModelStore` is finally cleared, and the `ViewModel`'s `onCleared()` method is called only when the **owning Activity/Fragment is finished permanently** (e.g., the user presses back and leaves the screen)."

Is there anything else you'd like to discuss about the ViewModel, such as the **`SavedStateHandle`** or how it interacts with **Flow**?

---

---

## Give me in detailed working of the viewmodels internally?

This is a perfect follow-up question. While the previous answer provided a high-level overview, a detailed explanation of the internal mechanisms of the `ViewModel` is necessary for an experienced role.

| Role/Category                                | Question                                                                                                                                                                                                     |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Android Architecture/Jetpack (Deep Dive)** | **Can you explain the detailed internal working of the ViewModel, specifically focusing on the roles of `ViewModelStoreOwner`, `ViewModelStore`, and the `ViewModelProvider` during configuration changes?** |
| **What the Interviewer is Expecting**        | \* A step-by-step breakdown of the interaction between the three core classes.                                                                                                                               |
|                                              | \* The crucial role of the **Non-Configuration Instance/Non-Config Host** in retaining the data structure across the death/re-creation of the Activity.                                                      |
|                                              | * A clear explanation of *when\* `onCleared()` is called.                                                                                                                                                    |
|                                              | \* Knowledge of how the factory creates the ViewModel instance.                                                                                                                                              |

> **Proper Answer:**
> "The internal workings of the ViewModel are elegant and entirely based on the concept of retaining a data container across the OS-managed destruction and re-creation cycle of a lifecycle owner.
> The process involves three key players: the **`ViewModelStoreOwner`**, the **`ViewModelStore`**, and the **`ViewModelProvider`**.
>
> ### **1. The `ViewModelStoreOwner` (Activity/Fragment)**
>
> An Activity or Fragment implementing the `ViewModelStoreOwner` interface is responsible for hosting the persistence mechanism.
>
> - When the owning component is a **Fragment**, the `ViewModelStore` is managed by the Fragment Manager.
> - When the owning component is an **Activity**, the `ViewModelStore` is hosted within a **Non-Config Host** (an internal class) that is retained across configuration changes using the legacy Android mechanism known as the **Non-Configuration Instance**.
>
> ### **2. The `ViewModelStore` (The Container)**
>
> The `ViewModelStore` is the actual, simple container—essentially a **`HashMap<String, ViewModel>`**—that holds the ViewModel instances.
>
> - During a configuration change (e.g., rotation), the OS destroys the Activity, but the system prevents the Activity's **Non-Config Host** from being garbage collected. This Host holds the reference to the `ViewModelStore`.
> - Thus, the `ViewModelStore` (and all the ViewModels inside it) is **retained** in memory, living longer than the Activity instance.
>
> ### **3. The `ViewModelProvider` (The Broker)**
>
> The `ViewModelProvider` is the class that handles the lifecycle logic and instance management.
> **Step 1: Get the Store**
> When the Activity (or Fragment) is created and calls the standard:
>
> ```kotlin
> val viewModel = ViewModelProvider(this).get(MyViewModel::class.java)
>
> ```
>
> The `ViewModelProvider` first requests the **`ViewModelStore`** from the `ViewModelStoreOwner` (`this`).
> **Step 2: Check the Cache**
> The `ViewModelProvider` attempts to look up a ViewModel instance of type `MyViewModel` in the retained `ViewModelStore`.
>
> - **On Initial Creation:** The ViewModel is **not** found. The Provider uses the registered **`ViewModelProvider.Factory`** (often `AndroidViewModelFactory` or a custom factory) to create a **new** instance of `MyViewModel`. This new instance is then placed into the `ViewModelStore`.
> - **After Configuration Change:** The ViewModel **is** found in the retained `ViewModelStore`. The Provider simply returns the existing, retained instance to the newly created Activity/Fragment.
>
> ### **When is `onCleared()` Called?**
>
> The `ViewModelStore` is only cleared, triggering the `ViewModel`'s `onCleared()` callback, when the associated `ViewModelStoreOwner` is **permanently finished**—not when it is temporarily destroyed for a configuration change.
> **Example Scenarios:**
>
> - **`onCleared()` Called:** The user presses the system Back button and leaves the screen, or the system calls `finish()` on the Activity.
> - **`onCleared()` NOT Called:** Screen rotation, multi-window mode changes, or language changes."

Would you like to focus on the **`SavedStateHandle`**, which is the mechanism for persisting small pieces of data even through process death?

---

---
