---
layout: default
title: rememberCoroutineScope
parent: 5. Side-Effects & Lifecycles
nav_order: 2
---

# rememberCoroutineScope

Here are your notes for **Topic 5.2**.

---

## **Topic 5.2: rememberCoroutineScope**

### **1. What It Is**

`rememberCoroutineScope` is a function that gives you a `CoroutineScope` bound to the lifecycle of the Composable where it is declared.
Unlike `LaunchedEffect` (which starts automatically), this scope is designed to be used **manually** inside callbacks like `onClick` or `onScroll`.

### **2. Why It Exists (The "Callback" Gap)**

- **The Rule:** You cannot call a `suspend` function (like `apiCall()` or `listState.animateScrollToItem()`) directly inside a standard lambda like `onClick`.
- **The Problem:** `LaunchedEffect` doesn't help here because `LaunchedEffect` runs as soon as the screen loads. We want to run code **only** when the user clicks a button.
- **The Solution:** We need a bridge. We "remember" a scope, and then inside the click listener, we use `scope.launch { ... }`.

### **3. How It Works**

1. **Creation:** Call `val scope = rememberCoroutineScope()` at the top of your function.
2. **Usage:** inside `onClick`, call `scope.launch { suspendFunction() }`.
3. **Lifecycle:** If the user leaves the screen while the coroutine is running (e.g., a slow network call), the scope is automatically cancelled. This prevents memory leaks.

### **4. Example: The Scroll-to-Top Button**

You want to click a button to scroll a list. `animateScrollToItem` is a suspend function.

**The Wrong Way (Compiler Error):**

```kotlin
Button(onClick = {
    // ERROR: Suspend function called from a non-suspend lambda!
    listState.animateScrollToItem(0)
}) { Text("Top") }

```

**The Right Way:**

```kotlin
@Composable
fun ScrollButton(listState: LazyListState) {
    // 1. Get the scope
    val scope = rememberCoroutineScope()

    Button(onClick = {
        // 2. Launch a coroutine manually on click
        scope.launch {
            // Now we can call suspend functions!
            listState.animateScrollToItem(0)
        }
    }) {
        Text("Scroll to Top")
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`rememberCoroutineScope`, User Actions vs Composition Lifecycle, Callback handling, Structured Concurrency, Cancellation.

**Interview Speak Paragraph**

> "I use `rememberCoroutineScope` specifically when I need to launch a coroutine in response to a user event, such as a button click or a gesture. While `LaunchedEffect` is for running coroutines during the composition lifecycle, it cannot be triggered by callbacks. `rememberCoroutineScope` provides a scope that is tied to the composable's lifecycle, allowing me to safely call suspend functions—like `drawerState.open()` or `listState.scrollTo()`—inside an `onClick` handler, ensuring that any running jobs are cancelled if the composable leaves the screen."

---

**Next Step:**
You have a long-running task. But what if a value changes _while_ that task is running?
Ready for **Topic 5.3: rememberUpdatedState**? This is a subtle but critical fix for "stale data" bugs in effects.

---

## Navigation

â† Previous
Next â†’
