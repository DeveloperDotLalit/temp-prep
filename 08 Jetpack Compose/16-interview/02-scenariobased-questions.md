---
layout: default
title: Scenario-Based Questions
parent: 16. Interview Prep
nav_order: 2
---

# Scenario-Based Questions

Here are your notes for **Topic 16.2: Scenario-Based Q&A**.

---

## **Topic 16.2: Scenario-Based Q&A**

These questions test your problem-solving skills. The interviewer presents a situation, and you must design a solution using your Compose knowledge.

### **Scenario 1: "How do you debug excessive recomposition?"**

**The Situation:**
"You have a list of items. When you scroll or click a 'Like' button on one item, the entire list lags, and the Layout Inspector shows that _every_ visible row is recomposing, not just the one you touched."

**The Diagnosis Steps:**

1. **Layout Inspector:** Verify the "Recomposition Count" is actually increasing for unrelated rows.
2. **Stability Check:** Check the parameters passed to the Row composable. Are you passing a `List<T>`? A class with `var`? A lambda that captures unstable state?
3. **Compiler Metrics:** Run the report. Is the Row function marked `restartable` but NOT `skippable`?

**The Solution:**

- **Fix Instability:** Wrap the `List` in an `@Immutable` data class or use `ImmutableList`.
- **Fix Lambdas:** If you pass `onClick = { viewModel.onItemClick(item) }`, you are creating a _new lambda object_ on every frame.
- _Fix:_ Pass a method reference `onClick = viewModel::onItemClick` or wrap the lambda in `remember`.

- **Derived State:** Are you reading `scrollState.value` in the main body? Move it to `derivedStateOf` or a `drawBehind` block.

**Interview Answer:**

> "First, I'd confirm the issue using the Layout Inspector to see which composables are recomposing. If unrelated rows are updating, it's usually a Stability issue. I'd check if the parameters passed to the Row are marked 'unstable' by the compiler—commonly caused by standard `List` interfaces or unstable lambdas. To fix it, I would wrap the data in an `@Immutable` class or use `PersistentList`. If the issue persists, I'd check if I'm accidentally reading a rapidly changing state (like scroll offset) in the composition phase instead of the draw phase, and defer that read using a lambda modifier."

---

### **Scenario 2: "Design a Chat Screen with bottom-up stacking"**

**The Situation:**
"Design a message thread view like WhatsApp or Slack. It needs to start at the bottom. When the keyboard opens, the list should push up. New messages should appear at the bottom."

**Key Challenges:**

1. **Stacking:** Standard lists start at the top. Chat starts at the bottom.
2. **Keyboard:** The input field must ride on top of the keyboard.
3. **Performance:** Loading 10,000 messages.

**The Solution:**

1. **`LazyColumn(reverseLayout = true)`:** This flips the list. Index 0 is at the bottom.

- _Advantage:_ When you add a new message to index 0, it appears instantly at the bottom without scrolling.

2. **`imePadding()`:** Apply this modifier to the root container (or the input field). It automatically pushes the UI up by the exact height of the software keyboard.
3. **Layout Structure:**

```kotlin
Scaffold(
    bottomBar = { MessageInput(Modifier.imePadding()) } // Pushes up with keyboard
) { padding ->
    LazyColumn(
        modifier = Modifier.padding(padding),
        reverseLayout = true // Starts from bottom
    ) {
        items(messages) { msg -> ChatBubble(msg) }
    }
}

```

**Interview Answer:**

> "I would implement this using a `LazyColumn` with `reverseLayout = true`. This anchors the content to the bottom, so adding a new message at index 0 naturally renders it at the bottom without manual scrolling logic. For the keyboard interaction, I would place the text input field in the `bottomBar` slot of a `Scaffold` or a `Column` and apply the `Modifier.imePadding()` or `WindowInsets.ime`. This ensures the input field and the list resize and translate smoothly in sync with the keyboard animation, providing a native feel."

---

### **Scenario 3: "Migrate a legacy Fragment to Compose"**

**The Situation:**
"We have a complex 'UserProfileFragment' with a CoordinatorLayout, Collapsing Toolbar, and a ViewPager. We want to rewrite the 'Posts' tab in Compose, but keep the rest in XML for now."

**The Strategy (Interoperability):**

1. **Identify the Seam:** The "Posts" tab content (likely a RecyclerView inside the ViewPager) is the target.
2. **The Bridge:** Replace the RecyclerView XML tag with a `ComposeView`.
3. **The Lifecycle:** Since this is a Fragment, we _must_ set the correct disposal strategy.
4. **The Theme:** Wrap the Compose content in `MdcTheme` (if using Material Components XML theme) or your own `AppTheme` to ensure colors match the existing app.

**The Solution:**

```kotlin
// In the Fragment's onCreateView or onViewCreated
val composeView = view.findViewById<ComposeView>(R.id.compose_view)
composeView.apply {
    // Crucial for Fragments!
    setViewCompositionStrategy(ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed)

    setContent {
        // Bridge existing XML theme colors to Compose
        MdcTheme {
            PostList(viewModel.posts)
        }
    }
}

```

**Interview Answer:**

> "I would adopt a bottom-up migration strategy. I'd replace the specific `RecyclerView` in the XML layout with a `androidx.compose.ui.platform.ComposeView`. In the Fragment's `onViewCreated`, I'd set the `ViewCompositionStrategy` to `DisposeOnViewTreeLifecycleDestroyed` to prevent memory leaks. Then, I'd call `setContent` and wrap the Composable in an adapter theme (like `MdcTheme`) to ensure it inherits the existing XML styles and colors seamlessly. This allows us to ship the new Compose list without rewriting the complex CoordinatorLayout header immediately."

---

**Next Step:**
You have the theory, the code, and the problem-solving patterns. Would you like me to create a **coding challenge** based on one of these scenarios to test your skills?

---

## Navigation

â† Previous
Next â†’
