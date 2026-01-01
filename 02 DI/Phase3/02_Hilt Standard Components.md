---
layout: default
title: Phase 3: Hilt – Topic 2: Standard Components & Hierarchy
parent: Phase3
nav_order: 2
---

Here are the detailed notes for the second topic of Phase 3, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 3: Hilt – Topic 2: Standard Components & Hierarchy

In Phase 2, we manually defined our own component hierarchy (`AppComponent` -> `AuthComponent`). We had to write the code to connect parents to children.

Hilt removes this burden by providing a **Predefined Component Hierarchy**. Google has analyzed thousands of Android apps and determined that almost every app needs the same standard "containers." Instead of letting you invent your own names, Hilt forces you to use theirs. This standardization makes your code instantly readable by any other Android developer.

### 1. The Hilt Component Tree

Hilt structures its containers in a strict parent-child relationship. Just like in our manual Dagger setup, a **Child** component can access any dependency defined in its **Parent**, but the Parent cannot access the Child.

Here is the standard hierarchy you will use daily:

1. **SingletonComponent** (The Root)

- **Lives for:** The entire Application lifecycle.
- **Equivalent to:** Our manual `AppComponent`.
- **Contains:** Global objects (`Retrofit`, `Database`, `SharedPrefs`).

2. **ActivityRetainedComponent** (The Survivor)

- **Lives for:** The configuration change survival period (ViewModel lifecycle).
- **Child of:** SingletonComponent.
- **Contains:** `ViewModel` logic that must survive rotation.

3. **ActivityComponent** (The UI Host)

- **Lives for:** The standard `Activity` lifecycle (`onCreate` to `onDestroy`).
- **Child of:** ActivityRetainedComponent.
- **Contains:** UI-specific objects (`Adapters`, `Dialogs`, `AnalyticsTrackers`).

4. **FragmentComponent** (The UI Fragment)

- **Lives for:** The `Fragment` lifecycle.
- **Child of:** ActivityComponent.
- **Contains:** Fragment-specific logic.

### 2. The `@InstallIn` Annotation

In Hilt, we don't manually list modules in a component interface. Instead, we tag the **Module** itself to tell Hilt where it belongs.

**Scenario A: Global Network Module**
We want `Retrofit` to be available everywhere. We install it in the Root.

```kotlin
@Module
@InstallIn(SingletonComponent::class) // Available everywhere
object NetworkModule {
    @Provides
    fun provideRetrofit(): Retrofit { ... }
}

```

**Scenario B: Activity-Specific Adapter Module**
We want an `AnalyticsLogger` that is specific to the current screen (Activity). We install it in the `ActivityComponent`.

```kotlin
@Module
@InstallIn(ActivityComponent::class) // Available ONLY in Activities and Fragments
object AnalyticsModule {
    @Provides
    fun provideLogger(): AnalyticsLogger { ... }
}

```

_Crucial Rule:_ If you install a module in `ActivityComponent`, you **cannot** inject those objects into a Service or the Application class, because those are "above" or "outside" the Activity in the hierarchy.

### 3. Hilt Scopes (The Matching Game)

Just like in Dagger, creating a component isn't enough to cache an object. You must apply a **Scope Annotation**. Hilt provides a specific scope annotation for every component.

| Component                   | Scope Annotation              | Behavior                                           |
| --------------------------- | ----------------------------- | -------------------------------------------------- |
| `SingletonComponent`        | **`@Singleton`**              | One instance per App.                              |
| `ActivityRetainedComponent` | **`@ActivityRetainedScoped`** | One instance per ViewModel (survives rotation).    |
| `ActivityComponent`         | **`@ActivityScoped`**         | One instance per Activity (recreated on rotation). |
| `FragmentComponent`         | **`@FragmentScoped`**         | One instance per Fragment.                         |
| `ServiceComponent`          | **`@ServiceScoped`**          | One instance per Service.                          |

### 4. Code Demonstration: Scoping in Action

This example demonstrates how changing the scope changes the behavior.

```kotlin
@Module
@InstallIn(ActivityComponent::class) // Lives inside the Activity Container
object NavigationModule {

    // UNSCOPED (Factory behavior)
    // Created NEW every time we inject it, even within the same Activity.
    @Provides
    fun provideNavigator(): Navigator = Navigator()

    // SCOPED
    // Created ONCE per Activity.
    // If you rotate the screen, the Activity is destroyed, so this is destroyed.
    // The new Activity gets a NEW instance.
    @Provides
    @ActivityScoped
    fun provideToolbarHandler(): ToolbarHandler = ToolbarHandler()
}

```

### 5. Why This is "Elite"

Understanding the hierarchy prevents the common **"Scope Mismatch" error**.

- _Error:_ You try to inject an `@ActivityScoped` object into a `@Singleton` class.
- _Why it fails:_ The Singleton lives forever; the Activity object dies often. You cannot put a short-lived object inside a long-lived object.
- _Fix:_ Remove the scope, or move the consuming class down to the Activity level.

---

## 🛑 Interview Summary: Hilt Hierarchy & Scopes

### **Keywords**

Predefined Components, Parent-Child Relationship, `@InstallIn`, Scope Alignment, Lifecycle Awareness, `SingletonComponent`, `ActivityComponent`, Inheritance, Contextual Injection, Graph Segmentation

### **Paragraph for Interview**

"Hilt simplifies dependency management by enforcing a predefined component hierarchy that mirrors the Android system components. Instead of manually creating subcomponents, I use standard containers like `SingletonComponent` for global dependencies and `ActivityComponent` for UI-related dependencies. I map my modules to these components using the `@InstallIn` annotation. Crucially, I align my scoping annotations to these components—using `@Singleton` for the app level and `@ActivityScoped` for the activity level. This structure ensures that dependencies are automatically garbage collected when their corresponding Android component is destroyed, preventing memory leaks without requiring manual cleanup logic."

---

### **Next Step**

We have the structure. Now we need to tackle the most important component in modern Android development: **The ViewModel**.
Hilt handles ViewModels differently than standard classes because they survive configuration changes.

We will proceed to **Topic 3: ViewModel Injection (@HiltViewModel)**.

Shall we proceed?
