---
layout: default
title: **Chapter 7: Jetpack Compose Testing**
parent: Phase7
nav_order: 5
---

Here are your in-depth study notes for the final topic of **Phase 7**.

This is one of the most common interview questions for modern Android roles: _"How do you test that clicking a button actually takes the user to the next screen in Compose?"_

---

# **Chapter 7: Jetpack Compose Testing**

## **Topic 7.5: Compose Navigation Testing**

### **1. The Problem: No more Fragments**

In the old world, you could check `activity.supportFragmentManager.findFragmentByTag(...)`.
In Compose, "Screens" are just composable functions swapped in and out of the view. There is no Fragment Manager to query.

- **Challenge:** The `NavController` is the source of truth, but it lives inside the Composable tree. How do we ask it _"What screen are we on?"_ from the test?

### **2. The Solution: `TestNavHostController**`

To test navigation, you **cannot** use the standard `rememberNavController()`.
You must use **`TestNavHostController`**.

- This is a special version of the controller designed for testing.
- It runs in memory and allows you to inspect the "Back Stack" (the history of screens).

**Dependency:**

```kotlin
androidTestImplementation("androidx.navigation:navigation-testing:2.7.x")

```

### **3. The Setup Pattern**

The trick is to create the Controller in the test, and pass it **down** into your `NavHost`.

**Your App Code (Must be testable):**

```kotlin
@Composable
fun MyAppNavHost(
    // Allow injecting the controller! Don't hardcode rememberNavController() inside.
    navController: NavHostController = rememberNavController()
) {
    NavHost(navController, startDestination = "home") {
        composable("home") { HomeScreen(onNavigateToDetails = { navController.navigate("details") }) }
        composable("details") { DetailScreen() }
    }
}

```

### **4. The Test Implementation**

Here is the step-by-step recipe.

```kotlin
@Test
fun testNavigation_homeToDetails() {
    // 1. Create the Test Controller
    val navController = TestNavHostController(ApplicationProvider.getApplicationContext())

    // 2. Set the UI Content
    composeTestRule.setContent {
        // Essential: Connect the controller to a LocalNavigator
        navController.navigatorProvider.addNavigator(ComposeNavigator())

        // Render your NavHost, passing the test controller
        MyAppNavHost(navController = navController)
    }

    // 3. Verify Start Destination
    // "currentBackStackEntry" tells us where we are right now
    assertThat(navController.currentBackStackEntry?.destination?.route).isEqualTo("home")

    // 4. Perform Action (Click Button)
    composeTestRule.onNodeWithText("Go to Details").performClick()

    // 5. Verify Navigation Happened
    assertThat(navController.currentBackStackEntry?.destination?.route).isEqualTo("details")
}

```

### **5. Testing Arguments (Deep Links)**

What if you navigate with arguments? `Maps("details/123")`?
You can inspect the arguments bundle in the test.

```kotlin
val route = navController.currentBackStackEntry?.destination?.route
val args = navController.currentBackStackEntry?.arguments

assertThat(route).isEqualTo("details/{userId}")
assertThat(args?.getString("userId")).isEqualTo("123")

```

### **6. Elite Tip: Asserting "Back" Navigation**

Don't just test forward; test backward.

```kotlin
// ... assume we are on 'details' screen ...

// 1. Press Back
Espresso.pressBack() // Or composeTestRule.activity.onBackPressed()

// 2. Assert we are back home
assertThat(navController.currentBackStackEntry?.destination?.route).isEqualTo("home")

```

### **7. Summary for Interviews**

> "To test navigation in Compose, I use the `TestNavHostController` from the navigation-testing library.
> I design my root `NavHost` composable to accept a `NavHostController` as a parameter (Dependency Injection). In my test, I instantiate the `TestNavHostController`, inject it into the composition, and then interact with the UI. Instead of checking for UI elements to verify the screen change, I inspect the source of truth: `navController.currentBackStackEntry?.destination?.route`. This confirms not just that the UI changed, but that the navigation graph state is correct."

---

**Congratulations! You have completed Phase 7.**
You are now proficient in testing the modern UI toolkit (Jetpack Compose).

**We are moving to Phase 8: Scenario-Based Solutions.**
This is essentially "The Interview Answer Key." We will tackle specific, hard questions asked by companies like Google, Meta, and Uber.

**Next Topic:** Scenario 1: **DB Migration Testing** (Ensuring data isn't lost during updates).
**Shall we proceed?**
