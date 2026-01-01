---
layout: default
title: Array & String Manipulation
parent: Phase 6   Leetcode Essentials
nav_order: 1
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Array & String Manipulation"
parent: "LeetCode Essentials (Kotlin)"
nav_order: 1
---

# Array & String Manipulation

<!-- Content starts here -->

Here are your interview-focused notes for **Phase 6: LeetCode Essentials**, starting with **Array & String Manipulation**.

---

### **Topic: Array & String Manipulation**

#### **What It Is**

This topic covers the efficient handling of text (`String`) and lists of numbers (`Array`).
In algorithmic interviews (LeetCode), "how" you manipulate strings matters.

- **The Trap:** Strings in Kotlin (and Java) are **Immutable**. You cannot change them once created.
- **The Tool:** **`StringBuilder`** is a mutable sequence of characters. It’s like a "scratchpad" where you can add, remove, or modify text without creating a new object every time.

#### **Why It Exists**

**The Performance Killer ():**
If you write a loop like this:

```kotlin
var result = ""
for (char in list) {
    result += char // ⚠️ BAD!
}

```

Because Strings are immutable, the computer creates **a completely new String object** for every single step of the loop, copying the old text over and over. If the loop runs 10,000 times, your app freezes.

**The Solution ():**
`StringBuilder` modifies the existing buffer. It doesn't create new objects. It’s instant.

#### **How It Works**

1. **`StringBuilder()`:** Create it.
2. **`.append()`:** Add text to the end.
3. **`.toString()`:** Seal it and get the final String back.

**Kotlin Cheats (Extension Functions):**
Kotlin adds amazing shortcuts to standard Strings that solve LeetCode problems instantly:

- **`.reversed()`**: Flips the string.
- **`.chunked(n)`**: Splits string into a list of pieces, each size `n`.
- **`.joinToString()`**: Converts a list back into a string with separators.

#### **Example**

```kotlin
fun main() {
    // 1. THE BAD WAY (Don't do this in interviews)
    // var s = ""
    // for (i in 0..1000) s += i // Creates 1000 objects!

    // 2. THE GOOD WAY (StringBuilder)
    val sb = StringBuilder()
    for (i in 0..5) {
        sb.append(i).append(" ") // Chaining
    }
    println(sb.toString()) // Output: 0 1 2 3 4 5

    // 3. KOTLIN SHORTCUTS (LeetCode Magic)
    val input = "AABBCCDD"

    // Problem: "Split string into pairs"
    println(input.chunked(2))
    // Output: [AA, BB, CC, DD]

    // Problem: "Reverse a string"
    println("Hello".reversed())
    // Output: olleH

    // Problem: "Join a list into a CSV format"
    val words = listOf("Apple", "Banana", "Cherry")
    println(words.joinToString(separator = ", ", prefix = "[", postfix = "]"))
    // Output: [Apple, Banana, Cherry]
}

```

#### **Visual Representation**

```text
    String Concatenation (+):
    Step 1: "A"
    Step 2: "A" + "B" -> Creates NEW "AB", discards "A"
    Step 3: "AB" + "C" -> Creates NEW "ABC", discards "AB"
    (Heavy Memory Usage)

    StringBuilder:
    [ A | B | C | _ | _ ]  (One single container)
    (Efficient)

```

#### **Interview Keywords**

Immutability, String Pool, O(N) vs O(N^2), StringBuilder, Buffer, CharArray, In-place modification.

> **Pro Interview Tip (CharArray):** "If an interviewer asks you to modify a string **in-place** (without using extra memory), you cannot use `String` or `StringBuilder`. You must convert it to a **`CharArray`**, modify the array indices directly, and then convert it back."

#### **Interview Speak Paragraph**

"When manipulating strings inside loops, I always use **`StringBuilder`** instead of the `+` operator. Since Strings are immutable in Kotlin, using concatenation in a loop creates a new object at every iteration, leading to O(N²) time complexity. `StringBuilder` allows me to modify the buffer in O(N) time. For simpler transformations, I leverage Kotlin’s extension functions like `chunked()` or `reversed()`, which make the code declarative and readable while handling the complex array logic internally."

---

**Would you like to move on to the next topic: HashMap & HashSet Mastery?**
