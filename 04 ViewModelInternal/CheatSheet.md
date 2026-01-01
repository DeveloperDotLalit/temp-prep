---
layout: default
title: "Cheatsheet"
parent: "ViewModel"
---

Here is your **Master Cheat Sheet** for Android ViewModel Internals. This condenses everything we have covered into a single, high-density reference guide.

Use this for your final review 15–30 minutes before the interview.

---

### **Android ViewModel Internals: The Ultimate Interview Cheat Sheet**

#### **1. The Elevator Pitch (The "What" & "Why")**

> "The ViewModel is a lifecycle-aware component designed to store and manage UI-related data. Its primary purpose is to survive **Configuration Changes** (like screen rotation) so data isn't lost when the Activity is recreated. It decouples the UI (Activity/Fragment) from the Data, preventing memory leaks and keeping code testable."

#### **2. The Internals (Under the Hood)**

- **ViewModelStore:** The `HashMap` that holds the actual ViewModel instances in memory.
- **ViewModelStoreOwner:** The Interface (implemented by Activity/Fragment) that says "I own a Store."
- **ViewModelProvider:** The Utility class that implements the "Get existing OR Create new" logic.
- **NonConfigurationInstances:** The "Secret Sauce." The internal mechanism where the Activity passes the `ViewModelStore` to the System during rotation, allowing it to bypass destruction.

**The Flow:**
`Activity Rotates` → `onRetainNonConfigurationInstance()` saves Store → `Activity Dies` → `New Activity` → `onCreate` gets Store back → `Provider` finds existing VM in Store.

#### **3. The Lifecycle Survival Matrix**

_Memorize this table. It answers 50% of tricky questions._

| Event                        | Activity Status         | ViewModel Status              | Memory Status                        |
| ---------------------------- | ----------------------- | ----------------------------- | ------------------------------------ |
| **Rotation** (Config Change) | Destroyed & Recreated   | **ALIVE** (Survives)          | Kept in RAM (Heap)                   |
| **Back Button** (Finish)     | Destroyed (Permanently) | **DEAD** (`onCleared` called) | Garbage Collected                    |
| **Home Button** (Background) | Stopped                 | **ALIVE** (Paused)            | Kept in RAM                          |
| **Process Death** (Low RAM)  | Destroyed (System Kill) | **DEAD** (Wiped)              | **LOST** (Unless `SavedStateHandle`) |

#### **4. The "Red Flags" (Instant Rejection Traps)**

- ❌ **Holding a View:** Never hold `TextView`, `Button`, or `ListAdapter` in a VM. (Leak!)
- ❌ **Holding Activity Context:** Never pass `this` (Activity) to a VM. (Leak!)
- _Fix:_ Use `AndroidViewModel(application)` if you need a Context.

- ❌ **Manual Lifecycle Handling:** Don't try to save/restore rotation state manually in the Activity if you have a ViewModel.
- ❌ **Ignoring Process Death:** Assuming "ViewModel survives everything." (It doesn't survive System Kill).

#### **5. Essential Patterns & Code**

**A. The Factory (Passing Dependencies)**
Used when your ViewModel needs arguments (like a Repository).

```kotlin
class MyFactory(val repo: Repository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return MyViewModel(repo) as T
    }
}
// Usage: ViewModelProvider(this, MyFactory(repo)).get(...)
// Modern Usage: Use Hilt (@HiltViewModel) to generate this automatically.

```

**B. Shared ViewModel (Fragment Communication)**
Two fragments, same data.

```kotlin
// In Fragment A AND Fragment B:
// Use 'requireActivity()' to scope to the Parent Activity
val sharedVM = ViewModelProvider(requireActivity()).get(SharedVM::class.java)

```

**C. Process Death Safety (SavedStateHandle)**
Surviving system kills.

```kotlin
class MyVM(private val handle: SavedStateHandle) : ViewModel() {
    // Read/Write directly to this handle
    val query = handle.getLiveData("key_query")
    fun save(text: String) { handle["key_query"] = text }
}

```

**D. Coroutines (Heavy Operations)**
Auto-cancellation.

```kotlin
fun loadData() {
    // Automatically cancels when ViewModel is cleared
    viewModelScope.launch {
        val data = repository.fetch()
    }
}

```

#### **6. Interview "Power Words"**

_Sprinkle these into your answers to sound senior._

- **Structured Concurrency** (Why we use `viewModelScope`)
- **Separation of Concerns** (Why we separate UI and Data)
- **Single Source of Truth** (The ViewModel holds the data, UI just observes)
- **Transient State** (Data that lives in memory, lost on process death)
- **Inversion of Control** (The UI observes the VM, the VM doesn't drive the UI)
- **Dependency Injection** (How we get Repositories into VMs)

---

**Final Tip:**
If you get stuck, draw the **Lifecycle Barrier**.
Draw a line. Put **Activity** on the left (Chaos/Recreation). Put **ViewModel** on the right (Stability). Explain that the ViewModel sits _outside_ the chaotic lifecycle of the View.
