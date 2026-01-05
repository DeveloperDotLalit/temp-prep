---
layout: default
title: Deep Links
parent: 4. Navigation in Compose (Type-Safe)
nav_order: 6
---

# Deep Links

Here are your notes for **Topic 4.6**.

---

## **Topic 4.6: Deep Links**

### **1. What It Is**

Deep Links allow users to open your app directly to a specific screen from an external source (like a website, an email, or another app).
Instead of opening the app's "Home" screen, clicking `https://www.myapp.com/profile/user123` takes them directly to the "Profile" screen with ID `user123`.

### **2. Why It Exists (Re-engagement)**

- **Marketing:** You send an email saying "Check out this sale!" Clicking it should open the Sale screen, not the generic homepage.
- **Sharing:** A user shares a link to a specific news article. The recipient should see that specific article.
- **Web-to-App Handoff:** If the user has your app installed, Android intercepts the web URL and opens your native app instead of the Chrome browser.

### **3. How It Works (Two Steps)**

#### **A. Step 1: The Android Manifest (The Gatekeeper)**

You must tell the Android OS that your app _owns_ this URL. You do this by adding an `<intent-filter>` to your Main Activity.

```xml
<activity android:name=".MainActivity" ...>
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https" android:host="www.myapp.com" />
    </intent-filter>
</activity>

```

#### **B. Step 2: The Navigation Graph (The router)**

Inside your `composable` definition, you add the `deepLinks` parameter. You define the URL pattern, and the Navigation component automatically extracts the arguments.

### **4. Example: Handling a Profile Link**

**Goal:** `https://www.myapp.com/profile/123` -> Opens Profile Screen with ID `123`.

```kotlin
// 1. Define the Route Object (Type-Safe)
@Serializable
data class Profile(val id: String)

// 2. Define the Graph
NavHost(navController, startDestination = Home) {

    composable<Profile>(
        // 3. Add Deep Link Configuration
        deepLinks = listOf(
            navDeepLink<Profile>(
                basePath = "https://www.myapp.com/profile"
            )
        )
    ) { backStackEntry ->
        // 4. Retrieve Argument (Same as normal navigation!)
        val profile: Profile = backStackEntry.toRoute()

        ProfileScreen(userId = profile.id)
    }
}

```

**Testing It (ADB Command):**
You don't need a real server to test this. You can force-trigger it via the terminal:
`adb shell am start -W -a android.intent.action.VIEW -d "https://www.myapp.com/profile/999" com.example.myapp`

### **5. Interview Prep**

**Interview Keywords**
`navDeepLink`, Intent Filter, URL Scheme, `basePath`, URI Parsing, Argument Extraction, `adb` testing.

**Interview Speak Paragraph**

> "Implementing Deep Links in Compose is remarkably streamlined. First, I configure the `intent-filter` in the Manifest to claim ownership of the domain (e.g., [https://myapp.com](https://myapp.com)). Then, within the `NavHost`, I use the `deepLinks` parameter on the specific composable. With the new Type-Safe Navigation, I simply provide the `basePath`, and the library automatically matches the URL segments to the fields in my Serializable data class. This means extracting the ID from `myapp.com/user/123` works seamlessly without manual string parsing."

---

**Congratulations!** You have completed **Part 4: Navigation in Compose**.
You can now build a multi-screen app with complex flows and external linking.

Now, we enter the **danger zone**. Doing this wrong causes infinite loops and crashes.
**Are you ready to start Topic 5: Side-Effects & Lifecycles?**

---

## Navigation

â† Previous
