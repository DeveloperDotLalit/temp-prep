---
layout: default
title: "Search As You Type"
parent: "Phase 6: Interview Scenarios and Real World Use Cases"
nav_order: 1
---

# Search As You Type

We are now in **Phase 6: Interview Scenarios**. This is where the interviewer moves away from "What is a Flow?" and asks "How would you build this feature?" The **Search-as-you-type** scenario is the single most common practical test for Flow knowledge.

---

### **What It Is – Simple explanation for beginners**

Search-as-you-type is a feature where the app starts searching automatically as the user types, without them having to click a "Search" button.

To make this feel smooth and not crash your servers, you need two gatekeepers:

1. **Debouncing:** Waiting for the user to stop typing for a split second (e.g., 300ms) before sending the request.
2. **Distinct Filtering:** Ensuring that if the user types "A", then "AB", then backspaces to "A" quickly, you don't perform the same search twice.

### **Why It Exists – The problem it solves**

- **Network Waste:** Without debouncing, if a user types "Pizza," the app would fire 5 separate network requests (for P, Pi, Piz, Pizz, Pizza). This wastes battery and server data.
- **Race Conditions:** If the request for "Pi" is slow and the request for "Pizza" is fast, the "Pi" results might arrive _after_ the "Pizza" results, causing the UI to show the wrong data.
- **Unnecessary UI Updates:** If the user deletes a character and types it back immediately, there's no need to refresh the UI with the same data.

### **How It Works – The Flow Pipeline**

1. **The Input:** A `MutableStateFlow` that updates every time a character is typed.
2. **`debounce(300)`:** It holds the value in a "waiting room." If a new character arrives within 300ms, it throws away the old one and restarts the timer.
3. **`filter { it.length >= 2 }`:** (Optional) Don't search for a single letter to avoid too many generic results.
4. **`distinctUntilChanged()`:** Only lets the value pass if it is different from the last value that successfully passed through.
5. **`flatMapLatest { ... }`:** Cancels the previous search if the user starts typing again.

---

### **Example – Code-based**

```kotlin
class SearchViewModel(private val api: SearchApi) : ViewModel() {

    private val searchQuery = MutableStateFlow("")

    // The optimized search stream
    val searchResults = searchQuery
        .debounce(300) // 1. Wait for 300ms pause in typing
        .filter { it.isNotBlank() } // 2. Don't search empty strings
        .distinctUntilChanged() // 3. Don't search if the query is the same as last time
        .flatMapLatest { query ->
            // 4. Cancel previous search and start new one
            flow { emit(api.search(query)) }
        }
        .flowOn(Dispatchers.IO) // 5. Do the heavy lifting on IO thread
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun onQueryChanged(newText: String) {
        searchQuery.value = newText
    }
}

```

### **Interview Focus: Trade-offs & Decision Making**

- **Question:** "Why use `flatMapLatest` instead of `flatMapConcat` here?"
- **Answer:** `flatMapConcat` would make the searches wait in a queue. If the user types fast, the UI would show results for "P," then "Pi," then "Piz," even though the user is already done. `flatMapLatest` ensures we only care about the most recent search.
- **Question:** "What is a good debounce time?"
- **Answer:** Usually between **300ms and 500ms**. Anything lower feels too "jumpy," and anything higher feels "laggy."

### **Interview Keywords**

Debounce, `distinctUntilChanged`, `flatMapLatest`, Rate Limiting, Race Conditions, User Experience (UX), Network Optimization.

### **Interview Speak Paragraph**

> "For a search-as-you-type feature, I would use a Flow pipeline to optimize network usage and UI responsiveness. First, I’d use the `debounce` operator to wait for a pause in user typing, preventing a flood of API calls. Next, I’d apply `distinctUntilChanged` to avoid redundant searches if the query hasn't actually changed. Finally, I would use `flatMapLatest` to trigger the search; this is crucial because it automatically cancels any previous, ongoing search if a new query arrives, ensuring the user only sees the results for their most recent input and preventing race conditions."

---

**Next Step:** Let's look at another real-world scenario. Shall we explore **Network Polling: Creating a repeating background task using Flow**? (e.g., updating a stock price or crypto value every 10 seconds).

Would you like me to proceed with that?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
