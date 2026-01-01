---
layout: default
title: **Chapter 3: Intermediate Unit Testing (Mockk & Architecture)**
parent: Phase3
nav_order: 1
---

Here are your in-depth study notes for **Phase 3, Topic 3.1**.

This concept is the gateway to testing real-world architecture. You cannot test a ViewModel without understanding this, because ViewModels depend on Repositories, and Repositories depend on Databases. We need to replace those heavy dependencies.

---

# **Chapter 3: Intermediate Unit Testing (Mockk & Architecture)**

## **Topic 3.1: Fakes vs. Mocks (Test Doubles)**

### **1. The Umbrella Term: "Test Double"**

Just as a movie star has a "Stunt Double" to do the dangerous work, your production classes have "Test Doubles" to handle the unit tests.

- **Problem:** Your `LoginViewModel` needs a `UserRepository` to work. The real `UserRepository` needs a network connection.
- **Solution:** Pass a "Double" of the Repository to the ViewModel. It _looks_ like the Repository, but it's safe and fast.

There are many types of doubles (Dummies, Stubs, Spies), but in modern Android development, we focus on two: **Fakes** and **Mocks**.

### **2. What is a Fake?**

A **Fake** is a working implementation of an interface that takes a shortcut. It actually has logic inside it, but it's simplified logic.

- **Mechanism:** You manually create a new class (e.g., `FakeUserRepository`) that implements the `UserRepository` interface.
- **Behavior:** Instead of hitting a database, it might just save users into a simple `HashMap` or `List` in memory.
- **Pros:** It behaves very realistically. If you save user "A", and then try to get user "A", it works. It maintains state.
- **Cons:** You have to write and maintain the code for the Fake class yourself. If the interface changes, you must update the Fake.

**Example of a Fake:**

```kotlin
// The Contract
interface UserRepository {
    fun getAllUsers(): List<User>
    fun saveUser(user: User)
}

// The Fake Implementation (Written by YOU)
class FakeUserRepository : UserRepository {
    private val users = mutableListOf<User>() // In-memory database

    override fun getAllUsers(): List<User> {
        return users
    }

    override fun saveUser(user: User) {
        users.add(user)
    }
}

```

### **3. What is a Mock?**

A **Mock** is an object created by a library (like Mockk or Mockito) where you pre-program specific behavior for specific calls. It has no logic or state unless you tell it to.

- **Mechanism:** You ask the library: "Give me an object that looks like `UserRepository`."
- **Behavior:** By default, it does nothing. You must "teach" it: _"If someone calls `getAllUsers()`, return this empty list."_
- **Pros:** extremely fast to set up. No extra classes to write. Perfect for verifying behavior (e.g., "Was `saveUser` called exactly once?").
- **Cons:** It doesn't remember things. If you tell it to return "Success" for a login, it returns "Success" even if you send the wrong password, because it has no logic—it just follows the script.

**Example of a Mock (using Mockk):**

```kotlin
// Created instantly in your test file
val mockRepo = mockk<UserRepository>()

// The Script (Teaching the mock)
every { mockRepo.getAllUsers() } returns listOf(User("Gemini"))

```

### **4. Visual Comparison**

- **Fake:** Like a **lightweight engine**. It runs, consumes fuel, and spins the wheels, but it's smaller than the real engine.
- **Mock:** Like a **cardboard cutout of an engine**. It looks right from the outside, but there is nothing inside. You just paste a sticker on it saying "Speed = 100mph".

### **5. When to use Which? (The Elite Strategy)**

This is where beginners get confused. Here is the rule of thumb for Android:

- **Use MOCKS for:**
- **Behavior Verification:** When you want to check _if_ a function was called. (e.g., "Did the ViewModel call `analytics.logEvent()`?").
- **External Services:** Permission handlers, Analytics, Navigation Controllers.
- **One-off scenarios:** When you just need a function to return an Exception to test error handling.

- **Use FAKES for:**
- **Data Layer / Repositories:** This is the big shift. Google now recommends using Fakes for Repositories instead of Mocks.
- **Why?** Because Repositories have complex state. Mocking every single outcome of a database (insert, then delete, then select) leads to massive, messy test setups. A `FakeRepository` backed by a `HashMap` behaves correctly automatically.

### **6. Summary for Interviews**

> "A **Fake** is a lightweight, working implementation of an interface (usually using an in-memory list) that behaves like the real thing but is faster. A **Mock** is a synthetic object created by a framework where we script specific inputs and outputs.
> In my architecture, I prefer using **Fakes for the Data Layer** (Repositories) because they maintain state and make tests more realistic/readable. I use **Mocks for the Service Layer** (Analytics, Observers) where I care more about verifying interactions ('Did this method get called?') rather than state."

---

**Would you like to proceed to Topic 3.2: "Introduction to Mockk" (Setting up the library and syntax)?**
