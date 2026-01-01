---
layout: default
title: **Chapter 2: The Basics (JUnit & Assertions)**
parent: Unit & UI Testing: Phase2
nav_order: 1
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Topic 2.1: Project Setup & Gradle**.

This is the "Engine Room" of testing. If these dependencies are wrong, nothing works. We will configure the "Elite" stack we discussed: **JUnit 4, Mockk, Google Truth, and Coroutines Test**.

---

# **Chapter 2: The Basics (JUnit & Assertions)**

## **Topic 2.1: Project Setup & Gradle**

### **1. Dependency Scopes (Where does the code live?)**

In Gradle, you don't just "add a library." You must tell Gradle _when_ that library should be available.

- **`implementation`**: Available in your main app code (Production).
- **`testImplementation`**: Available **ONLY** in `src/test/java` (Local Unit Tests). This code is _stripped out_ when you build the release APK.
- **`androidTestImplementation`**: Available **ONLY** in `src/androidTest/java` (Instrumented/UI Tests).
- **`debugImplementation`**: Available only in debug builds. (Used for testing tools like the Fragment Testing library that need to interact with the manifest).

### **2. The "Elite" Testing Stack**

We are skipping the old defaults (standard Java assertions, Mockito) and using the modern standard:

1. **JUnit 4:** The standard Test Runner for Android (JUnit 5 requires complex setup in Android, so JUnit 4 remains the industry standard for now).
2. **Mockk:** The Kotlin-native mocking library.
3. **Google Truth:** Fluent assertions (Readability).
4. **Coroutines Test:** For controlling time and dispatchers.
5. **Arch Core Testing:** For testing LiveData/Architecture components.

### **3. Configuration: Kotlin DSL (`build.gradle.kts`)**

This is the modern standard for Android projects.

```kotlin
dependencies {
    // --- Local Unit Tests (src/test) ---
    // The Test Runner
    testImplementation("junit:junit:4.13.2")

    // Assertions (Fluent & Readable)
    testImplementation("com.google.truth:truth:1.1.5")

    // Mocking (The Kotlin Standard)
    testImplementation("io.mockk:mockk:1.13.8")

    // Coroutines & Flow Testing
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")

    // Architecture Components (LiveData logic)
    testImplementation("androidx.arch.core:core-testing:2.2.0")

    // --- Instrumented UI Tests (src/androidTest) ---
    // Android JUnit Runner
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test:runner:1.5.2")

    // Espresso (UI Interactions)
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")

    // Mockk for Android (allows mocking on device)
    androidTestImplementation("io.mockk:mockk-android:1.13.8")
}

```

### **4. Configuration: Groovy DSL (`build.gradle`)**

Use this if your project is older and hasn't migrated to Kotlin scripts yet.

```groovy
dependencies {
    // --- Local Unit Tests (src/test) ---
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'com.google.truth:truth:1.1.5'
    testImplementation 'io.mockk:mockk:1.13.8'
    testImplementation 'org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3'
    testImplementation 'androidx.arch.core:core-testing:2.2.0'

    // --- Instrumented UI Tests (src/androidTest) ---
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test:runner:1.5.2'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    androidTestImplementation 'io.mockk:mockk-android:1.13.8'
}

```

### **5. Critical Setup: The Test Runner**

Simply adding libraries isn't enough. You must tell the Android Build System which "Runner" to use to orchestrate the tests on the device.

Inside the `defaultConfig` block of your `build.gradle` (Module: app), you **must** have this line:

```kotlin
android {
    defaultConfig {
        // ... appId, minSdk etc.

        // This tells Android: "Use the AndroidX Runner, not the old default runner"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
}

```

- **Why is this needed?** Without this, your Espresso tests will fail to launch because the system won't know how to interpret the `@Test` annotations on the device.

### **6. Dependency Explanation (The "Why")**

- **`junit:junit`**: Provides the `@Test`, `@Before`, `@After` annotations. It is the engine that executes the methods.
- **`io.mockk:mockk`**: Allows us to create "fake" versions of complex objects. (e.g., `val repo = mockk<UserRepository>()`).
- **`com.google.truth:truth`**: Replaces `assertEquals(a, b)` with `assertThat(a).isEqualTo(b)`. It provides much better error messages when tests fail.
- _Bad Error:_ "Expected: 4, Actual: 5"
- _Truth Error:_ "Not true that <5> is equal to <4>" (Easier to read).

- **`kotlinx-coroutines-test`**: Provides `runTest` and `TestDispatcher`. It allows you to skip the 5-second delay in your code instantly during tests.
- **`androidx.arch.core:core-testing`**: Contains `InstantTaskExecutorRule`. This forces Architecture Components (like LiveData) to run instantly on the main thread, preventing "Looper not mocked" errors.

---

**Would you like to proceed to Topic 2.2: "Test Artifacts Folder Structure" (Where to put the files), or jump straight to 2.3: "JUnit Annotations"?**
