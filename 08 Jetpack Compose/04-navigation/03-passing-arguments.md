---
layout: default
title: Passing Arguments
parent: 4. Navigation in Compose (Type-Safe)
nav_order: 3
---

# Passing Arguments

Here are your notes for **Topic 4.3**.

---

## **Topic 4.3: Passing Arguments**

### **1. What It Is**

This topic covers how to send data from one screen to another (e.g., clicking a user in a list -> sending their ID to the Profile screen) and how to return data back (e.g., selecting a filter -> returning the choice to the previous list).

### **2. Why It Exists (The "Single Source of Truth" Rule)**

- **The Golden Rule:** You should **not** pass complex objects (like a full `User` object with bio, photo, address) as navigation arguments.
- **Why?**

1. **Size Limits:** Android Bundles have a size limit (1MB). If the object is too big, the app crashes (`TransactionTooLargeException`).
2. **Stale Data:** If you pass a `User` object, and the user edits their profile on the next screen, the previous screen still holds the old object.

- **The Best Practice:** Pass a **Minimal ID** (e.g., `userId: String`). Let the destination screen fetch the fresh data from the Repository using that ID.

### **3. How It Works**

#### **A. Passing Data Forward (Type-Safe)**

Using the `@Serializable` method (Topic 4.2), passing data is just passing a constructor parameter.

- **Required:** `data class Profile(val id: String)`
- **Optional:** `data class Search(val query: String? = null)`. By making it nullable and providing a default, Navigation treats it as optional.

#### **B. Returning Data Back (`savedStateHandle`)**

To send data back (like `startActivityForResult`), we use the `SavedStateHandle` of the BackStackEntry.

1. **Screen B (Selection):** Sets a value in the `previousBackStackEntry`.
2. **Screen A (Listener):** Observes that value in the `currentBackStackEntry`.

### **4. Example: The Full Flow**

**Scenario:** List Screen -> Click Item -> Detail Screen.

**1. The Argument Object**

```kotlin
@Serializable
data class UserDetail(val userId: String) // Only passing the ID!

```

**2. The Navigation Graph**

```kotlin
composable<UserDetail> { backStackEntry ->
    // Extract ID safely
    val args = backStackEntry.toRoute<UserDetail>()

    // Pass ID to ViewModel to load full data
    val viewModel = hiltViewModel<DetailViewModel>()
    // (In real app, ViewModel usually reads SavedStateHandle directly, but this works too)
    LaunchedEffect(args.userId) { viewModel.loadUser(args.userId) }

    DetailScreen(viewModel)
}

```

**3. Returning a Result (e.g., Date Picker)**

```kotlin
// IN THE DESTINATION SCREEN (Screen B)
Button(onClick = {
    navController.previousBackStackEntry
        ?.savedStateHandle
        ?.set("selected_date", "2025-01-01") // Set the result
    navController.popBackStack()
}) { Text("Confirm Date") }

// IN THE ORIGIN SCREEN (Screen A)
val result = navController.currentBackStackEntry
    ?.savedStateHandle
    ?.getLiveData<String>("selected_date")
    ?.observeAsState()

Text("Selected: ${result.value}")

```

### **5. Interview Prep**

**Interview Keywords**
`SavedStateHandle`, Single Source of Truth, TransactionTooLargeException, Minimal Arguments, `previousBackStackEntry`, Nullable Arguments.

**Interview Speak Paragraph**

> "When passing arguments in Compose Navigation, I adhere to the principle of 'Minimal IDs.' I avoid passing complex Parcelable objects because they can exceed the Bundle size limit and lead to data synchronization issues. Instead, I pass a unique ID (like a generic `userId`) and have the destination screen's ViewModel fetch the latest data from the repository. For returning results—like picking a filter or a date—I use the `SavedStateHandle` associated with the `previousBackStackEntry`. This allows the calling screen to observe the result via a standard LiveData or State flow without complex coupling."

---

**Next Step:**
We can go A -> B, but what if we have A -> B -> C -> D and want to group them?
Ready for **Topic 4.4: Nested Navigation**? This is essential for features like "Login Flow" or "Checkout Flow".

---

## Navigation

â† Previous
Next â†’
