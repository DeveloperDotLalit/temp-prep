---
layout: default
title: "Top Technical Interview Questions"
parent: "Phase 5: Interview Final Polish"
nav_order: 1
---

# Top Technical Interview Questions

We have reached the final stage! As an SDE-II, interviewers at companies like **Honeywell** or **RiseBird** won't just ask "What is an Intent?" They will focus on **architectural decisions, security, and performance**.

Here is a curated list of the top 20 interview questions, categorized by topic, with the "Senior-level" answers you need.

---

## **Part 1: Intents & Deep Linking**

### **1. How do you pass a large amount of data (e.g., a 2MB Bitmap) between two activities?**

**Answer:** You **never** pass large data through an Intent because of the `TransactionTooLargeException` (limit is ~1MB). Instead:

- Save the data to a local file or database.
- Pass only the **File URI** or **Database ID** through the Intent.
- The second Activity then fetches the data from the source.

### **2. What is the difference between `FLAG_ACTIVITY_NEW_TASK` and `FLAG_ACTIVITY_CLEAR_TOP`?**

**Answer:** `NEW_TASK` starts the activity in a new task stack (like opening a separate "window"). `CLEAR_TOP` checks if the activity is already running; if it is, it closes all activities on top of it and brings it to the front instead of creating a new instance.

### **3. Explain the security risks of "Intent Redirection."**

**Answer:** It occurs when an app receives an Intent from an untrusted source and uses it to launch another internal component. A hacker can use your app as a proxy to open private, non-exported activities. Prevention: Validate the destination or use `PendingIntent` with `FLAG_IMMUTABLE`.

### **4. How does the system resolve an Implicit Intent?**

**Answer:** It performs **Intent Resolution**. The OS matches the Intent's Action, Data (MIME type/URI), and Category against the **Intent Filters** of all installed apps. If multiple matches exist, it shows the App Chooser.

### **5. Why are App Links better than Deep Links?**

**Answer:** Deep Links are unverified and show an "App Chooser." **App Links** use a `Digital Asset Links` JSON file on your website to verify ownership, making them more secure and providing a seamless "zero-click" transition into your app.

---

## **Part 2: Broadcast Receivers**

### **6. Why was `LocalBroadcastManager` deprecated?**

**Answer:** It uses the Intent system, which is heavy and lacks type-safety. Modern alternatives like **SharedFlow** or **StateFlow** are lifecycle-aware, more efficient, and fit better into Clean Architecture.

### **7. What are "Implicit Broadcast Restrictions" in Android Oreo+?**

**Answer:** To save battery, Google stopped allowing apps to register for most system broadcasts (like `WIFI_STATE_CHANGED`) in the Manifest. You must now register them **dynamically** in code while the app is running.

### **8. How do you ensure a Broadcast Receiver doesn't cause an ANR?**

**Answer:** The `onReceive()` method runs on the **Main Thread**. I must keep logic under 10 seconds (ideally much less). For heavy work, I use **WorkManager** or a **JobService** to offload the task.

### **9. What is an "Ordered Broadcast"? Give a real-world use case.**

**Answer:** It's a broadcast delivered to one receiver at a time based on priority. **Use Case:** An SMS app. A security app with high priority can intercept an SMS, check for a "Remote Wipe" command, and call `abortBroadcast()` so the default messaging app never sees it.

### **10. How do you prevent other apps from "spoofing" a broadcast to your app?**

**Answer:** 1. Set `android:exported="false"` in the Manifest. 2. Use a **Signature-level Permission** so only your own apps can send the signal. 3. Use the `RECEIVER_NOT_EXPORTED` flag during dynamic registration.

---

## **Part 3: Content Providers**

### **11. When should you actually build a Content Provider?**

**Answer:** Only when you need to share data **across different app processes**. If you only need data inside your own app, use a **Room Database** or a **Repository**—it's faster and less complex.

### **12. What is a `ContentResolver`?**

**Answer:** It is the "Client-side" interface. You never talk to a Provider directly; the `ContentResolver` acts as a central hub that routes your query to the correct Provider based on the URI Authority.

### **13. How do you handle multi-threading with Content Providers?**

**Answer:** Content Providers are **thread-safe** by default. However, multiple calls to `query()` or `insert()` can come from different threads. I must ensure the underlying database (like SQLite) handles concurrent access properly.

### **14. What is the role of `UriMatcher`?**

**Answer:** It’s a helper class inside the Provider used to parse incoming URIs. It differentiates between a request for a whole table (e.g., `/products`) and a request for a single row (e.g., `/products/5`).

### **15. Explain `ContentObserver`.**

**Answer:** It’s a listener that detects changes in a Provider. When a Provider updates data, it calls `notifyChange()`. The observer then triggers a UI refresh or a background sync in the client app.

---

## **Part 4: Security & Advanced IPC**

### **16. Why is `FileProvider` necessary in Android 7.0+?**

**Answer:** Sharing `file://` URIs is banned. `FileProvider` creates a secure `content://` URI and uses `FLAG_GRANT_READ_URI_PERMISSION` to give another app temporary access to a file without exposing the app's internal folder structure.

### **17. What is "Marshalling" in the context of Android IPC?**

**Answer:** Since processes can't share memory, **Marshalling** is the process of flattening a complex object (like a `User` class) into a byte-stream (via `Parcelable`) that the **Binder** driver can transport across process boundaries.

### **18. How do you protect a public Content Provider from SQL Injection?**

**Answer:** Never concatenate strings in queries. Always use **Selection Arguments** (`?` placeholders).

- _Bad:_ `"name = '" + input + "'"`
- _Good:_ `"name = ?"`, `arrayOf(input)`

### **19. What is the "Thundering Herd" problem?**

**Answer:** It occurs when a single system broadcast (like `BOOT_COMPLETED`) causes dozens of apps to wake up at the same time, causing a CPU/RAM spike. Google solved this by restricting static broadcasts.

### **20. How would you design a system to share "Live Stock Prices" between two apps?**

**Answer:** \* **App A (Provider):** Uses a **Content Provider**.

- **App B (Listener):** Uses a **ContentObserver** to get real-time updates without polling.
- **Security:** Use **Signature Permissions** so only authorized apps see the data.

---

### **Interview Keywords**

`Binder IPC`, `TransactionTooLargeException`, `Implicit Broadcast Restrictions`, `FileProvider`, `Signature Permissions`, `ContentObserver`, `UriMatcher`, `Digital Asset Links`.

---

### **Interview Speak Paragraph**

> "In high-traffic environments like Bajaj Finserv, I focus on the **security and efficiency** of Inter-Process Communication. I prefer **App Links** for seamless navigation and **WorkManager** for background tasks to avoid battery drain caused by static broadcasts. For data sharing, I leverage **FileProvider** to avoid exposing raw file paths and always secure my **Content Providers** using signature-level permissions. By understanding the underlying **Binder mechanism**, I ensure that data passing via Parcelables remains within memory limits and doesn't impact the app's performance during context switching."

---

**Congratulations! We have covered the entire roadmap.** 🎓

**Would you like me to conduct a "Mock Interview" where I give you a scenario and you explain how you would solve it using these components?**

---

[â¬… Back to Phase Overview](../)
