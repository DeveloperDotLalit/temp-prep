---
layout: default
title: Stability System
parent: 12. Performance & Internals
nav_order: 1
---

# Stability System

Here are your notes for **Topic 2.6**.

---

## **Topic 2.6: Stability System**

### **1. What It Is**

Compose is "lazy." It wants to **skip** recomposing parts of the UI that haven't changed.
To do this, it needs to know if your data is **Stable**.

- **Stable:** "I promise this data won't change mysteriously. If it changes, I will notify you (like `MutableState`)."
- **Unstable:** "This is just a regular mutable object. It might change behind my back, so I have to redraw just in case."

### **2. Why It Exists (The "Performance" Guard)**

If you pass a regular `List<String>` or a generic class to a Composable, Compose assumes it is **Unstable**.
Why? Because `List` is an interface. It _could_ be a `MutableList`. If someone adds an item to that list _outside_ of Compose, Compose wouldn't know. To be safe, it redraws the whole list every frame. This kills performance.

### **3. How It Works**

#### **A. The Annotations**

You can force Compose to trust your data.

- **`@Immutable`:** "This object will **never** change." (e.g., A `data class` with only `val` properties).
- **`@Stable`:** "This object might change, but if it does, I promise to use State/Flow so you know about it."

#### **B. Inferred Stability**

Compose tries to guess.

- **Primitives (Int, String):** Always Stable.
- **Data Class with `val`:** Stable.
- **Data Class with `var`:** Unstable (unless backed by `MutableState`).
- **Collections (`List`, `Map`):** **Always Unstable** (by default). This is the #1 trap!

### **4. Example: The "List" Trap**

**The Problem:**
Even if you use `val list: List<String>`, Compose treats it as unstable because `List` is an interface.

```kotlin
// BAD: This will recompose deeply every time, even if data is same.
@Composable
fun UserList(names: List<String>) { ... }

```

**The Fix (Immutable Wrapper):**
Wrap the list in a class annotated with `@Immutable`.

```kotlin
@Immutable
data class UserListState(val names: List<String>)

// GOOD: Compose sees 'UserListState' is immutable, so it skips this if unchanged.
@Composable
fun UserList(state: UserListState) { ... }

```

_Note: You can also use `kotlinx.collections.immutable` (ImmutableList) which Compose supports natively if configured._

### **5. Interview Prep**

**Interview Keywords**
Skipping, Recomposition, `@Stable`, `@Immutable`, Inferred Stability, `List` interface trap, `kotlinx.collections.immutable`.

**Interview Speak Paragraph**

> "One of the most critical performance optimizations in Compose is ensuring data stability to enable **Skipping**. By default, Compose treats standard interfaces like `List` as unstable because they could be mutable. This prevents smart recomposition. To fix this, I either use the `kotlinx.collections.immutable` library or wrap my collections in a data class annotated with `@Immutable`. This gives the Compose compiler the guarantee it needs to skip recomposition when the data hasn't changed."

---

**Next Step:**
We've optimized the data, but what about the memory?
Ready for **Topic 2.7: Side-Effects & Cleanup**? (Wait... we covered Side Effects in Topic 5. Let's move to **Lists & Grids**).

**Are you ready to start Part 3: Lists, Grids & UI Enhancements?**

---

## Navigation

Next â†’
