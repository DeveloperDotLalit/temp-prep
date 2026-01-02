---
layout: default
title: "Managing Global State"
parent: "Phase 5: Real World Interview Scenarios"
nav_order: 2
---

# Managing Global State

### **Interview Scenario: Managing Global State (User Sessions)**

In a real-world Android app, a "User Session" (the logged-in user's ID, token, and profile info) is the most critical piece of global state. It needs to be accessible from the Profile screen, the Checkout screen, and the Settings screen.

The interviewer wants to see how you prevent **data inconsistency** (one screen thinking the user is logged out while another shows their name) and how you ensure **security**.

---

### **1. The Strategy: Combining Patterns for State**

To manage a global session, we combine three specific patterns:

- **Singleton:** To create a single "UserSessionManager" that holds the data in memory.
- **Observer (StateFlow/LiveData):** To notify all screens the moment the user logs in or out.
- **Proxy (or Decorator):** To intercept network calls and automatically add the "Session Token" to the headers.

---

### **2. Why This Combination Exists**

- **The Problem:** If you store the user's name in an `Intent` and pass it from screen to screen, what happens if the user updates their name on the 5th screen? The 1st screen still has the old name. This is called **State Fragmentation**.
- **The Solution:** You create a **Single Source of Truth**. Every screen "subscribes" to the session manager. When the state changes, every screen updates instantly.

---

### **3. How It Works (Step-by-Step Architecture)**

1. **The Central Store (Singleton + Observer):** A manager class that lives as long as the app does. It holds a `StateFlow` representing the `UserSession`.
2. **The Reactive UI:** Screens observe this flow. If the session becomes `null`, the app automatically navigates to the Login screen.
3. **The Automatic Injector (Proxy/Interceptor):** An OkHttp Interceptor acts as a proxy. For every outgoing request, it checks the Session Manager, grabs the token, and attaches it to the request.

---

### **4. Example (The "Clean Session" Architecture)**

```kotlin
// The data model for our state
data class UserSession(val token: String, val userName: String)

// --- 1. SINGLETON + OBSERVER ---
object SessionManager {
    // A private stream that only this class can change
    private val _session = MutableStateFlow<UserSession?>(null)

    // A public stream that others can only watch
    val session: StateFlow<UserSession?> = _session

    fun login(user: UserSession) {
        _session.value = user
    }

    fun logout() {
        _session.value = null
    }

    fun isLoggedIn() = _session.value != null
}

// --- 2. THE PROXY (OkHttp Interceptor) ---
class AuthInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val requestBuilder = chain.request().newBuilder()

        // Automatically inject the token into every call
        SessionManager.session.value?.let {
            requestBuilder.addHeader("Authorization", "Bearer ${it.token}")
        }

        return chain.proceed(requestBuilder.build())
    }
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
      [ User Logs In ]
             |
             v
   [ SessionManager (Singleton) ] <--- Updates State to "Logged In"
             |
    /--------+--------\
    |                 |
[ View A ]       [ View B ]       [ Network Interceptor (Proxy) ]
(Shows Name)     (Shows Profile)  (Attaches Token to API calls)
    ^                 ^                 ^
    |                 |                 |
    \--- (Observes via StateFlow) ------/

```

---

### **6. Interview Keywords**

- **Single Source of Truth:** One place where the data lives.
- **Unidirectional Data Flow:** State changes in the manager and flows down to the UI.
- **Reactivity:** The UI "reacts" to state changes without being manually told.
- **Interceptor:** A pattern used to modify requests/responses globally.
- **In-Memory Cache:** Keeping the session in RAM for fast access while the app is open.

---

### **7. Interview Speak Paragraph**

> "To manage global user sessions, I implement a **Single Source of Truth** using the **Singleton** and **Observer** patterns. I create a `SessionManager` that holds the current user state in a reactive stream like `StateFlow`. This allows all UI components to observe the session status and update themselves automatically if a user logs out or updates their profile. To handle security, I use an **Interceptor**, which acts as a **Proxy** for our network layer, automatically injecting the session token into every outgoing API request. This architecture ensures data consistency across all screens and keeps the individual ViewModels clean of session-handling logic."

---

### **Common Interview "Follow-up" Questions**

**1. "What happens if the app is killed by the OS? Does the Singleton stay?"**

- **Answer:** "No, the memory is cleared. To handle this, I combine the Singleton with a **Persistence Layer** (like EncryptedSharedPreferences or DataStore). On app launch, the `SessionManager` initializes by reading the saved token from disk."

**2. "How do you handle a '401 Unauthorized' error globally?"**

- **Answer:** "I use the **Observer** pattern. If an Interceptor detects a 401 error, it calls `SessionManager.logout()`. Since all my Activities are observing the session flow, they will all see the state change to `null` and trigger a navigation to the Login screen simultaneously."

---

**Would you like to try the "Image Loading Library" scenario next, or are you ready for the final Phase 6: Interview Q&A?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
