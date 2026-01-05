---
layout: default
title: System Back Handling
parent: 5. Side-Effects & Lifecycles
nav_order: 6
---

# System Back Handling

Here are your notes for **Topic 5.6**.

---

## **Topic 5.6: System Back Handling**

### **1. What It Is**

System Back Handling is the ability to **intercept** the physical back button or the back gesture swipe on an Android device.
Instead of the default action (which usually destroys the current screen or closes the app), you can run your own custom logic first.

The tool for this in Compose is the **`BackHandler`** composable.

### **2. Why It Exists (The "Modal" Problem)**

Default Android behavior pop the Navigation Stack. But sometimes, "Back" shouldn't mean "Go back to the previous screen."

- **Scenario 1 (Drawers):** If a side menu is open, pressing Back should close the menu, not close the app.
- **Scenario 2 (Forms):** If the user has typed a long email but hasn't sent it, pressing Back should show "Save Draft?" dialog, not just delete their work.

### **3. How It Works (LIFO Priority)**

The `BackHandler` is smart. It follows a **Last-In, First-Out (LIFO)** priority system.

- If you have 3 composables on screen, and all 3 have a `BackHandler`, the one deemed "most active" (usually the deepest in the hierarchy or latest added) catches the event.
- **The `enabled` flag:** You can turn the listener on or off dynamically. If `enabled = false`, the handler is ignored, and the system looks for the next handler up the chain.

### **4. Example: The "Unsaved Changes" Guard**

We want to stop the user from exiting if they have unchecked checkboxes.

```kotlin
@Composable
fun SurveyScreen(navController: NavController) {
    var hasUnsavedChanges by remember { mutableStateOf(false) }
    var showExitDialog by remember { mutableStateOf(false) }

    // 1. Intercept the Back Press
    // Only active if 'hasUnsavedChanges' is true.
    // If false, the system handles Back normally (pops the stack).
    BackHandler(enabled = hasUnsavedChanges) {
        // 2. Custom Logic: Don't exit yet! Show the dialog.
        showExitDialog = true
    }

    if (showExitDialog) {
        AlertDialog(
            onDismissRequest = { showExitDialog = false },
            title = { Text("Exit?") },
            text = { Text("You will lose your progress.") },
            confirmButton = {
                TextButton(onClick = {
                    // 3. Force exit (Navigating up ignores the BackHandler)
                    navController.popBackStack()
                }) { Text("Exit") }
            },
            dismissButton = {
                TextButton(onClick = { showExitDialog = false }) { Text("Stay") }
            }
        )
    }

    // ... Content where user sets hasUnsavedChanges = true ...
}

```

### **5. Interview Prep**

**Interview Keywords**
`BackHandler`, `OnBackPressedDispatcher`, Interception, LIFO Priority, Predictive Back Gesture, Modal Logic.

**Interview Speak Paragraph**

> "In Compose, managing the system back button is handled by the `BackHandler` composable. It registers a callback with the Activity's `OnBackPressedDispatcher`. The key behavior to understand is that it respects the composition hierarchy—if multiple handlers are present, the innermost active handler wins. I commonly use this for custom UI states like closing an open Navigation Drawer or showing a 'Discard Changes' dialog on a form. By toggling the `enabled` parameter, I can dynamically decide whether to intercept the event or let the system handle standard navigation."

---

**Congratulations!** You have completed **Part 5: Side-Effects & Lifecycles**.
You can now safely run code, manage memory, and handle system events.

Now, let's build the interactive parts of the UI.
**Are you ready to start Topic 6: Forms, Inputs & Sheets?**

---

## Navigation

â† Previous
