---
layout: default
title: Phase 1: The Fundamentals – Topic 4: Field Injection & Framework Classes
parent: Dependency Injection: Phase 1: The Fundamentals
nav_order: 4
grand_parent: Dependency Injection
---

Here are the detailed notes for the fourth topic of Phase 1, strictly adhering to the "Book Style" format and the revised interview summary structure.

---

# Phase 1: The Fundamentals – Topic 4: Field Injection & Framework Classes

In the previous topic, we established that Constructor Injection is the "Gold Standard" for dependency management. It guarantees that a class is fully formed and immutable upon creation. However, when we step into the specific domain of Android development, we encounter a significant architectural hurdle: **We do not control the creation of every class.**

### The Android Framework Instantiation Problem

In a standard Kotlin application, you are the god of your objects; you decide when to say `val myObject = MyClass()`. In Android, however, core components such as **Activities, Fragments, Services, and BroadcastReceivers** are instantiated by the Android Operating System, not by your code.

When a user taps an app icon, the Android OS reads the `AndroidManifest.xml`, finds the `MainActivity`, and uses Java Reflection to instantiate it. The system expects a **zero-argument constructor**. If you attempt to add a custom constructor—e.g., `class MainActivity(val repo: Repository) : AppCompatActivity()`—the app will crash immediately upon launch with a `java.lang.InstantiationException`. The system simply does not know how to provide that repository argument.

### The Solution: Field Injection

Since we cannot pass dependencies _during_ creation (Constructor Injection), we must pass them _after_ creation but _before_ usage. This pattern is known as **Field Injection** (or Member Injection).

In this pattern, we declare the dependency as a public or internal property within the class. Since the dependency cannot be set in the constructor, it must be mutable (`var`) and initially empty. In Kotlin, we utilize the `lateinit` modifier to tell the compiler: _"I promise to initialize this variable before I use it, so please don't force me to make it nullable."_

### The "Temporal Coupling" Risk

Field Injection introduces a risk known as **Temporal Coupling**. The class now has a period of time—between its creation and its injection—where it exists in an invalid state. If you try to access the dependency in the `init {}` block or before `onCreate()`, the app will crash. You are now responsible for knowing _when_ it is safe to access the object, which is usually after the `super.onCreate()` call.

### Code Demonstration: Manual Field Injection

Here is how we integrate our manual dependency graph into an Android Activity.

```kotlin
class LoginActivity : AppCompatActivity() {

    // 1. Declare the dependency using 'lateinit var'.
    // We cannot use 'private val' like we did in Constructor Injection.
    // This variable is mutable and technically unsafe until initialized.
    lateinit var userViewModel: UserViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        // 2. The Injection Point.
        // We manually reach out to our Application Container to get the dependency.
        // This is where "Field Injection" actually happens.
        val appContainer = (application as MyAndroidApp).appContainer
        userViewModel = appContainer.userViewModel

        // 3. Safe Usage.
        // Now that the variable is populated, we can use it.
        userViewModel.showUser()
    }
}

```

### Setter Injection

A variation of this is **Setter Injection**, where you expose a public function like `fun setViewModel(vm: UserViewModel)`. This is functionally identical to Field Injection but acts through a method. This was common in Java but is rarely used in Kotlin Manual DI because direct property access is more concise. However, you should know the term exists.

### Why This Matters for Hilt/Dagger

Understanding this manual process explains why Hilt and Dagger introduce specific annotations for Activities.

- In Manual DI, we write: `userViewModel = container.viewModel` inside `onCreate`.
- In Hilt, we write: `@Inject lateinit var userViewModel: UserViewModel`.
- In Hilt, the library generates code that essentially does the exact same thing: it waits for `super.onCreate()` and then assigns the variable for you. The mechanism is identical; only the syntax changes.

---

## 🛑 Interview Summary: Field Injection

### **Keywords**

Framework Instantiation, Zero-Argument Constructor, `lateinit`, Mutability, Lifecycle, Temporal Coupling, Reflection, `onCreate`, Member Injection, System-Initiated

### **Paragraph for Interview**

"While I prefer Constructor Injection for the classes I control, such as ViewModels and Repositories, I utilize Field Injection for Android framework components like Activities and Fragments. This is necessary because the Android OS instantiates these classes via reflection and requires a zero-argument constructor, preventing me from passing dependencies during instantiation. To handle this, I declare dependencies using the `lateinit var` modifier and manually assign them in the `onCreate` or `onAttach` lifecycle methods. I am careful to perform this injection before any business logic is executed to avoid `UninitializedPropertyAccessException`, acknowledging that this approach introduces a small window of temporal coupling that doesn't exist with Constructor Injection."

---

### **Next Step**

We have now covered the "Why" and the "How" of manual injection. But we still have a problem with our `AppContainer`. Right now, it holds _everything_ as a Singleton. But what if we have a `checkoutRepository` that should only exist while the user is checking out, and should be destroyed afterwards to save memory?

We need to learn about **Scopes and Lifecycle Management** in our manual container.

Shall we proceed to **Topic 5: The Application Container & Scoping**?
