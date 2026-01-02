---
layout: default
title: "Cheatsheet Kotlin Flow"
parent: "Kotlin Flows Mastery Roadmap"
nav_order: 8
---

# Cheatsheet Kotlin Flow

This is your **Final Master Cheat Sheet** for Kotlin Flows. It is designed to be your last-minute review before walking into an interview. It covers the core "why," the critical operators, and the architectural "must-knows."

---

## 🚀 The Kotlin Flow "Pocket" Cheat Sheet

### **1. Foundations: The Basics**

| Concept             | Explanation                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| **What is a Flow?** | An asynchronous stream of data that emits multiple values over time.                                 |
| **Why use it?**     | To handle data that changes (GPS, DB, Sensors) without blocking the Main Thread.                     |
| **Cold Flow**       | Starts only when `collect()` is called. Like a **YouTube video** (plays from start for each viewer). |
| **Hot Flow**        | Active even without collectors. Like a **Live Radio** (you join in the middle).                      |

### **2. The Flow Anatomy**

1. **Producer:** Uses `flow { emit(value) }` to send data.
2. **Intermediary:** Uses `map`, `filter`, `transform` to change data.
3. **Consumer:** Uses `collect` to receive and use data.

---

### **3. Essential Operators (The "Toolkit")**

| Operator                   | When to use it?                                                             |
| -------------------------- | --------------------------------------------------------------------------- |
| **`flowOn`**               | Changes the thread **above** it (Upstream). Use it for IO tasks.            |
| **`catch`**                | Handles errors from **above** it. Can `emit` a fallback value.              |
| **`debounce`**             | Waits for a pause in data (perfect for **Search-as-you-type**).             |
| **`distinctUntilChanged`** | Skips the update if the new value is the same as the last one.              |
| **`collectLatest`**        | Cancels the current work if a new value arrives (prevents race conditions). |
| **`combine`**              | Merges two flows using the **latest** values of both.                       |

---

### **4. Hot Flows: State vs. Events**

| Feature           | **StateFlow**                     | **SharedFlow**                           |
| ----------------- | --------------------------------- | ---------------------------------------- |
| **Analogy**       | A Digital Scoreboard.             | An Intercom Announcement.                |
| **Best For**      | UI State (Loading/Success/Error). | One-time Events (Toasts/Navigation).     |
| **Initial Value** | **Mandatory.**                    | Not required.                            |
| **Behavior**      | Holds the last value (Stateful).  | Broadcasts and disappears (Event-based). |

---

### **5. Senior Architect's Checklist**

- **Context Preservation:** Never use `withContext` inside a flow; always use `flowOn`.
- **Exception Transparency:** Don't wrap `emit` in `try-catch`. Use the `.catch` operator.
- **Safe Collection:** Always use `repeatOnLifecycle(STARTED)` in Activities/Fragments to prevent battery drain and memory leaks.
- **Sharing:** Use `.stateIn()` to turn a cold database flow into a hot UI flow shared by multiple fragments.

---

## 🎙️ The "Million Dollar" Interview Answers

### **Q: Why use Flow instead of LiveData?**

> "StateFlow is superior because it is thread-independent, offers a massive range of operators (like combine and flatMap), and is part of the Kotlin library, making it compatible with Clean Architecture and Multiplatform projects. It also handles 'distinct-until-changed' filtering by default."

### **Q: How do you handle Backpressure?**

> "Flow handles backpressure through coroutine suspension. If a producer is too fast, I use `.buffer()` to run them in parallel, `.conflate()` to skip old data, or `.collectLatest()` to cancel old work and focus on the newest data."

### **Q: What is the difference between `flatMapLatest` and `flatMapConcat`?**

> "`flatMapConcat` waits for each inner flow to finish before starting the next one (sequential). `flatMapLatest` cancels the previous inner flow the moment a new value arrives, which is ideal for search features where old queries are no longer relevant."

---

### **The "Red Flag" Code Review Summary**

- **Red Flag:** `lifecycleScope.launch { flow.collect { ... } }`
- _Correction:_ Use `repeatOnLifecycle` or it will leak in the background.

- **Red Flag:** `withContext(Dispatchers.IO) { emit(data) }`
- _Correction:_ This will crash. Use `.flowOn(Dispatchers.IO)`.

- **Red Flag:** `MutableStateFlow` as a public variable.
- _Correction:_ Keep the Mutable version `private` and expose a read-only `StateFlow`.

---

**Would you like me to create a "Mock Interview" session now where I ask you a few tough questions and you try to answer them using your "Interview Speak"?**
