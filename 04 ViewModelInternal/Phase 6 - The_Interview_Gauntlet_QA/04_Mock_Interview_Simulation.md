---
layout: default
title: "Mock Interview Simulation"
parent: "Phase 6: The Interview Gauntlet"
nav_order: 4
---

Here are your **Mock Interview Simulation** notes. This is your "Cheat Sheet"—a condensed version of everything we’ve covered, designed for rapid review 15 minutes before your interview.

---

### **Section 1: The Warm-Up (Basics)**

#### **Q1: "What is a ViewModel and why do we need it?"**

- **The Hook:** "It’s a lifecycle-aware data holder."
- **Key Points:**
- It separates UI logic (Activity/Fragment) from Data logic.
- **The Problem:** Activities are destroyed on configuration changes (like rotation).
- **The Solution:** ViewModel survives this destruction, preserving data so we don't have to re-fetch it.

- **Keyword Drop:** Separation of Concerns, Configuration Change, Transient Data.

#### **Q2: "What is the difference between `onSaveInstanceState` and ViewModel?"**

- **The Hook:** "Storage size and data types."
- **Key Points:**
- `onSaveInstanceState` (Bundles) is for **small amounts of data** (IDs, Strings) needed to restore state after process death. It requires serialization.
- ViewModel is for **large, complex objects** (Live Lists, Bitmap, Database streams) in memory.

- **Keyword Drop:** Serialization limits, Process Death vs. Rotation.

---

### **Section 2: The Internals (Senior Level)**

#### **Q3: "How does the ViewModel actually survive rotation internally?"**

- **The Hook:** "Through the `NonConfigurationInstances` mechanism."
- **Key Points:**

1. **The Container:** ViewModels are stored in a `ViewModelStore` (a HashMap).
2. **The Handoff:** When Activity rotates, it passes this Store to the System via `onRetainNonConfigurationInstance`.
3. **The Restore:** The new Activity grabs this Store back from the System in `onCreate`.

- **Keyword Drop:** `ViewModelStore`, `ViewModelStoreOwner`, System Server.

#### **Q4: "What is the role of the `ViewModelProvider`?"**

- **The Hook:** "It’s the broker or factory logic."
- **Key Points:**
- It implements the **'Get or Create'** logic.
- Checks the `ViewModelStore` using a canonical key.
- If found → Returns existing instance.
- If missing → Uses a `Factory` to create a new one, saves it, then returns it.

---

### **Section 3: The Traps (Red Flags)**

#### **Q5: "Can I pass a View or Activity Context to a ViewModel?"**

- **The Hook:** "Absolutely not. That’s a guaranteed memory leak."
- **Key Points:**
- ViewModel lives **longer** than the Activity.
- If ViewModel holds the Activity, the Garbage Collector cannot clean up the Activity.
- **Fix:** Use `AndroidViewModel` for Application Context, or expose streams (`LiveData`) for the View to observe.

- **Keyword Drop:** GC Roots, Strong Reference, OutOfMemoryError, Lifecycle Mismatch.

#### **Q6: "Does the ViewModel survive if I press the Back button?"**

- **The Hook:** "No, it dies."
- **Key Points:**
- Back button = `Activity.finish()` (Permanent destruction).
- System calls `store.clear()`.
- ViewModel’s `onCleared()` is triggered to clean up resources.
- It only survives **Configuration Changes**, not **Finishing**.

---

### **Section 4: The Edge Cases (Process Death)**

#### **Q7: "What happens to the ViewModel if the System kills the app (Low Memory)?"**

- **The Hook:** "The ViewModel is destroyed."
- **Key Points:**
- This is **Process Death**, not rotation. Everything in RAM is wiped.
- To survive this, we must use **`SavedStateHandle`**.
- This allows us to persist keys/values into the OS Bundle directly from the ViewModel.

- **Keyword Drop:** System-Initiated Process Death, `SavedStateHandle`, State Restoration.

---

### **Section 5: Architecture & Scenarios**

#### **Q8: "How do two Fragments communicate?"**

- **The Hook:** "Shared ViewModel pattern."
- **Key Points:**
- Both Fragments request a ViewModel using the **Activity scope** (`requireActivity()`).
- They receive the **same instance**.
- Fragment A writes to `LiveData`; Fragment B observes it.

- **Keyword Drop:** `activityViewModels()` delegate, Single Source of Truth, Decoupling.

#### **Q9: "Why MVVM over MVP?"**

- **The Hook:** "Lifecycle safety."
- **Key Points:**
- **MVP:** Presenter holds reference to View. Risky (NullPointerExceptions on rotation).
- **MVVM:** ViewModel holds **no** reference to View. It exposes Observables.
- The View observes the ViewModel. If the View dies, it just stops observing. No crashes.

- **Keyword Drop:** Inversion of Control, Observer Pattern, Testability.

---

### **Review: Your Final "Cheat Sheet" Table**

| Concept                | Key "Senior" Terminology                      |
| ---------------------- | --------------------------------------------- |
| **Why ViewModel?**     | Preserves state across Configuration Changes. |
| **Internal Storage**   | `ViewModelStore` (HashMap).                   |
| **Survival Mechanism** | `NonConfigurationInstances` (The Handoff).    |
| **Creation Logic**     | `ViewModelProvider` + `Factory` pattern.      |
| **Memory Leak**        | Never hold `View` or `Activity` context.      |
| **Process Death**      | Use `SavedStateHandle` (RAM is wiped).        |
| **Communication**      | Scope to `requireActivity()` (Shared VM).     |
| **Cleanup**            | `onCleared()` (Cancel Coroutines/RxJava).     |

---

**Coach's Final Note:**
You are ready. You aren't just memorizing code; you understand the **Lifecycle**, the **Memory Model**, and the **Architecture**.

- If you get stuck, remember the **"Lifecycle Barrier"** diagram.
- If they ask about leaks, remember the **"Zombie Activity."**

**Would you like me to start a new topic, or drill specifically into one of these questions deeper?**
