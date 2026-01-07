---
layout: default
title: Shared Element Transitions
parent: 9. Animations
nav_order: 5
---

# Shared Element Transitions

Here are your notes for **Topic 9.5**.

---

## **Topic 9.5: Shared Element Transitions**

### **1. What It Is**

Shared Element Transitions (often called "Hero Animations") allow a UI element (like an image or text) to smoothly morph and move from one screen to another during navigation.

- **Screen A:** A small thumbnail of a shoe in a list.
- **Screen B:** The full-screen detail image of that same shoe.
- **The Transition:** Instead of Screen B sliding in over Screen A, the small shoe "flies" and expands to become the big shoe.

**Status:** This is a **new** feature in Compose (stabilized around Navigation 2.8.0 / Compose UI 1.7.0).

### **2. Why It Exists (Continuity)**

It creates a visual connection between two different states of the app. It tells the user: "This item you clicked is the _same_ item you are looking at now." It reduces cognitive load and feels premium.

### **3. How It Works (The Scope)**

To make this work, Compose needs to know which element on Screen A corresponds to which element on Screen B.

1. **`SharedTransitionLayout`:** The root container that manages the animation overlay.
2. **`AnimatedVisibilityScope`:** Usually provided by `NavHost` automatically.
3. **`Modifier.sharedElement()`:** The tag you put on _both_ composables (the start and the end) to link them.
4. **`sharedElementKey`:** The unique ID (e.g., "shoe_123") that matches the two elements.

### **4. Example: List to Detail Hero Animation**

**Setup:** You need the `SharedTransitionLayout` wrapping your NavHost.

```kotlin
@OptIn(ExperimentalSharedTransitionApi::class)
@Composable
fun AppNavGraph() {
    SharedTransitionLayout {
        val navController = rememberNavController()

        NavHost(navController, startDestination = "list") {

            // Screen 1: The List
            composable("list") {
                // Pass the 'animatedVisibilityScope' to the screen
                ListScreen(
                    onItemClick = { id -> navController.navigate("detail/$id") },
                    sharedTransitionScope = this@SharedTransitionLayout,
                    animatedVisibilityScope = this
                )
            }

            // Screen 2: The Detail
            composable("detail/{id}") { backStackEntry ->
                val id = backStackEntry.arguments?.getString("id")
                DetailScreen(
                    id = id!!,
                    sharedTransitionScope = this@SharedTransitionLayout,
                    animatedVisibilityScope = this
                )
            }
        }
    }
}

```

**The Components:**

```kotlin
@OptIn(ExperimentalSharedTransitionApi::class)
@Composable
fun ListScreen(
    onItemClick: (String) -> Unit,
    sharedTransitionScope: SharedTransitionScope,
    animatedVisibilityScope: AnimatedVisibilityScope
) {
    // We MUST be inside the scope to use the modifier
    with(sharedTransitionScope) {
        Row(modifier = Modifier.clickable { onItemClick("shoe_1") }) {
            Image(
                painter = painterResource(R.drawable.shoe),
                contentDescription = null,
                modifier = Modifier
                    .size(100.dp)
                    // THE MAGIC: Link this image with the key "shoe_1"
                    .sharedElement(
                        state = rememberSharedContentState(key = "image-shoe_1"),
                        animatedVisibilityScope = animatedVisibilityScope
                    )
            )
            Text("Nike Air Max")
        }
    }
}

@OptIn(ExperimentalSharedTransitionApi::class)
@Composable
fun DetailScreen(
    id: String,
    sharedTransitionScope: SharedTransitionScope,
    animatedVisibilityScope: AnimatedVisibilityScope
) {
    with(sharedTransitionScope) {
        Column {
            Image(
                painter = painterResource(R.drawable.shoe),
                contentDescription = null,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(300.dp)
                    // THE MAGIC: Use the SAME key "image-shoe_1"
                    .sharedElement(
                        state = rememberSharedContentState(key = "image-$id"),
                        animatedVisibilityScope = animatedVisibilityScope
                    )
            )
            Text("Details about the shoe...")
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`SharedTransitionLayout`, `SharedTransitionScope`, `Modifier.sharedElement`, `rememberSharedContentState`, Hero Animation, Key Matching, Spatial Continuity.

**Interview Speak Paragraph**

> "I implement Hero animations using the new Shared Element Transition APIs in Compose. This involves wrapping the navigation graph in a `SharedTransitionLayout`. The key mechanism is `Modifier.sharedElement`, which requires two scopes: the `SharedTransitionScope` (to manage the overlay) and the `AnimatedVisibilityScope` (from the NavHost, to know when screens are entering/exiting). By assigning the same unique key (e.g., 'image-123') to the thumbnail on the list screen and the full-size image on the detail screen, Compose automatically calculates the transform and animates the content seamlessly between the two destinations."

---

**Next Step:**
You have mastered Graphics and Animations.
Now, let's move to the final essential pillar: ensuring your code actually works.
**Are you ready to start Topic 10: Testing & Interoperability?**

---

## Navigation

â† Previous
