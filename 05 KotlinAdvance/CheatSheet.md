---
layout: default
title: Cheatsheet
parent: Advanced
---

This **Kotlin Interview Master Cheat Sheet** is designed to give you the highest-value information in the shortest possible time. Use this for a "final scan" 30 minutes before your interview.

---

### **1. The Async Trinity (Coroutines)**

- **Suspend Functions:** Functions that can be paused and resumed. They do not block the thread they are running on.
- **Dispatchers:** \* `Main`: UI updates and interactions.
- `IO`: Network calls, Database, File I/O (Scales up to 64+ threads).
- `Default`: CPU-intensive work (Sorting, JSON parsing, Math).

- **Flow:** An asynchronous stream of data.
- **Cold:** Only starts producing data when `collect()` is called.

---

### **2. Kotlin vs. Java (Idiomatic Syntax)**

- **Data Classes:** Use for POJOs. Automatically provides `equals()`, `hashCode()`, `toString()`, and `copy()`.
- **Null Safety:**
- `String?`: Nullable type.
- `?.`: Safe call (runs only if not null).
- `?:`: Elvis operator (provides a default value).
- `!!`: Not-null assertion (Avoid! Throws NPE if null).

- **Scope Functions:**
- `apply` / `also`: Returns the **original object**. (Good for config).
- `let` / `run` / `with`: Returns the **lambda result**. (Good for mapping/null-checks).

---

### **3. Collections & Performance (LeetCode Prep)**

- **StringBuilder:** Essential for string building inside loops.
- **HashMap / HashSet:** lookup and uniqueness checks.
- **ArrayDeque:** Use this for both Stacks (LIFO) and Queues (FIFO).
- **windowed(size, step):** Built-in utility for Sliding Window algorithms.

---

### **4. Advanced Architecture Patterns**

- **LCE Pattern:** Use `Sealed Classes` to model UI state: `Loading`, `Content`, and `Error`.
- **Structured Concurrency:** Always use lifecycle-aware scopes (`viewModelScope`, `lifecycleScope`) to prevent memory leaks.
- **Backing Property:** Use a private `_mutableList` and a public `immutableList` to protect your data from outside modification.

---

### **5. "Tricky" Concepts (Rapid Fire)**

- **`==` vs `===`:** `==` checks structural equality (content); `===` checks referential equality (memory address).
- **`const val` vs `val`:** `const` is determined at **compile-time**; `val` is determined at **runtime**.
- **`lateinit` vs `lazy`:** `lateinit` is for `var` (not null, initialized later); `lazy` is for `val` (calculated only when accessed).
- **Object Initialization:** Parent `init` blocks and properties always run before Child `init` blocks.

---

### **The "Golden Rule" of Kotlin Interviews**

> **"Prefer Immutability and Null Safety."** > If you are unsure of an answer, choose the option that makes the code safer (read-only `val`, non-null types, or structured concurrency).

**Would you like to try a "Blind Mock Interview" where I ask you 3 random questions from this sheet to test your memory?**
