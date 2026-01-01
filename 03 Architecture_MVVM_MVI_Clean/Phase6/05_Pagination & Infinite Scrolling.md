---
layout: default
title: Pagination & Infinite Scrolling
parent: Architecture (MVVM/MVI/Clean): Phase6
nav_order: 5
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Pagination & Infinite Scrolling**.

This is a mandatory topic for any app that displays lists (Social Feeds, E-commerce, Search Results).

---

### **Topic: Pagination & Infinite Scrolling (Paging 3)**

#### **What It Is**

Pagination is the technique of loading data in **chunks** (pages) rather than all at once.
**Infinite Scrolling** is the user experience where the next chunk loads automatically as the user scrolls to the bottom, creating the illusion of an endless list.

Google's **Paging 3** library is the standard tool for this. It handles the difficult math of "When do I load the next page?" so you don't have to write scroll listeners manually.

#### **Why It Exists (The Problem)**

1. **Memory Crash (OOM):** If you try to download 10,000 photos at once, the phone runs out of RAM and the app crashes.
2. **Network Speed:** The user shouldn't wait 2 minutes for 10,000 items to download just to see the top 10.
3. **Complexity:** Writing code to detect "End of List," handle errors, retry failed pages, and prevent duplicate requests is extremely hard to get right manually.

#### **How It Works (The Clean Architecture Flow)**

Paging 3 fits perfectly into Clean Architecture layers:

1. **Data Layer (The Worker):**

- Define a `PagingSource`. This class answers: _"Given Page #1, how do I get Page #2?"_

2. **Repository (The Stream):**

- Creates a `Pager`. This object turns the PagingSource into a reactive stream (`Flow<PagingData>`).

3. **ViewModel (The Holder):**

- Simply holds this Flow and caches it (`cachedIn(viewModelScope)`) so rotation doesn't restart the load.

4. **UI Layer (The Renderer):**

- Uses a `PagingDataAdapter` (XML) or `collectAsLazyPagingItems` (Compose). It observes the Flow. **The Library** detects when the user scrolls near the bottom and asks the Data Layer for more.

#### **Example (The Paging Source)**

**1. The Logic (Data Layer):**

```kotlin
class NewsPagingSource(private val api: NewsApi) : PagingSource<Int, Article>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Article> {
        val currentPage = params.key ?: 1 // Default to page 1

        return try {
            // Fetch data from API
            val response = api.getNews(page = currentPage)

            LoadResult.Page(
                data = response.articles,
                prevKey = if (currentPage == 1) null else currentPage - 1,
                nextKey = if (response.articles.isEmpty()) null else currentPage + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }
}

```

**2. The Repository (Exposing the Stream):**

```kotlin
fun getNewsStream(): Flow<PagingData<Article>> {
    return Pager(
        config = PagingConfig(pageSize = 20),
        pagingSourceFactory = { NewsPagingSource(api) }
    ).flow
}

```

**3. The UI (Compose - LazyColumn):**

```kotlin
@Composable
fun NewsScreen(viewModel: NewsViewModel) {
    // The UI doesn't manage page numbers! It just collects items.
    val newsItems = viewModel.newsFlow.collectAsLazyPagingItems()

    LazyColumn {
        items(newsItems.itemCount) { index ->
            NewsRow(newsItems[index])
        }
    }
}

```

#### **Interview Keywords**

Paging 3, `PagingSource`, `RemoteMediator` (for caching), `LoadState`, Infinite Scroll, Backpressure, Buffer, `cachedIn`.

#### **Interview Speak Paragraph**

> "I implement infinite scrolling using the Jetpack Paging 3 library. This allows me to maintain strict separation of concerns. I create a `PagingSource` in the Data layer that defines how to fetch pages from the API. My Repository exposes a `Flow<PagingData>`, which the UI collects. This is powerful because the UI code doesn't need to calculate scroll positions or manage page numbers manually; the library handles the 'end-of-list' detection and triggers the next data fetch automatically within the data layer."

---

### **Phase 6 Complete!**

You now have the "Senior" toolkit: **Refactoring**, **Shared ViewModels**, **Concurrency**, **Complex Lists**, and **Pagination**.

**Would you like to move to Phase 7: "The Interview Q&A & Defense"?** (This is the final phase where we cover the exact questions interviewers will ask you).
