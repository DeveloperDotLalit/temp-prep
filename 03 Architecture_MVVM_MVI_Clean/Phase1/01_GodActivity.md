---
layout: default
title: Godactivity
parent: Architecture (MVVM/MVI/Clean): Phase1
nav_order: 1
grand_parent: Architecture (MVVM/MVI/Clean)
---

Here are your focused notes on **God Activities & Tight Coupling**.

---

### **Topic: God Activities & Tight Coupling**

#### **What It Is**

A **"God Activity"** (or God Object) is a class that tries to be a "one-man army." Imagine a single `MainActivity.kt` file that does absolutely everything: it handles the UI (buttons, text), validates user logic (checking passwords), makes network calls (API), and saves data to the database.

**Tight Coupling** is the result of this. It means the different parts of your code (UI, Data, Logic) are glued together like a tangled ball of headphones. You cannot move or change one part without dragging the others with it.

#### **Why It Exists (The Problem)**

This usually happens because it is the fastest way to write code when you are learning. You just put everything in `onCreate` or inside a button's `onClick`.

However, in a professional environment, this is dangerous because:

1. **Fragility:** If you change a small logic rule (e.g., how the database sorts a list), you might accidentally break the UI because the code is mixed together.
2. **Untestable:** You cannot test your business logic (like "is this email valid?") without running the entire Android app on a device/emulator. You can't isolate the logic.
3. **Unreadable:** The file grows to 1,000+ lines. Debugging becomes a nightmare because you can't find where the UI ends and the logic begins.

#### **How It Works (The Mechanics of Failure)**

Here is the flow of a "God Activity" disaster:

1. You need a "Login" feature.
2. You write the code to find the Views (`findViewById`) in `MainActivity`.
3. Inside the button's `setOnClickListener`, you write an `if/else` statement to check if the password is 8 characters (Logic).
4. Inside that same `if` block, you write an `OkHttp` request to send the password to a server (Data).
5. Inside the network callback, you try to update the `TextView` (UI).
6. **The Crash:** If the user rotates the screen while the network call is happening, the Activity is destroyed, but the network call tries to update a `TextView` that no longer exists -> **App Crash**.

#### **Example (The "Spaghetti" Code)**

This is what **Tight Coupling** looks like. The UI knows too much about the Network.

```kotlin
// BAD CODE: A God Activity
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val loginButton = findViewById<Button>(R.id.btnLogin)
        val statusText = findViewById<TextView>(R.id.tvStatus)

        loginButton.setOnClickListener {
            // 1. UI Code mixed with Logic
            val email = findViewById<EditText>(R.id.etEmail).text.toString()

            if (email.contains("@")) { // Logic embedded in UI

                // 2. Logic mixed with Networking
                Thread {
                    // Direct network call inside View -> TIGHT COUPLING
                    val success = performNetworkLogin(email)

                    runOnUiThread {
                        // 3. Updating UI based on raw data
                        if (success) statusText.text = "Success"
                    }
                }.start()
            }
        }
    }

    fun performNetworkLogin(email: String): Boolean {
        // Fake network logic
        return true
    }
}

```

#### **Interview Keywords**

God Object, Monolithic Class, Tight Coupling, Low Cohesion, Spaghetti Code, Scalability, Maintenance Nightmare, Untestable Code.

#### **Interview Speak Paragraph**

> "I strictly avoid 'God Activities' where all the code sits in one file. This creates tight coupling, meaning the UI logic and data logic are tangled together. This makes the app fragile—changing one thing often breaks another—and makes unit testing impossible because I can't test the logic without running the UI. Instead, I separate concerns so the Activity only handles the screen, while other classes handle the logic."

---

**Would you like me to create the next note on "Separation of Concerns (SoC)"?**
