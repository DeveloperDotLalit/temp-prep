---
layout: default
title: "Argument Capturing (Slots)"
parent: "Phase 3: Intermediate Unit Testing (Mockk & Architecture)"
nav_order: 4
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 3.3**.

This is an advanced technique used when "Stubbing" isn't enough. You use this when data disappears into a dependency (like saving to a database or sending analytics) and you need to pull it back out to check it.

---

# **Chapter 3: Intermediate Unit Testing (Mockk & Architecture)**

## **Topic 3.3: Argument Capturing (Slots)**

### **1. The Problem Scenario**

Imagine you are testing a `SignUpViewModel`. When the user clicks "Sign Up", the ViewModel creates a `User` object internally and passes it to `AnalyticsRepository.trackUser(user)`.

- **The Issue:** The `trackUser` function returns `Unit` (void). It doesn't give anything back.
- **The Question:** How do you verify that the `User` object created _inside_ the ViewModel has the correct ID and Timestamp? You can't see it; it was passed into the void of the Mock.

### **2. The Solution: The Capturing Slot**

A **Slot** is a special variable provided by Mockk that acts like a "bucket." You tell Mockk: _"When this function is called, take the argument that was passed and drop it into this bucket so I can look at it later."_

### **3. The Syntax (3 Steps)**

#### **Step 1: Create the Slot**

Define a slot for the specific type of object you want to catch.

```kotlin
val userSlot = slot<User>()

```

#### **Step 2: Capture the Argument**

In your `every` or `verify` block, use the `capture()` function instead of `any()`.

```kotlin
// Tell the mock: "When trackUser is called, CAPTURE the argument into userSlot"
every { analyticsRepo.trackUser(capture(userSlot)) } returns Unit

```

#### **Step 3: Assert the Captured Data**

After the action is performed, access the `captured` property of the slot.

```kotlin
// Inspect the object that was caught
val capturedUser = userSlot.captured

assertThat(capturedUser.name).isEqualTo("Gemini")
assertThat(capturedUser.timestamp).isGreaterThan(1000L)

```

### **4. Real-World Code Example**

**The Code (ViewModel):**

```kotlin
class SignUpViewModel(private val database: DatabaseService) {
    fun signUp(name: String, age: Int) {
        // The ViewModel creates the object internally
        val newUser = User(id = UUID.randomUUID().toString(), name = name, age = age)

        // It saves it to the DB (Fire and Forget)
        database.save(newUser)
    }
}

```

**The Test (Using Slots):**

```kotlin
@Test
fun `signUp - saves correct user details to database`() {
    // 1. ARRANGE
    val mockDb = mockk<DatabaseService>(relaxed = true) // Relaxed so we don't need 'every'
    val userSlot = slot<User>() // The Bucket

    val viewModel = SignUpViewModel(mockDb)

    // 2. ACT
    viewModel.signUp("Alice", 25)

    // 3. ASSERT (Verification + Capture)
    // We verify the call happened AND capture the data at the same time
    verify { mockDb.save(capture(userSlot)) }

    // Now we inspect the evidence
    val savedUser = userSlot.captured

    assertThat(savedUser.name).isEqualTo("Alice")
    assertThat(savedUser.age).isEqualTo(25)
    // We can even check that the ID is not null, even though it was random!
    assertThat(savedUser.id).isNotEmpty()
}

```

### **5. Capturing Multiple Arguments (The List)**

A `slot` only remembers the **most recent** value captured. If `database.save()` is called 5 times, `userSlot.captured` will only hold the 5th user.

If you need to check _all_ of them, use a `MutableList`:

```kotlin
val allUsers = mutableListOf<User>()

every { mockDb.save(capture(allUsers)) } returns Unit

// After execution, allUsers will contain [User1, User2, User3...]
assertThat(allUsers).hasSize(3)

```

### **6. Why not just use `verify { match { ... } }`?**

Mockk allows you to do inline assertions:

```kotlin
verify { mockDb.save(match { it.name == "Alice" }) }

```

**Why use Slots instead?**

- **Debuggability:** If `match` fails, it just says "Verification failed." If a Slot assertion fails, Google Truth tells you _"Expected name Alice but was Bob"_.
- **Complexity:** If you need to check 10 different properties of the object, writing a massive lambda inside `match { ... }` is messy. Capturing the object and asserting on it line-by-line is cleaner.

### **7. Summary for Interviews**

> "I use `Slots` in Mockk when I need to perform 'Black Box' verification of data passed to a dependency. This is common in 'Fire and Forget' operations like logging analytics or database insertions where the method returns void. By capturing the argument into a Slot, I can run detailed assertions on the object's properties (like checking if a timestamp was generated correctly) using Google Truth, rather than relying on complex argument matchers."

---

**Would you like to proceed to Topic 3.4: "Testing ViewModels" (Integrating Repositories, LiveData, and Coroutines)?**
