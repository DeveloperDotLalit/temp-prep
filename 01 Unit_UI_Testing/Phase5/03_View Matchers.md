---
layout: default
title: "View Matchers & RecyclerViews"
parent: "Phase 5: UI Testing (Espresso)"
nav_order: 3
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 5.3**.

This topic covers the two most common reasons UI tests crash: "I found too many views" (Ambiguity) and "I can't find the view" (RecyclerViews).

---

# **Chapter 5: UI Testing (Espresso)**

## **Topic 5.3: View Matchers & RecyclerViews**

### **1. The Hierarchy Problem**

Espresso sees your app as a tree of View objects. When you say `onView(withText("Save"))`, it traverses this entire tree.

- **The Happy Path:** It finds exactly one view.
- **The Crash:** It finds two views with the text "Save" (e.g., one in the Toolbar, one in the Dialog). This throws `AmbiguousViewMatcherException`.

### **2. Fixing Ambiguity: The `allOf` Combinator**

To fix ambiguity, you must be more specific. You combine multiple characteristics using the `allOf()` function (from Hamcrest matchers).

**Scenario:** You have two "Save" buttons. One is visible, one is hidden (gone).

- **Bad Code:** `onView(withText("Save")).perform(click())` -> **CRASH**
- **Good Code:**

```kotlin
onView(allOf(
    withText("Save"),
    isDisplayed() // Only pick the one the user can see
)).perform(click())

```

**Scenario:** You have two "Login" buttons. One in the header, one in the footer.

- **Strategy:** Use the Parent to distinguish them.

```kotlin
onView(allOf(
    withText("Login"),
    isDescendantOfA(withId(R.id.footer_layout)) // Only the one inside the footer
)).perform(click())

```

### **3. The RecyclerView Challenge**

RecyclerViews break standard Espresso logic.

- **The Problem:** Standard `scrollTo()` only works for `ScrollView`. It does **not** work for `RecyclerView`.
- **The Invisible View:** If item #50 is off-screen, the `View` object for it _does not exist in memory_ (it hasn't been inflated yet). Therefore, `onView(withText("Item 50"))` will fail with `NoMatchingViewException`.

### **4. The Solution: `espresso-contrib**`

To test RecyclerViews, you need a separate library designed to handle the "Recycling" logic.

**Step 1: Add the Dependency**

```groovy
androidTestImplementation 'androidx.test.espresso:espresso-contrib:3.5.1'

```

**Step 2: Use `RecyclerViewActions**`
Instead of finding the _item_ directly, you find the **RecyclerView** itself, and then tell it to perform an action on its children.

### **5. RecyclerView Actions Cheat Sheet**

#### **Action A: Click Item at Index**

"I want to click the 3rd item in the list."

```kotlin
onView(withId(R.id.my_recycler_view)) // 1. Find the RecyclerView
    .perform(
        RecyclerViewActions.actionOnItemAtPosition<MyViewHolder>(
            2, // Index (0-based)
            click() // Action
        )
    )

```

#### **Action B: Scroll to Specific Data**

"I want to find the row that contains the text 'Settings' and scroll to it."

- _Note:_ This requires that your ViewHolder works with standard matchers.

```kotlin
onView(withId(R.id.my_recycler_view))
    .perform(
        RecyclerViewActions.scrollTo<MyViewHolder>(
            hasDescendant(withText("Settings")) // Matcher for the child inside the row
        )
    )

```

#### **Action C: Click Specific Data**

"Scroll until you find 'Logout', then click it."

```kotlin
onView(withId(R.id.my_recycler_view))
    .perform(
        RecyclerViewActions.actionOnItem<MyViewHolder>(
            hasDescendant(withText("Logout")),
            click()
        )
    )

```

### **6. Checking RecyclerView Data (Assertions)**

How do you check: "Does the list have 5 items?"

- Espresso does not have a built-in matcher for RecyclerView count.
- **Elite Solution:** Write a Custom Matcher.

**File:** `RecyclerViewMatchers.kt`

```kotlin
fun hasItemCount(count: Int): Matcher<View> {
    return object : BoundedMatcher<View, RecyclerView>(RecyclerView::class.java) {
        override fun describeTo(description: Description) {
            description.appendText("RecyclerView with item count: $count")
        }

        override fun matchesSafely(view: RecyclerView): Boolean {
            return view.adapter?.itemCount == count
        }
    }
}

```

**Usage:**

```kotlin
onView(withId(R.id.my_recycler_view))
    .check(matches(hasItemCount(5)))

```

### **7. Summary for Interviews**

> "Handling standard views is straightforward with `withId`, but ambiguity often arises in complex layouts. I resolve `AmbiguousViewMatcherException` by using `allOf()` to combine matchers, filtering by visibility (`isDisplayed`) or parentage (`isDescendantOfA`).
> For dynamic lists, standard matchers fail because off-screen views don't exist. I use the `espresso-contrib` library and `RecyclerViewActions`. This allows me to target the RecyclerView itself and command it to 'scroll to position X' or 'find the row with text Y', ensuring robust tests regardless of screen size."

---

**Would you like to proceed to Topic 5.4: "The Robot Pattern" (The Architecture of UI Testing)?**
