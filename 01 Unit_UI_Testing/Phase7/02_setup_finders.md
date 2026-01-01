---
layout: default
title: **Chapter 7: Jetpack Compose Testing**
parent: Phase7
nav_order: 2
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Topic 7.2**.

Now that you understand the "Semantics Tree," we need the tools to navigate it. This is where we learn how to "find" things without IDs.

---

# **Chapter 7: Jetpack Compose Testing**

## **Topic 7.2: Setup & Finders**

### **1. The Two Rules (The Entry Point)**

Just like `ActivityScenarioRule` in Espresso, Compose needs a "Rule" to set up the environment. You have two choices.

#### **A. `createComposeRule()` (The Pure Unit Test)**

- **Use Case:** Testing a single Composable function (e.g., just the `LoginButton()` composable) in complete isolation.
- **Environment:** Does NOT launch an Activity. It creates a blank canvas.
- **Speed:** Faster.

```kotlin
@get:Rule
val composeTestRule = createComposeRule()

@Test
fun testButton() {
    composeTestRule.setContent {
        MyButton() // Launch just this component
    }
    // Test logic...
}

```

#### **B. `createAndroidComposeRule<MainActivity>()` (The Integration Test)**

- **Use Case:** Testing a full screen or navigation where you need access to the Android **Context**, **Resources** (Strings/Colors), or the Activity itself.
- **Environment:** Launches the actual Activity.
- **Benefit:** You can access `rule.activity.getString(R.string.login)` to ensure your test matches your localization.

### **2. The "Big Three" Finders**

In Espresso, you used `onView(withId(...))`. In Compose, we use `onNode(...)`. There are three main ways to find a node.

#### **Finder 1: `onNodeWithText("...")**`

The most common finder for buttons and static labels.

- **Pros:** Easy to read. Tests what the user actually sees.
- **Cons:** Brittle. If you change "Submit" to "Confirm", the test breaks.
- **Elite Tip:** Use resource strings instead of hardcoded strings.
  `onNodeWithText(activity.getString(R.string.submit))`

#### **Finder 2: `onNodeWithContentDescription("...")**`

The standard for **Icons** and **Images**.

- **Constraint:** You _must_ provide `contentDescription` in your production code (which you should do anyway for Accessibility).
- **Example:** Finding the "Back" arrow or a "Settings" gear icon.

#### **Finder 3: `onNodeWithTag("...")` (The "New ID")**

This is the closest equivalent to `R.id`.

- **The Problem:** Composables don't have IDs.
- **The Fix:** You add a special modifier to the Composable in production code.

**Production Code:**

```kotlin
Button(
    onClick = {},
    modifier = Modifier.testTag("login_submit_btn") // Define the tag
) { Text("Login") }

```

**Test Code:**

```kotlin
composeTestRule.onNodeWithTag("login_submit_btn").performClick()

```

- _Trade-off:_ You are polluting production code with test tags. This is generally accepted in the Compose community because it is often the _only_ way to find complex nodes reliably.

### **3. `onNode` vs `onAllNodes**`

- **`onNode(...)`**: Expects to find **exactly one** match. If it finds 0 or 2+, the test crashes immediately.
- **`onAllNodes(...)`**: Returns a collection of nodes. Useful for lists.
- _Usage:_ `onAllNodesWithText("Delete").onFirst().performClick()`

### **4. Advanced: The "Unmerged" Tree**

Recall from Topic 7.1 that Compose "Merges" nodes (Button + Text = One Button Node).
Sometimes, you specifically need to verify the _Text_ node inside the Button (e.g., checking the font color of the text, not the button).

You must explicitly ask Compose to **un-merge** the tree.

**The Scenario:**
You have a Button. The Semantics Node is "Button". You want to check if the text inside is "Login".

**Standard (Merged) - Fails:**
`onNodeWithText("Login")` might point to the Button, but if you try to check text properties specific to the text child, it might be ambiguous.

**Unmerged - Succeeds:**

```kotlin
// Look inside the children of the merged node
composeTestRule
    .onNodeWithText("Login", useUnmergedTree = true)
    .assertIsDisplayed()

```

### **5. Summary for Interviews**

> "To interact with the UI, I use `createAndroidComposeRule` which gives me access to the Activity context for resolving string resources.
> For finding elements, I prefer `onNodeWithText` for text-heavy components as it mimics user behavior. For icons, I use `onNodeWithContentDescription`. However, for complex or dynamic layouts where text might change, I use `Modifier.testTag` in the production code and find it using `onNodeWithTag`. This acts as a stable identifier similar to `R.id` in the old View system."

---

**Would you like to proceed to Topic 7.3: "Actions & Assertions" (Clicking, Scrolling, and Checking)?**
