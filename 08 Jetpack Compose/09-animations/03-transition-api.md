---
layout: default
title: Transition API
parent: 9. Animations
nav_order: 3
---

# Transition API

Here are your notes for **Topic 9.3**.

---

## **Topic 9.3: Transition API (Complex/Chained)**

### **1. What It Is**

The Transition API is used when you need to coordinate **multiple** animations based on a **single** state change.
Instead of having 5 independent `animate*AsState` variables (which might get out of sync), you create one `Transition` object. This object drives all child animations (Color, Size, Alpha, Rotation) simultaneously.

It also includes `rememberInfiniteTransition`, which is a special variant for animations that loop forever (like a loading pulse).

### **2. Why It Exists (Synchronization)**

- **The Problem:** If you use separate `animateFloatAsState` and `animateColorAsState` variables, they are unaware of each other. If one animation is interrupted or has a different duration, your UI might look glitchy (e.g., the box finishes shrinking before it finishes turning blue).
- **The Solution:** `updateTransition` creates a parent controller. All child animations are strictly synchronized to the parent's state. You can see the whole state change in the Android Studio Animation Preview.

### **3. How It Works**

#### **A. `updateTransition` (Finite States)**

1. **Define State:** Usually an Enum (e.g., `BoxState.Small`, `BoxState.Large`).
2. **Create Transition:** `val transition = updateTransition(targetState = currentState)`.
3. **Define Children:** Use extension functions on the transition object: `transition.animateColor`, `transition.animateDp`.
4. **Use Values:** Use `color` and `size` in your modifiers.

#### **B. `rememberInfiniteTransition` (Looping)**

1. **Create Transition:** `val infiniteTransition = rememberInfiniteTransition()`.
2. **Define Child:** `infiniteTransition.animateFloat(...)`.
3. **Set Repeat Mode:** `RepeatMode.Reverse` (Pulse) or `RepeatMode.Restart` (Spin).

### **4. Example: The "Selectable" Card (updateTransition)**

We want a card that, when selected, grows larger, elevates, and turns gold—all at once.

```kotlin
enum class CardState { Normal, Selected }

@Composable
fun SelectableCard() {
    var state by remember { mutableStateOf(CardState.Normal) }

    // 1. Create the Master Controller
    val transition = updateTransition(targetState = state, label = "CardTransition")

    // 2. Define Child Animations (Synced)
    val color by transition.animateColor(label = "Color") { state ->
        when (state) {
            CardState.Normal -> Color.LightGray
            CardState.Selected -> Color.Yellow
        }
    }

    val size by transition.animateDp(label = "Size") { state ->
        when (state) {
            CardState.Normal -> 100.dp
            CardState.Selected -> 150.dp
        }
    }

    val elevation by transition.animateDp(label = "Elevation") { state ->
        when (state) {
            CardState.Normal -> 2.dp
            CardState.Selected -> 12.dp
        }
    }

    // 3. Use values
    Card(
        modifier = Modifier
            .size(size)
            .clickable { state = if (state == CardState.Normal) CardState.Selected else CardState.Normal },
        colors = CardDefaults.cardColors(containerColor = color),
        elevation = CardDefaults.cardElevation(defaultElevation = elevation)
    ) {
        // Content
    }
}

```

### **5. Example: The Pulsing Loader (rememberInfiniteTransition)**

A circle that scales up and down forever.

```kotlin
@Composable
fun PulsingCircle() {
    val infiniteTransition = rememberInfiniteTransition(label = "Pulse")

    // Animate scale from 1f to 1.5f and back
    val scale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.5f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000),
            repeatMode = RepeatMode.Reverse // Yo-yo effect
        ),
        label = "Scale"
    )

    Box(
        modifier = Modifier
            .size(50.dp)
            .scale(scale)
            .background(Color.Red, CircleShape)
    )
}

```

### **6. Interview Prep**

**Interview Keywords**
`updateTransition`, `rememberInfiniteTransition`, Synchronization, Child Animations, `RepeatMode.Reverse`, `infiniteRepeatable`, State Preview (Tooling).

**Interview Speak Paragraph**

> "When I need to orchestrate complex animations where multiple properties (like size, color, and elevation) change simultaneously based on a single state, I use `updateTransition`. Unlike independent `animate*AsState` calls, `updateTransition` ensures all child animations remain synchronized and allows for previewing the entire state change in Android Studio. For continuous background effects, like a pulsing notification badge or a loading spinner, I use `rememberInfiniteTransition` with `infiniteRepeatable`, setting the repeat mode to either `Restart` for rotations or `Reverse` for pulsing effects."

---

**Congratulations!** You have completed **Part 8 & 9: Graphics and Animations**.
You can now build custom, performant, and beautiful interactive UIs.

The final section covers the essential non-UI logic: Testing and Interop.
**Are you ready to start Topic 10: Testing & Interoperability?**

---

## Navigation

â† Previous
Next â†’
