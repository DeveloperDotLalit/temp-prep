---
layout: default
title: "Android IPC: Intents, Broadcast Receivers, and Content Providers"
nav_order: 13
has_children: true
---

# Android IPC Components

An interview-focused guide to **how Android components communicate internally and across apps**,  
covering **Intents, Broadcast Receivers, and Content Providers** with real-world architectural reasoning.

Hello! I'm excited to be your learning partner for this. Since you're an SDE-II working on high-traffic apps, we’ll skip the fluff and focus on the architectural "why" and "how" that interviewers look for at your level, while keeping the language simple and conversational.

Here is your comprehensive, phase-wise roadmap for mastering **Intents, Broadcast Receivers, and Content Providers**.

---

## 🗺️ The Learning Roadmap

### **Phase 1: Intents – The Glue of Android**

_Focus: Understanding how different components talk to each other._

- **What is an Intent?**: Understanding the "Intent" as a messaging object used to request an action.
- **Explicit vs. Implicit Intents**: Knowing when to call a specific class versus asking the system to find an app that can do the job.
- **Intent Filters**: How apps "advertise" their capabilities to the Android System.
- **Data Passing (Bundles & Parcelable)**: The mechanism of moving data between components and why we don't just use global variables.
- **PendingIntents**: A deep dive into "giving permission" to another app (like Notification Manager) to execute code on your behalf.

### **Phase 2: Broadcast Receivers – The System’s Megaphone**

_Focus: How your app listens to system-wide events or app-specific signals._

- **Introduction to Broadcasting**: Why we need a "publish-subscribe" model in mobile OS.
- **Static vs. Dynamic Registration**: Understanding Manifest-declared vs. Context-declared receivers (and why Google is moving away from Static).
- **Standard vs. Ordered Broadcasts**: Learning how to prioritize who hears a message first and how to "abort" a broadcast.
- **LocalBroadcastManager vs. Flow/Bus**: Why `LocalBroadcastManager` is deprecated and what modern Kotlin-first alternatives you should mention in interviews.
- **Security & Permissions**: How to ensure only specific apps can send or receive your broadcasts.

### **Phase 3: Content Providers – The Data Gateway**

_Focus: Managing access to a central repository of data, often across different apps._

- **The Problem of Data Silos**: Why we don't just let Apps read each other's databases directly.
- **The Content URI Structure**: Deconstructing the "address" used to find specific data (Authority, Path, ID).
- **ContentResolver & Cursor**: How the "client-side" of your app queries the provider.
- **Working with System Providers**: Real-world examples like accessing Contacts, MediaStore, or Calendar.
- **Security & FileProvider**: Safely sharing files (like images) with other apps without exposing your entire file system.

### **Phase 4: Advanced Architectures & Interview Scenarios**

_Focus: High-level design decisions and "What if" questions._

- **Inter-Process Communication (IPC)**: How these three components form the backbone of Android's IPC.
- **Deep Linking & App Links**: Using Intents to drive users from a URL directly into a specific screen.
- **Battery & Performance Impact**: Why the system limits Broadcasts and how to handle background restrictions in modern Android (Oreo+).
- **Security Best Practices**: Preventing Intent Redirection attacks and securing Content Providers.

### **Phase 5: The Interview Final Polish**

_Focus: Direct Q&A and Mock Drill._

- **Top 20 Technical Questions**: Curated list of questions from companies like Honeywell, RiseBird, and big tech.
- **Scenario-based Problem Solving**: "How would you design a system where App A needs to notify App B when a file is downloaded?"
- **Edge Case Handling**: What happens if an Intent is sent but no app can handle it? What if a Broadcast Receiver takes too long on the main thread?

---

**Would you like to modify any part of this roadmap, or shall we dive straight into Phase 1: Intents?**
