---
layout: default
title: Oncleared Cleanup And Memory Leaks
parent: Phase 3   Creation & Dependency Injection
nav_order: 3
---

Here are your detailed notes for the third topic of Phase 3.

---

### **Topic: `onCleared()` Method**

#### **What It Is**

`onCleared()` is the final lifecycle callback method inside a ViewModel. It is the **destructor** or the "last will and testament" of the ViewModel.

It is called exactly **once** in the ViewModel's life: right before the ViewModel object is destroyed and garbage collected.

#### **Why It Exists (The Problem)**

Even though the ViewModel prevents memory leaks by not holding Views, the ViewModel _itself_ can cause leaks if it starts background tasks that never stop.

Imagine your ViewModel opens a **Socket Connection**, starts a **Timer**, or subscribes to a **Data Stream** (like RxJava or a Location Listener).

- If the user closes the app (calls `finish()`), the ViewModel dies.
- **The Problem:** If you don't close that Socket or stop that Timer, it keeps running in the background, eating up battery and data. This is a **Resource Leak**.

`onCleared()` exists to give you a specific place to say: _"Stop everything, I am dying now."_

#### **How It Works**

The system knows the difference between a "Rotation" (Temporary destroy) and a "Finish" (Permanent destroy).

1. **User Rotates:** The Activity is destroyed, but the System knows it's a configuration change. It **DOES NOT** call `onCleared()`. The ViewModel stays alive.
2. **User Presses Back:** The Activity is destroyed, and the System knows it is "finishing."
3. **The Trigger:** The System calls `getViewModelStore().clear()`.
4. **The Hook:** This triggers the `onCleared()` method inside your ViewModel.
5. **The Cleanup:** You close your connections, and then the ViewModel is garbage collected.

**Visualizing the Cleanup:**

```text
[ User Action: Press BACK ]
       |
       v
[ Activity onDestroy() ]
       |
       |  "Is this a rotation?" -> NO.
       |  "Is the Activity finishing?" -> YES.
       |
       v
[ ViewModelStore.clear() ]
       |
       |  Loop through all ViewModels...
       |
       v
[ specificViewModel.onCleared() ] <--- YOUR CODE RUNS HERE
       |
       |  "Cancel Coroutines"
       |  "Unsubscribe RxJava"
       |  "Close Files"
       |
       v
[ Garbage Collection ]

```

#### **Example: Cleaning up RxJava (Classic Use Case)**

In modern Kotlin, `viewModelScope` handles coroutines automatically (it actually cancels itself inside `onCleared` internally!). However, if you use **RxJava** or manual threads, you **must** override this.

```kotlin
class MyViewModel : ViewModel() {

    // A bag to hold all our active background tasks (RxJava)
    private val disposables = CompositeDisposable()

    fun startDataStream() {
        val subscription = repository.getData()
            .subscribe { /* update UI */ }

        // Add this task to the bag
        disposables.add(subscription)
    }

    // This runs when the Activity is FINISHED (not rotated)
    override fun onCleared() {
        super.onCleared()

        // STOP everything.
        // If we don't do this, the stream keeps running even after the app closes!
        disposables.clear()

        Log.d("MyViewModel", "Cleaned up resources.")
    }
}

```

#### **Interview Keywords**

Resource Release, Memory Leak, Garbage Collection, `viewModelScope`, CompositeDisposable, Lifecycle termination, Backing properties.

#### **Interview Speak Paragraph**

> "`onCleared()` is the lifecycle hook designed for cleanup. It is called only when the lifecycle owner (the Activity or Fragment) is permanently destroyed—such as when the user hits the Back button—but _not_ during configuration changes like rotation. This is the critical place where we must cancel any long-running background operations that aren't lifecycle-aware, such as RxJava subscriptions, open file streams, or manual threads. If we fail to do this, these background tasks will continue running even after the UI is gone, leading to resource leaks and wasted battery."

---

**Next Step:**
We have cleaned up our resources. Now, let's look at how modern tools make this easier.
Shall we move to **Dependency Injection Integrations**: A high-level look at how libraries like Hilt generate factories for us automatically?
