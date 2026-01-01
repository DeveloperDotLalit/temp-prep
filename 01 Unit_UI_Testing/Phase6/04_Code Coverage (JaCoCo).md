---
layout: default
title: **Chapter 6: The Elite Level (System & Architecture)**
parent: Unit & UI Testing: Phase 6: The Elite Level & Interview Prep
nav_order: 4
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for the final topic, **Topic 6.4**.

This topic covers the "meta" side of testing: measuring your success and maintaining sanity in your CI/CD pipeline.

---

# **Chapter 6: The Elite Level (System & Architecture)**

## **Topic 6.4: Code Coverage & Flakiness**

### **Part 1: Code Coverage (JaCoCo)**

#### **1. What is Code Coverage?**

Code coverage is a metric that tells you what percentage of your codebase was actually executed while your tests were running.

- **Line Coverage:** "Did the test hit Line 50?"
- **Branch Coverage:** "Did the test hit both the `if (true)` AND the `else` blocks?" (This is the more important metric).

#### **2. The Tool: JaCoCo**

**JaCoCo** (Java Code Coverage) is the industry standard for the JVM.

- **How it works:** It "instruments" your bytecode. It inserts tiny probes into your compiled classes. When a test runs, these probes report back: "I was touched!"
- **The Output:** A report (HTML/XML) showing green bars (covered) and red bars (missed) for every file.

#### **3. The "100% Coverage" Myth**

One of the biggest mistakes teams make is mandating "100% Coverage."

- **The Reality:** You can write a test that executes every line of code but asserts **nothing**. The coverage will be 100%, but the code could be completely broken.
- **The Elite Metric:** Aim for **80%**.
- **Cover:** Business Logic, ViewModels, Repositories, Utils.
- **Ignore:** Activities (mostly glue code), Dagger Modules, Generated Code.

#### **4. Setting up JaCoCo (Gradle)**

It requires a plugin in your `app/build.gradle`.

```kotlin
plugins {
    id("jacoco")
}

task("jacocoTestReport", JacocoReport::class) {
    dependsOn("testDebugUnitTest")

    // Tell JaCoCo where to look for source code and compiled classes
    classDirectories.setFrom(...)
    sourceDirectories.setFrom(...)
    executionData.setFrom(fileTree(buildDir).include("**/*.exec"))

    // Exclude generated files (Hilt, DataBinding) to avoid skewing stats
    classDirectories.setFrom(files(classDirectories.files.map {
        fileTree(it).exclude("**/R.class", "**/BuildConfig.*", "**/*_Factory.*")
    }))
}

```

---

### **Part 2: Managing Flaky Tests**

#### **1. What is a "Flaky" Test?**

A flaky test is a test that:

- Passes on your machine but fails on the CI server.
- Passes 9 times in a row, then fails the 10th time.
- **Danger:** Developers stop trusting the test suite. They start ignoring red builds ("Oh, that's just the flaky Login test, ignore it"). **This is the death of quality.**

#### **2. The Top 3 Causes & Fixes**

| Cause                             | The Symptom                                                                       | The Elite Fix                                                                                                           |
| --------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Concurrency / Race Conditions** | Test expects data to be ready, but background thread isn't done.                  | Use **IdlingResources** (UI) or `advanceUntilIdle()` (Unit). Never use `Thread.sleep()`.                                |
| **Shared State**                  | Test A creates a User. Test B expects an empty DB but finds the User from Test A. | Ensure `@After` or `@Before` cleans the database completely (Room `clearAllTables`). Use distinct Data Stores per test. |
| **External Dependencies**         | Network timeout, API 500 Error, Animation lag.                                    | Use **Hermetic Testing** (MockWebServer). Disable device animations.                                                    |

#### **3. The "Quarantine" Strategy**

If a test is flaky and you cannot fix it immediately:

1. **Do NOT ignore it silently.**
2. **Quarantine it:** Move it to a separate folder or annotate it with `@FlakyTest` (custom annotation).
3. **Exclude it from CI:** Configure your Pull Request check to run only "Stable" tests.
4. **Ticket it:** Create a JIRA ticket to fix the quarantined test. If it isn't fixed in 2 weeks, **delete the test**. No test is better than a flaky test.

#### **4. Interview Strategy (How to answer "How do you handle flakiness?")**

> "I approach flakiness with a Zero Tolerance policy. A flaky test destroys trust in the CI pipeline.
> First, I identify the root cause—usually synchronization issues or shared state. I replace `Thread.sleep()` with **IdlingResources** and ensure tests are **Hermetic** by mocking the network layer.
> If a test remains flaky, I strictly **quarantine** it using a `@FlakyTest` annotation so it doesn't block deployments, and I prioritize fixing it. I also use **JaCoCo** to ensure we have meaningful coverage (around 80%), focusing on branch coverage in business logic rather than raw line coverage in UI glue code."

---

### **Congratulations! You have completed the Roadmap.**

You have gone from "I don't know unit testing" to a complete, elite-level architectural understanding of the Android Testing Ecosystem.

**Here is your mastered tech stack:**

1. **Unit Logic:** JUnit 4 + Google Truth.
2. **Mocking:** Mockk (Strict/Relaxed, Slots).
3. **Concurrency:** Coroutines-Test (`runTest`, `StandardTestDispatcher`) + Turbine.
4. **Architecture:** MVVM Testing + Hilt Injection.
5. **UI:** Espresso + Robot Pattern + RecyclerViewActions.
6. **System:** IdlingResources + MockWebServer + JaCoCo.

**One final question for you:**
Do you want me to generate a **Single "Cheat Sheet" Code Block** that contains the templates for a `BaseTest`, a `Robot`, and a `DispatcherRule` all in one place for you to copy-paste into your future projects?
