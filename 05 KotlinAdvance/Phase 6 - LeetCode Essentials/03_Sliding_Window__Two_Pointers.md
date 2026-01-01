---
layout: default
title: "Sliding Window & Two Pointers"
parent: "Advanced Kotlin: Phase 6   Leetcode Essentials"
nav_order: 3
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Sliding Window & Two Pointers"
parent: "LeetCode Essentials (Kotlin)"
nav_order: 3
---

# Sliding Window & Two Pointers

<!-- Content starts here -->

Here are your interview-focused notes for **Sliding Window & Two Pointers**.

---

### **Topic: Sliding Window & Two Pointers**

#### **What It Is**

These are two optimization techniques used to solve array/string problems without using nested loops (Avoiding ).

1. **Two Pointers:** Using two variables (indices) to traverse an array, usually moving towards each other or moving in the same direction at different speeds.
2. **Sliding Window:** Creating a "frame" (window) over a part of the array and sliding it one step at a time to calculate something (like a sum) without recalculating the whole thing.

#### **Why It Exists**

**The Brute Force Problem ():**
If asked: "Find the maximum sum of any 3 consecutive numbers."

- **Bad way:** Loop `i` from 0 to end. Inside that, loop `j` from `i` to `i+3`. Sum them up.
- **The Problem:** You are re-adding numbers you just added.

**The Solution ():**

- **Sliding Window:** Instead of re-adding, you just **subtract** the number that fell out of the left side and **add** the number that entered the right side.
- **Two Pointers:** Instead of trying every combination of pairs, you use sorted logic to skip impossible pairs.

#### **How It Works**

1. **Two Pointers:** Set `left = 0` and `right = lastIndex`. Move them based on a condition (e.g., if sum is too small, move left; if too big, move right).
2. **Sliding Window:** Keep a running sum.

- Add `arr[right]`.
- If window size > `k`, subtract `arr[left]` and increment `left`.

**Kotlin Shortcut:** Kotlin has a built-in function `windowed(size, step)` that does this automatically for you!

#### **Example**

```kotlin
fun main() {
    // 1. SLIDING WINDOW (Manual - The Interview Way)
    // Problem: Max sum of 3 consecutive elements
    val nums = listOf(1, 4, 2, 10, 23, 3, 1, 0, 20)
    val k = 4

    var windowSum = 0
    var maxSum = 0

    for (i in nums.indices) {
        windowSum += nums[i] // Add element entering the window

        // Once we hit the window size 'k'
        if (i >= k - 1) {
            maxSum = maxOf(maxSum, windowSum)
            // Remove the element leaving the window (the leftmost one)
            windowSum -= nums[i - (k - 1)]
        }
    }
    println("Max Sum (Manual): $maxSum") // Output: 39 (10+23+3+3)

    // 2. KOTLIN SHORTCUT (windowed)
    // Great for production code or quick scripting
    val maxWithKotlin = nums.windowed(size = 4, step = 1) { window ->
        window.sum()
    }.maxOrNull()

    println("Max Sum (Kotlin): $maxWithKotlin")

    // 3. TWO POINTERS (Classic "Two Sum - Sorted")
    // Problem: Find two numbers that add up to Target in a SORTED list
    val sortedNums = listOf(1, 2, 7, 11, 15)
    val target = 9

    var left = 0
    var right = sortedNums.lastIndex

    while (left < right) {
        val sum = sortedNums[left] + sortedNums[right]
        if (sum == target) {
            println("Found pair: ${sortedNums[left]}, ${sortedNums[right]}")
            break
        } else if (sum < target) {
            left++ // Need bigger number
        } else {
            right-- // Need smaller number
        }
    }
}

```

#### **Visual Representation**

```text
    Sliding Window (Sum of 3):
    [ 2, 1, 5 ], 1, 3, 2  -> Sum: 8
       [ 1, 5, 1 ], 3, 2  -> Sum: 7 (Subtract 2, Add 1)
          [ 5, 1, 3 ], 2  -> Sum: 9 (Subtract 1, Add 3)

    Two Pointers (Target 9):
    [ 1 ... ... ... 15 ] -> Sum 16 (Too big, move Right)
    [ 1 ... ... 11 ]     -> Sum 12 (Too big, move Right)
    [ 1 ... 7 ]          -> Sum 8  (Too small, move Left)
    [ 2 ... 7 ]          -> Sum 9  (Found!)

```

#### **Interview Keywords**

Subarray, Substring, Contiguous, Window Size, Left/Right Pointers, Running Sum, vs , In-Place.

#### **Interview Speak Paragraph**

"For problems involving contiguous subarrays or substrings, I invariably use the **Sliding Window** technique. It allows me to convert a nested loop solution () into a linear one () by maintaining a running state (like a sum) and adjusting it as the window moves. For searching pairs in a sorted array, I use the **Two Pointers** approach, starting from both ends and narrowing down. In Kotlin, if I need a quick non-optimized solution, I use the `windowed()` extension function, but for performance-critical interview questions, I implement the index manipulation manually to avoid object creation."

---

**Would you like to move on to the next topic: Stack & Queue Implementations?**
