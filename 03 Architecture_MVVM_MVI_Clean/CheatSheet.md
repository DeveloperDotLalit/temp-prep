---
layout: default
title: 🚀 Android Architecture Cheat Sheet: Clean MVVM/MVI
parent: Architecture (MVVM/MVI/Clean)
---

Here is your **Ultimate Android Architecture Cheat Sheet**. This condenses weeks of learning into a single, rapid-revision guide.

---

# 🚀 Android Architecture Cheat Sheet: Clean MVVM/MVI

## **1. The Blueprint: Clean Architecture Layers**

**The Rule:** Dependencies only point **INWARDS**. Inner layers know nothing about outer layers.

```mermaid
graph TD
    UI[Presentation Layer (UI)] --> Domain[Domain Layer (Business Logic)]
    Data[Data Layer (Repository/API)] --> Domain

```

- **Presentation (Outer):** `Activity`, `Fragment`, `ViewModel`. Handles the screen.
- **Domain (Inner/Core):** `UseCases`, `Models`. Pure Kotlin. The "Business Rules."
- **Data (Outer):** `RepositoryImpl`, `Retrofit`, `Room`. Handles data fetching.

> **🎙 Interview Speak:** "I follow the Dependency Rule where inner layers, like the Domain, rely on nothing. Outer layers, like UI and Data, depend on the Domain. This ensures my business logic is stable, testable, and platform-agnostic."

---

## **2. The Pattern: MVVM (Model - View - ViewModel)**

**The Goal:** Separate the UI from the Logic and survive screen rotations.

```text
+---------------------+                          +----------------------+                          +---------------------+
|      View (UI)      |      Observes            |      ViewModel       |          Calls           |        Model        |
|  Activity/Fragment  | <--- (StateFlow) ------- |    (State Holder)    | ----- (suspend) -----> |   (Repo/Source)     |
|                     |                          |                      |                          |                     |
|                     | ------- (Events) ------> |                      | <---- (Data/Error) --- |                     |
+---------------------+                          +----------------------+                          +---------------------+

```

- **View:** Dumb. Only draws pixels. Observes ViewModel.
- **ViewModel:** The Brain. Holds state. Survives rotation. Talks to Repo.
- **Model:** The Data. Repository, Database, API.

> **🎙 Interview Speak:** "I use MVVM because it decouples the UI from the logic. The ViewModel acts as a State Holder that survives configuration changes, ensuring data isn't lost during rotations, while the View remains passive and reactive."

---

## **3. The Flow: Unidirectional Data Flow (UDF)**

**The Rule:** Data flows **DOWN**. Events flow **UP**.

1. **Event:** User clicks button -> UI sends Event to ViewModel.
2. **Process:** ViewModel talks to UseCase/Repo -> Updates State.
3. **State:** ViewModel exposes new `UiState` -> UI observes and redraws.

**UI State Modeling (Sealed Classes):**
Don't use separate variables (`isLoading`, `isError`). Use one State object.

```kotlin
sealed class UiState {
    object Loading : UiState()
    data class Success(val data: List<User>) : UiState()
    data class Error(val msg: String) : UiState()
}

```

> **🎙 Interview Speak:** "I strictly follow Unidirectional Data Flow. The View sends intents or events up to the ViewModel, and the ViewModel pushes a single immutable State down to the View. This prevents inconsistent states and makes debugging significantly easier."

---

## **4. Data Management: Repository & Mappers**

**Repository Pattern:** The "Single Source of Truth."

- Decides: Fetch from **Local DB** (Cache) OR **Network** (API)?

**Mapper Classes:** The "Translator."

- Converts dirty `NetworkEntity` (JSON) -> clean `DomainModel` -> formatted `UiModel`.

```text
[API JSON] --> (Mapper) --> [Domain Model] --> (Mapper) --> [UI State]

```

> **🎙 Interview Speak:** "I use the Repository Pattern to abstract data sources. It acts as the single source of truth, managing caching logic between the local database and the network. I also use Mapper classes to convert data at layer boundaries, ensuring my domain logic never relies on API-specific structures."

---

## **5. Quality Control: DI & Testing**

**Dependency Injection (Hilt):**

- **Don't:** `val repo = Repository()` (Hard Dependency).
- **Do:** `@Inject constructor(private val repo: Repository)` (Inversion of Control).

**Unit Testing (AAA Pattern):**

1. **Arrange:** Mock the Repository (`mockk`).
2. **Act:** Call `viewModel.loadData()`.
3. **Assert:** Check `assertEquals(Success, viewModel.state.value)`.

> **🎙 Interview Speak:** "I use Hilt for Dependency Injection to make my code testable. Instead of creating objects manually, I inject them, which allows me to pass 'Fake' repositories during unit tests. I test my ViewModels using the Arrange-Act-Assert pattern to verify logic in isolation."

---

## **6. Advanced Topics (The "Senior" Badge)**

### **A. MVVM vs MVI**

- **MVVM:** View calls methods (`vm.login()`). Good for standard apps.
- **MVI:** View sends Intents (`vm.process(LoginIntent)`). Strict, single entry point. Good for complex state.

### **B. Handling Concurrency (Race Conditions)**

- **Problem:** User searches "A" then "AB". "A" returns last and overwrites "AB".
- **Fix:** Use `job?.cancel()` or `flatMapLatest` to kill the old request.

### **C. Pagination (Paging 3)**

- **Logic:** `PagingSource` (Data Layer) defines how to fetch next page.
- **Stream:** Repository exposes `Flow<PagingData>`.
- **UI:** `collectAsLazyPagingItems()` handles the scroll detection automatically.

### **D. External SDKs (Wrapper Pattern)**

- **Rule:** Never let `Firebase` leak into Domain.
- **Fix:** Create `AnalyticsRepo` (Interface) in Domain. Implement `FirebaseAnalyticsImpl` in Data.

---

## **7. Rapid Fire Definitions (Memorize These)**

1. **Memory Leak:** Object is unused but GC cannot delete it because something holds a reference (e.g., Context in ViewModel).
2. **Race Condition:** Timing bug. Two threads change data at the same time, causing unpredictable results.
3. **Singleton:** A class with only one instance (e.g., Database instance, Retrofit client).
4. **Observer Pattern:** An object (Subject) maintains a list of dependents (Observers) and notifies them of state changes (e.g., LiveData).
5. **Coroutines:** Lightweight threads for async programming.
6. **DiffUtil:** Utility that calculates the difference between two lists for RecyclerView to update efficiently.
7. **Cold Flow:** Code inside runs _only_ when someone collects it.
8. **Hot Flow (StateFlow):** Active stream. Holds a value even if no one is listening.
9. **Idempotency:** Doing the same operation multiple times produces the same result (e.g., Retry button shouldn't charge user twice).
10. **ProGuard/R8:** Tool that shrinks and obfuscates code to make the APK smaller and harder to reverse engineer.

---

## **8. The "Golden Rule" for Any Coding Question**

If asked **"Where does X go?"**:

- Is it **UI/Screen** stuff? -> **Presentation Layer**
- Is it **Business Logic/Math**? -> **Domain Layer (UseCase)**
- Is it **API/Database/Sensor**? -> **Data Layer**
