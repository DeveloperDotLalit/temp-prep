---
layout: default
title: "Introduction to Concurrency"
parent: "Phase 1: The Foundations"
nav_order: 1
---

Starting with **Phase 1**, let’s break down why we even need things like Coroutines by looking at the "Old Way" of doing things: **Traditional Threading**.

---

## **Introduction to Concurrency**

### **What It Is**

Concurrency is the ability of a program to handle multiple tasks at the same time. Think of it like a chef in a kitchen: they don't just wait for the water to boil before cutting vegetables; they start chopping _while_ the water is heating up. In coding, concurrency allows your app to download a file in the background while the user continues to scroll through a list.

### **Why It Exists**

In the early days of computing, apps did one thing at a time (Sequential Execution). If you clicked "Download," the entire app would freeze until the download finished.

- **The Problem:** Modern users expect "smoothness." We need multitasking to keep the UI responsive while performing "heavy" tasks like API calls, database indexing, or image processing.
- **The Solution:** Historically, we used **Threads**. A Thread is like a "worker" that the Operating System (OS) provides to run code.

### **How It Works (The Traditional Way)**

When you want to do something in the background without Coroutines, you manually create a new `Thread`. The OS manages these threads, giving each one a tiny slice of time on the CPU.

**The "Heavy Cost" of Threads:**

1. **Memory Hog:** Each thread is "expensive." On many systems, a single thread can take up about **1MB of RAM** just for its stack. If you try to start 10,000 threads, your app will likely crash with an `OutOfMemoryError`.
2. **Context Switching:** This is the "mental tax" the CPU pays. When the CPU stops working on Thread A to work on Thread B, it has to save everything about Thread A and load everything for Thread B. Doing this thousands of times per second slows down the whole system.
3. **Blocking:** Traditional threads are "blocking." If a thread is waiting for a slow server response, that worker is essentially "stuck" and cannot do anything else. It just sits there, holding onto its 1MB of memory, doing nothing.

### **Example (The "Waiter" Analogy)**

- **Sequential (No Concurrency):** A waiter takes an order, walks to the kitchen, and stands there staring at the chef until the food is ready. Only then does he bring it to the table and move to the next customer. (Very inefficient!)
- **Traditional Threading:** Every time a new customer walks in, the restaurant hires a _brand new waiter_. If 1,000 customers walk in, you have 1,000 waiters standing in the kitchen. The kitchen gets crowded (Memory limit), and the manager spends all day just telling waiters whose turn it is (Context switching).
- **Coroutines (The Goal):** One waiter takes an order, gives it to the kitchen, and immediately goes to serve another table. When the food is ready, he comes back to finish the first task. **This is "Non-blocking" concurrency.**

### **Interview Keywords**

Concurrency, Multi-threading, Blocking vs. Non-blocking, Context Switching, Stack Memory, Thread Overhead.

### **Interview Speak Paragraph**

> "In traditional programming, we achieved multitasking using Threads, but they come with a high cost. Each thread is a heavy-weight object managed by the OS, consuming roughly 1MB of memory and requiring expensive 'context switching' to move between tasks. If we create too many threads, we risk an OutOfMemoryError. This is why we need a more efficient way to handle concurrency—where we can pause a task without 'blocking' the underlying thread, which is exactly what Kotlin Coroutines allow us to do."

---

**Would you like to move on to the next topic in Phase 1: The "Suspending" Secret?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
