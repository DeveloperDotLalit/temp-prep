---
layout: default
title: **Chapter 3: Intermediate Unit Testing (Mockk & Architecture)**
parent: Phase3
nav_order: 5
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Topic 3.4**.

This is the most critical topic for an Android Developer. If you are asked to "write a test" in an interview, 95% of the time, they will ask you to test a **ViewModel**.

---

# **Chapter 3: Intermediate Unit Testing (Mockk & Architecture)**

## **Topic 3.4: Testing ViewModels**

### **1. The Two "Main Thread" Crashes**

When you try to test a ViewModel on your local machine (JVM), it will likely crash immediately with two specific errors. You must understand _why_ to fix them.

#### **Crash A: "Method getMainLooper in Looper not mocked"**

- **Cause:** ViewModels (specifically `LiveData`) try to hook into the Android OS Main Thread (UI Thread) to post updates safely. The JVM doesn't have an Android Main Thread.
- **The Fix:** `InstantTaskExecutorRule`.

#### **Crash B: "Module with the Main dispatcher is missing"**

- **Cause:** Most ViewModels launch coroutines using `viewModelScope.launch`, which defaults to `Dispatchers.Main`. The JVM doesn't have a Main Looper, so it doesn't know what "Main" means.
- **The Fix:** Replace `Dispatchers.Main` with a `TestDispatcher`.

### **2. Solution 1: InstantTaskExecutorRule**

This rule comes from `androidx.arch.core:core-testing`. It swaps the background executor used by Architecture Components with a synchronous one that executes everything instantly on the current thread.

**Usage:**

```kotlin
@get:Rule
val instantTaskExecutorRule = InstantTaskExecutorRule()

```

- _Note:_ Even if you use Flows instead of LiveData, if your ViewModel extends the standard `ViewModel` class or uses any Lifecycle features, keep this rule.

### **3. Solution 2: The MainDispatcherRule (Elite Pattern)**

Instead of setting up the Coroutine Dispatcher in every single test file (boilerplate), we create a reusable **JUnit Rule**.

**Create this file in `src/test/java/utils/MainDispatcherRule.kt`:**

```kotlin
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.rules.TestWatcher
import org.junit.runner.Description

@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    private val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {

    override fun starting(description: Description) {
        // Before test: Swap Main Dispatcher for our Test Dispatcher
        Dispatchers.setMain(testDispatcher)
    }

    override fun finished(description: Description) {
        // After test: Reset it to avoid leaking into other tests
        Dispatchers.resetMain()
    }
}

```

- **`UnconfinedTestDispatcher`:** Runs coroutines eagerly (immediately). Great for simple tests.
- **`StandardTestDispatcher`:** Pauses execution until you say `advanceUntilIdle()`. Great for testing timing.

### **4. The Anatomy of a ViewModel Test**

We treat the ViewModel as a "Black Box" of logic.

1. **Input:** We call a function (e.g., `vm.login()`).
2. **Dependency:** It calls the Mocked Repository.
3. **Output:** It updates a `LiveData` or `StateFlow` variable.
4. **Verification:** We check the value of that variable.

### **5. Complete Code Example**

**The Production Code (ViewModel):**

```kotlin
class LoginViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _loginState = MutableLiveData<String>()
    val loginState: LiveData<String> = _loginState

    fun login(username: String) {
        _loginState.value = "Loading..."

        viewModelScope.launch {
            val success = repository.loginUser(username)
            if (success) {
                _loginState.value = "Success"
            } else {
                _loginState.value = "Error"
            }
        }
    }
}

```

**The Test Code:**

```kotlin
class LoginViewModelTest {

    // 1. Fix LiveData Looper issue
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    // 2. Fix Coroutine Main Thread issue (Our custom rule)
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    // 3. Mocks
    private val mockRepo = mockk<AuthRepository>()

    // 4. Class Under Test
    private lateinit var viewModel: LoginViewModel

    @Before
    fun setup() {
        // Initialize the VM with the mock
        viewModel = LoginViewModel(mockRepo)
    }

    @Test
    fun `login - when repo returns true - sets state to Success`() = runTest {
        // ARRANGE
        // "coEvery" is used because loginUser is a suspend function
        coEvery { mockRepo.loginUser("gemini") } returns true

        // ACT
        viewModel.login("gemini")

        // ASSERT
        // Note: For LiveData, we simply check the .value
        assertThat(viewModel.loginState.value).isEqualTo("Success")

        // Verify the repo was actually called
        coVerify { mockRepo.loginUser("gemini") }
    }

    @Test
    fun `login - when repo returns false - sets state to Error`() = runTest {
        // ARRANGE
        coEvery { mockRepo.loginUser(any()) } returns false

        // ACT
        viewModel.login("wrong_user")

        // ASSERT
        assertThat(viewModel.loginState.value).isEqualTo("Error")
    }
}

```

### **6. Important Note on `runTest`**

In the example above, I used `= runTest`.

- This is from `kotlinx-coroutines-test`.
- It creates a "TestScope" which automatically handles uncaught exceptions and ensures coroutines finish before the test ends.
- **Always** wrap coroutine tests in `runTest`.

### **7. Summary for Interviews**

> "Testing ViewModels requires handling two specific environmental constraints. First, we use the `InstantTaskExecutorRule` to force LiveData to update synchronously. Second, since unit tests run on the JVM without a Main Looper, we must replace `Dispatchers.Main` with a `TestDispatcher` (using `Dispatchers.setMain`). I typically encapsulate this dispatcher logic in a custom JUnit Rule (`MainDispatcherRule`) to keep my test classes clean. Once setup, I mock the repository using `coEvery` for suspend functions and assert that the ViewModel's exposed state updates correctly."

---

**Congratulations! You have completed Phase 3.**
You can now write professional unit tests for standard Android Architecture.

**We are moving to Phase 4: Asynchronous Testing (Coroutines & Flows).**
This is where we go deep into `Turbine` and handling "Time".

**Next Topic:** Phase 4.1: **Testing Flows with Turbine** (The modern standard).
**Shall we proceed?**
