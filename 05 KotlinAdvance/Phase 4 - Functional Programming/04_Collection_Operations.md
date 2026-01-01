---
layout: default
title: Collection Operations
parent: Advanced Kotlin: Phase 4   Functional Programming
nav_order: 4
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Collection Operations"
parent: "Functional Programming & Scoping"
nav_order: 4
---

# Collection Operations

<!-- Content starts here -->

Here are your interview-focused notes for **Collection Operations**. This is the last topic of Phase 4!

---

### **Topic: Collection Operations (Filter, Map, FlatMap, Zip)**

#### **What It Is**

These are powerful functions that allow you to process and transform lists of data **declaratively**.
Instead of writing a manual `for` loop to go through items one by one, creating temporary variables, and adding them to a new list, you just tell Kotlin **what** you want to happen.

- **`filter`**: Keeps only the items that match a condition.
- **`map`**: Changes every item into something else (1-to-1 transformation).
- **`flatMap`**: Unpacks nested lists into one single list (Flattening).
- **`zip`**: Glues two lists together into pairs.

#### **Why It Exists**

**The "For-Loop" Problem:**
Old code: "Create empty list. Loop through original. Check `if` age > 18. If yes, get name. Add name to new list."
This is **Imperative** (Micromanaging). It's long and error-prone.

**The Solution:**
Kotlin code: `list.filter { age > 18 }.map { name }`
This is **Declarative** (Manager style). You just say "Filter by age, then map to names." It reads like a sentence.

#### **How It Works**

1. **`filter`**: Takes a predicate (true/false). If true, keeps item.
2. **`map`**: Takes a function. Returns a new list where every item is transformed.
3. **`flatMap`**: Use this when your map function returns a _List_, but you don't want a `List<List<String>>`. You just want one big `List<String>`.
4. **`zip`**: Takes two lists of equal size (usually) and merges index 0 with index 0, 1 with 1.

#### **Example**

```kotlin
data class User(val name: String, val age: Int, val emails: List<String>)

fun main() {
    val users = listOf(
        User("Alice", 25, listOf("alice@work.com", "alice@home.com")),
        User("Bob", 15, listOf("bob@gmail.com")),
        User("Charlie", 30, listOf())
    )

    // 1. FILTER & MAP (The Classic Combo)
    // "Get names of all adults"
    val adultNames = users
        .filter { it.age >= 18 } // Only Alice and Charlie
        .map { it.name }         // Transform User -> String

    println(adultNames) // Output: [Alice, Charlie]

    // 2. FLATMAP (The Unpacker)
    // "Give me ONE list of ALL emails from EVERYONE"
    // If we used .map, we would get [[email, email], [email], []] (List of Lists)
    val allEmails = users.flatMap { it.emails }

    println(allEmails)
    // Output: [alice@work.com, alice@home.com, bob@gmail.com] (One flat list)

    // 3. ZIP (The Merger)
    val students = listOf("A", "B", "C")
    val scores = listOf(90, 85, 92)

    val reportCard = students.zip(scores)
    println(reportCard)
    // Output: [(A, 90), (B, 85), (C, 92)]
}

```

#### **Visual Representation**

```text
    Original:   [ 1, 2, 3, 4 ]

    filter(isEven) ->  [ 2, 4 ]              (Subset)

    map(x * 10)    ->  [ 10, 20, 30, 40 ]    (Transformation)

    flatMap        ->  [[1,2], [3,4]]  becomes  [1, 2, 3, 4]  (Flattening)

    zip([A, B])    ->  [(1,A), (2,B)]        (Merging)

```

#### **Interview Keywords**

Declarative Programming, Transformation, Predicate, Flattening, Intermediate Operations, Chaining, Lazy Evaluation (Sequences).

> **Pro Interview Tip (Sequences):** If you have a massive list (1 million items), chaining `.filter().map()` is slow because it creates a new temporary list for _every_ step.
> **Solution:** "For large datasets, I convert the list to a **Sequence** using `.asSequence()`. This processes items one by one through the whole chain (lazily) without creating temporary lists."

#### **Interview Speak Paragraph**

"I avoid traditional `for` loops for data transformation and instead rely on standard collection operators. I use `filter` to select specific items and `map` to transform them, which makes the code readable and chainable. A key distinction I always make is between `map` and `flatMap`: if I need to transform an object into a list of items and then combine them all into a single list (like getting all phone numbers from a list of users), I use `flatMap` to avoid creating nested lists."

---

### **🎉 Phase 4 Complete!**

You have mastered **Functional Programming**. You know how to pass logic with Lambdas, configure objects with Scope Functions, and transform data like a data scientist.

**Ready for the Heavy Lifting?**
Phase 5 is **Advanced Topics & Async**. This is where we learn **Coroutines**—the topic that separates Junior devs from Senior devs.

**Shall we start Phase 5 with "Generics (<T>)"?**
