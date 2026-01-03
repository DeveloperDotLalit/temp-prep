---
layout: default
title: "Tricky Scenario Questions"
parent: "Phase 7: Final Interview Drill"
nav_order: 2
---

# Tricky Scenario Questions

---

Here are your expert notes for **Phase 7, Topic 2**.

---

### **Topic: Tricky Scenario Questions ("What happens if I force stop the app?")**

#### **The Question**

**Interviewer:** "I schedule a OneTimeWorkRequest to upload a file. Then, I go to Settings -> Apps -> My App -> **Force Stop**. Does the task still run?"

**The Short Answer:** **NO.**
**The Nuanced Answer:** No, but... it depends on what happens _next_.

#### **Why It Exists (The Security Model)**

Android treats a "Force Stop" as a **User Command** to completely kill the app.

- When a user Force Stops an app, the OS puts the app into a "stopped state."
- **All** alarms, jobs, and broadcast receivers are cancelled.
- The app will **never** wake up again until the **User manually opens the app** (launches an Activity).
- This prevents malware from restarting itself after you killed it.

#### **How It Works (The Recovery)**

1. **Scenario A: Force Stop -> Nothing Happens.**

- If the user force stops the app and never touches it again, the WorkManager task will **never** run. It sits in the database forever.

2. **Scenario B: Force Stop -> User Re-opens App.**

- If the user taps the app icon the next day:
- The app process starts.
- WorkManager initializes.
- It checks the database: _"Hey, I have a pending task from yesterday!"_
- It **reschedules** the task to run (respecting constraints).

3. **Scenario C: Swipe Away from Recents (NOT Force Stop).**

- **Interviewer:** "What if I just swipe the app away from the recent apps list?"
- **Answer:** **YES, it will run.**
- Swiping away kills the UI process, but the WorkManager task (managed by `JobScheduler` in the system process) remains active or will be restarted by the system shortly.

#### **Other Tricky Scenarios**

**Q2: "I set a PeriodicWorkRequest for every 15 minutes. Can I make it run exactly at 10:00 AM, 10:15 AM, 10:30 AM?"**

- **Answer:** **No.** WorkManager is **inexact**.
- Android uses "Doze Mode" windows. It might group your 10:15 task with another app's task and run them both at 10:18 to save battery.
- _Solution:_ If you need EXACT time, use `AlarmManager`.

**Q3: "What happens if I update the app? Do pending tasks disappear?"**

- **Answer:** **No.**
- The database persists across app updates.
- **Caveat:** If you _changed_ the Worker class name or package, WorkManager might fail to find the class. (Always keep worker classes stable or provide a mapping).

#### **Interview Keywords**

Force Stop, Stopped State, User Interaction, Reschedule, Inexact Timing, Doze Windows, Persistence, Swipe vs. Kill.

#### **Interview Speak Paragraph**

"If a user manually **Force Stops** the app from Settings, the Android system cancels all pending intents, alarms, and background jobs, including WorkManager tasks. The app enters a 'stopped state' and will not receive any system broadcasts or run any jobs until the user explicitly re-launches the app. However, the task is not lost; it remains persisted in the WorkManager database. Once the user opens the app again, WorkManager initializes, detects the pending task, and re-queues it. This is different from simply swiping the app away from the Recents screen, which does not put the app in a stopped state and allows WorkManager tasks to continue running or restart shortly."

---

**Would you like to move to the next topic: "Code-Based Questions" (Identifying bugs in a snippet)?**

---

[â¬… Back to Phase Overview](../)
