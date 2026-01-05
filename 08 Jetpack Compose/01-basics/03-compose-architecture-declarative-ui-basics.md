---
layout: default
title: Compose Architecture (Declarative UI Basics)
parent: 1. Introduction + Basic Composables
nav_order: 3
---

# Compose Architecture (Declarative UI Basics)

Here are your notes for **Topic 1.3**.

---

## **Topic 1.3: Compose Architecture (Declarative UI Basics)**

### **1. What It Is**

Compose Architecture is built on the idea that your User Interface (UI) is just a visual representation of your data.
In math terms, it uses the formula: **`UI = f(State)`**.
This means the UI is a function (`f`) of the current data (`State`). If the data changes, the function runs again, and the UI updates automatically.

### **2. Why It Exists (The Synchronization Problem)**

In the old architecture, the UI and the Data were separate entities that you had to manually sync.

- _Scenario:_ You have a `User` object and a `TextView`.
- _Problem:_ If the `User` name changes, the `TextView` doesn't know. You (the developer) have to remember to call `textView.setText()`. If you forget, the app shows old data.
- _Solution:_ Compose eliminates this gap. Since the UI is _generated_ from the data, it is impossible for the UI to show something different from the data. They are tightly bound.

### **3. How It Works (The UI Tree)**

When you run a Compose app, you aren't creating Views; you are creating a **UI Tree** (also called the Composition).

1. **Emission:** When a `@Composable` function runs, it "emits" information.
2. **The Tree:** These emissions form a hierarchy (a tree) of nodes in memory.
3. **Transformation:** Your function's job is to take Data (Inputs) and transform it into UI Nodes (Output).

**The Separation of Concerns Re-imagined**

- _Old Way:_ We separated code by **File Type** (XML for layout, Kotlin for logic). This was an artificial separation. The layout and logic were usually tightly coupled anyway.
- _Compose Way:_ We separate code by **Logical Responsibility**. A specific button's look and its click logic belong together. This is called **Cohesion**. It’s okay to have logic inside your UI code, as long as it's _UI logic_ (like formatting a string).

### **4. Example: The Tree in Action**

Imagine a profile screen.

- **Data:** `User(name="Alex", isOnline=true)`
- **Function:** `UserProfile(user)`

**Step 1: The Code**

```kotlin
@Composable
fun UserProfile(user: User) {
    Column {                // Parent Node
        Image(user.photo)   // Child Node 1
        Text(user.name)     // Child Node 2
        if (user.isOnline) {
            Badge("Online") // Child Node 3 (Conditional)
        }
    }
}

```

**Step 2: The Resulting Tree**
If `isOnline` is **true**, the system builds this tree in memory:

```text
Root (Column)
 ├── Node A (Image)
 ├── Node B (Text: "Alex")
 └── Node C (Badge: "Online")

```

**Step 3: The Update (Recomposition)**
If `isOnline` changes to **false**, Compose re-runs the function. It sees the `if` block is now false. It effectively "prunes" Node C from the tree. You didn't delete the view; you just described a state where the view doesn't exist.

### **5. Interview Prep**

**Interview Keywords**
UI as a Function of State (UI = f(State)), Composition, UI Tree, Unidirectional Data Flow, Cohesion, Separation of Concerns.

**Interview Speak Paragraph**

> "Compose architecture is based on the principle that the UI is a direct function of state. Instead of manually updating views, we define composables that transform data into a UI hierarchy or 'Tree'. When the underlying data changes, the framework intelligently re-executes these functions—a process called Recomposition—to update only the parts of the tree that changed. This shifts the 'Separation of Concerns' from grouping by file type (XML vs Kotlin) to grouping by feature and logic, which creates more cohesive and maintainable components."

---

**Next Step:**
Now that we understand the theory, we need to build it. Ready for **Topic 1.4: Setting up the Environment**? This is a quick but crucial check to ensure we know about BOM and dependencies.

---

## Navigation

â† Previous
Next â†’
