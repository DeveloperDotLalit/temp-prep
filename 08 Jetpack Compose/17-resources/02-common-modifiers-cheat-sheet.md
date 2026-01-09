---
layout: default
title: Common Modifiers Cheat Sheet
parent: 17. Resources & Cheat Sheets
nav_order: 2
---

# Common Modifiers Cheat Sheet

Here are your notes for **Topic 1.6**.

---

## **Topic 1.6: Common Modifiers Cheat Sheet**

### **1. What It Is**

Modifiers are standard Kotlin objects used to decorate or augment a Composable.
They are chainable methods that tell a UI element how to lay itself out, how to display, or how to behave.

**The Golden Rule:** **Order Matters.**
Modifiers are applied from left to right (or top to bottom).

- **Outer Layer first:** The first modifier touches the "outside" world.
- **Inner Layer last:** The last modifier touches the content.

### **2. The Cheat Sheet**

#### **A. Sizing (How big am I?)**

| Modifier               | Description                                                 |
| ---------------------- | ----------------------------------------------------------- |
| `.fillMaxSize(1f)`     | Fills 100% of the parent's available space.                 |
| `.fillMaxWidth()`      | Fills width only.                                           |
| `.size(50.dp)`         | Sets hard width and height to 50dp.                         |
| `.width(100.dp)`       | Sets only width.                                            |
| `.heightIn(min=40.dp)` | Dynamic height, but never smaller than 40dp.                |
| `.weight(1f)`          | **(Row/Col only)** Takes up remaining space proportionally. |
| `.wrapContentSize()`   | Ignores minimum size constraints and wraps content.         |

#### **B. Spacing (Margin vs. Padding)**

In Compose, **there is no Margin modifier.**

- To create a **Margin** (space _outside_ the background): Add `padding` **before** `background`.
- To create **Padding** (space _inside_ the background): Add `padding` **after** `background`.

| Modifier                      | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `.padding(16.dp)`             | 16dp on all 4 sides.                                      |
| `.padding(horizontal = 8.dp)` | 8dp Left & Right only.                                    |
| `.offset(x, y)`               | Shifts the element visually without changing layout flow. |

#### **C. Styling (How do I look?)**

| Modifier                     | Description                                  |
| ---------------------------- | -------------------------------------------- |
| `.background(Color.Red)`     | Fills the shape with color.                  |
| `.border(2.dp, Color.Black)` | Adds a border stroke.                        |
| `.clip(CircleShape)`         | Crops the content (image/box) to a shape.    |
| `.alpha(0.5f)`               | Sets opacity (0.0 = invisible, 1.0 = solid). |
| `.shadow(elevation)`         | Adds a shadow (requires a shape).            |

#### **D. Actions (What can I do?)**

| Modifier                  | Description                                   |
| ------------------------- | --------------------------------------------- |
| `.clickable { }`          | Makes it tappable and adds a Ripple effect.   |
| `.combinedClickable(...)` | Adds Long Click and Double Click support.     |
| `.verticalScroll(...)`    | Makes a Column scrollable (for simple lists). |
| `.toggleable(...)`        | For Checkboxes/Switches (Semantics support).  |

### **3. Alignment (Scope Specific)**

Some modifiers only exist when you are inside a specific parent.

- **Inside `Column`:** `.align(Alignment.Start / CenterHorizontally / End)`
- **Inside `Row`:** `.align(Alignment.Top / CenterVertically / Bottom)`
- **Inside `Box`:** `.align(Alignment.TopStart / Center / BottomEnd)`

### **4. Example: The "Order Matters" Trap**

**Scenario:** A button with a border, space outside, and space inside.

```kotlin
Box(
    modifier = Modifier
        .padding(20.dp)          // 1. MARGIN (Outer space)
        .background(Color.Blue)  // 2. BACKGROUND COLOR
        .padding(10.dp)          // 3. PADDING (Inner space)
        .border(2.dp, Color.Red) // 4. BORDER (Inside the blue area)
) {
    Text("Hello")
}

```

### **5. Interview Prep**

**Interview Keywords**
Chaining order, Scope-specific modifiers (`weight`, `align`), `padding` vs margin logic, `clickable` ripple, `fillMaxSize` vs `wrapContent`.

**Interview Speak Paragraph**

> "Modifiers in Compose are immutable objects that decorate composables. The most critical concept is that **order matters**. Modifiers are applied sequentially, like wrapping layers of an onion. For example, applying `padding` before `background` creates a margin effect, while applying it after creates internal padding. I also utilize scope-specific modifiers like `weight` inside Rows and Columns to create flexible layouts, and `clip` to enforce shapes on images and surfaces."

---

**Next Step:**
You have the blocks. Now, how do you handle data changing?
Ready for **Part 2: State Management & Performance**?

---

## Navigation

â† Previous
Next â†’
