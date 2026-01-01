---
layout: default
title: Trick Questions
parent: Phase 6   The Interview Gauntlet Qa
nav_order: 2
---

Here are your detailed notes for the second topic of Phase 6.

These questions are designed to trip you up. They test if you are just memorizing definitions or if you actually understand the lifecycle flow.

---

### **Topic: Trick Questions (The "Gotchas")**

#### **Trick Question 1: "Does a ViewModel survive if the user hits the Back button?"**

- **The Trap:** You might be so focused on "ViewModels survive destruction" that you instinctively say "Yes."
- **The Correct Answer:** **NO.**
- **The Explanation:**
  The ViewModel survives **Configuration Changes** (Rotation), but it does **not** survive **Finishing**.
  When the user presses the Back button:

1. The Activity calls `finish()`.
2. The System checks `isFinishing()` and sees it returns `true`.
3. The System calls `getViewModelStore().clear()`.
4. The ViewModel's `onCleared()` is triggered.
5. The ViewModel is destroyed and garbage collected.

If the ViewModel survived the Back button, your app would run out of memory because every screen you ever visited would still be alive in RAM!

#### **Trick Question 2: "If I rotate the screen 10 times, how many ViewModels are created?"**

- **The Trap:** Thinking it creates 10 or 11 instances because the Activity is created 11 times.
- **The Correct Answer:** **Only ONE.**
- **The Explanation:**
  That is the entire point of the ViewModel.
- Rotation 1: Provider checks Store -> Returns Instance A.
- Rotation 5: Provider checks Store -> Returns Instance A.
- Rotation 10: Provider checks Store -> Returns Instance A.
  It is the exact same object in memory the whole time.

#### **Trick Question 3: "Can I perform a Fragment Transaction (replace) and keep the ViewModel?"**

- **The Trap:** Confusing Fragment Scope with Activity Scope.
- **The Correct Answer:** **It depends on the Scope.**
- **If scoped to the Fragment (`this`):** NO. If the Fragment is replaced (destroyed), its private ViewModel dies.
- **If scoped to the Activity (`requireActivity()`):** YES. The Activity stays alive, so the shared ViewModel stays alive.

#### **Trick Question 4: "Why shouldn't I just use a Singleton instead of a ViewModel?"**

- **The Trap:** "Singletons live forever, so they solve the rotation problem too!"
- **The Correct Answer:** **Memory Management.**
- A **Singleton** lives for the _entire life of the app process_. If you put "Checkout Data" in a Singleton, it stays in memory even when the user is on the "Login" screen. This is a memory leak.
- A **ViewModel** lives only as long as the _screen_ needs it. When the user finishes the screen, the ViewModel cleans itself up. It is a "Scoped Singleton," which is much healthier for memory.

#### **Visualizing the Logic Check:**

```text
[ Activity onDestroy() called ]
          |
          v
[ System Check: activity.isFinishing()? ]
          |
  +-------+-------+
  | YES           | NO (It's just rotating)
  v               v
[ KILL VM ]     [ KEEP VM ]
(Call clear())  (Save to NonConfigInstance)

```

#### **Interview Speak Paragraph**

> "It's important to distinguish between a configuration change and the user finishing an activity. If the user presses the Back button, the Activity is permanently destroyed. The system detects this via the `isFinishing()` check, and consequently, the `ViewModelStore` is cleared, triggering `onCleared()` and destroying the ViewModel. The ViewModel is designed to hold data only relevant to the current task; if it survived the Back button, we would leak memory for every screen the user has closed. So, simply put: it survives rotation, but it dies on 'Back'."

---

**Next Step:**
We are almost at the finish line. Let's tackle the "High Level" architecture question.
Shall we move to **Architecture Questions**: "Why MVVM over MVP?" and the ViewModel's role in Clean Architecture?
