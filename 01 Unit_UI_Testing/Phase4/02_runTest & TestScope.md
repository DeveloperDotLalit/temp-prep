---
layout: default
title: "`runTest` & TestScope"
parent: "Phase 4: Asynchronous Testing (Coroutines & Flows)"
nav_order: 2
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 4.2**.

This is the "Time Travel" chapter. This is how you test code that takes 10 seconds to run, but make the test finish in 10 milliseconds.

---

# **Chapter 4: Asynchronous Testing (Coroutines & Flows)**

## **Topic 4.2: `runTest` & TestScope**

### **1. The Old Way vs. The New Way**

- **Deprecated:** `runBlocking` (Blocks the thread, doesn't skip delays).
- **Deprecated:** `runBlockingTest` (Old API, had bugs with Flows).
- **The Standard:** **`runTest`**.
- This is the official API provided by `kotlinx-coroutines-test` (1.6.0+).
- It creates a coroutine scope specifically designed for testing.

### **2. The Superpower: Virtual Time**

In production, `delay(1000)` pauses execution for 1 real second.
In `runTest`, `delay(1000)` advances the "Virtual Clock" by 1000ms, but execution happens **instantly**.

- **Result:** A test that involves `delay(10_000)` (10 seconds) will finish in ~50ms on your computer.

### **3. `runTest` Mechanics**

When you wrap your test body in `runTest`:

1. It creates a **`TestScope`**.
2. It creates a **`StandardTestDispatcher`** (by default) and attaches it to that scope.
3. It executes the coroutine body.
4. It automatically calls `advanceUntilIdle()` at the end to make sure all coroutines finish.

```kotlin
@Test
fun `example test`() = runTest {
    // This is a Coroutine Scope
    val result = performAsyncOperation()
    assertThat(result).isTrue()
}

```

### **4. Controlling Time (Manual Scheduling)**

Sometimes you _don't_ want the test to fast-forward automatically. You want to freeze time to check a "Loading" state.

You need a `StandardTestDispatcher` for this (which `runTest` uses by default).

#### **A. `advanceTimeBy(millis)**`

Moves the virtual clock forward by a specific amount.

#### **B. `advanceUntilIdle()**`

Runs all pending coroutines until there is nothing left to do.

#### **C. `runCurrent()**`

Executes tasks that are currently pending at the _current_ time, but does not advance the clock.

### **5. Practical Example: Testing a Loading State**

Imagine a ViewModel that shows a "Loading" spinner, waits 5 seconds, then shows "Success".

**ViewModel:**

```kotlin
fun fetchData() {
    _state.value = "Loading"
    viewModelScope.launch {
        delay(5000) // The 5-second wait
        _state.value = "Success"
    }
}

```

**The Test (Using Time Control):**

```kotlin
@Test
fun `fetchData - shows loading then success`() = runTest {
    // 1. Trigger the action
    viewModel.fetchData()

    // 2. CHECK IMMEDIATE STATE
    // The coroutine has started, hit the delay(5000), and paused.
    // The virtual clock is at 0ms.
    assertThat(viewModel.state.value).isEqualTo("Loading")

    // 3. FAST FORWARD PARTIALLY
    advanceTimeBy(4000)
    // It's been 4 seconds. Still waiting.
    assertThat(viewModel.state.value).isEqualTo("Loading")

    // 4. FAST FORWARD TO FINISH
    advanceTimeBy(1001) // Now we are at 5001ms
    // The delay is over, the next line in ViewModel runs.
    assertThat(viewModel.state.value).isEqualTo("Success")
}

```

### **6. The "Unconfined" Caveat**

If you use `UnconfinedTestDispatcher` (the eager one we discussed in the previous topic), it ignores delays and runs everything immediately.

- **Pro:** Tests are simple and fast.
- **Con:** You **cannot** test the intermediate "Loading" state easily, because it switches from Loading -> Success instantly before you can check it.
- **Strategy:**
- Use `Unconfined` for simple data tests.
- Use `Standard` (default in `runTest`) when you need to check state changes _during_ a coroutine's execution.

### **7. Summary for Interviews**

> "`runTest` is the standard entry point for coroutine unit tests. It creates a `TestScope` with virtual time capabilities. This allows `delay()` functions to be skipped instantly, making tests fast. By default, it uses a `StandardTestDispatcher`, which allows me to use `advanceTimeBy()` to granularly control execution. This is critical for testing intermediate states, like verifying a ProgressBar is visible _while_ a network request is happening, before ensuring it hides when the request completes."

---

**Would you like to proceed to Topic 4.3: "Testing Flows with Turbine" (The industry standard library for Streams)?**
