---
layout: default
title: Image Loading (Coil/Glide)
parent: 3. Lists, Grids & UI Enhancements
nav_order: 8
---

# Image Loading (Coil/Glide)

Here are your notes for **Topic 3.8**.

---

## **Topic 3.8: Image Loading (Coil/Glide)**

### **1. What It Is**

Jetpack Compose does **not** have a built-in way to load images from URLs (e.g., "https://.../cat.png").
To do this, we use third-party libraries.

- **Coil (Recommended):** "Coroutine Image Loader". It is built specifically for Kotlin and Compose. It is lightweight and backed by Google.
- **Glide:** The old standard for XML. It works in Compose but is heavier and less "Compose-native."

### **2. Why It Exists (The Network Problem)**

Loading an image is hard:

1. Download bytes from the internet (background thread).
2. Decode bytes into a Bitmap (CPU intensive).
3. Resize to fit the screen (Memory intensive).
4. Cache it so we don't download it again next time.
5. Fade it in so it doesn't pop.
   Coil handles all of this with one line of code: `AsyncImage`.

### **3. How It Works**

#### **A. The Standard Way: `AsyncImage**`

This is the simple "fire and forget" composable.

- **model:** The URL (or File/URI).
- **contentDescription:** Mandatory for accessibility.
- **placeholder:** Shown _while_ downloading.
- **error:** Shown _if_ download fails.

#### **B. The Advanced Way: `SubcomposeAsyncImage**`

Sometimes `AsyncImage` is too simple. You want to show a **CircularProgressIndicator** while loading, not just a static placeholder image.

- **Logic:** `SubcomposeAsyncImage` gives you a "scope" where you can check the current state (Loading, Success, Error) and decide exactly what Composable to draw.

#### **C. Caching**

Coil handles caching automatically.

- **Memory Cache:** Keeps recently used bitmaps in RAM for instant access.
- **Disk Cache:** Saves files to the device storage so they work offline or after an app restart.

### **4. Example: Simple vs. Complex**

**Scenario A: The Simple Avatar (AsyncImage)**

```kotlin
AsyncImage(
    model = "https://example.com/avatar.jpg",
    contentDescription = "User Avatar",
    placeholder = painterResource(R.drawable.placeholder_gray),
    error = painterResource(R.drawable.error_icon),
    modifier = Modifier.clip(CircleShape).size(50.dp)
)

```

**Scenario B: The Complex Banner (SubcomposeAsyncImage)**

```kotlin
SubcomposeAsyncImage(
    model = "https://example.com/banner.jpg",
    contentDescription = "Banner",
    modifier = Modifier.fillMaxWidth()
) {
    val state = painter.state
    if (state is AsyncImagePainter.State.Loading) {
        // Show a spinner instead of a static image!
        CircularProgressIndicator()
    } else {
        // Show the actual image
        SubcomposeAsyncImageContent()
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Coil vs. Glide, `AsyncImage`, `SubcomposeAsyncImage`, Memory vs. Disk Caching, Image Pipeline, Crossfade animation.

**Interview Speak Paragraph**

> "For image loading in Compose, I strictly use **Coil** because it's Kotlin-first and built with Coroutines in mind, unlike Glide which was designed for the View system. For standard usage, I use `AsyncImage` to handle asynchronous loading, caching, and placeholders. However, if I need to display a complex loading state—like a progress spinner or a shimmer effect while the image downloads—I use `SubcomposeAsyncImage`, which allows me to define custom composables for the loading and error states."

---

**Congratulations!** You have completed **Part 3: Lists, Grids & UI Enhancements**.
You can now build beautiful, scrollable, interactive UIs.

But... clicking a button doesn't go anywhere yet.
**Are you ready to start Topic 4: Navigation in Compose (Type-Safe)?**
_This is one of the most complex topics, so take a deep breath!_

---

## Navigation

â† Previous
