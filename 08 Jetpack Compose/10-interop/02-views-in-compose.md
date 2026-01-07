---
layout: default
title: Views in Compose
parent: 10. Interoperability & Migration
nav_order: 2
---

# Views in Compose

Here are your notes for **Topic 10.2**.

---

## **Topic 10.2: Views in Compose (AndroidView)**

### **1. What It Is**

This is the "Top-Down" migration strategy. You have a full Compose screen, but you need to include a widget that **only** exists in the old View system (e.g., Google Maps, WebView, AdView, or a 3rd party Camera library).
You use the **`AndroidView`** composable to wrap the legacy View.

### **2. Why It Exists (The "Missing Parts" Gap)**

Compose is great, but it doesn't rewrite 15 years of Android history overnight.

- **WebView:** There is no native "Compose WebView". You must wrap the `android.webkit.WebView`.
- **Maps:** While there is now a Compose Maps library, for years `AndroidView` was the only way.
- **CameraX:** The `PreviewView` for camera streams is a standard Android View.

### **3. How It Works (The Factory & Update Pattern)**

`AndroidView` takes three main arguments:

1. **`factory` (Run Once):** A lambda where you create the View (e.g., `return WebView(context)`). This runs **only once** when the composable enters the screen.
2. **`update` (Run Often):** A lambda that runs on **every recomposition**. This is where you update the View's properties (e.g., `view.loadUrl(url)`).
3. **`modifier`:** To size and place the wrapper box.

### **4. Critical: Lifecycle Management**

Complex Views like `MapView` or `AdView` have their own lifecycle methods (`onResume`, `onPause`, `onDestroy`) that **must** be called.
Since Compose doesn't call these automatically, you have to manually bridge the lifecycle (see Topic 5.5).

- _Note: Many modern libraries (like Google Maps for Compose) now wrap this for you, but you need to know this for custom legacy views._

### **5. Example: Embedding a WebView**

```kotlin
@Composable
fun WebPageScreen(url: String) {
    // AndroidView is a composable that displays a View
    AndroidView(
        modifier = Modifier.fillMaxSize(),

        // 1. FACTORY: Create the view (Runs ONCE)
        factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = true
                webViewClient = WebViewClient() // Open links inside, not Chrome

                // Initial Load
                loadUrl(url)
            }
        },

        // 2. UPDATE: React to state changes (Runs on Recomposition)
        update = { webView ->
            // If the 'url' parameter changes, this block runs again
            if (webView.url != url) {
                webView.loadUrl(url)
            }
        }
    )
}

```

### **6. Interview Prep**

**Interview Keywords**
`AndroidView`, Factory Block, Update Block, `WebView`, Interoperability, Context, Lifecycle bridging.

**Interview Speak Paragraph**

> "When I need to use a component that doesn't exist in Compose yet—like a WebView or a specific Ad SDK—I use the `AndroidView` composable. It requires a `factory` lambda to instantiate the legacy View and an `update` lambda to modify properties during recomposition. Crucially, for complex views like `MapView` that have their own internal lifecycle needs (onCreate, onResume), I must manually manage the lifecycle events, usually by attaching a `LifecycleEventObserver` to the current `LocalLifecycleOwner` to forward events to the embedded view."

---

**Next Step:**
You can mix Compose and Views. But how do you verify your Composables work without running the app manually?
Ready for **Topic 10.3: UI Testing (Semantics)**? This is how you find nodes and click buttons in tests.

---

## Navigation

â† Previous
