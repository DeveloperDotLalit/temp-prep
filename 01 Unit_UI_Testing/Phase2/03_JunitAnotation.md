---
layout: default
title: **Chapter 2: The Basics (JUnit & Assertions)**
parent: Unit & UI Testing: Phase 2: Project Setup & Gradle" and get your environment ready right now?
nav_order: 3
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Topic 2.3**.

This is the grammar of testing. Understanding these annotations is the difference between a test suite that is flaky and hard to debug, and one that is clean and predictable.

---

# **Chapter 2: The Basics (JUnit & Assertions)**

## **Topic 2.3: JUnit Annotations**

### **1. The Lifecycle of a Test Class**

A common misconception is that a Test Class is instantiated once, and then all test methods run. **This is false.**

- **The Reality:** JUnit creates a **new instance** of the Test Class for _every single_ `@Test` method.
- **Why?** To ensure isolation. If Test A changes a class variable, Test B won't see that change because Test B gets a brand new class instance.

### **2. Core Annotations (The "Big Three")**

#### **`@Test`**

- **Purpose:** Marks a function as a test case.
- **Behavior:** The Test Runner looks for this annotation to know which methods to execute.
- **Elite Tip:** In Kotlin, you can use backticks for function names to make them readable sentences.

```kotlin
@Test
fun `calculate_tax - negative income returns zero`() { ... }

```

- **Parameters (JUnit 4):**
- `expected`: Use this if the test _should_ throw an exception to pass.
- `@Test(expected = IllegalArgumentException::class)`

- `timeout`: Fails the test if it takes longer than X milliseconds.

#### **`@Before` (Setup)**

- **Purpose:** Executed **before** _every single_ `@Test` method in the class.
- **Use Case:** Resetting variables, creating fresh instances of the class under test, or initializing Mocks.
- **Why not just put it in the constructor?** While possible, `@Before` is explicit and handles initialization order better when inheritance is involved.
- _JUnit 5 equivalent:_ `@BeforeEach`

#### **`@After` (Teardown)**

- **Purpose:** Executed **after** _every single_ `@Test` method, regardless of whether the test passed or failed.
- **Use Case:** Closing database connections, stopping a mock server, or un-registering static listeners.
- **Elite Tip:** Rarely needed in pure Unit Tests (Memory is cleared when the instance dies). Critical in **Instrumented Tests** (to clear the database).
- _JUnit 5 equivalent:_ `@AfterEach`

### **3. Static Lifecycle Annotations (Global Setup)**

Sometimes you need to set up something expensive _once_ (like loading a heavy configuration file) and share it across all tests in that file.

#### **`@BeforeClass`**

- **Purpose:** Executed **once** before any tests run.
- **Constraint:** The method must be **static** (in Kotlin, inside a `companion object` annotated with `@JvmStatic`).
- **Risk:** Whatever you change here persists across all tests. This breaks isolation if you aren't careful.
- _JUnit 5 equivalent:_ `@BeforeAll`

#### **`@AfterClass`**

- **Purpose:** Executed **once** after all tests are finished.
- **Use Case:** Releasing expensive resources like a file handle or a database connection.
- _JUnit 5 equivalent:_ `@AfterAll`

### **4. The Visual Flow**

Imagine a test class with two tests: `testA()` and `testB()`. The execution flow is:

1. `@BeforeClass` (Static Setup)
2. `Constructor` (Instance 1) -> `@Before` -> **`testA()`** -> `@After`
3. `Constructor` (Instance 2) -> `@Before` -> **`testB()`** -> `@After`
4. `@AfterClass` (Static Teardown)

### **5. `@Rule` (The Superpower)**

This is specific to JUnit 4 but is **mandatory** for Android Architecture components.

- **Purpose:** Rules intercept test method calls and allow you to do things _around_ the test execution, or change how the test runs.
- **Common Android Rules:**
- `InstantTaskExecutorRule`: Forces LiveData to post values immediately on the current thread (Essential for ViewModel testing).
- `TestRule` / `ExternalResource`: Creating custom rules to set up complex environments (like a temporary folder).

```kotlin
// Example of a required rule for LiveData
@get:Rule
val instantTaskExecutorRule = InstantTaskExecutorRule()

```

### **6. `@Ignore`**

- **Purpose:** Tells the runner to skip this test.
- **Use Case:** You have a broken test that you can't fix right now, but you don't want to delete code.
- **Elite Tip:** Always add a reason string.
- `@Ignore("Blocked by Backend Ticket-123")`

- _JUnit 5 equivalent:_ `@Disabled`

### **7. Summary for Interviews**

> "JUnit manages the test lifecycle by instantiating a fresh class for every `@Test` method to ensure isolation. We use `@Before` to set up the 'Arrange' part of our tests (initializing mocks), and `@After` to clean up resources. For expensive global setup, we use `@BeforeClass`. In Android specifically, we heavily rely on `@Rule` to modify execution behavior, such as forcing background architecture components to run synchronously on the main thread."

---

**Would you like to proceed to Topic 2.4: "Assertions (Google Truth)" (Moving away from `assertEquals`)?**
