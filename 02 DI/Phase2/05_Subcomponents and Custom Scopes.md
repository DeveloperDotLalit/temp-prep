---
layout: default
title: "Subcomponents & Custom Scopes"
parent: "Phase 2: Dagger 2 - The Engine"
nav_order: 5
grand_parent: "Dependency Injection"
---

Here are the detailed notes for the final topic of Phase 2, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 2: Dagger 2 – Topic 5: Subcomponents & Custom Scopes

We have built a powerful "Global Container" (`AppComponent`) that holds Singletons like `Retrofit` and `Database`. However, a professional Android app is not just a single bucket of global objects. It has distinct flows: a Login flow, a User Dashboard flow, a Settings flow.

**The Problem:**
If we put _everything_ in the `AppComponent`, two bad things happen:

1. **Memory Waste:** Objects needed only for the "Login Screen" stay in memory forever.
2. **State Leaks:** If the user logs out and logs back in, old data might persist because the objects were never destroyed.

**The Solution:**
We need a hierarchy. We want a **Parent Container** (App) that lives forever, and **Child Containers** (Activity/Feature) that are created and destroyed as needed. In Dagger, we call these **Subcomponents**.

### 1. The Parent-Child Relationship

A Subcomponent is a component that is born inside another component.

- **Inheritance:** The Child (Subcomponent) automatically has access to all objects in the Parent.
- **Isolation:** The Parent _cannot_ access objects in the Child.
- **Lifecycle:** When the Parent dies, the Child dies. But the Child can die independently while the Parent keeps living.

### 2. Custom Scopes (Creating `@ActivityScope`)

Since the `AppComponent` uses the `@Singleton` scope, we cannot use `@Singleton` for our child component (Dagger forbids two components sharing the same scope annotation in a hierarchy). We need a new label that means "I live as long as the Activity lives."

We create a custom annotation. This is just a marker, exactly like `@Singleton`.

```kotlin
import javax.inject.Scope

// This is just a stamp. It doesn't have logic.
@Scope
@Retention(AnnotationRetention.RUNTIME)
annotation class ActivityScope

```

### 3. Defining the Subcomponent

We create a new interface for our Activity-specific graph. Notice we use `@Subcomponent`, not `@Component`.

```kotlin
// This component belongs to ONE Activity.
@ActivityScope
@Subcomponent(modules = [AuthModule::class]) // It can have its own private modules!
interface AuthComponent {

    // Standard injection method for the activity
    fun inject(activity: LoginActivity)

    // We need a Factory so the Parent knows how to create this Child
    @Subcomponent.Factory
    interface Factory {
        fun create(): AuthComponent
    }
}

```

### 4. Linking Parent to Child

We must modify the Parent (`AppComponent`) to recognize this Child. We do this by adding the Child to the Parent's "Module" or exposing the factory.

```kotlin
@Singleton
@Component(modules = [NetworkModule::class, SubcomponentsModule::class])
interface AppComponent {
    // We expose the Factory of the child, not the child itself.
    // This allows the Activity to ask: "Please spawn a new AuthComponent for me."
    fun authComponentFactory(): AuthComponent.Factory
}

// We need a module to tell Dagger that AuthComponent is a subcomponent of App
@Module(subcomponents = [AuthComponent::class])
class SubcomponentsModule

```

### 5. Usage in Activity

Now, the Activity asks the Application for the factory, creates its private component, and injects itself.

```kotlin
class LoginActivity : AppCompatActivity() {

    @Inject lateinit var loginViewModel: LoginViewModel // Scoped to Activity
    @Inject lateinit var retrofit: Retrofit // Inherited from Parent (Singleton)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1. Get the Parent
        val appComponent = (application as MyAndroidApp).appComponent

        // 2. Spawn the Child
        val authComponent = appComponent.authComponentFactory().create()

        // 3. Inject
        authComponent.inject(this)
    }
}

```

### 6. Why This is "Elite"

This setup mimics exactly how **Hilt** works internally.

- Hilt's `SingletonComponent` is your `AppComponent`.
- Hilt's `ActivityComponent` is your `AuthComponent`.
- Hilt's `@ActivityScoped` is your `@ActivityScope`.

By building this manually, you understand that **scoping is just managing the life of a Subcomponent**. When the Activity is destroyed, the `authComponent` variable is garbage collected, and all `@ActivityScope` objects inside it (like `LoginViewModel`) are destroyed. The `Retrofit` instance in the Parent remains untouched.

---

## 🛑 Interview Summary: Subcomponents & Hierarchy

### **Keywords**

Graph Hierarchy, Encapsulation, Parent-Child, Object Inheritance, Lifecycle Alignment, Memory Management, `@Subcomponent`, Custom Scopes, Component Factory, Partitioning

### **Paragraph for Interview**

"To manage memory efficiently and prevent state leaks, I structure my Dagger graph hierarchically using Subcomponents. Instead of keeping all objects in the global `@Singleton` scope, I create Child Components—like an `AuthComponent`—that live only as long as the specific feature or Activity is active. I annotate these with custom scopes like `@ActivityScope`. This setup allows the child component to inherit global dependencies (like Retrofit) from the parent `AppComponent` while maintaining its own private dependencies (like `LoginViewModel`) that are garbage collected as soon as the Activity is destroyed. This mirrors the behavior of Hilt's `ActivityComponent` but gives me granular control over the graph's structure."

---

### **End of Phase 2**

You have now mastered the engine. You understand the Graph, Modules, Providers, Scoping, and Subcomponents. You have built a complete, scalable DI architecture.

But... it was a lot of boilerplate code. Factories, Interfaces, wiring modules manually.

**Phase 3: Hilt** is about removing this boilerplate. Now that you know _what_ Hilt is hiding, you are ready to use it safely.

We will start with **Phase 3, Topic 1: The Migration - How Hilt Simplifies Dagger**.

Shall we proceed to **Phase 3**?
