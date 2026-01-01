---
layout: default
title: **Chapter 8: Scenario-Based Solutions**
parent: Unit & UI Testing: Phase8
nav_order: 3
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Phase 8, Scenario 3**.

This is the "Senior Engineer" litmus test. Juniors fix race conditions by adding `delay(500)`; Seniors fix them by architecting synchronization.

---

# **Chapter 8: Scenario-Based Solutions**

## **Scenario 3: Testing Race Conditions**

### **1. The Interview Question**

> **"We have a Search screen. When the user types 'A', we fire a network request. If they immediately type 'B' (forming 'AB'), we fire a second request. The first request might return _after_ the second one, showing wrong data. How do you test that your app correctly handles this race condition and only shows the results for 'AB'?"**

### **2. The Concept: Debouncing & Cancellation**

This isn't just a testing question; it's an architecture question.

- **The Fix:** You need to ensure the `ViewModel` cancels the previous job when a new query arrives.
- **The Test:** You need to simulate two events happening essentially "at the same time" but verify that only the _latest_ result survives.

### **3. The Tool: `TestCoroutineScheduler**`

To test race conditions, you need God-like control over time. You must pause the "Network" (Virtual Time), fire multiple events, and then let the network finish.
We use the `StandardTestDispatcher` which gives us `advanceTimeBy()`.

### **4. The Code Solution (ViewModel Test)**

**The Architecture (ViewModel):**

```kotlin
class SearchViewModel(private val api: SearchApi) : ViewModel() {
    private var searchJob: Job? = null

    fun onQueryChanged(query: String) {
        // 1. Cancel previous work (The Fix)
        searchJob?.cancel()

        searchJob = viewModelScope.launch {
            // 2. Debounce (Optional but good)
            delay(300)

            // 3. Network Call
            val results = api.search(query)
            _uiState.value = results
        }
    }
}

```

**The Test (Proving the Race Condition Handling):**

```kotlin
@Test
fun search_rapidInput_onlyReturnsLatestResult() = runTest {
    // 1. Setup Mock API with delays
    // We mock the API to simulate network lag
    coEvery { api.search("A") } coAnswers {
        delay(2000) // Takes 2 seconds
        listOf("Result A")
    }
    coEvery { api.search("AB") } coAnswers {
        delay(500) // Takes 0.5 seconds (Faster!)
        listOf("Result AB")
    }

    // 2. User types "A"
    viewModel.onQueryChanged("A")

    // 3. Virtual Clock: Advance slightly (100ms)
    // The "A" request is now in-flight (waiting for 2000ms delay)
    advanceTimeBy(100)

    // 4. User types "B" (Total "AB") immediately
    // This should CANCEL the "A" job
    viewModel.onQueryChanged("AB")

    // 5. Fast forward until everything is done
    advanceUntilIdle()

    // 6. ASSERT
    // The state should be "Result AB".
    // If "Result A" overwrote it (race condition), this assertion fails.
    assertThat(viewModel.uiState.value).contains("Result AB")

    // Elite Verify: Ensure "Result A" was never emitted to the UI
    assertThat(viewModel.uiState.value).doesNotContain("Result A")
}

```

### **5. UI Race Conditions (Espresso)**

Testing this on the UI layer is harder.

- **Scenario:** User clicks "Save" twice rapidly. We don't want two database entries.
- **Test:**

1. Disable the button immediately after the first click.
2. Use **IdlingResources** to pause the test while the first click is processing.
3. Assert the button is `DISABLED`.

```kotlin
@Test
fun doubleClick_onlySubmitsOnce() {
    // 1. Click Save
    onView(withId(R.id.btn_save)).perform(click())

    // 2. IMMEDIATELY check state (before network finishes)
    // This works because Espresso waits for UI events but NOT background threads (unless IdlingResource is used).
    // If we assume IdlingResource is NOT registered yet for this specific check:
    onView(withId(R.id.btn_save)).check(matches(not(isEnabled())))

    // 3. Register IdlingResource to wait for network
    IdlingRegistry.getInstance().register(myIdlingResource)

    // 4. Wait for finish
    onView(withText("Saved")).check(matches(isDisplayed()))
}

```

### **6. Summary for Interviews**

> "To test race conditions, I rely on **controlling virtual time** using `StandardTestDispatcher` in my unit tests.
> For a search feature, I mock the repository to return results with different simulated delays (using `coAnswers { delay(...) }`). I trigger two search events in rapid succession. I then use `advanceUntilIdle()` to let the coroutines finish. I assert that the ViewModel's state reflects only the _second_ query's result, proving that the first coroutine was correctly cancelled or ignored.
> On the UI layer, I verify that buttons become disabled immediately upon clicking to prevent 'double-submit' race conditions."

---

**Would you like to proceed to Scenario 4: "Testing Push Notifications" (Verifying system tray behavior)?**
