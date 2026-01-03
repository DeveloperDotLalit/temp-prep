---
layout: default
title: "Multibindings (Plugin Architecture)"
parent: "Phase 4: Elite Scenarios & Architecture"
nav_order: 3
grand_parent: "Dependency Injection"
---

Here are the detailed notes for the first topic of Phase 4, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 4: Elite Architecture – Topic 1: Multibindings (Plugin Architecture)

At the beginning of a project, dependency injection is usually 1-to-1. A `ViewModel` needs **one** `Repository`. A `Repository` needs **one** `DataSource`.

However, as applications scale to an enterprise level, we often encounter **1-to-Many** relationships.
**The Problem:**
Imagine you are building an Analytics system. You need to log events to:

1. Firebase
2. Facebook
3. Your internal backend
4. Console (for debugging)

**The Naive Approach:**

```kotlin
class AnalyticsManager @Inject constructor(
    val firebase: FirebaseLogger,
    val facebook: FacebookLogger,
    val backend: BackendLogger
    // Every time you add a new logger, you must edit this constructor.
    // This violates the Open/Closed Principle.
) {
    fun log(event: String) {
        firebase.log(event)
        facebook.log(event)
        backend.log(event)
    }
}

```

**The Elite Solution: Multibindings**
Multibindings allow Dagger/Hilt to inject a **Collection** of dependencies (`Set<T>` or `Map<K, V>`) instead of individual objects. This creates a **Plugin Architecture**. You can add a new Logger module, and Dagger will automatically "plug it in" to the collection without you ever touching the `AnalyticsManager` code.

### 1. The `@IntoSet` Annotation

The most common form of multibinding is injecting a `Set`. Dagger ensures the set is immutable and populated with every element contributing to it from across the entire app graph.

**Step 1: Define the Contract**
First, we need a common interface.

```kotlin
interface AnalyticsLogger {
    fun logEvent(name: String)
}

```

**Step 2: Define the Plugins (Modules)**
We create modules that contribute elements to the set. We use the `@IntoSet` annotation along with `@Binds` or `@Provides`.

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class AnalyticsModule {

    // Plugin 1: Firebase
    @Binds
    @IntoSet // <--- Magic Annotation
    @Singleton
    abstract fun bindFirebase(impl: FirebaseLogger): AnalyticsLogger

    // Plugin 2: Facebook
    @Binds
    @IntoSet // <--- Magic Annotation
    @Singleton
    abstract fun bindFacebook(impl: FacebookLogger): AnalyticsLogger
}

```

**Step 3: The Consumer**
The manager no longer asks for specific loggers. It asks for the **Set**.

```kotlin
@Singleton
class AnalyticsManager @Inject constructor(
    // Dagger collects all @IntoSet bindings and delivers them here.
    private val loggers: Set<@JvmSuppressWildcards AnalyticsLogger>
) {
    fun log(event: String) {
        // We just loop. We don't care if there are 2 loggers or 20.
        loggers.forEach { it.logEvent(event) }
    }
}

```

_Note: `@JvmSuppressWildcards` is a Kotlin-specific tweak often needed when injecting generic collections in Dagger._

### 2. The `@IntoMap` Annotation

Sometimes you don't just want a list; you want to look up specific implementations by a key (e.g., handling Deep Links or ViewTypes).

To use Maps, you need two things:

1. `@IntoMap` to tell Dagger it's a map entry.
2. A **Map Key** annotation (like `@StringKey`, `@IntKey`, or `@ClassKey`) to define the key.

**Code Demonstration:**

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object PaymentModule {

    @Provides
    @IntoMap
    @StringKey("PAYPAL") // The Key
    fun providePaypal(): PaymentProcessor = PaypalProcessor()

    @Provides
    @IntoMap
    @StringKey("STRIPE") // The Key
    fun provideStripe(): PaymentProcessor = StripeProcessor()
}

// Usage
class PaymentHandler @Inject constructor(
    // Injects Map<String, PaymentProcessor>
    private val processors: Map<String, @JvmSuppressWildcards PaymentProcessor>
) {
    fun pay(method: String) {
        // Look up the processor dynamically!
        processors[method]?.process()
    }
}

```

### 3. Why This is "Elite"

Multibindings enable **Decoupled Feature Modules**.

- You can have a `Core` module that defines the `AnalyticsLogger` interface.
- You can have a `FeatureA` module that provides a `FeatureALogger`.
- You can have a `FeatureB` module that provides a `FeatureBLogger`.
- The `AnalyticsManager` in Core will automatically pick up loggers from Feature A and B without knowing they exist.
- This is how scalable, multi-module architectures are built.

---

## 🛑 Interview Summary: Multibindings

### **Keywords**

Plugin Architecture, Open/Closed Principle, Extensibility, `Set<T>`, `Map<K, V>`, `@IntoSet`, `@IntoMap`, `@ElementsIntoSet`, Decoupling, Map Keys (`@StringKey`, `@ClassKey`)

### **Paragraph for Interview**

"I use Dagger Multibindings to build scalable, plugin-based architectures that adhere to the Open/Closed Principle. Instead of explicitly injecting multiple implementations of an interface—like having distinct variables for Firebase, Facebook, and Internal Analytics—I inject a generic `Set<AnalyticsLogger>`. I configure individual modules to contribute to this set using the `@IntoSet` annotation. This allows me to add or remove logging implementations simply by adding or removing a module, without ever modifying the consuming `AnalyticsManager` class. Similarly, I use `@IntoMap` for factory patterns where I need to look up dependencies dynamically at runtime based on a key, such as handling different deep link types."

---

### **Next Step**

We have covered architecture. Now we must address the most critical aspect of engineering: **Quality Assurance**.

**The Problem:** How do we test our Dagger/Hilt setup?

- In Unit Tests, we don't need Dagger (we just pass mocks manually).
- But in **UI Tests (Espresso/Compose)**, the app actually launches. It tries to build the real graph.
- If we run a UI test, we don't want the _Real_ Network Module to fire requests. We need to swap it for a _Fake_ Network Module.

We will proceed to **Topic 2: Hilt Testing Strategy (@TestInstallIn & @UninstallModules)**.

Shall we proceed?
