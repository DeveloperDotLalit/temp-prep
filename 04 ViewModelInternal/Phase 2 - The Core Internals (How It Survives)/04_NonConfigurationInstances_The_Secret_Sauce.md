---
layout: default
title: "Nonconfigurationinstances The Secret Sauce"
parent: "ViewModel Internals: Phase 2   The Core Internals (How It Survives)"
nav_order: 4
grand_parent: ViewModel Internals
---

Here are your detailed notes for the final topic of Phase 2. This is the deepest part of the internals—the "Secret Sauce."

---

### **Topic: The `NonConfigurationInstances` (The Secret Sauce)**

#### **What It Is**

`NonConfigurationInstances` is a special internal class (wrapper) used by the Android System to pass live objects from a dying Activity to a newly created one during a configuration change.

Think of it as the **"Baton"** in a relay race.

- The **Old Activity** (Runner 1) is about to stop.
- It hands the **Baton** (NonConfigurationInstances) to the System (The Judge).
- The **New Activity** (Runner 2) starts running and immediately grabs the **Baton** from the System.

Crucially, the `ViewModelStore` is hidden inside this baton.

#### **Why It Exists**

We learned earlier that `onSaveInstanceState` (Bundles) cannot hold complex objects like the `ViewModelStore`.
This mechanism exists specifically to bypass that limitation. It keeps the objects in **RAM (Heap Memory)** without serializing them. This is the only way the `ViewModelStore` (and thus your ViewModels) stays alive while the Activity object itself is garbage collected.

#### **How It Works**

This logic happens deep inside `ComponentActivity` (the parent of `AppCompatActivity`).

1. **The Trigger:** You rotate the screen. The system prepares to destroy the Activity.
2. **The Save:** The system calls the internal method `onRetainNonConfigurationInstance()`.

- The Activity creates a `NonConfigurationInstances` object.
- It puts the **current `ViewModelStore**` inside it.
- It returns this object to the System.

3. **The Handoff:** The Activity is destroyed, but the System holds onto this one `NonConfigurationInstances` object tightly.
4. **The Restore:** The new Activity is created (`onCreate`).

- It immediately calls `getLastNonConfigurationInstance()`.
- It extracts the `ViewModelStore` from the returned object.
- It assigns this old store to its own internal field.

**Visualizing the Baton Pass:**

```text
      [ OLD ACTIVITY INSTANCE ]                  [ NEW ACTIVITY INSTANCE ]
      +-----------------------+                  +-----------------------+
      |                       |                  |                       |
      |   ViewModelStore      |                  |   ViewModelStore      |
      |   (The "Treasure")    |                  |   (Empty at first)    |
      +-----------------------+                  +-----------------------+
                 |                                           ^
                 | (1) onRetainNonConfigurationInstance()    |
                 v                                           | (3) getLast...()
      +-----------------------+                  +-----------------------+
      | NonConfigurationInstances                | NonConfigurationInstances
      | (The "Baton")         | ---------------->| (The "Baton")         |
      | contains: Store       |      (2)         | contains: Store       |
      +-----------------------+    System        +-----------------------+
                                   keeps
                                  in RAM

```

#### **Example: Inside the Source Code (Simplified)**

This is roughly what the Android SDK code looks like inside `ComponentActivity.java`:

```java
// Inside ComponentActivity.java

// 1. Holding the store
private ViewModelStore mViewModelStore;

// 2. Saving the store when rotation starts
@Override
public final Object onRetainNonConfigurationInstance() {
    // Create the container
    NonConfigurationInstances nci = new NonConfigurationInstances();

    // Put the store inside
    nci.viewModelStore = mViewModelStore;

    return nci;
}

// 3. Restoring the store when new Activity starts
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    // Ask the system: "Did anyone leave a baton for me?"
    NonConfigurationInstances nci =
        (NonConfigurationInstances) getLastNonConfigurationInstance();

    if (nci != null) {
        // Yes! Restore the store.
        mViewModelStore = nci.viewModelStore;
    }
}

```

#### **Interview Keywords**

`onRetainNonConfigurationInstance`, `getLastNonConfigurationInstance`, Heap Memory, Object Reference, ComponentActivity, System Server, State Restoration.

#### **Interview Speak Paragraph**

> "The secret mechanism that allows ViewModels to survive rotation is the `NonConfigurationInstances` class. When an Activity is destroyed due to a configuration change, the `ComponentActivity` overrides `onRetainNonConfigurationInstance`. It bundles the active `ViewModelStore` into a special container object and passes it to the system. This object remains in memory (RAM) and is not destroyed. When the new Activity instance is created, it calls `getLastNonConfigurationInstance` to retrieve this container, extracts the `ViewModelStore`, and re-attaches it. This is why the new Activity sees the exact same ViewModel instances as the old one."

---

**Phase 2 Complete!**
You now understand the "Magic" inside the box. You know about the Owner, the Store, the Provider, and the secret Handshake that keeps it alive.

**Next Step:**
We are moving to **Phase 3: Creation & Dependency Injection**. This is practical, "Day-to-Day Coding" knowledge.
Shall we start with **ViewModelFactory (The Builder Pattern)**: Why we can't just say `new ViewModel()`?
