---
layout: default
title: Mindmap
parent: 17. Resources & Cheat Sheets
nav_order: 1
---

# Mindmap

Here is a text-based **Mindmap** of the entire syllabus we have covered.
You can use this to visualize the connections between topics.

---

# **Jetpack Compose: The Master Mindmap**

- **1. Foundation & Layouts**
- **Core Mental Model**
- Declarative UI (Describe _what_, not _how_)
- Recomposition (The loop: State changes -> UI redraws)
- Composables (`@Composable` functions)

- **Layouts**
- Standard: `Column`, `Row`, `Box`
- Scaffold: `TopBar`, `FAB`, `Drawer`
- Modifiers: Order matters (Size -> Padding -> Background)

- **2. State Management**
- **The Basics**
- `State<T>` / `MutableState<T>`
- `remember` (Survives recomposition)
- `rememberSaveable` (Survives rotation/death)

- **Patterns**
- State Hoisting (Unidirectional Flow)
- Stateless vs. Stateful Composables

- **Performance**
- Stability: `@Stable` vs `@Immutable`
- Skipping: Avoiding unnecessary redraws
- Pitfalls: Reading state in Composition vs. Draw phase

- **3. Lists & Grids**
- **Lazy Components**
- `LazyColumn` / `LazyRow`
- `LazyVerticalGrid`

- **Optimization**
- `key` (Smart updates)
- `contentType` (Recycling efficiency)

- **Features**
- Sticky Headers
- Pagination (Paging 3 integration)

- **4. Navigation**
- **Setup**
- `NavHost`, `NavController`, `NavGraph`
- Type-Safe Navigation (Serialization)

- **Structure**
- Nested Navigation (Sub-graphs)
- Bottom Bar & Rail Integration
- Deep Links (External URLs)

- **5. Side-Effects & Lifecycle**
- **APIs**
- `LaunchedEffect` (Suspend functions)
- `DisposableEffect` (Cleanup/Listeners)
- `SideEffect` (Publish to non-Compose)

- **Helpers**
- `rememberCoroutineScope` (Manual triggers like clicks)
- `rememberUpdatedState` (Fix stale lambdas)
- `produceState` / `snapshotFlow` (Bridges)

- **System**
- Lifecycle Awareness (`ON_START`, `ON_RESUME`)
- Back Handling (`BackHandler`)

- **6. Forms & Inputs**
- **Text**
- `TextField` / `OutlinedTextField`
- `VisualTransformation` (Passwords)
- Focus & Keyboard Actions (`ImeAction.Next`)

- **Selection**
- Pickers (Date/Time)
- `ExposedDropdownMenu`

- **Validation**
- Real-time feedback
- Derived state logic

- **7. Architecture (Clean MVVM)**
- **Layers**
- UI (Screen + ViewModel)
- Domain (UseCases - Pure Kotlin)
- Data (Repository + Retrofit)

- **State Flows**
- `StateFlow` (Persistent UI State)
- `SharedFlow` (One-off Events)
- `collectAsStateWithLifecycle`

- **MVI**
- Sealed Class Actions (`UserIntent`)
- Single Entry Point (`onEvent`)

- **8. Graphics & Custom UI**
- **Layouts**
- `ConstraintLayout` (References, Barriers)
- Custom Layouts (`measure` & `place`)

- **Drawing**
- `Canvas` (DrawScope)
- `graphicsLayer` (Rotation, Scale, Blur)

- **9. Animations**
- **State-Based**
- `animate*AsState` (Simple)
- `AnimatedVisibility` (Enter/Exit)
- `AnimatedContent` (Layout transitions)

- **Orchestrated**
- `updateTransition` (Synced values)
- Shared Element (Hero animations)

- **Gestures**
- `draggable` / `AnchoredDraggable`

- **10. Testing & Interop**
- **Testing**
- Semantics Tree & `testTag`
- `createComposeRule` (Isolated) vs `Android` rule
- Screenshot Testing (Paparazzi)

- **Interop**
- `ComposeView` (Compose inside XML)
- `AndroidView` (XML inside Compose)

- **Accessibility**
- TalkBack support (`mergeDescendants`)
- Font Scaling (`sp` vs `dp`)

- **11. Server-Driven UI (Advanced)**
- **Core**
- JSON Schema -> Registry -> Recursive Renderer

- **Logic**
- Versioning & Fallbacks
- Dynamic Action Handling

---

**This is the complete picture.**

```mermaid
graph TD
    Start((Start Here)) --> L1[1. Foundation & Layouts]

    %% Level 1: Basics
    L1 --> L1_1{Core Concepts}
    L1_1 -->|Thinking in Compose| L1_2[Declarative UI]
    L1_1 -->|The Loop| L1_3[Recomposition]
    L1 --> L1_4[Basic Layouts]
    L1_4 -->|Rows/Cols| L1_5[Standard Layouts]
    L1_4 -->|Styling| L1_6[Modifiers]

    %% Level 2: State
    L1_5 --> L2[2. State Management]
    L2 --> L2_1{Handling Data}
    L2_1 -->|Memory| L2_2[remember / rememberSaveable]
    L2_1 -->|Flow| L2_3[State Hoisting]
    L2 --> L2_4{Performance}
    L2_4 -->|Optimization| L2_5[Stability & Skipping]
    L2_4 -->|Pitfalls| L2_6[Deferring Reads]

    %% Level 3: Lists
    L2_3 --> L3[3. Lists & Grids]
    L3 --> L3_1[LazyColumn / LazyRow]
    L3 --> L3_2[LazyVerticalGrid]
    L3 --> L3_3[Optimization Keys & Types]

    %% Level 4: Navigation
    L3_1 --> L4[4. Navigation]
    L4 --> L4_1[NavHost & Controller]
    L4 --> L4_2[Type-Safe Args]
    L4 --> L4_3[Nested Graphs]
    L4 --> L4_4[Deep Links]

    %% Level 5: Architecture
    L4 --> L5[5. Architecture & Data]
    L5 --> L5_1[MVVM + Clean Arch]
    L5 --> L5_2[Retrofit & Repositories]
    L5 --> L5_3{Reactive Flow}
    L5_3 -->|UI State| L5_4[StateFlow]
    L5_3 -->|Events| L5_5[SharedFlow / MVI]

    %% Level 6: Side Effects
    L5 --> L6[6. Side-Effects & Lifecycle]
    L6 --> L6_1[LaunchedEffect]
    L6 --> L6_2[DisposableEffect]
    L6 --> L6_3[Lifecycle Awareness]

    %% Level 7: Advanced UI
    L6 --> L7[7. Graphics & Animations]
    L7 --> L7_1{Motion}
    L7_1 -->|Simple| L7_2[animate*AsState]
    L7_1 -->|Complex| L7_3[updateTransition]
    L7_1 -->|Layout| L7_4[Shared Element]
    L7 --> L7_5{Custom UI}
    L7_5 -->|Drawing| L7_6[Canvas & DrawScope]
    L7_5 -->|Layout| L7_7[Custom Layouts]

    %% Level 8: Production
    L7 --> L8[8. Production Quality]
    L8 --> L8_1{Testing}
    L8_1 -->|Unit| L8_2[Semantics & Rules]
    L8_1 -->|Visual| L8_3[Screenshot Tests]
    L8 --> L8_4{Interop}
    L8_4 -->|Old in New| L8_5[AndroidView]
    L8_4 -->|New in Old| L8_6[ComposeView]
    L8 --> L8_7[Accessibility & TalkBack]

    L8 --> End((Ready for Interview))
```

---

## Navigation

Next â†’
