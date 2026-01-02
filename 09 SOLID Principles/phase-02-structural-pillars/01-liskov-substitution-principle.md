---
layout: default
title: "Liskov Substitution Principle"
parent: "Phase 2: Structural Pillars (L and I)"
nav_order: 1
---

# Liskov Substitution Principle

We are now entering **Phase 2**. While SRP and OCP are about how you _organize_ your code, the **Liskov Substitution Principle (LSP)** is about how you _design your inheritance_ so your app doesn't crash unexpectedly.

---

## **4. Liskov Substitution Principle (LSP)**

### **What It Is**

The formal definition is a bit scary, but the beginner version is simple: **"A child class should be able to do everything the parent class can do, without behaving in a way the caller doesn't expect."**

If you have a function that takes a `View` as a parameter, you should be able to pass a `Button`, `TextView`, or `ImageView` into it, and the app should not crash or behave weirdly. The child must be a **true** substitute for the parent.

### **Why It Exists**

- **The Problem:** Developers often use inheritance just to "reuse code," even if the relationship doesn't make sense. They create a child class that "breaks" or "disables" a feature of the parent.
- **The Consequence:** You get `RuntimeExceptions` (like `UnsupportedOperationException`). If someone else on your team uses your class thinking it's a normal `View`, but you've made it do something completely different, the app breaks.
- **The Goal:** To ensure that inheritance hierarchies are logically sound and safe to use anywhere.

### **How It Works**

1. **Don't Force It:** If a child class cannot implement a method of the parent, it shouldn't be a child of that parent.
2. **Avoid Type Checking:** If you find yourself writing `if (view is Button)` inside a function that takes a `View`, you are likely violating LSP.
3. **Behavioral Consistency:** The child should follow the "contract" of the parent. If the parent says `saveData()` returns a boolean, the child shouldn't throw an error instead.

---

### **Example (The Android Way)**

#### **❌ The Wrong Way (Violating LSP)**

Imagine we have a base class for Fragments that require a User ID.

```kotlin
open class BaseUserFragment {
    open fun loadUserData(userId: String) {
        // Logic to fetch user
    }
}

class GuestProfileFragment : BaseUserFragment() {
    override fun loadUserData(userId: String) {
        // VIOLATION: Guests don't have IDs!
        // We throw an error because this method "doesn't make sense" here.
        throw UnsupportedOperationException("Guests have no ID!")
    }
}

```

**Why this is bad:** If a `FragmentPager` tries to refresh all `BaseUserFragments`, it will crash when it hits the `GuestProfileFragment`. The guest fragment is **not** a valid substitute for the base.

#### **✅ The LSP Way (Refactored)**

We move the specific requirement into a more specialized subclass or an interface.

```kotlin
// Base for ALL fragments
open class BaseFragment {
    // Common logic for all fragments
}

// Specialized base for fragments that NEED data
open class AuthenticatedFragment : BaseFragment() {
    open fun loadUserData(userId: String) { ... }
}

class UserProfileFragment : AuthenticatedFragment() {
    override fun loadUserData(userId: String) { ... }
}

class GuestProfileFragment : BaseFragment() {
    // No loadUserData method here, so no chance of crashing!
}

```

---

### **LSP in Custom Views**

If you create a `MyCustomButton` that extends `AppCompatButton`, but you override `setOnClickListener` to do nothing (because you want it to be "unclickable" internally), you are violating LSP. Any developer who uses your button will expect `setOnClickListener` to work because that is the "contract" of a Button.

---

### **Interview Keywords**

Substitutability, Inheritance Contract, Behavioral Subtyping, Runtime Exceptions, Hierarchy Design.

### **Interview Speak Paragraph**

> "Liskov Substitution Principle ensures that a subclass can replace its parent class without affecting the correctness of the program. In Android, a common violation occurs when we create a subclass that throws an 'UnsupportedOperationException' for a method inherited from the parent. This breaks the contract. To follow LSP, I ensure that subclasses stay true to the parent's behavior, or I refactor the hierarchy so that common functionality is moved to a more appropriate base class or an interface."

---

### **Common Interview Question/Angle**

**Q: "How do you detect an LSP violation during a Code Review?"**
**A:** "I look for two things: First, any overridden methods that are empty or throw 'Not Implemented' errors. Second, any code that uses `instanceof` or `is` checks to verify a specific type before calling a method. These are major red flags that the inheritance structure is flawed."

**Are you ready to move to the next topic in Phase 2: Interface Segregation Principle (ISP)?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
