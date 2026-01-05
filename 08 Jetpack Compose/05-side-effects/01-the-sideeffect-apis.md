---
layout: default
title: The Side-Effect APIs
parent: 5. Side-Effects & Lifecycles
nav_order: 1
---

# The Side-Effect APIs

Here are your notes for **Topic 5.1**.

---

# Topic 5: Side-Effects & Lifecycles

This section is where many developers introduce bugs. Since Composable functions can run dozens of times a second (recomposition), putting a network call or a database save directly in the function body is a disaster. You need "Safe Zones" to run this code. These safe zones are called **Side-Effect APIs**.

## **Topic 5.1: The Side-Effect APIs**

### **1. What It Is**

A **Side-Effect** is any action that escapes the scope of the Composable function.

- **Pure UI:** "Take name 'Alex', return Text('Alex')." (Safe to run 100 times).
- **Side Effect:** "Log to Analytics", "Start a Timer", "Listen to Sensor", "Update System Status Bar". (Must run exactly when needed, not on every redraw).

Compose provides specific APIs to handle these: `LaunchedEffect`, `SideEffect`, and `DisposableEffect`.

### **2. Why It Exists (The "Recomposition" Trap)**

If you write `Log.d("Tag", "Hello")` inside a Composable, it might print 50 times just because a scrolling animation happened nearby.
You need a way to tell Compose:

- "Run this code **only once** when the screen opens."
- "Run this code **only when** `userId` changes."
- "Run this code and **clean it up** when the screen closes."

### **3. How It Works (The Big Three)**

#### **A. `LaunchedEffect` (Coroutines / Suspend Functions)**

- **Use Case:** Running async tasks (loading data, showing a Snackbar, starting a timer).
- **Behavior:** It launches a Coroutine in the scope of the Composable.
- **Enter:** Starts the coroutine.
- **Leave:** Automatically cancels the coroutine.
- **Key Change:** If the `key` parameter changes, it cancels the old one and starts a new one.

#### **B. `DisposableEffect` (Cleanup Required)**

- **Use Case:** Anything that needs a "Start" and a "Stop" (Listeners, BroadcastReceivers, Sensor Managers).
- **Behavior:**
- **Enter:** Runs the effect.
- **Leave:** **MUST** run the `onDispose` block to clean up.
- **Key Change:** Disposes the old one, starts the new one.

#### **C. `SideEffect` (Publish to Non-Compose)**

- **Use Case:** Communicating with external non-Compose code _after_ a successful recomposition. (e.g., Updating the Android Status Bar color or updating a `StringBuilder` for logging).
- **Behavior:** Runs on **every** successful recomposition. It does _not_ support suspend functions.

### **4. Example: When to use which?**

**Scenario A: Show a Snackbar (LaunchedEffect)**
We only want to show the snackbar when `errorMessage` changes, not on every frame.

```kotlin
@Composable
fun ErrorScreen(errorMessage: String, snackbarHostState: SnackbarHostState) {
    // Key = errorMessage. If the message changes, the effect restarts.
    LaunchedEffect(errorMessage) {
        if (errorMessage.isNotEmpty()) {
            snackbarHostState.showSnackbar(errorMessage)
        }
    }
}

```

**Scenario B: Listen to Keyboard Visibility (DisposableEffect)**
We need to attach a listener when the screen opens and **remove** it when it closes to avoid memory leaks.

```kotlin
@Composable
fun KeyboardListener() {
    val context = LocalContext.current

    DisposableEffect(Unit) { // Unit = Run once on enter
        val listener = ViewTreeObserver.OnGlobalLayoutListener {
            /* Check keyboard */
        }

        val view = (context as Activity).window.decorView
        view.viewTreeObserver.addOnGlobalLayoutListener(listener)

        // CLEANUP IS MANDATORY
        onDispose {
            view.viewTreeObserver.removeOnGlobalLayoutListener(listener)
        }
    }
}

```

**Scenario C: Analytics / Status Bar (SideEffect)**
Update the system bar color to match the current theme state.

```kotlin
@Composable
fun SystemBarUpdater(color: Color) {
    val systemUiController = rememberSystemUiController()

    // Runs after every successful draw to ensure system bars are in sync
    SideEffect {
        systemUiController.setSystemBarsColor(color)
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Side-effect, `LaunchedEffect`, `DisposableEffect`, `onDispose`, Recomposition Loop, Coroutine Scope, Cleanup, Structured Concurrency.

**Interview Speak Paragraph**

> "In Compose, we must isolate non-UI logic from the standard composition phase to avoid bugs caused by frequent recomposition. I use `LaunchedEffect` for firing one-off asynchronous events or coroutines, like showing a snackbar or fetching initial data. For operations that require cleanup—like registering a BroadcastReceiver or a Sensor listener—I use `DisposableEffect` to ensure the listener is detached when the composable leaves the screen. Finally, for syncing Compose state with the legacy Android system (like updating the Status Bar color), I use `SideEffect`, which ensures the update happens only after a successful composition."

---

**Next Step:**
Using `LaunchedEffect` is great, but what if you want to trigger a coroutine from a Button click? You can't put `LaunchedEffect` inside an `onClick` lambda.
Ready for **Topic 5.2: rememberCoroutineScope**? This is the bridge between user events and coroutines.

---

## Navigation

Next â†’
