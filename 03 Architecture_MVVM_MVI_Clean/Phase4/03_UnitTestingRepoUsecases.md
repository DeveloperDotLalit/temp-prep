---
layout: default
title: Unittestingrepousecases
parent: Phase4
nav_order: 3
---

Here are your focused notes on **Unit Testing Use Cases & Repositories**.

This is often the easiest part of testing because these layers usually have no Android UI code.

---

### **Topic: Unit Testing Use Cases & Repositories**

#### **What It Is**

This involves testing the "invisible" parts of your app.

- **Testing Use Cases:** Verifying that your business rules (Logic) are correct. (e.g., "Does the math work?", "Does the validator reject bad emails?").
- **Testing Repositories:** Verifying that your data decisions are correct. (e.g., "If the database is empty, did we call the API?", "Did we map the API response to the correct Domain model?").

#### **Why It Exists (The Problem)**

1. **Pure Logic Verification:** You don't want to wait until the user sees a "0.00" price on the checkout screen to realize your tax calculation formula is wrong. You want to catch that bug in the code phase.
2. **No Emulator Needed:** Since Use Cases and Repositories (usually) don't touch `View` or `Context`, these tests run on the JVM (your computer). They are blazing fast.
3. **Boundary Protection:** It ensures that if the API sends garbage data, your Repository filters it out before it crashes the app.

#### **How It Works**

The strategy is **Isolation**.

- **For Use Cases:** We treat them like simple math functions. Input -> [Black Box] -> Output. We don't care about the database here; we just mock the return value.
- **For Repositories:** We mock the **Data Sources** (API and DAO). We verify that the Repository calls the right source.

#### **Example 1: Testing a Use Case (Business Logic)**

**Scenario:** A `ValidatePasswordUseCase`. Rule: Password must be > 5 chars.

```kotlin
@Test
fun `when password is short, return false`() {
    // 1. Arrange
    val useCase = ValidatePasswordUseCase()

    // 2. Act
    val result = useCase("123") // Too short

    // 3. Assert
    assertFalse(result)
}

@Test
fun `when password is valid, return true`() {
    val result = useCase("123456")
    assertTrue(result)
}

```

#### **Example 2: Testing a Repository (Data Flow)**

**Scenario:** If local data exists, return it. If not, call API.

```kotlin
@Test
fun `when local data is empty, fetch from remote`() = runTest {
    // 1. Arrange: Create Mocks
    val mockDao = mockk<UserDao>()
    val mockApi = mockk<UserApi>()
    val repo = UserRepository(mockDao, mockApi)

    // Setup: Local DB is empty, API returns User
    coEvery { mockDao.getUser() } returns null
    coEvery { mockApi.fetchUser() } returns NetworkUser("John")

    // 2. Act
    val result = repo.getUser()

    // 3. Assert
    assertEquals("John", result.name) // Verify we got data
    coVerify { mockApi.fetchUser() } // Verify API was actually called
}

```

#### **Interview Keywords**

Business Logic Testing, Mocking Data Sources, Boundary Testing, Pure Functions, JVM Tests, Input-Output Verification, Fast Feedback Loop.

#### **Interview Speak Paragraph**

> "I find testing Use Cases and Repositories to be the most efficient part of the testing strategy. Since Use Cases are often pure Kotlin logic, I can test them heavily with various inputs to ensure edge cases are handled without needing any mocks. For Repositories, I focus on the data flow—using mocks for my API and Database interfaces to verify that the Repository correctly decides when to fetch from the network versus the local cache, and that it maps the data models correctly."

---

### **Phase 4 Complete!**

You now have the "Professional" toolkit: **DI** (asking for help) and **Testing** (verifying your work).

**Would you like to move to Phase 5: "Interview Edge – Trade-offs & Best Practices"?** (This is the final phase where we cover MVVM vs. MVI and tough interview questions).
