---
layout: default
title: "Intent Filters"
parent: "Phase 1: Intents - The Glue of Android"
nav_order: 3
---

# Intent Filters

## **Topic 3: Intent Filters – The App’s Resume**

### **What It Is**

If an **Intent** is a "request" for an action, an **Intent Filter** is an "advertisement" that says, _"I am capable of performing this action."_ Think of it like a **job description** or a **label** you stick on your Activity in the `AndroidManifest.xml`. It tells the Android System: "Hey, if anyone asks to 'Send an Email' or 'View a Website', I know how to do that!"

### **Why It Exists**

In the Android ecosystem, apps need a way to talk to each other without knowing each other's code.

- **The Problem:** If you build a photo editing app, how does the Gallery app know it can send photos to you?
- **The Solution:** Your app declares an **Intent Filter**. The Android System keeps a master list of all these filters. When an Implicit Intent is fired, the System scans this list to find the perfect match.

---

### **How It Works**

An Intent Filter usually sits inside your `AndroidManifest.xml` and is defined by three main components:

1. **Action**: The **"What"**. (e.g., `ACTION_SEND`, `ACTION_VIEW`).
2. **Data**: The **"On What"**. What kind of data can it handle? (e.g., a URI starting with `https://` or a MIME type like `image/png`).
3. **Category**: The **"In what context"**. Most common is `DEFAULT`, but it could be `BROWSABLE` (can be opened from a web browser).

---

### **Example (Code-based)**

Imagine you are building a **PDF Viewer** app. You want the system to suggest your app whenever a user tries to open a PDF file.

**In your `AndroidManifest.xml`:**

```xml
<activity android:name=".PdfViewerActivity"
    android:exported="true"> <intent-filter>
        <action android:name="android.intent.action.VIEW" />

        <category android:name="android.intent.category.DEFAULT" />

        <data android:mimeType="application/pdf" />
    </intent-filter>

</activity>

```

**What happens now?** When another app (like WhatsApp) tries to open a PDF using an Implicit Intent, the Android System sees your filter and includes your app in the "Open with..." list.

---

### **Interview Keywords**

- **Manifest Declaration**: Where Intent Filters are almost always defined.
- **Implicit Intent Resolution**: The process the OS uses to match an Intent to a Filter.
- **MIME Type**: Used in the `<data>` tag to specify file types (like `image/*` or `text/plain`).
- **Exported Attribute**: A security setting (`android:exported`) that determines if other apps can trigger your activity.

---

### **Interview Speak Paragraph**

> "Intent Filters are declarations in the Android Manifest that specify the types of Implicit Intents a component is willing to receive. While an Intent is a 'call' for an action, the Filter is the 'response' saying it can handle that action. For a match to occur, the Intent must pass three tests: the Action, the Data (including MIME types), and the Category. If an Activity doesn't have an Intent Filter, it can only be started using an Explicit Intent."

---

### **Common Interview Question/Angle**

- **"What is the importance of `android.intent.category.DEFAULT`?"**
- _Answer:_ Most Implicit Intents (sent via `startActivity()`) automatically add the `DEFAULT` category. If your Activity's Intent Filter doesn't include this category, it will **not** receive any Implicit Intents from the system.

- **"Why do we need `android:exported="true"`?"**
- _Answer:_ Starting with Android 12, if your component has an Intent Filter, you **must** explicitly set `android:exported`. If it's `false`, other apps cannot see or trigger that component, even if the Intent Filter matches.

---

**Next: Data Passing (Bundles & Parcelable) – Moving data between these components. Should we proceed?**

---

[â¬… Back to Phase Overview](../)
