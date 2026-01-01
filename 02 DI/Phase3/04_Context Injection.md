---
layout: default
title: "Phase 3: Hilt – Topic 4: Context Injection (@ApplicationContext & @ActivityContext)"
parent: "Dependency Injection: Phase 3: Hilt - The Android Standard (The Solution)"
nav_order: 4
grand_parent: Dependency Injection
---

Here are the detailed notes for the fourth topic of Phase 3, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 3: Hilt – Topic 4: Context Injection (@ApplicationContext & @ActivityContext)

In Android development, the `Context` object is the gateway to the system. You need it to access resources, launch activities, instantiate databases, and interact with system services. However, `Context` is also the most dangerous object to handle in Dependency Injection because it comes in two distinct flavors with vastly different lifecycles: **Application Context** (lives forever) and **Activity Context** (lives briefly).

**The Problem:**
If you mistakenly inject an **Activity Context** into a **Singleton** class (like a Repository), the Singleton will hold a reference to that Activity forever. This prevents the Garbage Collector from cleaning up the Activity even after the user closes it, causing a massive **Memory Leak**.

Hilt solves this danger by removing the guesswork. It provides predefined **Qualifiers** that force you to be explicit about exactly _which_ Context you are requesting.

### 1. The Predefined Qualifiers

Hilt comes with two built-in annotations that you can use anywhere in your graph. You do not need to create Modules or Providers for these; Hilt provides them automatically.

1. **`@ApplicationContext`**

- **Safe for Singletons.**
- This is the global Context. It is tied to the `Application` class.
- Use this for: Database initialization, Shared Preferences, Network Clients, Analytics.

2. **`@ActivityContext`**

- **Unsafe for Singletons.** (Hilt will actually crash/fail to compile if you try to inject this into a `@Singleton` component, saving you from a leak).
- This is the specific Context of the current screen.
- Use this for: UI helpers, Dialog Builders, Toast messages, View Adapters.

### 2. Usage Scenario A: Injecting into a Class

Let's say we have a `ToastHelper` that needs a Context to show messages. Since Toasts are UI-related, we might prefer the Activity Context, but usually, the Application Context is safer for utility classes to avoid leaks.

```kotlin
// A utility class that can be injected anywhere
@Singleton
class resourceProvider @Inject constructor(
    // We explicitly ask for the Application Context.
    // Hilt looks for the Application instance and passes it here.
    @ApplicationContext private val context: Context
) {
    fun getString(resId: Int): String {
        return context.getString(resId)
    }
}

```

### 3. Usage Scenario B: Injecting into a Module

Often, third-party libraries need a Context during initialization. For example, creating a Room Database requires the Application Context.

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(
        // Hilt automatically fills this parameter
        @ApplicationContext context: Context
    ): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "my-db"
        ).build()
    }
}

```

### 4. The "No Context" Rule (The Ambiguity Check)

You might ask: _"Why can't I just write `@Inject constructor(val context: Context)`?"_

Hilt **deliberately forbids** this. If you try to inject just plain `Context` without a qualifier, Hilt will throw a compile-time error: `[Dagger/MissingBinding] android.content.Context cannot be provided`.

This is a safety feature. Hilt forces you to pause and decide: _"Do I need the one that lives forever, or the one that dies with the screen?"_ By forcing you to type the annotation, Hilt ensures you are making a conscious architectural decision regarding memory management.

### 5. Why This is "Elite"

A junior developer often passes `context` from the Activity all the way down to the ViewModel and then to the Repository. This creates a messy chain of dependencies.
An elite developer uses Hilt to inject the `@ApplicationContext` directly into the Repository. This keeps the ViewModel clean and "Context-free," which is crucial for unit testing (since you don't need to mock the Android OS to test your ViewModel logic).

---

## 🛑 Interview Summary: Context Injection

### **Keywords**

Memory Leaks, Context Lifecycle, Qualifiers, Explicit Bindings, Safety, `@ApplicationContext`, `@ActivityContext`, Ambiguity, Garbage Collection, Predefined Bindings

### **Paragraph for Interview**

"Handling Context in Dependency Injection is a common source of memory leaks, specifically when a long-lived object holds a reference to a short-lived Activity. Hilt addresses this by refusing to provide a generic `Context` binding. Instead, it forces me to use explicit qualifiers: `@ApplicationContext` and `@ActivityContext`. I always use `@ApplicationContext` for my data layer and global singletons—like Repositories or Database modules—to ensure they don't block garbage collection of my Activities. I reserve `@ActivityContext` strictly for UI-related dependencies that live within the `ActivityComponent`. This explicit requirement eliminates ambiguity and prevents the accidental creation of context-related memory leaks."

---

### **Next Step**

We have mastered the basics of Hilt, ViewModels, and Context. Now we must face the **Advanced Scenarios**.

**The Problem:** We just learned about Qualifiers (`@ApplicationContext`). But what if we need to create **our own** qualifiers?

- Example: You have two String variables in your graph. One is `API_KEY` and one is `BASE_URL`. If you just inject `String`, Dagger gets confused.

We need to learn **Topic 5: Custom Qualifiers (Disambiguating Dependencies)**.

Shall we proceed?
