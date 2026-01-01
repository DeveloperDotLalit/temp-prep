---
layout: default
title: Phase 3: Hilt – Topic 1: The Migration (Hilt vs. Dagger)
parent: Dependency Injection: Phase 3: Hilt - The Android Standard (The Solution)
nav_order: 1
grand_parent: Dependency Injection
---

Here are the detailed notes for the first topic of Phase 3, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 3: Hilt – Topic 1: The Migration (Hilt vs. Dagger)

We have spent Phase 2 building a robust Dagger architecture. We wrote Component interfaces, we created Subcomponents for Activities, we manually wired factories, and we called `inject(this)` in every single Activity. It was powerful, but it was verbose.

Enter **Hilt**. Hilt is not a separate library; it is a wrapper built _on top_ of Dagger. Its purpose is to standardize the Dagger setup for Android. Google realized that 90% of Android apps write the exact same Dagger boilerplate (AppComponent, ActivityComponent, FragmentComponent). Hilt auto-generates these standard components for you, effectively removing the need to write the "wiring" code.

### 1. The Philosophy: Opinionated Defaults

Dagger is flexible; you can structure your graph however you want. Hilt is **opinionated**; it forces you to use a specific structure.

- **Dagger:** You must define your own Component hierarchy (`AppComponent` -> `AuthComponent`).
- **Hilt:** The hierarchy is pre-defined (`SingletonComponent` -> `ActivityComponent` -> `FragmentComponent`).

Because the hierarchy is fixed, Hilt can generate the Components for you. You never need to write `interface AppComponent` again.

### 2. The Great Mapping: Dagger vs. Hilt

To understand Hilt, you simply need to map the manual Dagger concepts we just learned to their Hilt annotations.

| Concept             | Manual Dagger (Phase 2)                 | Hilt (Phase 3)                                                                           |
| ------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------- |
| **The Container**   | You write `interface AppComponent`      | **Removed.** Hilt creates `SingletonComponent` automatically.                            |
| **The Application** | You write `DaggerAppComponent.create()` | **`@HiltAndroidApp`**. Triggers code generation for the App class.                       |
| **The Injection**   | You write `component.inject(this)`      | **`@AndroidEntryPoint`**. Hilt injects automatically in `super.onCreate()`.              |
| **The Modules**     | `@Module`                               | `@Module` + **`@InstallIn`**. You must tell Hilt _which_ container the module goes into. |
| **The Scope**       | `@Singleton`                            | `@Singleton` (Same).                                                                     |

### 3. Step-by-Step Migration

#### Step A: The Application Class

**Dagger (Old):** We had to manually store the component.

```kotlin
class MyApp : Application() {
    val appComponent = DaggerAppComponent.create()
}

```

**Hilt (New):** We just annotate. Hilt generates a base class that holds the component.

```kotlin
@HiltAndroidApp
class MyApp : Application()
// Hilt quietly generates the AppComponent code behind the scenes here.

```

#### Step B: The Activity Injection

**Dagger (Old):** We had to manually request injection.

```kotlin
class LoginActivity : AppCompatActivity() {
    @Inject lateinit var repo: UserRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        (application as MyApp).appComponent.inject(this) // Boilerplate!
    }
}

```

**Hilt (New):** The annotation handles the connection.

```kotlin
@AndroidEntryPoint
class LoginActivity : AppCompatActivity() {
    // Hilt looks at this annotation, finds the generated component,
    // and injects this variable in super.onCreate().
    @Inject lateinit var repo: UserRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // No code needed here!
    }
}

```

#### Step C: The Modules (@InstallIn)

This is the only "new" concept. In Dagger, we listed modules inside the Component (`@Component(modules = [NetworkModule::class])`).
In Hilt, since we don't write the Component, we must tag the Module to tell it where to go.

**Dagger (Old):**

```kotlin
@Module
class NetworkModule { ... }

```

**Hilt (New):**

```kotlin
@Module
// "Put this module inside the Global (Singleton) container"
@InstallIn(SingletonComponent::class)
class NetworkModule {
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit { ... }
}

```

### 4. Why This is "Elite"

Many developers use Hilt without understanding Dagger. They copy-paste `@InstallIn(SingletonComponent::class)` without knowing why.

- **You know:** `SingletonComponent` is just the `AppComponent` we built in Phase 2.
- **You know:** If you change it to `@InstallIn(ActivityComponent::class)`, the module will now live in the Subcomponent we built in Phase 2, Topic 5.
- **You know:** `@AndroidEntryPoint` is just a hidden `inject(this)` call.

Hilt is not magic; it is simply a **boilerplate assassin**.

---

## 🛑 Interview Summary: Hilt Migration

### **Keywords**

Opinionated Framework, Boilerplate Reduction, `@HiltAndroidApp`, `@AndroidEntryPoint`, `@InstallIn`, Standardized Components, Pre-defined Hierarchy, Monolithic Components, Annotation Processor, Wrapper

### **Paragraph for Interview**

"I view Hilt not as a replacement for Dagger, but as an opinionated wrapper that standardizes the Dagger implementation for Android. In manual Dagger, we are responsible for defining the Component hierarchy, creating the boilerplate interfaces, and manually triggering injection in lifecycle methods. Hilt eliminates this by providing a pre-defined component hierarchy—such as `SingletonComponent` and `ActivityComponent`—which covers 99% of Android use cases. By using annotations like `@HiltAndroidApp` and `@AndroidEntryPoint`, I can leverage Dagger's compile-time safety and performance without managing the complex wiring code. The `@InstallIn` annotation is particularly useful as it explicitly declares which scope a module belongs to, making the dependency graph easier to read and maintain."

---

### **Next Step**

Now that we have the basic Hilt setup, we need to dive into the **Component Hierarchy**. Hilt provides more than just a Singleton Component; it has specific containers for ViewModels, Services, and Views.

We will proceed to **Topic 2: Hilt Standard Components & Hierarchy**.

Shall we proceed?
