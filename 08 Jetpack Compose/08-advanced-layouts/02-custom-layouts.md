---
layout: default
title: Custom Layouts
parent: 8. Advanced Layouts & Graphics
nav_order: 2
---

# Custom Layouts

Here are your notes for **Topic 8.2**.

---

## **Topic 8.2: Custom Layouts**

### **1. What It Is**

When `Row`, `Column`, or `ConstraintLayout` aren't enough, you build a **Custom Layout**.
At the core of every composable (even `Row`) is the generic **`Layout`** function. By calling this directly, you take full control over exactly where every pixel goes.

### **2. Why It Exists (Breaking the Grid)**

Standard layouts follow strict rules (vertical lists, horizontal rows). Custom layouts allow you to:

- **Overlap items** in specific ways (like a deck of cards).
- **Arrangement based on content:** Create a "Tag Cloud" where words wrap automatically to the next line if they don't fit.
- **Circular Layouts:** Place items in a circle around a center point.

### **3. How It Works (The 3-Step Protocol)**

The `Layout` composable gives you a lambda with `measurables` (the children) and `constraints` (max width/height allowed).

1. **Measure Children:** You loop through every child (`measurable`) and ask it to measure itself using `measurable.measure(constraints)`. This turns them into **`Placeables`** (items that know their size but not their position).
2. **Decide Own Size:** You calculate how big _you_ (the parent container) need to be to fit all these children. You call `layout(width, height)`.
3. **Place Children:** Inside the `layout` block, you loop through the `Placeables` and define their `x` and `y` coordinates using `placeable.place(x, y)`.

### **4. Example: A "Cascade" Layout**

Let's build a layout that places items diagonally like a staircase. Each item is shifted down and to the right by a fixed amount.

```kotlin
@Composable
fun CascadeLayout(
    spacing: Int = 20, // Shift each item by 20px
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Layout(
        modifier = modifier,
        content = content
    ) { measurables, constraints ->
        // STEP 1: Measure all children
        // We don't restrict them; let them be as big as they want (up to parent max)
        val placeables = measurables.map { measurable ->
            measurable.measure(constraints)
        }

        // STEP 2: Calculate generic container size
        // Width = Width of last item + total shifting
        // Height = Height of last item + total shifting
        val stepCount = placeables.size - 1
        val layoutWidth = (placeables.lastOrNull()?.width ?: 0) + (stepCount * spacing)
        val layoutHeight = (placeables.lastOrNull()?.height ?: 0) + (stepCount * spacing)

        // Report our size to the parent
        layout(width = layoutWidth, height = layoutHeight) {

            // STEP 3: Place children
            var xPosition = 0
            var yPosition = 0

            placeables.forEach { placeable ->
                placeable.placeRelative(x = xPosition, y = yPosition)

                // Shift the next item
                xPosition += spacing
                yPosition += spacing
            }
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`Layout` composable, `Measurable` vs `Placeable`, Constraints, `measure()`, `layout()`, `placeRelative` (RTL support), Intrinsic Measurements.

**Interview Speak Paragraph**

> "When standard layouts like Row or Column don't meet specific design requirements, I create a Custom Layout using the `Layout` composable. This involves a two-pass system: first, the **Measure Phase**, where I iterate through the `measurables` and determine the size of each child given the incoming constraints. This produces `Placeables`. Second, the **Placement Phase**, where I calculate the total dimensions of the container, call the `layout()` function, and then mathematically calculate the X and Y coordinates for each `placeable`. I always use `placeRelative` instead of `place` to automatically support Right-to-Left (RTL) languages without extra logic."

---

**Next Step:**
You can place items. Now let's draw on them.
Ready for **Topic 8.3: Canvas & Custom Drawing**? This is where you draw charts, graphs, and weird shapes.

---

## Navigation

â† Previous
Next â†’
