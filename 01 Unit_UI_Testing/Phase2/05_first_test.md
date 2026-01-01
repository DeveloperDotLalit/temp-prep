---
layout: default
title: **Chapter 2: The Basics (JUnit & Assertions)**
parent: Unit & UI Testing: Phase 2: Project Setup & Gradle" and get your environment ready right now?
nav_order: 5
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Topic 2.5**.

This is the moment where theory becomes practice. We will write a "Pure Logic" test. This is the simplest type of test because it has zero Android dependencies—just pure Kotlin code.

---

# **Chapter 2: The Basics (JUnit & Assertions)**

## **Topic 2.5: Writing Your First Test**

### **1. The Scenario**

To practice, we need a piece of logic to test. We won't test a ViewModel yet (that requires mocking). We will test a **Utility Object**.

**Feature:** A user registration form.
**Requirement:** We need a function to validate the input.

- Username cannot be empty.
- Password must be at least 2 characters long.
- "Confirm Password" must match "Password".

### **2. Step 1: The Production Code**

Create this file in your `src/main/java/...` folder.

**File:** `RegistrationUtil.kt`

```kotlin
object RegistrationUtil {

    /**
     * Validates the registration input.
     * Returns TRUE if valid, FALSE if invalid.
     */
    fun validateRegistrationInput(
        username: String,
        password: String,
        confirmedPassword: String
    ): Boolean {

        // Rule 1: Empty Username
        if (username.isEmpty()) {
            return false
        }

        // Rule 2: Password matches Confirm Password
        if (password != confirmedPassword) {
            return false
        }

        // Rule 3: Password Length
        if (password.length < 2) {
            return false
        }

        // If all checks pass
        return true
    }
}

```

### **3. Step 2: Creating the Test File**

1. Open `RegistrationUtil.kt`.
2. Place your cursor on the class name `RegistrationUtil`.
3. Press `Ctrl + Shift + T` (Windows) or `Cmd + Shift + T` (Mac).
4. Select **Create New Test...**
5. **Testing Library:** JUnit 4.
6. **Destination:** Select the folder `.../src/test/java/...` (NOT `androidTest`).
7. Click **OK**.

You now have an empty class `RegistrationUtilTest`.

### **4. Step 3: Writing the Test Cases**

We will write three tests to cover the "Happy Path" (Success) and "Edge Cases" (Failures).

**File:** `src/test/java/.../RegistrationUtilTest.kt`

```kotlin
import com.google.truth.Truth.assertThat // Import the Truth entry point
import org.junit.Test // Import the JUnit annotation

class RegistrationUtilTest {

    // TEST CASE 1: The Happy Path (Everything is correct)
    @Test
    fun `validateInput - valid username and matching passwords - returns true`() {
        // 1. ARRANGE (Given)
        val result = RegistrationUtil.validateRegistrationInput(
            username = "GeminiUser",
            password = "123",
            confirmedPassword = "123"
        )

        // 2. ACT (When) -> (Merged with Arrange usually for simple pure functions)

        // 3. ASSERT (Then)
        assertThat(result).isTrue()
    }

    // TEST CASE 2: Edge Case (Empty Username)
    @Test
    fun `validateInput - empty username - returns false`() {
        val result = RegistrationUtil.validateRegistrationInput(
            username = "",
            password = "123",
            confirmedPassword = "123"
        )

        assertThat(result).isFalse()
    }

    // TEST CASE 3: Edge Case (Passwords do not match)
    @Test
    fun `validateInput - passwords do not match - returns false`() {
        val result = RegistrationUtil.validateRegistrationInput(
            username = "GeminiUser",
            password = "123",
            confirmedPassword = "456" // Different
        )

        assertThat(result).isFalse()
    }

    // TEST CASE 4: Edge Case (Password too short)
    @Test
    fun `validateInput - password less than 2 digits - returns false`() {
        val result = RegistrationUtil.validateRegistrationInput(
            username = "GeminiUser",
            password = "1",
            confirmedPassword = "1"
        )

        assertThat(result).isFalse()
    }
}

```

### **5. Step 4: Running the Tests**

You have three ways to run these tests:

1. **Gutter Icons:** Click the green "Play" triangle next to the class name (runs all tests) or next to a specific function (runs just that test).
2. **Right Click:** Right-click the file in the Project view and select "Run 'RegistrationUtilTest'".
3. **Keyboard Shortcut:** `Ctrl + Shift + F10` (Windows) / `Ctrl + Shift + R` (Mac).

### **6. Understanding the Output**

- **Green Bar:** Success. All assertions passed.
- **Red Bar:** Failure.
- Click on the failing test in the console.
- Look at the "Cause" section.
- _Example:_ `expected: true, but was: false`.

### **7. The "Red-Green-Refactor" Cycle (TDD Preview)**

Notice how we wrote the code first, then the test? In **Test Driven Development (TDD)**, you reverse this:

1. **Red:** Write the test _before_ the logic exists (it fails immediately/doesn't compile).
2. **Green:** Write the _minimum_ amount of code in `RegistrationUtil` to make the test pass.
3. **Refactor:** Clean up the code knowing the test ensures you didn't break it.

### **8. Summary for Interviews**

> "In a basic unit test, we define a scenario using the AAA pattern. For `RegistrationUtil`, I would Arrange the inputs (username/password), Act by calling the validate function, and Assert the boolean result using Google Truth. Since this is a pure logic class, these tests run instantly on the JVM without any mocking required."

---

**Congratulations! You have completed Phase 2.**
You now know how to configure a project, where to put files, and how to write basic logical tests.

**We are now entering Phase 3: Intermediate Unit Testing (Mockk & Architecture).**
This is where it gets real. We will learn how to test code that isn't "pure"—code that depends on other classes.

**Next Topic:** Phase 3.1: **Fakes vs. Mocks** (The conceptual difference).
**Shall we proceed?**
