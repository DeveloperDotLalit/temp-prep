---
layout: default
title: Concept & Architecture
parent: 13. Server Driven UI (SDUI)
nav_order: 1
---

# Concept & Architecture

Here are your notes for **Topic 11.1**.

---

# Part 11: Server-Driven UI (SDUI) [Bonus Advanced Topic]

## **Topic 11.1: Concept & Architecture**

### **1. What It Is**

Server-Driven UI (SDUI) is an architectural pattern where the **Server** decides _what_ to render, and the **App** only knows _how_ to render components.
Instead of hardcoding "Profile Screen has an Image and two Buttons," the app asks the server "What should I show?" and the server responds with a JSON tree describing the layout.

### **2. Why It Exists (The "App Store" Bypass)**

- **Instant Updates:** You can change the order of the dashboard, add a new banner, or hide a broken feature instantly without waiting for a 2-day App Store review.
- **A/B Testing:** You can show Layout A to User Group 1 and Layout B to User Group 2 just by sending different JSON, measuring which one performs better.
- **Cross-Platform Consistency:** The same JSON drives iOS, Android, and Web, ensuring they look identical.

### **3. How It Works (The 3 Pillars)**

1. **The Schema (Contract):** A defined set of UI primitives that both Backend and Frontend agree on (e.g., `type: "card"`, `type: "text"`, `type: "row"`).
2. **The Registry (Mapper):** A dictionary in your Android app that maps the string `"card"` to the Composable function `@Composable fun Card(...)`.
3. **The Recursive Renderer:** A Composable that takes a generic UI Node, looks it up in the Registry, renders it, and then (if it has children) calls itself for the children.

### **4. Example: Building a Simple Engine**

**Step 1: The JSON Response (The "What")**

```json
{
  "type": "column",
  "children": [
    {
      "type": "text",
      "data": { "content": "Welcome Back!", "style": "h1" }
    },
    {
      "type": "button",
      "data": { "label": "Click Me", "action": "open_settings" }
    }
  ]
}
```

**Step 2: The Data Models**

```kotlin
// A generic node representing any UI element
data class UiNode(
    val type: String,
    val data: Map<String, Any> = emptyMap(),
    val children: List<UiNode> = emptyList()
)

```

**Step 3: The Registry & Renderer (The "How")**

```kotlin
@Composable
fun SduiRenderer(node: UiNode) {
    when (node.type) {
        // Container Elements (Recursive)
        "column" -> {
            Column {
                node.children.forEach { child -> SduiRenderer(child) }
            }
        }
        "row" -> {
            Row {
                node.children.forEach { child -> SduiRenderer(child) }
            }
        }

        // Leaf Elements (Widgets)
        "text" -> {
            val content = node.data["content"] as? String ?: ""
            Text(text = content)
        }
        "button" -> {
            val label = node.data["label"] as? String ?: "Button"
            Button(onClick = { /* Handle Action */ }) {
                Text(label)
            }
        }

        // Fallback for unknown types (Safety)
        else -> {
            Text("Unknown Widget: ${node.type}", color = Color.Red)
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
JSON Schema, Recursive Rendering, Component Registry, Backward Compatibility (Fallback components), Dynamic Layouts, A/B Testing.

**Interview Speak Paragraph**

> "I implement Server-Driven UI to enable flexibility and instant updates without app releases. The architecture relies on a strict contract—usually a JSON schema—that defines UI primitives like 'Rows', 'Cards', and 'Images'. On the client side, I build a **Registry** that maps these JSON types to specific Composable functions. The core engine is a recursive Composable that iterates through the JSON tree, delegating rendering to the appropriate component from the registry. This separation allows the backend to dictate the layout structure and content hierarchy while the mobile app focuses purely on rendering performant native UI."

---

**Next Step:**
We can render buttons, but clicking them does nothing.
Ready for **Topic 11.2: Handling Actions & Navigation**? This covers how to route JSON click events to code.

---

## Navigation

Next â†’
