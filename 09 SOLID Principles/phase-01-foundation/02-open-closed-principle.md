---
layout: default
title: "Open Closed Principle"
parent: "Phase 1: The Foundation (S and O)"
nav_order: 2
---

# Open Closed Principle

Next in Phase 1 is the **Open/Closed Principle (OCP)**. If SRP is about making sure a class doesn't do too much, OCP is about making sure you don't have to "break" your existing, working code every time a product manager asks for a new feature.

---

## **2. Open/Closed Principle (OCP)**

### **What It Is**

The principle states: **"Software entities (classes, modules, functions) should be open for extension, but closed for modification."**

- **Open for Extension:** You should be able to add new behavior or features to your class.
- **Closed for Modification:** You should be able to add those features _without_ changing the source code that is already written, tested, and working.

### **Why It Exists**

- **The Problem:** Imagine you have a working "Payment Processor" that handles Credit Cards. Now, you need to add PayPal. If you have to go inside the existing `PaymentProcessor` class and add an `if/else` or `switch` case, you risk breaking the Credit Card logic that was already perfect.
- **The Consequence:** Every time you "modify" existing code, you have to re-test everything. This leads to "regression bugs" (where old features break because of new ones).
- **The Goal:** To create "Plug-and-Play" code where new features are just new classes plugged into the system.

### **How It Works**

The secret sauce to OCP is **Abstractions (Interfaces or Abstract Classes)**.

1. Instead of writing logic for a specific class, write it for an **Interface**.
2. When a new feature is needed, create a **new class** that implements that interface.
3. The main system doesn't care which class it is using; it just knows it follows the interface rules.

### **Example (The Android Way)**

#### **❌ The Wrong Way (Violating OCP)**

Every time we add a new notification type, we have to modify this `NotificationManager` class.

```kotlin
class NotificationManager {
    // VIOLATION: We have to keep modifying this method for every new type
    fun sendNotification(type: String) {
        if (type == "Email") {
            // Email logic
        } else if (type == "Push") {
            // Push notification logic
        } else if (type == "SMS") {
            // SMS logic
        }
    }
}

```

#### **✅ The OCP Way (Refactored)**

We create an interface and let each notification type handle its own logic. Now, `NotificationManager` is "Closed for Modification."

```kotlin
// 1. Create an Abstraction
interface Notification {
    fun send()
}

// 2. Create specific implementations (Open for Extension)
class EmailNotification : Notification {
    override fun send() { /* Email Logic */ }
}

class PushNotification : Notification {
    override fun send() { /* Push Logic */ }
}

// 3. The Manager class (Closed for Modification)
class NotificationSender {
    fun send(notification: Notification) {
        // This code NEVER changes, even if you add 100 new notification types
        notification.send()
    }
}

```

### **Interview Keywords**

Abstraction, Polymorphism, Interfaces, Plugin Architecture, Regression Bugs, Scalability.

### **Interview Speak Paragraph**

> "The Open/Closed Principle means that our classes should be designed in a way that allows us to add new functionality without modifying the existing source code. In Android, we achieve this through abstraction—using interfaces or abstract classes. For example, instead of using a hardcoded 'when' expression to handle different data sources, we define a Repository interface. This allows us to plug in a new data source, like a Mock API for testing or a new Database, without ever touching the logic in our ViewModels."

---

### **Common Interview Question/Angle**

**Q: "Doesn't OCP lead to over-engineering? When should I NOT use it?"**
**A:** "Great point. OCP is most valuable when you anticipate that a logic or feature is likely to grow or change (like payment methods or analytics providers). If a piece of code is extremely simple and 100% unlikely to ever change, applying OCP might add unnecessary complexity. The key is to apply OCP to the 'volatile' parts of your app."

---

### **Refining Phase 1**

We have covered:

1. **SRP:** One class, one job.
2. **OCP:** Add features by adding new classes, not changing old ones.

**Would you like to wrap up Phase 1 by discussing how to "Identify and Refactor" these in a real project, or shall we move straight to Phase 2: The Structural Pillars (Liskov Substitution Principle)?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
