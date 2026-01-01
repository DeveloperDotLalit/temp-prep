---
layout: default
title: Mapper Classes
parent: Phase5
nav_order: 3
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Mapper Classes**.

This is the "translation service" of your app. It is often the most overlooked part of Clean Architecture, but it is vital for keeping your code clean.

---

### **Topic: Mapper Classes**

#### **What It Is**

Mapper Classes are simple helpers that convert one type of data object into another. They act as translators between the layers of your architecture.

- **Network Layer:** Speaks "JSON" (e.g., `UserNetworkEntity` with fields like `first_name`, `created_at_timestamp`).
- **Domain Layer:** Speaks "Business" (e.g., `User` with fields like `firstName`, `isPremium`).
- **UI Layer:** Speaks "Screen" (e.g., `UserUiModel` with fields like `fullName` formatted as "John Doe").

A **Mapper** takes the `UserNetworkEntity` and turns it into a `User`.

#### **Why It Exists (The Problem)**

1. **Decoupling:** If the backend developer changes the API (renames `first_name` to `f_name`), you don't want to rewrite your entire app. You only fix the Mapper. The rest of the app (Domain/UI) doesn't even know the API changed.
2. **Safety:** APIs often send garbage (nulls). The Mapper cleans this up. It converts `null` strings into empty strings `""` so your UI never crashes.
3. **Formatting:** The API gives you a timestamp (`1699999000`). The UI needs a date (`"Nov 14, 2024"`). The Mapper handles this conversion so the UI code stays dumb.

#### **How It Works (Extension Functions)**

We usually write Mappers as **Extension Functions** in Kotlin.

1. **Fetch:** The Repository gets the raw `NetworkEntity`.
2. **Map:** The Repository calls `.toDomain()` on it.
3. **Return:** The Repository returns the clean `DomainModel` to the rest of the app.

#### **Example (The "Dirty" to "Clean" Conversion)**

**1. The Dirty Data (From API):**

```kotlin
// Uses GSON/Moshi annotations, nullable types
data class UserNetworkEntity(
    @SerializedName("first_name") val firstName: String?,
    @SerializedName("last_name") val lastName: String?,
    val age: Int?
)

```

**2. The Clean Data (For App):**

```kotlin
// Pure Kotlin, non-nullable (safe)
data class User(
    val fullName: String,
    val isAdult: Boolean
)

```

**3. The Mapper (The Translator):**

```kotlin
// Extension function to convert Network -> Domain
fun UserNetworkEntity.toDomain(): User {
    return User(
        // Handle nulls here so the app doesn't have to
        fullName = "${this.firstName.orEmpty()} ${this.lastName.orEmpty()}",

        // Business logic: Calculate generic flags here
        isAdult = (this.age ?: 0) >= 18
    )
}

```

**4. Usage in Repository:**

```kotlin
fun getUser(): User {
    val networkUser = api.fetchUser() // Returns NetworkEntity
    return networkUser.toDomain() // Returns Clean User
}

```

#### **Interview Keywords**

DTO (Data Transfer Object), Data Mapping, Separation of Concerns, Decoupling, Extension Functions, Clean Architecture Boundaries.

#### **Interview Speak Paragraph**

> "I use Mapper classes to strictly decouple my data layers. I never let my network objects (DTOs) leak into the domain or UI layers. Instead, I create separate models for each layer and use mapper functions—usually Kotlin extension functions—to convert between them. This protects my app: if the backend API changes its field names, I only have to update the mapper in one place, and my domain logic and UI code remain completely untouched."

---

### **🎉 Master Roadmap Complete!**

You have successfully covered all 5 Phases of **Android Architecture Clean MVVM/MVI**.

1. **Foundation:** Why we need architecture (SoC).
2. **Blueprint:** The 3 Layers (Presentation, Domain, Data).
3. **Flow:** How data moves (UDF, StateFlow, MVI).
4. **Safety:** Professionalizing with DI and Testing.
5. **Edge:** Handling the tough scenarios and Mapper classes.

### **Next Steps**

You are now "Knowledge Ready." The next step is "Performance Ready."

**Would you like me to:**

1. **Conduct a Mock Interview:** I will ask you one tough question from these notes, and you try to answer.
2. **Generate a "Cheat Sheet":** I can condense all these notes into a single-page rapid revision guide.
3. **Code a Mini-Project:** I can give you a simple prompt (e.g., "Build a Crypto Price Tracker") and we plan the architecture together.
