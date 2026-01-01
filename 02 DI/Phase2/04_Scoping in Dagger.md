---
layout: default
title: Phase 2: Dagger 2 – Topic 4: Scoping & The @Singleton Annotation
parent: Phase2
nav_order: 4
---

Here are the detailed notes for the fourth topic of Phase 2, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 2: Dagger 2 – Topic 4: Scoping & The @Singleton Annotation

In our previous discussions, we successfully taught Dagger how to create objects using `@Inject` and `@Provides`. However, by default, Dagger acts as a **Factory**. This means every time you request a dependency—whether via injection into an Activity or as a parameter for another class—Dagger runs the creation logic again and delivers a brand-new instance.

### 1. The "Unscoped" Problem

For lightweight objects like a `Presenter` or a `DateFormatter`, creating a new instance is negligible. However, for heavy infrastructure objects like **Retrofit**, **OkHttpClient**, or a **Database**, this behavior is catastrophic.

- **Performance Hit:** Re-initializing `Retrofit` involves parsing annotations and setting up thread pools, which takes significant time.
- **Memory Leaks:** If your app asks for the Database 10 times, you now have 10 open database connections in memory.
- **State Inconsistency:** If one part of your app writes to `Repository_Instance_A` and another reads from `Repository_Instance_B` (which has its own cache), the data will be out of sync.

### 2. The Solution: Scoping

To solve this, Dagger uses **Scopes**. A scope is an instruction that tells Dagger to cache the instance within the Component. The most common scope is `@Singleton`.

When we apply `@Singleton`, Dagger changes its behavior from "Create New" to "Check Cache -> Return Existing or Create New."

### 3. The "Double-Annotation" Rule

Implementing scoping in Dagger requires a strict contract. You cannot simply mark a class as `@Singleton` and expect it to work. You must follow the **Double-Annotation Rule**:

1. **The Binding:** The recipe (Class or `@Provides` method) must be annotated.
2. **The Component:** The Component that uses that recipe **must also** have the same annotation.

If these two do not match, Dagger will throw a compile-time error. This ensures that a Component strictly manages the lifecycle of the objects it holds.

### Code Demonstration

**Step 1: Scope the Dependency (The Module or Class)**

```kotlin
@Module
class NetworkModule {

    // @Singleton here tells Dagger:
    // "Create this ONCE per component, and reuse it."
    @Singleton
    @Provides
    fun provideRetrofit(): Retrofit {
        println("Creating Retrofit...") // This prints only once now!
        return Retrofit.Builder()
            .baseUrl("https://google.com")
            .build()
    }
}

```

**Step 2: Scope the Component (The Container)**
This step is often forgotten by beginners. You must tell the Component that it is capable of holding Singleton objects.

```kotlin
@Singleton // This MUST match the scope used in the modules
@Component(modules = [NetworkModule::class])
interface AppComponent {
    fun inject(activity: LoginActivity)
}

```

### 4. Custom Scopes (It's just a label)

It is vital to understand that `@Singleton` is **not magical**. To Dagger, `@Singleton` is just a label. Dagger does not know what "Singleton" means in the pattern sense; it only knows that objects marked `@Singleton` should live as long as the `AppComponent` lives.

If you create a new `AppComponent` every time you open a screen, you will get a new "Singleton" `Retrofit` every time. The "Single-ness" of the object is tied to the **lifecycle of the Component**.

- If `AppComponent` is stored in the `Application` class (which lives forever), `@Singleton` objects live forever.
- If `AppComponent` is created in an Activity `onCreate`, `@Singleton` objects are destroyed when the Activity dies.

This realization leads us to create **Custom Scopes** like `@ActivityScope` or `@LoggedUserScope`, which we will explore when we deal with sub-graphs.

---

## 🛑 Interview Summary: Scoping & @Singleton

### **Keywords**

Lifecycle Management, Caching, Instance Reusability, Component Contract, Double-Annotation Rule, Memory Efficiency, Global State, Semantic Scopes, Unscoped vs. Scoped

### **Paragraph for Interview**

"By default, Dagger creates a new instance of a dependency every time it is requested, acting as a factory. To prevent this for expensive objects like Retrofit or Databases, I use Scoping. I annotate the providing method or class with `@Singleton`, which instructs Dagger to cache the instance. However, this only works if the Component itself is also annotated with `@Singleton`. I understand that the scope is tied to the lifecycle of the Component instance, not the application itself. Therefore, for true Singleton behavior, I ensure the `@Singleton` Component is instantiated in the Android `Application` class so that it persists for the entire app lifecycle, ensuring heavy objects are created only once."

---

### **Next Step**

We have a global graph now. But real apps are not just global singletons. We have **User Flows** (Login, Dashboard, Settings). We need objects that live _only_ while a specific Activity is alive.

This brings us to **Topic 5: Component Dependencies & Subcomponents (Hierarchical Graphs)**.

Shall we proceed?
