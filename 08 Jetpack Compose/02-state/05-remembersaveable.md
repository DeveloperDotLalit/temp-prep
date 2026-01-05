---
layout: default
title: rememberSaveable
parent: 2. State & Recomposition (The Core)
nav_order: 5
---

# rememberSaveable

Here are your notes for **Topic 2.5**.

---

## **Topic 2.5: rememberSaveable**

### **1. What It Is**

`rememberSaveable` is a specialized version of `remember`.
While `remember` keeps your data alive while the app is running, `rememberSaveable` keeps your data alive even if the **Activity is destroyed and recreated**.

### **2. Why It Exists (The Rotation Problem)**

- **The Scenario:** You have a counter at 5. You rotate your phone from Portrait to Landscape.
- **The Crash (with `remember`):** Android destroys the entire Activity to reload resources (layouts, strings) for the new orientation. Your `remember` cache is wiped out. The counter resets to 0.
- **The Fix (`rememberSaveable`):** It saves your value into the Android `Bundle` (the standard `onSaveInstanceState` mechanism). When the Activity restarts, it restores the value from the bundle.

### **3. How It Works**

It automatically saves simple types (Int, String, Boolean, etc.) because they are already supported by the Android Bundle.

**Comparison:**

- `val x = remember { mutableStateOf(0) }` -> Survives Recomposition. dies on Rotation.
- `val x = rememberSaveable { mutableStateOf(0) }` -> Survives Recomposition AND Rotation (and Process Death).

### **4. Handling Custom Objects**

If you try to save a custom class (like `User`), the app will crash because Android doesn't know how to put a `User` object into a Bundle. You have three solutions:

#### **A. The Easy Way: @Parcelize (Recommended)**

Annotate your data class with `@Parcelize` and implement `Parcelable`.

```kotlin
@Parcelize
data class User(val name: String, val age: Int) : Parcelable

// Now rememberSaveable handles it automatically!
val user = rememberSaveable { mutableStateOf(User("Alex", 25)) }

```

#### **B. The Manual Way: MapSaver**

If you can't modify the class (e.g., it's from a library), you define how to convert it to a Map.

```kotlin
val UserSaver = run {
    val nameKey = "Name"
    val ageKey = "Age"
    mapSaver(
        save = { mapOf(nameKey to it.name, ageKey to it.age) },
        restore = { User(it[nameKey] as String, it[ageKey] as Int) }
    )
}

val user = rememberSaveable(stateSaver = UserSaver) { mutableStateOf(User("Alex", 25)) }

```

#### **C. The List Way: ListSaver**

Similar to MapSaver, but saves data as a list of values (indices matter).

```kotlin
val UserSaver = listSaver<User, Any>(
    save = { listOf(it.name, it.age) },
    restore = { User(it[0] as String, it[1] as Int) }
)

```

### **5. Example: The Rotation Test**

```kotlin
@Composable
fun RotationCounter() {
    // 1. DIES on rotation
    var basicCount by remember { mutableStateOf(0) }

    // 2. SURVIVES rotation
    var persistentCount by rememberSaveable { mutableStateOf(0) }

    Column {
        Text("I forget easily: $basicCount")
        Button(onClick = { basicCount++ }) { Text("Add") }

        Spacer(Modifier.height(20.dp))

        Text("I remember everything: $persistentCount")
        Button(onClick = { persistentCount++ }) { Text("Add") }
    }
}

```

### **6. Interview Prep**

**Interview Keywords**
Configuration Change, Bundle, Parcelable, Process Death, Serialization, Bundle Limits (TransactionTooLargeException).

**Interview Speak Paragraph**

> "`remember` is sufficient for preserving state during recomposition, but it fails during configuration changes like screen rotation because the Activity is recreated. To solve this, I use `rememberSaveable`. It leverages the underlying Android `savedInstanceState` mechanism to serialize data into a Bundle and restore it after the Activity recreates. For primitive types, it works out of the box; for custom objects, I usually annotate the class with `@Parcelize` or write a custom `MapSaver` if I don't own the class definition."

---

**Next Step:**
We can save state, but what if we want to _calculate_ state efficiently?
Ready for **Topic 2.6: derivedStateOf**? This is a huge performance optimizer for scrolling and animations.

---

## Navigation

â† Previous
Next â†’
