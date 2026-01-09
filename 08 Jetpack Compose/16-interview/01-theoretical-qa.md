---
layout: default
title: Theoretical Q&A
parent: 16. Interview Prep
nav_order: 1
---

# Theoretical Q&A

Here are your notes for **Topic 16: Interview Prep (Theoretical Q&A)**.

This section aggregates the high-level concepts typically asked in Senior Android Interviews. These questions test if you understand _how_ Compose works under the hood, not just how to use it.

---

### **1. The Lifecycle of a Composable**

**Q: Explain the lifecycle of a Composable function. How does it differ from a View?**

- **The Theory:** Unlike an Android View (which is a Java object with `onCreate`, `onMeasure`, `onDraw`, `onDestroy`), a Composable is just a function. Functions don't have lifecycles; they just run.
- **The Compose Lifecycle:** To manage this, Compose tracks the function in the Composition Tree.

1. **Enter:** The function is called for the first time. Nodes are added to the tree.
2. **Recompose:** The function is called again with new data. The tree is updated (nodes might remain, update, or move).
3. **Leave:** The function is no longer called. Its nodes and state are removed from the tree.

**Interview Answer:**

> "A Composable's lifecycle is defined by its presence in the Composition tree. It has three distinct phases: **Entering the Composition**, **Recomposing** (when state changes), and **Leaving the Composition**. Unlike Views, we don't manually manage initialization or destruction methods. Instead, we use Side-Effect APIs like `DisposableEffect` to hook into these lifecycle events—for example, to release resources when the Composable leaves the tree."

---

### **2. Side-Effects & The "Recomposition Loop"**

**Q: Why can't I just launch a Coroutine directly inside a Composable? Why do I need `LaunchedEffect`?**

- **The Theory:** Recomposition can happen extremely fast (e.g., every frame during an animation) and can be cancelled midway.
- **The Problem:** If you write `scope.launch { api.call() }` in the function body, it will trigger a new network call _every single time_ the screen draws. This leads to 100s of duplicate calls.
- **The Solution:** `LaunchedEffect` acts as a barrier. It guarantees the code block runs **only** when the Composable enters the composition (or when its keys change), shielding it from the chaos of recomposition.

**Interview Answer:**

> "Executing code directly in the composable body is unsafe because recomposition is frequent and unpredictable. A standard Coroutine launch would re-trigger on every frame update. `LaunchedEffect` is specifically designed to bridge this gap. It launches a coroutine that is bound to the Composable's lifecycle—it starts when entering the composition and is automatically cancelled when leaving. This ensures structured concurrency and prevents resource leaks or duplicate operations."

---

### **3. Compiler Magic (`@Composable`)**

**Q: What does the `@Composable` annotation actually do to my code?**

- **The Theory:** It is not just a marker. It is a **compiler plugin** that transforms your code.
- **Transformation 1 (The Composer):** It injects an extra parameter usually called `$composer` into every function. This parameter gives the runtime access to the "Gap Buffer" (the memory structure used to store the tree).
- **Transformation 2 (Changed Type):** It changes the function type. Standard functions are `(A, B) -> C`. Composable functions are `(A, B, Composer, Int) -> Unit`.
- **Transformation 3 (Positional Memoization):** The compiler inserts code to "remember" where the function is called. This allows `remember { }` to find the correct value based on its position in the code.

**Interview Answer:**

> "The `@Composable` annotation triggers a compiler plugin that transforms the function's signature. It injects a `Composer` parameter, which is the interface to the Compose runtime. This allows the runtime to track the execution, perform 'Positional Memoization' (knowing which `remember` call belongs to which location in the code), and handle the restarting of functions during recomposition. Essentially, it turns a standard stateless function into a restartable, state-aware unit of UI."

---

### **4. State Management (The "Single Source of Truth")**

**Q: What is the difference between `remember`, `rememberSaveable`, and `StateFlow`?**

- **`remember`:** Caches a value across recompositions. If you rotate the screen (Activity destruction), the value is **LOST**.
- **`rememberSaveable`:** Caches a value across recompositions AND saves it to the `Bundle`. If you rotate the screen or the OS kills the process to save RAM, the value is **SAVED**.
- **`StateFlow` (ViewModel):** Holds state outside the UI entirely. Best for business logic. Survives rotation (because ViewModel does), but does NOT survive process death unless you implement `SavedStateHandle`.

**Interview Answer:**

> "`remember` is for transient UI state (like animation values) that persists during recomposition but dies on rotation. `rememberSaveable` is for critical UI state (like input text or scroll position) that must survive configuration changes and process death; it serializes data to the Bundle. `StateFlow` lives in the ViewModel and is used for Business State; it decouples the data from the View layer entirely, allowing for easier testing and separation of concerns."

---

### **5. Recomposition Optimizations**

**Q: What is "Skipping" in Compose, and what breaks it?**

- **The Theory:** If a Composable is called with the _exact same inputs_ as the last time, Compose "skips" running it to save battery.
- **The Breaker:** Unstable parameters. If you pass a generic `List<T>` (which is an interface and potentially mutable), Compose assumes it _might_ have changed and refuses to skip.
- **The Fix:** Wrap collections in an `@Immutable` data class or use the `kotlinx.collections.immutable` library.

**Interview Answer:**

> "Skipping is the mechanism where Compose avoids re-running a function if its inputs haven't changed. However, this relies on stability inference. The most common pitfall is passing unstable types, like a standard `List` or `var` properties, which force Compose to always recompose. To fix this, I ensure my state classes are marked `@Immutable` or `@Stable`, and I use immutable collections, ensuring the compiler can safely verify that the data has not changed."

---

**This concludes the Theoretical Interview Prep.**

You now have the complete package:

1. **Practical Coding Skills** (Layouts, Lists, Animations).
2. **Architecture Patterns** (MVVM, MVI, Clean Arch).
3. **Deep Theory** (Compiler, Lifecycle, Stability).

**What is your final wish?**

1. **Download PDF:** Combine all notes into one document.
2. **Start Coding Challenge:** Build a "Task Manager" app using these skills.
3. **Mock Interview:** I ask you 3 hard questions, and you type the answer.

---

## Navigation

Next â†’
