---
layout: default
title: "Testing Runtime Permissions"
parent: "Phase 8: Scenario-Based Solutions"
nav_order: 2
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Phase 8, Scenario 2**.

This is a classic "Gotcha" question. If you say "I use Espresso to click the 'Allow' button," you fail immediately. Espresso cannot see system dialogs.

---

# **Chapter 8: Scenario-Based Solutions**

## **Scenario 2: Testing Runtime Permissions**

### **1. The Interview Question**

> **"Your app has a feature that requires the Camera. How do you write an automated test that verifies the app behaves correctly when the user clicks 'Allow' on the system permission dialog? And what if they click 'Deny'?"**

### **2. The Challenge: The "Out of Process" Problem**

Espresso and Compose testing frameworks run **inside** your application's process.

- **System Dialogs:** The "Allow/Deny" popup belongs to the Android OS (System UI), not your app.
- **The Result:** `onView(withText("Allow"))` will fail with `NoMatchingViewException` because that view is not in your app's hierarchy.

### **3. Solution A: The "Cheat" (GrantPermissionRule)**

If your test is about the _Camera Feature_ (and not about the permission logic itself), you should skip the dialog entirely.

- **Tool:** `GrantPermissionRule`.
- **Behavior:** It automatically grants the permission _before_ the test starts. The dialog never appears.

```kotlin
@get:Rule
val permissionRule = GrantPermissionRule.grant(
    android.Manifest.permission.CAMERA,
    android.Manifest.permission.ACCESS_FINE_LOCATION
)

@Test
fun testCameraFeature() {
    // The dialog won't show up. We can go straight to testing the camera.
    onView(withId(R.id.btn_take_photo)).perform(click())
}

```

### **4. Solution B: The "Real" Test (UI Automator)**

If you specifically need to test the **Permission Flow** (e.g., "If user denies, show a rationale Snackbar"), you need **UI Automator**.

- **What is it?** A testing framework that can interact with the _entire device screen_, including the Notification Shade, Settings, and System Dialogs.
- **Dependency:** `androidTestImplementation("androidx.test.uiautomator:uiautomator:2.3.0")`

### **5. The Code Solution**

You combine Espresso (for your app) and UI Automator (for the dialog).

```kotlin
@Test
fun testPermissionDenied_showsRationale() {
    val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())

    // 1. Trigger the Permission Dialog (Espresso)
    onView(withId(R.id.btn_request_permission)).perform(click())

    // 2. Wait for the System Dialog to appear (UI Automator)
    // We look for a button that contains the text "Deny" or "Don't allow"
    // Note: Text varies by Android Version ("Deny", "Don't allow", etc.)
    val denyButton = device.findObject(
        UiSelector().textContains("Don't allow") // Or "Deny"
    )

    // 3. Click the System Button
    if (denyButton.exists()) {
        denyButton.click()
    }

    // 4. Verify App Handling (Espresso)
    // The app should now show a Snackbar explaining why it needs the permission
    onView(withText("We need camera access to scan QR codes"))
        .check(matches(isDisplayed()))
}

```

### **6. Handling Different Android Versions (The Regex Trick)**

Android 10, 11, 12, and 14 all have slightly different text for their buttons ("While using the app", "Only this time", "Allow").

- **Elite Strategy:** Use `Pattern` (Regex) to find the button.

```kotlin
val allowPattern = Pattern.compile("(?i)(Allow|While using the app|Only this time)")
val allowButton = device.findObject(UiSelector().textMatches(allowPattern.pattern()))
allowButton.click()

```

### **7. Summary for Interviews**

> "Testing permissions requires a hybrid approach because Espresso cannot interact with system-level dialogs.
> If I am testing the feature logic (like the Camera itself), I use `GrantPermissionRule` to auto-grant permissions and avoid the dialog entirely for stability.
> However, to test the 'Happy/Sad Paths' of the permission flow itself, I use **UI Automator**. I retrieve the `UiDevice` instance, trigger the dialog via Espresso, and then use `UiDevice.findObject()` with a text selector to locate and click the system's 'Allow' or 'Deny' buttons. This ensures the app correctly handles the user's decision, such as showing a rationale Snackbar upon denial."

---

**Would you like to proceed to Scenario 3: "Testing Race Conditions" (Network vs. User Speed)?**
