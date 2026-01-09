---
layout: default
title: TalkBack & Font Scaling
parent: 14. Accessibility (A11y)
nav_order: 2
---

# TalkBack & Font Scaling

Here are your notes for **Topic 10.9**.

---

## **Topic 10.9: TalkBack & Font Scaling**

### **1. What It Is**

- **TalkBack:** Google's screen reader service for Android. It allows blind and low-vision users to interact with devices using gestures and spoken feedback without seeing the screen.
- **Font Scaling:** The Android system setting that allows users to increase the font size (up to 200%) or display size.
- **The Goal:** Your app must be fully usable even when the text is huge and the user cannot see the UI.

### **2. Why It Exists (Inclusivity & Compliance)**

- **Legal:** Many countries (like the US/EU) require apps to be accessible (ADA/EAA compliance).
- **User Base:** A significant percentage of users set their font size to "Large" or "Huge" because of standard age-related vision loss. If your app breaks at 2x font size, you lose these users.

### **3. How It Works**

#### **A. The SP vs DP Rule**

- **`dp` (Density-independent Pixels):** Based on screen density. Use for **layout shapes** (padding, icons, buttons containers).
- **`sp` (Scale-independent Pixels):** Based on screen density **AND** user font preference. Use for **TEXT**.
- _Trap:_ If you define text size in `dp`, it will ignore the user's settings. This is an immediate accessibility violation.

#### **B. The "Fixed Height" Trap**

Never set a fixed height on a container with text (e.g., `Modifier.height(50.dp)`).

- **Why?** If the user sets fonts to 200%, the text will grow to 80dp, overflow the 50dp box, and be clipped (invisible).
- **Fix:** Use `Modifier.heightIn(min = 50.dp)` or `wrapContentHeight()`. This allows the box to grow if the text grows.

#### **C. Touch Targets (48dp Rule)**

Buttons must be large enough to tap easily, especially for users with motor impairments.

- **Requirement:** Interactable elements should be at least **48x48dp**.
- **Compose Helper:** Material components (like `Button` or `Checkbox`) handle this automatically. If you make a custom clickable `Box`, use `Modifier.minimumInteractiveComponentSize()`.

### **4. Example: The Scalable Row**

**The Bad Way (Breaks at 200% scale):**

```kotlin
Row(modifier = Modifier.height(50.dp)) { // BAD: Fixed height
    Text("Settings", fontSize = 16.dp)     // BAD: Using dp for text
    // Result: Text won't scale, or if it does, it will get cut off.
}

```

**The Good Way (Adapts to any scale):**

```kotlin
Row(
    modifier = Modifier
        .fillMaxWidth()
        .heightIn(min = 48.dp) // GOOD: Grows if text gets huge
        .padding(vertical = 8.dp),
    verticalAlignment = Alignment.CenterVertically
) {
    Text(
        text = "Settings",
        fontSize = 16.sp // GOOD: Respects system font size
    )
}

```

### **5. Interview Prep**

**Interview Keywords**
TalkBack, Linear Navigation, `sp` vs `dp`, `heightIn` vs `height`, 48dp Touch Target, `minimumInteractiveComponentSize`, Dynamic Type, Clipping.

**Interview Speak Paragraph**

> "Ensuring my apps work with TalkBack and Dynamic Type is a standard part of my development process. I strictly use `sp` for all text dimensions to respect user font preferences. Crucially, I avoid using fixed heights on containers that hold text; instead, I use `Modifier.heightIn(min = 48.dp)` or `wrapContentHeight()`. This ensures that if a user scales their font to 200%, the UI expands vertically to accommodate the content rather than clipping it. I also manually test using the Accessibility Scanner app and by enabling TalkBack on my device to verify the navigation order and touch target sizes."

---

**This concludes the core notes on Testing & Interoperability.**

You now have a complete, interview-ready roadmap for Modern Android Development with Jetpack Compose.

**What would you like to do next?**

1. **Download PDF:** I can format _all_ 11 parts into a single structured document.
2. **Mock Interview:** I can simulate a Tech Lead interviewing you on these topics.
3. **Code Challenge:** I can give you a "Take Home Assignment" prompt to build a mini-app using these skills.

---

## Navigation

â† Previous
