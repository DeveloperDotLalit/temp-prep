---
layout: default
title: Viewmodelfactory The Builder Pattern
parent: ViewModel Internals: Phase 3   Creation & Dependency Injection
nav_order: 1
grand_parent: ViewModel Internals
---

Here are your detailed notes for the first topic of Phase 3.

---

### **Topic: ViewModelFactory (The Builder Pattern)**

#### **What It Is**

The `ViewModelFactory` is a pattern that tells the `ViewModelProvider` **how** to create your ViewModel.

Think of the `ViewModelProvider` as a **Vending Machine**.

- **Default Behavior:** It knows how to dispense standard items (ViewModels with no constructor arguments).
- **The Problem:** If you want a special item (a ViewModel that needs a `Repository` or `Database` passed to it), the machine gets stuck. It doesn't know how to "cook" that complex item.
- **The Factory:** This is the **Recipe Card** you feed into the machine. It gives the machine exact instructions on how to build that complex ViewModel.

#### **Why It Exists (The Problem)**

Why can't we just write `val vm = new MyViewModel(repository)`?

Because **we** don't control the lifecycle.

1. **We need the Provider:** We _must_ go through `ViewModelProvider` so it can check the cache (Store) and handle rotation survival.
2. **Provider uses Reflection:** By default, the Provider tries to call the empty constructor (`MyViewModel()`).
3. **Crash:** If your ViewModel looks like this: `class MyViewModel(val repo: Repository)`, the default Provider crashes because it doesn't know what "repo" is or where to get it.

We use a Factory to solve **Dependency Injection**—passing external objects (like Repositories) into the ViewModel.

#### **How It Works**

It uses the standard **Factory Design Pattern**.

1. You create a class that implements `ViewModelProvider.Factory`.
2. You override the `create()` method.
3. Inside `create()`, you manually write the code `return MyViewModel(myRepository)`.
4. You pass this Factory to the Provider.

Now, when the Provider needs a new instance, it calls **your** `create()` method instead of trying to guess.

**Visualizing the Delegation:**

```text
[ ViewModelProvider ]                                [ Your Custom Factory ]
       |                                                      |
       | NEEDS NEW INSTANCE                                   |
       |                                                      |
       | 1. "I need a 'UserViewModel'.                        |
       |     I don't know how to make it.                     |
       |     Factory, you do it!"                             |
       |                                                      |
       | 2. Calls factory.create()  ------------------------> |
       |                                                      |
       |                                                      | 3. Runs your code:
       |                                                      |    return new UserViewModel(repo)
       |                                                      |
       | 4. Returns Instance <------------------------------- |
       v
[ Save to Store ] -> [ Return to Activity ]

```

#### **Example: Passing a Repository**

This is the standard way to inject data sources.

**1. The ViewModel (Needs a Repository)**

```kotlin
class UserViewModel(private val repository: UserRepository) : ViewModel() {
    // ... logic using repository
}

```

**2. The Factory (The Recipe)**

```kotlin
class UserViewModelFactory(private val repository: UserRepository) : ViewModelProvider.Factory {

    // This method is called by the Provider
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(UserViewModel::class.java)) {
            // We manually create the instance here
            return UserViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}

```

**3. The Usage (In Activity)**

```kotlin
val repo = UserRepository() // Create the dependency
val factory = UserViewModelFactory(repo) // Create the recipe

// Feed the recipe to the Provider
val viewModel = ViewModelProvider(this, factory).get(UserViewModel::class.java)

```

#### **Interview Keywords**

Dependency Injection, Constructor Injection, Factory Pattern, `ViewModelProvider.Factory`, Generic Type `T`, Reflection, `create()` method.

#### **Interview Speak Paragraph**

> "We use a `ViewModelFactory` whenever our ViewModel has dependencies, such as a Repository or a Database instance. Since we cannot instantiate the ViewModel directly with `new` (because we need the `ViewModelProvider` to manage the lifecycle scope), the Provider needs instructions on how to construct the object. By default, the Provider attempts to instantiate a class with an empty constructor. The Factory pattern overrides this behavior, allowing us to manually inject dependencies via the constructor inside the `create()` method, ensuring our architecture remains clean and testable."

---

**Next Step:**
Now that we know how to make custom ViewModels, let's look at a specific _type_ of ViewModel provided by Android.
Shall we move to **AndroidViewModel vs. ViewModel**: When to use which, and the dangers of holding a `Context`?
