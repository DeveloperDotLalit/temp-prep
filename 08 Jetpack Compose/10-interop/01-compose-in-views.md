---
layout: default
title: Compose in Views
parent: 10. Interoperability & Migration
nav_order: 1
---

# Compose in Views

Here are your notes for **Topic 10.1**.

---

# Topic 10: Testing & Interoperability

## **Topic 10.1: Compose in Views (Migration Strategy)**

### **1. What It Is**

This is the "Bottom-Up" migration strategy. You have an existing legacy app (Activities, Fragments, XML), and you want to start using Compose for **just one part** of the screen (e.g., a new chart or a button), without rewriting the whole Activity.
You use a special Android View called **`ComposeView`**.

### **2. Why It Exists (The "Strangler" Pattern)**

rewriting a 5-year-old app from scratch is a business suicide mission.

- **The Smart Way:** Keep the old XML layout. Replace _just_ the `RecyclerView` with a Compose `LazyColumn`.
- **The Result:** You migrate piece by piece over months. `ComposeView` acts as the bridge that lets Compose live inside the old world.

### **3. How It Works**

#### **A. Adding it to XML**

You add it like any other view.

```xml
<androidx.compose.ui.platform.ComposeView
    android:id="@+id/compose_view"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />

```

#### **B. Setting Content**

In your Fragment or Activity, you find the view and give it a Composable.

```kotlin
val composeView = view.findViewById<ComposeView>(R.id.compose_view)
composeView.setContent {
    MaterialTheme {
        Text("Hello from Compose inside XML!")
    }
}

```

### **4. Critical: The Disposal Strategy**

**This is the most important part of this topic.**
By default, Compose doesn't know _when_ to die. If you put a `ComposeView` in a `RecyclerView` or a `Fragment`, it might keep running (and listening to State flows) even after the View is destroyed, causing memory leaks.

You **MUST** set the `ViewCompositionStrategy`.

- **`DisposeOnViewTreeLifecycleDestroyed` (Best for Fragments):**
- Disposes the composition when the Fragment's _View_ Lifecycle is destroyed.
- _Why:_ Fragments have two lifecycles (Fragment vs View). If you don't use this, the composition survives when the user navigates away, leaking memory.

- **`DisposeOnDetachedFromWindow` (Best for Custom Views / RecyclerView):**
- Disposes as soon as the view leaves the screen.
- Use this if you are building a custom `MyComposeButton` class extending `AbstractComposeView`.

### **5. Example: Fragment Implementation**

```kotlin
class StatsFragment : Fragment(R.layout.fragment_stats) {

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<ComposeView>(R.id.compose_view).apply {
            // CRITICAL: Bind to the Fragment's View Lifecycle
            setViewCompositionStrategy(
                ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed
            )

            setContent {
                // Now we are in Compose land!
                StatsGraph(data = viewModel.data)
            }
        }
    }
}

```

### **6. Interview Prep**

**Interview Keywords**
`ComposeView`, `AbstractComposeView`, Interoperability, Migration, `ViewCompositionStrategy`, Fragment View Lifecycle, Memory Leaks.

**Interview Speak Paragraph**

> "When migrating an existing app to Compose, I use the 'Bottom-Up' approach using `ComposeView`. This allows me to replace specific UI components, like a generic RecyclerView, with a Compose LazyColumn without rewriting the entire Fragment. The most critical detail here is setting the correct `ViewCompositionStrategy`. For Fragments, I strictly use `DisposeOnViewTreeLifecycleDestroyed` to ensure the Composition is disposed of when the Fragment's view is destroyed, preventing memory leaks. For usages inside custom views or RecyclerView items, I use `DisposeOnDetachedFromWindow`."

---

**Next Step:**
That's how you put **Compose inside XML**. But what if you need to put a **MapView (XML) inside Compose**?
Ready for **Topic 10.2: Views in Compose (AndroidView)**?

---

## Navigation

Next â†’
