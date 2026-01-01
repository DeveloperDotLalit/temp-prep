---
layout: default
title: Domain Usecases
parent: Architecture (MVVM/MVI/Clean): Phase 2: The Blueprint – Implementing Clean Architecture
nav_order: 3
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **The Domain Layer & Use Cases**.

This is the most "intellectual" part of your code—it's where the actual business rules live.

---

### **Topic: The Domain Layer & Use Cases**

#### **What It Is**

The **Domain Layer** is the central circle of Clean Architecture. It contains the "Business Logic"—the specific rules that make your app unique.

Inside this layer, we use **Use Cases** (sometimes called Interactors).
A **Use Case** is a small class that does **one specific thing**.

- Examples: `LoginUserUseCase`, `CalculateTotalCostUseCase`, `ValidateEmailUseCase`.

**Crucially:** This layer is **Pure Kotlin**. It has **NO Android code** (no `Context`, no `Activity`, no `TextView`). It doesn't know it's running on a phone.

#### **Why It Exists (The Problem)**

1. **Reusability:** Business rules shouldn't depend on the UI. If you calculate a loan interest rate, that math is the same whether you display it on an Android phone, an iPhone, or a website.
2. **Readability (Screaming Architecture):** If a new developer looks at your Domain folder, they should see file names like `GetNewsUseCase`, `BookmarkArticleUseCase`. They instantly know _what the app does_ without reading the code.
3. **Testability:** Since there is no Android code, you can test these rules instantly on your computer (JVM test) without needing an emulator.

#### **How It Works**

A Use Case usually follows these steps:

1. **Input:** The ViewModel calls the Use Case (sometimes passing data).
2. **Process:** The Use Case applies business rules (e.g., "Is the password long enough?", "Add tax to the price").
3. **Data:** It asks the **Repository** for data if needed.
4. **Output:** It returns the final result to the ViewModel.

_Note: We often use the `operator fun invoke()` in Kotlin so we can call the class like a function._

#### **Example (E-Commerce App)**

Imagine a "Checkout" screen. You don't just send the price to the server; you have to calculate tax and check for coupons first.

**Bad Way (Logic in ViewModel):**
The ViewModel has a 50-line function calculating math. Hard to read, hard to reuse elsewhere.

**Good Way (Use Case):**

```kotlin
// Pure Kotlin class - No Android imports!
class CalculateTotalUseCase(private val repository: CartRepository) {

    // "invoke" allows us to call this class like a function
    operator fun invoke(basePrice: Double, couponCode: String?): Double {

        var finalPrice = basePrice

        // Rule 1: Apply Coupon
        if (couponCode == "DISCOUNT50") {
            finalPrice = finalPrice * 0.5
        }

        // Rule 2: Add Tax (e.g., 10%)
        finalPrice = finalPrice * 1.10

        return finalPrice
    }
}

// In ViewModel, usage is super clean:
val total = calculateTotalUseCase(100.0, "DISCOUNT50")

```

#### **Interview Keywords**

Business Logic, Pure Kotlin, Platform Agnostic, Single Responsibility Principle (SRP), Interactor, Screaming Architecture, Reusability, invoke operator.

#### **Interview Speak Paragraph**

> "I use a Domain Layer to isolate my business logic from the Android framework. I implement this using 'Use Cases,' where each class is responsible for a single action, like `LoginUser` or `RefreshFeed`. This keeps my ViewModels lean because they just delegate work to the Use Cases. It also makes the code 'Platform Agnostic'—meaning the business rules are pure Kotlin and can be easily unit-tested without needing an Android device."

---

**Would you like to proceed to the next note: "Dependency Rule"?**
