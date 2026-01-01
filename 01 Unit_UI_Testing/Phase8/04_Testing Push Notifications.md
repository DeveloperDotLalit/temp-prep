---
layout: default
title: **Chapter 8: Scenario-Based Solutions**
parent: Phase8
nav_order: 4
---

Here are your in-depth study notes for **Phase 8, Scenario 4**.

This scenario tests your ability to leave the "sandbox" of your application and interact with the Android OS itself.

---

# **Chapter 8: Scenario-Based Solutions**

## **Scenario 4: Testing Push Notifications**

### **1. The Interview Question**

> **"We send a push notification when a user receives a message. How do you write an automated test to verify that the notification actually appears in the system tray, has the correct title, and opens the correct Chat Screen when clicked?"**

### **2. The Limitation: The "Sandbox"**

Espresso and Compose tests are strictly bound to your app's window.

- **The Notification Shade:** This is a System UI component (`com.android.systemui`). Your test code cannot "see" it using standard matchers.
- **The Fix:** You must use **UI Automator** to interact with the device's status bar.

### **3. The Strategy**

1. **Trigger:** Simulate the notification (either by mocking the `NotificationManager` or sending a local broadcast).
2. **Open:** Use `device.openNotification()` to pull down the shade.
3. **Find:** Use `device.findObject()` to look for the notification title.
4. **Click:** Tap the notification.
5. **Verify:** Assert that the app is now in the foreground and on the correct screen.

### **4. The Code Solution**

**Prerequisite:**
You need a helper method to send a notification locally for the test (unless you have a real backend integrated).

```kotlin
@Test
fun testNotification_appearsAndOpensChat() {
    val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())

    // 1. Trigger Notification (Simulated)
    // Assume we have a helper in our app that generates a notification
    // In a real test, you might inject a fake 'MessageReceivedEvent'
    val context = ApplicationProvider.getApplicationContext<Context>()
    NotificationHelper(context).showNotification(
        id = 1,
        title = "New Message",
        body = "Hello World"
    )

    // 2. Open Notification Shade
    device.openNotification()

    // Wait a moment for animation
    device.wait(Until.hasObject(By.text("New Message")), 3000)

    // 3. Find the Notification object
    // We search for a UI element containing the title text
    val notification = device.findObject(UiSelector().text("New Message"))

    // ASSERT: It exists
    assertThat(notification.exists()).isTrue()

    // 4. Click it
    // This should close the shade and launch the app
    notification.clickAndWaitForNewWindow()

    // 5. Verify App Navigation (Espresso)
    // We are back in the app context now
    onView(withText("Chat Screen"))
        .check(matches(isDisplayed()))

    onView(withText("Hello World")) // The message body inside the app
        .check(matches(isDisplayed()))
}

```

### **5. Handling "Clear All" (Cleanup)**

If you don't clear notifications, your next test might find an old notification and pass falsely.

- **Elite Tip:** Always clear the shade in `@After`.

```kotlin
@After
fun teardown() {
    val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
    // There is no direct API to "Clear All", but we can use an Intent
    // OR just open shade and click the "Clear all" button if visible
    // Safest way: Cancel all via code
    val context = ApplicationProvider.getApplicationContext<Context>()
    NotificationManagerCompat.from(context).cancelAll()
}

```

### **6. Advanced: Testing Deep Links via Notification**

Often, a notification carries data (e.g., `chatId=123`).

- **Goal:** Ensure clicking the notification opens `ChatActivity` with `ID 123`.
- **Verification:** Use the `Intents` rule (from `androidx.test.espresso.intent`).

```kotlin
@get:Rule
val intentsRule = IntentsRule()

@Test
fun notification_hasCorrectIntentData() {
    // ... (Trigger and Click Notification as above) ...

    // ASSERT: Check the Intent that launched the activity
    intended(allOf(
        hasComponent(ChatActivity::class.java.name),
        hasExtra("chat_id", 123)
    ))
}

```

### **7. Summary for Interviews**

> "Testing notifications requires crossing the process boundary into the System UI. I use **UI Automator** for this.
> My test flow is: trigger the notification (usually via a local helper or mocked service), use `uiDevice.openNotification()` to pull down the shade, and then search for the `UiObject` matching the notification title.
> Once verified, I perform a click on that object and use `clickAndWaitForNewWindow()` to ensure the app handles the intent correctly. I then use Espresso or the `Intents` library to verify that the app navigated to the correct Deep Link destination with the expected extras."

---

**Would you like to proceed to Scenario 5: "Testing Deep Links" (Simulating external URLs)?**
