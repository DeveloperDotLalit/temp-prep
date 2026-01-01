---
layout: default
title: **Chapter 5: UI Testing (Espresso)**
parent: Unit & UI Testing: Phase5
nav_order: 1
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Phase 5, Topic 5.1**.

We are now leaving the **JVM**. We are stepping into the world of pixels, views, and actual user interactions.

---

# **Chapter 5: UI Testing (Espresso)**

## **Topic 5.1: Espresso Basics**

### **1. What is Espresso?**

Espresso is Google's native UI testing framework for Android. It is part of the AndroidX Test Library.

- **Goal:** To simulate user interactions (clicks, typing, scrolling) and assert that the UI behaves correctly.
- **The Engine:** It runs inside the same process as your app, allowing it to inspect the view hierarchy in real-time.
- **Synchronization:** This is its superpower. Espresso automatically waits for the UI thread to be idle before performing the next action. You (mostly) don't need `Thread.sleep()`.

### **2. The Golden Formula**

Every single line of Espresso code follows the exact same sentence structure. Memorize this pattern.

1. **Find it:** "Find the view with ID `R.id.login_button`..."
2. **Do something:** "...click on it..."
3. **Check it:** "...and ensure the next screen is displayed."

### **3. The Three Pillars (Components)**

#### **A. ViewMatchers (Finding the View)**

Used inside `onView(...)`.

- `withId(R.id.my_button)`: The most common and robust way.
- `withText("Submit")`: Finds a view displaying this specific text.
- `withContentDescription("Settings Icon")`: Useful for ImageViews without text.
- `isDisplayed()`: Often used to filter results (find a view that is visible).

#### **B. ViewActions (Interacting)**

Used inside `.perform(...)`.

- `click()`: Taps the view.
- `typeText("Hello")`: Types into an EditText.
- `replaceText("Hello")`: Pastes text (faster than typing).
- `closeSoftKeyboard()`: Critical! Often the keyboard covers a button, causing the test to fail.
- `scrollTo()`: Scrolls a ScrollView until the view is visible.

#### **C. ViewAssertions (Verifying)**

Used inside `.check(...)`.

- `matches(isDisplayed())`: Checks visibility.
- `matches(withText("Success"))`: Checks content.
- `doesNotExist()`: Checks that a view is _not_ present in the hierarchy.

### **4. Prerequisite: Device Setup**

Before running any Espresso test, you **MUST** disable animations on your test device/emulator.

- **Why?** If a view is fading in, Espresso might try to click it while it's only 50% opacity, causing a flake.
- **How:** Go to **Developer Options** -> **Drawing** section:

1. Window animation scale -> **Off**
2. Transition animation scale -> **Off**
3. Animator duration scale -> **Off**

### **5. Your First Espresso Test**

Let's test a simple Login Screen.

**The Code (`src/androidTest/java/...`):**

```kotlin
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class LoginActivityTest {

    // 1. Launch the Activity before the test starts
    @get:Rule
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)

    @Test
    fun login_success_displaysHomeScreen() {
        // 1. Type Username
        onView(withId(R.id.et_username))
            .perform(typeText("user123"), closeSoftKeyboard())

        // 2. Type Password
        onView(withId(R.id.et_password))
            .perform(typeText("password"), closeSoftKeyboard())

        // 3. Click Login Button
        onView(withId(R.id.btn_login))
            .perform(click())

        // 4. Assert Home Screen is visible
        // (Assuming the home screen has a unique view with ID tv_welcome)
        onView(withId(R.id.tv_welcome))
            .check(matches(isDisplayed()))

        // 5. Assert the text is correct
        onView(withId(R.id.tv_welcome))
            .check(matches(withText("Welcome, user123")))
    }
}

```

### **6. Common Errors to Watch For**

- **`NoMatchingViewException`**:
- _Cause:_ Espresso looked for `R.id.button` but couldn't find it.
- _Fix:_ Is the view on screen? Do you need to `.perform(scrollTo())` first? Is the ID correct?

- **`AmbiguousViewMatcherException`**:
- _Cause:_ You asked for `withText("Save")`, but there are TWO "Save" buttons on the screen (maybe one in a dialog, one in the background).
- _Fix:_ Be more specific. `onView(allOf(withText("Save"), isDisplayed()))`.

- **`PerformException` (Error performing action)**:
- _Cause:_ You tried to click a view, but it was covered by the keyboard or a loading spinner.
- _Fix:_ Use `closeSoftKeyboard()` or check for overlapping views.

### **7. Summary for Interviews**

> "Espresso is the standard framework for UI testing in Android. It operates on a fluent API structure: `onView` (to find), `perform` (to act), and `check` (to verify). Unlike unit tests, these run on the device (`androidTest`). A critical prerequisite is disabling device animations to prevent flakiness. I use `ActivityScenarioRule` to launch the specific screen I am testing, ensuring each test runs in an isolated activity instance."

---

**Would you like to proceed to the next topic: "The Robot Pattern" (How to clean up the code we just wrote)?**
