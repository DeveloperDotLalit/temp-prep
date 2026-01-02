---
layout: default
title: "SOLID in Jetpack Compose"
parent: "Phase 4: Real World Android Scenarios"
nav_order: 1
---

# SOLID in Jetpack Compose

In Phase 4, we move away from "Classes" and look at the modern way of building Android UIs: **Jetpack Compose**. Since Compose is functional and declarative, applying SOLID feels a bit different, but the principles are exactly the same.

---

## **9. SOLID in Jetpack Compose**

### **What It Is**

In Jetpack Compose, your "Units" are **@Composable functions** instead of Classes. SOLID in Compose means ensuring your UI functions are modular, reusable, and don't contain hidden business logic.

### **Why It Exists**

- **The Problem:** It is very easy to put "everything" (API calls, state calculation, formatting, and UI) inside a single Composable. This creates a "God Composable" that is impossible to preview or test.
- **The Goal:** To create "Stateless" and "Stateful" Composables that follow SRP and OCP, making your UI "Plug-and-Play."

---

### **1. SRP (Single Responsibility) in Compose**

A Composable should either **manage state** or **render UI**, but rarely both.

- **Stateful Composable:** Handles the "How" (collecting flows from ViewModel).
- **Stateless Composable:** Handles the "What" (the actual UI code). This is called **State Hoisting**.

#### **❌ Violation (The "Do-It-All" Composable)**

```kotlin
@Composable
fun UserProfile() {
    val viewModel: UserViewModel = hiltViewModel()
    val user by viewModel.user.collectAsState()

    // Violation: Fetching state AND rendering UI
    Column {
        Text("Name: ${user.name.uppercase()}") // Violation: Formatting logic in UI
        Button(onClick = { viewModel.updateUser() }) { Text("Update") }
    }
}

```

#### **✅ SRP Refactored**

```kotlin
@Composable
fun UserProfileScreen(viewModel: UserViewModel) { // Stateful
    val user by viewModel.user.collectAsState()
    UserProfileContent(name = user.name) { viewModel.updateUser() }
}

@Composable
fun UserProfileContent(name: String, onUpdate: () -> Unit) { // Stateless & Pure UI
    Column {
        Text("Name: $name")
        Button(onClick = onUpdate) { Text("Update") }
    }
}

```

---

### **2. OCP (Open/Closed) in Compose**

In Compose, OCP is achieved through **Slot API Patterns**. Instead of hardcoding a specific child Composable, you leave a "slot" (a `content: @Composable () -> Unit` parameter).

#### **✅ OCP Example (Slot API)**

```kotlin
@Composable
fun CustomCard(
    title: String,
    content: @Composable () -> Unit // OPEN for extension
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = title, style = MaterialTheme.typography.h6)
        content() // The card is "Closed for Modification" but anyone can add content
    }
}

```

---

### **3. LSP (Liskov Substitution) in Compose**

In Compose, this applies to the **Modifier** system. Every Composable should accept a `modifier: Modifier` as its first optional parameter. This ensures the Composable behaves like a standard Compose "View" and can be replaced or styled by the parent as expected.

---

### **4. ISP (Interface Segregation) in Compose**

Don't pass a giant "User" object if the Composable only needs a name. Pass only the data required.

- **Bad:** `fun UserAvatar(user: UserFullProfile)`
- **Good:** `fun UserAvatar(imageUrl: String)`

---

### **5. DIP (Dependency Inversion) in Compose**

Avoid hardcoding specific ViewModels inside deep UI components. Use **CompositionLocal** or **Parameter Injection** to provide dependencies. This allows you to pass "Mock ViewModels" into your **@Preview** blocks.

---

### **How It Works (Summary)**

1. **Extract Logic:** Move string formatting and data logic to the ViewModel (SRP).
2. **Hoist State:** Pass data down and events up (SRP/DIP).
3. **Use Slots:** Use the `@Composable () -> Unit` pattern to make layouts flexible (OCP).
4. **Stay Lean:** Pass only the primitive data needed for the UI (ISP).

---

### **Interview Keywords**

State Hoisting, Stateless vs. Stateful, Slot API, CompositionLocal, Reusability, Preview-friendly.

### **Interview Speak Paragraph**

> "In Jetpack Compose, SOLID principles are primarily applied through State Hoisting and the Slot API pattern. By separating a Composable into a 'Stateful' wrapper and a 'Stateless' content function, we follow the Single Responsibility Principle, making the UI easier to test and preview. Additionally, using Slot APIs allows our components to follow the Open/Closed Principle, where a layout can be extended with different content without modifying the underlying component's logic."

---

### **Common Interview Question/Angle**

**Q: "Why is it important to have Stateless Composables for SOLID?"**
**A:** "Stateless Composables are the key to the Single Responsibility Principle in Compose. Because they don't own their state, they are 'Pure Functions'—given the same input, they always produce the same UI. This makes them highly reusable across different screens and easily testable in Compose Previews without needing to mock complex ViewModels or Flows."

---

**Next Topic: SOLID in the Repository Pattern (Data Layer).**
This will cover how to handle multiple data sources (Room + Retrofit) while keeping your code clean.

**Would you like to proceed to the Repository Pattern notes?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
