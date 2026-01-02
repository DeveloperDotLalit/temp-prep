---
layout: default
title: "SOLID in Repository Pattern"
parent: "Phase 4: Real World Android Scenarios"
nav_order: 2
---

# SOLID in Repository Pattern

In the Android ecosystem, the **Repository Pattern** is the most common place where SOLID principles are put to the test. This layer is the "middleman" between your business logic (ViewModels) and your data sources (Retrofit for Network, Room for Database).

---

## **10. SOLID in the Repository Pattern**

### **What It Is**

Applying SOLID to the Repository means creating a clear boundary between **how we get data** and **how we use data**. It ensures that your ViewModel doesn't care if the data comes from a local cache or a remote server.

### **Why It Exists**

- **The Problem:** Without SOLID, the Repository becomes a "junk drawer." You might have Retrofit code, Room queries, and data mapping all mixed into one 1000-line class.
- **The Consequence:** If you want to change your API structure, you end up accidentally breaking your local database logic. It also makes Unit Testing impossible because you can't mock the network without also mocking the database.
- **The Goal:** To create a "Single Source of Truth" that is modular, interchangeable, and clean.

---

### **How It Works (Applying the Principles)**

#### **1. SRP (Single Responsibility)**

A Repository should only coordinate data. It shouldn't:

- Perform JSON parsing (use a Converter).
- Format strings for the UI (use a Mapper).
- Check for internet connectivity (use a NetworkHelper).

#### **2. OCP (Open/Closed)**

If you need to add a new data source (e.g., adding a "Mock" data source for a Demo mode), you shouldn't change the existing Repository code. You should be able to "extend" the system.

#### **3. DIP (Dependency Inversion) — The Star of the Show**

The ViewModel should depend on a `Repository Interface`, not the actual `RoomRepository` or `RetrofitRepository`.

---

### **Example: The "Clean" Repository Implementation**

#### **Step 1: The Abstraction (DIP)**

```kotlin
interface UserRepository {
    suspend fun getUser(id: String): User
}

```

#### **Step 2: Segregated Data Sources (ISP/SRP)**

Instead of one giant class, we have specific implementations for Local and Remote.

```kotlin
class RemoteUserDataSource(private val api: UserApi) {
    suspend fun fetchUser(id: String) = api.getUser(id)
}

class LocalUserDataSource(private val dao: UserDao) {
    suspend fun getSavedUser(id: String) = dao.getUserById(id)
}

```

#### **Step 3: The Implementation (The Coordinator)**

The Repository coordinates these sources but stays "Closed for Modification."

```kotlin
class UserRepositoryImpl(
    private val remote: RemoteUserDataSource,
    private val local: LocalUserDataSource
) : UserRepository {

    override suspend fun getUser(id: String): User {
        // Business Logic: Check local first, then remote
        val cachedUser = local.getSavedUser(id)
        return cachedUser ?: remote.fetchUser(id).also {
            local.save(it)
        }
    }
}

```

---

### **Refactoring for Interview Excellence**

When an interviewer asks about this, emphasize **Data Mapping**.

- **NetworkModel:** The JSON object from Retrofit.
- **EntityModel:** The object for Room.
- **DomainModel:** The object the ViewModel/UI uses.
  **SRP** dictates that you should use "Mappers" to convert between these. This ensures that if the API changes a field name, your UI doesn't break.

---

### **Interview Keywords**

Abstraction, Data Mapping, Single Source of Truth, Decoupling, Layered Architecture, Cache Strategy.

### **Interview Speak Paragraph**

> "In the Repository Pattern, I apply SOLID by first defining an interface in the Domain layer to follow the Dependency Inversion Principle. This ensures the ViewModel remains agnostic of the data source. I further apply SRP by using Mappers to separate Network DTOs from Domain entities. This decoupling allows us to swap a Retrofit implementation for a Ktor one, or a Room database for Realm, without ever touching the business logic or UI, making the data layer robust and independently testable."

---

### **Common Interview Question/Angle**

**Q: "Why define an interface for every Repository? Isn't that overkill for a single implementation?"**
**A:** "While it might seem like more code, it is essential for **Testability** and **Future-proofing**. By depending on an interface, I can inject a `FakeRepository` into my ViewModel unit tests to return instant, predictable data. Furthermore, it follows the **Open/Closed Principle**—if we later decide to add a complex caching layer or a different API, we can create a new implementation of the interface without modifying the existing ViewModel logic."

---

**You have finished Phase 4!** You now know how SOLID practically looks in modern Android tools like Compose and the Repository Pattern.

**Ready for the final phase? Phase 5: The Interview Final Polish.**
This is where we go over:

1. **Anti-SOLID Patterns:** When _not_ to use it.
2. **Scenario-based Questions:** The "How would you fix this?" type of questions.
3. **The Master Q&A list.**

**Should we start with the "Anti-SOLID" patterns and trade-offs?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
