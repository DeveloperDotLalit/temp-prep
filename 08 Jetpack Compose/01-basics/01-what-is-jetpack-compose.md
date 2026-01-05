---
layout: default
title: What is Jetpack Compose?
parent: 1. Introduction + Basic Composables
nav_order: 1
---

# What is Jetpack Compose?

Here are your notes for the first sub-topic of the Masterclass.

---

## **Topic 1.1: What is Jetpack Compose?**

### **1. What It Is**

Jetpack Compose is Google’s modern toolkit for building native Android apps. It is **Declarative**, meaning you describe **what** the UI should look like using Kotlin code, and the system handles the drawing.

It replaces the old way of building Android apps (which used XML files for layout and Java/Kotlin for logic) with a single, unified Kotlin codebase.

### **2. Why It Exists (The Evolution of Android UI)**

To understand Compose, you have to understand the problem with the old system (the "View System"):

- **The "God Class" Problem:** In the old system, every single UI element (Button, Checkbox, Slider) inherited from a class called `View`. Over 10+ years, this `View.java` file grew to be massive (over 30,000 lines of code!). Even if you just wanted a simple empty box, your app loaded all that heavy baggage.
- **The Split Brain Problem:** You had your layout in **XML** and your logic in **Kotlin/Java**. They didn't talk to each other directly. You had to use `findViewById` to bridge them. If you deleted a Button in XML but forgot to remove the code in Kotlin that referenced it, your app would crash.
- **The Update Problem:** The old View system was part of the Android OS. If Google fixed a bug in `TextView`, you had to wait for users to update their Android OS version to get that fix. Compose is a **library**—you can update it instantly, just like any other dependency.

### **3. Declarative vs. Imperative Programming**

This is the most important concept to master.

- **Imperative (The Old Way - XML/Views):**
  You are like a **Micromanager**. You tell the system exactly _how_ to change things step-by-step.
- _Code:_ "Find the text view. Now set its text to 'Hello'. Now change its color to Red."
- _Mental Model:_ You are manually mutating the widget.

- **Declarative (The New Way - Compose):**
  You are like an **Architect**. You hand over a blueprint and say, "This is what I want based on this data."
- _Code:_ "Show a Red Text that says 'Hello'."
- _Mental Model:_ You describe the result; the system figures out how to render it.

**Comparison Chart**

| Feature      | Imperative (XML)            | Declarative (Compose)                       |
| ------------ | --------------------------- | ------------------------------------------- |
| **Focus**    | Focus on _how_ to change UI | Focus on _what_ the UI should be            |
| **State**    | You manually update widgets | UI updates automatically when state changes |
| **Language** | XML + Kotlin/Java           | 100% Kotlin                                 |
| **Bugs**     | UI desync is common         | UI is the "Source of Truth"                 |

### **4. Compiler-Based UI Generation**

**How It Works**
Compose is technically not just a library; it is heavily powered by a **Kotlin Compiler Plugin**.

When you annotate a function with `@Composable`, the compiler steps in. It transforms your code into a structure that can track your data. When your data changes, the compiler-generated code knows exactly which part of the UI needs to be redrawn and skips the rest. This makes it efficient enough to rebuild the UI tree repeatedly without lag.

### **5. Example: The Shift**

**The Old Way (Imperative)**
You have to maintain two files.

- `layout.xml`: `<TextView android:id="@+id/tv_name" ... />`
- `Activity.kt`:

```kotlin
val textView = findViewById<TextView>(R.id.tv_name)
textView.text = "John Doe" // Manually mutating the view
textView.visibility = View.VISIBLE // Manually changing visibility

```

**The New Way (Declarative)**
Just one Kotlin file. You describe the UI based on the data.

```kotlin
@Composable
fun UserProfile(name: String, isVisible: Boolean) {
    if (isVisible) {
        // You don't "set" text. You "declare" a Text composable.
        Text(text = name)
    }
}

```

_Note: In the Compose example, if `isVisible` becomes false, the `Text` doesn't just hide—it is completely removed from the UI tree automatically._

---

### **6. Interview Prep**

**Interview Keywords**
Declarative UI, Imperative UI, View System, Unbundled Toolkit, Compiler-based, Source of Truth, UI Tree.

**Interview Speak Paragraph (Memorize this flow)**

> "Jetpack Compose is Android's modern, declarative UI toolkit. It solves the historical challenges of the legacy View system, such as the separation between XML and Kotlin and the bloated `View` class hierarchy. Unlike the imperative approach where we manually mutated views, Compose is declarative—we describe the UI based on its current state, and the compiler handles the rendering. It's also 'unbundled' from the Android OS, meaning we can get the latest UI features and bug fixes without waiting for the user to update their phone."

---

**Next Step:**
Would you like to move to **Topic 1.2: Why Compose (vs XML)?** where we dive deeper into specific benefits like Live Previews and less code?

---

## Navigation

Next â†’
