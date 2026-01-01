---
layout: default
title: Testing
parent: The Question Bank
nav_order: 11
---

# Android Testing

## Have you done any unit testing in your app?

That is an absolutely essential question for an experienced developer, as it verifies not just coding skill, but also commitment to quality, testability, and architecture.

| Role/Category                         | Question                                                                                                                                          |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Testing/Quality Assurance**         | **Have you done unit testing in your app? Can you explain what you unit-test, what tools you use, and how testing relates to your architecture?** |
| **What the Interviewer is Expecting** | * A strong affirmation and clear understanding of *why\* unit testing is important (verifying business logic).                                    |
|                                       | \* Distinction between **Local Unit Tests** (JVM) and **Instrumented Tests** (Device/Emulator).                                                   |
|                                       | \* Tools: **JUnit 5/4**, **Mockito/MockK**, and **Truth/Kotest** for assertions.                                                                  |
|                                       | \* Clear explanation of **Test Doubles** (Mocking/Stubbing).                                                                                      |
|                                       | \* Connection to Architecture: Only pure **Kotlin classes** (ViewModel, Use Case, Repository) are unit-tested.                                    |

> **Proper Answer:**
> "Yes, absolutely. Unit testing is a mandatory part of my development workflow. We rely on it to ensure the correctness and stability of our core application logic.
>
> ### **1. What We Unit Test (And Why)**
>
> In our **Clean MVVM** architecture, we focus unit tests exclusively on the layers that contain **business logic and data manipulation**. This means testing:
>
> - **View Model:** We verify how the ViewModel transforms data received from the Use Case and how it manages the UI state (e.g., loading, success, error states). We ensure that user actions (calls to ViewModel functions) result in the correct state being exposed via `StateFlow` or `LiveData`.
> - **Use Cases (Domain Layer):** Since this layer contains pure business rules (e.g., validation, aggregation), unit tests here are critical to verify that the core logic works correctly regardless of the UI or data source.
> - **Repositories (Data Layer):** We test the logic for making decisions—such as whether to fetch data from the local cache or the network—and how it handles mapping data transfer objects (DTOs) to domain entities. We **do not** test Room itself, as that is covered by Google's library tests.
>
> ### **2. Tools Used**
>
> | Tool                   | Usage                                                                                                                                                            |
> | :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | **JUnit 5**            | The standard framework for defining test cases, execution, and organization.                                                                                     |
> | **MockK (Preferred)**  | A modern, idiomatic mocking framework for Kotlin. Used to create **test doubles** (mocks/stubs) for dependencies like the Repository interfaces or data sources. |
> | **Mockito-Kotlin**     | Used in older projects, providing Kotlin-friendly syntax for the popular Mockito library.                                                                        |
> | **Truth (or AssertJ)** | For readable and fluent assertions (e.g., `assertThat(result).isEqualTo(expected)`).                                                                             |
> | **Coroutines Test**    | Provides `runTest` and `TestDispatcher` to correctly test suspend functions and manage asynchronous code predictably.                                            |
>
> ### **3. The Role of Mocking (Test Doubles)**
>
> When testing a component like a **ViewModel**, we don't want the test to actually make a network call or hit a database. That would make it an integration test, which is slower and less reliable.
> Instead, we use **MockK** to mock the **Repository Interface** (the dependency of the ViewModel). We then **stub** the mocked repository's methods to return predictable, controlled data (e.g., `every { repository.getUser() } returns Flow.just(testUser)`). This isolates the ViewModel, ensuring we are _only_ testing its internal logic.
>
> ### **4. Relation to Architecture**
>
> The reason unit testing is so effective in a **Clean MVVM** architecture is that the **ViewModel**, **Use Cases**, and **Repositories** are designed as **pure Kotlin classes** with no dependency on the Android Framework. This allows us to run these tests very quickly on the local **JVM** (Java Virtual Machine) without needing an emulator or device."

Would you like to review an example of a unit test for a simple ViewModel or Use Case?

---

---

## which library have you used? explain me how to do unit testing using Mockk?

This is a two-part question: confirming the library used and then detailing its implementation. As an experienced Android developer, the mocking library I use is **MockK**.

| Role/Category                         | Question                                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Testing/Kotlin Tooling**            | **Which mocking library do you use, and how do you perform unit testing using MockK, specifically for coroutines?**   |
| **What the Interviewer is Expecting** | \* Confirmation of **MockK** as the idiomatic Kotlin choice over Mockito.                                             |
|                                       | \* The core concepts: `mockk` (creation), `every` (stubbing/defining behavior), and `verify` (checking interactions). |
|                                       | \* The specialized keywords for coroutines: **`coEvery`** and **`coVerify`** and how to use `runTest`.                |
|                                       | \* Understanding of Test Doubles to isolate the System Under Test (SUT).                                              |

> **Proper Answer:**
> "My preferred mocking library for all Kotlin-based Android projects is **MockK**. It is a Kotlin-first library that provides native, idiomatic support for features like coroutines, extension functions, and final classes, which gives it a significant advantage over Java-based tools like Mockito.
> MockK relies on three core steps for effective unit testing:
>
> ### **1. Creation (`mockk`)**
>
> We use `mockk<T>()` to create a fake object (a test double) for a dependency. This dependency is then injected into the class we are actually testing (the System Under Test, or SUT), often a ViewModel or Use Case.
>
> ```kotlin
> // Dependency: The Repository Interface
> val mockRepository = mockk<UserRepository>()
> // SUT: The class under test
> val viewModel = UserViewModel(mockRepository)
>
> ```
>
> ### **2. Stubbing (`every` / `coEvery`)**
>
> Stubbing defines the predictable behavior of the mock. We tell the mock what to return when its functions are called during the test run.
>
> - **For Regular Functions:** Use **`every { ... } returns ...`**
> - **For Suspend Functions (Coroutines):** Use **`coEvery { ... } returns ...`**

> ```kotlin
> // Example: Mocking a suspend function that returns a User object
> coEvery {
>     mockRepository.fetchUser(userId = 1)
> } returns User(name = "Test User")
>
> ```
>
> ### **3. Verification (`verify` / `coVerify`)**
>
> Verification is used to check that the SUT correctly interacted with its dependency. We assert that a specific function on the mock was called, optionally with specific arguments or a certain number of times.
>
> - **For Regular Functions:** Use **`verify { ... }`**
> - **For Suspend Functions:** Use **`coVerify { ... }`**

> ```kotlin
> // Example: Verifying the ViewModel called the repository correctly
> coVerify(exactly = 1) {
>     mockRepository.fetchUser(userId = 1)
> }
>
> ```
>
> ### **Testing Coroutines with MockK**
>
> When testing classes that utilize coroutines, like a ViewModel, we combine MockK with the **Kotlin Coroutines Test library**:
>
> 1. We define the test using **`runTest { ... }`** which provides a controlled environment to run suspend functions synchronously.
> 2. We use **`coEvery`** and **`coVerify`** to handle the suspend functions defined in the interfaces.
>
> This approach ensures that we isolate the ViewModel and only test its logic for orchestrating the flow, without worrying about the actual network latency or thread switching, making the unit test deterministic and fast.
> [MockK Tutorial for Beginners | TDD Playlist - YouTube](https://www.youtube.com/watch?v=CTtc2DVAgnU) covers the core principles of using MockK for testing, including mocking suspend functions, which is highly relevant to this topic.

---

---

## Help me understand, how to do a unit testing for failure and success scenarios of an APi called from a home screen when user clicks the button?

That is a fantastic, practical question that combines architecture, threading, and testing best practices. It directly translates a real-world user interaction into a robust, testable structure.

We will focus on testing the **ViewModel** and **Repository** layers, as these are the components responsible for the business logic and handling the API result.

| Role/Category                         | Question                                                                                                                   |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Testing/Clean MVVM**                | **How do you unit test the success and failure scenarios for an API call triggered by a button click on the home screen?** |
| **What the Interviewer is Expecting** | \* Clear focus on testing the **ViewModel** logic.                                                                         |
|                                       | \* Correct use of **MockK** to fake the **Repository** behavior.                                                           |
|                                       | \* Proper handling of **Kotlin Flow** and **Coroutines** using `runTest` and `TestDispatcher`.                             |
|                                       | \* Verification of three critical states: **Loading**, **Success**, and **Error**.                                         |
|                                       | \* The role of the **Repository** in deciding success/failure (e.g., throwing an exception).                               |

---

## 🧪 Unit Testing API Scenarios (ViewModel)

We are testing the **`HomeViewModel`** logic, which depends on the **`UserRepository`** interface. Our goal is to verify that the ViewModel correctly transitions its UI state based on the mocked Repository response.

### **Setup (Test Doubles and Coroutines)**

We need MockK to mock the dependency and the Coroutines Test library to control threading.

```kotlin
// Dependencies
// Rule: Every test needs a TestDispatcher for coroutines
class HomeViewModelTest {

    // 1. Rule to manage Coroutine dispatchers for synchronous testing
    @get:Rule
    val coroutineRule = TestDispatcherRule()

    // 2. Mock the dependency: The UserRepository interface
    private val mockRepository: UserRepository = mockk()

    // 3. The System Under Test (SUT)
    private lateinit var viewModel: HomeViewModel

    @Before
    fun setup() {
        // Initialize the ViewModel before each test
        viewModel = HomeViewModel(mockRepository)
    }
    // ... tests follow
}

```

### **1. 🟢 Success Scenario Test**

**Goal:** Verify that when the button is clicked, the ViewModel exposes the **Loading** state, then successfully receives data, and finally exposes the **Success** state.

```kotlin
@Test
fun fetchUser_onSuccess_emitsLoadingThenSuccessState() = runTest {
    // ARRANGE: Define the successful data we expect
    val expectedUser = User(id = "1", name = "Jane Doe")
    val userFlow = flowOf(expectedUser)

    // STUB (MockK): Tell the mock repository to return the success Flow
    coEvery { mockRepository.fetchUser() } returns userFlow

    // ACT: Collect the StateFlow emissions and trigger the action
    // We launch collection separately to observe the state changes
    val results = mutableListOf<HomeUiState>()
    val job = launch(UnconfinedTestDispatcher(testScheduler)) {
        viewModel.uiState.collect { results.add(it) }
    }

    // ACT: Simulate the button click
    viewModel.onRefreshButtonClicked()

    // Assert the state transitions
    // The initial state is usually defined as Loading, but we check the sequence
    assertThat(results).hasSize(2)

    // ASSERT: Check the sequence of states
    assertThat(results[0]).isInstanceOf(HomeUiState.Loading::class.java)

    // The second state must be Success and contain the expected data
    assertThat(results[1]).isInstanceOf(HomeUiState.Success::class.java)
    val successState = results[1] as HomeUiState.Success
    assertThat(successState.user.name).isEqualTo("Jane Doe")

    // Cleanup the collection job
    job.cancel()
}

```

### **2. 🔴 Failure Scenario Test**

**Goal:** Verify that when the button is clicked and the API call fails (by the repository throwing an exception), the ViewModel exposes the **Loading** state, and then correctly exposes the **Error** state.

```kotlin
@Test
fun fetchUser_onFailure_emitsLoadingThenErrorState() = runTest {
    // ARRANGE: Define the exception we expect the repository to throw
    val expectedException = IOException("Network Error")

    // STUB (MockK): Tell the mock repository to throw an exception
    // The flow builder must emit the exception
    coEvery { mockRepository.fetchUser() } returns flow { throw expectedException }

    // ACT: Collect the StateFlow emissions and trigger the action
    val results = mutableListOf<HomeUiState>()
    val job = launch(UnconfinedTestDispatcher(testScheduler)) {
        viewModel.uiState.collect { results.add(it) }
    }

    // ACT: Simulate the button click
    viewModel.onRefreshButtonClicked()

    // Assert the state transitions
    assertThat(results).hasSize(2)

    // ASSERT: Check the sequence of states
    assertThat(results[0]).isInstanceOf(HomeUiState.Loading::class.java)

    // The second state must be Error and contain the expected message
    assertThat(results[1]).isInstanceOf(HomeUiState.Error::class.java)
    val errorState = results[1] as HomeUiState.Error
    assertThat(errorState.message).contains("Network Error")

    // Cleanup the collection job
    job.cancel()
}

```

### **Key Logic Behind the Testing Method**

1. **Isolation (MockK):** We only test the ViewModel. By mocking the `UserRepository`, we ensure that a failed test means the **ViewModel's logic** is flawed, not the network connection or the database.
2. **Coroutines Control (`runTest`):** We use `runTest` to execute the coroutines **synchronously**. This eliminates timing variability and makes the test deterministic. We don't have to wait for delays; everything executes instantly in the virtual time managed by the `TestScheduler`.
3. **State Observation:** Instead of checking the ViewModel's state variable once, we **collect** the emitted values of the `StateFlow` into a list. This allows us to assert the correct **sequence** of state transitions: `Loading` always precedes `Success` or `Error`.
4. **Error Handling:** The responsibility to handle the network error is placed on the **Repository** (by throwing an exception). The test verifies that the ViewModel's `catch` block correctly captures this exception and emits the appropriate `Error` state to the UI.

---

---
