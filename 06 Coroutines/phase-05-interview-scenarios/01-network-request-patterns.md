---
layout: default
title: "Network Request Patterns"
parent: "Phase 5: Real World Interview Scenarios"
nav_order: 1
---

# Network Request Patterns

In Phase 5, we transition from "How do Coroutines work?" to "How do I solve professional engineering problems?" In a Senior Android/Kotlin interview, you aren't just asked to define a coroutine; you are asked to **architect a solution** for complex data fetching.

---

## **Network Request Patterns: Serial vs. Parallel**

### **What It Is**

Network Request Patterns are strategies for managing multiple API calls.

- **Chaining (Serial):** When Request B depends on the result of Request A.
- **Parallel:** When you need results from Request A and Request B at the same time, and they don't depend on each other.

### **Why It Exists**

- **The Problem:** Mobile networks are slow and unreliable. If you run three independent requests one after another (Serially), the user waits 3x longer than necessary. Conversely, if you chain them incorrectly, your app might crash or show inconsistent data.
- **The Solution:** Coroutines make both patterns look like simple, readable code, eliminating the "Callback Hell" found in older libraries.

---

### **How It Works (The Two Main Patterns)**

#### **1. The Serial Pattern (Chaining)**

You simply write the calls line by line. Because Coroutines are **suspending**, the second line won't execute until the first line returns a result.

- **Best for:** Getting a User ID, then using that ID to fetch their Profile.

#### **2. The Parallel Pattern (Concurrent)**

You use the `async` builder. This starts all requests immediately. You then call `await()` on all of them to gather the results.

- **Best for:** Fetching "News," "Weather," and "Stock Prices" for a dashboard simultaneously.

---

### **Example: The Practical Code**

**Pattern A: Chaining (Serial)**

```kotlin
suspend fun getFullProfile() {
    // Execution stops here until we get the token
    val token = api.getAuthToken()

    // Execution resumes and uses the token
    val profile = api.getProfile(token)

    updateUI(profile)
}

```

**Pattern B: Parallel (Concurrent)**

```kotlin
suspend fun getDashboardData() = supervisorScope {
    // Start both at the same time
    val weatherDeferred = async { api.getWeather() }
    val newsDeferred = async { api.getNews() }

    try {
        // Wait for both results
        val weather = weatherDeferred.await()
        val news = newsDeferred.await()
        showDashboard(weather, news)
    } catch (e: Exception) {
        handleError(e)
    }
}

```

_Note: We use `supervisorScope` here so that if the Weather API fails, we can still potentially show the News._

---

### **Optimization: The `awaitAll()` Helper**

If you have a large list of requests, don't call `await()` on each one manually. Use `awaitAll()`:

```kotlin
val requests = listOf(async { api1() }, async { api2() }, async { api3() })
val results = requests.awaitAll() // Returns a List of results

```

---

### **Interview Keywords**

Serial Execution, Parallel Decomposition, `async`/`await`, `awaitAll`, `supervisorScope`, Network Latency, Callback Hell.

### **Interview Speak Paragraph**

> "When handling network requests in Kotlin, I choose between serial and parallel patterns based on data dependency. For dependent tasks, I use standard suspending calls to chain requests linearly, which keeps the code readable and easy to debug. For independent tasks, I use 'Parallel Decomposition' with the `async` builder. By launching multiple `async` blocks and then using `awaitAll()`, I can significantly reduce total latency, as the total wait time is limited to the slowest single request rather than the sum of all requests. I always wrap parallel calls in a `supervisorScope` to ensure that a failure in one non-essential API doesn't cancel the entire batch."

---

**Common Interview Question: "What happens if one of the `async` calls fails in a parallel setup?"**

- **Answer:** If using a normal `coroutineScope`, one failure will cancel all other sibling `async` blocks and the parent. If you want to keep the other results, you must use **`supervisorScope`**. This is a critical distinction for building resilient apps.

**Would you like to move on to the next topic: Database Operations (Using Coroutines with Room or local storage efficiently)?**

Would you like me to show how to add a **Timeout** to these network requests using `withTimeout`? (Very common follow-up question).

---

[â¬… Back to Phase](../) | [Next âž¡](../)
