---
layout: default
title: Bottom Navigation & Rail
parent: 4. Navigation in Compose (Type-Safe)
nav_order: 5
---

# Bottom Navigation & Rail

Here are your notes for **Topic 4.5**.

---

## **Topic 4.5: Bottom Navigation & Rail**

### **1. What It Is**

These are the top-level navigation patterns for your app.

- **Bottom Navigation (`NavigationBar`):** The standard row of 3-5 icons at the bottom of the screen. Best for **Phones** (Portrait).
- **Navigation Rail (`NavigationRail`):** A vertical side bar of icons. Best for **Tablets** or Phones in **Landscape**.

### **2. Why It Exists (Thumb Reachability)**

- **Bottom Bar:** On a phone, your thumb is at the bottom. It's the most ergonomic place for main tabs.
- **Rail:** On a tablet, the screen is too wide. A bottom bar stretches the icons too far apart, looking ugly. A side rail keeps icons grouped and accessible near your thumb while holding the device.
- **Adaptive UI:** The goal is to swap between these two automatically depending on the screen size (Window Size Class).

### **3. How It Works**

#### **A. The Structure**

You usually define a `Scaffold`.

- **Bottom Bar:** Goes into the `bottomBar` slot.
- **Rail:** Is tricky. `Scaffold` doesn't have a "leftBar" slot. You usually wrap the Scaffold in a `Row` and put the Rail _next_ to the Scaffold.

#### **B. The "Magic 4" Flags (Vital for Tabs)**

When navigating between tabs (Home -> Search -> Home), you don't want to "push" a new Home screen every time. You want to **restore** the old one (keep scroll position, typed text, etc.).
You need these 4 flags in your `onClick`:

1. **`popUpTo(startDestination)`:** Clears the stack so pressing Back doesn't cycle through 50 tab switches.
2. **`saveState = true`:** Saves the state of the screen you are leaving (e.g., scroll position).
3. **`launchSingleTop = true`:** Avoids creating a duplicate copy if you tap "Home" while already on Home.
4. **`restoreState = true`:** Restores the saved state of the screen you are entering.

### **4. Example: The Manual Way (Bar + Rail)**

**1. Define Tabs**

```kotlin
@Serializable object Home
@Serializable object Search
// List of your tabs
val tabs = listOf(Home, Search)

```

**2. The Navigation Logic (The Magic Flags)**

```kotlin
fun navigateToTab(navController: NavController, route: Any) {
    navController.navigate(route) {
        // 1. Pop up to the start destination of the graph to
        // avoid building up a large stack of destinations
        popUpTo(navController.graph.findStartDestination().id) {
            // 2. Save state of the popped destination
            saveState = true
        }
        // 3. Avoid multiple copies of the same destination
        launchSingleTop = true
        // 4. Restore state when re-selecting a previously selected item
        restoreState = true
    }
}

```

**3. The UI Integration**

```kotlin
Scaffold(
    bottomBar = {
        // Only show on Phones
        if (isPhone) {
            NavigationBar {
                tabs.forEach { dest ->
                    NavigationBarItem(
                        selected = currentRoute == dest,
                        onClick = { navigateToTab(navController, dest) },
                        icon = { /* Icon */ }
                    )
                }
            }
        }
    }
) { innerPadding ->
    // If Tablet, we use a Row to put Rail on the left
    Row(modifier = Modifier.padding(innerPadding)) {
        if (isTablet) {
            NavigationRail { /* Similar items logic */ }
        }

        // The NavHost fills the rest of the space
        NavHost(navController, startDestination = Home) {
            composable<Home> { HomeScreen() }
            composable<Search> { SearchScreen() }
        }
    }
}

```

### **5. Pro Tip: `NavigationSuiteScaffold` (The Modern Way)**

Google recently released a new component that handles **all of the above automatically**. It detects if the app is on a phone or tablet and swaps the Bar for the Rail for you.

```kotlin
NavigationSuiteScaffold(
    navigationSuiteItems = {
        item(
            selected = true,
            onClick = { /* navigate */ },
            icon = { Icon(...) }
        )
    }
) {
    // Your NavHost goes here
}

```

### **6. Interview Prep**

**Interview Keywords**
`NavigationBar` vs `NavigationRail`, `saveState`/`restoreState`, Multiple Back Stacks, `launchSingleTop`, `popUpTo` (inclusive), `NavigationSuiteScaffold`.

**Interview Speak Paragraph**

> "For top-level navigation, I typically implement a `NavigationBar` for compact screens and a `NavigationRail` for expanded screens to ensure ergonomics. The critical part of tab navigation is managing the back stack correctly. When navigating between tabs, I use the `Maps()` builder with four specific flags: `popUpTo(startDestination)` to prevent an infinite back stack, `launchSingleTop` to avoid duplicates, and crucially, `saveState` and `restoreState`. These ensure that when a user switches tabs, their scroll position and input state are preserved, mimicking the behavior users expect from a native Android app."

---

### **Recommended Video**

For a clear visual guide on implementing adaptive navigation that switches between a bottom bar and a side rail, this video is excellent:
[Automatically Adjust Navigation Based On Screen Size With NavigationSuiteScaffold](https://www.youtube.com/watch?v=u8vQgmgf3X4)

_I chose this video because it focuses on the `NavigationSuiteScaffold`, which is the modern, "Zero to Hero" way to handle this complexity without writing manual `if-else` layout logic._

---

**Next Step:**
You can navigate, but can you handle the "Outside World"?
Ready for **Topic 4.6: Deep Links [Added]**? This is how you open a specific screen from a web link (e.g., `myapp.com/post/123`).

---

## Navigation

â† Previous
Next â†’
