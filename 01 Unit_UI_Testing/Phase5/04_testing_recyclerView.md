---
layout: default
title: "Testing RecyclerViews"
parent: "Phase 5: UI Testing (Espresso)"
nav_order: 4
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 5.4**.

While we touched on this briefly in View Matchers, RecyclerViews are complex enough to deserve their own dedicated deep-dive. This is often where junior engineers get stuck.

---

# **Chapter 5: UI Testing (Espresso)**

## **Topic 5.4: Testing RecyclerViews**

### **1. The Fundamental Problem: "It doesn't exist yet"**

If you have a list of 100 items, Android only draws the 5 or 6 that fit on the screen. Item #50 is just data in memory; it has no `View` object.

- **Standard Espresso:** `onView(withText("Item 50"))` fails because it scans the _current_ view hierarchy.
- **The Fix:** We cannot search for the view. We must find the **Container** (the RecyclerView) and command it to create the view for us.

### **2. The Tool: `espresso-contrib**`

This functionality is not in the core library. You must ensure you have this specific dependency in `app/build.gradle`:

```kotlin
androidTestImplementation("androidx.test.espresso:espresso-contrib:3.5.1")

```

### **3. The Command Center: `RecyclerViewActions**`

This class contains static methods that generate special `ViewAction`s designed for lists.

#### **Scenario A: Scrolling to an item (Visibility Check)**

You just want to verify that "Item 50" exists. You don't need to click it.

```kotlin
// 1. Find the RecyclerView (The container)
onView(withId(R.id.recycler_view))
    .perform(
        // 2. Command it to scroll until it finds a holder matching this data
        RecyclerViewActions.scrollTo<MyViewHolder>(
            hasDescendant(withText("Item 50"))
        )
    )

// 3. NOW checking for it works, because it has been scrolled into view
onView(withText("Item 50")).check(matches(isDisplayed()))

```

#### **Scenario B: Clicking an item by Position**

You know exactly which index you want (e.g., "Click the first item").

```kotlin
onView(withId(R.id.recycler_view))
    .perform(
        RecyclerViewActions.actionOnItemAtPosition<MyViewHolder>(
            0,       // Position 0 (First item)
            click()  // The standard ViewAction
        )
    )

```

#### **Scenario C: Clicking an item by Content**

You don't know the position (it might be row 5 or row 50), but you know the text.

```kotlin
onView(withId(R.id.recycler_view))
    .perform(
        RecyclerViewActions.actionOnItem<MyViewHolder>(
            hasDescendant(withText("Settings")), // The Matcher
            click()                              // The Action
        )
    )

```

### **4. Advanced: Clicking a _Child_ inside the Row**

**The Interview Question:** _"How do you click the 'Delete' button inside a specific row, rather than clicking the row itself?"_

Standard `click()` clicks the center of the entire row. To click a specific button inside that row (e.g., `R.id.btn_delete`), you need a **Custom ViewAction**.

**Step 1: Create the Custom Action helper**

```kotlin
object MyViewActions {
    fun clickChildViewWithId(id: Int): ViewAction {
        return object : ViewAction {
            override fun getConstraints(): Matcher<View>? = null // Logic omitted for brevity
            override fun getDescription(): String = "Click on a child view with specified id."

            override fun perform(uiController: UiController, view: View) {
                // Find the child inside the row View
                val v = view.findViewById<View>(id)
                v.performClick()
            }
        }
    }
}

```

**Step 2: Use it with RecyclerViewActions**

```kotlin
onView(withId(R.id.recycler_view))
    .perform(
        RecyclerViewActions.actionOnItem<MyViewHolder>(
            hasDescendant(withText("Item to Delete")), // Find the Row
            MyViewActions.clickChildViewWithId(R.id.btn_delete) // Click the specific button
        )
    )

```

### **5. Identifying the ViewHolder (Technical Detail)**

You will notice the `<MyViewHolder>` generic type in the code above.

- **Strict Mode:** Ideally, you pass the actual ViewHolder class of your adapter.
- **Lazy Mode:** If you don't want to expose your ViewHolder to tests, you can often simply use `<RecyclerView.ViewHolder>`.

### **6. Summary for Interviews**

> "Testing RecyclerViews requires the `espresso-contrib` library. We cannot simply look for off-screen views using `onView` because they are not inflated. Instead, we target the RecyclerView itself and use `RecyclerViewActions`.
> I commonly use `scrollTo` to bring an item into the viewport before asserting its state. For interactions, I use `actionOnItem` to find a row by its content (using `hasDescendant`), and then perform a click. If I need to click a specific button _inside_ a row—like a 'Favorite' icon—I inject a custom `ViewAction` that finds the child view by ID and clicks it."

---

**Would you like to proceed to Topic 5.5: "The Robot Pattern" (The Architecture of UI Testing - The Final Elite Topic)?**
