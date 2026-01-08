---
layout: default
title: Dynamic Navigation
parent: 13. Server Driven UI (SDUI)
nav_order: 3
---

# Dynamic Navigation

Here are your notes for **Topic 11.3**.

---

## **Topic 11.3: Dynamic Navigation**

### **1. What It Is**

Dynamic Navigation is the practice of determining the destination screen at **runtime** based on data (usually from the server), rather than hardcoding it in the `onClick` listener.

- **Static:** `onClick = { navController.navigate("home") }`
- **Dynamic:** `onClick = { actionHandler.handle(serverData.action) }`

### **2. Why It Exists (Context & Flexibility)**

- **Contextual Routing:** Clicking a "Support" button might open a Chat screen for premium users, but an Email Form for free users. The server decides this logic.
- **Promotional Flows:** You can redirect a banner click to a specific "Sale" page that didn't exist when the app was compiled.
- **Universal Deep Linking:** The logic used to route a server click is often the exact same logic used to route an external URL (e.g., from an email).

### **3. How It Works (The Action Contract)**

#### **A. The Schema**

Just like UI components, Actions need a JSON schema.

```json
{
  "type": "button",
  "data": { "label": "View Profile" },
  "action": {
    "type": "navigate",
    "destination": "profile_screen",
    "args": { "user_id": "42" }
  }
}
```

#### **B. The Action Handler**

A central class or function that parses the action type and talks to the `NavController`.

### **4. Example: The Central Router**

**Step 1: Define the Action Model**

```kotlin
@Serializable
sealed class UiAction {
    @Serializable @SerialName("navigate")
    data class Navigate(val destination: String, val id: String? = null) : UiAction()

    @Serializable @SerialName("open_url")
    data class OpenUrl(val url: String) : UiAction()

    @Serializable @SerialName("toast")
    data class ShowToast(val message: String) : UiAction()
}

```

**Step 2: The Handler Logic**

```kotlin
class ActionHandler(
    private val navController: NavController,
    private val context: Context
) {
    fun handle(action: UiAction?) {
        when (action) {
            is UiAction.Navigate -> {
                // Dynamic Route Construction
                val route = if (action.id != null) {
                    "${action.destination}/${action.id}"
                } else {
                    action.destination
                }
                navController.navigate(route)
            }

            is UiAction.OpenUrl -> {
                // Handle external links
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(action.url))
                context.startActivity(intent)
            }

            is UiAction.ShowToast -> {
                Toast.makeText(context, action.message, Toast.LENGTH_SHORT).show()
            }

            null -> { /* Do nothing */ }
        }
    }
}

```

**Step 3: Integration in Renderer**

```kotlin
@Composable
fun SduiButton(node: UiNode, onAction: (UiAction) -> Unit) {
    // Parse the action from the raw JSON map
    val action = parseAction(node.actionData)

    Button(onClick = { onAction(action) }) {
        Text("Click Me")
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Action Schema, Centralized Routing, JSON deserialization, Deep Link Interception, Contextual Navigation, `Uri` parsing.

**Interview Speak Paragraph**

> "To handle navigation in a Server-Driven UI, I abstract the concept of a 'click' into a data model called `UiAction`. Instead of hardcoding navigation routes inside Composables, my UI components simply callback with an Action object parsed from the server JSON. A centralized `ActionHandler` then interprets this object—whether it's an internal navigation command, an external URL, or a system event like a Toast—and executes the appropriate logic using the `NavController` or Android Context. This decouples the UI from the navigation logic, allowing the server to dynamically redirect users to different flows without an app update."

---

**This concludes the Server-Driven UI section.**
You now have a grasp of the architecture used by major apps like Airbnb, Spotify, and Uber to control their UI remotely.

**Final Options:**

1. **Download PDF:** I can format _all_ 11 parts into a structured document.
2. **Mock Interview:** I can simulate a Tech Lead interviewing you on these topics.
3. **Code Challenge:** I can give you a "Take Home Assignment" prompt to build a mini-app using these skills.

---

## Navigation

â† Previous
