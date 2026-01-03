---
layout: default
title: "Shared Viewmodels"
parent: "Phase 6: Advanced MVVM Scenarios"
nav_order: 2
---

Here are your focused notes on **Shared ViewModels (Fragment Communication)**.

This is the modern, "Jetpack" way to handle communication between screens, replacing the old, messy way of using Interfaces and Bundles.

---

### **Topic: Shared ViewModels (Fragment Communication)**

#### **What It Is**

A **Shared ViewModel** is simply a ViewModel that is owned by the **Activity**, not the Fragment.

- Normal ViewModel: Dies when the Fragment dies.
- Shared ViewModel: Lives as long as the parent Activity lives.

Because multiple Fragments live inside the same Activity, they can all connect to this _same_ specific ViewModel instance. It acts as a "Common Room" where Fragments can leave messages for each other.

#### **Why It Exists (The Problem)**

1. **Passing Large Data:** You cannot pass large objects (like a full generic User object or a Bitmap) through Fragment arguments (Bundles) because there is a size limit (TransactionTooLargeException).
2. **Tight Coupling:** In the old days, Fragment A had to define an `Interface`, and the Activity had to implement it to talk to Fragment B. This was complex and fragile.
3. **Syncing State:** If you change data in the "Details" screen, the "List" screen needs to know. A Shared ViewModel keeps both updated automatically.

#### **How It Works (The Scope)**

The magic lies in **Scope**.

1. **Fragment A** asks for a ViewModel: _"Give me the one attached to the **Activity**."_
2. **Fragment B** asks for a ViewModel: _"Give me the one attached to the **Activity**."_
3. **System:** Since both asked for the Activity's instance, the system gives them the **exact same object**.

_Note: If Fragment A puts data in, Fragment B sees it immediately._

#### **Example (Master-Detail Flow)**

Imagine an Email app.

- **ListFragment:** Shows a list of emails. User clicks one.
- **DetailFragment:** Opens and shows the email body.

**The Shared ViewModel:**

```kotlin
class EmailViewModel : ViewModel() {
    // Both fragments watch this
    val selectedEmail = MutableLiveData<Email>()

    fun select(email: Email) {
        selectedEmail.value = email
    }
}

```

**Fragment A (The Sender - List):**

```kotlin
// "activityViewModels()" creates/finds the VM scoped to the Activity
private val sharedViewModel: EmailViewModel by activityViewModels()

fun onEmailClicked(email: Email) {
    // We don't launch a Bundle; we just update the Shared VM
    sharedViewModel.select(email)
    // Now navigate to the next screen...
}

```

**Fragment B (The Receiver - Details):**

```kotlin
// Connects to the SAME ViewModel instance
private val sharedViewModel: EmailViewModel by activityViewModels()

override fun onViewCreated(...) {
    // Data is already here waiting for us!
    sharedViewModel.selectedEmail.observe(viewLifecycleOwner) { email ->
        displayEmail(email)
    }
}

```

#### **Interview Keywords**

Activity Scope, `activityViewModels`, Fragment Communication, Single Source of Truth, TransactionTooLargeException, Decoupling.

#### **Interview Speak Paragraph**

> "I use Shared ViewModels for communication between Fragments. Instead of passing complex data via Bundles—which has size limits—or implementing messy interfaces in the Activity, I scope the ViewModel to the Activity lifecycle using the `by activityViewModels()` delegate. This allows multiple Fragments to observe the exact same instance of the ViewModel. It acts as a synchronized data holder: when the List Fragment updates the selected item, the Detail Fragment observes that change instantly, ensuring data consistency across screens."

---

**Would you like to proceed to the next note: "Concurrency & Race Conditions"?**
