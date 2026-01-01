---
layout: default
title: LifeCycles
parent: The Question Bank
nav_order: 1
---

# Android LifeCycles

## Can you describe the Android Activity lifecycle and explain the difference between onStart(), onResume(), and onPause()?

Here is a list of some of the most common and important questions an experienced Android developer is asked in interviews, presented in the specified format:

---

## 🧠 Common Android Developer Interview Questions

### 1. **Activity Lifecycle**

| Role/Category                         | Question                                                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Foundation/Core**                   | **Can you describe the Android Activity lifecycle and explain the difference between `onStart()`, `onResume()`, and `onPause()`?**   |
| **What the Interviewer is Expecting** | \* A clear, structured description of the 7 main lifecycle states.                                                                   |
|                                       | \* Understanding of when an Activity is considered "visible" versus "in the foreground" and "interactive."                           |
|                                       | \* Knowledge of where to save simple UI state (`onPause()`) versus where to save more persistent data (`onStop()` or `onDestroy()`). |
|                                       | \* **Crucially:** Understanding when the system can destroy the process without further notification (after `onStop()`).             |

> **Proper Answer:**
> "The Activity lifecycle is one of the most fundamental concepts in Android. It's the series of callbacks the system invokes as an Activity transitions between states. The key methods are `onCreate()`, `onStart()`, `onResume()`, `onPause()`, `onStop()`, `onDestroy()`, and `onRestart()`.
> The key differences you asked about are:
>
> - **`onStart()`:** The Activity is becoming **visible** to the user, but it may not yet be in the foreground. This is where you might register a `BroadcastReceiver` or start animations.
> - **`onResume()`:** The Activity is now **in the foreground** and **interactive**. This is the state where the user can interact with your app. You typically open resources that need to be actively used here, such as connecting to a camera.
> - **`onPause()`:** This is the first indication that the user is leaving your Activity. The Activity is still visible (e.g., a semi-transparent dialog is over it), but it's about to be hidden. It's crucial to release resources that consume CPU/battery (like stopping animations or camera access) and to save any simple, non-persistent UI state, as the next callback might be `onStop()` or, in rare cases, a return to `onResume()`."

### 2. **Process and Threading**

| Role/Category                         | Question                                                                                                                                                                           |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Performance/Concurrency**           | **How do you handle background tasks in Android, and what are the main differences between `Service`, `WorkManager`, and coroutines?**                                             |
| **What the Interviewer is Expecting** | \* A deep understanding of the **Main Thread** (UI thread) and the need to offload work.                                                                                           |
|                                       | \* Knowledge of the modern, recommended approaches (e.g., `WorkManager` for deferrable background tasks, coroutines for in-app concurrency).                                       |
|                                       | \* The ability to differentiate between tasks that need to run immediately, tasks that must persist beyond the app's process, and tasks that are tied to the Activity's lifecycle. |
|                                       | \* Mentioning the concept of **Application Not Responding (ANR)**.                                                                                                                 |

> **Proper Answer:**
> "In Android development, performance and responsiveness are paramount, which means all non-UI blocking operations must be offloaded from the Main Thread to prevent an **ANR** error.
> The modern approach favors:
>
> 1. **Coroutines (for in-app concurrency):** This is my primary tool for asynchronous work within an Activity or ViewModel. They allow us to write sequential-looking asynchronous code and are perfect for tasks like making network calls or reading from a database without blocking the UI. They are lifecycle-aware when used with `ViewModelScope` or `LifecycleScope`.
> 2. **WorkManager (for deferrable, guaranteed execution):** This is the preferred solution for tasks that must run, even if the user leaves the app or the device is rebooted (e.g., syncing data, uploading logs). It respects system constraints (like network availability, charging state) and handles task persistence and retries automatically.
> 3. **Services (for persistent tasks):** A `Service` is an application component for long-running operations. Modern Android development generally recommends using **Foreground Services** _only_ when the task is user-facing and ongoing (e.g., media playback, fitness tracking), and you must show a persistent Notification. Otherwise, `WorkManager` is the better choice."

### 3. **Architecture**

| Role/Category                         | Question                                                                                                                                        |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maintainability/Scalability**       | **What architectural pattern do you use, and why do you prefer it over others? Can you briefly explain the components of your chosen pattern?** |
| **What the Interviewer is Expecting** | \* Familiarity with standard patterns like MVVM, MVP, or MVI.                                                                                   |
|                                       | \* A clear explanation of the separation of concerns (who does what).                                                                           |
|                                       | \* Mentioning the benefits of testability and maintainability.                                                                                  |
|                                       | \* **Crucially:** Understanding how Google's Jetpack components (e.g., `LiveData`, `ViewModel`, `Room`) fit into this pattern.                  |

> **Proper Answer:**
> "I predominantly use the **MVVM (Model-View-ViewModel)** architectural pattern. It's the de-facto standard in modern Android development because it integrates seamlessly with the **Android Architecture Components** library.
> Here’s a brief breakdown:
>
> - **View (Activity/Fragment):** Only responsible for rendering the UI and handling user input. It holds a reference to the ViewModel and observes state changes. It is deliberately passive.
> - **ViewModel (Jetpack ViewModel):** Acts as a bridge between the View and the Data layer. It holds and manages UI-related data in a lifecycle-aware way (survives configuration changes). It exposes data to the View, typically via `LiveData` or Kotlin `StateFlow`.
> - **Model/Data Layer (Repository Pattern):** This is responsible for business logic and data retrieval. It acts as the single source of truth, abstracting data sources (e.g., a local Room database, a remote API, or SharedPreferences). The ViewModel communicates with the Repository, and the Repository decides where the data comes from.
>
> I prefer MVVM because it makes my code highly **testable** (I can easily test the ViewModel and Repository without needing an Android device) and significantly improves **separation of concerns** and **maintainability**."

---
