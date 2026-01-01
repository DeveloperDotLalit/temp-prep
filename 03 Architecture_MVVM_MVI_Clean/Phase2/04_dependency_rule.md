---
layout: default
title: Dependency Rule
parent: Architecture (MVVM/MVI/Clean): Phase2
nav_order: 4
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **The Dependency Rule**.

This is the rule that holds the entire architecture together. If you break this, Clean Architecture collapses.

---

### **Topic: The Dependency Rule**

#### **What It Is**

The Dependency Rule is the strict law that governs how the layers of your app talk to each other.
**The Rule:** Dependencies can only point **inwards**.

- **Outer layers** (UI, Database, Frameworks) know about **Inner layers** (Domain).
- **Inner layers** (Domain) **NEVER** know about **Outer layers**.

Think of it like a castle:

- The **King (Domain)** sits in the center. He gives orders.
- The **Guards (UI/Data)** are on the outer walls. They listen to the King.
- The King does not know the names of the guards. He doesn't care if the guards change shift; he just cares that his orders are followed.

#### **Why It Exists (The Problem)**

If the Inner Layer depends on the Outer Layer, your code becomes fragile.

- **Example of Breaking the Rule:** If your business logic (Inner) imports an Android button (Outer).
- **Consequence:** If Google updates how buttons work, your business logic breaks. You don't want your math calculations to crash just because the UI changed color.
- **Stability:** The Domain is the most stable part of your app. It shouldn't change just because you switched from SQLite to Room (Data layer change).

#### **How It Works (Dependency Inversion)**

You might ask: _"Wait, if the Domain (Inner) needs data from the Repository (Outer), how does it call it without knowing it?"_

We use a trick called **Dependency Inversion** (using Interfaces):

1. **The Domain defines an Interface:** "I need a `UserRepository` that has a `getUser()` function." (It doesn't know _how_ it works, just _what_ it needs).
2. **The Data Layer implements that Interface:** "I will build the actual class that fetches data from the API and matches the Domain's requirements."
3. **Result:** The Domain calls the Interface (which lives in the Domain). It never touches the Data layer directly.

#### **Example (The Illegal Import)**

The easiest way to check if you are following this rule is to look at your `imports` at the top of the file.

**Scenario:** You are writing a Use Case in the **Domain Layer**.

**❌ BAD (Breaking the Rule):**

```kotlin
package com.myapp.domain

// STOP! You are importing an Android UI class into the Domain!
import android.widget.Toast
// STOP! You are importing a Data library into the Domain!
import com.myapp.data.MyRetrofitApi

class LoginUseCase {
    fun execute() {
        Toast.makeText(...) // The Domain now depends on the UI.
    }
}

```

**✅ GOOD (Following the Rule):**

```kotlin
package com.myapp.domain

// Only pure Kotlin imports allowed here.
import com.myapp.domain.repository.UserRepository // Interface defined in Domain

class LoginUseCase(private val repository: UserRepository) {
    fun execute() {
        // We talk to the Interface, not the implementation
        repository.login()
    }
}

```

#### **Interview Keywords**

Dependency Rule, Inversion of Control (IoC), Dependency Inversion Principle, Abstraction, Inner vs. Outer Layers, Unidirectional Dependency.

#### **Interview Speak Paragraph**

> "I strictly follow the Dependency Rule, which states that source code dependencies can only point inwards. The inner layers, like the Domain, should know nothing about the outer layers, like the UI or Database. This ensures that my business logic is protected from changes in the framework. If I need the Domain to communicate with the Data layer, I use Dependency Inversion: the Domain defines an interface, and the Data layer implements it."

---

### **Phase 2 Complete!**

You now have the "Blueprint." You know how to structure the code and keep the layers independent.

**Would you like to move to Phase 3: "The Flow – Reactive Data & State Management"?** (This covers how we actually move data using Coroutines and Flow).
