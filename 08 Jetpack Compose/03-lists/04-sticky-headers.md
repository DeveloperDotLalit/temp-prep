---
layout: default
title: "Sticky Headers"
parent: "3. Lists, Grids & UI Enhancements"
nav_order: 4
---

# Sticky Headers

Here are your notes for **Topic 3.4**.

---

## **Topic 3.4: Sticky Headers**

### **1. What It Is**

Sticky Headers are section titles in a scrollable list that "stick" or pin themselves to the top of the screen while you are scrolling through the items in that section.
As soon as you reach the next section, the new header pushes the old one up and out of view.

### **2. Why It Exists (The Context Problem)**

Imagine scrolling through a list of 2,000 contacts. You are in the middle of the "M" names.

- **Without Sticky Headers:** You scroll down and forget which letter you are looking at. Are these M's or N's? You have to scroll back up to check.
- **With Sticky Headers:** The letter "M" stays pinned at the top until you scroll past the last "M" name. It provides constant **Context** to the user.

### **3. How It Works**

To implement this, you typically need to structure your data as a **Map** (Group -> List of Items) rather than a flat List.

1. **Group Data:** Convert `List<String>` into `Map<Char, List<String>>` (e.g., 'A' -> ["Alex", "Adam"], 'B' -> ["Bob"]).
2. **Lazy DSL:** Inside the `LazyColumn`, you iterate through this Map.
3. **The Function:** Instead of `item`, you use the special `stickyHeader` function for the title.

### **4. Example: Contacts List**

```kotlin
@OptIn(ExperimentalFoundationApi::class) // Required for stickyHeader
@Composable
fun ContactList(names: List<String>) {
    // 1. Prepare Data: Group names by first letter
    // Result: {'A': ["Adam", "Alice"], 'B': ["Bob"], ...}
    val grouped = remember(names) {
        names.sorted().groupBy { it.first() }
    }

    LazyColumn {
        // 2. Iterate over the Groups
        grouped.forEach { (initial, namesInGroup) ->

            // 3. The Sticky Header
            stickyHeader {
                Text(
                    text = initial.toString(),
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color.LightGray) // Header needs a background!
                        .padding(8.dp)
                )
            }

            // 4. The Items in that Group
            items(namesInGroup) { name ->
                Text(name, modifier = Modifier.padding(16.dp))
            }
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Grouped Data, Map Structure, `stickyHeader`, `ExperimentalFoundationApi`, Context preservation, Z-Index (Header sits on top).

**Interview Speak Paragraph**

> "I use Sticky Headers primarily for long, categorized lists like contacts or date-based history feeds. The implementation in Compose is straightforward using the `stickyHeader` function within a `LazyColumn`. The key pre-requisite is transforming the flat data list into a grouped Map structure (like grouping by initial or date). It's also important to give the header a solid background color; otherwise, the scrolling content underneath will be visible through the header, which ruins the 'pinned' illusion."

---

**Next Step:**
We can scroll, but can we interact? What if users want to delete items?
Ready for **Topic 3.5: Swipe to Dismiss / Delete**? This is the standard pattern for removing emails or notifications.

---

## Navigation

â† Previous
Next â†’
