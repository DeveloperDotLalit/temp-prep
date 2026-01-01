---
layout: default
title: Spotting Code Smells
parent: Phase7
nav_order: 3
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Spotting "Code Smells" (The Bad Code Test)**.

This is a common interview format: _"Here is a class. Tell me what is wrong with it."_ You need to act like a strict code reviewer.

---

### **Topic: Spotting "Code Smells" (The Bad Code Test)**

#### **What It Is**

A "Code Smell" isn't a bug (the code might actually run), but it indicates a deeper design problem that will cause crashes, memory leaks, or maintenance headaches later.

In Android interviews, they intentionally give you code that violates Clean Architecture principles to see if you catch it.

#### **The "Big 5" Android Smells (What to Look For)**

**1. Context in ViewModel (The #1 Sin)**

- **The Smell:** Passing `Activity`, `Fragment`, or `View` into the ViewModel constructor.
- **The Danger:** **Memory Leak.** The ViewModel lives longer than the Activity. If the Activity dies (rotation) but the ViewModel is holding onto it, the Garbage Collector cannot delete the Activity.
- **The Fix:** Use `AndroidViewModel` and pass `Application` context only if absolutely necessary. Never hold UI references.

**2. Logic in the Activity**

- **The Smell:** Seeing `if (email.contains("@"))` or JSON parsing inside `MainActivity`.
- **The Danger:** **Tight Coupling.** You can't test that logic without an emulator. It belongs in the Domain layer or ViewModel.
- **The Fix:** Move logic to a Use Case or ViewModel.

**3. Hardcoded Dependencies (No DI)**

- **The Smell:** `private val repository = UserRepository()` inside the class.
- **The Danger:** **Untestable.** You cannot swap the real repository for a "FakeRepository" during testing.
- **The Fix:** Use Constructor Injection: `class ViewModel(private val repo: UserRepository)`.

**4. Exposing Mutable State**

- **The Smell:** `val state = MutableLiveData<String>()` (Public and Mutable).
- **The Danger:** **Data Corruption.** Any class (even the View) can accidentally change the data (`viewModel.state.value = "Garbage"`).
- **The Fix:** Encapsulation. `private val _state` (Mutable) and `val state` (Immutable/Read-only).

**5. "God" Functions**

- **The Smell:** A function that is 50+ lines long or has nested `if { if { if } }` blocks.
- **The Danger:** **Unreadable & Unmaintainable.**
- **The Fix:** Extract Logic. Break it into smaller private functions with clear names.

#### **Example (The "Trap" Code)**

**❌ The Bad Code (Can you spot the 3 smells?):**

```kotlin
class BadViewModel(context: Context) : ViewModel() { // Smell 1: Context

    val data = MutableLiveData<String>() // Smell 2: Public Mutable

    private val repo = MyRepository() // Smell 3: Hardcoded Dependency

    fun load() {
        if (NetworkUtils.isConnected(context)) { // Usage of Context
             data.value = repo.fetch()
        }
    }
}

```

**✅ The Fix:**

```kotlin
@HiltViewModel
class GoodViewModel @Inject constructor(
    private val repo: MyRepository // 3. Injection
    // 1. No Context here!
) : ViewModel() {

    private val _data = MutableLiveData<String>() // 2. Private Mutable
    val data: LiveData<String> = _data            // 2. Public Immutable

    fun load() {
        // Network checks should happen in Repository, not here!
        viewModelScope.launch {
            _data.value = repo.fetch()
        }
    }
}

```

#### **Interview Keywords**

Memory Leak, Dependency Injection, Inversion of Control, Encapsulation, Single Responsibility Principle, Tight Coupling, Context references.

#### **Interview Speak Paragraph**

> "When reviewing this code, I immediately notice three critical issues. First, the ViewModel is holding a reference to the `Context`, which will cause a memory leak because ViewModels outlive Activities. Second, it instantiates the Repository directly instead of using Dependency Injection, which makes unit testing impossible. Third, it exposes a `MutableLiveData` to the public, breaking encapsulation principles because the View should never be able to modify the state directly."

---

**Would you like to proceed to the next note: "The 'Over-Engineering' Trap"?** (Knowing when _not_ to use Clean Architecture).
