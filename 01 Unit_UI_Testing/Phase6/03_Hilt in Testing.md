---
layout: default
title: **Chapter 6: The Elite Level (System & Architecture)**
parent: Phase6
nav_order: 3
---

Here are your in-depth study notes for **Topic 6.3**.

This is the glue that holds everything together. You know _what_ to mock (Topic 3.1) and _how_ to mock the server (Topic 6.2), but **Hilt** (Dependency Injection) is what allows you to swap the Real Component for the Fake Component inside the running application.

---

# **Chapter 6: The Elite Level (System & Architecture)**

## **Topic 6.3: Hilt in Testing**

### **1. The Challenge with Dependency Injection (DI)**

In a production app using Hilt, you annotate a class with `@AndroidEntryPoint`, and Hilt magically injects the real `Repository`.

- **The Problem:** In a UI Test, Hilt still tries to inject the _Real_ Repository (connecting to the real server).
- **The Goal:** We need to tell Hilt: _"For this test, ignore the Production Module. Use this Test Module (with Fakes) instead."_

### **2. Setup: Dependencies & The Custom Runner**

Hilt doesn't work out-of-the-box with the standard `AndroidJUnitRunner`. You must replace the Application class with a Hilt-supported Test Application.

**Step A: Dependencies**

```kotlin
androidTestImplementation("com.google.dagger:hilt-android-testing:2.x.x")
kaptAndroidTest("com.google.dagger:hilt-android-compiler:2.x.x")

```

**Step B: The Custom Test Runner**
You must create this file once in your project. It forces the app to use `HiltTestApplication` when running tests.

**File:** `src/androidTest/java/.../CustomTestRunner.kt`

```kotlin
class CustomTestRunner : AndroidJUnitRunner() {
    override fun newApplication(
        cl: ClassLoader?,
        className: String?,
        context: Context?
    ): Application {
        // This is the Magic: Use HiltTestApplication instead of your real App class
        return super.newApplication(cl, HiltTestApplication::class.java.name, context)
    }
}

```

**Step C: Update build.gradle**
Tell Gradle to use your new runner.

```kotlin
android {
    defaultConfig {
        testInstrumentationRunner = "com.example.myapp.CustomTestRunner" // Your path
    }
}

```

### **3. The `@HiltAndroidTest` Annotation**

Every test class that uses Hilt must have these two components:

1. **Annotation:** `@HiltAndroidTest` at the top.
2. **Rule:** `HiltAndroidRule` inside.

```kotlin
@HiltAndroidTest // 1. Tells Hilt to generate a component for this test
class LoginTest {

    @get:Rule(order = 0) // 2. Must run BEFORE ActivityScenarioRule
    val hiltRule = HiltAndroidRule(this)

    @Before
    fun init() {
        hiltRule.inject() // 3. Triggers the injection
    }
}

```

### **4. Strategy A: Global Replacement (`@TestInstallIn`)**

Use this when you want to replace a dependency for **ALL** UI tests (e.g., swapping `AnalyticsService` for a dummy logger).

**The Production Module:**

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AnalyticsModule {
    @Provides
    fun provideAnalytics(): AnalyticsService = FirebaseAnalyticsService()
}

```

**The Test Module (In `src/androidTest/...`):**

```kotlin
@Module
@TestInstallIn(
    components = [SingletonComponent::class],
    replaces = [AnalyticsModule::class] // "Replace the Prod module with THIS"
)
object FakeAnalyticsModule {
    @Provides
    fun provideAnalytics(): AnalyticsService = FakeAnalyticsService()
}

```

_Result:_ Every time any test runs, Hilt injects `FakeAnalyticsService`.

### **5. Strategy B: Single-Test Replacement (`@UninstallModules`)**

Use this when you want to swap a dependency for **just one specific test class** (e.g., mocking the Repository for a specific error scenario).

1. **Uninstall:** Tell Hilt to forget the Production Module for this test.
2. **Re-bind:** Create a new Module inside the test class to provide the Mock.

```kotlin
@UninstallModules(RepositoryModule::class) // 1. Remove the Real Repo
@HiltAndroidTest
class LoginErrorTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    // 2. Create the Mock
    @BindValue
    @JvmField
    val mockRepo: UserRepository = mockk(relaxed = true)

    @Test
    fun testLoginFailure() {
        // 3. Train the Mock
        every { mockRepo.login() } returns false

        // 4. Run Test
        // Hilt will inject 'mockRepo' into the ViewModel because of @BindValue
        LoginRobot().clickLogin().assertErrorShown()
    }
}

```

- **`@BindValue`**: An incredibly powerful annotation. It takes the field in your test class and injects it anywhere in the app that asks for that type (`UserRepository`).

### **6. Summary for Interviews**

> "Integrating Hilt into UI tests requires setting up a custom `AndroidJUnitRunner` to load the `HiltTestApplication`.
> To swap production dependencies with Fakes, I use two strategies. For global replacements (like swapping real Analytics for a stub), I use `@TestInstallIn`. For test-specific replacements (like mocking a Repository to force an error), I use `@UninstallModules` to remove the production binding and `@BindValue` to inject a Mockk instance directly from the test class into the application graph."

---

**Congratulations! You have completed Phase 6.3.**

We have one final topic left in the entire roadmap. The metric managers love, and engineers misunderstand.

**Final Topic:** Topic 6.4: **Code Coverage (JaCoCo) & Flakiness Management**.

**Shall we proceed to the finish line?**
