---
layout: default
title: CompositionLocal
parent: 2. State & Recomposition (The Core)
nav_order: 7
---

# CompositionLocal

Here are your notes for **Topic 2.7**.

---

## **Topic 2.7: CompositionLocal**

### **1. What It Is**

**CompositionLocal** is a tool for passing data down the UI tree **implicitly**, without having to pass it as a parameter through every single function.

- **Explicit (Standard):** Passing `color` from A -> B -> C -> D.
- **Implicit (CompositionLocal):** A sets the `color`. D just "grabs" it from the environment. B and C don't even know it exists.

This is exactly how `MaterialTheme`, `LocalContext`, and `LocalConfiguration` work.

### **2. Why It Exists (The "Prop Drilling" Problem)**

Imagine you have a `UserSession` object that your Profile Screen needs.

- **The Problem:** The Profile Screen is 10 layers deep. To get the object there, you have to pass it as a parameter through the Dashboard, the Settings, the Layout, the TabBar... even though none of those middle layers use it. This is called **Prop Drilling**, and it makes code messy and rigid.
- **The Solution:** You put the `UserSession` into a `CompositionLocal` at the very top. Any child, anywhere deep in the tree, can just reach out and grab `LocalUserSession.current`.

### **3. How It Works**

1. **Define:** You create a `CompositionLocal` variable (usually global).
2. **Provide:** You wrap your tree in a `CompositionLocalProvider` and give it a value.
3. **Consume:** A child calls `.current` to read the value.

### **4. staticCompositionLocalOf vs. compositionLocalOf (Vital)**

There are two ways to create one, and picking the wrong one kills performance.

#### **A. compositionLocalOf (Dynamic)**

- **Behavior:** If the value changes, **only the components that read it** will recompose.
- **Use Case:** Frequently changing data (e.g., IsLoading, Current User Name, Dark Mode toggle).
- **Performance:** Slightly higher overhead to track who is reading it.

#### **B. staticCompositionLocalOf (Static)**

- **Behavior:** If the value changes, **the entire content lambda** of the Provider recomposes (basically the whole tree).
- **Use Case:** Data that rarely or never changes (e.g., Dependency Injection objects, Analytics Loggers, Font Styles).
- **Performance:** Very fast to read because it doesn't track readers.

### **5. Example: Building a "Logged In User" Provider**

**Step 1: Define the Local**

```kotlin
data class User(val name: String, val age: Int)

// We define a global variable.
// We use 'compositionLocalOf' because user data might update.
val LocalUser = compositionLocalOf<User> { error("No user found!") }

```

**Step 2: Provide the Data (At the Root)**

```kotlin
@Composable
fun MyApp() {
    val currentUser = User("Alex", 30)

    // Everything inside this block can access LocalUser
    CompositionLocalProvider(LocalUser provides currentUser) {
        Dashboard()
    }
}

```

**Step 3: Consume the Data (Deep in the tree)**

```kotlin
@Composable
fun Dashboard() {
    // Note: Dashboard doesn't take 'User' as a parameter!
    SettingsScreen()
}

@Composable
fun SettingsScreen() {
    // We grab the user directly from the 'air' (the environment)
    val user = LocalUser.current
    Text("Hello, ${user.name}")
}

```

### **6. Interview Prep**

**Interview Keywords**
Prop Drilling, Implicit Data Flow, Scoped Providers, Ambient Context, Static vs Dynamic CompositionLocal, Tree-scoped Global.

**Interview Speak Paragraph**

> "CompositionLocal is the solution to the 'Prop Drilling' problem, where data needs to be passed through multiple layers of components that don't actually use it. It allows us to pass data implicitly down the UI tree. I use `compositionLocalOf` for data that might change frequently, like theme colors or user state, ensuring only the consuming components recompose. For static data like DI graphs or Analytics loggers, I use `staticCompositionLocalOf`, which is more performant for reads but causes a full tree recomposition if the value ever changes—which shouldn't happen for static data."

---

**Congratulations!** You have completed **Part 2: State & Recomposition**.
This was the heavy lifting. You now understand the _brain_ of Compose.

Next, we move to the _body_—building complex lists and grids.
**Are you ready to start Topic 3: Lists, Grids & UI Enhancements?**

---

## Navigation

â† Previous
