---
layout: default
title: HorizontalPager / VerticalPager
parent: 3. Lists, Grids & UI Enhancements
nav_order: 6
---

# HorizontalPager / VerticalPager

Here are your notes for **Topic 3.6**.

---

## **Topic 3.6: HorizontalPager / VerticalPager**

### **1. What It Is**

These are the Compose equivalents of the old `ViewPager` or `ViewPager2`.

- **`HorizontalPager`:** Allows users to swipe left and right through pages (e.g., Image Carousel, Onboarding Screens).
- **`VerticalPager`:** Allows users to swipe up and down (e.g., TikTok or YouTube Shorts feed).

### **2. Why It Exists**

Lists (`LazyColumn`) are for scrolling smoothly through continuous content.
Pagers are for **snapping** to distinct "Pages." When you let go of your finger, a Pager doesn't just coast to a stop anywhere; it snaps perfectly to center the current item.

### **3. How It Works**

#### **A. The `PagerState` (The Brain)**

Just like Lists have `LazyListState`, Pagers have `PagerState`. You must create this first. It controls:

- Which page is currently active (`currentPage`).
- How far you have scrolled (`currentPageOffsetFraction`).
- Programmatic scrolling (`scrollToPage`).

#### **B. The Indicator (The Dots)**

Compose (unlike the old View system) does not have a built-in "TabLayout" indicator for simple dots. You usually build this yourself by drawing a `Row` of circles and checking:
`if (index == state.currentPage) Color.Black else Color.Gray`.

### **4. Example: Image Carousel with Dots**

```kotlin
@Composable
fun ImageCarousel(images: List<Int>) {
    // 1. Create the State
    // "pageCount" tells the state how many items exist
    val pagerState = rememberPagerState(pageCount = { images.size })

    Column {
        // 2. The Pager Area
        HorizontalPager(
            state = pagerState,
            modifier = Modifier.height(200.dp).fillMaxWidth()
        ) { pageIndex ->
            // This lambda is like "onBindViewHolder"
            Image(
                painter = painterResource(id = images[pageIndex]),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
        }

        Spacer(modifier = Modifier.height(8.dp))

        // 3. The Custom Indicators (Dots)
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center
        ) {
            repeat(images.size) { iteration ->
                val color = if (pagerState.currentPage == iteration) Color.DarkGray else Color.LightGray
                Box(
                    modifier = Modifier
                        .padding(2.dp)
                        .clip(CircleShape)
                        .background(color)
                        .size(8.dp)
                )
            }
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`rememberPagerState`, `pageCount`, Snapping, `currentPageOffsetFraction`, Custom Indicator, ViewPager2 migration.

**Interview Speak Paragraph**

> "For implementing carousels or onboarding flows, I use `HorizontalPager`. It replaces the legacy ViewPager2. The core component is the `PagerState`, which we initialize using `rememberPagerState`. This state object is powerful—it not only tracks the `currentPage` for logic (like updating a bottom tab) but also provides the `currentPageOffsetFraction`. This offset is crucial for creating advanced animations, like fading out a page as it is swiped away, or synchronizing a custom page indicator."

---

**Next Step:**
We have covered the main screen elements. Now, what about pop-ups?
Ready for **Topic 3.7: Dialogs & Popups**? This is how you handle alerts and overlays.

---

## Navigation

â† Previous
Next â†’
