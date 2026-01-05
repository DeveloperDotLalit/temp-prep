---
layout: default
title: Why Compose vs XML?
parent: 1. Introduction + Basic Composables
nav_order: 2
---

# Why Compose vs XML?

Here are your notes for **Topic 1.2**.

---

## **Topic 1.2: Why Compose (vs XML)?**

### **1. What It Is**

This topic covers the tangible benefits of switching to Jetpack Compose. It isn't just "newer"; it fundamentally removes the friction points developers hated about Android development for the last decade. It unifies your tech stack (Kotlin everywhere) and drastically reduces the amount of code you write.

### **2. Why It Exists (The Problems with XML)**

To appreciate Compose, look at the headaches the XML View System gave us:

- **Context Switching:** You constantly jumped between XML files (layout) and Kotlin files (logic). This broke your mental flow.
- **Boilerplate Code:** To make a simple list of items, you needed an Adapter, a ViewHolder, an XML layout for the item, and an XML layout for the container. That's 4 files for 1 list!
- **Coupling:** The XML had no idea what the Kotlin code was doing. If you renamed a variable in Kotlin, the XML didn't update automatically, often leading to runtime crashes.

### **3. How It Works (The Key Advantages)**

**A. Less Code (The "LazyColumn" Magic)**
Compose allows you to do more with less. The most famous example is lists.

- _XML:_ Requires `RecyclerView`, `Adapter`, `ViewHolder`, `xml_item.xml`. (~50+ lines of code).
- _Compose:_ Requires `LazyColumn`. (~5 lines of code).

**B. Kotlin Integration (Power of the Language)**
In XML, logic was limited. You had to use special attributes like `android:visibility="gone"`.
In Compose, you just use standard Kotlin code.

- Want to hide something? Use an `if` statement.
- Want a list? Use a `for` loop (or `items` function).
- Want to format text? Use Kotlin string templates.

**C. Unbundled Libraries**

- _Old Way:_ The `View` class is baked into the Android OS on the user's phone. If Google adds a new feature to `TextView`, only users on the newest Android version (e.g., Android 14) get it.
- _Compose Way:_ Compose is a **library** you add in `build.gradle`. If a new feature comes out, you update the library version, and **all** your users get it, even those on older phones (back to Android 5.0/Lollipop).

**D. Live Previews**
In XML, the preview was static. In Compose, the `@Preview` annotation lets you see your component in different states (Dark Mode, different font sizes, different data) simultaneously inside Android Studio without running the app on a device.

### **4. Example: The RecyclerView vs. LazyColumn Comparison**

**The Old XML Way (Conceptually):**

1. Create `activity_main.xml` (add RecyclerView).
2. Create `list_item.xml` (design the row).
3. Create `MyAdapter.kt` (inflate XML, bind data, count items).
4. Create `MyViewHolder.kt` (hold references to views).
5. In `MainActivity.kt`, connect Adapter to RecyclerView.

**The Compose Way:**

```kotlin
// That's it. This replaces the Adapter, ViewHolder, and XMLs.
@Composable
fun NameList(names: List<String>) {
    LazyColumn {
        items(names) { name ->
            Text(text = name, modifier = Modifier.padding(16.dp))
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Boilerplate reduction, Context switching, Unbundled library, Backward compatibility, Interoperability, Single language stack.

**Interview Speak Paragraph**

> "I prefer Compose over XML primarily for efficiency and maintainability. Compose drastically reduces boilerplate—especially for lists, where a 50-line RecyclerView setup becomes a 5-line `LazyColumn`. It eliminates the context switching between XML and Kotlin, allowing me to use standard Kotlin control flow like `if` and `for` loops directly in the UI logic. Furthermore, because Compose is an 'unbundled' library, I can ship the latest UI features to users on older Android versions without waiting for OS updates."

---

**Next Step:**
Ready for **Topic 1.3: Compose Architecture (Declarative UI Basics)**? This will explain the "Tree" concept which is crucial for understanding how Compose actually thinks.

---

## Navigation

â† Previous
Next â†’
