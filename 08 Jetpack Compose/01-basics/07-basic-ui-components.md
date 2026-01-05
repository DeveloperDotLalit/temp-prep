---
layout: default
title: Basic UI Components
parent: 1. Introduction + Basic Composables
nav_order: 7
---

# Basic UI Components

Here are your notes for **Topic 1.7**.

---

## **Topic 1.7: Basic UI Components**

### **1. What It Is**

These are the "Lego bricks" of your application. Just as you build a house from bricks, wood, and glass, you build a Compose screen using `Text`, `Button`, `Icon`, and `Surface`. These are the fundamental atoms provided by the Material Design library.

### **2. Why It Exists**

In the old XML days, we had `TextView`, `Button`, `ImageView`, and `CardView`.
Compose replaces these with composable functions that are far more flexible.

- **Flexibility:** You don't need a separate "SpannableString" class to bold one word; you just use `AnnotatedString`.
- **Composition:** You don't have a "Button with Image" widget. You just put an `Icon` _inside_ a `Button`.

### **3. Detailed Breakdown**

#### **A. Text (The Label)**

Displays read-only text.

- **Styling:** You don't look for an XML style file. You pass a `TextStyle` object (font, size, color) or `MaterialTheme.typography` styles.
- **Spans (AnnotatedString):** If you want "Hello **World**" (where World is bold), you don't use HTML tags. You use `buildAnnotatedString` to apply styles to specific character ranges.

#### **B. Button (The Clickable)**

Triggers an action.

- **Variants:** Material Design offers different levels of emphasis:
- `Button`: Solid background (High emphasis).
- `OutlinedButton`: Border only (Medium emphasis).
- `TextButton`: No border, no background (Low emphasis).

- **Content:** A Button is just a container. You _must_ put a `Text` or `Icon` inside it for it to show anything.

#### **C. Icon (The Symbol)**

Displays vector assets (SVG-like paths).

- **Vectors:** Uses `ImageVector` (often from `Icons.Default.Home`) or `painterResource` for local files.
- **Tinting:** Can easily change color using the `tint` parameter.
- **Accessibility:** Has a mandatory `contentDescription` field. This is what screen readers speak to blind users (e.g., "Back Button").

#### **D. Spacer (The Gap)**

An invisible box used to create space.

- **Usage:** Instead of adding "margin-right" to a button, you place a `Spacer` between two buttons.
- **Why:** It makes the spacing explicit and visible in the code structure.

#### **E. Surface (The Canvas)**

The fundamental "sheet of paper" in Material Design.

- **Role:** It handles the background color, the shape (rounded corners), the border, and the elevation (shadow).
- **Clipping:** If you set a shape (like a Circle), `Surface` clips its content to match that shape.

### **4. Example: Combining Them**

This example creates a "Card" look using Surface, containing a row of icons and text.

```kotlin
@Composable
fun UserCard() {
    // Surface provides the Background, Shadow (Elevation), and Shape
    Surface(
        shadowElevation = 4.dp,
        shape = RoundedCornerShape(8.dp),
        color = MaterialTheme.colorScheme.surface
    ) {
        // Row arranges items horizontally
        Row(modifier = Modifier.padding(16.dp)) {
            Icon(
                imageVector = Icons.Default.Person,
                contentDescription = "User Profile Image",
                tint = MaterialTheme.colorScheme.primary
            )

            // Adds a 16dp gap between Icon and Text
            Spacer(modifier = Modifier.width(16.dp))

            Text(
                text = "John Doe",
                style = MaterialTheme.typography.bodyLarge
            )
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
AnnotatedString, Slot API (Button content), Accessibility (contentDescription), Elevation, Z-Index, Painter vs Vector.

**Interview Speak Paragraph**

> "For basic UI construction, I rely on the standard Compose building blocks. I use `Surface` as the root container to handle elevation, clipping, and background colors. For spacing, I prefer using `Spacer` components rather than margins, as it makes the layout logic more readable in the code structure. When dealing with text that requires mixed styling—like making one word bold—I use `AnnotatedString` instead of splitting text into multiple composables. Finally, for buttons and icons, I strictly adhere to accessibility guidelines by ensuring every visual element has a meaningful `contentDescription`."

---

**Next Step:**
Now that we have the atoms, let's learn how to arrange them. Ready for **Topic 1.8: Layout Primitives: Column, Row, Box**? This is how we build the actual screen structure.

---

## Navigation

â† Previous
Next â†’
