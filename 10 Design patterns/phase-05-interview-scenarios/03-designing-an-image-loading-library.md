---
layout: default
title: "Designing an Image Loading Library"
parent: "Phase 5: Real World Interview Scenarios"
nav_order: 3
---

# Designing an Image Loading Library

### **Interview Scenario: Building an Image Loading Library (The "Glide" Challenge)**

If an interviewer asks you to design a simplified version of **Glide** or **Coil**, they are testing your ability to handle **asynchronous tasks**, **caching**, and **resource management**. This scenario is a goldmine for design patterns.

---

### **1. The Strategy: The "Big Three" Patterns**

To build a robust image loader, we use these patterns to handle configuration, display, and state:

- **Builder Pattern:** To handle the complex configuration of an image request (placeholders, transformations, etc.).
- **Proxy Pattern:** To handle the "Lazy Loading" and "Placeholder" logic.
- **Observer Pattern:** To notify the UI when the image has finished downloading or failed.

---

### **2. Why This Combination Exists**

- **The Problem:** Loading an image isn't just a simple URL call. You need to decide: _Should I show a loading spinner? What if the URL is broken? Should I crop the image?_ If you pass all these as constructor parameters, it’s a nightmare.
- **The Solution:** 1. The **Builder** makes the request readable.

2.  The **Proxy** ensures we don't crash the app by loading a 10MB image immediately; it shows a "fake" image (placeholder) first.
3.  The **Observer** waits for the background thread to finish and "pushes" the result to the ImageView.

---

### **3. How It Works (Logical Flow)**

1. **Configuring (Builder):** The user defines the request: `MyGlide.with(context).load(url).into(imageView)`.
2. **Standing In (Proxy):** Before the real image arrives, the library places a **Proxy** object in the `ImageView`. This proxy manages the "Loading State" and shows the placeholder.
3. **Delivering (Observer):** A background worker fetches the image. Once done, it notifies the **Observer** (the UI listener) to replace the placeholder with the actual Bitmap.

---

### **4. Example (A "Mini-Glide" Implementation)**

```kotlin
// --- 1. BUILDER PATTERN ---
// Used to configure the complex request
class ImageRequest(
    val url: String,
    val imageView: ImageView,
    val placeholder: Int = R.drawable.ic_default_loading
) {
    class Builder(val url: String, val imageView: ImageView) {
        private var placeholder: Int = R.drawable.ic_default_loading

        fun placeholder(resId: Int) = apply { this.placeholder = resId }

        fun load() {
            // Here is where the Observer and Proxy logic would kick in
            val request = ImageRequest(url, imageView, placeholder)
            ImageLoaderEngine.execute(request)
        }
    }
}

// --- 2. PROXY PATTERN (The Logic) ---
// The Engine acts as a proxy for the real bitmap
object ImageLoaderEngine {
    fun execute(request: ImageRequest) {
        // 1. Show Placeholder immediately (Proxy behavior)
        request.imageView.setImageResource(request.placeholder)

        // 2. Start Background Thread (Observer logic)
        fetchBitmapAsync(request.url) { bitmap ->
            // --- 3. OBSERVER PATTERN ---
            // Notify the UI when the data is ready
            request.imageView.setImageBitmap(bitmap)
        }
    }
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
[   User Code  ] ----> [ Builder ] ----> (Configures Request)
                                             |
                                             v
[ ImageView ] <--- (Shows Placeholder) --- [ Proxy ]
      |                                      |
      | (Wait for download...)               | (Downloads in Background)
      |                                      v
[ ImageView ] <--- (Notifies/Updates) --- [ Observer ]

```

---

### **6. Interview Keywords**

- **Lazy Loading:** Loading the image only when it’s actually needed.
- **Fluency:** Using the Builder pattern to make the API read like a sentence.
- **Placeholder Logic:** The Proxy acting as a temporary visual stand-in.
- **Asynchronous Callback:** The Observer pattern handling the switch from background thread to UI thread.
- **Resource Management:** Ensuring we don't load the same image twice (Caching).

---

### **7. Interview Speak Paragraph**

> "To design a simplified image loading library like Glide, I would utilize the **Builder pattern** to provide a fluent and readable API for configuring image requests, such as adding placeholders or transformations. I would use the **Proxy pattern** to manage the `ImageView` state, allowing the library to display a lightweight placeholder immediately while the 'real' heavy image is being processed. Finally, the **Observer pattern** would be used to handle the asynchronous delivery of the bitmap; once the background download is complete, the observer notifies the UI thread to update the view. This combination ensures a smooth user experience and clean separation between request configuration, background processing, and UI updates."

---

### **Common Interview "Follow-up" Questions**

**1. "What other pattern would you add for Caching?"**

- **Answer:** "I would use the **Flyweight Pattern** or a simple **Singleton cache**. This ensures that if the same image URL is requested multiple times, we share the same Bitmap in memory rather than creating new ones, which prevents 'Out of Memory' errors."

**2. "How would you handle scrolling in a RecyclerView where images might be canceled?"**

- **Answer:** "I would use the **Command Pattern**. Each image request is a 'Command' that can be stored and, more importantly, **canceled**. If the user scrolls past an item, the library calls `command.cancel()` to stop the background thread and save bandwidth."

---

**This completes our Phase 5 Scenarios!** We have covered Networking, Global State, and Resource Loading.

**Next Step:** Are you ready for **Phase 6: The Interview Q&A (Final Phase)**? We will look at the most common "gotcha" questions and how to answer them with total confidence. Shall we proceed?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
