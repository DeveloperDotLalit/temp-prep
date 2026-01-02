---
layout: default
title: "Cold Flow vs Hot Flow"
parent: "Phase 4: Hot Flows StateFlow and SharedFlow"
nav_order: 1
---

# Cold Flow vs Hot Flow

This is perhaps the most important architectural distinction in Kotlin Flows. In Android development, moving from **Cold Flows** to **Hot Flows** is like moving from a "one-time request" to a "live data source."

---

### **What It Is – Simple explanation for beginners**

- **Cold Flow:** Only starts when a consumer asks for it. It’s like a **Netflix movie**. It doesn't play for anyone until you press "Play," and every person who presses "Play" watches it from the very beginning, independently.
- **Hot Flow:** Is always active and "on." It’s like a **Live Radio Station**. The music is playing whether you are listening or not. If you tune in late, you miss the beginning and start hearing whatever is playing _right now_.

### **Why It Exists – The problem it solves**

Standard (Cold) Flows have two limitations in a UI-driven app:

1. **Multiple Observers:** If three different UI components collect a Cold Flow, the producer runs **three separate times**. This is wasteful if you're fetching the same data from a network.
2. **State Management:** Cold Flows don't "hold" onto their values. Once the data is emitted, it's gone. In Android, we need our UI to remember the current state (e.g., "Is the button clicked?" or "Is the list loading?") even if the screen rotates.

Hot Flows solve this by being **Multicast** (one producer, many consumers) and **Stateful** (they can remember data).

### **How It Works – Step-by-step logic**

1. **Unicast (Cold):** One Producer One Collector. The lifecycle of the producer is tied to the collector.
2. **Multicast (Hot):** One Producer Multiple Collectors. The producer lives independently of whether anyone is currently listening.
3. **Active State:** Hot flows (like `StateFlow` or `SharedFlow`) usually live inside a `ViewModel` or a `Singleton` so they persist as long as the screen or the app is alive.

---

### **Detailed Comparison Table**

| Feature            | Cold Flow (standard `flow {}`)                | Hot Flow (`StateFlow` / `SharedFlow`)            |
| ------------------ | --------------------------------------------- | ------------------------------------------------ |
| **Lifecycle**      | Created on demand; ends when `collect` stops. | Created once; lives independently of collectors. |
| **Data Storage**   | No. Does not store the last value.            | Yes. Usually stores the current state.           |
| **Producers**      | One producer per collector (Unicast).         | One producer for all collectors (Multicast).     |
| **Starting Point** | Collector always starts from the beginning.   | Collector joins and gets the "current" data.     |
| **Usage**          | Network calls, Database queries.              | UI State, Navigation events, Global updates.     |

---

### **Example – Real-world Analogy**

- **Cold Flow (On-Demand TV):** You want to watch "The Batman." You click it. It starts at 0:00. Your friend comes over an hour later and starts it in another room; they also start at 0:00.
- **Hot Flow (Live Sports):** You tune into a live football match at the 30th minute. You missed the first 30 minutes. Your friend tunes in at the 45th minute. You are both watching the same live action at the same time.

```kotlin
// COLD FLOW
val coldFlow = flow {
    emit("New Data")
}
// Each time you collect, "New Data" is re-generated.

// HOT FLOW (StateFlow)
private val _state = MutableStateFlow("Initial State")
val state: StateFlow<String> = _state
// The state "Initial State" is stored.
// Anyone who joins late gets the current value immediately.

```

### **Interview Keywords**

Multicasting, Unicast vs Multicast, Stateful, Independent Lifecycle, Shared Resources, Hot vs Cold.

### **Interview Speak Paragraph**

> "The fundamental difference between Cold and Hot flows lies in their lifecycle and how they share data. A Cold Flow is demand-driven and starts from scratch for every collector, making it ideal for one-off tasks like network requests. In contrast, a Hot Flow—such as StateFlow or SharedFlow—is active independently of its collectors and multicasts data to multiple subscribers simultaneously. In Android, we use Hot Flows in the ViewModel to manage UI state, as they allow multiple UI components to observe the same data source without re-triggering the underlying production logic."

---

**Next Step:** Now that you know the difference, we need to look at the most common Hot Flow in Android. Shall we dive into **StateFlow: The modern replacement for LiveData**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
