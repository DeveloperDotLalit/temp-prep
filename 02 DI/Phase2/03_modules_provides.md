---
layout: default
title: Phase 2: Dagger 2 – Topic 3: Modules & @Provides
parent: Dependency Injection: Phase2
nav_order: 3
grand_parent: Dependency Injection
---

Here are the detailed notes for the third topic of Phase 2, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 2: Dagger 2 – Topic 3: Modules & @Provides

In the previous topic, we learned that adding `@Inject` to a constructor allows Dagger to automatically create that class. However, real-world Android development involves many classes that we do not own.

**The Problem:**
Imagine you need to inject `Retrofit` (a network library) or `SharedPreferences` (an Android system class).

1. **Read-Only Code:** You cannot open the `Retrofit.java` file inside the library JAR and add `@Inject` to its constructor. It is read-only.
2. **Builder Pattern:** Many libraries use a Builder pattern (e.g., `new Retrofit.Builder()...`) rather than a simple constructor, which Dagger cannot guess.

To solve this, Dagger introduces **Modules** and **Providers**. If `@Inject` is "Auto-Discovery," then Modules are "Manual Instructions."

### 1. The `@Module` (The Recipe Book)

A **Module** is a class annotated with `@Module`. It serves as a collection of recipes. It tells Dagger: _"If you can't find an `@Inject` constructor for a class, look in here. I might have written a manual instruction for it."_

### 2. The `@Provides` Method (The Recipe)

Inside a module, we write functions annotated with `@Provides`.

- The **return type** of the function tells Dagger _what_ dependency this recipe creates.
- The **body** of the function contains the actual code to create it.
- The **parameters** of the function are dependencies that Dagger must find first.

**Code Demonstration: The Network Module**

```kotlin
@Module
class NetworkModule {

    // 1. The Instruction
    // "Dagger, whenever someone asks for 'Retrofit', run this function."
    @Provides
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com")
            .build()
    }

    // 2. Chaining Dependencies
    // "Dagger, to make a UserApi, I need that Retrofit object you just learned to make."
    @Provides
    fun provideUserApi(retrofit: Retrofit): UserApi {
        // Dagger automatically passes the result of provideRetrofit() here.
        return retrofit.create(UserApi::class.java)
    }
}

```

### 3. Connecting the Module to the Component

Writing the module is not enough; the Component doesn't know it exists yet. We must explicitly register the module in the Component's `modules` list.

```kotlin
// We update the annotation to include the module class.
@Component(modules = [NetworkModule::class])
interface AppComponent {
    fun inject(activity: LoginActivity)
}

```

Now, when you build the project:

1. Dagger tries to inject `UserApi`.
2. It looks for an `@Inject` constructor (Doesn't find one).
3. It checks `NetworkModule` (because it's listed in the Component).
4. It finds `provideUserApi`.
5. It sees `provideUserApi` needs `Retrofit`.
6. It finds `provideRetrofit`.
7. It executes them in order and succeeds.

### 4. The `Dependency` vs. `Provider` Mental Model

It is crucial to understand that Dagger cares about the **Return Type**.

- If you name your function `fun giveMeTheNetworkThing(): Retrofit`, Dagger doesn't care about the name. It only sees that it returns `Retrofit`.
- Whenever any other part of your app requests `Retrofit`, Dagger links it to this specific function.

### 5. Why this is "Elite"

Modules allow you to configure complex objects cleanly. For example, in a `DatabaseModule`, you can write logic to migrate the database schema inside the `@Provides` method. The rest of your app just asks for `@Inject database: Database` and never worries about the complex configuration logic hidden inside the module. This is true **Separation of Concerns**.

---

## 🛑 Interview Summary: Modules & Providers

### **Keywords**

Third-party Libraries, Builder Pattern, Configuration, Separation of Concerns, Return Type, Chaining, Dependency Graph, `@Module`, `@Provides`, Read-Only Classes

### **Paragraph for Interview**

"When I need to inject dependencies that I cannot modify—such as third-party libraries like Retrofit or system classes like SharedPreferences—I use Dagger Modules. Since I cannot add the `@Inject` annotation to the constructors of these classes, I create a class annotated with `@Module` and define methods annotated with `@Provides`. These methods act as factories: the return type defines the dependency being provided, and the method body contains the logic to instantiate and configure it. I then register this module with my Dagger Component. This allows Dagger to incorporate these external objects into the dependency graph alongside my own classes, treating them seamlessly."

---

### **Next Step**

We have connected Modules, Components, and Injection. But there is a massive performance flaw in our current setup.

Right now, every time we ask for `Retrofit`, Dagger runs the `@Provides` function again. It creates a **new** Retrofit instance every time. For heavy objects, this kills memory. We need to tell Dagger to reuse the same instance.

This leads us to **Topic 4: Scoping in Dagger (@Singleton)**.

Shall we proceed?
