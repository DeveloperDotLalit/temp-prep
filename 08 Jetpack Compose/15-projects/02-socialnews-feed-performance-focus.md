---
layout: default
title: Social/News Feed (Performance Focus)
parent: 15. Real World Projects
nav_order: 2
---

# Social/News Feed (Performance Focus)

Here are your notes for **Topic 15.2**.

---

## **Topic 15.2: Social/News Feed (Performance Focus)**

### **1. What It Is**

This project simulates a high-traffic feed like Instagram, X (Twitter), or Reddit.
It isn't just a list of text; it handles heavy media (images, auto-playing videos) and infinite scrolling. The primary challenge isn't "making it work," but **"keeping it smooth (60fps)"** while loading heavy assets.

**Key Constraints:**

- **Infinite Scroll:** Seamlessly loading pages of data without the user noticing.
- **Polymorphic Content:** Supporting different post types (Text-only, Image, Video, Ads) in the same list.
- **Media Efficiency:** Only playing video when it is 100% visible and releasing resources immediately when scrolled away.

### **2. Why It Exists (The Performance Test)**

This project proves you can handle **Memory Management** and **UI Optimization**.

- **Paging 3:** Shows you can handle large datasets without crashing memory.
- **Lazy Loading:** Shows you understand how to recycle UI nodes.
- **Lifecycle Management:** Shows you know how to clean up heavy objects (ExoPlayer) to prevent battery drain.

### **3. Architecture & Key Tech**

#### **A. Paging 3 (The Data Pipeline)**

We don't just load a `List<Post>`. We use a stream.

- **Source:** Retrofit API.
- **Mediator:** (Optional) Caches data to Room for offline support.
- **UI:** `collectAsLazyPagingItems()`.

#### **B. Heterogeneous Views (Polymorphism)**

A feed has various shapes. In `RecyclerView` XML, you used `getItemViewType`. In Compose, we use a `when` statement and the `contentType` key.

#### **C. Video Auto-Play Logic**

You cannot have 10 VideoPlayers active at once.

- **Logic:** You must track `lazyListState.firstVisibleItemIndex`.
- **Rule:** If `visibleIndex == videoPostIndex`, initialize Player. As soon as it changes, `release()` the player.

### **4. Implementation Details**

#### **Step 1: The Polymorphic List (Optimized)**

The `contentType` parameter is critical. It tells Compose: "This item is a Video. Only recycle this node for other Videos." This prevents Compose from trying to turn a Text View into a Video Player, which is expensive.

```kotlin
@Composable
fun NewsFeed(feedItems: LazyPagingItems<FeedItem>) {
    LazyColumn {
        items(
            count = feedItems.itemCount,
            key = feedItems.itemKey { it.id }, // Stable Key

            // CRITICAL OPTIMIZATION: Group items by type
            contentType = { index -> feedItems[index]?.type }
        ) { index ->
            val item = feedItems[index]

            when (item) {
                is FeedItem.TextPost -> TextPostRow(item)
                is FeedItem.ImagePost -> ImagePostRow(item)
                is FeedItem.VideoPost -> VideoPostRow(item)
                is FeedItem.Ad -> AdRow(item)
                null -> PlaceholderRow()
            }
        }
    }
}

```

#### **Step 2: Video Player (Resource Safety)**

We use `DisposableEffect` to ensure the player is killed exactly when the post leaves the screen.

```kotlin
@Composable
fun VideoPlayer(url: String, isVisible: Boolean) {
    val context = LocalContext.current

    // 1. Create Player ONLY if visible
    if (isVisible) {
        val exoPlayer = remember {
            ExoPlayer.Builder(context).build().apply {
                setMediaItem(MediaItem.fromUri(url))
                prepare()
                playWhenReady = true
            }
        }

        // 2. Attach to View
        AndroidView(
            factory = { PlayerView(context).apply { player = exoPlayer } },
            modifier = Modifier.aspectRatio(16/9f)
        )

        // 3. Cleanup when 'isVisible' becomes false or user leaves screen
        DisposableEffect(exoPlayer) {
            onDispose {
                exoPlayer.release()
            }
        }
    } else {
        // Show a static thumbnail image when not playing to save resources
        Image(painter = rememberAsyncImagePainter(thumbnailUrl), ...)
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`LazyPagingItems`, `contentType` optimization, `remoteMediator`, ExoPlayer Lifecycle, `DisposableEffect` cleanup, `firstVisibleItemIndex`, Nested Scrolling (Horizontal Carousel inside Vertical List).

**Interview Speak Paragraph**

> "For the Social Feed project, my primary focus was scroll performance and memory efficiency. I implemented **Paging 3** to handle infinite scrolling, ensuring that we strictly load data in small chunks. To handle the complex, heterogeneous layouts (mixed text, images, and videos), I utilized `LazyColumn` with the `contentType` parameter. This hints the Compose runtime to reuse nodes efficiently, similar to `getItemViewType` in the old View system. For the video auto-play feature, I avoided creating multiple ExoPlayer instances. Instead, I tracked the `LazyListState` to identify the currently centered item and only initialized the player for that specific node, immediately releasing it via `DisposableEffect` when it scrolled out of view."

---

Here are your detailed notes for **Topic 15.2 Addendum: Prefetching in Compose**.

---

## **Topic 15.2 (Addendum): Prefetching in Social Feeds**

### **1. What It Is**

Prefetching is the proactive loading of content (images, videos, or data pages) _before_ the user actually scrolls to them.

- **Standard Loading:** User scrolls -> "Loading..." spinner -> Data appears.
- **Prefetching:** User scrolls -> Data is already there (Zero-Latency feel).

### **2. Why It Exists (The "0ms" Latency Goal)**

In a social feed, waiting 500ms for an image to load feels "laggy." If the user is looking at Post #5, we should be silently downloading the images for Post #6 and #7 in the background so they appear instantly when scrolled into view.

### **3. How It Works in Compose**

There are two distinct layers of prefetching you must handle:

1. **Data Prefetching (Paging 3):** Fetching the JSON for the next page of items.
2. **Asset Prefetching (Coil/ExoPlayer):** Downloading the actual bytes for images/videos.

---

#### **A. Data Prefetching (Paging 3 Built-in)**

The Paging 3 library handles JSON prefetching automatically via the `prefetchDistance` parameter in its configuration.

- **Config:** You tell the Pager: "If the user is within 5 items of the end, silently fetch the next page."

```kotlin
val flow = Pager(
    PagingConfig(
        pageSize = 20,
        // The Magic Number:
        // Trigger next page load when user is 5 items away from bottom.
        prefetchDistance = 5,
        enablePlaceholders = false
    )
) { ... }.flow

```

#### **B. Image Prefetching (Coil Integration)**

Coil (the standard image loader for Compose) allows you to "warm up" the cache. The strategy involves observing the scrolling state and preloading the URLs of the _next_ few items.

**The Strategy:**

1. **Monitor State:** Use `rememberLazyListState()` to track the `firstVisibleItemIndex`.
2. **Calculate Range:** If index 5 is visible, identify the URLs for indices 6 through 10.
3. **Enqueue Request:** Call `imageLoader.enqueue(request)` with `Priority.LOW` (so it doesn't compete with the currently visible images).

### **4. Example: The Prefetching Hook**

This is a reusable Composable helper that silently loads images for upcoming posts. It separates the "Loading Logic" from the "Rendering Logic."

```kotlin
@Composable
fun FeedPrefetcher(
    listState: LazyListState,
    feedItems: LazyPagingItems<FeedItem>,
    prefetchOffset: Int = 5 // How many items ahead to look
) {
    val context = LocalContext.current
    val imageLoader = context.imageLoader

    // 1. Efficiently monitor the scroll position
    // derivedStateOf ensures we only run logic when the index CHANGES,
    // not on every pixel scroll.
    val firstVisibleIndex by remember { derivedStateOf { listState.firstVisibleItemIndex } }

    LaunchedEffect(firstVisibleIndex) {
        // 2. Calculate the range we want to prefetch
        // e.g., If visible is 10, prefetch 11, 12, 13, 14, 15
        val start = firstVisibleIndex + 1
        val end = (start + prefetchOffset).coerceAtMost(feedItems.itemCount - 1)

        for (i in start..end) {
            val item = feedItems[i] // Safe access to Paging data

            // Only prefetch if it's an Image Post
            if (item is FeedItem.ImagePost) {
                val request = ImageRequest.Builder(context)
                    .data(item.imageUrl)
                    // CRITICAL: Set Priority LOW.
                    // We don't want to slow down the images the user is looking at NOW.
                    .priority(Priority.LOW)
                    .build()

                // Fire and forget - loads into disk cache
                imageLoader.enqueue(request)
            }
        }
    }
}

```

### **5. Usage in the Feed Screen**

```kotlin
@Composable
fun SocialFeedScreen(viewModel: FeedViewModel) {
    val feedItems = viewModel.feed.collectAsLazyPagingItems()
    val listState = rememberLazyListState()

    // 1. Activate the Prefetcher (Invisible Logic)
    // It sits here silently and warms up the cache
    FeedPrefetcher(
        listState = listState,
        feedItems = feedItems
    )

    // 2. The UI
    LazyColumn(state = listState) {
        items(
            count = feedItems.itemCount,
            contentType = { feedItems[it]?.type }
        ) { index ->
            // When this row finally appears, the image is likely
            // already in the disk cache -> Instant Load!
            FeedItemRow(feedItems[index])
        }
    }
}

```

### **6. Interview Prep (Prefetching)**

**Interview Keywords**
`prefetchDistance` (Paging Config), `ImageLoader.enqueue`, Low Priority Requests, `derivedStateOf` (Scroll Monitoring), Cache Warming, Network Bandwidth Management, Decoupled Logic.

**Interview Speak Paragraph**

> "To achieve a buttery-smooth scrolling experience in media-heavy feeds, I implement a two-tiered prefetching strategy. First, I configure the Paging 3 `prefetchDistance` to ensure the next page of JSON data is fetched well before the user hits the bottom. Second, I implement a custom `LaunchedEffect` that observes the `LazyListState`. It calculates the indices of the upcoming 5 rows and submits `Priority.LOW` requests to the Coil ImageLoader. This 'warms up' the disk cache, so by the time the user scrolls the image into view, it loads instantly from the file system rather than waiting for a network handshake."

---

**Next Step:**
You have optimized the feed to perfection with Paging and Prefetching.
Ready for **Topic 15.3: E-Commerce Dashboard**? This focuses on complex nested layouts (Carousels inside Grids).

---

## Navigation

â† Previous
Next â†’
