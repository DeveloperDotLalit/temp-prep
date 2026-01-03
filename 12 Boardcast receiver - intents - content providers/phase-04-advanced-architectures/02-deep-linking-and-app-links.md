---
layout: default
title: "Deep Linking and App Links"
parent: "Phase 4: Advanced Architectures and Interview Scenarios"
nav_order: 2
---

# Deep Linking and App Links

## **Topic 2: Deep Linking & App Links**

### **What It Is**

Deep Linking is a way to use a **URL** (like `https://www.bajajfinserv.com/loans`) to open a specific screen inside your app instead of just opening your website in a browser.

In Android, there are two main types:

1. **Deep Links (Traditional):** Uses a custom scheme (e.g., `myapp://profile`) or a standard URL. It usually triggers an "App Chooser" dialog if multiple apps can handle it.
2. **App Links (Verified):** These are "Digital Asset Links." When a user clicks a verified link, the Android System knows for a fact that _only_ your app is allowed to open it. It bypasses the "App Chooser" and opens your app directly.

---

### **Why It Exists**

**The "Seamless Journey" Problem:**
Imagine a user receives an email about a "Personal Loan Offer."

- **The Problem:** If they click the link and it opens in a mobile browser, they might have to log in again, leading to a high drop-off rate.
- **The Solution:** Deep Linking. The link triggers an **Intent**, the OS finds your app, and takes the user directly to the "Loan Details" screen inside the app where they are already logged in. This significantly increases conversion rates.

---

### **How It Works**

It all comes back to **Intent Filters**.

1. **The Trigger:** A user clicks a link in another app (Chrome, Gmail, WhatsApp).
2. **The Matching:** The Android System looks for an Activity that has an Intent Filter with:

- **Action:** `ACTION_VIEW`
- **Category:** `BROWSABLE` and `DEFAULT`
- **Data:** Matches the `scheme` and `host` of the URL.

3. **App Links Verification:** For **App Links**, the Android System checks a special file on your website (located at `/.well-known/assetlinks.json`). If the website "vouches" for the app, the link is verified.

---

### **Example (Code-based)**

**1. Define the Intent Filter in `AndroidManifest.xml`:**

```xml
<activity android:name=".ProductDetailActivity" android:exported="true">
    <intent-filter android:autoVerify="true"> <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />

        <data android:scheme="https" android:host="www.myapp.com" android:pathPrefix="/products" />
    </intent-filter>
</activity>

```

**2. Extracting Data in Kotlin:**

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    val data: Uri? = intent.data
    if (data != null) {
        // Get the ID from the path (e.g., "123")
        val productId = data.lastPathSegment
        fetchProductDetails(productId)
    }
}

```

---

### **Interview Keywords**

- **Digital Asset Links**: The JSON file used to verify App Links.
- **autoVerify="true"**: The Manifest attribute that tells the OS to check the website for ownership.
- **Ambiguous Intent**: When multiple apps can handle a Deep Link (showing the App Chooser).
- **Scheme/Host/Path**: The three components of the `<data>` tag.

---

### **Interview Speak Paragraph**

> "Deep Linking allows us to map web URLs to specific app components using Intent Filters with the `ACTION_VIEW` and `BROWSABLE` categories. To provide a more seamless user experience, I prefer **Android App Links** over standard Deep Links. By setting `android:autoVerify="true"` and hosting a **Digital Asset Links** JSON file on our domain, we allow the OS to verify that our app is the rightful owner of that URL. This eliminates the 'App Chooser' dialog and drives users directly from a browser or social media link into a specific Activity, which is crucial for retention and conversion in high-traffic apps."

---

### **Common Interview Question/Angle**

- **"What is the difference between Deep Links and App Links?"**
- _Answer:_ Deep Links are unverified and can show an "Open with..." dialog if multiple apps match. **App Links** are verified against a website's domain, ensuring the link opens directly in the specific app without a prompt.

- **"What happens if verification for an App Link fails?"**
- _Answer:_ The system treats it as a standard Deep Link. It will show the "App Chooser" to the user if other apps (like a browser) can also handle the URL.

- **"How do you handle parameters in a Deep Link?"**
- _Answer:_ You can extract them from the `intent.data` object. You can use `data.getQueryParameter("key")` for query params (like `?id=123`) or `data.pathSegments` for path-based parameters.

---

**Next: Battery & Performance Impact – Why the system limits Broadcasts and how to handle background restrictions in modern Android. Ready for the "Optimization" talk?**

Would you like to continue to **Battery & Performance**, or would you like to see the structure of a `Digital Asset Links` JSON file first?

---

[â¬… Back to Phase Overview](../)
