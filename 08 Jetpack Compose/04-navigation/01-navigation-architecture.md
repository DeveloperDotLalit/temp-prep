---
layout: default
title: Navigation Architecture
parent: 4. Navigation in Compose (Type-Safe)
nav_order: 1
---

# Navigation Architecture

Here are your notes for **Topic 4.1**.

---

# Topic 4: Navigation in Compose (Type-Safe)

## **Topic 4.1: Navigation Architecture**

### **1. What It Is**

Navigation in Compose is based on the **Single Activity Architecture**.
Instead of creating a new `Activity` for every screen (which is heavy and slow), you have **one** Activity.
The screens are just Composable functions. When you navigate, you aren't opening a new window; you are simply swapping one Composable (e.g., `HomeScreen`) for another (e.g., `ProfileScreen`) inside that same Activity.

### **2. Why It Exists (The "Fragment" Mess)**

- **Old Way:** You used Fragments or Activities. Fragments had complex lifecycles (`onCreate`, `onViewCreated`, `onActivityCreated`...) and communicating between them was painful.
- **New Way:** Navigation is just logic. You have a "Back Stack" (a pile of screens). When you go forward, you push a screen onto the stack. When you press back, you pop it off. The Navigation component handles the deep linking, back stack management, and screen transitions for you.

### **3. How It Works (The Trinity)**

The system relies on three main parts working together. Think of it like a **Taxi Ride**:

1. **`NavController` (The Driver):**

- This is the brain. It knows how to drive.
- You tell it: `navController.navigate("profile")`.
- It manages the back stack (history).

2. **`NavHost` (The Car):**

- This is the container on your screen where the content changes.
- It sits inside your Scaffold.
- It listens to the Driver. If the Driver goes to "profile", the NavHost clears the "Home" UI and draws the "Profile" UI.

3. **Navigation Graph (The Map):**

- This is the list of all valid destinations.
- You define it inside the `NavHost`. You say, "If the route is 'home', show `HomeScreen()`. If the route is 'settings', show `SettingsScreen()`."

### **4. Example: The Basic Setup**

```kotlin
@Composable
fun AppNavigation() {
    // 1. Create the Driver (Controller)
    // Always create this at the top level of your app logic.
    val navController = rememberNavController()

    // 2. The Car (NavHost)
    // "startDestination" is where we begin the journey.
    NavHost(navController = navController, startDestination = "home") {

        // 3. The Map (Graph Builder)
        // Define route 'home'
        composable(route = "home") {
            HomeScreen(
                // Pass the driver to the screen so it can drive elsewhere
                onNavigateToProfile = { navController.navigate("profile") }
            )
        }

        // Define route 'profile'
        composable(route = "profile") {
            ProfileScreen()
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Single Activity Architecture, Back Stack, `NavHost`, `NavController`, Destination, Route, Deep Links, Scoped ViewModels.

**Interview Speak Paragraph**

> "Compose Navigation follows the Single Activity Architecture pattern. Instead of using Fragments or Activities, we use a `NavHost` composable which acts as a placeholder container. We define a navigation graph inside this host that maps string routes (or type-safe objects) to specific Composable screens. The `NavController` acts as the orchestrator; it manages the back stack and handles the actual navigation actions. This setup decouples navigation logic from UI rendering and makes handling deep links and complex flows much simpler than the legacy FragmentManager approach."

---

**Next Step:**
Using strings like `"profile"` is dangerous. What if you make a typo?
Ready for **Topic 4.2: Type-Safe Navigation (Kotlin Serialization)**? This is the _new_ official standard (released late 2024) that kills string routes forever.

---

## Navigation

Next â†’
