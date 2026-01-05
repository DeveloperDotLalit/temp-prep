---
layout: default
title: derivedStateOf
parent: 2. State & Recomposition (The Core)
nav_order: 6
---

# derivedStateOf

Here are your notes for **Topic 2.6**.

---

## **Topic 2.6: derivedStateOf**

### **1. What It Is**

`derivedStateOf` is a performance tool used to convert a **rapidly changing** state (like a scroll position changing every pixel) into a **slowly changing** state (like a boolean "Is Scrolled?").

It creates a new State object that only updates its listeners when the _result_ of the calculation changes, not necessarily when the _inputs_ change.

### **2. Why It Exists (The "Firehose" Problem)**

Imagine scrolling a list.

- **The Input:** The scroll offset changes: 0px, 1px, 2px, 3px, 4px... (Updates 60 times a second).
- **The Logic:** You want to show a "Back to Top" button only when the user scrolls past 100px.
- **The Problem:** If you just write `val showButton = scrollOffset > 100`, your variable is recalculated and might trigger recompositions on every single pixel scroll. This is wasteful.
- **The Solution:** `derivedStateOf` acts like a filter. Even if the offset goes 101, 102, 103... the result of `offset > 100` remains `true`. `derivedStateOf` sees that `true` hasn't changed to `false`, so it **stops** the update from propagating to the UI.

### **3. How It Works (The Deduplication Filter)**

1. **Listen:** It tracks the states read inside its block.
2. **Calculate:** When those input states change, it runs the calculation.
3. **Compare:** It compares the new result with the old result.
4. **Notify or Silence:**

- If `New == Old`: It does nothing. (UI sleeps).
- If `New != Old`: It notifies the UI to recompose.

### **4. Example: The "Scroll to Top" Button**

**Without `derivedStateOf` (Bad Performance):**
If used directly in composition, any read of `firstVisibleItemIndex` triggers recomposition.

```kotlin
val listState = rememberLazyListState()

// BAD: This reads listState.firstVisibleItemIndex every time it changes (0, 1, 2...).
// The whole function might recompose on every pixel scroll.
val showButton = listState.firstVisibleItemIndex > 0

```

**With `derivedStateOf` (Optimized):**

```kotlin
val listState = rememberLazyListState()

// GOOD: derivedStateOf buffers the rapid changes.
// The downstream UI only hears about it when the boolean actually flips
// from False -> True (or vice versa).
val showButton by remember {
    derivedStateOf { listState.firstVisibleItemIndex > 0 }
}

if (showButton) {
    ScrollToTopButton() // Only recomposes when visibility actually toggles
}

```

### **5. Interview Prep**

**Interview Keywords**
Performance Optimization, Granularity of State, Deduplication, Throttling Updates, Scroll State, LazyListState.

**Interview Speak Paragraph**

> "I use `derivedStateOf` specifically to optimize performance when dealing with high-frequency state updates, such as scroll offsets or animation values. Its main purpose is to convert a rapidly changing state into a coarser, derived state. For example, if I need to show a 'Jump to Top' button when a list is scrolled, checking the scroll offset directly would trigger a recomposition on every pixel. By wrapping that logic in `derivedStateOf`, the system only triggers a recomposition when the resulting boolean actually changes value, effectively dropping the thousands of unnecessary intermediate updates."

---

**Next Step:**
We've optimized local state. But what if you need to pass data deep down the tree without passing arguments through 10 layers?
Ready for **Topic 2.7: CompositionLocal [Added - Advanced]**? This is how Themes work under the hood.

---

## Navigation

â† Previous
Next â†’
