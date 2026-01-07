---
layout: default
title: Architectural Layers
parent: 7. Clean MVVM with Compose
nav_order: 1
---

# Architectural Layers

Here are your notes for **Topic 7.1**.

---

# Topic 7: Clean MVVM with Compose

## **Topic 7.1: Architectural Layers**

### **1. What It Is**

Clean Architecture divides your application into three clear layers, each with a specific responsibility. This separation ensures that your logic doesn't get tangled with your UI code.

1. **UI Layer (Presentation):**

- **Who:** Composables (`Screen.kt`) and StateHolders (`ViewModel.kt`).
- **Job:** Displays data on the screen and captures user events (clicks).

2. **Domain Layer (Business Logic):**

- **Who:** UseCases (e.g., `ValidatePasswordUseCase`, `GetNewsFeedUseCase`).
- **Job:** Contains the "Rules" of your business. Pure Kotlin code. No Android imports!

3. **Data Layer:**

- **Who:** Repositories (`UserRepository`) and Data Sources (Retrofit, Room).
- **Job:** Fetches and stores data. It decides: "Do I get this from the Network or the Database?"

### **2. Why It Exists (Separation of Concerns)**

- **Replaceability:** If you want to switch from a local SQLite database to a cloud Firestore database, you only touch the **Data Layer**. The UI doesn't know (and doesn't care) where the data comes from.
- **Testability:** You can test the "Business Logic" (Domain) without running an emulator. You can test the UI without making real network calls.
- **Scalability:** In a team, one person can build the UI while another builds the API connector.

### **3. How It Works (Dependency Direction)**

The golden rule is the **Direction of Dependencies**.

- **The Rule:** Outer layers depend on inner layers. Inner layers **never** know about outer layers.
- **Flow:** `UI` -> depends on -> `Domain` -> depends on -> `Data`.

**Detailed Flow:**

1. **UI:** The User clicks "Login". The ViewModel calls the UseCase.
2. **Domain:** The `LoginUseCase` checks if the email is valid. If yes, it calls the Repository.
3. **Data:** The `AuthRepository` calls the API.
4. **Return:** Data flows back up: API -> Repository -> UseCase -> ViewModel -> UI State updates.

### **4. Example: The Folder Structure**

Here is how a "Login Feature" is split across files.

**1. Data Layer (The Fetcher)**

```kotlin
// UserRepository.kt
class UserRepository(private val api: ApiService) {
    suspend fun login(username: String): Boolean {
        return api.login(username) // Call Network
    }
}

```

**2. Domain Layer (The Logic)**

```kotlin
// LoginUseCase.kt
// Pure Kotlin. Doesn't know about buttons or text fields.
class LoginUseCase(private val repository: UserRepository) {
    suspend operator fun invoke(username: String): Boolean {
        if (username.isEmpty()) return false // Business Rule
        return repository.login(username)
    }
}

```

**3. UI Layer (The Presenter)**

```kotlin
// LoginViewModel.kt
@HiltViewModel
class LoginViewModel @Inject constructor(
    private val loginUseCase: LoginUseCase // Dependency Injection
) : ViewModel() {

    fun onLoginClick(username: String) {
        viewModelScope.launch {
            val success = loginUseCase(username) // Call Domain
            // Update State...
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Separation of Concerns, Single Responsibility Principle, Unidirectional Dependency, UseCase, Repository Pattern, Pure Kotlin, Scalability.

**Interview Speak Paragraph**

> "I structure my Compose apps using Clean Architecture with MVVM. I separate the code into three distinct layers: Data, Domain, and UI. The **Data Layer** handles data retrieval via Repositories. The **Domain Layer** contains pure Kotlin UseCases that encapsulate business logic, ensuring it's testable and independent of the Android framework. The **UI Layer** consists of Composables and ViewModels; the ViewModel holds the state and communicates with the Domain layer. This strict separation ensures that my dependencies always point downwards, making the app modular, easier to test, and simpler to maintain."

---

**Next Step:**
You have the structure, but how does the ViewModel actually talk to the Composable?
Ready for **Topic 7.2: State Management Patterns**? We'll cover `StateFlow` vs `SharedFlow`.

---

## Navigation

Next â†’
