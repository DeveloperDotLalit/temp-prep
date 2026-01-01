---
layout: default
title: Viewmodelstore
parent: ViewModel Internals: Phase 2   The Core Internals (How It Survives)
nav_order: 2
grand_parent: ViewModel Internals
---

Here are your detailed notes for the second topic of Phase 2.

---

### **Topic: ViewModelStore**

#### **What It Is**

The `ViewModelStore` is effectively a specialized **storage box**.

In technical terms, it is a very simple class that wraps a `HashMap`. This map holds the actual instances of your ViewModels in memory.

If `ViewModelStoreOwner` is the person who _owns_ the safe, `ViewModelStore` is the **safe itself** where the valuables (ViewModels) are kept.

#### **Why It Exists**

We need a concrete place to hold references to the ViewModels.

- If we just held them in a variable in the Activity (`var myVM = ...`), they would be destroyed on rotation.
- We need a separate object (the Store) that can be detached from the dying Activity and re-attached to the new one.
- It also provides a central place to clean up. When the Activity is finally finished, we just need to call `clear()` on this one Store, and it will automatically clean up all the ViewModels inside it.

#### **How It Works**

It works like a standard dictionary or lookup table.

1. **Storage:** When you create a ViewModel, it is saved into this map using a specific **String Key**.
2. **Retrieval:** When you ask for the ViewModel later, the system looks up that String Key in the map.
3. **Cleanup:** It has a `clear()` method. When called, it iterates through the map and calls `onCleared()` on every single ViewModel inside, then empties the map.

**Visualizing the Internals:**

```text
[ ViewModelStore Object ]
+-------------------------------------------------------------+
|  Internal HashMap <String, ViewModel>                       |
|                                                             |
|  Key (String)                       Value (Instance)        |
|  ---------------------------------  ----------------------  |
|  "androidx...UserViewModel"   --->  [ UserViewModel Object ]|
|  "androidx...CartViewModel"   --->  [ CartViewModel Object ]|
|  "custom_key_for_vm"          --->  [ SpecialViewModel Obj ]|
|                                                             |
+-------------------------------------------------------------+
       |
       | clear() method called?
       v
   Loop through all values -> call viewModel.onCleared()

```

#### **Example: A Conceptual Implementation**

The actual code inside the Android SDK is surprisingly simple. It looks almost exactly like this:

```java
public class ViewModelStore {

    // 1. The Map that holds everything
    private final HashMap<String, ViewModel> mMap = new HashMap<>();

    // 2. Put a ViewModel in (Save it)
    final void put(String key, ViewModel viewModel) {
        ViewModel oldViewModel = mMap.put(key, viewModel);
        if (oldViewModel != null) {
            oldViewModel.onCleared();
        }
    }

    // 3. Get a ViewModel out (Retrieve it)
    final ViewModel get(String key) {
        return mMap.get(key);
    }

    // 4. Destroy everything (Cleanup)
    public final void clear() {
        for (ViewModel vm : mMap.values()) {
            vm.onCleared(); // <--- This is where your onCleared() gets triggered!
        }
        mMap.clear();
    }
}

```

#### **Interview Keywords**

HashMap, Key-Value Pair, Caching, Retention, Cleanup, Memory Management, `onCleared()`.

#### **Interview Speak Paragraph**

> "The `ViewModelStore` is the internal container that actually holds the ViewModel instances. Under the hood, it's essentially a wrapper around a HashMap where ViewModels are stored as values against string keys. This structure allows the `ViewModelProvider` to quickly check if a ViewModel already exists for a given key. Crucially, the `ViewModelStore` is also responsible for the cleanup process; when its `clear()` method is triggered by the lifecycle owner, it iterates through all stored ViewModels and executes their `onCleared()` methods to free up resources."

---

**Next Step:**
We have the **Owner** and the **Store**. Now we need the middleman who puts things in and takes things out.
Shall we move to **ViewModelProvider**: The utility class you use to get a ViewModel?
