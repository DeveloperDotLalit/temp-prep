---
layout: default
title: What is State?
parent: 2. State & Recomposition (The Core)
nav_order: 1
---

# What is State?

Here are your notes for **Topic 2.1**.

---

# Topic 2: State & Recomposition (The Core)

This is the most critical section of the entire roadmap. If you understand this, you understand Compose. If you don't, you will write buggy apps that crash or lag.

## **Topic 2.1: What is State?**

### **1. What It Is**

**State** is any value that can change over time.
If your app isn't a static painting, it has state.

- A checkbox being checked (`Boolean`).
- A text field having text (`String`).
- A list of messages loading (`List<Message>`).
- A network error showing (`Enum`).

In Compose, the UI is not an object you control; it is a reflection of this State.

### **2. Why It Exists (The Problem with Static UI)**

An app that cannot change is useless. Users interact with apps.

- **The Old Way:** You listened for an event, then _manually_ found the view and changed it.
- _Event:_ User clicks "Send".
- _Action:_ `messageView.setText("")` (You explicitly clear the box).

- **The Compose Way:** You change the **State**. The UI automatically reacts.
- _Event:_ User clicks "Send".
- _Action:_ `messageText = ""` (You update the variable).
- _Result:_ The UI sees the variable changed and redraws itself.

### **3. How It Works (UI = f(State))**

This is the golden formula of Compose: **`UI = f(State)`**

- **UI:** The layout you see on screen.
- **f:** Your Composable functions.
- **State:** The data feeding the functions.

**State vs. Events (The Loop)**
You need to clearly separate "Nouns" (State) from "Verbs" (Events).

1. **Event (The Trigger):** Something happens (User clicks, Network returns data). Use callbacks/lambdas for this.
2. **Update State:** The event handler updates the variable.
3. **State (The Data):** The current value (e.g., `count = 5`).
4. **Recomposition:** The UI redraws because the State changed.

### **4. Example: The Light Switch**

Think of a real-world light switch.

- **State:** Is the electricity flowing? (True/False).
- **UI:** Is the bulb glowing? (Light/Dark).
- **Event:** Your finger flipping the switch.

You don't "tell" the bulb to turn on. You flip the switch (Event), which changes the electricity flow (State), and the bulb naturally glows (UI) because physics (Compose) handles it.

```kotlin
@Composable
fun LightSwitch() {
    // 1. THE STATE (Source of Truth)
    // We use 'mutableStateOf' so Compose watches this variable
    var isJsOn by remember { mutableStateOf(false) }

    Column {
        // 2. THE UI (Reflects State)
        if (isOn) {
            Icon(Icons.Default.LightMode, contentDescription = "Bulb On")
        } else {
            Icon(Icons.Default.DarkMode, contentDescription = "Bulb Off")
        }

        // 3. THE EVENT (Changes State)
        Switch(
            checked = isOn,
            onCheckedChange = { newState ->
                isOn = newState // Update the state -> UI redraws automatically
            }
        )
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Source of Truth, Unidirectional Data Flow (UDF), UI = f(State), State Observation, Event Propagation.

**Interview Speak Paragraph**

> "In Compose, State determines what is shown on the screen at any given moment. Unlike the imperative view system where we manually update widgets, Compose follows the `UI = f(State)` paradigm. This means the UI is simply a visual representation of the current data. When an **Event** occurs (like a user click), we update the **State**, and the framework automatically triggers a Recomposition to update the UI. This clear separation between State (what is) and Events (what happened) simplifies logic and reduces bugs."

---

**Next Step:**
Now that we know _what_ state is, we need to know how Compose handles the updates efficiently.
Ready for **Topic 2.2: Composition & Recomposition**? This explains the "magic" of how the screen updates without redrawing everything.

---

## Navigation

Next â†’
