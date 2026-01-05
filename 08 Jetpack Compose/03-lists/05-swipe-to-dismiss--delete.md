---
layout: default
title: "Swipe to Dismiss / Delete"
parent: "3. Lists, Grids & UI Enhancements"
nav_order: 5
---

# Swipe to Dismiss / Delete

Here are your notes for **Topic 3.5**.

---

## **Topic 3.5: Swipe to Dismiss / Delete**

### **1. What It Is**

This is the standard mobile gesture where a user swipes a list item horizontally (left or right) to perform an action, typically **deleting** or **archiving** it.
In Material 3 Compose, the component is named **`SwipeToDismissBox`** (previously `SwipeToDismiss` in older versions).

### **2. Why It Exists (Gesture Efficiency)**

- **Clean UI:** Putting a "Delete" trash can button on every single row makes the UI look cluttered and ugly.
- **Speed:** Swiping is a "gross motor skill"—it's faster and easier for users to swipe a whole row than to tap a tiny button.

### **3. How It Works (The 3 Layers)**

To build this, you wrap your list item in a `SwipeToDismissBox`. This composable requires three main things:

1. **The State (`SwipeToDismissBoxState`):** Tracks if the user is swiping, how far they swiped, and if the item should be dismissed. This is where you put your logic (e.g., "If fully swiped, delete from DB").
2. **The Background:** The UI layer that sits _behind_ the content. This is revealed as you swipe (e.g., a Red background with a Trash Icon).
3. **The Content:** The actual list item (your white row with text).

**The Logic Flow:**

- User starts drag -> Content moves.
- Background shows.
- User crosses the **Threshold** (usually 50%).
- User lifts finger -> State becomes `DismissedToStart` or `DismissedToEnd`.
- You react to this state change to remove the item from your list.

### **4. Example: The Swipe-to-Delete Implementation**

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SwipeableItem(
    item: String,
    onRemove: (String) -> Unit
) {
    val context = LocalContext.current

    // 1. Define the State & Logic
    val dismissState = rememberSwipeToDismissBoxState(
        confirmValueChange = { dismissValue ->
            // Check if the swipe was a "Delete" swipe
            if (dismissValue == SwipeToDismissBoxValue.EndToStart) {
                onRemove(item) // Actually remove data
                true // Return true to confirm the action
            } else {
                false
            }
        }
    )

    // 2. The Box Component
    SwipeToDismissBox(
        state = dismissState,
        // 3. The Background (The Red Layer)
        backgroundContent = {
            val color = if (dismissState.dismissDirection == SwipeToDismissBoxValue.EndToStart) {
                Color.Red
            } else {
                Color.Transparent
            }

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(color)
                    .padding(16.dp),
                contentAlignment = Alignment.CenterEnd
            ) {
                Icon(Icons.Default.Delete, contentDescription = "Delete", tint = Color.White)
            }
        },
        // 4. The Foreground (The List Item)
        content = {
            Card {
                Text(
                    text = item,
                    modifier = Modifier.fillMaxWidth().padding(16.dp)
                )
            }
        }
    )
}

```

### **5. Interview Prep**

**Interview Keywords**
`SwipeToDismissBox`, `confirmValueChange`, Thresholds, Background Content, `EndToStart` vs `StartToEnd`, Optimistic Updates.

**Interview Speak Paragraph**

> "To implement swipe-to-delete, I use the `SwipeToDismissBox` composable from Material 3. The core of the logic resides in `rememberSwipeToDismissBoxState`, specifically the `confirmValueChange` lambda. This is where I intercept the swipe completion event to trigger the data removal. It's crucial to define the `backgroundContent` carefully so the user receives visual feedback (like a red background) during the drag. I also ensure the actual list data is updated immediately; otherwise, the swipe animation will finish, but the item will snap back into place."

---

**Next Step:**
We can scroll, sort, and delete. Now let's make it fancy.
Ready for **Topic 3.6: HorizontalPager / VerticalPager**? This is how you build image carousels and Instagram-like swiping.

---

## Navigation

â† Previous
Next â†’
