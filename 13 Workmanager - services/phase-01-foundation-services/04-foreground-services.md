---
layout: default
title: "Foreground Services"
parent: "Phase 1: Foundation - Services and Background Concepts"
nav_order: 4
---

# Foreground Services

---

Here are your expert notes for **Phase 1, Topic 4**.

---

### **Topic: Foreground Services**

#### **What It Is**

A **Foreground Service** is a special type of Service that performs work the user is actively aware of.
Unlike a regular background service (which is invisible), a Foreground Service **must** display a permanent **Notification** in the status bar. This notification cannot be dismissed by the user unless the service stops.

Think of it as a "VIP Service."

- **Standard Service:** "I'm working in the back room, nobody needs to know." (Low Priority).
- **Foreground Service:** "I am working right here! Look at me!" (High Priority).

Common examples: **Music Players (Spotify notification), Google Maps Navigation, Screen Recorders, Fitness Trackers.**

#### **Why It Exists (The Problem of Killing)**

Android's Operating System is a ruthless killer. To save battery and memory, it constantly hunts down and kills apps running in the background.

- **The Problem:** If you run a regular background service to play music, Android might say, "The user is on Instagram now, they don't need this music app consuming memory," and **kill it** suddenly. The music stops. This is a bad user experience.
- **The Solution:** You promote your service to a **Foreground Service**.
- **The Trade-off:** Android agrees not to kill your service, **BUT** you must show a visible Notification. This warns the user: _"Hey, this app is draining your battery right now."_ It prevents apps from spying or mining crypto in the background without the user knowing.

#### **How It Works (Survival Strategy)**

It works by changing the **Process Priority**.

1. **Priority Levels:** Android ranks apps by importance.

- **Level 1 (Highest):** The App currently on screen (Foreground App).
- **Level 2 (High):** An App running a **Foreground Service** (perceived as "visible" to the user).
- **Level 3 (Low):** An App running a standard Background Service.
- **Level 4 (Lowest):** Cached/Closed apps.

2. **Low Memory Killer (LMK):** When the phone runs out of RAM, the LMK starts killing processes from Level 4 up to Level 1.
3. **Survival:** By calling `startForeground()`, your service jumps from Level 3 to Level 2. It becomes almost immune to being killed, unless the device is under extreme stress.

#### **Example Code Structure**

To create a Foreground Service, you must do two things differently:

1. Request permission in `AndroidManifest.xml`.
2. Call `startForeground()` immediately inside the Service.

**1. Permissions (Manifest):**

```xml
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />

```

**2. The Service Code:**

```kotlin
class MyMusicService : Service() {

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // 1. Create the Notification (The "Badge" of a Foreground Service)
        val notification = NotificationCompat.Builder(this, "CHANNEL_ID")
            .setContentTitle("Playing Music")
            .setContentText("Song: Blinding Lights")
            .setSmallIcon(R.drawable.ic_music)
            .build()

        // 2. PROMOTE to Foreground Service
        // ID must be > 0. This makes the notification stick to the status bar.
        startForeground(1, notification)

        // 3. Do the work
        playMusic()

        return START_STICKY
    }
}

```

**3. Starting it (From Activity):**

```kotlin
val intent = Intent(this, MyMusicService::class.java)
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
    // For Android 8.0+, we must use startForegroundService
    startForegroundService(intent)
} else {
    startService(intent)
}

```

#### **Interview Keywords**

startForeground, Notification Channel, Process Priority, Low Memory Killer (LMK), FOREGROUND_SERVICE_TYPE (Android 14+), Persistent Notification.

#### **Interview Speak Paragraph**

"A Foreground Service is used for tasks that are noticeable to the user and must continue running even if the user interacts with other apps, like audio playback or navigation. Unlike standard background services, which the system can kill to reclaim memory, a Foreground Service runs with a higher process priority, making it essentially immune to the system's Low Memory Killer. To prevent abuse, Android requires these services to display a persistent notification, ensuring the user is always aware that the app is active and consuming resources. From Android 8.0 onwards, we must use `startForegroundService()` to launch it and call `startForeground()` within 5 seconds to avoid a crash."

---

**Would you like to move to the next topic: "The Problem with Background Services" (Why traditional services started failing)?**

---

[â¬… Back to Phase Overview](../)
