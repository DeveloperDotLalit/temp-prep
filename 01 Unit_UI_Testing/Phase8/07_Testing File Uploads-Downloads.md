---
layout: default
title: **Chapter 8: Scenario-Based Solutions**
parent: Phase8
nav_order: 7
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Phase 8, Scenario 7**.

This is a specific case of "Testing System Interactions," but it focuses on data transfer (URIs and Content Resolvers) rather than just UI.

---

# **Chapter 8: Scenario-Based Solutions**

## **Scenario 7: Testing File Uploads (Mocking the Gallery)**

### **1. The Interview Question**

> **"Our app lets users upload a profile picture. When they tap 'Upload', it opens the System Gallery (`Intent.ACTION_GET_CONTENT`). How do you test this without needing a real user to scroll through photos and pick one? Also, how do you guarantee the test works on an Emulator that might have zero photos?"**

### **2. The Problem: The External App**

The "Gallery" or "File Picker" is a separate app.

- **Flakiness:** Different devices have different Gallery apps (Google Photos, Samsung Gallery, Files Go). You cannot write a UI Automator script that works on all of them.
- **Data:** A fresh emulator has no images. The test would fail simply because the gallery is empty.

### **3. The Solution: Intent Stubbing (`intending`)**

Instead of letting the Intent actually launch the Gallery, we **intercept** it.
We tell Espresso: _"When you see an Intent asking for a photo, don't open the Gallery. Instead, immediately pretend the Gallery returned **Success** with this specific fake URI."_

- **Tool:** `IntentsRule` (from `androidx.test.espresso.intent`).

### **4. The Code Solution**

**Step 1: Create a Dummy Image**
The app expects a readable URI. You usually create a small dummy file in the test context's cache during setup.

```kotlin
private fun createFakeImageUri(): Uri {
    // Create a temporary file
    val file = File.createTempFile("test_image", ".png")
    file.writeBytes(byteArrayOf(1, 2, 3)) // Write dummy data

    // Return the Uri (requires FileProvider in real apps, or simple file:// in tests)
    return Uri.fromFile(file)
}

```

**Step 2: The Test**

```kotlin
@get:Rule
val intentsRule = IntentsRule()

@Test
fun testProfileImageUpload_setsImageCorrectly() {
    // 1. Prepare the Result
    val fakeUri = createFakeImageUri()

    // Construct the result data container
    val resultData = Intent().apply { data = fakeUri }
    val result = Instrumentation.ActivityResult(Activity.RESULT_OK, resultData)

    // 2. STUB the Intent
    // "When an intent with ACTION_GET_CONTENT is fired..."
    intending(hasAction(Intent.ACTION_GET_CONTENT)).respondWith(result)

    // 3. Trigger the Action
    // This clicks the button. The app calls startActivityForResult.
    // Espresso intercepts it and immediately returns the 'result' above.
    onView(withId(R.id.btn_upload_image)).perform(click())

    // 4. Verify UI Update
    // The app should display the selected image
    // (Assuming the ImageView has a tag or some visible state change)
    onView(withId(R.id.iv_profile_pic))
        .check(matches(isDisplayed()))

    // Elite: Verify the ViewModel received the correct URI
    // (Requires looking at the ViewModel/State logic)
}

```

### **5. Testing the "User Cancelled" Path**

It is critical to ensure the app doesn't crash if the user backs out of the gallery.

```kotlin
@Test
fun testUpload_userCancels_doesNothing() {
    // Stub a CANCELED result
    val result = Instrumentation.ActivityResult(Activity.RESULT_CANCELED, null)
    intending(hasAction(Intent.ACTION_GET_CONTENT)).respondWith(result)

    onView(withId(R.id.btn_upload_image)).perform(click())

    // Assert the placeholder image is still shown (not replaced)
    onView(withId(R.id.iv_profile_pic))
        .check(matches(hasContentDescription("Placeholder")))
}

```

### **6. Summary for Interviews**

> "I never test the actual System Gallery because it is an external app that varies by device and is prone to flakiness. Instead, I use **Intent Stubbing** with Espresso's `IntentsRule`.
> I define a matcher for the `ACTION_GET_CONTENT` intent and use `intending(...).respondWith(...)` to return a pre-fabricated `Activity.RESULT_OK` containing a URI to a temporary test file I generate at runtime. This simulates a successful user selection instantly and deterministically. It allows me to verify that my app correctly handles the URI and updates the UI, without worrying about whether the emulator actually has photos or how the specific Gallery app UI looks."

---

**Congratulations! You have completed Phase 8 (Scenarios).**
You now have the "Answer Key" for the toughest technical interview questions.

**We are moving to the Final Phase: Phase 9 (CI/CD & Azure DevOps).**
This is the final piece: Automating everything we just learned.

**Next Topic:** Phase 9.1: **The CI Pipeline Lifecycle** (Concept & Flow).
**Shall we proceed?**
