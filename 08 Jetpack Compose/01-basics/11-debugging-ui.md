---
layout: default
title: Debugging UI
parent: 1. Introduction + Basic Composables
nav_order: 11
---

# Debugging UI

Here are your notes for **Topic 1.11**.

---

## **Topic 1.11: Debugging UI**

### **1. What It Is**

Debugging UI involves using specific tools provided by Android Studio to inspect, visualize, and troubleshoot your Compose layouts. Since you don't have an XML file to "look at," you need tools that can read the compiled Kotlin UI tree.

### **2. Why It Exists**

In declarative UI, bugs are often invisible in the code.

- **The "Zero Size" Bug:** You added a text, but it’s not showing. Is it hidden? Is it white text on a white background? Or is its size 0dp?
- **The "Recomposition" Bug:** Why is my app lagging? Is this list item redrawing 100 times a second?
- You cannot solve these by just reading the code. You need tools to "X-ray" the running app.

### **3. The Toolset**

#### **A. Layout Inspector (The X-Ray)**

This is your primary tool for debugging running apps.

- **How to access:** `Tools -> Layout Inspector`.
- **What it does:** It connects to your emulator/device and shows the live 3D layers of your UI.
- **Killer Feature - Recomposition Counts:** It shows two numbers next to each composable (e.g., `3 / 0`).
- First number: How many times it recomposed (redrew).
- Second number: How many times it was skipped (good performance).
- _If you see a static button recomposing 50 times while you scroll a list, you have a performance bug._

#### **B. @Preview (Design Time)**

Allows you to see your UI without building the whole app.

- **Annotation:** Add `@Preview` above a composable.
- **Parameters:**
- `showBackground = true`: Adds a white background (useful for transparent text).
- `device = "id:pixel_5"`: Shows how it looks on a specific phone.
- `uiMode = Configuration.UI_MODE_NIGHT_YES`: Previews Dark Mode.

- **Multipreview:** You can define a custom annotation (e.g., `@DevicePreviews`) that bundles multiple previews (Phone, Tablet, Dark Mode) so you don't have to write them every time.

#### **C. Interactive Preview**

- **What it is:** A "mini-emulator" inside the design window.
- **Usage:** Click the "Touch/Finger" icon in the Preview pane.
- **Why use it:** To test quick interactions like button clicks, scrolling a list, or typing in a text field without waiting for the full Gradle build and install process.

#### **D. Deploy to Device**

- **What it is:** Running the app on a real phone.
- **Why use it:** Previews are simulations. They don't perfectly replicate hardware performance, notch handling, or specific OEM quirks (like Samsung's OneUI behavior). Always test on real hardware before shipping.

### **4. Example: Setting up a Useful Preview**

Don't just write `@Preview`. Make it useful.

```kotlin
// Create a preview that checks both Light and Dark mode at once
@Preview(name = "Light Mode", showBackground = true)
@Preview(
    name = "Dark Mode",
    uiMode = Configuration.UI_MODE_NIGHT_YES,
    showBackground = true
)
@Composable
fun UserCardPreview() {
    // Wrap in your theme to ensure fonts/colors work
    MyAppTheme {
        UserCard(name = "Test User")
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Layout Inspector, Recomposition Counts, Semantic Tree, Interactive Preview, Multipreview, Skipped compositions.

**Interview Speak Paragraph**

> "When debugging Compose UI, my first line of defense is the `@Preview` tool for visual verification of different states and dark mode. For runtime issues, I rely heavily on the **Layout Inspector**. It not only lets me visualize the UI hierarchy and check for zero-sized elements but provides critical performance insights through **Recomposition Counts**. If I see a component recomposing unexpectedly during unrelated state changes, I know I need to optimize my state stability or side effects."

---

**Congratulations!** You have completed **Part 1: Introduction + Basic Composables**.
You now have a solid foundation in _how_ to build static UIs.

The next section is the most critical part of Jetpack Compose. It separates the beginners from the pros.
**Are you ready to start Topic 2: State & Recomposition (The Core)?**

---

## Navigation

â† Previous
