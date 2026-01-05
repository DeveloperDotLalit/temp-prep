---
layout: default
title: State Hoisting
parent: 2. State & Recomposition (The Core)
nav_order: 4
---

# State Hoisting

Here are your notes for **Topic 2.4**.

---

## **Topic 2.4: State Hoisting**

### **1. What It Is**

**State Hoisting** is a design pattern where you move the state _out_ of a composable and "hoist" (lift) it up to the parent (the caller).

- **Internal State:** The composable holds its own `remember { mutableStateOf(...) }`.
- **Hoisted State:** The composable receives the state as a **parameter** and receives a **lambda** to ask for changes.

This turns a "Stateful" component (smart, hard to reuse) into a "Stateless" component (dumb, easy to reuse).

### **2. Why It Exists (Reusability & Testing)**

Imagine a `SearchInput` component.

- **If it has Internal State:** It decides what is typed. If you want to clear that text from a "Clear All" button outside the component, you can't. The state is locked inside.
- **If it is Hoisted:** The parent holds the text. The parent can pass "hello" or " " (empty string) whenever it wants. The component just renders whatever it is told.

**Benefits:**

1. **Single Source of Truth:** You don't have duplicate state scattered everywhere.
2. **Encapsulation:** The logic stays in the parent (ViewModel/Screen), the UI stays in the child.
3. **Testability:** You can easily test the UI by passing dummy data without needing complex mocks.

### **3. How It Works (The Pattern)**

The standard pattern for hoisting involves adding two parameters to your function:

1. **`value: T`**: The current value to display (State flows **Down**).
2. **`onValueChange: (T) -> Unit`**: A function to call when the user interacts (Events flow **Up**).

This creates **Unidirectional Data Flow (UDF)**.

### **4. Example: Stateful vs. Stateless**

**A. The "Stateful" Version (Hard to control)**

```kotlin
@Composable
fun StatefulCounter() {
    // The state is locked inside. No one outside can reset this count.
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Count: $count")
    }
}

```

**B. The "Stateless" Version (Hoisted - Reusable)**

```kotlin
// 1. The Child (Pure UI)
// It doesn't own the count. It just asks to update it.
@Composable
fun StatelessCounter(
    count: Int,                  // State comes down
    onIncrement: () -> Unit      // Events go up
) {
    Button(onClick = onIncrement) {
        Text("Count: $count")
    }
}

// 2. The Parent (The Controller)
@Composable
fun ParentScreen() {
    var totalCount by remember { mutableStateOf(0) }

    Column {
        Text("Total Clicks: $totalCount")

        // We can use the SAME component logic, but controlled by us.
        StatelessCounter(
            count = totalCount,
            onIncrement = { totalCount++ }
        )

        // We can even add a reset button that affects the counter!
        Button(onClick = { totalCount = 0 }) { Text("Reset") }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
State Hoisting, Stateless vs Stateful, Unidirectional Data Flow (UDF), Reusability, Single Source of Truth, Event Bubbling.

**Interview Speak Paragraph**

> "State Hoisting is the practice of moving state out of a composable and up to its caller. This transforms a component from being 'Stateful' to 'Stateless.' By accepting data as a parameter and exposing events via lambdas (the `value` and `onValueChange` pattern), we decouple the UI from the logic. This makes the component reusable, easier to test, and allows the parent to act as the single source of truth, strictly following Unidirectional Data Flow."

---

**Next Step:**
You moved the state up, but what happens if the user rotates the screen? The `remember` block resets!
Ready for **Topic 2.5: rememberSaveable**? This fixes the rotation data-loss bug.

---

## Navigation

â† Previous
Next â†’
