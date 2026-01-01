---
layout: default
title: Refactor Java Code to Kotlin
parent: Advanced Kotlin: Phase 7   Interview Scenarios
nav_order: 1
grand_parent: Advanced Kotlin
---

﻿---
layout: default
title: "Refactor Java Code to Kotlin"
parent: "Real-World Interview Scenarios"
nav_order: 1
---

# Refactor Java Code to Kotlin

<!-- Content starts here -->

Here are your interview-focused notes for **Phase 7: Real-World Interview Scenarios**, starting with the most common practical test: **Refactoring Java to Kotlin**.

---

### **Scenario: "Refactor this Java code to Kotlin"**

#### **The Goal**

The interviewer gives you a snippet of "Java-style" code (verbose, clunky).
Your job is **not** to just translate it syntax-wise. Your job is to make it **Idiomatic** (The "Kotlin Way").
They are checking if you know features like `data class`, `when`, `apply`, and string templates.

#### **The Checklist (Mental Cheat Sheet)**

1. **POJOs (Getters/Setters)** **Data Class**.
2. **`switch` or chained `if-else**`  **`when`\*\*.
3. **Object Setup (x.setA(); x.setB();)** **`apply { }`**.
4. **String Concatenation** **String Templates (`$`)**.
5. **Static Utility Methods** **Extension Functions**.

---

#### **The Challenge (Java Code)**

_Imagine the interviewer hands you this:_

```java
public class UserUtils {

    // 1. A verbose POJO
    public static class User {
        private String name;
        private int roleId;

        public User(String name, int roleId) {
            this.name = name;
            this.roleId = roleId;
        }

        // ... imagine 20 lines of Getters, Setters, toString(), equals() ...
        public int getRoleId() { return roleId; }
        public String getName() { return name; }
    }

    public void configureUser(User user) {
        // 2. Chained If-Else
        String roleName;
        if (user.getRoleId() == 1) {
            roleName = "Admin";
        } else if (user.getRoleId() == 2) {
            roleName = "Editor";
        } else {
            roleName = "Guest";
        }

        // 3. String Concatenation
        System.out.println("User: " + user.getName() + " is a " + roleName);
    }

    // 4. Object Configuration (Builder style)
    public void setupUI() {
        Button btn = new Button();
        btn.setText("Submit");
        btn.setColor("Blue");
        btn.setVisible(true);
    }
}

```

---

#### **The Solution (The "Kotlin Way")**

**Step 1: The Data Class**
Kill the boilerplate. No getters, setters, or `toString`.

```kotlin
data class User(val name: String, val roleId: Int)

```

**Step 2: The Logic (`when` & `apply`)**
Refactor the logic to be declarative and concise.

```kotlin
// 1. Extension Function (Instead of a static Utils class)
fun User.printRole() {

    // 2. WHEN expression (Replaces if-else)
    // We assign the result directly to the variable
    val roleName = when (roleId) {
        1 -> "Admin"
        2 -> "Editor"
        else -> "Guest"
    }

    // 3. String Template (Replaces concatenation)
    println("User: $name is a $roleName")
}

fun setupUI() {
    // 4. APPLY Scope Function (Replaces repetitive btn.set...)
    val btn = Button().apply {
        text = "Submit"
        color = "Blue"
        isVisible = true
    }
}

```

---

#### **Why This Wins Interviews**

1. **Readability:** You reduced ~40 lines of Java to ~10 lines of Kotlin.
2. **Safety:** `data class` ensures `equals()` works correctly.
3. **Scoping:** Using `apply` keeps the button configuration grouped together, making it clear that those lines belong to `btn`.
4. **Expressiveness:** `when` is easier to read and maintain than multiple `if-else` blocks.

#### **Interview Speak Paragraph**

"When refactoring this code, I first converted the `User` class into a **Data Class** to automatically generate `equals`, `hashCode`, and `toString` without boilerplate. I replaced the imperative `if-else` block with a **`when` expression**, which is more readable and returns a value directly. Instead of modifying the Button properties line-by-line, I used the **`apply` scope function** to group the initialization logic, making the code cleaner. Finally, I replaced string concatenation with **String Templates** for better readability."

---

**Would you like to move on to the next scenario: "Scenario: Debug this crash" (Finding hidden NPEs)?**
