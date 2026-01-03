---
layout: default
title: "Data Passing Bundles and Parcelable"
parent: "Phase 1: Intents - The Glue of Android"
nav_order: 4
---

# Data Passing Bundles and Parcelable

## **Topic 4: Data Passing (Bundles & Parcelable)**

### **What It Is**

In Android, when you use an Intent to move from one Activity to another, you often need to carry data with you (like a User ID or a Product object). This data is packed into a **Bundle** (a key-value map) and attached to the Intent.

To pass complex "objects" (like a `User` class with name, age, and address), we use an interface called **Parcelable**, which decomposes the object into primitive types that the Android System can easily transport.

---

### **Why It Exists**

**The "Why not Global Variables?" Problem:**
You might think, _"Why not just store data in a Static/Global variable that both activities can access?"_

1. **Process Death:** Android can kill your app's process to free up memory while it's in the background. When the user returns, the system restarts the Activity, but your **static variables will be null (reset)**. However, the **Bundle** attached to the Intent is saved by the OS and restored.
2. **Memory Leaks:** Static variables stay in memory as long as the app process is alive, which can lead to memory bloat.
3. **Tight Coupling:** Using globals makes your components depend on each other's state, making the code hard to test and maintain.

---

### **How It Works**

1. **The Bundle:** It’s like a suitcase. You put things in with a "Tag" (Key) and retrieve them using that same tag.
2. **Serialization/Parceling:** When you pass an object through an Intent, it has to cross "Process Boundaries" (or at least be managed by the OS). Android can't move a live memory pointer of a Kotlin object.

- **Parcelable** is the Android-optimized way to "flatten" an object into a byte stream and "reconstruct" it on the other side.

---

### **Example (Code-based)**

**1. The Data Model (Using @Parcelize):**
In modern Kotlin, we use the `@Parcelize` annotation (from the `kotlin-parcelize` plugin) to avoid writing boilerplate code.

```kotlin
import kotlinx.parcelize.Parcelize
import android.os.Parcelable

@Parcelize
data class User(val id: Int, val name: String) : Parcelable

```

**2. Sending the Data:**

```kotlin
val intent = Intent(this, ProfileActivity::class.java)
val user = User(101, "Lalit")

// Passing primitive data and a Parcelable object
intent.putExtra("USER_ID", 101)
intent.putExtra("USER_DATA", user)

startActivity(intent)

```

**3. Receiving the Data:**

```kotlin
val userId = intent.getIntExtra("USER_ID", -1)
// For Parcelable in modern Android (API 33+)
val user = intent.getParcelableExtra("USER_DATA", User::class.java)

```

---

### **Interview Keywords**

- **Key-Value Pairs**: How data is stored in a Bundle.
- **Process Death**: The main reason we prefer Bundles over Static variables.
- **Serialization vs. Parcelization**: Serializable is standard Java (slow), Parcelable is Android-specific (fast).
- **Boilerplate**: Code that `@Parcelize` helps us avoid.

---

### **Interview Speak Paragraph**

> "We use Bundles and Parcelable for data passing because Android components are decoupled and subject to process death. Unlike static variables, which are cleared if the OS kills the app process in the background, the Intent's Bundle is persisted by the system and restored when the user returns. For complex objects, I prefer **Parcelable** over Java's Serializable because it is specifically optimized for Android, offering much better performance by avoiding the heavy use of reflection."

---

### **Common Interview Question/Angle**

- **"Parcelable vs. Serializable: Which one is better?"**
- _Answer:_ **Parcelable** is significantly faster (often 10x) because it is manual/optimized for Android and doesn't use reflection. However, **Serializable** is easier to implement (just a marker interface). In a professional SDE-II role, always recommend Parcelable (or `@Parcelize`).

- **"Is there a size limit for data passing?"**
- _Answer:_ Yes! The **TransactionTooLargeException** occurs if your Bundle exceeds roughly **1MB**. You should never pass large bitmaps or huge lists through an Intent; instead, pass a URI or an ID and fetch the data from a database or repository on the next screen.

---

**Next: PendingIntents – A very important topic for Notifications and Security. Ready to dive in?**

---

[â¬… Back to Phase Overview](../)
