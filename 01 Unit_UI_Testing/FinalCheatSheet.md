---
layout: default
title: "Finalcheatsheet"
parent: "Unit & UI Testing"
---

Here is your **Final "Elite" Android Testing Cheat Sheet**.

This document condenses weeks of study into copy-paste templates and mental models. Save this for your daily work and interview prep.

---

### **Part 1: The Master Mind Map**

This text-based map visualizes the entire ecosystem we covered.

```text
ANDROID TESTING ECOSYSTEM
│
├── 1. JVM LAYER (Unit Tests - Fast & Isolated)
│   ├── Logic: JUnit 4/5 (The Runner)
│   ├── Assertions: Google Truth (Fluent API)
│   ├── Mocking: Mockk (Kotlin-native, Coroutine support)
│   └── Strategy: Testing Pyramid (70% Unit, 20% Integration, 10% UI)
│
├── 2. ARCHITECTURE LAYER (MVVM & Glue)
│   ├── ViewModel:
│   │   ├── InstantTaskExecutorRule (Fix LiveData Looper)
│   │   └── MainDispatcherRule (Fix Coroutines Main Thread)
│   ├── Data Layer:
│   │   ├── Fakes (Memory Lists) -> Better for Repositories
│   │   └── Mocks (Behavior) -> Better for Analytics/Services
│   └── Streams: Turbine (Testing Flows/StateFlows)
│
├── 3. UI LAYER (The Pixel World)
│   ├── View System (Espresso):
│   │   ├── Formula: onView() -> perform() -> check()
│   │   ├── Robot Pattern: Decoupling IDs from Test Logic
│   │   └── Recycler: espresso-contrib (RecyclerViewActions)
│   └── Compose (Modern):
│   │   ├── Semantics Tree: onNodeWithText / onNodeWithTag
│   │   ├── Navigation: TestNavHostController
│   │   └── State: Recomposition happens automatically
│
├── 4. SYSTEM & STABILITY (The "Hard" Stuff)
│   ├── Flakiness: IdlingResources (Sync), DispatcherProvider
│   ├── Network: Hermetic Testing (MockWebServer - No Real API)
│   ├── DI: Hilt (@TestInstallIn, @UninstallModules)
│   └── Scenarios:
│       ├── DB Migration (MigrationTestHelper)
│       └── Deep Links (IntentsRule)
│
└── 5. DEVOPS (The Factory)
    ├── CI Pipeline: Lint -> Unit Tests -> Build -> UI Tests
    ├── Execution: Firebase Test Lab (Real Devices) vs Headless
    └── Reporting: JUnit XML + JaCoCo Coverage

```

---

### **Part 2: The Code Cheat Sheet**

#### **1. The "Elite" Dependencies (`build.gradle.kts`)**

```kotlin
dependencies {
    // --- UNIT TESTS ---
    testImplementation("junit:junit:4.13.2")
    testImplementation("com.google.truth:truth:1.4.2")
    testImplementation("io.mockk:mockk:1.13.10")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0") // runTest
    testImplementation("androidx.arch.core:core-testing:2.2.0") // InstantTaskExecutorRule
    testImplementation("app.cash.turbine:turbine:1.1.0") // Flows

    // --- UI TESTS ---
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:3.5.1") // RecyclerViews
    androidTestImplementation("androidx.compose.ui:ui-test-junit4:1.6.0") // Compose Rule
    androidTestImplementation("androidx.navigation:navigation-testing:2.7.7") // NavController
    androidTestImplementation("com.google.dagger:hilt-android-testing:2.51") // Hilt
    kaptAndroidTest("com.google.dagger:hilt-android-compiler:2.51")
}

```

#### **2. The Main Dispatcher Rule (Copy-Paste this!)**

_Use this in Unit Tests to fix "Main dispatcher is missing" errors._

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(testDispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}

```

#### **3. The Perfect ViewModel Test Template**

```kotlin
class MyViewModelTest {
    @get:Rule val instantTaskExecutorRule = InstantTaskExecutorRule()
    @get:Rule val mainDispatcherRule = MainDispatcherRule()

    private val mockRepo = mockk<MyRepository>(relaxed = true)
    private lateinit var viewModel: MyViewModel

    @Before
    fun setup() { viewModel = MyViewModel(mockRepo) }

    @Test
    fun `login - success updates state`() = runTest {
        // ARRANGE
        coEvery { mockRepo.login() } returns true

        // ACT
        viewModel.login()

        // ASSERT (StateFlow)
        assertThat(viewModel.uiState.value).isEqualTo(Success)
        coVerify { mockRepo.login() }
    }
}

```

#### **4. The Compose Test Template**

```kotlin
@get:Rule
val composeRule = createComposeRule()

@Test
fun testCounter() {
    composeRule.setContent { CounterScreen() }

    // Finder -> Action -> Assertion
    composeRule.onNodeWithText("Increment").performClick()

    composeRule.onNodeWithText("Count: 1").assertIsDisplayed()
}

```

#### **5. The Azure Pipeline (`azure-pipelines.yml`)**

```yaml
trigger:
  - master
pool:
  vmImage: "ubuntu-latest"
steps:
  - task: JavaToolInstaller@0
    inputs:
      versionSpec: "17"
      jdkArchitectureOption: "x64"
      jdkSourceOption: "PreInstalled"

  - task: Gradle@3
    displayName: "Run Unit Tests"
    inputs:
      tasks: "testDebugUnitTest jacocoTestReport"
      publishJUnitResults: true # Shows "Tests" tab
      testResultsFiles: "**/TEST-*.xml"

  - task: PublishCodeCoverageResults@1
    inputs:
      codeCoverageTool: "JaCoCo"
      summaryFileLocation: "$(System.DefaultWorkingDirectory)/**/build/reports/jacoco/**/*.xml"
```

---

### **Part 3: The Interview "Answer Key"**

**Q: "How do you handle flaky tests?"**

> "I have a Zero Tolerance policy. First, I identify if it's **Concurrency** (race conditions) or **Network** flakiness.
>
> - For Network: I use **Hermetic Testing** (MockWebServer) to remove real API calls.
> - For Concurrency: I replace `Thread.sleep` with **IdlingResources** (Espresso) or `advanceUntilIdle` (Coroutines).
> - If it persists, I **Quarantine** the test (`@FlakyTest`) so it doesn't block CI, but I ticket it for immediate repair."

**Q: "Tell me about your CI/CD setup."**

> "I design pipelines that 'Fail Fast'.
>
> 1. **Static Analysis:** Lint/Ktlint runs first (seconds).
> 2. **Unit Tests:** Business logic tests run next on the JVM.
> 3. **UI Tests:** I offload these to **Firebase Test Lab** to run on real devices (sharded for speed).
> 4. **Reporting:** I publish JUnit XML and JaCoCo coverage reports to the PR dashboard to ensure no regression merges without visibility."

**Q: "How do you test a Singleton?"**

> "I prefer Dependency Injection. Even if it's a Singleton, I inject it as an interface into my ViewModel. In tests, I pass a `mockk` of that interface. If I must test legacy code accessing the Singleton directly, I add a `@VisibleForTesting` method to reset its state in the `@After` teardown method."

**Q: "How do you test Compose Navigation?"**

> "I use `TestNavHostController`. I inject this controller into my Compose hierarchy during the test setup. Instead of checking if the new screen's UI is visible, I verify the source of truth: `navController.currentBackStackEntry?.destination?.route`. This ensures the navigation graph state is correct."
