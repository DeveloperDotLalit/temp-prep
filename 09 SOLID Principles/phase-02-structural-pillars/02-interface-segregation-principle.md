---
layout: default
title: "Interface Segregation Principle"
parent: "Phase 2: Structural Pillars (L and I)"
nav_order: 2
---

# Interface Segregation Principle

The **Interface Segregation Principle (ISP)** is all about "keeping it lean." If LSP was about being a good child class, ISP is about being a good "contract maker." In Android, where we deal with many listeners and callbacks, this principle is a lifesaver for keeping code clean.

---

## **5. Interface Segregation Principle (ISP)**

### **What It Is**

The principle states: **"No client should be forced to depend on methods it does not use."**

In simple terms: It is better to have many small, specific interfaces than one giant, "fat" interface. If you create an interface with 10 methods, but a class only needs 1 of them, that class is still forced to implement the other 9 (usually as empty functions). That’s a violation of ISP.

### **Why It Exists**

- **The Problem:** We often create "Manager" interfaces that try to handle everything. For example, a `UserActionListener` that handles clicks, long presses, swipes, and double-taps.
- **The Consequence:** If a developer only wants to handle a "Click," they still have to override `onSwipe`, `onLongPress`, etc., leaving them as empty `{ }` blocks. This clutters the code and makes it confusing for others to read (they won't know if the empty method is a mistake or intentional).
- **The Goal:** To create "Modular Contracts." You only sign up for the part of the contract you actually care about.

### **How It Works**

1. **Identify "Fat" Interfaces:** Look for interfaces with many unrelated methods.
2. **Break Them Down:** Split the big interface into smaller ones based on functionality.
3. **Multiple Implementation:** In Kotlin, a class can implement as many small interfaces as it needs. This is much cleaner than implementing one giant one.

---

### **Example (The Android Way)**

#### **❌ The Wrong Way (Violating ISP)**

Imagine a giant listener for a Video Player.

```kotlin
interface VideoPlayerListener {
    fun onPlay()
    fun onPause()
    fun onDownloadStarted()
    fun onDownloadFinished()
}

// This UI class only cares about UI buttons (Play/Pause)
class PlayButtonHandler : VideoPlayerListener {
    override fun onPlay() { /* Logic */ }
    override fun onPause() { /* Logic */ }

    // VIOLATION: Forced to implement methods it doesn't care about
    override fun onDownloadStarted() {}
    override fun onDownloadFinished() {}
}

```

#### **✅ The ISP Way (Refactored)**

We split the responsibilities so clients can pick and choose.

```kotlin
// Small, specific interfaces
interface PlaybackListener {
    fun onPlay()
    fun onPause()
}

interface DownloadListener {
    fun onDownloadStarted()
    fun onDownloadFinished()
}

// Now the UI handler only takes what it needs
class PlayButtonHandler : PlaybackListener {
    override fun onPlay() { /* Logic */ }
    override fun onPause() { /* Logic */ }
}

// A background service might take both
class MediaService : PlaybackListener, DownloadListener {
    override fun onPlay() { ... }
    override fun onPause() { ... }
    override fun onDownloadStarted() { ... }
    override fun onDownloadFinished() { ... }
}

```

---

### **Real-World Android Examples**

- **`View.OnClickListener` vs. `View.OnTouchListener`:** Android doesn't force you to handle a touch event just to get a click. These are segregated.
- **TextWatcher:** Actually, `TextWatcher` in Android is a slight **violation** of ISP! It forces you to implement `beforeTextChanged`, `onTextChanged`, and `afterTextChanged` even if you only need one. Modern libraries often fix this by providing "Core" versions where you only override what you need.

---

### **Interview Keywords**

Fat Interfaces, Lean Contracts, Multiple Inheritance (via Interfaces), Decoupling, Boilerplate Reduction.

### **Interview Speak Paragraph**

> "The Interface Segregation Principle suggests that it's better to have multiple specific interfaces rather than one large, general-purpose one. This prevents 'polluting' classes with unnecessary empty method implementations. In Android, I apply this by splitting complex listeners into smaller ones—for example, separating UI interaction callbacks from background task callbacks. This makes the code more readable and ensures that a class only depends on the specific actions it actually performs."

---

### **Common Interview Question/Angle**

**Q: "If I have many small interfaces, won't that make my code hard to manage?"**
**A:** "It’s a balance. However, the 'cost' of having 5 small interfaces is much lower than the 'cost' of a single giant interface that forces every implementing class to have 10 lines of empty code. Small interfaces promote **reusability**. You can reuse a `DownloadListener` in many parts of the app without dragging in `Playback` logic."

---

**Great! You've finished Phase 2.** You now understand the structural pillars (LSP and ISP) that keep your code safe and lean.

**Ready to move to Phase 3: The Integration Layer (Dependency Inversion Principle)?** This is where everything starts to come together with Hilt, Dagger, and Testing.

---

[â¬… Back to Phase](../) | [Next âž¡](../)
