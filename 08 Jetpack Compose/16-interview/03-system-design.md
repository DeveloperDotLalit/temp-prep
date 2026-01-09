---
layout: default
title: System Design
parent: 16. Interview Prep
nav_order: 3
---

# System Design

Here are your notes for **Topic 16.3: System Design**.

---

## **Topic 16.3: System Design (Design Systems & Navigation)**

### **1. Designing a Design System**

**The Situation:**
"You need to build a reusable UI library for your company so that 5 different teams can build apps that look consistent."

**Key Concepts:**

1. **Atomic Design:**

- **Atoms:** Colors, Typography, Spacing, Icons. (The foundation).
- **Molecules:** Input Fields (Label + Box + Error Text), Buttons (Text + Icon + Background).
- **Organisms:** DatePicker, NavigationBar, ProductCard.
- **Templates/Pages:** Complete screens.

2. **The Theme Object:**
   Instead of using `MaterialTheme` directly, wrap it in your own `AppTheme`. This allows you to add custom semantic colors (e.g., `successColor`, `warningColor`) that Material doesn't have.

```kotlin
object AppColors {
    val BrandPrimary = Color(0xFF6200EE)
    val Success = Color(0xFF4CAF50)
}

// Custom CompositionLocal to pass your custom system down the tree
val LocalAppColors = staticCompositionLocalOf { AppColors }

```

3. **Tokenization:**
   Never hardcode values. Use tokens.

- _Bad:_ `padding(16.dp)`
- _Good:_ `padding(AppTheme.spacing.medium)`

**Interview Answer:**

> "I approach design systems using Atomic Design principles. I start by defining the 'Atoms'—the immutable tokens for colors, typography, and spacing—in a central `AppTheme` object backed by `CompositionLocal`. This ensures that if the brand color changes, I only update one file. I then build 'Molecules' like buttons and input fields that consume these tokens. Crucially, I expose these components as stateless Composables, hoisting all state to the caller, which maximizes reusability across different feature modules."

---

### **2. Planning Navigation for a Multi-Module App**

**The Situation:**
"Your app has 3 modules: `:app`, `:feature:home`, and `:feature:profile`. The `:feature:home` module needs to navigate to the `:feature:profile` module, but they cannot depend on each other (circular dependency)."

**The Solution (The Navigation API Pattern):**
You cannot use direct class references (e.g., `ProfileScreen`). You must decouple navigation.

1. **The Common Module:** Create a `:core:navigation` module that everyone depends on.
2. **Route Definitions:** Define the routes as objects/interfaces in `:core:navigation`.

```kotlin
// In :core:navigation
interface NavigationDestination {
    val route: String
}

object ProfileDestination : NavigationDestination {
    override val route = "profile/{userId}"
    fun createRoute(userId: String) = "profile/$userId"
}

```

3. **The Navigator:** Create a `Navigator` class that exposes a `SharedFlow` of commands.
4. **Feature Integration:**

- The `HomeViewModel` calls `navigator.navigate(ProfileDestination.createRoute("123"))`.
- The `:app` module (which knows everyone) collects the flow and performs the actual navigation.

**Interview Answer:**

> "In a multi-module architecture, feature modules should not know about each other. To solve navigation, I implement a dependency inversion pattern. I create a `:core:navigation` module that contains route definitions and a `Navigator` interface. Feature modules depend on this core module to request navigation (e.g., 'Go to Profile'). The main `:app` module, which depends on all feature modules, observes these requests and executes the actual `NavController` commands. This keeps the features decoupled and allows me to refactor or remove modules without breaking the navigation graph."

---

### **3. Scaling State (State Holders)**

**The Situation:**
"You have a complex screen (e.g., a Video Editor). The ViewModel is 2000 lines long. How do you refactor it?"

**The Solution:**
Break the ViewModel into smaller **State Holders** (plain classes).

1. **ViewModel:** Becomes the coordinator. It just initializes the smaller classes.
2. **Sub-State Holders:**

- `TimelineStateHolder`: Manages the video timeline logic.
- `AudioStateHolder`: Manages volume and tracks.
- `EffectStateHolder`: Manages filters.

3. **Composition:** The UI observes the state from these smaller holders.

**Interview Answer:**

> "When a ViewModel becomes monolithic, I refactor by delegating logic to granular State Holders. For example, in a Video Editor, I would create a `TimelineManager` and an `AudioManager` class. These classes hold their own internal `StateFlows` and logic. The main ViewModel simply instantiates them and exposes their states to the UI. This follows the Single Responsibility Principle and makes the individual logic pieces much easier to unit test."

---

**This completes the Scenario-Based Design notes.**

You are now fully equipped to handle:

- **Coding:** "Build this list."
- **Theory:** "How does Compose work?"
- **Design:** "Architect this app."

**Would you like me to:**

1. **Generate the PDF now?**
2. **Quiz you** on one of these design scenarios?

---

## Navigation

â† Previous
