---
layout: default
title: "Strategy Pattern"
parent: "Phase 3: Behavioral Patterns"
nav_order: 2
---

# Strategy Pattern

### **Strategy Pattern: The "Swiss Army Knife" Approach**

Think of the **Strategy Pattern** like a **GPS Navigation App**. When you want to go from Point A to Point B, the app asks: "How do you want to get there?" You can choose **Driving**, **Walking**, **Cycling**, or **Public Transport**. The _goal_ is the same (reaching the destination), but the _algorithm_ (the route calculation) changes based on your choice. You can swap these "strategies" instantly without restarting the app.

---

### **1. What It Is**

The **Strategy Pattern** is a behavioral design pattern that defines a family of algorithms, encapsulates each one in a separate class, and makes them interchangeable. It lets the algorithm vary independently from the clients that use it.

In simple terms: It’s a way to change the **behavior** of an object at runtime without changing the object itself.

---

### **2. Why It Exists (The Problem it Solves)**

Imagine you are building a **Checkout Screen** for an e-commerce app.

- **The Problem (The "If-Else" Nightmare):** You start by supporting Credit Cards. Then you add PayPal. Then Google Pay. Then "Buy Now, Pay Later."
  Without the Strategy pattern, your `processPayment()` function would look like this:
  `if (type == CARD) { ... } else if (type == PAYPAL) { ... } else if (type == GOOGLE_PAY) { ... }`
  This makes the class huge, hard to test, and every time you add a new payment method, you risk breaking the old ones.
- **The Solution:** You create a "Payment Strategy" interface. Each payment method gets its own class. The Checkout class just holds a reference to the interface and calls `.pay()`. You can plug in any strategy you want.

**Key Benefits:**

- **Clean Code:** Replaces messy conditional logic (`if-else` or `switch`).
- **Open/Closed Principle:** You can add new behaviors (strategies) without touching the existing code.
- **Runtime Flexibility:** You can switch behaviors while the app is running (e.g., changing a sorting filter).

---

### **3. How It Works**

1. **The Strategy Interface:** A common interface for all supported versions of the algorithm.
2. **Concrete Strategies:** The actual classes that implement the specific algorithms.
3. **The Context:** The class that _uses_ the strategy. It doesn't know _which_ strategy it has; it just knows it has one that follows the interface.

---

### **4. Example (Practical Android/Kotlin)**

#### **The Scenario: Image Compression in a Chat App**

Users can choose to send images in "High Quality," "Balanced," or "Data Saver" mode.

```kotlin
// 1. The Strategy Interface
interface CompressionStrategy {
    fun compress(imagePath: String)
}

// 2. Concrete Strategies
class HighQualityCompression : CompressionStrategy {
    override fun compress(imagePath: String) {
        println("Compressing $imagePath slightly to keep maximum detail... ✨")
    }
}

class DataSaverCompression : CompressionStrategy {
    override fun compress(imagePath: String) {
        println("Compressing $imagePath heavily to save mobile data... 📉")
    }
}

// 3. The Context (The class that uses the strategy)
class ImageUploader(private var strategy: CompressionStrategy) {

    // This allows swapping the strategy at runtime!
    fun setCompressionMode(newStrategy: CompressionStrategy) {
        this.strategy = newStrategy
    }

    fun upload(path: String) {
        strategy.compress(path)
        println("Uploading image...")
    }
}

// --- HOW TO USE IT ---
fun main() {
    val uploader = ImageUploader(HighQualityCompression())
    uploader.upload("vacation.jpg")

    // User switches to Data Saver mode in settings
    println("--- User switched to Data Saver ---")
    uploader.setCompressionMode(DataSaverCompression())
    uploader.upload("vacation.jpg")
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
  [ Client Code ]
         |
         | 1. Select Strategy (e.g., Credit Card)
         v
  [ Context Object ] ----> Uses ----> [ Strategy Interface ]
                                              ^
                                              |
                          /-------------------+-------------------\
                [ Strategy A ]          [ Strategy B ]          [ Strategy C ]
                (Credit Card)           (PayPal)                (Google Pay)

```

---

### **6. Interview Keywords**

- **Interchangeable Algorithms:** Swapping logic at runtime.
- **Composition over Inheritance:** Instead of inheriting to change behavior, we compose with a strategy object.
- **Encapsulation:** Hiding the specific logic inside separate classes.
- **Open/Closed Principle:** Open for extension (new strategies), closed for modification (the Context stays the same).
- **Runtime Switch:** Changing behavior while the app is live.

---

### **7. Interview Speak Paragraph**

> "The Strategy Pattern is a behavioral pattern that allows us to define a family of algorithms and make them interchangeable at runtime. In Android, this is incredibly useful for scenarios like payment processing, data compression, or even choosing between different sorting behaviors in a list. Instead of using complex `if-else` or `when` blocks that make a class difficult to maintain, we encapsulate each behavior into its own class. This promotes the Open/Closed Principle, allowing us to add new behaviors without modifying existing code, and results in a more modular and testable architecture."

---

### **Interview "Pro-Tip" (Strategy vs. State)**

An interviewer might ask: **"How is Strategy different from the State pattern?"**

- **Your Answer:** "The intent is different. In the **Strategy** pattern, the user (or the client) usually chooses which strategy to use, and the strategies are often independent of each other. In the **State** pattern, the object changes its own behavior automatically based on its internal state, and the states often know about each other to trigger transitions (like moving from 'Loading' to 'Success')."

---

**Next Step:** Would you like to dive into the **State Pattern** now to see that comparison in action, or should we look at the **Command Pattern**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
