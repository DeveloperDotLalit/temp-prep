---
layout: default
title: System Design
parent: Phase7
nav_order: 2
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **System Design: "Design a Search Screen"**.

This is a very common "Whiteboard" or "Live Coding" interview question because it touches on UI, Networking, Caching, and Concurrency all at once.

---

### **Topic: System Design: "Design a Search Screen"**

#### **What It Is**

The interviewer says: _"Design a screen where a user types a query, we fetch results from an API, and display them in a list. Oh, and make sure it doesn't crash if the user types fast."_

You need to design the full flow:
**UI -> ViewModel -> Repository -> API/Cache.**

#### **The 4 Key Challenges**

To pass this, you must explicitly mention and solve these four problems:

1. **Debouncing:** Don't call the API for every single letter ("A", "Ap", "App", "Appl", "Apple"). Wait until the user stops typing.
2. **Race Conditions:** If "Ap" returns _after_ "Apple", don't show the "Ap" results.
3. **Loading States:** Show a spinner while searching, but don't flash it annoying if the search is super fast.
4. **Caching:** If I search "Apple", then "Banana", then "Apple" again—show the previous "Apple" result instantly without a network call.

#### **The Architecture Walkthrough**

**Step 1: The UI (View)**

- **Input:** Listen to text changes.
- **Output:** Observe `StateFlow<UiState>`.
- **Optimization:** Don't send every character change to the ViewModel if using Compose. Use `LaunchedEffect` or a specific listener to throttle events.

**Step 2: The Logic (ViewModel)**

- **The Input Stream:** Use a `MutableStateFlow` for the query.
- **The Transformation:** Use `flatMapLatest` (this is the magic operator).
- It cancels the previous search automatically (solving Race Conditions).
- It allows us to add `.debounce(300ms)`.

**Step 3: The Data (Repository)**

- **The Decision:** Check memory cache first.
- **The Source:** If not in cache, call API.
- **The Save:** Save result to `Map<String, List<Result>>` (In-Memory Cache).

#### **The Code Blueprint (Mental Model)**

```kotlin
class SearchViewModel(private val repository: SearchRepository) : ViewModel() {

    private val _query = MutableStateFlow("") // 1. User types here

    // 2. The Pipeline
    val results = _query
        .debounce(300) // Wait 300ms for user to stop typing
        .filter { it.length > 2 } // Don't search for "A"
        .flatMapLatest { query -> // Cancel old searches automatically
            flow {
                emit(Loading) // Show spinner
                emit(repository.search(query)) // Fetch data
            }
        }
        .stateIn(viewModelScope, SharingStarted.Lazily, Idle)
}

```

#### **Example (The Repository with Caching)**

```kotlin
class SearchRepository(private val api: ApiService) {
    // Simple in-memory cache
    private val cache = mutableMapOf<String, List<Item>>()

    suspend fun search(query: String): List<Item> {
        // 1. Check Cache
        if (cache.containsKey(query)) {
            return cache[query]!!
        }

        // 2. Call Network
        val result = api.fetch(query)

        // 3. Save Cache
        cache[query] = result
        return result
    }
}

```

#### **Interview Keywords**

Debouncing, Throttling, Race Conditions, `flatMapLatest` (SwitchMap), Caching Strategy, In-Memory Cache, Network Bandwidth Optimization, User Experience (UX).

#### **Interview Speak Paragraph**

> "To design a robust search screen, I focus on performance and data integrity. First, I implement **debouncing** (typically 300ms) in the ViewModel to prevent API spam while the user is typing. I use the `flatMapLatest` operator on the query flow, which handles **concurrency** by automatically canceling any outdated network requests if the user changes the query before the previous one finishes. Finally, I implement a Repository with an in-memory **cache** (like a Map). This ensures that if the user clears and re-types a previous term, the results load instantly without hitting the network again."

---

**Would you like to proceed to the next note: "Spotting 'Code Smells' (The Bad Code Test)"?**
