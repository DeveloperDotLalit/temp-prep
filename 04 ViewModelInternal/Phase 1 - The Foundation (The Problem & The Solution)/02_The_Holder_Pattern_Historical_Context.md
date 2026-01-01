---
layout: default
title: The Holder Pattern Historical Context
parent: ViewModel Internals: Phase 1   The Foundation (The Problem & The Solution)
nav_order: 2
grand_parent: ViewModel Internals
---

Here are your detailed notes for the second topic of Phase 1.

---

### **Topic: The "Holder" Pattern (Historical Context)**

#### **What It Is**

Before the `ViewModel` architecture existed, Android developers used a method called `onRetainNonConfigurationInstance()` to solve the rotation problem.

Think of this as a **"handoff"** maneuver. Just as the old Activity is dying, it hands a specific object (the "Holder") to the Android System. The System holds onto it safely while the Activity is destroyed. When the new Activity is created moments later, it reaches out and grabs that same object back from the System.

#### **Why It Exists (The Problem)**

We already had `onSaveInstanceState` (which saves data to a `Bundle`), but that had a major limitation: **Size and Type.**

- `onSaveInstanceState` only works for small data (Strings, Integers) because it has to be serialized (converted to bytes) to survive process death.
- You cannot put a large complex object (like a live Network Connection, a Database stream, or a Bitmap) into a Bundle.

We needed a way to keep **live, heavy objects** in memory during rotation without killing them. The "Holder" pattern was the manual way to do this.

#### **How It Works**

This was a manual two-step process handled directly in the Activity:

1. **The Handoff (Old Activity):**
   When the activity is about to be destroyed due to rotation, you override `onRetainNonConfigurationInstance()`. You return the object you want to save.
2. **The Retrieval (New Activity):**
   In the `onCreate()` of the new Activity, you call `getLastNonConfigurationInstance()`. If it returns an object, you cast it back to your data type and use it.

**Visualizing the Handoff:**

```text
[ Activity A (Dying) ]      [ Android System ]       [ Activity B (New) ]
          |                        |                          |
          |  "Here, hold this!"    |                          |
   (onRetainNonConfigurationInstance)                         |
          | ---------------------> |                          |
          |                        |                          |
          |                        |   "Give it back!"        |
          |                        | (getLastNonConfigurationInstance)
          |                        | <---------------------   |
          |                        |                          |
          |                        | --------------------->   |
          |                        |                          |

```

#### **Example: The "Custom Data" Holder**

Imagine you are downloading a list of users. You don't want to restart the download on rotation.

**Old Way Code (Simplified):**

```java
// inside MyActivity

// 1. Define a simple class to hold data
class MyDataHolder {
    List<User> userList;
    boolean isLoading;
}

// 2. Pass it to the system before death
@Override
public Object onRetainNonConfigurationInstance() {
    MyDataHolder data = new MyDataHolder();
    data.userList = this.currentUserList;
    return data;
}

// 3. Get it back in the new Activity
@Override
public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    MyDataHolder data = (MyDataHolder) getLastNonConfigurationInstance();

    if (data != null) {
        // We survived rotation! Use the old data.
        this.currentUserList = data.userList;
    } else {
        // This is a fresh start. Load data from scratch.
        loadData();
    }
}

```

#### **Why We Stopped Using It (The Flaws)**

While effective, this method was dangerous for beginners:

1. **Memory Leaks:** If you accidentally put a `View`, a `TextView`, or the `Activity Context` inside that `MyDataHolder` object, the old Activity could never be destroyed (garbage collected). This caused massive memory leaks.
2. **No Lifecycle Awareness:** The holder object didn't know if the user actually closed the app or just rotated it. You had to manage cleanup manually.
3. **Deprecated:** Google eventually deprecated this method in favor of ViewModels, which handle this logic internally and much safer.

#### **Interview Keywords**

onRetainNonConfigurationInstance, getLastNonConfigurationInstance, Deprecated, Memory Leaks, Hard Reference, Serialization.

#### **Interview Speak Paragraph**

> "Before ViewModels, we handled rotation by overriding `onRetainNonConfigurationInstance`. This allowed us to pass a live object from the dying Activity instance to the new one, bypassing the serialization limits of `onSaveInstanceState`. However, this approach was risky because it required manual management and easily led to memory leaks if the retained object held a reference to the Activity or a View. The ViewModel architecture essentially wraps this internal mechanism but makes it safer and lifecycle-aware."

---

**Next Step:**
Now that we know the history, shall we move to **Introduction to ViewModel** to see how the modern solution works?
