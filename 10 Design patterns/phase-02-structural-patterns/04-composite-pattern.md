---
layout: default
title: "Composite Pattern"
parent: "Phase 2: Structural Patterns"
nav_order: 4
---

# Composite Pattern

### **Composite Pattern: The "Tree Branch" Structure**

Think of the **Composite Pattern** like a **Folder System** on your computer. You have "Files" and you have "Folders." A folder can contain files, but it can also contain _other_ folders. Whether you want to "Delete," "Copy," or "Move" them, you treat a single file and a whole folder exactly the same way. The folder is a "composite" of many items, but it acts like a single unit.

---

### **1. What It Is**

The **Composite Pattern** is a structural design pattern that lets you compose objects into tree structures to represent part-whole hierarchies. It allows clients to treat individual objects (Leaves) and compositions of objects (Composites) uniformly.

In Android, this is exactly how the **UI Layout** works. A `Button` is a single item, and a `LinearLayout` is a group of items. However, both are `Views`, and you can call `.invalidate()` or `.setVisibility()` on either one without caring which is which.

---

### **2. Why It Exists (The Problem it Solves)**

Imagine you are building a UI rendering engine.

- **The Problem:** You have simple elements (TextView, ImageView) and containers (FrameLayout, ConstraintLayout). If you want to hide a whole section of the screen, you don't want to manually loop through every single TextView and call `hide()`. That code would be a mess of `if (item is Group) { loop } else { hide }`.
- **The Solution:** You make the "Group" and the "Item" share the same interface. When you tell the "Group" to `hide()`, it automatically tells all its children to `hide()`. To the person using the code, the Group looks just like a single Item.

**Key Benefits:**

- **Uniformity:** You can treat complex trees and simple objects the same way.
- **Recursive Power:** You can have groups inside groups inside groups (like nested Layouts).
- **Simplicity:** The client code doesn't need to check if it's talking to a single object or a collection.

---

### **3. How It Works**

1. **The Component (Interface):** The common "language" both single items and groups speak (e.g., the `View` class).
2. **The Leaf (Simple Object):** The basic building block that has no children (e.g., a `Button` or `TextView`).
3. **The Composite (Group):** The object that has children and implements the same Component interface (e.g., a `ViewGroup` or `LinearLayout`).

---

### **4. Example (Practical Android/Kotlin)**

#### **The Scenario: A File System (Folders and Files)**

```kotlin
// 1. The Component (The Interface)
interface FileSystemItem {
    fun getInfo()
}

// 2. The Leaf (The individual file)
class File(val name: String) : FileSystemItem {
    override fun getInfo() {
        println("File: $name")
    }
}

// 3. The Composite (The Folder that contains items)
class Folder(val name: String) : FileSystemItem {
    private val children = mutableListOf<FileSystemItem>()

    fun add(item: FileSystemItem) {
        children.add(item)
    }

    override fun getInfo() {
        println("Folder: $name contains:")
        // The composite delegates the work to its children
        for (item in children) {
            item.getInfo()
        }
    }
}

// --- HOW TO USE IT ---
fun main() {
    val file1 = File("Resume.pdf")
    val file2 = File("Photo.jpg")

    val myFolder = Folder("My Documents")
    myFolder.add(file1)
    myFolder.add(file2)

    val rootFolder = Folder("Root")
    rootFolder.add(myFolder) // Adding a folder inside a folder!

    // We treat 'file1' and 'rootFolder' exactly the same!
    file1.getInfo()
    println("---")
    rootFolder.getInfo()
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
       [ Component (View) ]
        /              \
 [ Leaf (Button) ]   [ Composite (Layout) ]
                             |
                   /---------+---------\
            [ Leaf (Text) ]      [ Composite (Layout) ]
                                          |
                                    [ Leaf (Image) ]

```

---

### **6. Interview Keywords**

- **Part-Whole Hierarchy:** Representing things that contain other things of the same type.
- **Recursive Composition:** A structure that can contain itself.
- **Leaf vs. Composite:** The individual unit vs. the container unit.
- **Uniformity:** Treating all objects in the tree the same way.
- **View vs. ViewGroup:** The classic Android example of this pattern.

---

### **7. Interview Speak Paragraph**

> "The Composite Pattern is a structural design pattern that allows us to treat individual objects and groups of objects uniformly by arranging them into a tree-like hierarchy. The most significant application of this in Android is the View system. Every `ViewGroup`—like a `LinearLayout`—is a composite that can contain multiple `Views`. Because `ViewGroup` itself inherits from `View`, we can treat a complex layout and a single `Button` the same way, such as when calling `draw()` or setting visibility. This recursion allows for highly flexible and deeply nested UI structures while keeping the client code simple and agnostic of the tree's complexity."

---

### **Interview "Pro-Tip" (The Deep Dive)**

An interviewer might ask: **"How does the Composite pattern help with the 'OnDraw' call in Android?"**

- **Your Answer:** "When the system calls `onDraw()` on a `DecorView` (the root), it doesn't need to know what's inside. It calls `draw()` on the root. Because of the Composite pattern, if the root is a `ViewGroup`, it automatically calls `draw()` on all its children. This recursive process continues down the tree until every 'Leaf' (like a TextView) has drawn itself. This makes the entire rendering process clean and automated."

---

**This concludes Phase 2: Structural Patterns!** We have covered **Adapter, Facade, Proxy, and Composite.**

## Are you ready to dive into **Phase 3: Behavioral Patterns**? We'll start with the most important one for modern Android development: the **Observer Pattern** (the magic behind LiveData and Flows).

[â¬… Back to Phase](../) | [Next âž¡](../)
