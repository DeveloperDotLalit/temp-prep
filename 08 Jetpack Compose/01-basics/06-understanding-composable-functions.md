---
layout: default
title: Understanding @Composable functions
parent: 1. Introduction + Basic Composables
nav_order: 6
---

# Understanding @Composable functions

Here are your notes for **Topic 1.6**.

---

## **Topic 1.6: Understanding @Composable functions**

### **1. What It Is**

A `@Composable` function is a standard Kotlin function that has been marked with a special annotation: `@Composable`.
This annotation changes the function's nature. instead of "returning" a value (like an `Int` or `String`), it "emits" UI into the hierarchical tree that Compose manages. It is the fundamental building block of any Compose app.

### **2. Why It Exists (The "Magic" Link)**

Standard functions in programming are "one-and-done." You call them, they calculate, they return.
UI is different. UI needs to **persist** on the screen, and it needs to **update** when data changes.

- **Problem:** A normal Kotlin function doesn't know how to track state or update itself later.
- **Solution:** The `@Composable` annotation tells the Kotlin compiler to inject extra code into your function. This injected code allows the runtime to "listen" to the data used inside the function and re-run (recompose) the function automatically whenever that data changes.

### **3. How It Works (The Compiler Magic)**

**A. Transformation**
When you compile your code, the Compose Compiler Plugin changes the function signature.

- _You write:_ `fun Greeting(name: String)`
- _Compiler sees:_ `fun Greeting(name: String, $composer: Composer, $changed: Int)`
  It adds a `$composer` parameter that connects your code to the Compose runtime.

**B. Idempotency (Crucial Concept)**
A Composable function must be **Idempotent**. This means:

- If you call it with the same inputs, it must produce the same UI output.
- It should not depend on global variables or random numbers directly.
- **Why?** Compose might run your function 100 times a second (during animations) or skip it entirely. If the result depends on "luck" or external variables, your UI will flicker or bug out.

**C. Side-Effect Free**
You should **never** change app state directly inside the body of a Composable.

- _Bad:_ `Database.saveUser()` simply sitting inside the function.
- _Why:_ Since the function can re-run at any time, you might accidentally save the user 50 times in one second. (We use special "Effect Handlers" for this, covered in Topic 5).

### **4. Example: The Rules**

**The Correct Way**
A pure function of data.

```kotlin
@Composable
fun Greeting(name: String) {
    // Input: name. Output: Text UI.
    // No hidden logic.
    Text(text = "Hello $name")
}

```

**The Wrong Way (Breaking the Rules)**

```kotlin
// Global variable (BAD)
var clickCount = 0

@Composable
fun BadButton() {
    // SIDE EFFECT! Modifying an external variable.
    // Every time this redraws, count increases unpredictably.
    clickCount++

    Button(onClick = {}) { Text("Count: $clickCount") }
}

```

### **5. Interview Prep**

**Interview Keywords**
Annotation Processing, Compiler Plugin, Idempotency, Side-effect free, Emission, Recomposition, Gap Buffer (Advanced).

**Interview Speak Paragraph**

> "The `@Composable` annotation is effectively a marker for the Compose Compiler Plugin. It transforms a standard Kotlin function by injecting a `Composer` parameter, which allows the runtime to track the function and its data dependencies. A key requirement for these functions is **idempotency**—given the same inputs, they must always produce the same UI output. They must also be free of side effects in their main body because the framework reserves the right to re-execute them (recompose) multiple times or in parallel to optimize performance."

---

**Next Step:**
Now that we understand the function syntax, let's put it to use. Ready for **Topic 1.7: Basic UI Components**? We will look at Text, Buttons, and Images.

---

## Navigation

â† Previous
Next â†’
