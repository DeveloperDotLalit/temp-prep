---
layout: default
title: "Designing a Network Layer"
parent: "Phase 5: Real World Interview Scenarios"
nav_order: 1
---

# Designing a Network Layer

### **Interview Scenario: Designing a Network Layer**

This is a classic "Senior" level interview question. The interviewer isn't just looking for a library name (like Retrofit); they want to see if you can architect a system that is **scalable, testable, and easy to use** by combining multiple design patterns.

---

### **1. The Strategy: Combining the "Big Three"**

To build a professional-grade network layer, we don't just pick one pattern; we use them as a "team."

- **Singleton:** To ensure we don't waste memory by creating multiple network clients.
- **Factory:** To create different types of API services or interceptors.
- **Facade (The Repository):** To give the UI a simple way to get data without caring about the network complexity.

---

### **2. Why This Combination Exists**

- **The Problem:** Network code is messy. You have base URLs, headers, timeouts, JSON parsing, and error handling. If you put this everywhere, your app becomes impossible to update (e.g., changing an API key would require touching 20 files).
- **The Solution:** 1. **Singleton** keeps the "engine" (Retrofit/OkHttp) running in one place.

2.  **Factory** builds the specific "tools" (API Interfaces).
3.  **Facade** provides the "service counter" where the rest of the app goes to ask for data.

---

### **3. How It Works (Step-by-Step Architecture)**

1. **Singleton Layer:** You create a single instance of your `OkHttpClient` and `Retrofit`. This prevents memory leaks and ensures connection pooling (reusing the same socket).
2. **Factory Layer:** You use a Factory to instantiate different API Services. For example, an `AuthService` and a `ProductService`.
3. **Facade Layer (The Repository):** You wrap these services in a Repository. The ViewModel calls `repository.getProducts()`. It has no idea that Retrofit is being used under the hood.

---

### **4. Example (The "Standard" Network Stack)**

```kotlin
// --- 1. SINGLETON PATTERN ---
// Ensures we only have one Retrofit instance for the whole app
object NetworkClient {
    private const val BASE_URL = "https://api.example.com/"

    val retrofit: Retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
}

// --- 2. FACTORY PATTERN ---
// A centralized place to create different API implementations
object ServiceFactory {
    fun <T> createService(serviceClass: Class<T>): T {
        return NetworkClient.retrofit.create(serviceClass)
    }
}

// --- 3. FACADE PATTERN (The Repository) ---
// Hides the complexity of ServiceFactory and NetworkClient from the UI
class ProductRepository {
    // The Repository uses the Factory to get the specific service
    private val apiService = ServiceFactory.createService(ProductApi::class.java)

    suspend fun fetchProducts(): List<Product> {
        return try {
            apiService.getProducts()
        } catch (e: Exception) {
            emptyList()
        }
    }
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
[  ViewModel  ]
       |
       | 1. "Give me data"
       v
[ ProductRepository (FACADE) ]
       |
       | 2. Uses ServiceFactory to get API instance
       v
[ ServiceFactory (FACTORY) ] ----> [ Retrofit (SINGLETON) ]
       |                                     |
       | 3. Creates/Returns Service          | 4. Executes Call
       v                                     v
[   ProductApi   ] <------------------- [ Network ]

```

---

### **6. Interview Keywords**

- **Separation of Concerns:** Keeping network configuration separate from data fetching.
- **Abstraction:** The UI doesn't know about Retrofit or OkHttp.
- **Resource Efficiency:** Singleton prevents creating thousands of unnecessary objects.
- **Centralized Configuration:** Changing a timeout or a Base URL happens in exactly one file.
- **Scalability:** Adding a new API service takes seconds using the Factory.

---

### **7. Interview Speak Paragraph**

> "When designing a network layer in Android, I combine the Singleton, Factory, and Facade patterns to ensure high performance and maintainability. I use a **Singleton** for the core `Retrofit` and `OkHttpClient` instances to manage resource overhead and connection pooling. I then use a **Factory** pattern to instantiate various API service interfaces, which keeps the creation logic centralized. Finally, I implement a **Repository as a Facade**, which provides a clean and simplified API to the ViewModels. This decouples the UI from the network implementation, making it easy to add logging, caching, or even swap out the entire network library without affecting the rest of the application."

---

### **Common Interview "Follow-up" Questions**

**1. "Where would you put Dependency Injection (Hilt/Dagger) in this scenario?"**

- **Answer:** "DI would actually replace the manual **Singleton** and **Factory** logic. Instead of me calling `ServiceFactory.create()`, Hilt would 'inject' the Singleton Retrofit instance into the Repository automatically. It automates the patterns we just discussed."

**2. "How does the Facade (Repository) help with Unit Testing?"**

- **Answer:** "Because the Repository acts as a Facade, I can easily create a 'MockRepository' for my Unit Tests. The ViewModel doesn't care if the data comes from a real API or a hardcoded list in a test—it just calls the same method on the Facade."

---

**Would you like to move to the next scenario: "Managing Global State" (how to handle user sessions across the app), or do you want to try a different one?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
