---
layout: default
title: "3 Layer Structure"
parent: "Architecture (MVVM/MVI/Clean): Phase 2: The Blueprint – Implementing Clean Architecture"
nav_order: 1
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **The 3-Layer Structure (Presentation, Domain, Data)**.

This is the "Blueprint" of Clean Architecture.

---

### **Topic: The 3-Layer Structure (Presentation, Domain, Data)**

#### **What It Is**

This is the standard way to organize professional Android apps. Instead of throwing all files into one folder, we split the app into three distinct "circles" or layers.

1. **Presentation Layer (The UI):** "How things look." Contains Activities, Fragments, ViewModels, and Compose files.
2. **Domain Layer (The Rules):** "What the app does." Contains pure business logic (Use Cases) and data models. It is the core of the app.
3. **Data Layer (The Source):** "Where data comes from." Contains API calls (Retrofit), Databases (Room), and Preferences.

#### **Why It Exists (The Problem)**

Imagine building a house. You don't put the plumbing, the electrical wiring, and the interior painting on the same blueprint. If you did, the painter might accidentally cut a water pipe.

In coding:

- **Independence:** If Google changes how the UI works (e.g., XML to Jetpack Compose), you only touch the Presentation Layer. The Business Logic and Data layers remain 100% safe.
- **Reusability:** The "Business Rules" (Domain) are pure Kotlin. They don't depend on Android. You could theoretically take the Domain layer and use it in a desktop app.

#### **How It Works (The Dependency Rule)**

There is one strict rule you must memorize: **The Dependency Rule.**

- **Outer layers know about inner layers.**
- **Inner layers NEVER know about outer layers.**

**The Flow:**

1. **Presentation** asks **Domain** to do something.
2. **Domain** asks **Data** for information.
3. **Data** gives it back to **Domain**.
4. **Domain** processes it and gives it to **Presentation**.

_Crucially: The **Domain** layer (the center) has NO IDEA that an Android Activity exists. It is blind to the UI._

#### **Example (A News App)**

Let's trace a feature: "Show the latest news."

- **Layer 1: Data (The Fetcher)**
- `NewsRepository`: Uses Retrofit to download JSON from `newsapi.org`. It converts that JSON into a list of articles.

- **Layer 2: Domain (The Processor)**
- `GetLatestNewsUseCase`: This class asks the Repository for news. It might also have a rule: "Filter out any articles that don't have images." It doesn't know _how_ to show the news, just _what_ the news is.

- **Layer 3: Presentation (The Display)**
- `NewsViewModel`: Calls `GetLatestNewsUseCase`.
- `NewsActivity`: Observes the ViewModel and draws the list on the screen.

#### **Interview Keywords**

Clean Architecture, Separation of Concerns, Dependency Rule, Scalability, Modularity, Business Logic vs UI Logic, Use Cases.

#### **Interview Speak Paragraph**

> "I structure my apps using Clean Architecture with three main layers: Presentation, Domain, and Data. The Presentation layer handles the UI, the Data layer manages network and database operations, and the Domain layer sits in the middle holding the pure business logic. Crucially, I follow the dependency rule where the Domain layer depends on nothing, ensuring my business rules remain stable even if I change the UI framework or database library."

---

**Would you like to proceed to the next note: "The Data Layer & Repository Pattern"?**
