---
layout: default
title: "Control Flow: if / else / when"
parent: "Phase 1: The Foundation"
nav_order: 4
---

﻿---
layout: default
title: "Control Flow: if / else / when"
parent: "The Foundation (Building Blocks)"
nav_order: 4
---

# Control Flow: if / else / when

<!-- Content starts here -->

Here are your interview-focused notes for **Control Flow (If/Else & When)**.

---

### **Topic: Control Flow (If/Else & When)**

#### **What It Is**

Control flow is how your code makes decisions.

- **`if` / `else`:** Standard logic. If a condition is true, do X; otherwise, do Y.
- **`when`:** This is Kotlin's replacement for the traditional `switch` statement found in other languages. It takes a value and checks it against multiple possible scenarios.

#### **Why It Exists**

**1. The `if` Upgrade:**
In Java, `if` is just a statement—it controls flow but doesn't give you a result. You needed the "ternary operator" (`result = condition ? a : b`) to assign values based on a check.
**Kotlin removed the ternary operator.** Why? Because in Kotlin, `if` is an **expression**. It returns a value automatically.

**2. The `when` Upgrade (The Supercharged Switch):**
Old `switch` statements were weak. They only worked with simple numbers or strings, and if you forgot to write `break`, the code would "fall through" and execute the wrong case.
**`when` fixes this:**

- **No `break` needed:** It stops automatically after finding a match.
- **Smart:** It can check ranges (1 to 10), types (is this a String?), and complex logic, not just simple matches.

#### **How It Works**

- **`if` as Expression:** You assign the result of the `if` block directly to a variable. The last line of the block is what gets returned.
- **`when` Logic:** Kotlin checks branches one by one. The moment it finds a match, it runs that code and **exits** the `when` block. It can also return a value just like `if`.

#### **Example**

```kotlin
fun main() {
    // 1. IF as an EXPRESSION (Replacing Ternary Operator)
    val a = 10
    val b = 20

    // In Java: int max = (a > b) ? a : b;
    // In Kotlin:
    val max = if (a > b) {
        println("A is bigger")
        a // Returns a
    } else {
        println("B is bigger")
        b // Returns b
    }
    println("Max value is: $max")

    // 2. WHEN (The Supercharged Switch)
    val score = 85

    val grade = when (score) {
        in 90..100 -> "A"       // Check a RANGE
        in 80..89 -> "B"
        in 70..79 -> "C"
        10, 20, 30 -> "Fail"    // Check MULTIPLE specific numbers
        !in 0..100 -> "Invalid" // Check what it is NOT
        else -> "D"             // "else" acts like "default"
    }
    println("Grade: $grade")

    // 3. WHEN without arguments (acting like a clean if-else chain)
    val x = 15
    when {
        x.isOdd() -> print("x is odd")
        x.isEven() -> print("x is even")
        else -> print("x is funny")
    }
}

```

#### **Visual Representation**

```text
    Traditional Switch (Java)       Kotlin 'when'
    -------------------------       -------------
    case 1:                         1 -> doSomething()
      doSomething();
      break; (Forget this? Bug!)    (No break needed!)

    case 2:                         2, 3 -> doSomethingElse()
    case 3:
      doSomethingElse();            in 10..20 -> doRange()
      break;
                                    is String -> doTypeCheck()

```

#### **Interview Keywords**

Expression vs. Statement, Ternary Operator, Pattern Matching, Smart Casting, Exhaustive, Range Check.

#### **Interview Speak Paragraph**

"I prefer Kotlin's control flow because both `if` and `when` are expressions, meaning they can return values directly, which reduces the need for temporary variables. Specifically, `when` is a massive improvement over the traditional `switch` statement. It eliminates common bugs like 'fall-through' because it doesn't need `break` statements. It's also much more powerful: I can use it to check ranges, verify data types, or evaluate complex conditions, making it my go-to choice for complex branching logic."

---

**Would you like to move on to the next topic: Loops & Ranges (`for`, `while`, `..`)?**
S