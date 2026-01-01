---
layout: default
title: 🏆 Master Cheatsheet: Dependency Injection (Zero to Elite)
parent: Dependency
---

Here is your **Master Cheatsheet** for Dependency Injection in Android. This document aggregates the "Elite" interview responses and critical syntax patterns for rapid revision.

---

# 🏆 Master Cheatsheet: Dependency Injection (Zero to Elite)

## **Part 1: The Core Concepts (Philosophy)**

### **1. Tight vs. Loose Coupling**

- **Keywords:** Coupling, Testability, Refactoring, Flexibility, Constructor Injection, Scalability.
- **Interview Response:**
  > "I prioritize Dependency Injection primarily to avoid tight coupling. When a class instantiates its own dependencies (e.g., `val repo = Repository()`), it becomes impossible to test in isolation because I cannot swap real network calls for mocks. By using Constructor Injection, I invert this control, passing dependencies from the outside. This allows me to inject real implementations in production but 'Fake' implementations during Unit Testing, ensuring tests are fast, reliable, and hermetic."

### **2. Inversion of Control (IoC)**

- **Keywords:** Hollywood Principle ("Don't call us..."), Externalization, Container, Delegation, Framework.
- **Interview Response:**
  > "I view Inversion of Control as the architectural philosophy where the responsibility of object creation is transferred from the class to an external container. Instead of a class 'controlling' the creation of its dependencies, it becomes a passive consumer that simply defines its requirements. This separation of concerns allows the framework to manage complex lifecycle logic while the class focuses solely on its business logic."

### **3. Dependency Injection (DI) Types**

- **Keywords:** Constructor Injection (State Safety), Field Injection (Framework Classes), Mutable vs. Immutable.
- **Interview Response:**
  > "I strongly prefer **Constructor Injection** for all classes I control (ViewModels, Repositories) because it enforces strict state integrity at compile time—an object cannot exist without its dependencies. However, for Android framework components like Activities and Fragments, which are instantiated by the OS via reflection, I use **Field Injection**. I declare dependencies as `lateinit var` and the framework injects them during the `onCreate` or `onAttach` lifecycle phase."

---

## **Part 2: Dagger 2 (The Engine)**

### **4. Dagger Fundamentals**

- **Keywords:** Compile-time Code Generation, DAG (Directed Acyclic Graph), Annotation Processing, No Reflection.
- **Interview Response:**
  > "I choose Dagger 2 because it is a compile-time dependency injection framework. Unlike other libraries that rely on runtime reflection (which can be slow and crash-prone), Dagger generates standard Java code during the build process. If I have a missing binding or a circular dependency, the build fails immediately. This guarantees zero runtime overhead and ensures that my dependency graph is valid before the app even runs."

### **5. Modules & @Provides**

- **Keywords:** Third-party Libraries, Builder Pattern, Configuration, Separation of Concerns.
- **Interview Response:**
  > "For classes I cannot modify—like Retrofit, Room, or System Services—I cannot use `@Inject` on the constructor. In these cases, I use Dagger Modules. I create a class annotated with `@Module` and define methods annotated with `@Provides`. These methods act as factories where I write the logic to instantiate and configure the external library, and the return type tells Dagger what dependency is being satisfied."

### **6. Scoping (@Singleton)**

- **Keywords:** Lifecycle Management, Instance Reusability, Component Contract, Double-Annotation Rule.
- **Interview Response:**
  > "By default, Dagger creates a new instance every time a dependency is requested. To prevent this for expensive objects like Database connections, I use Scoping. I annotate the provider with `@Singleton` and ensure the holding Component is also annotated with `@Singleton`. This instructs Dagger to cache the instance for the lifetime of that Component. I understand that 'Singleton' in Dagger means 'Unique per Component Instance', not necessarily unique per App, so I ensure the Singleton Component is held in the Application class."

---

## **Part 3: Hilt (The Standard)**

### **7. Hilt Migration & Hierarchy**

- **Keywords:** Opinionated Framework, `@HiltAndroidApp`, `@AndroidEntryPoint`, `@InstallIn`, Predefined Components.
- **Interview Response:**
  > "Hilt is an opinionated wrapper around Dagger that removes the boilerplate of manually creating Component interfaces. It provides a standard hierarchy—`SingletonComponent`, `ActivityRetainedComponent`, and `ActivityComponent`—that aligns with the Android lifecycle. By using `@AndroidEntryPoint`, Hilt automatically handles the injection of Activities and Fragments. I use the `@InstallIn` annotation to place my modules into these standard containers, ensuring dependencies are available in the correct scopes."

### **8. ViewModels & SavedStateHandle**

- **Keywords:** `@HiltViewModel`, `by viewModels()`, Process Death, Configuration Changes.
- **Interview Response:**
  > "Hilt simplifies MVVM by automating the creation of ViewModel Factories. I annotate my ViewModel with `@HiltViewModel` and use `@Inject` on the constructor. Hilt generates the factory code that bridges the gap between the Dagger graph and the Android ViewModelProvider. A key advantage is the automatic injection of `SavedStateHandle`, which allows me to persist UI state across system-initiated process death without manually handling Bundles."

### **9. Context Injection**

- **Keywords:** Memory Leaks, Qualifiers, `@ApplicationContext`, `@ActivityContext`, Ambiguity.
- **Interview Response:**
  > "To prevent memory leaks, Hilt forbids injecting a raw `Context`. I must explicitly use qualifiers: `@ApplicationContext` or `@ActivityContext`. I consistently use `@ApplicationContext` for long-lived dependencies like Repositories and Databases to ensure they don't hold references to destroyed Activities. I reserve `@ActivityContext` strictly for UI-bound classes like View Adapters or Dialog Helpers that require the current theme/screen context."

### **10. Qualifiers (Ambiguity)**

- **Keywords:** Multiple Implementations, `@Qualifier`, Disambiguation, Custom Annotations.
- **Interview Response:**
  > "When I need multiple instances of the same type—like an `AuthRetrofit` and a `PublicRetrofit`—Dagger cannot distinguish them by type alone. I solve this by defining custom annotations annotated with `@Qualifier`. I tag both the `@Provides` method and the `@Inject` constructor with these annotations, giving Dagger a clear instruction on which specific implementation to inject where."

---

## **Part 4: Elite Architecture**

### **11. Assisted Injection**

- **Keywords:** Runtime Arguments, `@AssistedInject`, Factory Pattern, Immutability.
- **Interview Response:**
  > "When an object needs both Dagger dependencies (like a Repo) and runtime arguments (like a User ID from an Intent), I use Assisted Injection. I annotate the constructor with `@AssistedInject` and mark the dynamic parameters with `@Assisted`. I then define an `@AssistedFactory` interface. Dagger generates the implementation, allowing me to create the object cleanly at runtime while maintaining immutability."

### **12. Multibindings (Plugins)**

- **Keywords:** Plugin Architecture, `@IntoSet`, `@IntoMap`, Open/Closed Principle.
- **Interview Response:**
  > "To build scalable architectures, I use Multibindings to inject collections like `Set<AnalyticsLogger>`. Different feature modules can contribute their own loggers to this set using `@IntoSet`, without modifying the core logic. This decouples the modules and allows me to add new implementations simply by adding a new module."

### **13. Testing Strategy**

- **Keywords:** Hermetic Testing, `@TestInstallIn`, Module Replacement, Deterministic.
- **Interview Response:**
  > "For UI testing, I ensure reliability by replacing flaky external dependencies with Fakes. I use Hilt's `@TestInstallIn` to globally replace production modules (like `NetworkModule`) with test modules (like `FakeNetworkModule`) in the `androidTest` source set. This creates a hermetic environment where tests run against static data, making them fast and deterministic."

---

## **Part 5: Syntax Quick Reference**

### **Hilt Setup**

```kotlin
@HiltAndroidApp
class MyApp : Application()

@AndroidEntryPoint
class LoginActivity : AppCompatActivity()

```

### **Constructor Injection (Standard)**

```kotlin
class Repository @Inject constructor(
    private val api: ApiService,
    private val dao: UserDao
)

```

### **Modules & Providers**

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit = ...
}

```

### **ViewModel Injection**

```kotlin
// Definition
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repo: Repository,
    private val savedStateHandle: SavedStateHandle
) : ViewModel()

// Usage (Activity)
private val viewModel: UserViewModel by viewModels()

```

### **Qualifiers**

```kotlin
@Qualifier
annotation class AuthRetrofit

@Provides @AuthRetrofit fun provideAuth() ...
@Inject constructor(@AuthRetrofit val api: Api) ...

```

### **Assisted Injection**

```kotlin
class Worker @AssistedInject constructor(
    val repo: Repo,
    @Assisted val id: String
)

@AssistedFactory
interface WorkerFactory {
    fun create(id: String): Worker
}

```

---
