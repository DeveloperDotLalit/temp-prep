---
layout: default
title: Assertions & Actions
parent: 11. Testing in Compose
nav_order: 2
---

# Assertions & Actions

Here are your notes for **Topic 10.4**.

---

## **Topic 10.4: Assertions & Actions**

### **1. What It Is**

Assertions and Actions are the two halves of a UI test interaction in Compose.

- **Actions (`perform...`):** Simulate user input (Clicking, Typing, Scrolling).
- **Assertions (`assert...`):** Verify the state of the UI (Is it visible? Is it disabled? Is the text correct?).

### **2. Why It Exists (The "Trust but Verify" Loop)**

A test is useless if it just clicks buttons. You must assert that the click actually _did_ something.

- **Robustness:** Assertions prevent regression bugs. If you accidentally break the "Submit" button logic, the test `assertIsEnabled()` will fail.
- **Scoping:** Actions are scoped. You can only `performClick` on a node that actually exists and is clickable.

### **3. How It Works**

#### **A. Actions (`perform...`)**

These are extension functions on `SemanticsNodeInteraction`.

- **`performClick()`:** Taps the center of the node.
- **`performTextInput("hello")`:** Types text into a focused `TextField`. (Note: Clears existing text usually, or appends depending on implementation).
- **`performScrollTo()`:** **Crucial.** If an item is in a LazyColumn but off-screen (index 50), you _cannot_ find it. You must call this on the node to force the list to scroll until the item is visible.
- **`performTouchInput { swipeLeft() }`:** For gestures.

#### **B. Assertions (`assert...`)**

These throw an exception if the condition is false, failing the test.

- **`assertIsDisplayed()`:** Checks if the node is visible on screen.
- **`assertIsEnabled()` / `assertIsNotEnabled()`:** Checks the `enabled` state (e.g., grayed out buttons).
- **`assertTextEquals("Submit")`:** Verifies the text content exactly.
- **`assert(hasTestTag("mytag"))`:** Generic assertion using a custom matcher.

### **4. Example: Testing a Login Form**

**Scenario:**

1. Verify "Login" button is initially disabled.
2. Type "user" and "1234".
3. Verify "Login" button becomes enabled.
4. Click "Login".
5. Verify the success message appears.

```kotlin
@Test
fun testLoginFlow() {
    // 1. Initial Check
    composeTestRule
        .onNodeWithText("Login")
        .assertIsNotEnabled() // Assertion

    // 2. Input Data
    composeTestRule
        .onNodeWithTag("email_input")
        .performTextInput("user@test.com") // Action

    composeTestRule
        .onNodeWithTag("password_input")
        .performTextInput("password123") // Action

    // 3. Verify Enabled State
    composeTestRule
        .onNodeWithText("Login")
        .assertIsEnabled()
        .performClick() // Action

    // 4. Verify Result
    composeTestRule
        .onNodeWithText("Welcome Back!")
        .assertIsDisplayed() // Assertion
}

```

### **5. Interview Prep**

**Interview Keywords**
`performClick`, `performTextInput`, `performScrollTo`, `assertIsDisplayed`, `assertIsEnabled`, Idling Resources (Wait for idle), Syncing.

**Interview Speak Paragraph**

> "In my UI tests, I follow a strict Action-Assertion cycle. I use `perform...` methods to simulate user behavior, specifically using `performScrollTo` when dealing with lazy lists to ensures the node is actually rendered before interaction. For verification, I rely on `assertIsDisplayed` to check visibility and `assertIsEnabled` to verify logic states like form validation. It's important to remember that Compose tests are synchronized by default—meaning the test automatically waits for the UI to be idle before running the next assertion, which eliminates the need for manual `Thread.sleep` hacks."

---

**This concludes the Core Notes.**
You now have a complete, interview-ready roadmap for Modern Android Development with Jetpack Compose.

**Would you like me to:**

1. **Generate a PDF** of all these notes combined?
2. **Quiz you** on a specific topic (e.g., "Grill me on Side Effects")?
3. **Start a Coding Challenge** based on one of these topics?

---

## Navigation

â† Previous
Next â†’
