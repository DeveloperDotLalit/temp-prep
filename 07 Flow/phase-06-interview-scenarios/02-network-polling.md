---
layout: default
title: "Network Polling"
parent: "Phase 6: Interview Scenarios and Real World Use Cases"
nav_order: 2
---

# Network Polling

We are continuing **Phase 6: Interview Scenarios**. A common requirement in Android apps is to keep data fresh—like a stock ticker, a crypto price, or a delivery boy's location. This is called **Polling**.

---

### **What It Is – Simple explanation for beginners**

**Network Polling** is the process of repeatedly checking a server for updates at a fixed interval (e.g., every 10 seconds).

Using Flow for polling is like setting a **smart alarm clock**. You tell the clock: "Wake up, fetch the data, show it to me, then go back to sleep for 10 seconds, and repeat this forever as long as I am looking at the screen."

### **Why It Exists – The problem it solves**

- **The "Manual Refresh" Problem:** Users shouldn't have to pull-to-refresh every 5 seconds to see if a price changed.
- **Lifecycle Safety:** You don't want the polling to continue while the user is answering a phone call or has the app in the background. Flow combined with `repeatOnLifecycle` handles this perfectly.
- **Simplicity:** In the past, we used `Handlers` or `Timers`, which were hard to cancel and prone to memory leaks. Flow makes it a simple loop.

### **How It Works – Step-by-step logic**

1. **The Loop:** Use a `while(true)` loop inside a `flow { ... }` builder.
2. **The Action:** Perform the network request (a `suspend` function).
3. **The Emission:** `emit()` the result to the UI.
4. **The Delay:** Use `delay(time)` to pause the loop. Because `delay` is non-blocking, it doesn't freeze the app.
5. **The Lifecycle:** The collector (UI) uses `repeatOnLifecycle`. When the UI stops, the coroutine is cancelled, which automatically stops the `while(true)` loop.

---

### **Example – Code-based**

```kotlin
class CryptoViewModel(private val api: CryptoApi) : ViewModel() {

    // 1. Create the polling flow
    val btcPriceFlow: Flow<Double> = flow {
        while (true) {
            try {
                val price = api.getLatestBtcPrice() // Suspend network call
                emit(price)
            } catch (e: Exception) {
                // Log error but keep the loop alive if desired
            }
            delay(10_000) // 2. Wait for 10 seconds before next poll
        }
    }
    // Note: No need for explicit 'stop' logic;
    // Flow cancellation handles it!
}

// UI Side (Activity/Fragment)
lifecycleScope.launch {
    // 3. This ensures polling ONLY happens when the user sees the screen
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.btcPriceFlow.collect { price ->
            binding.priceText.text = "BTC: $$price"
        }
    }
}

```

### **Interview Focus: Optimization & Edge Cases**

- **Question:** "What happens to the loop if the network request fails?"
- **Answer:** If not handled with a `try-catch` inside the loop, the exception will travel upstream, trigger `.catch()` or crash the flow, and the loop will **stop**. Always wrap the network call in a `try-catch` if you want polling to continue after a failure.
- **Question:** "How do you stop the polling?"
- **Answer:** You don't need a `stop()` function. Since the flow is collected in a lifecycle-aware coroutine, the moment the user leaves the screen, the coroutine is cancelled, and the `while(true)` loop exits automatically. This is called **Cooperative Cancellation**.

### **Interview Keywords**

Polling, Infinite Loop, Non-blocking Delay, Cooperative Cancellation, `repeatOnLifecycle`, Resource Efficiency, BTC/Stock Ticker scenario.

### **Interview Speak Paragraph**

> "To implement network polling using Kotlin Flow, I would create a flow using a `while(true)` loop that performs a suspending network request and then emits the result. By using a non-blocking `delay()` at the end of each iteration, I can control the polling frequency. The beauty of this approach in Android is that when we collect this flow using `repeatOnLifecycle`, the polling automatically starts and stops in sync with the UI's visibility. This prevents battery drain by ensuring we aren't hitting the network when the app is in the background, all without needing to write manual start and stop logic."

---

**Next Step:** Let's look at how Flow interacts with your local data. Shall we explore **Scenario: Room & DataStore Integration: Using Flow for local database reactivity**? (e.g., how the UI updates automatically when you save something to the DB).

Would you like me to proceed with that?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
