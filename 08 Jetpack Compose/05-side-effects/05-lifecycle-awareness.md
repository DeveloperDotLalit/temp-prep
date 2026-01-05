---
layout: default
title: Lifecycle Awareness
parent: 5. Side-Effects & Lifecycles
nav_order: 5
---

# Lifecycle Awareness

Here are your notes for **Topic 5.5**.

---

## **Topic 5.5: Lifecycle Awareness**

### **1. What It Is**

Lifecycle Awareness in Compose refers to the ability of a Composable to react to the Android Activity/Fragment lifecycle events (like `ON_START`, `ON_RESUME`, `ON_PAUSE`, `ON_STOP`).
Since Composables don't have these methods built-in (unlike Activities), we need to manually attach an **Observer** to listen for them.

### **2. Why It Exists (The "Video Player" Problem)**

Imagine a Video Player composable.

- **Problem:** If the user minimizes the app (Home button), the video keeps playing sound in the background. This is bad UX.
- **Goal:** You need to pause the video when the app goes to the background (`ON_PAUSE`) and resume it when it comes back (`ON_RESUME`).
- **Solution:** We observe the `LocalLifecycleOwner`.

### **3. How It Works**

1. **Get the Owner:** Use `LocalLifecycleOwner.current` to get the current lifecycle holder (usually the Activity or Fragment).
2. **Create an Observer:** Implement `LifecycleEventObserver`.
3. **Attach/Detach:** Use `DisposableEffect` to add the observer when the composable starts and remove it when it leaves the composition.

### **4. Example: The Lifecycle Listener**

This generic function can be reused anywhere in your app to listen for events.

```kotlin
@Composable
fun OnLifecycleEvent(onEvent: (Lifecycle.Event) -> Unit) {
    // 1. Get the current Lifecycle Owner (Activity/Fragment)
    val lifecycleOwner = LocalLifecycleOwner.current

    // 2. Safely Update the lambda if it changes (Topic 5.3)
    val currentOnEvent by rememberUpdatedState(onEvent)

    // 3. Add/Remove the observer
    DisposableEffect(lifecycleOwner) {
        // Create the observer
        val observer = LifecycleEventObserver { source, event ->
            currentOnEvent(event)
        }

        // Attach
        lifecycleOwner.lifecycle.addObserver(observer)

        // Detach (Cleanup is mandatory!)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }
}

// Usage in a Screen
@Composable
fun VideoScreen() {
    OnLifecycleEvent { event ->
        when (event) {
            Lifecycle.Event.ON_RESUME -> videoPlayer.play()
            Lifecycle.Event.ON_PAUSE -> videoPlayer.pause()
            else -> { /* Other events */ }
        }
    }

    // ... UI Code ...
}

```

### **5. Interview Prep**

**Interview Keywords**
`LocalLifecycleOwner`, `LifecycleEventObserver`, `DisposableEffect`, Resource Management, Background/Foreground detection.

**Interview Speak Paragraph**

> "Handling Android Lifecycle events in Compose requires a bit of manual setup since Composables don't have methods like `onResume`. To solve this, I access the `LocalLifecycleOwner.current` and use a `DisposableEffect` to attach a `LifecycleEventObserver`. This allows me to execute logic specifically when the app moves to the background or foreground—critical for tasks like pausing video players, stopping GPS tracking, or refreshing data when the user returns to the app. I always ensure the observer is removed in the `onDispose` block to prevent memory leaks."

---

**Next Step:**
We can handle the App closing, but what if we want to _prevent_ it?
Ready for **Topic 5.6: System Back Handling**? This is how you intercept the "Back" button to show a "Do you want to exit?" dialog.

---

## Navigation

â† Previous
Next â†’
