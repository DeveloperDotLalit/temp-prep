---
layout: default
title: "Assertions (Google Truth)"
parent: "Phase 2: The Basics (JUnit & Assertions)"
nav_order: 4
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 2.4**.

This topic marks the transition from "writing tests that run" to "writing tests that are readable and debuggable."

---

# **Chapter 2: The Basics (JUnit & Assertions)**

## **Topic 2.4: Assertions (Google Truth)**

### **1. What is an Assertion?**

The "Assertion" is the **Assert** phase of the **AAA** pattern. It is the moment of truth.

- It compares the **Actual Result** (what your code produced) with the **Expected Result** (what you wanted it to produce).
- If they match, the test passes silently.
- If they differ, the test fails and throws an `AssertionError`.

### **2. The Old Way: Standard JUnit Assertions**

For years, developers used the default assertions built into JUnit (`org.junit.Assert`).

- **Syntax:** `assertEquals(expected, actual)`
- **The Problem (The "Yoda" Confusion):**
- When writing `assertEquals(4, result)`, you often forget which argument comes first. Is it `(expected, actual)` or `(actual, expected)`?
- If you mix them up, the error message reads: _"Expected: 5, but was: 4"_ when it was actually the reverse. This causes confusion during debugging.

- **The Problem (Vague Errors):**
- If you compare two lists and they differ by one item, `assertEquals` just says "Lists are not equal." It doesn't tell you _what_ is missing.

### **3. The Elite Way: Google Truth**

**Google Truth** is a "fluent" assertion library maintained by the Guava team. It is the industry standard for Android development today.

- **Philosophy:** Tests should read like English sentences.
- **Syntax:** `assertThat(actual).verb(expected)`
- **Dependency:** `testImplementation "com.google.truth:truth:1.1.x"`

### **4. Syntax Comparison (Cheat Sheet)**

| Scenario           | Legacy (JUnit 4)                    | Google Truth (The Elite Way)        |
| ------------------ | ----------------------------------- | ----------------------------------- |
| **Equality**       | `assertEquals(10, result)`          | `assertThat(result).isEqualTo(10)`  |
| **Boolean**        | `assertTrue(isValid)`               | `assertThat(isValid).isTrue()`      |
| **Null Check**     | `assertNotNull(user)`               | `assertThat(user).isNotNull()`      |
| **List Size**      | `assertEquals(3, list.size())`      | `assertThat(list).hasSize(3)`       |
| **List Content**   | `assertTrue(list.contains("A"))`    | `assertThat(list).contains("A")`    |
| **String Content** | `assertTrue(str.startsWith("Err"))` | `assertThat(str).startsWith("Err")` |

### **5. The "Killer Feature": Failure Messages**

The main ROI of using Truth is not writing the test, but **fixing** the test when it fails. Truth provides detailed, context-aware error messages.

**Scenario:** Checking a list of User IDs.

- **Code:** `assertThat(userIds).containsExactly("101", "102", "103")`
- **Actual List:** `["101", "105", "103"]`

**Legacy Error Message:**

> "AssertionFailedError: expected list to contain [101, 102, 103]"

**Google Truth Error Message:**

> "Not true that <[101, 105, 103]> contains exactly <[101, 102, 103]>. It is missing <[102]> and has unexpected items <[105]>"

_Elite Insight:_ You fix the bug instantly because the error told you exactly what was wrong.

### **6. Assertion Chaining**

Because Truth is fluent, you can chain multiple checks on the same object without rewriting the `assertThat` line.

```kotlin
val username = " super_admin "

assertThat(username)
    .trim()            // Transforms the string (strips whitespace)
    .isNotEmpty()      // Check 1
    .hasLength(11)     // Check 2
    .startsWith("super") // Check 3

```

If any link in the chain fails, the test fails.

### **7. Testing Exceptions**

Testing that code _crashes_ correctly is just as important as testing it succeeds.

- **Scenario:** Ensuring your validator throws an exception for empty input.

```kotlin
// The Cleanest Way (using JUnit 4 + AssertThrows)
val exception = assertThrows(IllegalArgumentException::class.java) {
    validator.validate("") // This line should crash
}

// Now use Truth to check the exception message
assertThat(exception).hasMessageThat().isEqualTo("Input cannot be empty")

```

### **8. Summary for Interviews**

> "I prefer Google Truth over standard JUnit assertions because it improves the 'Mean Time to Repair' for broken tests. Truth uses a fluent API that reads like natural language (`assertThat(x).isEqualTo(y)`), which eliminates the confusion of parameter order. More importantly, its failure messages are rich and descriptive, telling me exactly what item was missing from a list or how a string differed, rather than just saying 'false'."

---

**You have now mastered the Theory and the Tools.**

It is time to write code.
**Would you like to proceed to Topic 2.5: "Writing Your First Test" (A practical walk-through of a Calculator/Validator test)?**
