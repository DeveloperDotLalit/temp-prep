---
layout: default
title: "Grids: LazyVerticalGrid / StaggeredGrid"
parent: "3. Lists, Grids & UI Enhancements"
nav_order: 3
---

# Grids: LazyVerticalGrid / StaggeredGrid

Here are your notes for **Topic 3.3**.

---

## **Topic 3.3: Grids: LazyVerticalGrid / StaggeredGrid**

### **1. What It Is**

These are the Composable equivalents of a `RecyclerView` with a `GridLayoutManager` or `StaggeredGridLayoutManager`.

- **`LazyVerticalGrid`:** Creates a standard grid where all cells in a row have the same height. (Think: Android Gallery app).
- **`LazyVerticalStaggeredGrid`:** Creates a "Masonry" layout where items can have different heights, and they pack together tightly. (Think: Pinterest feed).

### **2. Why It Exists**

Displaying data in a single column is boring. Sometimes you want 2, 3, or more items per row.

- **The Responsive Problem:** On a phone, you might want 2 columns. On a tablet, you want 4. Hardcoding "2" is bad.
- **The "Gap" Problem:** In a standard grid, if one image is tall and the other is short, you get ugly empty white space. Staggered Grids solve this by interlocking items like a puzzle.

### **3. How It Works**

#### **A. The `columns` Parameter**

You control the grid structure using `GridCells`:

1. **`GridCells.Fixed(count)`:** Forces exactly `count` columns. (e.g., Always 2 columns).
2. **`GridCells.Adaptive(minSize)`:** **The Magic One.** You say, "I want items to be at least 128dp wide."

- On a small phone: It fits 2 items.
- On a tablet: It fits 5 items.
- _Result:_ Automatic responsiveness!

#### **B. The Staggered Logic**

`LazyVerticalStaggeredGrid` accepts `StaggeredGridCells`. It places the next item in whichever column is currently shortest, filling gaps naturally.

### **4. Example: Adaptive vs. Staggered**

**Scenario A: Photo Gallery (Standard Grid)**
Responsive grid that fits as many 120dp columns as possible.

```kotlin
@Composable
fun PhotoGallery(photos: List<Photo>) {
    LazyVerticalGrid(
        // MAGIC: Adapts to screen width automatically
        columns = GridCells.Adaptive(minSize = 120.dp),

        // Adds space between grid items
        verticalArrangement = Arrangement.spacedBy(4.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        items(photos) { photo ->
            PhotoCard(photo)
        }
    }
}

```

**Scenario B: Pinterest Note Feed (Staggered)**
Items have random heights (short notes vs long notes).

```kotlin
@Composable
fun NoteFeed(notes: List<Note>) {
    LazyVerticalStaggeredGrid(
        columns = StaggeredGridCells.Fixed(2),
        verticalItemSpacing = 4.dp,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        items(notes) { note ->
            // If this card is taller, the grid adjusts automatically
            NoteCard(note)
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Adaptive Layouts, GridCells, Masonry Layout, Staggered Grid, Responsive UI, `minSize`.

**Interview Speak Paragraph**

> "For grid layouts, I prefer `LazyVerticalGrid` over manual implementations because of its powerful `GridCells.Adaptive` feature. This allows the layout to be responsive out of the box—adding more columns on tablets and fewer on phones—without writing custom calculation logic. If I'm dealing with content of varying heights, like a user-generated feed, I switch to `LazyVerticalStaggeredGrid` to achieve a masonry or 'Pinterest-style' look, which eliminates awkward whitespace gaps between items."

---

**Next Step:**
You have a grid, but what if you want to group items with titles?
Ready for **Topic 3.4: Sticky Headers [Added]**? This is a classic UI pattern for contact lists (A, B, C...).

---

## Navigation

â† Previous
Next â†’
