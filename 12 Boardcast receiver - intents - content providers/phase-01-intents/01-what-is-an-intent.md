---
layout: default
title: "What is an Intent"
parent: "Phase 1: Intents - The Glue of Android"
nav_order: 1
---

# What is an Intent

## **Topic 1: What is an Intent?**

### **What It Is**

In simple terms, an **Intent** is a "message" or a "request" that you send to the Android System. Think of it as a **digital courier**. You give the courier a package (data) and a destination (where to go), and the Android System ensures it gets delivered to the right component—whether that’s an Activity, a Service, or a Broadcast Receiver.

### **Why It Exists**

In traditional programming, if you want to move from Class A to Class B, you just create an instance of Class B. But in Android, components (like Activities) are managed by the **Android OS**, not by your code directly.

**The Problem:** You can't just call `ActivityB().start()`. The system needs to manage the lifecycle, memory, and security of that new screen.
**The Solution:** Intents. They act as a formal request to the OS saying, _"Hey Android, I intend to do 'X'. Please help me start the component that can handle 'X'."_ This keeps apps decoupled and allows the OS to stay in control.

---

### **How It Works**

Imagine you are at a restaurant (Your App).

1. **Creating the Intent:** You (the Activity) write down an order (the Intent object). This order contains:

- **Who:** The specific person you want to talk to (Explicit).
- **What:** Or just the "action" you want done, like "I want a pizza" (Implicit).
- **Extra Info:** Specific instructions, like "no onions" (Extras/Data).

2. **Sending the Intent:** You hand the order to the Waiter (the Android System) using methods like `startActivity(intent)`.
3. **Delivery:** The Android System looks at the order, finds the right chef (another Activity or App), and delivers the message.

---

### **Example (Code-based)**

Let's look at the most common way we use an Intent in Kotlin to move from one screen to another.

```kotlin
// 1. Create the Intent
// 'this' is the current context (the sender)
// 'SecondActivity::class.java' is the destination (the receiver)
val intent = Intent(this, SecondActivity::class.java)

// 2. Add some data (optional)
intent.putExtra("USER_NAME", "Lalit")

// 3. Tell the system to execute the intent
startActivity(intent)

```

---

### **Interview Keywords**

- **Messaging Object**: The technical definition of an Intent.
- **Asynchronous**: Intents don't always happen "instantly" in a blocking way; the system schedules the transition.
- **Inter-component Communication (ICC)**: The formal term for how Android parts talk to each other.
- **Decoupling**: Using Intents means Activity A doesn't need to know the inner workings of Activity B.

---

### **Interview Speak Paragraph**

> "An Intent is a messaging object used to request an action from another app component. It serves as the primary glue for Inter-component Communication in Android. Instead of directly instantiating classes, we use Intents to tell the Android System what we want to do—like starting an activity, starting a service, or delivering a broadcast. This allows the OS to handle the lifecycle and security of the components while keeping our code modular and decoupled."

---

### **Common Interview Question/Angle**

- **"Can you start a component of another app using an Intent?"**
- _Answer:_ Yes! That is the power of **Implicit Intents**. For example, you can send an Intent with the action `ACTION_VIEW` and a URL, and the system will find a Browser app to handle it. You don't need to know which browser the user has; the Intent handles the "handshake."

**Would you like to move on to the next subtopic: Explicit vs. Implicit Intents?**

---

[â¬… Back to Phase Overview](../)
