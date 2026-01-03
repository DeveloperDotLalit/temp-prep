---
layout: default
title: "Started Services vs Bound Services"
parent: "Phase 1: Foundation - Services and Background Concepts"
nav_order: 3
---

# Started Services vs Bound Services

---

Here are your expert notes for **Phase 1, Topic 3**.

---

### **Topic: Started Services vs. Bound Services**

#### **What It Is**

We know what a Service is. But Android Services come in two distinct "flavors" depending on how they communicate with the rest of your app.

1. **Started Service (Fire-and-Forget):**

- You tell the service to start, and it runs indefinitely in the background until it finishes its job or is explicitly stopped.
- The component that started it (e.g., an Activity) does **not** care about the result and does not keep a connection open.
- _Analogy:_ **Turning on a Ceiling Fan.** You flip the switch (start) and walk away. The fan keeps running even if you leave the room. You don't need to stand there holding the switch.

2. **Bound Service (Client-Server):**

- It acts like a server inside your app. Components (Activities/Fragments) bind to it as "clients."
- You can send requests, get results, and communicate back and forth.
- It only runs as long as at least one client is bound to it. If all clients unbind, the service dies.
- _Analogy:_ **Calling Customer Support.** You dial the number (bind). You talk back and forth. The connection only exists while you are on the line. When you hang up (unbind), the service session ends.

#### **Why It Exists**

- **Started Services** exist for tasks that need to complete regardless of what the user does next (e.g., uploading a file. If the user closes the app, the upload should finish).
- **Bound Services** exist for tasks where the UI needs to interact closely with the background process (e.g., a music player where the UI needs to update the progress bar every second and the user needs to pause/play).

#### **How It Works (Comparison Table)**

| Feature           | Started Service                                                    | Bound Service                                               |
| ----------------- | ------------------------------------------------------------------ | ----------------------------------------------------------- |
| **Command**       | `startService(Intent)`                                             | `bindService(Intent, Connection, Flags)`                    |
| **Key Method**    | `onStartCommand()`                                                 | `onBind()`                                                  |
| **Lifespan**      | Runs indefinitely until `stopSelf()` or `stopService()` is called. | Runs only as long as a client is bound to it.               |
| **Communication** | Difficult. Usually uses Broadcasts to talk back to UI.             | Easy. Uses an `IBinder` interface to call methods directly. |
| **Context**       | Independent.                                                       | Dependent on the client.                                    |

#### **The "Hybrid" Service (Important for Interviews)**

A service can be **both** Started and Bound!

- **Example:** A Music Player.
- **Why?**
- It must be **Started** so the music keeps playing even if the user closes the app.
- It must be **Bound** so the Now Playing screen can show the current song time and handle the "Pause" button.

#### **Example Code Structure**

**1. Started Service (The "Download" Pattern):**

```kotlin
// In Activity
val intent = Intent(this, UploadService::class.java)
startService(intent) // Fire and forget

// In Service
override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
    uploadFile()
    // Service keeps running until this is called
    stopSelf()
    return START_NOT_STICKY
}

```

**2. Bound Service (The "Binder" Pattern):**

```kotlin
// In Service
class LocalBinder : Binder() {
    fun getService(): MyService = this@MyService
}
private val binder = LocalBinder()

override fun onBind(intent: Intent): IBinder {
    return binder // Return the "phone line" to the activity
}

// Custom method the Activity can call
fun getRandomNumber(): Int {
    return Random.nextInt()
}

```

```kotlin
// In Activity
val connection = object : ServiceConnection {
    override fun onServiceConnected(className: ComponentName, service: IBinder) {
        val binder = service as LocalBinder
        val myService = binder.getService()

        // Direct communication!
        val num = myService.getRandomNumber()
    }
}
// Connect
bindService(intent, connection, Context.BIND_AUTO_CREATE)

```

#### **Interview Keywords**

startService, bindService, IBinder, ServiceConnection, IPC (Inter-Process Communication), LocalBinder, Fire-and-Forget, Client-Server.

#### **Interview Speak Paragraph**

"The main difference lies in communication and lifecycle. A **Started Service** is designed for 'fire-and-forget' tasks; it's triggered by `startService()`, processes work in `onStartCommand()`, and runs indefinitely until explicitly stopped, even if the component that started it is destroyed. A **Bound Service**, on the other hand, follows a client-server model. It's initialized using `bindService()`, providing an `IBinder` interface that allows components to interact directly with the service. Unlike a started service, a bound service only stays alive as long as there is at least one client bound to it. In complex apps like Music Players, we often use a hybrid approach—starting the service to keep it alive in the background while also binding to it to update the UI."

---

**Would you like to move to the next topic: "Foreground Services"?**

---

[â¬… Back to Phase Overview](../)
