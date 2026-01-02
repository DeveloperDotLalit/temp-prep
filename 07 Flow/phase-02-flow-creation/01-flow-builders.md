---
layout: default
title: "Flow Builders"
parent: "Phase 2: Basic Operations and Flow Creation"
nav_order: 1
---

# Flow Builders

We are now moving into **Phase 2: Basic Operations & Flow Creation**. Now that you know _why_ we use Flows, it’s time to learn how to actually build one.

In Kotlin, we have three primary "factories" (Builders) used to create a Flow. Think of these as different ways to start a water pump.

---

### **What It Is**

**Flow Builders** are functions used to create a new Flow. Depending on whether you have a fixed list of items, an existing collection, or a complex block of logic, you choose the builder that fits best.

1. **`flow { ... }`**: The most flexible and common builder. You manually "emit" values.
2. **`flowOf(...)`**: Used when you have a fixed set of values (like hardcoded strings).
3. **`.asFlow()`**: An extension function that converts existing things (like Lists or Ranges) into a Flow.

### **Why It Exists**

In a real app, data comes in different shapes:

- **Case A:** You need to run a loop, fetch from a database, and send updates. (`flow { }`)
- **Case B:** You just want to test a UI and need 3 dummy items. (`flowOf`)
- **Case C:** You already have a `List` of users and want to process them asynchronously. (`asFlow`)

Builders provide a standardized way to turn any data source into a reactive stream.

### **How It Works**

- **`flow { }`**: Inside this block, you use the `emit()` function to push a value into the stream. You can also use `delay()` or call other `suspend` functions here.
- **`flowOf(1, 2, 3)`**: It takes the arguments you provide and emits them one by one automatically, then closes the stream.
- **`list.asFlow()`**: It iterates through the collection and emits each element individually.

**Comparison Chart: Which Builder to Use?**

| Builder         | Best Used For...                        | Flexibility                              |
| --------------- | --------------------------------------- | ---------------------------------------- |
| **`flow { }`**  | Complex logic, API calls, DB queries.   | **High** (Can use `emit`, `delay`, etc.) |
| **`flowOf()`**  | Static/Hardcoded data or Testing.       | **Low** (Just emits provided values)     |
| **`.asFlow()`** | Converting existing Collections/Ranges. | **Medium** (Quick conversion)            |

### **Example – Code-based**

```kotlin
// 1. The Powerhouse: flow { }
// Use this for "real" work.
val logicFlow = flow {
    emit("Starting...")
    val user = repository.fetchUser() // Can call suspend functions!
    emit("User fetched: ${user.name}")
    delay(1000)
    emit("Process Complete")
}

// 2. The Quick Fix: flowOf()
// Great for simple sets of data.
val staticFlow = flowOf("Apple", "Banana", "Cherry")

// 3. The Converter: .asFlow()
// Turn an existing list into a stream.
val listFlow = listOf(1, 2, 3, 4, 5).asFlow()

```

### **Interview Keywords**

Emission, `emit()`, Flow Builder, Suspending Block, Extension Function, `flowOf`, `asFlow`.

### **Interview Speak Paragraph**

> "Kotlin provides three main builders to create Flows. The most powerful is the `flow { }` builder, which allows us to define a custom stream and use the `emit` function to send values asynchronously; it's perfect for complex tasks like network requests. For simpler use cases, we can use `flowOf` to create a stream from a fixed set of values, or the `.asFlow()` extension function to instantly convert existing collections or ranges into a Flow. All of these builders produce 'Cold Flows,' meaning the code inside them won't execute until a collector is attached."

---

### **Interview Focus: Trade-offs & Common Questions**

- **Question:** "Can you call a `suspend` function inside `flowOf`?"
- **Answer:** No. `flowOf` just takes static values. If you need to perform a suspending operation (like a network call) to get your data, you **must** use the `flow { }` builder because it provides a suspending block.

**Next Step:** Now that we’ve built the stream, we need to know how to start it. Shall we move to **Terminal Operators (`.collect()`, `.first()`, `.toList()`)**?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
