---
layout: default
title: "Hermetic Testing (MockWebServer)"
parent: "Phase 6: The Elite Level & Interview Prep"
nav_order: 2
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 6.2**.

This is the technique that separates "Hobbyist" apps from "Enterprise" apps. Large companies (Google, Uber, Square) do not let their CI/CD pipelines hit real servers because it is too flaky. They use **Hermetic Testing**.

---

# **Chapter 6: The Elite Level (System & Architecture)**

## **Topic 6.2: Hermetic Testing (MockWebServer)**

### **1. The Problem with Real Networks**

Testing against a live backend (`https://api.myservice.com`) is an **End-to-End (E2E) Test**, not a UI Test. It is dangerous for automated suites because:

- **Flakiness:** If the office WiFi blinks, the test fails.
- **Data State:** If Test A deletes "User X", Test B fails when it tries to log in as "User X". You can't guarantee the server's state.
- **Impossible Scenarios:** How do you test a "500 Internal Server Error" screen? You can't ask the backend team to crash the production server just for your test.

### **2. The Solution: Hermetic Testing**

**Hermetic** means "airtight" or "sealed."
A Hermetic Test is completely self-contained. It contains the App **AND** the Server (simulated).

- The network boundary is cut off.
- The app makes real HTTP requests, but they are intercepted by a local server running inside the test environment.

### **3. The Tool: MockWebServer**

Developed by Square (the same people behind Retrofit and OkHttp), **MockWebServer** is a small, scriptable web server that runs on your Android device or local JVM.

**Dependency:**

```kotlin
androidTestImplementation("com.squareup.okhttp3:mockwebserver:4.11.0")

```

### **4. How it Works (The Workflow)**

1. **Start:** You start the MockWebServer on `localhost` (e.g., `http://127.0.0.1:8080`).
2. **Redirect:** You tell your App (Retrofit) to use this `localhost` URL instead of the real URL.
3. **Queue:** You queue up fake responses ("When the next request comes, return a 200 OK with this JSON").
4. **Run:** The test runs, hits the local server, gets the JSON, and updates the UI.

### **5. The Challenge: Swapping the URL**

The hardest part is Step 2. Your app probably has the base URL hardcoded or in `BuildConfig`.

- **Elite Strategy:** You must design your Network Module (Hilt/Koin) to accept a Base URL, rather than hardcoding it.
- **Test Setup:** In the test, you inject the `mockWebServer.url("/")` as the Base URL.

### **6. Implementation Example**

**Step 1: The Test Setup**

```kotlin
class LoginTest {

    // The Fake Server
    private val mockWebServer = MockWebServer()

    @Before
    fun setup() {
        mockWebServer.start(8080) // Runs on localhost:8080

        // CRITICAL: You must configure your app to point to "http://localhost:8080/"
        // This usually requires Dependency Injection (replacing the 'BaseUrl' string).
        configureAppToUseUrl("http://localhost:8080/")
    }

    @After
    fun teardown() {
        mockWebServer.shutdown()
    }

    @Test
    fun login_error_showsSnackbar() {
        // 1. Script the Server: "The next request you receive will fail"
        val errorResponse = MockResponse()
            .setResponseCode(500)
            .setBody("""{"error": "Server on fire"}""")

        mockWebServer.enqueue(errorResponse)

        // 2. Run the Test
        LoginRobot()
            .typeEmail("user")
            .clickLogin() // App hits localhost -> gets 500 error

        // 3. Verify UI handles the crash gracefully
        onView(withText("Server Error")).check(matches(isDisplayed()))
    }
}

```

### **7. Advanced: The Dispatcher (Handling Multiple Endpoints)**

`enqueue()` is a First-In-First-Out queue. If your app calls `/profile` before `/login` due to a race condition, the test breaks.
For complex tests, use a **Dispatcher** to handle routing dynamically.

```kotlin
val dispatcher = object : Dispatcher() {
    override fun dispatch(request: RecordedRequest): MockResponse {
        return when (request.path) {
            "/login" -> MockResponse().setResponseCode(200).setBody(successJson)
            "/profile" -> MockResponse().setResponseCode(200).setBody(profileJson)
            else -> MockResponse().setResponseCode(404)
        }
    }
}
mockWebServer.dispatcher = dispatcher

```

### **8. Summary for Interviews**

> "For stable UI tests, I practice **Hermetic Testing** using **MockWebServer**. Instead of hitting the real production API (which introduces flakiness and data dependency), I spin up a local server instance on the device. I configure Retrofit to point to this localhost address.
> This allows me to queue precise responses—including edge cases like 404s, 500s, or malformed JSON—that are impossible to test against a real backend. It guarantees that if a test fails, it is due to a code regression, not a network glitch."

---

**Would you like to proceed to Topic 6.3: "Hilt in Testing" (How to swap those dependencies in practice)?**
