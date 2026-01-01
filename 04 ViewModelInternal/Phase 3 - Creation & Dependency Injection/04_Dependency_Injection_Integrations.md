---
layout: default
title: Dependency Injection Integrations
parent: Phase 3   Creation & Dependency Injection
nav_order: 4
---

Here are your detailed notes for the final topic of Phase 3.

---

### **Topic: Dependency Injection Integrations (Hilt)**

#### **What It Is**

Dependency Injection (DI) Integrations, specifically with **Hilt**, automate the tedious process of creating `ViewModelFactories`.

Remember how we had to write that "Recipe Card" (Factory) manually?

- **Without Hilt:** You write the Factory class, you write the `create` logic, and you instantiate it in the Activity.
- **With Hilt:** You just add an annotation (`@HiltViewModel`), and Hilt **writes the Factory code for you** in the background during compilation.

#### **Why It Exists (The Problem)**

Writing manual Factories for every single ViewModel is boilerplate-heavy and error-prone.

- If your ViewModel needs 5 repositories, your Factory constructor needs 5 arguments.
- If you change one argument, you have to update the Factory, the Activity, and the ViewModel.
- It scales poorly in large apps.

Hilt solves this by using **Annotation Processing** to generate that boilerplate code automatically.

#### **How It Works**

It uses a concept called **multibinding**.

1. **Annotation:** You tag your ViewModel with `@HiltViewModel` and the constructor with `@Inject`.
2. **Code Generation:** When you build the app, Hilt's compiler looks at these tags. It silently generates a specific `Factory` that knows how to find your repositories (dependencies).
3. **The Default Factory:** Hilt automatically sets this generated factory as the "Default Factory" for your Activity/Fragment.
4. **Usage:** In your Activity, you just call `by viewModels()`. You don't pass _any_ factory. Hilt injects it behind the scenes.

**Visualizing the Automation:**

```text
       MANUAL WAY                            HILT WAY
   +------------------+                +------------------+
   |  Write ViewModel |                |  Write ViewModel |
   +------------------+                |  Add @Inject     |
           |                           +------------------+
           v                                    |
   +------------------+                         |
   | Write Factory    | <---- (Deleted!)        | (Hilt does this
   | Class Manually   |                         |  in background)
   +------------------+                         |
           |                                    v
           v                           +------------------+
   +------------------+                | Activity Code:   |
   | Activity Code:   |                | val vm by        |
   | new Factory(...) |                |   viewModels()   |
   +------------------+                +------------------+

```

#### **Example: The "Magic" of Hilt**

**1. The ViewModel (With Annotations)**

```kotlin
@HiltViewModel // 1. Tell Hilt this is a ViewModel
class ProfileViewModel @Inject constructor( // 2. Tell Hilt to build this constructor
    private val repository: UserRepository, // 3. Hilt finds this automatically
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {
    // ...
}

```

**2. The Activity (Clean)**

```kotlin
@AndroidEntryPoint // Enable Hilt for this screen
class ProfileActivity : AppCompatActivity() {

    // NO Factory needed! Hilt handles it.
    private val viewModel: ProfileViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // ready to use
    }
}

```

#### **Interview Keywords**

Hilt, Dagger, `@HiltViewModel`, Annotation Processing, Boilerplate Reduction, Multibinding, `SavedStateHandle` Injection.

#### **Interview Speak Paragraph**

> "In modern Android development, we use Hilt to eliminate the boilerplate of manual ViewModel Factories. By annotating the ViewModel with `@HiltViewModel` and using constructor injection, Hilt automatically generates the factory code at compile time. This allows us to inject complex dependencies, like Repositories or UseCases, directly into the ViewModel's constructor without ever writing a custom `ViewModelProvider.Factory` class. In the UI layer, we simply use the `by viewModels()` delegate, and Hilt ensures the correct factory is hooked up behind the scenes."

---

**Phase 3 Complete!**
You now understand how to _build_ ViewModels properly, both manually and with modern tools.

**Next Step:**
We are moving to **Phase 4: State Saving & Process Death**. This is the area where many mid-level developers fail interviews.
Shall we start with **Configuration Change vs. Process Death**: The critical distinction?
