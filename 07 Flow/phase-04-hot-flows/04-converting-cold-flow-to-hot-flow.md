---
layout: default
title: "Converting Cold Flow to Hot Flow"
parent: "Phase 4: Hot Flows StateFlow and SharedFlow"
nav_order: 4
---

# Converting Cold Flow to Hot Flow

In an interview, you might be asked: _"How do you take a flow from a database (which is cold) and make it available to multiple UI components without re-querying the database?"_ This is where `.stateIn()` and `.sharedIn()` come into play. They are the "bridges" between the Cold and Hot worlds.

---

### **What It Is – Simple explanation for beginners**

Converting a flow from Cold to Hot is essentially **"Sharing"** a stream.

Imagine a cold flow is like a **personal faucet**—every time someone turns it on, a new pipe is laid to the water source. By using `.stateIn()` or `.sharedIn()`, you are installing a **water tank** (the Hot Flow). The cold flow fills the tank, and all users just connect their pipes to the tank. The source only has to work once.

### **Why It Exists – The problem it solves**

- **Avoiding Duplicate Work:** If your Cold Flow performs a heavy network request, and you have two UI fragments observing it, without conversion, the network request happens twice.
- **Providing Lifecycle Awareness:** You need to tell the Hot Flow _when_ to start and _when_ to stop. You don't want to keep a network connection open if no one is looking at the screen.
- **State Preservation:** It allows you to turn a simple stream of data into a "State" that survives screen rotations.

### **How It Works – The Three Pillars**

To use these operators, you must provide three things:

1. **Scope:** The `CoroutineScope` where the sharing happens (usually `viewModelScope`).
2. **Started:** The strategy for when sharing starts and stops (e.g., `WhileSubscribed`).
3. **Initial Value:** (Only for `stateIn`) The value to show before the first data arrives.

---

### **The Two Key Operators**

#### **1. `.stateIn()**`

Converts a Cold Flow into a **StateFlow**.

- **Use case:** When you need to represent a UI State (like a list of items).
- **Requirement:** Needs an initial value.

```kotlin
val userList: StateFlow<List<User>> = repository.getUsersFlow() // Cold
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000), // Stop 5s after last collector leaves
        initialValue = emptyList()
    )

```

#### **2. `.sharedIn()**`

Converts a Cold Flow into a **SharedFlow**.

- **Use case:** When you need to broadcast events (like a stream of error messages) to multiple listeners.
- **Requirement:** No initial value needed; you can configure the `replay` cache.

---

### **Interview Focus: `SharingStarted` Strategies**

Interviewers love to ask about the `started` parameter. These are the "Rules of the Water Tank":

- **`SharingStarted.Eagerly`:** Starts immediately and never stops until the scope is cancelled. (Wasteful if no one is watching).
- **`SharingStarted.Lazily`:** Starts when the first collector joins and never stops.
- **`SharingStarted.WhileSubscribed(5000)`:** **The Best Practice for Android.** It starts when someone joins. If the user leaves (like during a screen rotation), it waits for 5 seconds. If no one comes back, it stops the upstream flow to save battery/data.

### **Interview Keywords**

Upstream, Downstream, Sharing Strategy, `WhileSubscribed`, `viewModelScope`, Multicasting, Resource Optimization.

### **Interview Speak Paragraph**

> "To transform a Cold Flow into a Hot Flow, we use the `.stateIn()` or `.sharedIn()` operators. This process, known as 'sharing,' allows multiple collectors to observe the same data stream without re-triggering the upstream producer's logic, which is critical for performance. When using these operators in a ViewModel, the `SharingStarted.WhileSubscribed` strategy is the recommended practice; it ensures that the producer is only active when the UI is visible, while the 5-second buffer prevents the flow from restarting unnecessarily during configuration changes like screen rotations."

---

**Congratulations! You have successfully completed Phase 4.** You now know everything about Hot and Cold flows and how to switch between them.

**Next Step:** We move to **Phase 5: Advanced Transformations & Composition**. This phase is all about handling multiple data sources. Shall we start with **Combining Flows: Using `zip` and `combine**`?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
