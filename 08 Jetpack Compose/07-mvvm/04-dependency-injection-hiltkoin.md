---
layout: default
title: Dependency Injection (Hilt/Koin)
parent: 7. Clean MVVM with Compose
nav_order: 4
---

# Dependency Injection (Hilt/Koin)

Here are your notes for **Topic 7.4**.

---

## **Topic 7.4: Dependency Injection (Hilt/Koin)**

### **1. What It Is**

Dependency Injection (DI) is a technique where you don't create objects manually (using `new` or `User()`); instead, you ask a "Factory" to give them to you.

- **Without DI:** `val repo = Repository(Api(Client()))` (Hard to manage).
- **With DI:** `class ViewModel(private val repo: Repository)` (The framework finds and inserts the `repo` for you).

In Android Compose, **Hilt** (built on Dagger) is the official standard, while **Koin** is a popular lightweight alternative.

### **2. Why It Exists (The "Bag of Objects")**

- **Lifecycle Management:** ViewModels need to survive configuration changes. Hilt knows exactly how to keep a ViewModel alive during rotation but kill it when the screen finishes.
- **Testing:** If your ViewModel asks for a generic `Repository` interface, you can easily swap the "Real Network Repository" for a "Fake Test Repository" without changing a single line of ViewModel code.
- **Boilerplate:** It stops you from writing factory factories to pass arguments to ViewModels.

### **3. How It Works (The Hilt Way)**

#### **A. The Setup (`@HiltAndroidApp`)**

You must annotate your `Application` class and your `MainActivity` with `@AndroidEntryPoint`. This creates the graph container.

#### **B. The ViewModel (`@HiltViewModel`)**

You annotate the ViewModel class. The `@Inject` constructor tells Hilt what ingredients this ViewModel needs.

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository // Hilt finds this and passes it in
) : ViewModel() { ... }

```

#### **C. The Composable (`hiltViewModel()`)**

This is the magic integration. You **do not** create the ViewModel yourself. You use the `hiltViewModel()` function.

- It looks up the current `NavBackStackEntry` or Activity.
- It checks if a ViewModel already exists.
- If **Yes**: It gives you the existing instance (State preserved!).
- If **No**: It creates a new one using the Factory.

### **4. Providing Dependencies (Modules)**

Sometimes you can't add `@Inject` to a class (e.g., `Retrofit` or `RoomDatabase` because they are 3rd party libraries). You use **Modules**.

```kotlin
@Module
@InstallIn(SingletonComponent::class) // Live as long as the App lives
object NetworkModule {

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder().baseUrl("https://api.com").build()
    }

    @Provides
    @Singleton
    fun provideApi(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}

```

### **5. Example: Wiring it All Together**

**1. The Logic (ViewModel)**

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val api: ApiService // Hilt injects this from the Module above
) : ViewModel() {
    // ...
}

```

**2. The UI (Screen)**

```kotlin
// Ideally, pass the state/events, not the ViewModel itself (State Hoisting)
@Composable
fun HomeScreen(
    // hiltViewModel() automatically finds the correct scope
    viewModel: HomeViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Text(text = state.data)
}

```

### **6. Interview Prep**

**Interview Keywords**
`@HiltViewModel`, `@AndroidEntryPoint`, `@Inject`, Scoped ViewModels, Dependency Graph, Module/Provides, `hiltViewModel()` vs `viewModel()`, Koin DSL.

**Interview Speak Paragraph**

> "For dependency injection in Compose, I primarily use Hilt. It integrates seamlessly with the Jetpack Navigation component via the `hiltViewModel()` function. This allows me to scope ViewModels to specific navigation back-stack entries automatically, ensuring state is preserved during rotation but cleared when the screen is popped. I use `@HiltViewModel` to annotate my ViewModels and constructor injection for dependencies. For third-party classes like Retrofit, I define Hilt Modules with `@Provides`. While I'm familiar with Koin's service locator pattern, I prefer Hilt for its compile-time safety."

---

**Next Step:**
We have the code, but we need to talk to the server.
Ready for **Topic 7.5: Network & Data Integration**? We'll fetch real data using Retrofit.

---

## Navigation

â† Previous
Next â†’
