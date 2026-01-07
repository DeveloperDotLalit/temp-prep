---
layout: default
title: Gesture-Driven Animations
parent: 9. Animations
nav_order: 4
---

# Gesture-Driven Animations

Here are your notes for **Topic 9.4**.

---

## **Topic 9.4: Gesture-Driven Animations**

### **1. What It Is**

Gesture-Driven Animations are animations where the **user's finger** controls the timeline.
Instead of an animation playing automatically from 0ms to 500ms, the animation progresses based on how many pixels the user drags.

- **Release:** When the user lets go, the animation usually "snaps" to the nearest valid point (using a decay or spring animation).

### **2. Why It Exists (Tactile Feel)**

- **Direct Manipulation:** It feels like you are physically moving an object, not just triggering a command.
- **Context:** Used for "Swipe to Delete", "Pull to Refresh", "Bottom Sheet Dragging", or "Parallax Scrolling".

### **3. The Toolset**

#### **A. `draggable` (Raw Movement)**

- **Use Case:** Custom sliders, cropping tools, or 1D games.
- **Behavior:** Gives you the raw delta (pixels moved). You update your state manually.
- **Code:** `Modifier.draggable(state = rememberDraggableState { delta -> offset += delta })`

#### **B. `AnchoredDraggable` (Snapping)**

- **Use Case:** Switch toggles, Bottom Sheets, Swipe-to-Dismiss.
- **Behavior:** You define specific "Anchors" (e.g., x=0 is "Closed", x=500 is "Open"). The modifier automatically calculates which anchor is closest and snaps to it when you release.
- _Note: This replaces the older `swipeable` API._

#### **C. Parallax (Scroll-Driven)**

- **Use Case:** Header images moving slower than the list content.
- **Logic:** You read the scroll offset from a `LazyListState` or `ScrollState` and apply a fraction of it to a `graphicsLayer` translation.

### **4. Example: Parallax Header**

Here, the header image moves at **half speed** compared to the text list, creating depth.

```kotlin
@Composable
fun ParallaxScreen() {
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState) // Drive state via scroll
    ) {
        // 1. THE HEADER (Moves slowly)
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
                .graphicsLayer {
                    // MAGIC: Move the image down by 50% of the scroll distance
                    // If we scroll 100px up, image moves 50px up.
                    translationY = 0.5f * scrollState.value
                }
                .background(Color.Blue)
        ) {
            Text("Parallax Header", Color.White, Modifier.align(Alignment.Center))
        }

        // 2. THE CONTENT (Moves normally)
        // We add a white background so it covers the header as it slides up
        Column(modifier = Modifier.background(Color.White).height(800.dp)) {
            Text("Scroll me!", modifier = Modifier.padding(16.dp))
        }
    }
}

```

### **5. Example: Anchored Draggable (Swipe Switch)**

_Note: `AnchoredDraggable` is complex. This is the conceptual simplified setup._

```kotlin
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun SwipeableSwitch() {
    val density = LocalDensity.current

    // 1. Define Anchors (Pixels)
    val anchors = DraggableAnchors {
        DragValue.Start at 0f
        DragValue.End at 200f // 200px width
    }

    // 2. State Controller
    val state = remember {
        AnchoredDraggableState(
            initialValue = DragValue.Start,
            anchors = anchors,
            positionalThreshold = { distance: Float -> distance * 0.5f },
            velocityThreshold = { with(density) { 100.dp.toPx() } },
            animationSpec = tween()
        )
    }

    // 3. UI
    Box(
        modifier = Modifier
            .width(300.dp)
            .background(Color.Gray)
            .anchoredDraggable(state, Orientation.Horizontal) // Connect Gesture
    ) {
        Box(
            modifier = Modifier
                .offset { IntOffset(x = state.requireOffset().roundToInt(), y = 0) } // Apply Position
                .size(50.dp)
                .background(Color.Red)
        )
    }
}

enum class DragValue { Start, End }

```

### **6. Interview Prep**

**Interview Keywords**
`draggable`, `AnchoredDraggable` (vs deprecated `swipeable`), `DraggableState`, Anchors, Decay Animation, Parallax, `translationY`, `ScrollState`.

**Interview Speak Paragraph**

> "For gesture-driven animations, I choose the tool based on the requirement. If I need the UI to snap to specific states—like a swipe-to-unlock button or a bottom sheet—I use the `AnchoredDraggable` API. It handles the physics of finding the nearest anchor and snapping automatically upon release. For continuous effects like Parallax, I don't use a gesture modifier directly; instead, I observe the `ScrollState` or `LazyListState` and apply a calculated fraction of the scroll offset to the `translationY` property of a `graphicsLayer`. This creates a smooth depth effect without intercepting touch events manually."

---

**Next Step:**
We have covered all the major UI and Logic topics.
Now, we must ensure the app works correctly and interoperates with legacy code.
**Are you ready to start Topic 10: Testing & Interoperability?**

---

## Navigation

â† Previous
Next â†’
