---
layout: default
title: "Factory Pattern"
parent: "Phase 1: Creational Patterns"
nav_order: 2
---

# Factory Pattern

### **Factory Pattern: The "Digital Restaurant"**

In the real world, when you go to a restaurant and order a burger, you don't go into the kitchen, find the buns, grill the meat, and assemble it yourself. You just tell the **Waiter (The Factory)**: "I want a Veggie Burger." The waiter handles the complexity of the kitchen and hands you the finished product.

---

### **1. What It Is**

The **Factory Pattern** is a creational pattern that provides a way to create objects without exposing the logic of _how_ they are created to the user. Instead of using the `new` keyword (or calling a constructor) directly for a specific class, you call a "Factory" method and tell it what type of object you need.

---

### **2. Why It Exists (The Problem it Solves)**

Imagine you are building an Android app that supports different types of **Notifications**: _Email_, _SMS_, and _Push Notifications_.

- **The Problem:** Without a Factory, every time you want to send a notification, you have to write `if/else` logic: "If user chose SMS, create SMS object; if Email, create Email object." If you decide to add _WhatsApp_ notifications later, you have to go through your **entire codebase** and update every single `if/else` block. This makes your code "brittle" (easy to break).
- **The Solution:** You move all that "creation logic" into one single place: **The Notification Factory**. Your app just says, "Hey Factory, give me an SMS object," and the Factory does the work. If you add WhatsApp later, you only change the code inside the Factory.

---

### **3. How It Works**

1. **The Interface:** Create a common interface (or abstract class) that all your objects will follow (e.g., `Notification`).
2. **The Concrete Classes:** Build the actual classes that implement that interface (e.g., `SmsNotification`, `EmailNotification`).
3. **The Factory:** Create a class with a method (usually called `create...`) that takes an input (like a String or Enum) and returns the correct object type.

---

### **4. Example (Practical Android/Kotlin)**

#### **The Scenario: A Dialog Creator**

Suppose your app shows different types of Dialogs based on user priority (Success, Error, or Warning).

```kotlin
// 1. The common interface
interface MyDialog {
    fun show()
}

// 2. Concrete Classes (The actual objects)
class SuccessDialog : MyDialog {
    override fun show() = println("Showing Green Success Dialog ✅")
}

class ErrorDialog : MyDialog {
    override fun show() = println("Showing Red Error Dialog ❌")
}

// 3. The Factory (The "Waiter")
object DialogFactory {
    fun createDialog(type: String): MyDialog {
        return when (type) {
            "SUCCESS" -> SuccessDialog()
            "ERROR" -> ErrorDialog()
            else -> throw IllegalArgumentException("Unknown Dialog type")
        }
    }
}

// --- HOW TO USE IT ---
fun main() {
    // The user doesn't know about 'SuccessDialog' or 'ErrorDialog' classes directly
    val dialog = DialogFactory.createDialog("SUCCESS")
    dialog.show()
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
 Client (Your Activity)
        |
        | "I need a 'SUCCESS' object"
        v
  [ DialogFactory ]  <--- (Logic: if type == SUCCESS return SuccessDialog)
        |
        | (Creates object internally)
        v
 [ SuccessDialog ]   <--- (Sent back to Client as 'MyDialog' interface)

```

---

### **6. Interview Keywords**

- **Abstraction:** Hiding the "how" and showing only the "what."
- **Decoupling:** Separating the code that _uses_ the object from the code that _creates_ the object.
- **Open/Closed Principle:** The code is open for extension (you can add new notification types) but closed for modification (you don't have to change the UI code).
- **Centralized Logic:** Creation logic is kept in one place.

---

### **7. Interview Speak Paragraph**

> "The Factory Pattern is a creational design pattern that abstracts the process of object creation. Instead of the client class instantiating specific objects directly, it delegates that responsibility to a Factory class. This is extremely useful in Android when dealing with multiple types of a similar component—like different types of ViewHolders or Notification types. It promotes 'loose coupling' because the calling class doesn't need to know the specific implementation details, making the code much easier to maintain and scale when new types are added."

---

### **Interview "Pro-Tip" (The Difference)**

An interviewer might ask: **"How is this different from a Simple Constructor?"**

- **Your Answer:** "A constructor always returns an instance of the _exact_ class you are calling. A Factory is more flexible; it can return any subclass or implementation of an interface based on the input provided, and it can even reuse existing objects instead of creating new ones if needed."

---

**Would you like to move on to the Builder Pattern next, or do you want to explore more about how the Factory Pattern is used in Android Framework (like ViewModelProvider)?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
