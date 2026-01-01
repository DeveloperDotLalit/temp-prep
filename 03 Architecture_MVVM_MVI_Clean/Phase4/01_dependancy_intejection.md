---
layout: default
title: Dependancy Intejection
parent: Architecture (MVVM/MVI/Clean): Phase4
nav_order: 1
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Dependency Injection (DI) Basics (Hilt/Koin)**.

This is the concept that separates "Junior" developers from "Mid/Senior" developers.

---

### **Topic: Dependency Injection (DI) Basics**

#### **What It Is**

Dependency Injection (DI) is a fancy term for **"Asking for help"** instead of **"Doing it yourself."**

- **Without DI (Doing it yourself):** When you need a coffee, you build a coffee machine from scratch inside your kitchen.
- **With DI (Asking for help):** You just say "I need a coffee machine," and someone delivers one to your door.

In code:

- **Without DI:** The ViewModel creates the Repository (`val repo = new Repository()`).
- **With DI:** The ViewModel asks for the Repository in its constructor, and a library (like Hilt or Koin) automatically gives it to the ViewModel.

#### **Why It Exists (The Problem)**

If you create objects manually inside a class (using `new` or `val = ...`), you create a hard dependency.

1. **Impossible to Test:** If your ViewModel creates a real `NetworkRepository`, you cannot test that ViewModel without making real network calls. You can't swap the real network for a "Fake Network" because the code is hard-coded.
2. **Boilerplate Hell:** If `Repository` needs an `API`, and `API` needs a `Client`, and `Client` needs a `Context`... you have to write 50 lines of code just to create one ViewModel.

#### **How It Works (The "Magic Box")**

We use a framework like **Hilt** (Google's standard) or **Koin** (lightweight Kotlin).
Think of DI as a "Magic Box" or "Container" that holds all your objects.

1. **Registration (The Setup):** You tell the Magic Box how to create things.

- _"Hey Hilt, if anyone asks for a `Repository`, here is how you make one."_

2. **Injection (The Request):** You put `@Inject` on your ViewModel constructor.

- _"Hey Hilt, I am a ViewModel. I need a Repository. Please inject it."_

3. **Auto-Wiring:** When the app runs, Hilt looks at the ViewModel, sees it needs a Repository, creates one, and hands it over. You never write `new Repository()`.

#### **Example (Manual vs. Hilt)**

**❌ Manual Creation (Bad for Testing):**

```kotlin
class UserViewModel : ViewModel() {
    // HARD DEPENDENCY!
    // We cannot swap this for a test repository.
    private val repository = UserRepository()

    fun load() { ... }
}

```

**✅ Hilt Injection (Good for Testing):**

```kotlin
// @HiltViewModel tells Hilt "This class is yours to manage"
@HiltViewModel
class UserViewModel @Inject constructor(
    // We just ask for it. Hilt provides it.
    private val repository: UserRepository
) : ViewModel() {

    fun load() { ... }
}

```

#### **Interview Keywords**

Dependency Injection (DI), Inversion of Control (IoC), Hilt, Koin, Dagger, Testability, Loose Coupling, Constructor Injection, @Inject, @Provides.

#### **Interview Speak Paragraph**

> "I use Dependency Injection (typically Hilt) to manage my object creation. Instead of instantiating dependencies like Repositories directly inside my ViewModels, I inject them via the constructor. This creates 'Inversion of Control,' meaning the class receives its dependencies from the outside rather than creating them itself. The biggest benefit is testability: when I write unit tests, I can easily pass in a 'FakeRepository' to the ViewModel to test logic without making real network calls."

---

**Would you like to proceed to the next note: "Unit Testing the ViewModel"?**
