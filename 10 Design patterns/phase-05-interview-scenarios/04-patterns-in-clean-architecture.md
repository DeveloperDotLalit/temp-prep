---
layout: default
title: "Patterns in Clean Architecture"
parent: "Phase 5: Real World Interview Scenarios"
nav_order: 4
---

# Patterns in Clean Architecture

### **Interview Scenario: Clean Architecture & Design Patterns**

In a **Clean Architecture** interview, the recruiter is looking to see if you understand how to "fence off" your business logic from the outside world (like the Internet or Databases). They want to know how you keep your code clean so that if you change your database from Room to Realm, your business logic doesn't even notice.

---

### **1. The Strategy: Patterns as "Gatekeepers"**

In Clean Architecture, we divide the app into layers (usually Data, Domain, and Presentation).

- **Facade (The Repository):** Acts as the gatekeeper for the **Data Layer**. It hides the mess of APIs and Databases.
- **Dependency Injection (DI):** Acts as the "Glue" that connects the layers without them being "welded" together. It allows the **Domain Layer** to use the Data Layer without actually knowing it exists.

---

### **2. Why This Combination Exists**

- **The Problem:** If your **Domain Layer** (UseCases) creates a `RoomDatabase` object directly, your business logic is now "stuck" to Room. You can't test it easily on a computer, and you can't swap Room for something else later.
- **The Solution:** 1. The **Domain Layer** defines an **Interface** (the "Rule").

2.  The **Data Layer** implements that interface using a **Facade** (the Repository).
3.  **Dependency Injection** "injects" the implementation into the Domain layer at runtime.

---

### **3. How It Works (Layer by Layer)**

1. **Domain Layer (The Brains):** Contains **UseCases** and **Entities**. It defines an Interface (e.g., `UserRepository`). It doesn't care _how_ a user is fetched; it just knows it needs a user.
2. **Data Layer (The Muscle):** Contains the actual implementation. It uses a **Facade** (Repository) to coordinate between a local DB and a Remote API.
3. **DI (The Connector):** Informs the app: "Whenever a UseCase asks for a `UserRepository`, give it this specific implementation from the Data Layer."

---

### **4. Example (The "Clean" Code Structure)**

#### **The Domain Layer (Pure Kotlin - No Android/Library code)**

```kotlin
// The "Rule"
interface UserRepository {
    suspend fun getUserData(): User
}

// The UseCase (Business Logic)
class GetUserUseCase(private val repository: UserRepository) {
    suspend fun execute(): User {
        // Logic: Add a "Welcome" prefix to the name
        val user = repository.getUserData()
        return user.copy(name = "Welcome, ${user.name}")
    }
}

```

#### **The Data Layer (Implementation - Where the Facade lives)**

```kotlin
// The FACADE: Hiding the complexity of API and DB
class UserRepositoryImpl(
    private val api: ApiService,
    private val dao: UserDao
) : UserRepository {
    override suspend fun getUserData(): User {
        // Complex logic hidden behind the Facade
        return if (networkIsAvailable) {
            val user = api.fetchUser()
            dao.insertUser(user)
            user
        } else {
            dao.getUserFromLocal()
        }
    }
}

```

#### **The DI Layer (The Glue - Hilt/Dagger)**

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    // DI links the Interface (Domain) to the Implementation (Data)
    @Binds
    abstract fun bindUserRepository(
        repoImpl: UserRepositoryImpl
    ): UserRepository
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
[ Presentation ] ----> [ Domain Layer ] <---- [ Data Layer ]
      |                      |                     |
 (ViewModel)            (UseCases)            (Repositories)
      |                      |                     |
      | calls                | talks to            | Facade hides:
      v                      v                     v
 [ UseCase ] --------> [ Interface ] <------- [ API / DB ]
                               ^
                               |
                        [ DI (Hilt) ]
                 (Provides implementation)

```

---

### **6. Interview Keywords**

- **Dependency Inversion Principle:** The Domain layer shouldn't depend on the Data layer; both should depend on abstractions (Interfaces).
- **Separation of Concerns:** Business logic (Domain) is separate from implementation (Data).
- **Pluggable Architecture:** The ability to swap the Data layer implementation without touching the Domain logic.
- **Abstraction Layer:** Using interfaces to hide details.
- **Single Source of Truth:** The Repository (Facade) deciding where the data comes from.

---

### **7. Interview Speak Paragraph**

> "In Clean Architecture, I use the **Facade pattern** within the Data layer to implement the Repository pattern. This Repository hides the complexity of managing multiple data sources—like Room for local storage and Retrofit for remote APIs—providing a simplified interface to the Domain layer. To keep the layers decoupled, I use **Dependency Injection** to pass these implementations into my UseCases. This follows the **Dependency Inversion Principle**, where my business logic depends only on interfaces defined in the Domain layer, not on specific frameworks. This makes the system highly testable, as I can easily swap the real Repository implementation with a mock during unit testing without changing a single line of business logic."

---

### **Common Interview "Follow-up" Questions**

**1. "Why do we put the Repository Interface in the Domain layer but the Implementation in the Data layer?"**

- **Answer:** "Because the Domain layer is the 'center' of the app. It shouldn't know about outside tools like Retrofit or Room. By putting the interface in Domain, we 'invert' the dependency—now the Data layer has to follow the rules set by the Domain layer."

**2. "Can a UseCase talk to another UseCase?"**

- **Answer:** "Yes, that's perfectly fine in Clean Architecture if one UseCase needs the logic of another to complete its task. However, a UseCase should **never** talk directly to an Activity or a Database; it must always go through an interface or a Facade."

---

**You have mastered the most advanced scenarios!** **Next Step:** Are you ready for the final stretch? **Phase 6: The Interview Q&A.** This is a collection of the "trick" questions interviewers love to ask about patterns, trade-offs, and "anti-patterns." Shall we begin the final phase?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
