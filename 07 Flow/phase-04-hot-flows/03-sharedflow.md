---
layout: default
title: "SharedFlow"
parent: "Phase 4: Hot Flows StateFlow and SharedFlow"
nav_order: 3
---

# SharedFlow

While **StateFlow** is the "Scoreboard" (always showing the current state), **SharedFlow** is the "Announcement System." It’s designed for things that happen once, like a bell ringing or a notification popping up.

---

### **What It Is – Simple explanation for beginners**

**SharedFlow** is a "Hot" Flow that is highly configurable and used to send messages to one or many listeners.

Think of it like a **School Intercom System**.

- An announcement is made: "Principal's office, now!"
- If you are in the hallway, you hear it.
- If you are in the gym, you hear it.
- But if you arrive at school **after** the announcement was made, you missed it. It doesn't repeat itself just because you showed up late (unless you tell it to "replay").

### **Why It Exists – The problem it solves**

- **The "Event" vs. "State" Problem:** StateFlow is bad for one-time events (like showing a Snackbar). Why? Because if the user rotates the screen, StateFlow will re-emit the last value, and the Snackbar will pop up again. You don't want that!
- **Broadcasts:** Sometimes you need one action (like a "Logout" signal) to trigger changes in five different parts of your app simultaneously.
- **Configurable Replay:** Unlike StateFlow (which always replays the last 1 value), SharedFlow lets you choose to replay 0, 5, or 100 previous values to new subscribers.

### **How It Works – Step-by-step logic**

1. **No Initial Value:** Unlike StateFlow, SharedFlow does **not** need an initial value. It starts empty.
2. **Multicasting:** It sends the same emission to every active collector.
3. **Replay Cache:** You can set a `replay` parameter. If `replay = 0`, new collectors miss past events. If `replay = 1`, it acts a bit like StateFlow.
4. **Buffer & Overflow:** You can decide what happens if the producer is too fast (e.g., drop the oldest message or suspend).

---

### **Example – Code-based**

```kotlin
class MyViewModel : ViewModel() {
    // 1. Create a MutableSharedFlow
    // replay = 0 means "If you miss it, you miss it"
    private val _events = MutableSharedFlow<String>(replay = 0)
    val events = _events.asSharedFlow()

    fun triggerAlert() {
        viewModelScope.launch {
            // 2. emit() is a suspend function here!
            _events.emit("Unauthorized Access!")
        }
    }
}

// UI Side (Activity)
lifecycleScope.launch {
    viewModel.events.collect { message ->
        // 3. This only triggers when emit() is called.
        // If screen rotates, this DOES NOT re-trigger automatically.
        showToast(message)
    }
}

```

### **Comparison: SharedFlow vs. StateFlow**

| Feature                  | SharedFlow                               | StateFlow                           |
| ------------------------ | ---------------------------------------- | ----------------------------------- |
| **Primary Use**          | **Events** (Navigation, Toasts).         | **State** (UI models, List data).   |
| **Initial Value**        | Not required.                            | **Mandatory**.                      |
| **Replay**               | Configurable (0, 1, or more).            | Always 1 (the current state).       |
| **Behavior on Rotation** | Events are not re-emitted (if replay=0). | Current state is always re-emitted. |

### **Interview Focus: The "One-Time Event" Debate**

A common interview question for experienced developers: _"How do you handle navigation events in Compose/Flow?"_ **The Answer:** Use a `SharedFlow` with `replay = 0`. This ensures that the navigation only happens once when the event is fired, preventing "double navigation" or "back-stack loops" during configuration changes.

### **Interview Keywords**

One-time events, Multicasting, Replay Cache, Broadcast, Event-driven, Configuration changes, `asSharedFlow`.

### **Interview Speak Paragraph**

> "SharedFlow is a highly customizable hot flow designed for broadcasting events to multiple subscribers. Unlike StateFlow, it doesn't require an initial value and is ideal for one-time events like navigation, showing Snackbars, or triggering alerts. Its most powerful feature is the configurable 'replay cache,' which allows us to decide how many previous emissions a new collector should receive upon joining. By using SharedFlow with a replay of zero, we can ensure that events are processed only once and are not redundantly re-fired when a Fragment or Activity is recreated during a configuration change."

---

**Next Step:** You've mastered the two types of Hot Flows! Now, how do we turn a regular Cold Flow into one of these? Shall we move to **Converting Cold to Hot: Using the `.stateIn()` and `.sharedIn()` operators**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
