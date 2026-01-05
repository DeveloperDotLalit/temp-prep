---
layout: default
title: "State Holders: remember vs mutableStateOf"
parent: 2. State & Recomposition (The Core)
nav_order: 3
---

# State Holders: remember vs mutableStateOf

Here are your notes for **Topic 2.3**.

---

## **Topic 2.3: State Holders: remember vs mutableStateOf**

### **1. What It Is**

In Compose, managing state usually involves two functions working together:

1. **`mutableStateOf`**: Creates a bucket that holds data and **tells Compose to update** when that data changes.
2. **`remember`**: Tells Compose to **not forget** the data when the function runs again (recomposes).

You almost always see them together:
`val name = remember { mutableStateOf("Alex") }`

### **2. Why It Exists (The "Amnesia" Problem)**

Composable functions are just functions. In standard programming, when a function runs, its local variables are created from scratch.

- **The Problem:** If you write `var count = 0` inside a Composable, every time the screen updates (recomposes), the line runs again, and `count` resets to `0`. Your app has amnesia.
- **The Solution (`remember`):** This function tells Compose: "Store this value in the composition tree memory. If this function runs again, give me back the _old_ value, don't create a new one."
- **The Trigger (`mutableStateOf`):** Standard variables (Int, String) don't trigger updates. `MutableState` is a special observable wrapper. When you change its `.value`, it shouts, "Hey Compose! I changed! Redraw me!"

### **3. How It Works**

#### **A. `mutableStateOf` (The Observer)**

- It wraps your value in a `State<T>` object.
- It is "Observable."
- **Role:** Triggers Recomposition.

#### **B. `remember` (The Cache)**

- It stores a value in the Composition cache.
- **Role:** Survives Recomposition.
- _Note:_ It does NOT survive "Configuration Changes" (like screen rotation). For that, we need `rememberSaveable` (Topic 2.5).

#### **C. The Syntax Options**

You will see three ways to write this:

1. **Raw:** `val count = remember { mutableStateOf(0) }` -> Access via `count.value`.
2. **Destructured:** `val (value, setValue) = remember { mutableStateOf(0) }` -> Access via `value`, update via `setValue`.
3. **Delegate (Best Practice):** `var count by remember { mutableStateOf(0) }` -> Access directly as `count`. (Requires `import androidx.compose.runtime.getValue` & `setValue`).

### **4. Example: The "Amnesia" Bug vs. The Fix**

**The Bug (No `remember`):**

```kotlin
@Composable
fun BrokenCounter() {
    // BUG: Every time the button is clicked, this function re-runs.
    // This line executes again, resetting count to 0.
    // The UI will never show 1.
    val count = mutableStateOf(0)

    Button(onClick = { count.value++ }) {
        Text("Count is ${count.value}")
    }
}

```

**The Fix (With `remember`):**

```kotlin
@Composable
fun WorkingCounter() {
    // FIX: 'remember' checks the cache.
    // First run: initializes to 0.
    // Second run: ignores the block, retrieves the stored value (e.g., 1).
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Count is $count")
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
State Observability, Recomposition Scope, Property Delegation (`by`), Persistence, Cache, `MutableState`.

**Interview Speak Paragraph**

> "In Compose, we typically define state using `remember` and `mutableStateOf` together. `mutableStateOf` creates an observable wrapper around the data that notifies the framework to trigger a recomposition whenever the value changes. However, since Composable functions can re-execute frequently, simply declaring a variable would reset it every time. That's why we wrap it in `remember`, which caches the object in the Composition tree, ensuring the value persists across recompositions."

---

**Next Step:**
You know how to hold state _inside_ a component. But what if you want to share that state with other components?
Ready for **Topic 2.4: State Hoisting [Added - Vital]**? This is the most important architectural pattern in Compose.

---

## Navigation

â† Previous
Next â†’
