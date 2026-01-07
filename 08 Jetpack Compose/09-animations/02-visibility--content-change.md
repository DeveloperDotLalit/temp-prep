---
layout: default
title: Visibility & Content Change
parent: 9. Animations
nav_order: 2
---

# Visibility & Content Change

Here are your notes for **Topic 9.2**.

---

## **Topic 9.2: Visibility & Content Change**

### **1. What It Is**

This topic covers how to animate elements entering or leaving the screen, or morphing from one layout to another.

- **`AnimatedVisibility`:** Use this when an item appears or disappears (Boolean logic: True/False).
- **`AnimatedContent`:** Use this when an item stays on screen but its _content_ changes (e.g., a counter changing from "1" to "2", or a view switching from "Loading" to "Success").

### **2. Why It Exists (UX Continuity)**

- **The Problem:** Using a simple `if (visible) { Text(...) }` causes the text to snap into existence instantly. This is jarring and pushes other UI elements around abruptly.
- **The Solution:** These composables manage the layout space. They calculate the start size and end size and smoothly transition between them, ensuring the UI "glides" rather than "snaps."

### **3. How It Works**

#### **A. `AnimatedVisibility` (The Toggle)**

It takes a `visible` boolean. You customize the `enter` and `exit` transitions.

- **Combinable Transitions:** You can add effects using the `+` operator.
- `enter = fadeIn() + expandVertically() + slideInVertically()`
- `exit = fadeOut() + shrinkVertically()`

#### **B. `AnimatedContent` (The Switcher)**

It watches a `targetState`. When the state changes, it runs a transition between the old content and the new content.

- **`transitionSpec`:** Defines the choreography.
- _Example:_ "Slide the old number UP and out, while sliding the new number UP and in."

- **`SizeTransform`:** If the new content is bigger than the old content, the container animates its size smoothly to fit.

### **4. Example: Visibility vs. Content**

**Scenario A: The "Show Details" Card (`AnimatedVisibility`)**

```kotlin
@Composable
fun DetailsCard() {
    var showDetails by remember { mutableStateOf(false) }

    Column {
        Button(onClick = { showDetails = !showDetails }) {
            Text("Toggle Details")
        }

        // Only animates appearance/disappearance
        AnimatedVisibility(
            visible = showDetails,
            enter = fadeIn() + expandVertically(), // Grow and Fade In
            exit = fadeOut() + shrinkVertically()  // Shrink and Fade Out
        ) {
            Text(
                "Here is the secret info...",
                modifier = Modifier.background(Color.LightGray).padding(16.dp)
            )
        }
    }
}

```

**Scenario B: The Sliding Counter (`AnimatedContent`)**
This creates a "slot machine" effect where numbers slide up.

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableIntStateOf(0) }

    Button(onClick = { count++ }) { Text("Add") }

    // Animates between different integers
    AnimatedContent(
        targetState = count,
        transitionSpec = {
            // Compare new vs old to decide direction
            if (targetState > initialState) {
                // If counting UP: New slides in from bottom, Old slides out to top
                (slideInVertically { height -> height } + fadeIn()) togetherWith
                (slideOutVertically { height -> -height } + fadeOut())
            } else {
                // If counting DOWN: Reverse it
                (slideInVertically { height -> -height } + fadeIn()) togetherWith
                (slideOutVertically { height -> height } + fadeOut())
            }
        }, label = "CounterAnimation"
    ) { targetCount ->
        // This is the content that gets animated
        Text("Count: $targetCount", style = MaterialTheme.typography.displayMedium)
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`AnimatedVisibility`, `AnimatedContent`, `enter`/`exit` transitions, `transitionSpec`, `SizeTransform`, `togetherWith` (infix), `Crossfade` (simpler version).

**Interview Speak Paragraph**

> "For layout transitions, I rely on `AnimatedVisibility` and `AnimatedContent`. I use `AnimatedVisibility` when I need to gracefully show or hide a component based on a boolean state, typically combining `fadeIn` and `expandVertically` to avoid jarring layout shifts. When I need to switch between two different pieces of data—like a loading state transitioning to a success state, or a number incrementing—I use `AnimatedContent`. This allows me to define a `transitionSpec` to choreograph how the old content exits and the new content enters, such as creating slide-in/slide-out effects that provide directional context to the user."

---

**Next Step:**
You have mastered single animations. But what if you need to coordinate multiple values at the same time (e.g., Color AND Size AND Position)?
Ready for **Topic 9.3: Transition API (Complex/Chained)**? This is for multi-state, synchronized animations.

---

## Navigation

â† Previous
Next â†’
