---
layout: default
title: "**Chapter 3: Intermediate Unit Testing (Mockk & Architecture)**"
parent: "Unit & UI Testing: Phase 3: Intermediate Unit Testing (Mockk & Architecture)"
nav_order: 3
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Topic 3.2**.

We are now entering the "Tooling" phase. You have likely heard of **Mockito** in the Java world. In the Kotlin world, **Mockk** is the king.

---

# **Chapter 3: Intermediate Unit Testing (Mockk & Architecture)**

## **Topic 3.2: Introduction to Mockk**

### **1. Why Mockk? (vs. Mockito)**

For years, Android developers used Mockito. However, Mockito is a Java library.

- **The Kotlin Problem:** In Kotlin, all classes and functions are `final` by default. Mockito cannot mock `final` classes without complex configuration. Kotlin also has static extension functions and Coroutines, which Mockito struggles with.
- **The Solution:** **Mockk** was built specifically for Kotlin.
- It uses Kotlin DSL (Lambda syntax).
- It mocks `final` classes, objects, and extension functions out of the box.
- It has first-class support for Coroutines (`coEvery`, `coVerify`).

### **2. The "Trinity" of Mockk Syntax**

Using Mockk revolves around three distinct steps. Memorize these keywords.

#### **A. Creation (`mockk`)**

This creates the fake object.

```kotlin
// Create a mock of the UserRepository interface/class
val userRepo = mockk<UserRepository>()

```

#### **B. Stubbing (`every`)**

This is the "Training" phase. You tell the mock what to do when a specific method is called. If you don't stub a method and try to call it, Mockk will throw an error (unless it's a "relaxed" mock).

- **Syntax:** "Every time _this_ happens, return _that_."

```kotlin
// When getAllUsers() is called, return a specific list
every { userRepo.getAllUsers() } returns listOf(User("A"), User("B"))

// You can also throw exceptions
every { userRepo.saveUser(any()) } throws RuntimeException("Database Error")

```

#### **C. Verification (`verify`)**

This is the "Checking" phase. You assert that a specific interaction actually happened.

- **Syntax:** "Verify that _this_ happened."

```kotlin
// Check that saveUser was called exactly once
verify(exactly = 1) { userRepo.saveUser(any()) }

// Check that deleteUser was NEVER called
verify(exactly = 0) { userRepo.deleteUser(any()) }

```

### **3. Argument Matching (`any()`)**

Often, you don't care exactly _what_ argument was passed, just that _some_ argument was passed.

- **`any()`**: A wildcard matcher.

```kotlin
// I don't care what User object is passed, just return true
every { userRepo.saveUser(any()) } returns true

```

- _Warning:_ If you are strict, pass the exact object: `every { userRepo.saveUser(expectedUser) } returns true`.

### **4. Strict vs. Relaxed Mocks**

This is a critical configuration option.

#### **Strict Mock (Default)**

```kotlin
val strictMock = mockk<UserRepository>()

```

- **Behavior:** If you call a function on this mock that you haven't explicitly defined with `every { ... }`, the test **crashes**.
- **Use Case:** When you want to be absolutely sure you know everything your code is doing.

#### **Relaxed Mock**

```kotlin
val relaxedMock = mockk<UserRepository>(relaxed = true)

```

- **Behavior:** If you call a function you haven't defined:
- If it returns `Unit` (void), it does nothing and proceeds.
- If it returns a primitive (Int, Boolean), it returns a default (0, false).
- If it returns an Object, it tries to return a simple mock of that object.

- **Use Case:** Great for things like **Analytics** or **Loggers** where you call 20 methods but only care about testing 1 of them. You don't want to write 19 dummy stubbings.

### **5. Putting it Together: A Simple Example**

Let's test a `UserProfileViewModel` that relies on a `UserRepository`.

**The Class to Test (ViewModel):**

```kotlin
class UserProfileViewModel(private val repo: UserRepository) {
    fun getUserName(): String {
        val user = repo.getUser() // Dependency call
        return user.name.uppercase() // Logic
    }
}

```

**The Test:**

```kotlin
@Test
fun `getUserName - returns uppercase name`() {
    // 1. ARRANGE
    val mockRepo = mockk<UserRepository>()
    // Teach the mock to return a specific User when getUser() is called
    every { mockRepo.getUser() } returns User("gemini")

    val viewModel = UserProfileViewModel(mockRepo)

    // 2. ACT
    val result = viewModel.getUserName()

    // 3. ASSERT
    assertThat(result).isEqualTo("GEMINI")

    // Optional: Verify the repo was actually touched
    verify { mockRepo.getUser() }
}

```

### **6. Summary for Interviews**

> "I use **Mockk** because it is designed for Kotlin. It handles final classes and coroutines natively. The workflow consists of creating the mock (`mockk`), stubbing the behavior (`every { ... } returns ...`), and verifying the interaction (`verify { ... }`). While strict mocks ensure we define all behavior explicitly, I sometimes use `relaxed = true` for auxiliary dependencies like Analytics to reduce boilerplate code."

---

**Would you like to proceed to Topic 3.3: "Argument Capturing (Slots)" (How to inspect data passed to a mock)?**
