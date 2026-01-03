---
layout: default
title: "Edge Case Handling"
parent: "Phase 5: Interview Final Polish"
nav_order: 3
---

# Edge Case Handling

## **Topic 5: Edge Case Handling**

### **What It Is**

In a perfect world, every Intent finds a destination and every Broadcast finishes instantly. In reality, things break. **Edge Case Handling** is about managing what happens when:

1. **Intent Failure:** You ask the system to "Open a PDF," but the user doesn't have a PDF viewer installed.
2. **Broadcast Timeout:** Your Receiver starts a heavy task on the main thread, causing the app to freeze.

---

### **Why It Exists**

- **For Intents:** Android is an open ecosystem. You can never guarantee that a specific third-party app exists on a user's device. If you don't handle the "missing app" case, your app will **crash** with an `ActivityNotFoundException`.
- **For Broadcasts:** The Android System has a "watchdog." If a Receiver blocks the main thread for too long (usually **10 seconds** for foreground broadcasts and **20-60 seconds** for background ones), the system assumes your app is dead and kills it with an **ANR (Application Not Responding)**.

---

### **How It Works**

#### **1. Intent Safety (The Check-Before-You-Leap)**

Before calling `startActivity()`, you should check if there’s anyone available to catch it. You can use:

- **`resolveActivity()`**: Returns the component that _would_ handle the intent. If it returns `null`, no app can handle it.
- **`try-catch`**: Wrapping the call in a block to catch `ActivityNotFoundException`.

#### **2. Broadcast Responsiveness (The 10-Second Rule)**

If you need a few more seconds in a Receiver (e.g., to write a small file), you can call **`goAsync()`**.

- This tells the system: "Don't kill me yet, I'm moving this work to a background thread."
- **Crucial:** You still only get about **10 seconds total**, and you _must_ call `finish()` on the result object to release the receiver.

---

### **Example (Code-based)**

**Handling Missing Apps (Intents):**

```kotlin
val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://www.lalit.com"))

// 1. The Proactive Way (Better)
if (intent.resolveActivity(packageManager) != null) {
    startActivity(intent)
} else {
    Toast.makeText(this, "Please install a web browser", Toast.LENGTH_SHORT).show()
}

// 2. The Reactive Way (Safety net)
try {
    startActivity(intent)
} catch (e: ActivityNotFoundException) {
    // Log error or show UI fallback
}

```

**Handling "Long" Work in Broadcast (The `goAsync` way):**

```kotlin
override fun onReceive(context: Context, intent: Intent) {
    val pendingResult = goAsync() // Ask for more time

    // Move to a background thread/coroutine
    CoroutineScope(Dispatchers.IO).launch {
        try {
            // Perform small disk I/O (must be < 10s)
            saveDataToDb(intent.data)
        } finally {
            pendingResult.finish() // CRITICAL: Tell the system you're done
        }
    }
}

```

---

### **Interview Keywords**

- **ActivityNotFoundException**: The crash caused by unresolvable intents.
- **`resolveActivity()`**: The method used to verify intent targets.
- **ANR (Application Not Responding)**: The result of blocking the main thread.
- **`goAsync()`**: The mechanism for short asynchronous work in a Receiver.
- **`PendingResult`**: The object returned by `goAsync()` used to signal completion.

---

### **Interview Speak Paragraph**

> "In a production environment, I never fire an Implicit Intent without a safety check. I use `resolveActivity()` or a `try-catch` block to handle **ActivityNotFoundException**, ensuring the app doesn't crash if a user lacks a compatible handler. Regarding Broadcast Receivers, I follow the strict rule that `onReceive()` must stay off the main thread for any long-running logic. If a task takes a few seconds, I use **`goAsync()`** to process it on a background thread while keeping the receiver alive. For anything longer than 10 seconds, I immediately delegate the work to **WorkManager** to ensure we remain compliant with Android’s battery and responsiveness policies."

---

### **Common Interview Question/Angle**

- **"What is the difference between `resolveActivity()` and `queryIntentActivities()`?"**
- _Answer:_ `resolveActivity()` returns the _best_ single match (or the app chooser), whereas `queryIntentActivities()` returns a _list_ of all apps that match the intent filter. Use the latter if you want to build your own custom app-picker UI.

- **"Can `goAsync()` be used to run a network call that might take 30 seconds?"**
- _Answer:_ **No.** Even with `goAsync()`, the system timeout is still roughly 10 seconds. For a network call that could be slow, you must use **WorkManager**. `goAsync()` is strictly for small tasks like disk I/O or slight processing that shouldn't glitch the UI thread.

---

**This concludes our deep dive into Edge Cases! 🛡️**

**Would you like to move into the "Final Mock Interview" where I provide a complex scenario and you explain your architectural approach using everything we've learned?**

---

[â¬… Back to Phase Overview](../)
