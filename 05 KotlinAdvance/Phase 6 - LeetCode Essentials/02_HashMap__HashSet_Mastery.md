---
layout: default
title: HashMap & HashSet Mastery
parent: Phase 6   Leetcode Essentials
nav_order: 2
---

﻿---
layout: default
title: "HashMap & HashSet Mastery"
parent: "LeetCode Essentials (Kotlin)"
nav_order: 2
---

# HashMap & HashSet Mastery

<!-- Content starts here -->

Here are your interview-focused notes for **HashMap & HashSet Mastery**.

---

### **Topic: HashMap & HashSet Mastery**

#### **What It Is**

These are the most important data structures for coding interviews because they are **fast**.

- **HashSet:** A collection of **Unique Keys** (No duplicates). Like a club guest list—names are checked at the door, and no one gets in twice.
- **HashMap:** A collection of **Key-Value Pairs**. Like a coat check—you give a "Key" (ticket #5), and you get back the specific "Value" (your jacket).

#### **Why It Exists**

**The "Search" Problem ( vs ):**

- **List:** If you want to find "Alice" in a list of 1 million users, you have to check every single name until you find her. That is slow ().
- **Map/Set:** Hashing allows you to calculate _exactly_ where "Alice" is stored instantly. No searching required. That is **Constant Time ()**.

**Common Interview Use Case:**

- **HashSet:** "Remove duplicates from this list."
- **HashMap:** "Count how many times each word appears in this sentence" (Frequency Counter).

#### **How It Works**

1. **The Hash Code:** When you save "Alice", the computer runs a math formula (hash function) on the string "Alice" to get a number (e.g., 123).
2. **The Bucket:** It puts "Alice" directly into Box #123.
3. **Retrieval:** When you ask for "Alice" again, it re-calculates 123 and goes straight to Box #123. It doesn't look at Box #1 or Box #2.

#### **Example**

```kotlin
fun main() {
    // 1. HASHSET (Uniqueness)
    // Problem: "Does this list have duplicates?"
    val numbers = listOf(1, 2, 3, 1)
    val uniqueSet = HashSet<Int>()

    for (num in numbers) {
        if (uniqueSet.contains(num)) {
            println("Duplicate found: $num")
        }
        uniqueSet.add(num)
    }

    // 2. HASHMAP (Frequency Counting - The LeetCode Classic)
    // Problem: "Count the frequency of each char"
    val input = "banana"
    val frequencyMap = HashMap<Char, Int>()

    for (char in input) {
        // The "Old Java Way" (Verbose)
        // val count = frequencyMap.getOrDefault(char, 0)
        // frequencyMap[char] = count + 1

        // The "Kotlin Way" (Smart)
        // "getOrPut": If char exists, get it. If not, put 0.
        // Then increment.
        frequencyMap[char] = frequencyMap.getOrDefault(char, 0) + 1
    }

    println(frequencyMap)
    // Output: {b=1, a=3, n=2}

    // 3. GROUPING (Advanced Kotlin Shortcut)
    // Does the same thing as above in one line!
    val counts = input.groupingBy { it }.eachCount()
    println(counts)
}

```

#### **Visual Representation**

```text
    List Search (Slow):
    [ Bob ] -> [ Dave ] -> [ Alice? ] (Found her!)
    (Walked 3 steps)

    HashMap Search (Instant):
    "Alice" --(Hash Function)--> Box #5

    [ Box 1 ] [ Box 2 ] ... [ Box 5 ] ...
                               |
                            "Alice" (Direct Access)

```

#### **Interview Keywords**

Key-Value Pair, Collision, Load Factor, Buckets, Lookup, Frequency Map, `getOrPut`, `getOrDefault`.

> **Pro Interview Tip (Collision):** "What happens if two keys have the same Hash Code?"
> **Answer:** "This is called a **Collision**. The HashMap handles this by storing both items in the same bucket (usually as a Linked List or a Tree). When we look them up, it goes to the bucket and then checks the actual keys one by one. This slows access down slightly from to for that specific bucket."

#### **Interview Speak Paragraph**

"For problems involving lookups, uniqueness, or frequency counting, I always reach for a **HashMap** or **HashSet**. They provide average time complexity for insertions and retrievals, which is significantly faster than searching through a List. In Kotlin, I specifically use `getOrPut()` or the `groupingBy().eachCount()` extension to solve frequency problems concisely without writing boilerplate `if-else` logic to check if a key exists."

---

**Would you like to move on to the next topic: Sliding Window & Two Pointers?**
