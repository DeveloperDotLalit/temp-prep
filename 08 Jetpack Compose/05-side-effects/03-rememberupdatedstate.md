---
layout: default
title: rememberUpdatedState
parent: 5. Side-Effects & Lifecycles
nav_order: 3
---

# rememberUpdatedState

Here are your notes for **Topic 5.3**.

---

## **Topic 5.3: rememberUpdatedState**

### **1. What It Is**

`rememberUpdatedState` is a wrapper that ensures a long-running side effect (like a timer or a listener) always captures the **latest** value of a variable, without forcing the side effect to restart.

### **2. Why It Exists (The "Restart" Problem)**

Imagine a `LaunchedEffect` that waits for 10 seconds and then logs a message.

- **Problem:** If you pass the message as a key to `LaunchedEffect(message)`, every time the message changes, the timer **restarts** from 0. You never reach 10 seconds if the message changes quickly.
- **Problem 2:** If you _don't_ pass it as a key (`LaunchedEffect(Unit)`), the effect runs once, but it captures the **old** message from 10 seconds ago (Stale Data).
- **Solution:** `rememberUpdatedState` creates a reference that is technically stable (so it doesn't restart the effect) but internally mutable (so inside the effect, you always read the fresh value).

### **3. How It Works**

It uses a `mutableStateOf` internally but exposes the value safely.
Inside your long-running effect, you reference this wrapper instead of the raw parameter.

### **4. Example: The Timeout Logger**

**Scenario:** We want to wait 5 seconds and then print the _current_ screen name. If the user navigates rapidly, we don't want to restart the timer; we just want to print whatever screen they are on when the timer finishes.

```kotlin
@Composable
fun LandingScreen(currentScreenName: String, onTimeout: () -> Unit) {
    // 1. Capture the latest value in a State holder.
    // This variable 'currentOnTimeout' will ALWAYS hold the freshest lambda.
    val currentOnTimeout by rememberUpdatedState(onTimeout)
    val currentName by rememberUpdatedState(currentScreenName)

    // 2. The Effect key is 'Unit' (Run ONCE).
    // It will NOT restart when 'currentScreenName' changes.
    LaunchedEffect(Unit) {
        delay(5000) // Wait 5 seconds

        // 3. Use the updated state.
        // Even if 'currentScreenName' changed 10 times during the delay,
        // this line prints the LATEST one, not the one from 5 seconds ago.
        Log.d("App", "Timer finished on screen: $currentName")
        currentOnTimeout()
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Stale Data, Long-running Effects, Restarting Effects, Closure Capture, Stable Reference.

**Interview Speak Paragraph**

> "`rememberUpdatedState` is essential when handling long-running operations inside a `LaunchedEffect` or `DisposableEffect` that should _not_ restart when a parameter changes. For example, if I have a 10-second timer that logs the 'current user status' at the end, I don't want the timer to reset to zero every time the status updates. By wrapping the status in `rememberUpdatedState`, the effect accesses a stable reference that always points to the latest value, allowing the effect to continue running uninterrupted while still using fresh data when it completes."

---

**Next Step:**
We can handle Compose state, but what about non-Compose data like Flow or LiveData?
Ready for **Topic 5.4: produceState & snapshotFlow**? This is the bridge between the two worlds.

---

## Navigation

â† Previous
Next â†’
