---
layout: default
title: "Cheatsheet"
parent: "Unit & UI Testing"
nav_order: 12
---

Here is your **Elite Android Testing Cheat Sheet**.

This contains the "Golden Templates" we discussed. You can copy-paste these into any new Android project to instantly set up a professional testing architecture.

### **1. The Dependencies (`build.gradle.kts`)**

_Add these to your app-level `build.gradle.kts`._

```kotlin
dependencies {
    // --- Local Unit Tests (src/test) ---
    testImplementation("junit:junit:4.13.2")
    testImplementation("com.google.truth:truth:1.4.2")
    testImplementation("io.mockk:mockk:1.13.10")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0")
    testImplementation("androidx.arch.core:core-testing:2.2.0")
    testImplementation("app.cash.turbine:turbine:1.1.0")

    // --- UI Tests (src/androidTest) ---
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:3.5.1") // For RecyclerViews
    androidTestImplementation("io.mockk:mockk-android:1.13.10")

    // Hilt Testing
    androidTestImplementation("com.google.dagger:hilt-android-testing:2.51")
    kaptAndroidTest("com.google.dagger:hilt-android-compiler:2.51")
}

```

---

### **2. The Coroutine Rule (`MainDispatcherRule.kt`)**

_Put this in `src/test/java/utils/`._

```kotlin
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.rules.TestWatcher
import org.junit.runner.Description

/**
 * Replaces the Android Main Dispatcher with a Test Dispatcher.
 * Use @get:Rule val mainDispatcherRule = MainDispatcherRule()
 */
@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {

    override fun starting(description: Description) {
        Dispatchers.setMain(testDispatcher)
    }

    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}

```

---

### **3. The ViewModel Test Template**

_An example of a perfect Unit Test setup._

```kotlin
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.google.truth.Truth.assertThat
import io.mockk.*
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import utils.MainDispatcherRule

class MyViewModelTest {

    // 1. Force LiveData to run synchronously
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    // 2. Force Coroutines to run on TestDispatcher
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    // 3. Create Mocks (Relaxed = simpler setup for analytics/loggers)
    private val mockRepository = mockk<MyRepository>(relaxed = true)

    // 4. System Under Test
    private lateinit var viewModel: MyViewModel

    @Before
    fun setup() {
        // Inject the mocks
        viewModel = MyViewModel(mockRepository)
    }

    @Test
    fun `fetchData - when successful - updates state to Success`() = runTest {
        // ARRANGE
        coEvery { mockRepository.getData() } returns "Success Data"

        // ACT
        viewModel.fetchData()

        // ASSERT (Using Turbine for Flows if needed, or just value check)
        assertThat(viewModel.uiState.value).isEqualTo("Success Data")

        // VERIFY
        coVerify(exactly = 1) { mockRepository.getData() }
    }
}

```

---

### **4. The Robot Pattern Template (`BaseRobot.kt`)**

_Put this in `src/androidTest/java/utils/`._

```kotlin
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.ViewInteraction
import androidx.test.espresso.action.ViewActions
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers
import androidx.test.espresso.matcher.ViewMatchers.withId

/**
 * Base Robot to simplify Espresso syntax.
 */
open class BaseRobot {

    fun clickButton(resId: Int): ViewInteraction =
        onView(withId(resId)).perform(ViewActions.click())

    fun typeText(resId: Int, text: String): ViewInteraction =
        onView(withId(resId))
            .perform(ViewActions.typeText(text), ViewActions.closeSoftKeyboard())

    fun replaceText(resId: Int, text: String): ViewInteraction =
        onView(withId(resId))
            .perform(ViewActions.replaceText(text), ViewActions.closeSoftKeyboard())

    fun assertTextVisible(text: String): ViewInteraction =
        onView(ViewMatchers.withText(text)).check(matches(ViewMatchers.isDisplayed()))

    fun assertViewVisible(resId: Int): ViewInteraction =
        onView(withId(resId)).check(matches(ViewMatchers.isDisplayed()))

    fun assertViewGone(resId: Int): ViewInteraction =
        onView(withId(resId)).check(matches(org.hamcrest.CoreMatchers.not(ViewMatchers.isDisplayed())))
}

```

---

### **5. Usage of Robot (`LoginTest.kt`)**

_How to use the Robot in a real UI test._

```kotlin
// 1. Create the specific Robot
class LoginRobot : BaseRobot() {
    fun login(email: String, pass: String) {
        typeText(R.id.et_email, email)
        typeText(R.id.et_password, pass)
        clickButton(R.id.btn_login)
    }
}

// 2. The Test
@HiltAndroidTest
class LoginScreenTest {

    @get:Rule(order = 0)
    val hiltRule = HiltAndroidRule(this)

    @get:Rule(order = 1)
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)

    @Test
    fun login_success() {
        LoginRobot().apply {
            login("user@test.com", "password123")
            assertTextVisible("Welcome Back!")
        }
    }
}

```
