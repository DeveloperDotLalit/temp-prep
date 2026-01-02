---
layout: default
title: "Builder Pattern"
parent: "Phase 1: Creational Patterns"
nav_order: 3
---

# Builder Pattern

### **Builder Pattern: The "Custom Pizza" Approach**

Think of the **Builder Pattern** like ordering a custom pizza. You don't want a "Default Pizza" where you have to scrape off toppings you don't like. Instead, you start with the crust and say: "Add pepperoni," "Add extra cheese," and "Hold the onions." Only when you are finished giving instructions do you say, "Bake it!" (the `build()` command).

---

### **1. What It Is**

The **Builder Pattern** is a creational design pattern used to construct complex objects step-by-step. It allows you to produce different types and representations of an object using the same construction code.

In Android, it helps us avoid "Telescoping Constructors" (constructors with 10+ parameters where half of them are usually null or optional).

---

### **2. Why It Exists (The Problem it Solves)**

Imagine you are building a `User` profile object. A user _must_ have a Name, but they _might_ have an Age, a Phone Number, an Address, and a Profile Picture.

- **The Problem:** Without a Builder, you’d need a constructor like this:
  `User("John", null, null, "123 Street", null)`.
  This is hard to read. Which `null` is the phone number? Which one is the age? If you have 10 optional fields, the code becomes a nightmare to manage.
- **The Solution:** The Builder allows you to call only the methods you need:
  `UserBuilder().setName("John").setAddress("123 Street").build()`.
  It’s readable, organized, and you only provide the data that matters.

---

### **3. How It Works**

1. **The Product:** The complex class you want to create (e.g., `Notification`).
2. **The Builder:** A nested or separate class that contains all the fields of the Product.
3. **Setter Methods:** Methods in the Builder that return the Builder itself (`return this`). This allows for **Method Chaining** (linking calls with dots).
4. **The Build Method:** A final method (usually called `build()`) that returns the fully assembled Product.

---

### **4. Example (Practical Android/Kotlin)**

In Android, you see this everywhere with `NotificationCompat.Builder` or `AlertDialog.Builder`. Let’s look at how we’d write one for a custom `Laptop` object.

```kotlin
// 1. The Product
class Laptop(
    val processor: String?,
    val ram: String?,
    val battery: String?,
    val isGraphicsCardEnabled: Boolean
) {
    // 2. The Builder Class
    class Builder {
        private var processor: String? = null
        private var ram: String? = null
        private var battery: String? = null
        private var isGraphicsCardEnabled: Boolean = false

        // 3. Setters that return 'this' for chaining
        fun setProcessor(p: String) = apply { this.processor = p }
        fun setRam(r: String) = apply { this.ram = r }
        fun setBattery(b: String) = apply { this.battery = b }
        fun setGraphicsCard(enabled: Boolean) = apply { this.isGraphicsCardEnabled = enabled }

        // 4. The final build method
        fun build(): Laptop {
            return Laptop(processor, ram, battery, isGraphicsCardEnabled)
        }
    }
}

// --- HOW TO USE IT ---
fun main() {
    val myLaptop = Laptop.Builder()
        .setProcessor("i7")
        .setRam("16GB")
        .setGraphicsCard(true) // Notice we skipped 'setBattery' - it stays null/default
        .build()

    println("Laptop built with ${myLaptop.processor} processor.")
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
Step 1: Start Builder ----> [ Empty Laptop Shell ]
                                     |
Step 2: Config     ----> .setProcessor("i7")  [Add i7]
                                     |
Step 3: Config     ----> .setRam("16GB")      [Add 16GB]
                                     |
Step 4: Execution  ----> .build()             [Assemble & Return Final Object]

```

---

### **6. Interview Keywords**

- **Method Chaining:** Calling multiple methods in a single line using dots.
- **Telescoping Constructor:** An anti-pattern where you have too many constructor parameters.
- **Immutability:** Builders often create objects that cannot be changed once `build()` is called.
- **Optional Parameters:** Easily handling fields that aren't always required.
- **Fluent API:** Designing code that reads like a natural sentence.

---

### **7. Interview Speak Paragraph**

> "The Builder Pattern is a creational pattern designed to solve the problem of complex constructors. Instead of passing a long list of parameters into a single constructor, the Builder allows us to construct an object step-by-step using method chaining. This is used extensively in the Android Framework, such as with `NotificationCompat.Builder` or `Retrofit.Builder`. It significantly improves code readability and maintainability, especially when an object has many optional attributes, as it ensures that the resulting object is always in a valid state when finally constructed."

---

### **Interview "Pro-Tip" (The "Kotlin" Way)**

An interviewer might ask: **"Do we always need a Builder in Kotlin?"**

- **Your Answer:** "Strictly speaking, Kotlin's **Named and Default Parameters** can often replace the Builder pattern for simple data classes. For example, `class User(val name: String, val age: Int = 0)`. However, for complex objects where the construction logic involves validation or specific sequences (like building a `NetworkRequest`), the Builder Pattern is still the professional standard because it encapsulates that logic better than a simple constructor."

---

**Would you like to wrap up Phase 1 with Dependency Injection (DI), or would you prefer to move into Phase 2: Structural Patterns?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
