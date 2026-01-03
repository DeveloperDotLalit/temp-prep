---
layout: default
title: "Testing Deep Links"
parent: "Phase 8: Scenario-Based Solutions"
nav_order: 5
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Phase 8, Scenario 5**.

Deep links are the bridges between the web and your app. Testing them ensures that marketing campaigns and email links actually work.

---

# **Chapter 8: Scenario-Based Solutions**

## **Scenario 5: Testing Deep Links**

### **1. The Interview Question**

> **"Our marketing team sends emails with links like `https://www.shop.com/product/123`. When the user clicks this on their phone, it should open the app directly to the Product Detail screen for ID 123. How do you automate a test to prove this works and that the ID is parsed correctly?"**

### **2. The Concept: Intent Filters**

A deep link is essentially an **Implicit Intent**. The Android OS looks at the URL, checks the `AndroidManifest.xml` of all installed apps, and finds one that says "I can handle `shop.com/product`".

To test this, we don't need a real email client. We just need to construct an **Intent** that mimics exactly what the Android OS would generate when that link is clicked.

### **3. The Tool: `ActivityScenario.launch(Intent)**`

We use the standard AndroidX Test library, but instead of launching the activity normally, we launch it with a specific **Data URI**.

### **4. The Code Solution**

**The Setup (Manifest):**
Assume your `MainActivity` handles the navigation logic.

```xml
<activity android:name=".MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https" android:host="www.shop.com" android:pathPrefix="/product" />
    </intent-filter>
</activity>

```

**The Test:**

```kotlin
@Test
fun testDeepLink_opensProductDetails() {
    // 1. Construct the Intent
    // This mimics a user clicking the link in Chrome/Gmail
    val deepLinkIntent = Intent(
        Intent.ACTION_VIEW,
        Uri.parse("https://www.shop.com/product/123")
    ).apply {
        // Essential: Set the package to ensure it opens OUR app, not the browser chooser
        setPackage("com.example.myapp")
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    }

    // 2. Launch Activity with this Intent
    // ActivityScenario is powerful: it handles the lifecycle setup
    ActivityScenario.launch<MainActivity>(deepLinkIntent).use { scenario ->

        // 3. Verify UI (Espresso/Compose)
        // The app should interpret "123" and show the correct screen

        // Wait for potential network loading
        waitForIdle()

        onNodeWithText("Product ID: 123")
            .assertIsDisplayed()

        onNodeWithText("Add to Cart")
            .assertIsDisplayed()
    }
}

```

### **5. Validating the Argument Parsing**

Sometimes the UI isn't enough. You want to know if the `ViewModel` received the correct ID.
You can inspect the Activity directly using `onActivity`.

```kotlin
ActivityScenario.launch<MainActivity>(deepLinkIntent).use { scenario ->
    scenario.onActivity { activity ->
        // Check the Intent that started the activity
        val data = activity.intent.data
        assertThat(data?.lastPathSegment).isEqualTo("123")

        // Or check the NavController state if using Navigation Component
        val navController = activity.findNavController(R.id.nav_host_fragment)
        assertThat(navController.currentDestination?.label).isEqualTo("ProductDetails")
    }
}

```

### **6. Testing "Broken" Links**

It is equally important to test invalid links to ensure the app doesn't crash.

- **Test Case:** `https://www.shop.com/product/` (Missing ID) or `.../product/abc` (Non-numeric).
- **Assertion:** The app should show a "Product Not Found" error or redirect to Home, but **not crash**.

### **7. Summary for Interviews**

> "To test deep links, I simulate the Android OS behavior by constructing an `Intent` with `ACTION_VIEW` and the specific Data URI (e.g., `https://shop.com/product/123`).
> I pass this intent to `ActivityScenario.launch(intent)`. This spins up the entry point Activity exactly as if the user had clicked the link. I then verify two things: first, that the correct screen is rendered using Espresso/Compose matchers; and second, that the `Intent` data was parsed correctly by checking the `ViewModel` state or the `NavController`'s current destination. I also include negative test cases for malformed URLs to ensure the app degrades gracefully without crashing."

---

**Would you like to proceed to Scenario 6: "Testing WebViews" (The bridge between Native and Web)?**
