---
layout: default
title: Versioning & Compatibility
parent: 13. Server Driven UI (SDUI)
nav_order: 2
---

# Versioning & Compatibility

Here are your notes for **Topic 11.2**.

---

## **Topic 11.2: Versioning & Compatibility**

### **1. What It Is**

In Server-Driven UI (SDUI), the server changes faster than the client.

- **The Scenario:** The server team adds a new component called `"video_player"` and deploys it.
- **The Problem:** User A hasn't updated their app in 6 months. Their app looks at the registry, searches for `"video_player"`, finds nothing, and crashes (or shows nothing).
- **The Goal:** Build a system that gracefully handles "Unknown Components" so old apps don't break when new features launch.

### **2. Why It Exists (The "Update Gap")**

Unlike the Web (where everyone sees the new code instantly), Mobile apps have fragmentation.
You will always have users on version 1.0, 1.1, and 2.0 simultaneously hitting the same API.
You cannot force everyone to update just because you added a new button style.

### **3. Strategies for Compatibility**

#### **A. The "Graceful Fallback" (The Empty Box)**

If the recursive renderer encounters an unknown type, it should catch the error and render:

1. **Nothing (Empty Box):** Safest. The user just sees a gap.
2. **Placeholder:** "Update app to view content."
3. **Generic Container:** If the unknown component is a wrapper (like `"fancy_row"`), try to just render its _children_ so the content isn't lost, even if the fancy styling is missing.

#### **B. Schema Versioning**

The API response includes a version number: `{"version": 2, "layout": ...}`.

- The App checks: `if (response.version > app.supportedVersion) { showUpdateDialog() }`.
- _Pros:_ Simple.
- _Cons:_ Aggressive. Stops users from using the app just for minor UI changes.

#### **C. Strict Typings (Enums vs Strings)**

- **Bad:** Using `enum class UiType` in Kotlin. If the JSON sends a string not in the Enum, GSON/Moshi crashes immediately during parsing.
- **Good:** Parse the type as a `String`. Then use a `when (type)` block. The `else` branch handles the unknown smoothly.

### **4. Example: The Safe Renderer**

This renderer handles the "Unknown Component" problem by logging a warning and skipping it, rather than crashing.

```kotlin
@Composable
fun SafeSduiRenderer(node: UiNode) {
    // 1. Dynamic Lookup
    val component = ComponentRegistry.get(node.type)

    if (component != null) {
        // 2. Success: Render the known component
        component.Compose(node)
    } else {
        // 3. Fallback Strategy
        // Option A: Render nothing (invisible to user)
        // Option B: Show a debug placeholder (for developers)
        if (BuildConfig.DEBUG) {
            Box(
                modifier = Modifier
                    .background(Color.Red.copy(alpha = 0.3f))
                    .border(1.dp, Color.Red)
                    .padding(4.dp)
            ) {
                Text("Unknown: ${node.type}", fontSize = 10.sp)
            }
        }

        // Option C: Critical - Log this to Crashlytics/Analytics
        // "User on v1.2 encountered unknown type 'video_player'"
        LaunchedEffect(Unit) {
            Analytics.logEvent("sdui_unknown_type", mapOf("type" to node.type))
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Backward Compatibility, Fallback Strategy, Graceful Degradation, Loose Coupling, Parsing Safety (String vs Enum), Analytics Logging.

**Interview Speak Paragraph**

> "In Server-Driven UI, handling versioning is critical because mobile clients fragment. I never use strict Enums for component types in the data layer, as a new type from the server would cause a parsing crash on older clients. Instead, I parse types as Strings. In the UI Registry, I implement a 'Default Fallback' strategy. If the registry lookup returns null for a component type (e.g., 'new_video_player'), the app simply skips rendering that node or renders an empty `Box` instead of crashing. This ensures that users on older app versions can still use the core functionality, even if they miss out on the newest UI features."

---

**This concludes the Core Notes.**
You now have a complete, interview-ready roadmap for Modern Android Development with Jetpack Compose.

**Would you like me to:**

1. **Generate a PDF** of all these notes combined?
2. **Quiz you** on a specific topic (e.g., "Grill me on Side Effects")?
3. **Start a Coding Challenge** based on one of these topics?

---

## Navigation

â† Previous
Next â†’
