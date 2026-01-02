---
layout: default
title: "Adapter Pattern"
parent: "Phase 2: Structural Patterns"
nav_order: 1
---

# Adapter Pattern

### **Adapter Pattern: The "Universal Travel Plug"**

Think of the **Adapter Pattern** like traveling to a different country with your laptop. Your laptop plug has three pins (your Data), but the wall socket only has two holes (the UI/RecyclerView). You don't take your laptop apart to change the wire; you just use a **Travel Adapter**. The adapter takes the "incompatible" plug and makes it work with the "incompatible" socket.

---

### **1. What It Is**

The **Adapter Pattern** is a structural design pattern that allows two objects with incompatible interfaces to work together. It acts as a middleman (the bridge) that translates the data from one format into a format the other side understands.

---

### **2. Why It Exists (The Problem it Solves)**

In Android, the most common example is the `RecyclerView`.

- **The Problem:** You have a **List of Data** (like a List of "User" objects from a database). On the other side, you have a **List of Views** (the XML rows on the screen). The data doesn't know how to draw itself, and the View doesn't know what a "User" object is.
- **The Solution:** The `RecyclerView.Adapter`. It sits in the middle. It takes the "User" data, pulls out the name and photo, and "plugs" them into the TextViews and ImageViews of the row.

**Key Benefits:**

- **Reusability:** You can use the same data in different layouts by just changing the adapter.
- **Separation of Concerns:** The Data doesn't need to know about the UI, and the UI doesn't need to know about the Data structure.

---

### **3. How It Works**

1. **The Client:** The object that wants to show something (e.g., the `RecyclerView`).
2. **The Adaptee:** The incompatible object you have (e.g., your `List<User>`).
3. **The Target:** The interface the Client expects.
4. **The Adapter:** The class that joins them. It takes the Adaptee and converts it into the Target.

---

### **4. Example (Practical Android/Kotlin)**

In Android, we don't just use this for RecyclerViews; we use it whenever we need to bridge two systems. Let's look at a custom example: Converting an old "Legacy Printer" to work with a new "Modern Computer."

```kotlin
// 1. The Target (What the modern computer expects)
interface ModernUSB {
    fun connectWithUSB()
}

// 2. The Adaptee (The old machine we already have)
class LegacyPrinter {
    fun connectWithOldSerialPort() {
        println("Printing using the old 9-pin serial port...")
    }
}

// 3. The Adapter (The Bridge)
class PrinterAdapter(private val legacyPrinter: LegacyPrinter) : ModernUSB {
    override fun connectWithUSB() {
        // Translation happens here: USB signal is converted to Serial signal
        println("Adapter converting USB signal to Serial...")
        legacyPrinter.connectWithOldSerialPort()
    }
}

// --- HOW IT LOOKS IN ACTION ---
fun main() {
    val oldPrinter = LegacyPrinter()
    val adapter = PrinterAdapter(oldPrinter)

    // The computer thinks it's just using a USB device
    adapter.connectWithUSB()
}

```

**In a RecyclerView context:**

- **Adaptee:** Your `List<Message>`
- **Adapter:** `MessageAdapter`
- **Target:** `RecyclerView.ViewHolder` (The Adapter translates `Message.text` into `textView.text`).

---

### **5. Logical Flow (Text Diagram)**

```text
[ Data Source ]  ----->  [  Adapter  ]  ----->  [  UI Component  ]
(List of Objects)        (Translates)           (Displays View)

      ^                        |                       ^
      |                        |                       |
 "Here is a User"  --->  "Take Name/Bio"  --->  "Put in TextViews"

```

---

### **6. Interview Keywords**

- **Bridge/Middleman:** Acts as a connector.
- **Incompatible Interfaces:** When two classes can't talk directly.
- **Wrapper:** The Adapter "wraps" the original object to give it a new face.
- **RecyclerView.Adapter:** The most famous Android implementation.
- **Translation Logic:** Converting data format A to format B.

---

### **7. Interview Speak Paragraph**

> "The Adapter Pattern is a structural pattern that acts as a bridge between two incompatible interfaces. In Android, the most prominent example is the `RecyclerView.Adapter`, which bridges our data models—like a List of Kotlin objects—with the UI ViewHolders. It allows the RecyclerView to remain agnostic of the data structure while ensuring the UI is populated correctly. By using an adapter, we decouple the data logic from the presentation logic, making it easy to swap data sources or change UI layouts without breaking the underlying system."

---

### **Interview "Pro-Tip" (The "Real" Question)**

Interviewer might ask: **"Why do we need a ViewHolder inside the Adapter?"**

- **Your Answer:** "The Adapter's job is to bridge data to views. However, finding views using `findViewById` is expensive. The **ViewHolder pattern** (often used inside the Adapter) caches those view references. So, the Adapter handles the _mapping_ of data, while the ViewHolder handles the _performance_ of the views."

---

**Would you like to continue with the Facade Pattern, or shall we look at the Proxy Pattern next?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
