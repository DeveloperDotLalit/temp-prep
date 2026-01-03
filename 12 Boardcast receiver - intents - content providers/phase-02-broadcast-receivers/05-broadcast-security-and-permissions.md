---
layout: default
title: "Broadcast Security and Permissions"
parent: "Phase 2: Broadcast Receivers - The Systems Megaphone"
nav_order: 5
---

# Broadcast Security and Permissions

## **Topic 5: Security & Permissions in Broadcasts**

### **What It Is**

When you send a broadcast, by default, it’s like shouting in a public park—anyone nearby can listen, and anyone can start shouting back. **Broadcast Security** is the set of "ID checks" and "private rooms" you use to ensure that only the apps you trust can hear your messages or send messages to you.

---

### **Why It Exists**

Without security, your app is vulnerable to two main risks:

1. **Data Leaks (The "Eavesdropping" Problem):** If you broadcast a "Payment Successful" intent with sensitive transaction details, a malicious app sitting in the background could listen to that broadcast and steal the data.
2. **Intent Injection (The "Spoofing" Problem):** If your app has a receiver that triggers a "Clear User Data" action, a malicious app could send a fake broadcast that looks like it came from your system, tricking your app into deleting data.

---

### **How It Works**

There are three main layers of defense:

1. **The `android:exported` Attribute:** This is the "front door" lock. If set to `false`, no app outside your own can send broadcasts to that receiver.
2. **Signature Permissions:** You can define a custom permission in your Manifest. If you set the `protectionLevel` to `signature`, only apps signed with the **same digital key** (your other apps) can communicate.
3. **Package Specification:** When sending a broadcast, you can explicitly set the package name of the intended receiver, making it a "directed" shout rather than a general one.

---

### **Example (Code-based)**

**1. Restricting who can SEND to you (Receiving Security):**
In your `AndroidManifest.xml`, define a permission that only your apps can use.

```xml
<permission android:name="com.lalit.myapp.PERMISSION_ALARM"
    android:protectionLevel="signature" />

<receiver android:name=".MySecureReceiver"
    android:permission="com.lalit.myapp.PERMISSION_ALARM"
    android:exported="true">
    <intent-filter>
        <action android:name="com.lalit.myapp.ACTION_SECURE_EVENT" />
    </intent-filter>
</receiver>

```

**2. Restricting who can HEAR you (Sending Security):**
When you send a broadcast, you can require the receiver to have a specific permission.

```kotlin
val intent = Intent("com.lalit.myapp.ACTION_DATA_UPDATE")
// Only apps with this permission will receive this intent
sendBroadcast(intent, "com.lalit.myapp.PERMISSION_RECEIVE_DATA")

```

**3. The Modern Way (Android 14+):**
During dynamic registration, you **must** specify if the receiver is exported or not.

```kotlin
registerReceiver(
    myReceiver,
    filter,
    Context.RECEIVER_NOT_EXPORTED // Secure by default for internal events
)

```

---

### **Interview Keywords**

- **`android:exported`**: The most basic security toggle in the Manifest.
- **Signature Protection Level**: Ensures only apps from the same developer can talk.
- **Intent Spoofing**: When a malicious app sends a fake broadcast.
- **Eavesdropping**: When a malicious app listens to your private broadcasts.
- **`RECEIVER_NOT_EXPORTED`**: The mandatory flag for local safety in newer Android versions.

---

### **Interview Speak Paragraph**

> "Security is a critical aspect of Broadcasts, especially in high-traffic or financial applications. To prevent 'Intent Injection,' I use the `android:exported="false"` attribute for receivers that are strictly internal. For inter-app communication, I implement **Signature-level permissions**, which ensures that only apps signed with my specific developer key can send or receive these broadcasts. Furthermore, since Android 14, I explicitly define the export status during dynamic registration using the `RECEIVER_NOT_EXPORTED` flag to minimize the attack surface and prevent unauthorized third-party apps from interacting with my app's components."

---

### **Common Interview Question/Angle**

- **"What is the most secure way to communicate between two apps that you own?"**
- _Answer:_ Use a **Custom Permission** with `android:protectionLevel="signature"`. This is the gold standard because the OS enforces the check based on the signing certificate, which a hacker cannot fake.

- **"What happens if you don't set `android:exported` on a receiver with an Intent Filter?"**
- _Answer:_ On newer Android versions (12+), the app will fail to install or crash. On older versions, the system would default it to `true`, which is a security risk. You should always be explicit.

---

**This completes Phase 2: Broadcast Receivers! 🎙️**

**Are you ready to start Phase 3: Content Providers – The Data Gateway? We'll begin with "The Problem of Data Silos."**

---

[â¬… Back to Phase Overview](../)
