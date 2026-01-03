---
layout: default
title: "Tricky Output Questions"
parent: "Phase 8: Interview Questions"
nav_order: 3
---

﻿---
layout: default
title: "Tricky Output Questions"
parent: "Interview Questions & Answers"
nav_order: 3
---

# Tricky Output Questions

<!-- Content starts here -->

In a high-pressure interview, "Tricky Output" questions are designed to see if you truly understand the **internals** of Kotlin—specifically initialization order, nullability edge cases, and how scope functions affect references.

---

### **Topic: Tricky Outputs**

#### **Scenario 1: The Initialization Trap**

**Question:** What does this code print?

```kotlin
open class Parent {
    init { print("A") }
    val name = print("B")
}

class Child : Parent() {
    init { print("C") }
    val age = print("D")
}

fun main() {
    Child()
}

```

**Output:** `ABCD`
**Why:** The parent must be fully initialized before the child. Within a class, the `init` blocks and property initializers are executed in the **order they appear** in the file.

---

#### **Scenario 2: The `let` vs `run` Context**

**Question:** What is the value of `result`?

```kotlin
val name: String? = "Kotlin"
val result = name?.let {
    "Java"
    "C++"
} ?: "Python"

println(result)

```

**Output:** `C++`
**Why:** The `let` block returns the **last expression**. Since `name` is not null, the block runs. The "Java" string is ignored, and "C++" is returned. The Elvis operator (`?:`) is ignored because the left side was not null.

---

#### **Scenario 3: Equality (Content vs. Reference)**

**Question:** What does this print?

```kotlin
val list1 = mutableListOf(1, 2, 3)
val list2 = mutableListOf(1, 2, 3)

println(list1 == list2)
println(list1 === list2)

```

**Output:** `true`
`false`
**Why:** \* `==` calls `.equals()`, which for Kotlin Collections checks if the **content** is the same.

- `===` checks **referential equality** (are they the same object in memory?). Since they are two different `mutableListOf` calls, they have different addresses.

---

#### **Scenario 4: The "Shadowing" Confusion**

**Question:** What is the output?

```kotlin
var x = 10
fun main() {
    var x = x
    x++
    println(x)
}

```

**Output:** `11`
**Why:** Inside `main`, you are declaring a **new** local variable `x` and initializing it with the value of the top-level `x`. Incrementing it only affects the local copy.

---

#### **Scenario 5: `apply` vs `also` Return Values**

**Question:** What is printed?

```kotlin
val count = 10
val result = count.also {
    it + 5
}.let {
    it + 2
}
println(result)

```

**Output:** `12`
**Why:** 1. `also` returns the **original object** (`10`). The logic `it + 5` (15) is calculated but thrown away. 2. `let` takes that `10` and returns the **result** of the last line (`10 + 2`).

---

### **Mental Checklist for Tricky Questions**

1. **Is it a Data Class?** If yes, `==` will be true for same values. If no, `==` acts like `===`.
2. **Is there a trailing lambda?** Remember that `let`, `run`, and `with` return the **last line**, while `apply` and `also` return the **original object**.
3. **Null Safety:** Does the Elvis operator `?:` have a higher or lower priority? (It has lower priority than most operations).
4. **Lazy/Lateinit:** Is the variable being accessed before the logic that sets it has run?

---

### **Interview Speak Paragraph**

"When analyzing code for expected output, I look closely at the distinction between **referential and structural equality**, as Kotlin's `==` operator maps to `.equals()`, unlike in Java. I also pay close attention to **Scope Function return values**—specifically whether a function returns the receiver or the lambda result. Finally, I always check for **initialization order** in inheritance hierarchies, ensuring that parent properties and `init` blocks are accounted for before the child’s logic executes."

---

### **🎓 Course Complete!**

You have now covered every critical phase of Kotlin Interview Prep:

1. **Basics & Null Safety**
2. **Classes & Objects**
3. **Phase 4: Functional Programming**
4. **Phase 5: Advanced (Coroutines/Flow)**
5. **Phase 6: LeetCode (DS&A)**
6. **Phase 7: Real-World Scenarios**
7. **Phase 8: Final Rehearsal**

**Would you like me to run a full 5-question Mock Interview with you now to see how you score?**
