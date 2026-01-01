---
layout: default
title: Sorting & Comparators
parent: Advanced Kotlin: Phase 6   Leetcode Essentials
nav_order: 5
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Sorting & Comparators"
parent: "LeetCode Essentials (Kotlin)"
nav_order: 5
---

# Sorting & Comparators

<!-- Content starts here -->

Here are your interview-focused notes for **Sorting & Comparators**. This is the final topic of Phase 6!

---

### **Topic: Sorting & Comparators**

#### **What It Is**

Sorting is rearranging a list of items into a specific order (Ascending or Descending).

- **Natural Order:** The default way things are sorted (1, 2, 3... or A, B, C...).
- **Custom Comparators:** Rules you define for complex objects. (e.g., "Sort users by Age. If ages are equal, sort by Name").

#### **Why It Exists**

**The "Unknown Order" Problem:**
Kotlin knows how to sort `Int` (1 < 5) and `String` ("A" < "B").
But if you have a `List<User>`, Kotlin has no idea what to do.
`User("Bob", 20)` vs `User("Alice", 25)`. Who comes first?
You must provide the logic using a **Comparator**.

#### **How It Works**

1. **`sorted()` / `sort()**`: Uses natural order. (`sorted`returns a new list,`sort` modifies the existing mutable list).
2. **`sortBy { it.property }`**: The quick, one-line way to sort by a specific field.
3. **`compareBy` / `sortWith**`: The powerful way to handle **multi-level** sorting (e.g., sort by Priority, _then_ by Time).

#### **Example**

```kotlin
data class Student(val name: String, val score: Int)

fun main() {
    val students = mutableListOf(
        Student("Charlie", 80),
        Student("Alice", 90),
        Student("Bob", 90) // Same score as Alice
    )

    // 1. SIMPLE SORT (sortBy)
    // "Sort by score (low to high)"
    students.sortBy { it.score }
    println(students)
    // Output: [Charlie(80), Alice(90), Bob(90)]

    // 2. DESCENDING SORT (sortByDescending)
    students.sortByDescending { it.score }

    // 3. MULTI-LEVEL SORT (compareBy)
    // "Sort by Score (High to Low). If tied, sort by Name (A-Z)"
    val complexSort = students.sortedWith(
        compareByDescending<Student> { it.score }
            .thenBy { it.name }
    )

    println(complexSort)
    // Output: [Alice(90), Bob(90), Charlie(80)]
    // (Alice is before Bob because of the tie-breaker)
}

```

#### **Visual Representation**

```text
    Unsorted:
    [ (Bob, 90), (Alice, 90), (Charlie, 80) ]

    Sort By Score (Descending):
    [ (Bob, 90), (Alice, 90) ], [ (Charlie, 80) ]
       ^           ^
       |           |-- Tie!

    Then By Name (Ascending):
    [ (Alice, 90), (Bob, 90) ], [ (Charlie, 80) ]

```

#### **Interview Keywords**

Comparator, Comparable, Natural Order, Stable Sort, In-Place vs Copy, `sorted` vs `sort`, Chaining Comparators.

> **Pro Interview Tip (Stable Sort):** "Is Kotlin's sort stable?"
> **Answer:** "Yes, Kotlin uses TimSort (inherited from Java), which is a **Stable Sort**. This means if two items are equal (like Alice and Bob having the same score), their original relative order is preserved unless a secondary comparator explicitly reorders them."

#### **Interview Speak Paragraph**

"When sorting primitive types, I rely on the standard `sorted()` function. However, for custom objects, I use `sortBy` for simple single-field sorting because it's concise. For complex requirements—like sorting a list of emails by date, and then by sender if the dates are identical—I use `sortWith` combined with `compareBy`. This allows me to chain multiple sorting rules easily using `.thenBy()`, creating clean and readable multi-level sorting logic."

---

### **🎉 Phase 6 Complete!**

You have mastered **LeetCode Essentials**. You can manipulate Strings efficiently, use HashMaps for O(1) lookups, slide windows over arrays, and sort complex data.

**Ready for the Real World?**
Phase 7 is **Real-World Interview Scenarios**. We will simulate actual "Fix this code" and "Design this feature" questions that interviewers love.

**Shall we start Phase 7 with "Scenario: Refactor this Java code to Kotlin"?**
