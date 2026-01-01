---
layout: default
title: "Scenario Navigation Graph Scoping"
parent: "ViewModel Internals: Phase 5   Real World Interview Scenarios"
nav_order: 3
grand_parent: ViewModel Internals
---

Here are your detailed notes for the third topic of Phase 5.

This is a **Senior-level** topic. It shows you know how to handle complex flows, not just single screens.

---

### **Topic: Scenario: Navigation Graph Scoping**

#### **What It Is**

Navigation Graph Scoping is a technique where you create a ViewModel that lives only while the user is inside a specific **group of screens** (a Navigation Graph).

It sits right in the middle between the two scopes we already know:

1. **Fragment Scope:** Too short (dies when you move to the next screen).
2. **Activity Scope:** Too long (lives for the entire app session, keeping "Checkout Data" in memory even when you are browsing the home page).
3. **NavGraph Scope:** Just right (lives while in the "Checkout" flow, dies when you finish).

#### **Why It Exists (The Problem)**

Imagine a **Checkout Flow**:

- **Screen A:** Address Input
- **Screen B:** Payment Input
- **Screen C:** Confirm Order

**The Challenge:**

- You need to share data (Address) from Screen A to Screen C.
- If you use `activityViewModels()`, the "Address" stays in memory even after the user finishes the order and goes back to the Home screen. This is dirty.
- You want the data to exist **only** while the user is in this 3-screen process.

#### **How It Works**

We use the **Jetpack Navigation Component**.

1. **Group:** You define a "Nested Graph" in your XML navigation file (e.g., `<navigation android:id="@+id/checkout_graph">`).
2. **Owner:** This graph itself acts as a `ViewModelStoreOwner`.
3. **The Hook:** Instead of asking the Activity for the ViewModel, you ask the **Graph**.

- When you enter the graph: The ViewModel is created.
- When you navigate between A, B, and C: The ViewModel stays alive.
- When you exit the graph (finish or back out): The ViewModel is cleared.

**Visualizing the Scopes:**

```text
APP TIMELINE ------------------------------------------------------------------------>

[ HOME SCREEN ]   [ CHECKOUT FLOW (The Graph) ]               [ HOME SCREEN ]
                  ( Enters Graph )                            ( Exits Graph )
    |             |                                           |
    |             +-------------------------------------------+
    |             |  CheckoutViewModel (Alive)                |
    |             |  - Address                                |
    |             |  - Card Info                              |
    |             +-------------------------------------------+
    |                                                         |
    |             [ Screen A ] -> [ Screen B ] -> [ Screen C ]|
    |                                                         |
ViewModel         ViewModel CREATED                           ViewModel CLEARED
Does Not Exist                                                (Memory Freed)

```

#### **Example: The Checkout Flow**

**1. The Navigation XML (`nav_graph.xml`)**
We wrap our checkout fragments in a nested graph with the ID `checkout_graph`.

```xml
<navigation android:id="@+id/nav_graph" ...>

    <navigation android:id="@+id/checkout_graph" startDestination="@id/addressFragment">
        <fragment android:id="@+id/addressFragment" .../>
        <fragment android:id="@+id/paymentFragment" .../>
        <fragment android:id="@+id/reviewFragment" .../>
    </navigation>

</navigation>

```

**2. The Fragment Code (Kotlin)**
Inside _any_ of the checkout fragments (Address, Payment, or Review), you use the `navGraphViewModels` delegate.

```kotlin
class PaymentFragment : Fragment() {

    // ⚠️ KEY: Scope to the ID of the nested graph
    private val checkoutViewModel: CheckoutViewModel by navGraphViewModels(R.id.checkout_graph) {
        defaultViewModelProviderFactory
    }

    fun onSavePayment() {
        // This data is visible to AddressFragment and ReviewFragment too!
        checkoutViewModel.saveCard("1234-5678")
    }
}

```

#### **Interview Keywords**

Nested Navigation Graph, `NavBackStackEntry`, `navGraphViewModels`, Intermediate Scope, Flow Data, Modularization.

#### **Interview Speak Paragraph**

> "For multi-screen flows like a checkout or a registration wizard, relying on Activity-scoped ViewModels is inefficient because it keeps data in memory longer than necessary. Instead, I use **Navigation Graph Scoping**. By grouping related fragments into a nested navigation graph, I can use the `by navGraphViewModels(R.id.graph_id)` delegate. This creates a ViewModel that is scoped specifically to that navigation graph's `NavBackStackEntry`. It ensures the data persists while the user navigates between the steps of the flow but is automatically cleared from memory as soon as the user completes or exits the flow."

---

**Next Step:**
We have one final scenario before the main "Interview Gauntlet."
Shall we move to **Scenario: Heavy Operations**: Handling coroutines in `ViewModelScope` and ensuring they cancel correctly?
