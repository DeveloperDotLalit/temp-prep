---
layout: default
title: Layout Primitives: Column, Row, Box
parent: 1. Introduction + Basic Composables
nav_order: 8
---

# Layout Primitives: Column, Row, Box

Here are your notes for **Topic 1.8**.

---

## **Topic 1.8: Layout Primitives: Column, Row, Box**

### **1. What It Is**

These are the containers that determine **where** your UI elements sit on the screen.

- **Column:** Stacks items vertically (Top to Bottom).
- **Row:** Places items horizontally (Left to Right).
- **Box:** Stacks items on top of each other (Back to Front / Z-axis).

### **2. Why It Exists**

In the old XML system, we had complex layouts like `ConstraintLayout` or `RelativeLayout` because nesting layouts (putting a LinearLayout inside a LinearLayout) was bad for performance.
In Compose, nesting is cheap and efficient. You build complex screens by simply combining these three basic building blocks.

### **3. How It Works**

#### **A. Column & Row (The Grid Makers)**

These two are opposites but work the same way. They have two main properties to control positioning:

1. **Main Axis Arrangement:** Controls spacing along the container's primary direction.

- _Column (Vertical):_ How items are spaced from Top to Bottom.
- _Row (Horizontal):_ How items are spaced from Start to End.
- _Options:_ `Start`, `End`, `Center`, `SpaceBetween` (push to edges), `SpaceEvenly` (equal gaps), `SpaceAround`.

2. **Cross Axis Alignment:** Controls position perpendicular to the primary direction.

- _Column (Horizontal):_ aligning items Left/Right/Center.
- _Row (Vertical):_ aligning items Top/Bottom/Center.
- _Options:_ `Start`, `End`, `CenterHorizontally` (for Column), `CenterVertically` (for Row).

#### **B. Box (The Stacker)**

Used for overlays.

- **Usage:** Putting a "Like" heart icon on top of a photo, or a loading spinner on top of a screen.
- **Alignment:** You use the `contentAlignment` parameter (e.g., `Alignment.Center`) to default all children to one spot, or `Modifier.align()` on specific children to place them individually.

### **4. Example: The Chat Message Bubble**

This example uses all three.

1. **Row:** To put the Avatar next to the Message.
2. **Column:** To stack the Username above the Message Text.
3. **Box:** To overlay a small "Online" dot on the Avatar.

```kotlin
@Composable
fun ChatMessage() {
    Row(
        modifier = Modifier.fillMaxWidth().padding(8.dp),
        verticalAlignment = Alignment.CenterVertically // Centers text vertically relative to avatar
    ) {
        // Box allows stacking the green dot over the profile pic
        Box {
            Image(painter = painterResource(R.drawable.profile), contentDescription = null)
            // The Green Dot
            Icon(
                imageVector = Icons.Default.Circle,
                contentDescription = "Online",
                tint = Color.Green,
                modifier = Modifier.align(Alignment.BottomEnd) // Puts it in bottom-right corner
            )
        }

        Spacer(modifier = Modifier.width(8.dp))

        // Column stacks name and text
        Column {
            Text("John Doe", fontWeight = FontWeight.Bold)
            Text("Hey! How are you doing?")
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Main Axis, Cross Axis, Arrangement vs. Alignment, Z-Index (Box), Weights (`Modifier.weight`), Nesting.

**Interview Speak Paragraph**

> "In Compose, I handle 90% of layouts using just Column, Row, and Box. Column and Row handle the linear flow, where I use 'Arrangement' to control spacing along the main axis (like `SpaceBetween`) and 'Alignment' to position items on the cross axis. For overlays, like placing text over an image or a badge on an icon, I use Box, which allows for Z-index stacking. Unlike the old View system, Compose handles deep nesting of these primitives very efficiently, so we don't need a heavy ConstraintLayout for every screen."

---

**Next Step:**
You have the building blocks and the layout rules. But you need a frame for your screen. Ready for **Topic 1.9: The Scaffold Layout**? This is essential for real-world apps.

---

## Navigation

â† Previous
Next â†’
