---
layout: default
title: Collections: Mutable vs Immutable
parent: Phase 4   Functional Programming
nav_order: 3
---

﻿---
layout: default
title: "Collections: Mutable vs Immutable"
parent: "Functional Programming & Scoping"
nav_order: 3
---

# Collections: Mutable vs Immutable

<!-- Content starts here -->

Here are your interview-focused notes for **Collections (List, Set, Map)**.

---

### **Topic: Collections (List, Set, Map)**

#### **What It Is**

Collections are containers that hold multiple items. Kotlin provides three main types, and for each type, it offers **two versions** (Read-Only vs. Mutable).

1. **List:** An **ordered** collection. Elements have an index (0, 1, 2). Duplicates are allowed. (Like a shopping list).
2. **Set:** An **unordered** collection of **unique** elements. Duplicates are ignored. (Like a bag of marbles—you just care what's inside, not the order).
3. **Map:** A collection of **Key-Value pairs**. You look up value by its unique key. (Like a dictionary: Word -> Definition).

#### **Why It Exists**

**The "Immutability" Philosophy:**
In Java, `ArrayList` is always mutable. You pass a list to a function, and that function might secretly delete everything inside it. Scary!

Kotlin fixes this by splitting interfaces:

- **Immutable (Read-Only):** `List`, `Set`, `Map`. You can _read_ data, but you cannot add/remove/change it.
- **Mutable:** `MutableList`, `MutableSet`, `MutableMap`. You can read AND write.

**Why?** Safety. If you give someone a read-only `List`, you are 100% sure they cannot mess up your data.

#### **How It Works**

- **Creation:**
- `listOf(1, 2)` -> Read-Only.
- `mutableListOf(1, 2)` -> Mutable.

- **Conversion:** You can easily flip between them using `.toList()` or `.toMutableList()`.

#### **Example**

```kotlin
fun main() {
    // 1. LIST (Ordered, Duplicates OK)
    val readOnlyList = listOf("A", "B", "B")
    // readOnlyList.add("C") // ❌ ERROR: Unresolved reference 'add'

    val mutableList = mutableListOf("A", "B")
    mutableList.add("C") // ✅ Allowed

    // 2. SET (Unique items only)
    val numSet = mutableSetOf(1, 2, 2, 3)
    println(numSet) // Output: [1, 2, 3] (Duplicate '2' was ignored)

    // 3. MAP (Key-Value)
    val capitalMap = mutableMapOf("USA" to "DC", "France" to "Paris")
    capitalMap["Japan"] = "Tokyo" // Add new pair

    // 4. DEFENSIVE PROGRAMMING (The Interview Pro-Move)
    // We keep the mutable list PRIVATE so only this class can change it.
    // We expose a public Read-Only version to the outside world.
    val _data = mutableListOf<String>()
    val data: List<String> get() = _data
}

```

#### **Visual Representation**

```text
       Collection Type      Characteristics             Usage
    -------------------    -----------------------     ---------------------
    [ List ]               Ordered, Duplicates OK      "Top 10 Songs"
    [ Set  ]               Unordered, Unique only      "Active User IDs"
    [ Map  ]               Key -> Value Pairs          "User ID -> User Name"


    Immutable (Safe)       Mutable (Editable)
    ----------------       ------------------
    listOf()               mutableListOf()
    setOf()                mutableSetOf()
    mapOf()                mutableMapOf()

```

#### **Interview Keywords**

Immutable vs Mutable, `listOf` vs `mutableListOf`, Set Uniqueness, Key-Value Pair, Read-Only Interface, Defensive Copying.

> **Pro Interview Tip (Backing Properties):** If asked "How do you manage state in a ViewModel?", mention the **Backing Property** pattern shown in example #4. "I use a private `MutableList` (`_items`) to modify data internally, but expose a public immutable `List` (`items`) to the View. This ensures the View can observe the data but cannot accidentally modify it."

#### **Interview Speak Paragraph**

"I strictly distinguish between mutable and immutable collections to ensure data safety. By default, I use immutable collections like `List` or `Set` because they prevent accidental modification. When I need to modify data, I use `MutableList`, but I usually keep it `private` within the class. I then expose it to the outside world as a read-only `List`. This practice, known as using a 'Backing Property,' ensures that only the owning class can change the state, while other components can only read it."

---

**Would you like to move on to the next topic: Collection Operations (Filter, Map, FlatMap, Zip)?**
