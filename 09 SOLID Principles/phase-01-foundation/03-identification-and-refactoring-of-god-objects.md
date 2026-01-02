---
layout: default
title: "Identification and Refactoring of God Objects"
parent: "Phase 1: The Foundation (S and O)"
nav_order: 3
---

# Identification and Refactoring of God Objects

This is a crucial "bridge" topic. It’s one thing to know the definitions of SRP and OCP, but it's another to look at a messy codebase and know exactly where to start cutting. In interviews, this shows you have **senior-level experience** because you can identify "Code Smells."

---

## **3. Identification & Refactoring (Killing the "God Object")**

### **What It Is**

**Identification** is the process of spotting "Code Smells"—signs that your code is becoming unmaintainable. The most famous smell is the **God Object** (or God Class), which is a single class that knows too much or does too much.

**Refactoring** is the disciplined process of cleaning that code without changing what it actually does for the user.

### **Why It Exists**

- **The Problem:** Over time, features are "bolted on" to existing Activities or Fragments because it’s faster in the short term.
- **The Consequence:** You end up with a "Spaghetti Code" file that is 2,000 lines long, impossible to unit test, and crashes frequently because side effects are hidden everywhere.
- **The Goal:** To move from a **Monolithic** design (one giant block) to a **Decoupled** design (small, specialized pieces).

---

### **How to Spot a "God Object" (Identification)**

Look for these "Red Flags" in your code:

1. **Line Count:** Is your Activity/Fragment over 500 lines?
2. **The "And" Trap:** When describing the class, do you use the word "and"? (e.g., "This class fetches data **and** parses JSON **and** updates the UI **and** calculates taxes.")
3. **Too Many Dependencies:** Does the constructor (or the top of the file) have 10+ variables like `ApiService`, `Database`, `LocationManager`, `Analytics`, etc.?
4. **The "When" or "If/Else" Monster:** Do you see a 100-line `when` statement checking for different types or states? (This violates OCP).

---

### **How to Refactor (The Step-by-Step Flow)**

1. **Extract Data Logic:** Move all API and Room Database calls into a **Repository**.
2. **Extract Presentation Logic:** Move state handling (like "loading," "error," "success") and data formatting into a **ViewModel**.
3. **Extract Business Rules:** If you have complex math or logic that doesn't care about the UI, move it into a **Use Case** or **Interactor**.
4. **Extract UI Utilities:** Move things like Date Formatting or String manipulation into a **Mapper** or **Utility** class.
5. **Inject:** Use Dependency Injection (like Hilt) to provide these new pieces back to the Activity.

---

### **Example: Refactoring Scenario**

#### **Before (The Mess)**

```kotlin
class OrderActivity : AppCompatActivity() {
    // Flag: Doing too much!
    fun processOrder() {
        // 1. Networking Logic
        api.submitOrder(order)
        // 2. Business Logic
        val tax = order.price * 0.15
        // 3. UI Update Logic
        statusText.text = "Order Placed with tax: $tax"
        // 4. Analytics Logic
        FirebaseAnalytics.logEvent("order_placed")
    }
}

```

#### **After (The Clean Way)**

- **OrderRepository:** handles `api.submitOrder()`.
- **TaxCalculator:** handles the `order.price * 0.15` logic.
- **AnalyticsHelper:** handles the `Firebase` call.
- **OrderViewModel:** Coordinates these three.
- **OrderActivity:** Simply observes the ViewModel and sets `statusText.text`.

---

### **Interview Keywords**

Code Smells, God Object, Technical Debt, Separation of Concerns, Extraction, Delegation, Cognitive Load.

### **Interview Speak Paragraph**

> "When identifying a 'God Object' in Android, I look for classes—typically Activities or Fragments—that have multiple reasons to change, such as handling both API responses and complex UI state. To refactor this, I apply the Single Responsibility Principle by extracting the data layer into Repositories and the business logic into Use Cases or ViewModels. This reduces the 'Cognitive Load' of the file, makes the logic independently testable with JUnit, and ensures the UI layer only focuses on rendering data."

---

### **Common Interview Question/Angle**

**Q: "If you're tasked with refactoring a massive legacy Activity, where do you start? Do you rewrite the whole thing?"**
**A:** "Never rewrite everything at once—that’s how you introduce new bugs. I start by extracting the most 'testable' parts first, usually the business logic or data mapping. I move those into separate classes and write unit tests for them. Once the logic is safe and tested, I slowly thin out the Activity until it's just a thin wrapper for the UI."

---

**You have officially completed Phase 1!** You now know how to make classes focused (SRP), extensible (OCP), and how to fix them when they aren't.

**Ready to move to Phase 2: The Structural Pillars (starting with Liskov Substitution Principle)?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
