---
layout: default
title: Bottom Sheets
parent: 6. Forms, Inputs & Sheets
nav_order: 4
---

# Bottom Sheets

Here are your notes for **Topic 6.4**.

---

## **Topic 6.4: Bottom Sheets**

### **1. What It Is**

A **Bottom Sheet** is a surface that slides up from the bottom of the screen to reveal more content. In Material 3 Compose, there are two distinct types:

- **`ModalBottomSheet`:** A temporary overlay. It dims the screen behind it (scrim) and blocks interaction with the rest of the app. (Example: "Share" menu, "Three-dot" options menu).
- **`BottomSheetScaffold`:** A persistent sheet. It stays on screen (usually collapsed at the bottom) and allows you to interact with the main content simultaneously. (Example: Google Maps location details, Spotify mini-player).

### **2. Why It Exists (Ergonomics & Context)**

- **Thumb Reach:** On tall phones, dialogs in the center are harder to reach. Bottom sheets bring interactive elements right to your thumb.
- **Mobile Native:** It feels more "mobile-native" than a web-style popup box.
- **Content Volume:** Unlike a Dialog which looks bad if it's too tall, a Bottom Sheet handles long lists (like a comment section) perfectly because it can scroll internally.

### **3. How It Works**

#### **A. Modal Bottom Sheet (The Overlay)**

This works similarly to an `AlertDialog`.

1. **State:** You use a boolean (`var showSheet by remember { mutableStateOf(false) }`) to decide _if_ it is in the UI tree.
2. **Sheet State:** You use `rememberModalBottomSheetState()` to control expanding/hiding animations.
3. **Scope:** You need a `CoroutineScope` to trigger the `.hide()` animation before you set `showSheet = false`.

#### **B. Bottom Sheet Scaffold (The Persistent)**

This is a layout container.

1. **Structure:** It has a `sheetContent` slot and a `body` slot.
2. **Behavior:** The sheet is always there. You don't "remove" it; you just change its state from `Expanded` to `PartiallyExpanded` (Peek).

### **4. Example: The Modal Action Sheet**

This is the most common pattern. Note the specific logic to hide it gracefully.

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CommentSection() {
    // 1. Controls IF the sheet exists in the tree
    var showSheet by remember { mutableStateOf(false) }

    // 2. Controls the animation logic
    val sheetState = rememberModalBottomSheetState()
    val scope = rememberCoroutineScope()

    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Button(onClick = { showSheet = true }) {
            Text("View Comments")
        }
    }

    // 3. The Sheet
    if (showSheet) {
        ModalBottomSheet(
            onDismissRequest = {
                // Handle user clicking outside or dragging down
                showSheet = false
            },
            sheetState = sheetState
        ) {
            // Content inside the sheet
            Text("This is the comment section", modifier = Modifier.padding(16.dp))
            Button(
                onClick = {
                    // 4. Graceful Close: Animate hide, THEN remove from tree
                    scope.launch { sheetState.hide() }.invokeOnCompletion {
                        if (!sheetState.isVisible) {
                            showSheet = false
                        }
                    }
                },
                modifier = Modifier.padding(16.dp)
            ) {
                Text("Close")
            }
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Modal vs. Persistent, Scrim, `rememberModalBottomSheetState`, `PartiallyExpanded`, CoroutineScope, `invokeOnCompletion`.

**Interview Speak Paragraph**

> "When implementing bottom sheets, I distinguish between Modal and Persistent use cases. For temporary actions like a 'Share' menu, I use `ModalBottomSheet`. The tricky part here is closing it programmatically: I launch a coroutine to call `sheetState.hide()`, and only inside the `invokeOnCompletion` block do I actually set the visibility boolean to false. This ensures the slide-down animation finishes before the component is removed from the composition. For permanent elements like a music player controller, I use `BottomSheetScaffold`, which keeps the sheet available while allowing interaction with the background content."

---

**Next Step:**
You have a form, but how do you stop the user from submitting empty fields?
Ready for **Topic 6.5: Form Validation Patterns [Added]**? This is the final polish for user input.

---

## Navigation

â† Previous
Next â†’
