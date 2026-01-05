---
layout: default
title: Composition & Recomposition
parent: 2. State & Recomposition (The Core)
nav_order: 2
---

# Composition & Recomposition

Here are your notes for **Topic 2.2**.

---

## **Topic 2.2: Composition & Recomposition**

### **1. What It Is**

This is the lifecycle of your UI.

- **Composition:** The _first_ time your code runs. Compose builds the initial UI tree.
- **Recomposition:** The _updates_. When state changes, Compose re-runs the functions to update the tree.

Think of it like writing a document:

- _Composition:_ Writing the first draft.
- _Recomposition:_ Editing just the sentences that need to change (without rewriting the whole page).

### **2. Why It Exists (Performance)**

Rebuilding the entire screen from scratch (like a web page refresh) is expensive and slow.
Compose is designed to be **Smart**. It wants to do the _least amount of work possible_. If only one number on the screen changed, it should not redraw the background, the toolbar, or the footer.

### **3. How It Works**

#### **A. The Lifecycle Stages**

Unlike an Activity (which has `onCreate`, `onStart`, `onResume`), a Composable only has three main stages:

1. **Enter the Composition:** The function is called for the first time. The node is added to the tree.
2. **Recompose:** The function is called again because its input data changed. The node is updated.
3. **Leave the Composition:** The function is no longer called (e.g., hidden by an `if` statement). The node is removed (UI is destroyed).

#### **B. Smart Recomposition (Skipping)**

Compose looks at the inputs of your function.

- **Scenario:** You have a function `UserCard(name: String, age: Int)`.
- **Update:** You change `age` from 25 to 26. `name` stays "John".
- **Result:** Compose re-runs `UserCard`. Inside it, if there is a `Text(name)` and a `Text(age)`, Compose is smart enough to **skip** redrawing `Text(name)` because "John" didn't change. It _only_ redraws `Text(age)`.

#### **C. Call Site Identity (How it knows who is who)**

How does Compose know that the "Text" it drew 5 seconds ago is the same "Text" it is looking at now?
It assigns an identity based on the **Call Site**—the exact location in your source code where the function is called.

- If you call `Text("A")` and then `Text("B")`, they are two different nodes because they are on different lines of code.
- **Loop Warning:** Inside a `for` loop, the call site is the same for every item! (We solve this later with `key`, but be aware that identity gets tricky in loops).

### **4. Example: Visualization of Skipping**

Imagine a dashboard with a counter and a static title.

```kotlin
@Composable
fun Dashboard(count: Int) {
    Column {
        // Component A: Static Title
        // Since the string "My App" never changes,
        // Compose SKIPS this line during every update.
        Text("My App")

        // Component B: Dynamic Counter
        // 'count' changes, so this line RE-RUNS (Recomposes).
        Text("Count is $count")

        // Component C: Expensive Graph
        // If 'count' is not passed here, this is also SKIPPED.
        ExpensiveGraph()
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Composition, Recomposition, Skipping, Call Site Identity, Stability (Stable/Unstable), Lifecycle (Enter/Update/Leave).

**Interview Speak Paragraph**

> "The lifecycle of a Composable is defined by three stages: entering the composition, recomposing, and leaving the composition. The most powerful feature here is **Smart Recomposition**. When state changes, Compose re-executes the function, but it intelligently skips any child composables whose inputs haven't changed. This granular updating relies on **Call Site Identity**, where the framework tracks components based on their position in the source code to determine what to keep and what to update, ensuring high performance even in complex UIs."

---

**Next Step:**
Now you know _when_ it updates. But _how_ do you store the data so it survives these updates?
Ready for **Topic 2.3: State Holders: remember vs mutableStateOf**? This is the most common line of code you will write.

---

## Navigation

â† Previous
Next â†’
