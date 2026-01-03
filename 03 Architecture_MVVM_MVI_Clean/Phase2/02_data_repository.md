---
layout: default
title: "Data Repository"
parent: "Phase 2: The Blueprint – Implementing Clean Architecture"
nav_order: 2
---

Here are your focused notes on **The Data Layer & Repository Pattern**.

---

### **Topic: The Data Layer & Repository Pattern**

#### **What It Is**

The **Data Layer** is the part of your app responsible for handling data operations (fetching and saving).

Inside this layer lives the **Repository**. Think of the Repository as a **"Store Manager"**.

- The **UI (Customer)** comes to the counter and asks for "Milk" (Data).
- The **Repository (Manager)** decides where to get it:
- Is it on the shelf? (Local Database / Cache)
- Do I need to order it from the factory? (Network API)

- The UI doesn't care where it came from; it just wants the milk.

#### **Why It Exists (The Problem)**

1. **Abstraction:** If your ViewModel calls the API directly, what happens when the user goes offline? The app crashes or shows nothing.
2. **Single Source of Truth (SSOT):** If you display data from the API in one screen and data from the Database in another, they might disagree. The Repository ensures everyone gets data from the _same_ valid place.
3. **Offline Support:** It allows apps to work without internet by checking the local database first.

#### **How It Works (The "Offline-First" Logic)**

The Repository coordinates between two data sources:

1. **Remote Data Source:** Your API (e.g., Retrofit).
2. **Local Data Source:** Your Database (e.g., Room) or SharedPreferences.

**The Typical Flow:**

1. ViewModel asks Repository: "Get User Details."
2. Repository checks the **Local Database**.
3. **If data exists:** Return it immediately (Fast!).
4. **If data is missing/old:**

- Call the **Network API**.
- **Save** the new data into the Local Database.
- Return the new data to the ViewModel.

_This way, the app always relies on the Database as the "Single Source of Truth," and the Network is just a way to update that database._

#### **Example (Social Media Feed)**

Imagine scrolling through Instagram.

- **RemoteDataSource:** `TwitterApi` (Retrofit interface).
- **LocalDataSource:** `TweetDao` (Room database interface).
- **Repository:**

```kotlin
class TweetRepository(
    private val api: TwitterApi,
    private val database: TweetDao
) {
    // The ViewModel calls this
    suspend fun getTweets(): List<Tweet> {
        // 1. Try to get from database first (works offline!)
        val localTweets = database.getAllTweets()

        if (localTweets.isNotEmpty()) {
            return localTweets
        }

        // 2. If database is empty, fetch from network
        try {
            val remoteTweets = api.fetchTweets()
            // 3. Save to database for next time
            database.insertAll(remoteTweets)
            return remoteTweets
        } catch (e: Exception) {
            throw Exception("No internet and no local data")
        }
    }
}

```

#### **Interview Keywords**

Repository Pattern, Single Source of Truth (SSOT), Offline-First, Caching, Abstraction, Remote vs. Local Data Source, Separation of Concerns.

#### **Interview Speak Paragraph**

> "I implement the Repository Pattern to create a Single Source of Truth for my application's data. The Repository acts as a mediator between the data sources—like the Room database and Retrofit API—and the rest of the app. This allows me to implement caching logic, where I load data from the local database first for a snappy user experience, and then update it from the network in the background. It also ensures the ViewModel doesn't need to know the complex details of where the data is coming from."

---

**Would you like to proceed to the next note: "The Domain Layer & Use Cases"?**
