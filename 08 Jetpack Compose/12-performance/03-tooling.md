---
layout: default
title: Tooling
parent: 12. Performance & Internals
nav_order: 3
---

# Tooling

Here are your notes for **Topic 2.8**.

---

## **Topic 2.8: Tooling (Compiler Metrics & Inspector)**

### **1. What It Is**

These are the diagnostic tools provided by Google to verify if your Compose code is actually performant.

- **Layout Inspector:** Visualizes the UI tree in real-time.
- **Compiler Metrics:** A text report generated at build time that tells you exactly which functions are "Skippable" and which are "Restartable."
- **GPU Overdraw:** A developer setting on your phone to see if you are painting the same pixel 5 times in one frame.

### **2. Why It Exists (Invisible Bugs)**

Performance issues in Compose are often invisible.

- A Composable might look fine but is recomposing 100 times per second unnecessarily.
- A class might look stable but is treated as unstable by the compiler.
- **Compiler Metrics** reveal the hidden truth about your Stability.

### **3. How It Works**

#### **A. Compose Compiler Metrics**

You enable this in your `gradle.properties`.

```properties
kotlinOptions {
    freeCompilerArgs += [
        "-P",
        "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=" + project.buildDir.absolutePath + "/compose_metrics"
    ]
}

```

After building, you get a JSON/TXT file.

- **Look for:** `unstable`. If a function is marked `restartable` but NOT `skippable`, it means every time the parent redraws, this function redraws too. This is bad for performance.

#### **B. Layout Inspector**

In Android Studio: **Tools -> Layout Inspector**.

- Shows the **Recomposition Count** (How many times a composable ran).
- Shows the **Skip Count** (How many times it successfully did nothing).
- **Goal:** High Skip Count, Low Recomposition Count.

#### **C. GPU Overdraw**

On your Phone: **Developer Options -> Debug GPU Overdraw -> Show Overdraw Areas**.

- **Blue:** Drawn once (Good).
- **Green:** Drawn twice (Okay).
- **Red:** Drawn 4+ times (Bad - you have too many stacked backgrounds).

### **4. Example: Reading a Metric Report**

**Output File:** `composables.txt`

```text
restartable skippable fun UserRow(
  stable user: User
)

```

- **Result:** GOOD! It is "skippable".

```text
restartable fun UserList(
  unstable users: List<User>
)

```

- **Result:** BAD! It is NOT skippable because `users` is unstable.
- **Fix:** Use `@Immutable` wrapper or `ImmutableList`.

### **5. Interview Prep**

**Interview Keywords**
Compiler Metrics, `skippable`, `restartable`, Layout Inspector, Recomposition Counts, GPU Overdraw, Stability Inference.

**Interview Speak Paragraph**

> "I proactively monitor performance using Compose Compiler Metrics. I enable the reports in Gradle to audit my composables, specifically looking for functions that are 'restartable' but not 'skippable,' which indicates stability issues. I also use the Layout Inspector in Android Studio to observe real-time recomposition and skip counts during user interactions. This two-pronged approach allows me to catch stability regressions at build time and verify runtime performance on actual devices."

---

**Congratulations!** You have completed **Part 2: State Management & Performance**.
You now understand how Compose _thinks_.

Now, let's build something complex.
**Are you ready to start Part 3: Lists, Grids & UI Enhancements?**

---

## Navigation

â† Previous
Next â†’
