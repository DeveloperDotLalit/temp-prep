---
layout: default
title: Dialogs & Popups
parent: 3. Lists, Grids & UI Enhancements
nav_order: 7
---

# Dialogs & Popups

Here are your notes for **Topic 3.7**.

---

## **Topic 3.7: Dialogs & Popups**

### **1. What It Is**

These are UI layers that float **on top** of your main screen content.

- **`AlertDialog`:** The standard Android system dialog (Title, Message, Confirm/Cancel buttons).
- **`Dialog`:** A blank canvas modal. You can put _anything_ inside it (e.g., a login form, a color picker).
- **`Popup`:** A lightweight overlay that anchors to a specific location (used for tooltips, dropdown menus).

### **2. Why It Exists (Focus & Context)**

Sometimes you need to interrupt the user to get an answer ("Delete this file?") or show extra info ("Help text") without navigating to a completely new screen.

- **Modality:** Dialogs are "Modal," meaning they block the content behind them. You _must_ interact with or dismiss the dialog to go back to the app.
- **Independent Window:** Technically, these composables create a separate `Window` layer on top of your Activity. This is why they can float over everything, including the status bar.

### **3. How It Works**

#### **A. The `onDismissRequest` (Mandatory)**

Every dialog requires an `onDismissRequest` lambda. This is called when the user clicks the dark background (scrim) or presses the physical Back button.

- **Crucial Logic:** You must manually set your state (e.g., `showDialog = false`) inside this lambda. If you leave it empty, the dialog will never close!

#### **B. `DialogProperties**`

You can customize behavior using `properties`:

- `dismissOnBackPress`: Allow closing via back button? (Default: True).
- `dismissOnClickOutside`: Allow closing by tapping the background? (Default: True).
- `usePlatformDefaultWidth`: If false, the dialog can stretch to the full screen width.

### **4. Example: Standard vs. Custom**

**Scenario A: The Standard Alert (Easy)**

```kotlin
@Composable
fun DeleteConfirmation(
    onConfirm: () -> Unit,
    onDismiss: () -> Unit
) {
    AlertDialog(
        onDismissRequest = { onDismiss() }, // Handle back press/click outside
        title = { Text("Delete Item?") },
        text = { Text("This action cannot be undone.") },
        confirmButton = {
            TextButton(onClick = onConfirm) { Text("Delete") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}

```

**Scenario B: The Custom Dialog (Flexible)**

```kotlin
@Composable
fun CustomLoadingDialog(onDismiss: () -> Unit) {
    Dialog(
        onDismissRequest = { onDismiss() },
        properties = DialogProperties(dismissOnBackPress = false, dismissOnClickOutside = false)
    ) {
        // This is your canvas. Design whatever you want.
        Card(
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.padding(16.dp)
        ) {
            Column(
                modifier = Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                CircularProgressIndicator()
                Spacer(Modifier.height(16.dp))
                Text("Please wait...")
            }
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Modal, `onDismissRequest`, Scrim (Dark background), `DialogProperties`, Separate Window, Overlay.

**Interview Speak Paragraph**

> "For user alerts, I use `AlertDialog` for standard confirmations because it enforces Material Design guidelines automatically. For more complex overlays, like a loading spinner or a custom input form, I use the `Dialog` composable. The most important parameter to handle is `onDismissRequest`. Since Compose follows a unidirectional data flow, the dialog doesn't close itself; I must explicitly update the state variable to `false` inside that callback. For non-modal overlays like tooltips that anchor to specific elements, I use `Popup` instead."

---

**Next Step:**
We have static images, but real apps load images from the internet.
Ready for **Topic 3.8: Image Loading (Coil/Glide)**? This is one of the few places where we _must_ use a 3rd party library in Compose.

---

## Navigation

â† Previous
Next â†’
