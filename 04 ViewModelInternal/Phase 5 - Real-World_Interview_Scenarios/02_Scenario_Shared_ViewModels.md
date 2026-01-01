---
layout: default
title: Scenario Shared Viewmodels
parent: ViewModel Internals: Phase 5   Real World Interview Scenarios
nav_order: 2
grand_parent: ViewModel Internals
---

Here are your detailed notes for the second topic of Phase 5.

This is the standard answer for the interview question: _"How do you communicate between Fragments?"_

---

### **Topic: Scenario: Shared ViewModels**

#### **What It Is**

A **Shared ViewModel** is a design pattern where multiple Fragments typically within the same screen (Activity) access the **exact same instance** of a ViewModel.

Instead of each Fragment having its own private data box, they both agree to use the "Family Safe" located in the living room (the parent Activity).

#### **Why It Exists (The Problem)**

Communicating between Fragments used to be very hard.

- **Old Way:** Fragment A defines an Interface -> Activity implements it -> Activity calls method on Fragment B. This is complex, brittle, and creates tight coupling.
- **Bundle Way:** Fragment A passes arguments to Fragment B. This works for sending data _once_, but not for real-time updates (e.g., a Split Screen where clicking a list updates the details immediately).

Shared ViewModel allows **real-time, decoupled communication**. Fragment A doesn't even need to know Fragment B exists. They just both talk to the ViewModel.

#### **How It Works**

The magic lies in the **Scope** (the `ViewModelStoreOwner`).

1. **Fragment A** asks for a ViewModel using `requireActivity()` as the owner.
2. **Fragment B** asks for the _same class_ of ViewModel using `requireActivity()` as the owner.
3. **The Provider** sees that the Owner (Activity) already has an instance of that ViewModel.
4. **Result:** Both Fragments receive a reference to the **same object**.
5. **Communication:** Fragment A sets a value; Fragment B observes it and updates immediately.

**Visualizing the Triangle:**

```text
       [ Parent Activity (The Owner) ]
                  ^
                  | owns
                  v
       [ Shared ViewModel Instance ]
       |   liveData: SelectedItem  |
       +-------------+-------------+
                     ^
        (Observes)   |   (Updates)
      +--------------+--------------+
      |                             |
[ DetailFragment ]             [ ListFragment ]
 "I see the change!"            "User clicked item 5"

```

#### **Example: Master-Detail View (List & Details)**

**1. The Shared ViewModel**

```kotlin
class SharedViewModel : ViewModel() {
    // LiveData to hold the selected user
    private val _selectedUser = MutableLiveData<User>()
    val selectedUser: LiveData<User> = _selectedUser

    fun select(user: User) {
        _selectedUser.value = user
    }
}

```

**2. ListFragment (The Sender)**

```kotlin
class ListFragment : Fragment() {
    // ⚠️ KEY: Use 'requireActivity()' to get the Activity's scope
    private val model: SharedViewModel by activityViewModels()
    // OR: ViewModelProvider(requireActivity()).get(...)

    fun onListItemClick(user: User) {
        // Update the shared data
        model.select(user)
    }
}

```

**3. DetailFragment (The Receiver)**

```kotlin
class DetailFragment : Fragment() {
    // ⚠️ KEY: Also use 'requireActivity()'
    private val model: SharedViewModel by activityViewModels()

    override fun onViewCreated(...) {
        // Observe the SAME data
        model.selectedUser.observe(viewLifecycleOwner) { user ->
            // Update UI immediately
            displayUserDetails(user)
        }
    }
}

```

#### **Interview Keywords**

Fragment Communication, Decoupling, `requireActivity()`, `activityViewModels()` Delegate, Single Source of Truth, Observer Pattern, Scope.

#### **Interview Speak Paragraph**

> "The most robust way for Fragments to communicate is using a Shared ViewModel. Instead of instantiating a ViewModel scoped to the Fragment itself, both Fragments request a ViewModel scoped to their parent Activity using `requireActivity()` or the `by activityViewModels()` delegate. Because they pass the same `ViewModelStoreOwner` (the Activity), the `ViewModelProvider` returns the exact same instance to both Fragments. This allows Fragment A to update `LiveData` or `StateFlow` within the ViewModel, and Fragment B to observe those changes instantly, decoupling the Fragments completely from each other."

---

**Next Step:**
We've handled sharing data. Now, let's talk about navigation.
Shall we move to **Scenario: Navigation Graph Scoping**: How ViewModels live and die within specific flows?
