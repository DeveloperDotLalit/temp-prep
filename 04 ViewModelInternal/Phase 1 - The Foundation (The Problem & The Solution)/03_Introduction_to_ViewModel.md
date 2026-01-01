---
layout: default
title: Introduction To Viewmodel
parent: Phase 1   The Foundation (The Problem & The Solution)
nav_order: 3
---

Here are your detailed notes for the third topic of Phase 1.

---

### **Topic: Introduction to ViewModel**

#### **What It Is**

The `ViewModel` is a class designed to store and manage UI-related data in a lifecycle-conscious way. Think of it as a **safe deposit box** for your screen's data.

Even if the "building" (your Activity or Fragment) collapses due to an earthquake (configuration change like rotation), the "safe deposit box" (ViewModel) stays intact. When the building is rebuilt, the new Activity simply opens the same box and finds all the data exactly where it was left.

#### **Why It Exists**

It solves the two main problems we discussed earlier:

1. **Data Persistence:** It keeps data alive during configuration changes without the complex manual work of the "Holder" pattern.
2. **Separation of Concerns:** It separates the **UI Controller** (Activity/Fragment) from the **Data**. The Activity should only worry about _displaying_ data (drawing views), while the ViewModel worries about _holding and fetching_ that data.

#### **How It Works**

The ViewModel has a unique lifespan that is longer than the Activity's lifespan in specific scenarios (rotation).

1. **Creation:** When an Activity first starts, it asks for a ViewModel.
2. **Survival:** If the user rotates the screen, the Activity is destroyed, but the **ViewModel remains in memory**.
3. **Reconnection:** When the new Activity starts, it asks for the ViewModel again. The system sees one already exists and hands over the **same instance**.
4. **Death:** The ViewModel is only cleared (destroyed) when the Activity is finished for good (e.g., the user presses the Back button or calls `finish()`).

**Visualizing the Lifespan:**

```text
Time -------------------------------------------------------------------->

[ Activity Lifecycle ]
Created -> Started -> Resumed -> [ROTATION] -> Destroyed -> (New) Created -> Resumed -> Finished -> Destroyed
                                     ^                           ^
                                     |                           |
[ ViewModel Lifecycle ]              |                           |
Created -----------------------------+---------------------------+----------------------------------> Cleared
                               (Remains Alive)                                                  (Dies here)

```

#### **Example: A Counter App**

Let's look at the standard "Counter" example. We want a number to stay on screen even if we rotate.

**The Code:**

```kotlin
// 1. Create the ViewModel class
class CounterViewModel : ViewModel() {
    // This variable sits safely inside the ViewModel
    var count = 0
}

// 2. Use it in the Activity
class MainActivity : AppCompatActivity() {

    // We don't say "new CounterViewModel()". We ask the Provider.
    private lateinit var viewModel: CounterViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // "Get me the ViewModel for this Activity"
        // If it's a fresh start, it creates one.
        // If it's a rotation, it returns the existing one.
        viewModel = ViewModelProvider(this).get(CounterViewModel::class.java)

        // Display the count.
        // Even after rotation, 'viewModel.count' remembers the old number.
        textView.text = viewModel.count.toString()
    }
}

```

#### **Interview Keywords**

Lifecycle-Aware, Separation of Concerns, UI State, ViewModelScope, Business Logic, Activity Re-creation.

#### **Interview Speak Paragraph**

> "The ViewModel is a class designed to store and manage UI-related data in a lifecycle-conscious way. Its primary role is to survive configuration changes, like screen rotations, allowing data to persist while the Activity is destroyed and recreated. This eliminates the need to reload data repeatedly and helps separate the UI logic from the data handling logic, resulting in a cleaner, more testable architecture."

---

**Next Step:**
Ready for the final topic of Phase 1? Let's cover **The Lifecycle Barrier** to visualize exactly _where_ the ViewModel sits in relation to the Activity.
