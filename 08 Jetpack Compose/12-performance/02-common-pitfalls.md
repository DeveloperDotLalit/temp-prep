---
layout: default
title: Common Pitfalls
parent: 12. Performance & Internals
nav_order: 2
---

# Common Pitfalls

Here are your notes for **Topic 2.7**.

---

## **Topic 2.7: Common Pitfalls & Performance**

### **1. What It Is**

This topic covers the two most common mistakes that kill Compose performance:

1. **Reading State Too Early:** Reading a changing value (like scroll position) directly in the Composition phase instead of deferring it to the Layout or Draw phase.
2. **Unnecessary Allocations:** Creating new objects inside a Composable function that runs 60 times a second.

### **2. Why It Exists (The 3 Phases)**

Compose renders in three steps:

1. **Composition:** "What to show?" (Heavy logic, tree building).
2. **Layout:** "Where to put it?" (Measuring size and position).
3. **Draw:** "How to paint it?" (Pixels on screen).

**The Golden Rule:** If a value changes rapidly (like an animation or scroll offset), read it in the **latest phase possible** (Draw). If you read it in Composition, you force the entire tree to rebuild every millisecond.

### **3. Pitfall 1: Reading State in Composition (The "Jank" Maker)**

**The Wrong Way (Recomposes constantly):**
You want the background color to change as you scroll.

```kotlin
@Composable
fun BadHeader(scrollState: ScrollState) {
    // BAD: Reading 'value' here forces Recomposition every pixel you scroll.
    val offset = scrollState.value

    Box(
        modifier = Modifier
            .background(if (offset > 100) Color.Red else Color.Blue)
    )
}

```

**The Right Way (Deferring Reads):**
Use a lambda `() ->` or specific modifiers like `drawBehind` or `graphicsLayer` to read the state only during the Draw phase.

```kotlin
@Composable
fun GoodHeader(scrollState: ScrollState) {
    Box(
        modifier = Modifier
            .drawBehind {
                // GOOD: This block only runs during the DRAW phase.
                // Composition is skipped entirely!
                val color = if (scrollState.value > 100) Color.Red else Color.Blue
                drawRect(color)
            }
    )
}

```

### **4. Pitfall 2: Unnecessary Object Allocations**

**The Wrong Way:**
Creating a list or a formatter inside the function body.

```kotlin
@Composable
fun UserList(users: List<User>) {
    // BAD: A new 'SimpleDateFormat' is created 100 times if this recomposes.
    val formatter = SimpleDateFormat("yyyy-MM-dd")

    // BAD: 'sortedBy' creates a NEW list every single time.
    val sortedUsers = users.sortedBy { it.name }

    LazyColumn { ... }
}

```

**The Right Way:**
Use `remember` to cache expensive objects.

```kotlin
@Composable
fun UserList(users: List<User>) {
    // GOOD: Created once, reused forever.
    val formatter = remember { SimpleDateFormat("yyyy-MM-dd") }

    // GOOD: Calculation only runs if 'users' list actually changes.
    val sortedUsers = remember(users) {
        users.sortedBy { it.name }
    }

    LazyColumn { ... }
}

```

### **5. Interview Prep**

**Interview Keywords**
Deferring State Reads, Layout vs Draw Phase, `derivedStateOf`, `remember` keys, Premature Optimization, Recomposition Loops.

**Interview Speak Paragraph**

> "The most common performance pitfall in Compose is reading state in the wrong phase. If I read a rapidly changing value—like a scroll offset—directly in the Composition phase, it triggers a full recomposition on every frame. To prevent jank, I defer these reads to the Layout or Draw phases using lambda-based modifiers like `.offset {}` or `.drawBehind {}`. This skips the expensive Composition phase entirely. Additionally, I avoid object allocation inside composables by strictly using `remember` for expensive operations like sorting lists or formatting dates."

---

**Next Step:**
You have mastered State. Now, how do we display that data in long, scrolling lists?
Ready for **Part 3: Lists, Grids & UI Enhancements**?

---

## Navigation

â† Previous
Next â†’
