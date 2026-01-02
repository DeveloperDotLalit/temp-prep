---
layout: default
title: "Singleton Pattern"
parent: "Phase 1: Creational Patterns"
nav_order: 1
---

# Singleton Pattern

### **Singleton Pattern: The "There Can Be Only One" Rule**

In Android development, the **Singleton Pattern** is like a specialized department in a company that only ever has **one** manager. No matter who asks for the manager, they are always pointed to the same person.

---

### **1. What It Is**

The Singleton Pattern ensures that a class has **only one instance** (one object) throughout the entire life of the app. It also provides a single, global point to access that object.

Think of it like the **Power Button** on your phone. No matter how many apps you are using or what screen you are on, there is only one physical power button that controls the state of the device. You don't get a new power button every time you open Instagram.

---

### **2. Why It Exists (The Problem it Solves)**

Imagine you are building an app that uses a **Database**.

- **The Problem:** If every part of your app (the Login screen, the Profile screen, the Settings screen) created its own "Database Object," you would have multiple connections to the same file. This leads to data corruption, massive memory waste, and synchronization issues (one screen trying to write while another is trying to delete).
- **The Solution:** You create one "Manager" for the database. Every screen "talks" to this same manager. This saves memory and ensures that everyone is looking at the same, consistent data.

**Key Benefits:**

- **Controlled Access:** You know exactly how and when the object is accessed.
- **Memory Efficiency:** You aren't creating 100 objects when 1 will do the job.
- **Data Consistency:** Since there’s only one instance, there’s no risk of different parts of the app having "stale" or different versions of the data.

---

### **3. How It Works**

To make a class a Singleton, you need to follow three logical rules:

1. **Hide the Constructor:** Make the constructor `private` so no one can use the `new` keyword (or call the constructor in Kotlin) from outside the class.
2. **The Secret Instance:** Create a private variable inside the class that holds the "one and only" instance of itself.
3. **The "Get" Method:** Provide a public way for others to ask for that instance. If it doesn’t exist yet, create it; if it does, just hand over the existing one.

---

### **4. Example (Practical Android/Kotlin)**

In Kotlin, the language is so smart that it has a built-in way to create Singletons using the `object` keyword. This handles everything—thread safety, lazy loading, and the private constructor—automatically.

#### **The Scenario: A Network Manager**

You only want one network client (like Retrofit) to handle all your API calls.

```kotlin
// In Kotlin, 'object' creates a Singleton automatically
object NetworkManager {

    val baseUrl = "https://api.myapp.com"

    fun fetchData() {
        println("Fetching data from $baseUrl using the same instance!")
    }
}

// --- HOW TO USE IT ---
fun main() {
    // You don't call NetworkManager(). You just use the name directly.
    val client1 = NetworkManager
    val client2 = NetworkManager

    client1.fetchData()

    // This will print 'true' because they are exactly the same object in memory
    println(client1 === client2)
}

```

**What if you need to pass a context (like for a Database)?**
We use a "Companion Object" with a thread-safe check (using `@Volatile` and `synchronized`):

```kotlin
class AppDatabase private constructor(context: Context) {
    // Private constructor prevents instantiation from outside

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            // If INSTANCE is not null, return it.
            // If it is, create it in a thread-safe way.
            return INSTANCE ?: synchronized(this) {
                val instance = AppDatabase(context)
                INSTANCE = instance
                instance
            }
        }
    }
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
User Request ----> [ Check Instance ]
                          |
            /-------------+-------------\
      [ Exists? ]                 [ Doesn't Exist? ]
           |                              |
    Return existing <---------- [ Create New Instance ]
       instance                           |
                                    Save to memory

```

---

### **6. Interview Keywords**

- **Single Instance:** Only one object exists.
- **Global Access Point:** Can be accessed from anywhere.
- **Private Constructor:** Prevents external creation.
- **Thread Safety:** Ensuring two threads don't create two instances at the same time.
- **Object Keyword (Kotlin):** The easiest way to implement it in Android.
- **Lazy Initialization:** Creating the object only when it's first needed.

---

### **7. Interview Speak Paragraph**

> "The Singleton Pattern is a creational design pattern that ensures a class has only one instance while providing a global point of access to it. In Android, we use it for heavy objects like Database instances, Network clients, or Shared Preferences managers to save memory and prevent data conflicts. In Kotlin, I usually implement this using the `object` declaration, which is thread-safe and lazily initialized by default. If I need to pass a `Context` to the singleton, I use a companion object with a synchronized 'getInstance' method to ensure that even in a multi-threaded environment, only one instance is ever created."

---

### **Interview "Pro-Tip" (The Trade-off)**

Interviewer might ask: **"Is Singleton always good?"**

- **Your Answer:** "No. While they are useful, they can make **Unit Testing** difficult because they hold onto 'state' globally. Also, if a Singleton holds onto an Activity's `Context`, it can cause **Memory Leaks**. That’s why we should always use the `ApplicationContext` inside a Singleton, never an `ActivityContext`."

---

[â¬… Back to Phase](../) | [Next âž¡](../)
