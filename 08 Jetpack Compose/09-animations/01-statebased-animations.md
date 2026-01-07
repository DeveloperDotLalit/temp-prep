---
layout: default
title: State-Based Animations
parent: 9. Animations
nav_order: 1
---

# State-Based Animations

Here are your notes for **Topic 9.1**.

---

# Topic 9: Animations

## **Topic 9.1: State-Based Animations**

### **1. What It Is**

State-Based Animations are the simplest way to animate in Compose. They follow the "Fire-and-Forget" principle.
You don't manually tick a clock or calculate frames. You simply tell Compose:

- **"Value is currently A."**
- **"Value is now B."**
- **"Animate the change for me."**

The API follows the naming convention `animate*AsState` (e.g., `animateFloatAsState`, `animateColorAsState`, `animateDpAsState`).

### **2. Why It Exists (Declarative Motion)**

In the old View system, you had to start an `ObjectAnimator` and listen for updates.
In Compose, animations are just **State**.

- If `isSelected = true`, the color is Red.
- If `isSelected = false`, the color is Blue.
- `animateColorAsState` automatically interpolates the values between Red and Blue over time whenever the boolean flips. The UI just reads the current color value.

### **3. How It Works**

1. **Define Target:** You have a state variable (e.g., `targetSize`).
2. **Create Animation State:** You call `animateDpAsState(targetValue = targetSize)`.
3. **Read Value:** You use the result (`animatedSize.value`) in your modifier.

#### **The Animation Spec (`animationSpec`)**

You can customize _how_ it moves by passing a spec:

- **`tween(durationMillis = 300)`:** Standard linear or curved motion.
- **`spring()`:** Physics-based. Bounces like a rubber band. (Default for many values).
- **`keyframes { ... }`:** Complex multi-stage animation (0ms -> start, 50ms -> middle, 100ms -> end).

### **4. Example: The Expanding Button**

A button that grows and changes color when toggled.

```kotlin
@Composable
fun ExpandingButton() {
    var expanded by remember { mutableStateOf(false) }

    // 1. ANIMATE COLOR
    // When 'expanded' changes, this smoothly transitions the color.
    val backgroundColor by animateColorAsState(
        targetValue = if (expanded) Color.Red else Color.Blue,
        animationSpec = tween(durationMillis = 500), // Slow fade
        label = "ColorAnimation" // Optional label for Layout Inspector
    )

    // 2. ANIMATE SIZE
    // Uses a Spring for a bouncy effect
    val width by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy)
    )

    Box(
        modifier = Modifier
            .size(width = width, height = 50.dp) // Use the animated value
            .background(backgroundColor)
            .clickable { expanded = !expanded }, // Toggle the state
        contentAlignment = Alignment.Center
    ) {
        Text("Click Me", color = Color.White)
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`animate*AsState`, Fire-and-Forget, Interpolation, `AnimationSpec`, Spring Physics, `tween`, Recomposition driven.

**Interview Speak Paragraph**

> "For simple value changes, I use the `animate*AsState` family of functions, such as `animateColorAsState` or `animateDpAsState`. This is the declarative approach to animation: I simply define the target value based on a state boolean, and Compose handles the interpolation automatically. It eliminates the need for managing animation controllers or listeners. If I need a specific feel, I customize the `animationSpec` parameter to use `tween` for precise timing or `spring` for physics-based, natural motion."

---

**Next Step:**
Changing a value is easy. But what if you want to make an item appear or disappear with a slide effect?
Ready for **Topic 9.2: Visibility Animations**? This covers `AnimatedVisibility`.

---

## Navigation

Next â†’
