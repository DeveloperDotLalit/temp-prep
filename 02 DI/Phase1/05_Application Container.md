---
layout: default
title: Phase 1: The Fundamentals – Topic 5: The Application Container & Scoping
parent: Dependency Injection: Phase1
nav_order: 5
grand_parent: Dependency Injection
---

Here are the detailed notes for the final topic of Phase 1, strictly adhering to the "Book Style" format and the revised interview summary structure.

---

# Phase 1: The Fundamentals – Topic 5: The Application Container & Scoping

We have successfully moved dependency creation out of our Activities and into a manual system. However, a naive implementation of Manual DI often leads to a monolithic "God Object" where every dependency is created immediately when the app starts. In a professional application, this is inefficient. We need control over **when** objects are created and **how long** they live. This brings us to the concepts of **Containers** and **Scoping**.

### The Role of the Container

In Manual Dependency Injection, a **Container** is a class responsible for holding the dependency graph. It acts as the central registry. If the Application is the "government" of your app, the Container is the "warehouse" where all the tools are stored.

When we integrate this with Android, we typically place this Container inside the `Application` class. Since the `Application` class is created before any Activity and destroyed only when the app process is killed, any object stored within it acts as a global singleton.

### Scoping: Singleton vs. Factory

One of the most critical decisions in architecture is determining the **Scope** of an object.

1. **Singleton Scope:** The object is created once and shared everywhere. If you modify it in Screen A, Screen B sees the change. (Examples: `UserRepository`, `RetrofitClient`, `Database`).
2. **Factory Scope (Unscoped):** A new object is created every time it is requested. If you modify it in Screen A, Screen B is unaffected. (Examples: `Presenters`, `Helpers`, and sometimes `ViewModels`).

In Manual DI, we control this using Kotlin properties:

- `val instance = ...` creates a **Singleton** (computed once, stored in memory).
- `fun getInstance() = ...` or `val instance get() = ...` creates a **Factory** (computed every time it is called).

### Advanced: Sub-Containers (Flow Scoping)

Real apps have flows—like a "Login Flow" or a "Checkout Flow." You might have dependencies that should only exist while the user is logging in.

- If we put `LoginUserData` in the main `AppContainer`, it stays in memory forever (Memory Leak).
- If we recreate it in every Activity, we can't share data between the `EmailStep` and `PasswordStep` screens.

The solution is a **Sub-Container**. We create a `LoginContainer` that sits inside the `AppContainer`. When the user starts logging in, we create this container. When they finish, we null it out, destroying all the objects inside it. This mimics Dagger's **Subcomponents**.

### Code Demonstration: The Complete Manual System

This code represents the pinnacle of Manual DI. It handles Singletons, Factories, and Custom Scopes.

```kotlin
// 1. The Sub-Container (Lives only during Login)
class LoginContainer(private val userRepository: UserRepository) {
    // This is "Scoped" to the Login flow.
    // It is a Singleton relative to this container, but temporary relative to the App.
    val loginData = LoginData()

    fun makeLoginViewModel(): LoginViewModel {
        return LoginViewModel(userRepository, loginData)
    }
}

// 2. The Main Container (Lives forever)
class AppContainer {

    // SINGLETON SCOPE: defined as a 'val'.
    // Created once when the app starts. Shared globally.
    private val remoteDataSource = RemoteDataSource()
    val userRepository = UserRepository(remoteDataSource)

    // FACTORY SCOPE: defined as a function.
    // Created fresh every time we ask for it.
    fun makeHomeViewModel(): HomeViewModel {
        return HomeViewModel(userRepository)
    }

    // SUB-CONTAINER MANAGEMENT
    // We hold a reference to the sub-container but start it as null.
    var loginContainer: LoginContainer? = null

    fun startLoginFlow() {
        loginContainer = LoginContainer(userRepository)
    }

    fun finishLoginFlow() {
        loginContainer = null // 🛑 Garbage Collector destroys everything inside.
    }
}

```

### Usage in Android

```kotlin
class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val app = application as MyAndroidApp

        // Start the scope if it's not running
        if (app.appContainer.loginContainer == null) {
            app.appContainer.startLoginFlow()
        }

        // Inject from the specific sub-container
        val viewModel = app.appContainer.loginContainer!!.makeLoginViewModel()
    }

    override fun onDestroy() {
        super.onDestroy()
        // Ideally, check isFinishing to know if we are truly closing the flow
        if (isFinishing) {
           (application as MyAndroidApp).appContainer.finishLoginFlow()
        }
    }
}

```

### Why This Matters

This manual management of `loginContainer = null` is error-prone. If you forget to null it out, you leak memory. If you access it after nulling it, you crash. **This is exactly the problem Hilt solves** with `@ActivityScoped` and `@ViewModelScoped`. Hilt automatically attaches these containers to the Android lifecycle, so they are created and destroyed at the exact right microsecond without you writing `if (null)` logic.

---

## 🛑 Interview Summary: Containers & Scoping

### **Keywords**

Singleton, Factory Pattern, Lifecycle Management, Memory Leak, Sub-container, Graph, Garbage Collection, Global State, Shared Instance, Dependency Hierarchy

### **Paragraph for Interview**

"In a robust architecture, managing the lifecycle of dependencies is just as important as creating them. I conceptually divide my graph into containers or scopes. The top-level 'AppContainer' holds global Singletons—objects like the Network Client or Database that are expensive to create and must be shared across the entire application. For feature-specific data, such as a multi-screen registration flow, I utilize sub-containers or custom scopes. This allows me to share state between related screens (like a `RegistrationData` object) but ensures that this data is cleared from memory as soon as the flow is complete. While frameworks like Hilt handle this automatically via annotations like `@Singleton` and `@ActivityScoped`, understanding the underlying container logic is essential for debugging memory leaks and scoping issues."

---

### **End of Phase 1**

Congratulations! You have effectively mastered the theory and practice of Dependency Injection. You know:

1. Why we do it (Coupling).
2. How to pass it (Constructor Injection).
3. How to receive it in Android (Field Injection).
4. How to manage it (Containers & Scopes).

You are now ready to stop doing this manually and let a robot do it for you. It is time for **Phase 2: Dagger 2 - The Engine**.

We will start with **Topic 1: Introduction to the Graph & Dagger Setup**.

Shall we proceed to **Phase 2**?
