---
layout: default
title: Handling Complex Lists (Heterogeneous Views
parent: Phase6
nav_order: 4
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **Handling Complex Lists (Heterogeneous Views)**.

This is a classic "Real World" problem. Tutorials show simple lists, but real apps (like Instagram or YouTube) have Headers, Ads, Carousels, and Videos all in one scrollable feed.

---

### **Topic: Handling Complex Lists (Heterogeneous Views)**

#### **What It Is**

A **Heterogeneous RecyclerView** is a list that displays **different types of layouts** inside the same scrolling container.

Instead of passing a simple `List<String>`, you pass a `List<ListItem>`, where `ListItem` can be anything:

- A "Header" (Text only).
- An "Ad" (Image + 'Sponsored' tag).
- A "Post" (User Avatar + Content + Likes).

#### **Why It Exists (The Problem)**

1. **Rich UI Requirements:** Modern apps are rarely just a uniform list of items. Marketing teams want ads injected every 5th item, and designers want "Featured" sections at the top.
2. **Type Safety:** If you just use `List<Any>`, you have to cast objects manually (`if (item is String) ...`), which is messy and crashes easily.
3. **Scalability:** We need a clean way to add a new type (e.g., "Video Item") next month without rewriting the entire Adapter.

#### **How It Works (The Polymorphic List)**

We use **Kotlin Sealed Classes** to enforce strict type safety.

1. **The Contract:** Create a `sealed class ListItem`. This is the parent of everything in the list.
2. **The Types:** Create specific data classes (`HeaderItem`, `AdItem`, `ContentItem`) that inherit from `ListItem`.
3. **The Adapter:**

- In `getItemViewType()`: Check which specific class the item is (e.g., Return `TYPE_AD`).
- In `onCreateViewHolder()`: Inflate the correct XML layout based on that type.
- In `onBindViewHolder()`: Bind the data to that specific View.

#### **Example (The Feed Structure)**

**1. The Sealed Class (The Data Model):**

```kotlin
// The parent class
sealed class FeedItem {
    // Type 1: Simple Header
    data class Header(val title: String) : FeedItem()

    // Type 2: The actual content
    data class Post(val id: Int, val text: String) : FeedItem()

    // Type 3: An Advertisement
    data class Ad(val adUrl: String) : FeedItem()
}

```

**2. The Adapter (The Logic):**

```kotlin
class FeedAdapter : ListAdapter<FeedItem, RecyclerView.ViewHolder>(DiffCallback) {

    // 1. Tell RecyclerView which layout to use
    override fun getItemViewType(position: Int): Int {
        return when (getItem(position)) {
            is FeedItem.Header -> R.layout.item_header
            is FeedItem.Post -> R.layout.item_post
            is FeedItem.Ad -> R.layout.item_ad
        }
    }

    // 2. Create the correct ViewHolder
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        // Inflate layout based on viewType...
        return when (viewType) {
            R.layout.item_header -> HeaderViewHolder(...)
            R.layout.item_ad -> AdViewHolder(...)
            else -> PostViewHolder(...)
        }
    }

    // 3. Bind Data safely
    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        val item = getItem(position)
        when (holder) {
            is HeaderViewHolder -> holder.bind(item as FeedItem.Header)
            is AdViewHolder -> holder.bind(item as FeedItem.Ad)
            is PostViewHolder -> holder.bind(item as FeedItem.Post)
        }
    }
}

```

#### **Interview Keywords**

Heterogeneous Views, `getItemViewType`, Sealed Class, Polymorphism, Multiple ViewHolders, ViewType Pattern, Scalable Adapter.

#### **Interview Speak Paragraph**

> "To handle complex lists with multiple view types—like headers, ads, and content—I use a Kotlin Sealed Class to define a base `ListItem` type. My RecyclerView Adapter accepts a list of this base type. I override `getItemViewType` to distinguish between the sealed subclasses (like `Header` or `Ad`) and inflate the corresponding layouts in `onCreateViewHolder`. This approach provides strict type safety and makes the code scalable; if I need to add a new 'Video' type later, I just add a new data class and a new `when` branch, without breaking existing logic."

---

**Would you like to proceed to the next note: "Pagination & Infinite Scrolling"?**
