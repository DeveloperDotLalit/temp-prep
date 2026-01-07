---
layout: default
title: Pagination
parent: 7. Clean MVVM with Compose
nav_order: 6
---

# Pagination

Here are your notes for **Topic 7.6**.

---

## **Topic 7.6: Pagination (Paging 3)**

### **1. What It Is**

Pagination (specifically the **Paging 3** library) is the standard way to handle "Infinite Scrolling" in Android.
Instead of downloading 10,000 items at once, you download a small "page" (e.g., 20 items). When the user scrolls to the bottom, the library automatically fetches the next 20 items.

### **2. Why It Exists (Memory & Bandwidth)**

- **Memory:** Loading 10,000 high-res images into RAM will crash your app immediately (Out of Memory).
- **Bandwidth:** Why download data the user might never see? Pagination saves the user's data plan.
- **Compose Difference:** In standard Compose lists (`LazyColumn`), you pass a `List<T>`. In Paging 3, you pass a special `LazyPagingItems<T>`.

### **3. How It Works (The 3 Components)**

1. **`PagingSource` (The Fetcher):** A class where you define logic: "I am on Page 1. Fetch Page 2."
2. **`Pager` (The Config):** You define the page size (e.g., 20) and connect it to the Source.
3. **`collectAsLazyPagingItems` (The UI Consumer):**

- **Vital:** You cannot use standard `.collectAsState()` for Paging Data.
- You must use the specific extension function `.collectAsLazyPagingItems()`.
- This function returns a wrapper that acts like a List but triggers network calls automatically when you scroll near the end.

### **4. Example: Infinite Scroll with Loading Footer**

**The ViewModel (Setup)**

```kotlin
val usersFlow = Pager(PagingConfig(pageSize = 20)) {
    UserPagingSource(api) // Your custom source
}.flow.cachedIn(viewModelScope) // Cache results to survive rotation

```

**The UI (Compose)**

```kotlin
@Composable
fun UserList(viewModel: UserViewModel) {
    // 1. COLLECT: Use the special Paging collector
    val users: LazyPagingItems<User> = viewModel.usersFlow.collectAsLazyPagingItems()

    LazyColumn {
        // 2. ITEMS: Display the data
        items(
            count = users.itemCount,
            key = users.itemKey { it.id } // Use stable keys if possible!
        ) { index ->
            val user = users[index]
            if (user != null) {
                UserRow(user)
            }
        }

        // 3. FOOTER: Handle the "Loading More..." Spinner
        // We check the 'append' state (Adding more to the bottom)
        when (val state = users.loadState.append) {
            is LoadState.Loading -> {
                item { CircularProgressIndicator(modifier = Modifier.padding(16.dp)) }
            }
            is LoadState.Error -> {
                item {
                    Button(onClick = { users.retry() }) { Text("Retry") }
                }
            }
            else -> {}
        }

        // 4. HEADER: Handle the "First Load" Spinner
        // We check the 'refresh' state (Initial load)
        when (val state = users.loadState.refresh) {
            is LoadState.Loading -> {
               // Show a big spinner in the center of the screen
            }
            is LoadState.Error -> {
               // Show a big "Retry" button
            }
            else -> {}
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`Paging 3`, `collectAsLazyPagingItems`, `LoadState` (Refresh/Append/Prepend), `cachedIn(viewModelScope)`, `RemoteMediator` (for caching to DB), Infinite Scroll.

**Interview Speak Paragraph**

> "For large datasets, I use the Paging 3 library to implement infinite scrolling efficiently. In Compose, the key difference is using the `collectAsLazyPagingItems()` extension function instead of standard state collection. This gives me a `LazyPagingItems` object that I can pass to a `LazyColumn`. A critical part of the implementation is handling the `LoadState`—specifically `loadState.append` for showing a footer spinner when fetching the next page, and `loadState.refresh` for the initial screen loading state. This provides a seamless user experience without loading the entire dataset into memory."

---

**Congratulations!** You have completed **Part 7: Clean MVVM with Compose**.
You now have a professional-grade architecture: Clean Layers, Dependency Injection, Networking, and Pagination.

Now, let's make it _beautiful_.
**Are you ready to start Topic 8: Advanced Layouts & Graphics?**
_This is where we break out of the standard Row/Column boxes._

---

## Navigation

â† Previous
