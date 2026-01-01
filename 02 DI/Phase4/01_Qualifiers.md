---
layout: default
title: Phase 3: Hilt – Topic 5: Qualifiers (Custom Annotations)
parent: Dependency Injection: Phase 4: Elite Scenarios & Architecture
nav_order: 1
grand_parent: Dependency Injection
---

Here are the detailed notes for the fifth topic of Phase 3, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 3: Hilt – Topic 5: Qualifiers (Custom Annotations)

In a complex Android application, you will often encounter situations where you need multiple objects of the **same type** but with **different purposes**.

**The Problem: Ambiguity**
Imagine you are building an app that talks to two different servers:

1. An **Auth Server** (for login/token refresh).
2. A **Data Server** (for fetching user content).

Both of these need a `Retrofit` instance. However, if you create two `@Provides` methods that both return `Retrofit`, Dagger will fail to compile. It will throw a `DuplicateBindings` error because it identifies dependencies by their **Type**. When you ask for `@Inject retrofit: Retrofit`, Dagger screams: _"Which one? I have two!"_

**The Solution: Qualifiers**
A **Qualifier** is a custom annotation that acts as a "Name Tag" or "Label." It allows us to distinguish between two dependencies of the same type.

### 1. Creating a Qualifier

A Qualifier is just a simple annotation file. You create a marker and decorate it with `@Qualifier`.

```kotlin
import javax.inject.Qualifier

// Label 1: For the Authentication API
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class AuthRetrofit

// Label 2: For the Public Data API
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class PublicRetrofit

```

### 2. Tagging the Provider (The Module)

Now we go to our Module and "tag" our functions. We are telling Dagger: _"This function provides the Retrofit instance labeled as 'AuthRetrofit'."_

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    // 1. The Auth Client
    @AuthRetrofit // <--- The Tag
    @Provides
    @Singleton
    fun provideAuthRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://auth.api.com")
            .build()
    }

    // 2. The Public Client
    @PublicRetrofit // <--- The Tag
    @Provides
    @Singleton
    fun providePublicRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://data.api.com")
            .build()
    }
}

```

### 3. Tagging the Consumer (The Injection Point)

Finally, when we inject the dependency, we must specify which label we want.

```kotlin
class UserRepository @Inject constructor(
    // We explicitly ask for the 'Auth' version
    @AuthRetrofit private val authClient: Retrofit,

    // We explicitly ask for the 'Public' version
    @PublicRetrofit private val publicClient: Retrofit
) {
    // Now we can use them safely without confusion!
}

```

### 4. Advanced: The `@Named` Qualifier

For simple cases (like passing strings), Dagger includes a built-in qualifier called `@Named`. This saves you from creating a new annotation file for every little thing.

**Provider:**

```kotlin
@Provides
@Named("BaseUrl") // Built-in String label
fun provideBaseUrl() = "https://google.com"

```

**Consumer:**

```kotlin
@Inject constructor(
    @Named("BaseUrl") val url: String
)

```

_Note:_ While convenient, elite developers prefer **Custom Qualifiers** (like `@AuthRetrofit`) over `@Named` because `@Named` relies on raw strings ("BaseUrl"). If you make a typo ("BaseURL"), the app crashes. Custom annotations are typo-proof because the compiler checks them.

### 5. Why This is "Elite"

Qualifiers are the key to **A/B Testing** and **Mocking**.
You can have an interface `PaymentProcessor`.

- You create a Qualifier `@RealPayment`.
- You create a Qualifier `@FakePayment`.
- In your `PaymentModule`, you bind `@RealPayment` to `StripeProcessor`.
- In your `DebugModule`, you bind `@FakePayment` to `DummyProcessor`.
  This allows you to control exactly which implementation is injected into different parts of your app without changing the class logic.

---

## 🛑 Interview Summary: Qualifiers

### **Keywords**

Ambiguity, Duplicate Bindings, `@Qualifier`, Custom Annotations, `@Named`, Type Erasure, Differentiation, Metadata, Retention Policy, Explicit Selection

### **Paragraph for Interview**

"When my dependency graph contains multiple bindings for the same type—such as having two different `Retrofit` clients or multiple String constants—I use Qualifiers to resolve the ambiguity. Dagger identifies dependencies by type, so without differentiation, it throws a duplicate binding error. I solve this by defining custom annotations annotated with `@Qualifier`, such as `@AuthRetrofit` and `@PublicRetrofit`. I apply these annotations both to the `@Provides` methods in my modules and to the `@Inject` constructors in my consuming classes. While the built-in `@Named` qualifier exists for simple cases, I prefer custom qualifiers because they provide compile-time safety against string typos and make the code more readable."

---

### **Next Step**

We have handled Singletons, Activities, ViewModels, and Multiple Implementations.
But there is one final, complex topic in Phase 3 that separates the seniors from the leads: **Assisted Injection**.

**The Problem:** What if you want to inject a ViewModel, but you also want to pass a dynamic argument (like a `userId` from the Intent) into its constructor _at runtime_?

- `@Inject` is compile-time.
- `userId` is runtime.
- How do we mix them?

Shall we proceed to **Topic 6: Assisted Injection (Mixing Runtime & Compile-time args)**?
