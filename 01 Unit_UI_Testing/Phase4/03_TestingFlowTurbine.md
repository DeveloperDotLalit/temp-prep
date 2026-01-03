---
layout: default
title: "Testing Flows with Turbine"
parent: "Phase 4: Asynchronous Testing (Coroutines & Flows)"
nav_order: 3
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 4.3**.

This is the standard for testing streams in 2026. If you are using `Flow`, `StateFlow`, or `SharedFlow`, you need **Turbine**.

---

# **Chapter 4: Asynchronous Testing (Coroutines & Flows)**

## **Topic 4.3: Testing Flows with Turbine**

### **1. The Problem with Flows**

A standard Unit Test is linear: "Do X, check Y."
A **Flow** is a stream of data over time. It might emit "Loading", wait 2 seconds, emit "User Data", then wait, then emit "Updated Data".

- **The Old Way:** You had to collect the flow into a list inside a coroutine, add delays to wait for collection, and then assert on the list. This was verbose and flaky.

### **2. The Solution: Turbine**

**Turbine** is a small library built by Cash App (Square) specifically for testing Flows.

- **Concept:** It treats a Flow like a queue of events. You pull items off the queue one by one and assert them in order.
- **Dependency:** `testImplementation "app.cash.turbine:turbine:1.0.0"`

### **3. The Syntax (`.test { }`)**

Turbine adds an extension function `.test` to all Flows.

```kotlin
flow.test {
    // Inside this block, you interact with the stream
    val item1 = awaitItem() // Waits for the 1st emission
    val item2 = awaitItem() // Waits for the 2nd emission
    awaitComplete()         // Verifies the flow closed successfully
}

```

### **4. Key Functions (The API)**

- **`awaitItem()`**: Suspends and waits for the next item to be emitted. If nothing is emitted within a timeout (default 1s), the test fails.
- **`awaitComplete()`**: Asserts that the flow finished (called `emit` -> finished).
- **`awaitError()`**: Asserts that the flow threw an exception.
- **`expectNoEvents()`**: Asserts that nothing else happened. (Useful to ensure no extra data was sent).
- **`skipItems(n)`**: Ignores the next _n_ items (useful if you don't care about initial states).

### **5. Real-World Example: Loading -> Success**

Let's test a ViewModel that emits a loading state, fetches data, and then emits success.

**The ViewModel Logic:**

```kotlin
val uiState = flow {
    emit("Loading")
    delay(100) // Simulate network
    emit("Success: Data")
}

```

**The Test (Using Turbine):**

```kotlin
@Test
fun `uiState - emits Loading then Success`() = runTest {
    viewModel.uiState.test {
        // 1. First emission must be Loading
        val firstState = awaitItem()
        assertThat(firstState).isEqualTo("Loading")

        // 2. Second emission must be Success
        val secondState = awaitItem()
        assertThat(secondState).isEqualTo("Success: Data")

        // 3. The flow should finish
        awaitComplete()
    }
}

```

### **6. Testing `StateFlow` (The "Hot" Stream)**

Testing `StateFlow` (which is used in almost every modern ViewModel) has a specific quirk: **Replay**.

- `StateFlow` always has a value. When you start observing it (calling `.test`), it **immediately** emits its current value.

**Scenario:** A ViewModel starts with "Initial".

```kotlin
@Test
fun `stateFlow test`() = runTest {
    viewModel.uiState.test {
        // CRITICAL: You must consume the initial value first!
        val initial = awaitItem()
        assertThat(initial).isEqualTo("Initial")

        // Now trigger an action
        viewModel.login()

        // Check the result of the action
        val result = awaitItem()
        assertThat(result).isEqualTo("LoggedIn")
    }
}

```

### **7. Handling Exceptions**

If your Flow is designed to crash (e.g., Network Error), Turbine makes testing it clean.

```kotlin
@Test
fun `flow - emits error on failure`() = runTest {
    repository.errorFlow.test {
        // Assert that the flow terminates with a specific exception
        val error = awaitError()
        assertThat(error).isInstanceOf(IOException::class.java)
        assertThat(error).hasMessageThat().isEqualTo("Network Fail")
    }
}

```

### **8. Summary for Interviews**

> "I use the **Turbine** library to test Kotlin Flows. It simplifies asynchronous stream testing by allowing me to consume events sequentially using `awaitItem()`. This linearizes the test code, avoiding complex callbacks or latch mechanisms. For `StateFlows`, I ensure I consume the initial replay value before asserting on subsequent state updates triggered by my test actions."

---

**Congratulations! You have completed Phase 4.**
You can now test Coroutines, Time, and Streams.

**We are moving to Phase 5: UI Testing (Espresso).**
This is where we leave the JVM and start interacting with Views, Activities, and Clicks.

**Next Topic:** Phase 5.1: **Espresso Basics & The Robot Pattern**.
**Shall we proceed?**
