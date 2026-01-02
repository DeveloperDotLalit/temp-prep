---
layout: default
title: "Proxy Pattern"
parent: "Phase 2: Structural Patterns"
nav_order: 3
---

# Proxy Pattern

### **Proxy Pattern: The "Executive Assistant"**

Think of the **Proxy Pattern** like a busy CEO and their **Assistant**. If you want to talk to the CEO, you don't walk into their office directly. You talk to the Assistant first. The Assistant checks if the CEO is available, handles small requests themselves, or makes you wait if the CEO is busy. The Assistant is the "Proxy"—they stand in for the real person and control access to them.

---

### **1. What It Is**

The **Proxy Pattern** is a structural design pattern that provides a substitute or placeholder for another object. A proxy controls access to the original object, allowing you to perform something either before or after the request reaches the original object.

In Android, this is most common when dealing with **Heavy Resource Loading** (like high-resolution images or large database files) where you don't want to create the "heavy" object until it is absolutely needed.

---

### **2. Why It Exists (The Problem it Solves)**

Imagine an app that displays a high-definition 4K image.

- **The Problem:** If you load ten 4K images the moment the app starts, the app will freeze or crash due to "Out of Memory" (OOM) errors. You are creating "heavy" objects before the user even scrolls to see them.
- **The Solution:** You use a **Proxy Image**. This proxy is a lightweight object. It shows a simple "Loading..." spinner or a tiny thumbnail first. Only when the image is actually needed on the screen does the Proxy trigger the loading of the real, heavy 4K image.

**Key Benefits:**

- **Lazy Initialization:** The "heavy" object is only created when it's actually used.
- **Security/Access Control:** The proxy can check if a user has permission before letting them access the real object.
- **Performance:** It saves memory and processing power by acting as a lightweight "stand-in."

---

### **3. How It Works**

1. **The Subject (Interface):** An interface that both the Real Object and the Proxy follow.
2. **The Real Subject:** The heavy, resource-intensive object.
3. **The Proxy:** The object that the client talks to. it holds a reference to the Real Subject and controls its lifecycle.

---

### **4. Example (Practical Android/Kotlin)**

#### **The Scenario: Loading a Huge Video/Media File**

```kotlin
// 1. The common interface
interface VideoProvider {
    fun playVideo()
}

// 2. The Real Subject (The heavy object)
class RealVideoPlayer(val filename: String) : VideoProvider {
    init {
        loadHeavyFileFromDisk()
    }

    private fun loadHeavyFileFromDisk() {
        println("Loading 2GB video file: $filename... (This takes 5 seconds)")
    }

    override fun playVideo() {
        println("Now playing $filename")
    }
}

// 3. The Proxy (The lightweight stand-in)
class VideoProxy(val filename: String) : VideoProvider {
    private var realVideoPlayer: RealVideoPlayer? = null

    override fun playVideo() {
        // Access Control / Lazy Loading
        if (realVideoPlayer == null) {
            realVideoPlayer = RealVideoPlayer(filename)
        }
        realVideoPlayer?.playVideo()
    }
}

// --- HOW TO USE IT ---
fun main() {
    // We create the Proxy. Note: The heavy 2GB file IS NOT loaded yet!
    val video: VideoProvider = VideoProxy("Vacation_4K.mp4")

    println("User clicked the play button...")

    // Only now is the heavy object created and the file loaded
    video.playVideo()
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
 Client (Activity)  ----> [ Proxy Object ]
                               |
                               | (Check: Is real object created?)
                               |
              /----------------+----------------\
        [ Yes ]                          [ No ]
           |                               |
     Forward call to             [ Create Real Subject ]
      Real Subject                         |
                                     Heavy Loading...

```

---

### **6. Interview Keywords**

- **Placeholder:** An object that stands in for another.
- **Lazy Loading:** Delaying the creation of an object until it is used.
- **Virtual Proxy:** A proxy used to manage "expensive" resources (most common in Android).
- **Access Control:** Deciding who can use the real object.
- **Protection Proxy:** Managing security/permissions.

---

### **7. Interview Speak Paragraph**

> "The Proxy Pattern is a structural design pattern that acts as a placeholder for another object to control access to it. In Android development, we primarily use it as a 'Virtual Proxy' for heavy resource management. For example, when loading large media files or initializing expensive SDKs, the Proxy allows us to defer the memory-intensive creation of the real object until it is strictly necessary. This ensures that the app remains responsive and avoids unnecessary memory overhead. It essentially provides a layer of 'Lazy Initialization' that is transparent to the client."

---

### **Interview "Pro-Tip" (Comparison)**

An interviewer might ask: **"How is a Proxy different from a Facade?"**

- **Your Answer:** "The goals are different. A **Facade** is used to **simplify** a complex interface (one door for many rooms). A **Proxy** has the **same interface** as the original object but is used to **control access** (a security guard at the door). While they both sit in front of other classes, the Facade provides a _new_ interface, whereas the Proxy implements the _existing_ interface."

---

**This wraps up the most critical Structural Patterns!** Would you like to finish Phase 2 with the **Composite Pattern** (how Views and ViewGroups work), or are you ready to jump into **Phase 3: Behavioral Patterns** (starting with the very popular **Observer Pattern**)?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
