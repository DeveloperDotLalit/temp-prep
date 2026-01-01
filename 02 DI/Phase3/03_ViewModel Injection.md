---
layout: default
title: "Phase 3: Hilt – Topic 3: ViewModel Injection (@HiltViewModel)"
parent: "Dependency Injection: Phase 3: Hilt - The Android Standard (The Solution)"
nav_order: 3
grand_parent: Dependency Injection
---

Here are the detailed notes for the third topic of Phase 3, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 3: Hilt – Topic 3: ViewModel Injection (@HiltViewModel)

In the Android ecosystem, the `ViewModel` is a unique architectural component. Unlike a standard class, a ViewModel is designed to survive configuration changes (such as screen rotations). This unique lifecycle requirement creates a dependency injection problem: **We cannot simply instantiate a ViewModel.**

If we were to write `val vm = UserViewModel(repo)`, we would be creating a standard object that dies when the Activity rotates. To get the true "surviving" instance, we must ask the `ViewModelProvider` to give it to us. Historically, this required writing complex `ViewModelProvider.Factory` boilerplate code to bridge the gap between DI and the Android framework. Hilt solves this elegance with the `@HiltViewModel` annotation.

### 1. The Historical Struggle (The "Factory" Problem)

Before Hilt, injecting dependencies into a ViewModel was tedious. You had to:

1. Create a custom class implementing `ViewModelProvider.Factory`.
2. Pass your dependencies (Repositories) into this Factory.
3. Pass the Factory to the Activity.
4. Use the Factory to create the ViewModel.

This was often 50+ lines of boilerplate code just to get a ViewModel with a Repository.

### 2. The Hilt Solution

Hilt automates the generation of this Factory. By annotating a ViewModel, Hilt generates a specialized factory behind the scenes that knows how to read the Dagger graph and construct your class.

**Step 1: The Annotation**
We use `@HiltViewModel` on the class definition and `@Inject` on the constructor. This tells Hilt: _"I am a ViewModel. Please generate a Factory for me that pulls these dependencies from the graph."_

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository,
    // Hilt automatically provides this! No configuration needed.
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    fun loadUser() { ... }
}

```

**Step 2: The Consumer (Activity/Fragment)**
In the Activity, we do not perform Field Injection (we do not use `@Inject lateinit var`). Instead, we use the Kotlin Property Delegate `by viewModels()`.

This delegate lazily connects to the Hilt-generated factory and retrieves the correct instance.

```kotlin
@AndroidEntryPoint
class LoginActivity : AppCompatActivity() {

    // THE MAGIC LINE
    // 1. It checks if a ViewModel already exists (rotation).
    // 2. If not, it uses the Hilt Factory to create a new one with dependencies.
    private val viewModel: UserViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewModel.loadUser()
    }
}

```

### 3. The Elite Feature: SavedStateHandle

A mark of a senior developer is knowing how to handle **Process Death**. If the user puts your app in the background and the OS kills it to save memory, your ViewModel is destroyed. When the user returns, the ViewModel is recreated from scratch.

Standard dependencies (`UserRepository`) are fine, but **UI State** (like the user's search query) is lost.

Hilt allows you to inject `SavedStateHandle` into the ViewModel constructor automatically. This is a key-value map that survives process death.

- **Manual:** You have to pass the `Bundle` from Activity to Factory to ViewModel manually.
- **Hilt:** You just add `savedStateHandle: SavedStateHandle` to the constructor. Hilt does the rest.

### 4. Scope and Lifecycle

It is important to remember that a ViewModel lives in the **`ActivityRetainedComponent`**.

- It survives `Activity` destruction (rotation).
- It does _not_ survive `Application` destruction.
- **Do NOT** scope your ViewModel with `@Singleton`. It will leak.
- **Do NOT** scope your ViewModel with `@ActivityScoped`. It will die on rotation.
- By default, ViewModels are unscoped (created new for every owner), which is exactly what you want.

### 5. Why This is "Elite"

The combination of `@HiltViewModel` and `SavedStateHandle` eliminates one of the most error-prone areas of Android development: **State Restoration**.
A junior developer writes code that works until the phone is rotated or low on memory. An elite developer uses Hilt to ensure that the ViewModel and its state persist robustly through all system events without writing a single line of boilerplate factory code.

---

## 🛑 Interview Summary: ViewModel Injection

### **Keywords**

`@HiltViewModel`, `ViewModelProvider.Factory`, Boilerplate Elimination, `by viewModels()`, Property Delegate, `SavedStateHandle`, Process Death, Configuration Changes, `ActivityRetainedComponent`, Dependency resolution

### **Paragraph for Interview**

"Hilt radically simplifies MVVM architecture by automating ViewModel injection. Instead of writing manual `ViewModelProvider.Factory` classes to pass dependencies, I simply annotate my ViewModel with `@HiltViewModel` and use `@Inject` on the constructor. Hilt generates the necessary factory code at compile time. In my Activities or Fragments, I access these instances using the `by viewModels()` Kotlin property delegate, which handles the lazy initialization and lifecycle association. A critical advantage of this approach is the automatic injection of `SavedStateHandle`, which allows me to easily persist and restore UI state across system-initiated process death without complex bundle management."

---

### **Next Step**

We have covered the core Hilt features. Now we need to look at **Phase 3, Topic 4: Qualifiers**.

**The Problem:** What happens if you need _two_ different types of `Retrofit` clients? One for your internal API and one for a third-party API (like Google Maps)? `@Inject Retrofit` is ambiguous—Dagger won't know which one to give you.

Shall we proceed to **Topic 4: Qualifiers (Handling Multiple Implementations)**?
