---
layout: default
title: "Actions & Assertions"
parent: "Phase 7: Jetpack Compose Testing"
nav_order: 3
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 7.3**.

You know how to find the node. Now you need to drive it. The syntax is very similar to Espresso, but the engine under the hood is completely different.

---

# **Chapter 7: Jetpack Compose Testing**

## **Topic 7.3: Actions & Assertions**

### **1. The Interaction Chain**

Just like the Espresso Formula, Compose testing follows a fluent chain.

```kotlin
composeTestRule
    .onNodeWithText("Login")  // Finder
    .performClick()           // Action
    .assertDoesNotExist()     // Assertion

```

### **2. Actions (`perform...`)**

Once you have a `SemanticsNodeInteraction` (the result of `onNode`), you can perform actions on it.

#### **A. Clicks & Taps**

- **`performClick()`**: The standard tap.
- _Requirement:_ The node must have the `OnClick` semantic action defined (Buttons have this by default).

- **`performTouchInput { longClick() }`**: For long presses.
- **`performTouchInput { doubleClick() }`**: For double taps.

#### **B. Text Input**

- **`performTextInput("user123")`**: Simulates typing keys one by one. Use this if your app listens to specific key events.
- **`performTextReplacement("user123")`**: Clears the field and sets the text instantly.
- _Elite Tip:_ Use `performTextReplacement` for filling long forms to speed up tests.

- **`performTextClear()`**: Specifically clears the text field.

#### **C. Scrolling (The Major Upgrade)**

In Espresso, scrolling was painful (you needed `scrollTo` for ScrollView and `RecyclerViewActions` for Lists).
In Compose, **it is unified**.

- **`performScrollTo()`**:
- **Magic:** You call this on the **item** you want to see, not the container.
- **Behavior:** Compose automatically finds the parent scrollable container (LazyColumn or Column with `verticalScroll`) and scrolls until the node is visible.
- _Example:_ `onNodeWithText("Item 50").performScrollTo()`

#### **D. Gestures (`performTouchInput`)**

For complex interactions like swiping a carousel or drawing.

```kotlin
onNodeWithTag("MyCarousel")
    .performTouchInput {
        swipeLeft()
        // or
        swipeRight()
    }

```

### **3. Assertions (`assert...`)**

These functions verify the state of the Semantic Node.

#### **A. Existence & Visibility**

- **`assertExists()`**: The node is present in the Semantics Tree (even if off-screen).
- **`assertIsDisplayed()`**: The node is present **AND** visible to the user (in the viewport).
- _Note:_ If a node is transparent or clipped, this might fail.

- **`assertDoesNotExist()`**: Ensures the node is gone. (Critical for verifying navigation away from a screen).

#### **B. Content Checks**

- **`assertTextEquals("Submit")`**: Checks exact text match.
- **`assertTextContains("Sub")`**: Partial match.
- **`assertContentDescriptionEquals("...")`**: Verifies accessibility descriptions.

#### **C. State Checks**

- **`assertIsEnabled()`** / **`assertIsNotEnabled()`**: Great for checking form validation (e.g., Login button should be disabled if email is empty).
- **`assertIsSelected()`**: For Toggle Buttons or Bottom Navigation items.
- **`assertIsOn()`** / **`assertIsOff()`**: For Switches and Checkboxes.

### **4. Generic Assertions (`assert(Matcher)`)**

Sometimes there isn't a specific helper function (like `assertIsColorRed()`). You can use the generic `assert` with a `SemanticsMatcher`.

```kotlin
// Check if a node has a specific custom property or state
onNodeWithTag("LoginButton")
    .assert(hasClickAction()) // Ensures it is clickable
    .assert(hasAnyChild(withText("Submit"))) // Complex hierarchy check

```

### **5. Common "Gotcha": The Unfocused TextField**

A common failing test scenario:

1. Test: `onNodeWithTag("email").performTextInput("user")`
2. **Crash:** `IllegalStateException: Text input expects focus...`

**The Fix:**
Compose TextFields sometimes need to be clicked (focused) before they accept input.

```kotlin
onNodeWithTag("email")
    .performClick() // Focus it first!
    .performTextInput("user")

```

### **6. Summary for Interviews**

> "In Compose, actions and assertions are method calls on the `SemanticsNodeInteraction`.
> For actions, I use `performClick` for buttons and `performScrollTo` for list items. A massive advantage over Espresso is that `performScrollTo` is agnostic—it works on both `LazyColumn` and `ScrollableColumn` without needing separate APIs.
> For assertions, I rely on `assertIsDisplayed` to verify visibility and `assertIsEnabled` to verify business logic state (like form validation). For complex gestures like swiping, I use the `performTouchInput` block to define precise coordinate movements."

---

**Would you like to proceed to Topic 7.4: "Testing State & Recomposition" (Verifying that the UI actually updates)?**
