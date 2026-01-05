---
layout: default
title: Nested Navigation
parent: 4. Navigation in Compose (Type-Safe)
nav_order: 4
---

# Nested Navigation

Here are your notes for **Topic 4.4**.

---

## **Topic 4.4: Nested Navigation**

### **1. What It Is**

Nested Navigation is the practice of grouping a set of related screens into a **Sub-Graph**.
Think of it like organizing files on your computer. instead of having 100 files (screens) loose on the Desktop (Main Graph), you put related files into folders (Nested Graphs).

Common examples:

- **Auth Graph:** Login, Register, Forgot Password.
- **Onboarding Graph:** Welcome, Tutorial, Permissions.
- **Settings Graph:** Main Settings, Account, Notifications.

### **2. Why It Exists (Modularity & Scope)**

1. **Organization:** If your app has 50 screens, putting them all in one list makes the `NavHost` unreadable. Grouping them makes the code modular.
2. **Team Scaling:** One team can work on the "Checkout Flow" while another works on the "Profile Flow" without touching the same file.
3. **Scoped Logic:** You can define a `ViewModel` that lives only as long as the sub-graph exists. When the user exits the "Login Flow," the entire sub-graph and its shared data are cleared from memory.
4. **Stack Management:** It enables easy "Pop" operations. You can say "Pop everything in the Auth Graph" when the user successfully logs in.

### **3. How It Works**

You use the **`navigation`** builder function inside your `NavHost`.
This builder requires its own `startDestination` (which screen to show first when entering this folder) and a `route` (the name of the folder).

**Visual Structure:**

```text
Root NavHost
 ├── Home Screen
 ├── Profile Screen
 └── Auth Graph (Nested)
      ├── Login Screen (Start)
      ├── Sign Up Screen
      └── Forgot Password Screen

```

### **4. Example: The Authentication Flow**

Here is how you group Login and Sign Up into a single "Auth" module.

**1. Define the Routes (Type-Safe)**

```kotlin
// The "Folder" Name
@Serializable object AuthGraph

// The Screens inside
@Serializable object Login
@Serializable object SignUp

```

**2. The Navigation Graph**

```kotlin
NavHost(navController, startDestination = AuthGraph) {

    // Create the Nested Graph
    navigation<AuthGraph>(startDestination = Login) {

        // Screens belonging to this graph
        composable<Login> {
            LoginScreen(
                onSignUpClick = { navController.navigate(SignUp) }
            )
        }

        composable<SignUp> {
            SignUpScreen()
        }
    }

    // Other main screens outside the nest
    composable<Home> { HomeScreen() }
}

```

### **5. Interview Prep**

**Interview Keywords**
Sub-graph, Modularization, `navigation` builder, Scoped ViewModels, Encapsulation, Feature Modules.

**Interview Speak Paragraph**

> "I use Nested Navigation to organize my app into logical modules, such as separating the Authentication flow from the Main App flow. This involves using the `navigation` builder to create sub-graphs within the main `NavHost`. Beyond just code organization, this allows for **Scoped ViewModels**—where state can be shared across multiple screens in a specific flow (like a multi-step registration) and automatically cleared when that flow is popped. It also simplifies deep linking and popping entire sections of the back stack at once."

---

**Next Step:**
You have the flows set up. Now, how do we handle the standard "Tabs" at the bottom of the screen?
Ready for **Topic 4.5: Bottom Navigation & Rail**? This integrates the NavController with the visible UI bars.

---

## Navigation

â† Previous
Next â†’
