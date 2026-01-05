---
layout: default
title: Jetpack Compose Masterclass
nav_order: 9
has_children: true
---

# Jetpack Compose Masterclass: Zero to Hero

A complete end-to-end roadmap covering Jetpack Compose from fundamentals to advanced internals, real-world projects, and interview preparation.

### **Jetpack Compose Masterclass: Zero to Hero**

#### **1. Introduction + Basic Composables**

- **What is Jetpack Compose?**
  _Description:_ Evolution of Android UI, declarative vs. imperative programming, compiler-based UI generation.

- **Why Compose (vs XML)?**
  _Description:_ Less code, live previews, Kotlin integration, unbundled libraries, legacy view system drawbacks.

- **Compose Architecture (Declarative UI Basics)**
  _Description:_ The concept of a UI tree, how functions transform data into UI, separation of concerns.

- **Setting up the Environment** [Added]
  _Description:_ Gradle dependencies, Bill of Materials (BOM) versioning, setting up Android Studio for Compose.

- **Theme, Typography, Colors, Shapes**
  _Description:_ Material3 design tokens, defining color palettes (light/dark), centralized typography styles, shape definitions.

- **Understanding @Composable functions**
  _Description:_ Function syntax, annotation processing, idempotency, side-effect free requirement.

- **Basic UI Components**
  _Description:_ `Text` (styling, spans), `Button` (variants, onClick), `Spacer` (layout gaps), `Icon` (vectors, contentDescription), `Surface` (elevation, clipping).

- **Layout Primitives: Column, Row, Box**
  _Description:_ Arrangement (Start, End, Center, SpaceBetween), Alignment (CenterVertically, etc.), stacking views with Box.

- **The Scaffold Layout** [Added - Vital]
  _Description:_ The standard material layout structure, TopBar, BottomBar, FloatingActionButton (FAB), SnackbarHost slots.

- **Modifier Basics & Chaining Order**
  _Description:_ Padding, sizing (fillMaxWidth, wrapContent), background, clickable, border, clip. _Focus on how order matters (padding before background vs. after)._

- **Debugging UI**
  _Description:_ Layout Inspector, Preview tools, Interactive Preview mode, deploying to device.

#### **2. State & Recomposition (The Core)**

- **What is State?**
  _Description:_ UI as a function of state, source of truth, state vs. events.

- **Composition & Recomposition**
  _Description:_ The lifecycle of a composable, smart recomposition (skipping unchanged elements), call site identity.

- **State Holders: `remember` vs `mutableStateOf`**
  _Description:_ Preserving state across recompositions vs. creating observable state holders.

- **State Hoisting** [Added - Vital]
  _Description:_ Moving state up to the caller to make components stateless and reusable, unidirectional data flow (UDF).

- **`rememberSaveable`**
  _Description:_ Surviving configuration changes (screen rotation), Parcelize, MapSaver, ListSaver.

- **`derivedStateOf`**
  _Description:_ Optimizing performance by converting rapid state changes into fewer distinct updates (e.g., scroll offsets).

- **`CompositionLocal`** [Added - Advanced]
  _Description:_ Implicitly passing data down the tree (like Themes or Context) without passing arguments everywhere, `staticCompositionLocal` vs `compositionLocalOf`.

#### **3. Lists, Grids & UI Enhancements**

- **Lazy Layouts: `LazyColumn` / `LazyRow`**
  _Description:_ Recycling mechanics, view vs. item, `contentPadding`, `verticalArrangement`.

- **Efficient Item Keys**
  _Description:_ Using stable IDs for `key` parameter to prevent unnecessary recompositions during sorting/shuffling.

- **Grids: `LazyVerticalGrid` / `StaggeredGrid`** [Added]
  _Description:_ Fixed count columns, adaptive columns, masonry-style layouts.

- **Sticky Headers** [Added]
  _Description:_ Grouping data with headers that stick to the top during scroll.

- **Swipe to Dismiss / Delete** [Added]
  _Description:_ `SwipeToDismissBox`, background modifiers, handling swipe thresholds.

- **HorizontalPager / VerticalPager**
  _Description:_ Carousel implementation, `PagerState`, page indicators, snapping behaviors.

- **Dialogs & Popups**
  _Description:_ `AlertDialog`, custom `Dialog` window, `Popup` properties to overlay content.

- **Image Loading (Coil/Glide)**
  _Description:_ `AsyncImage`, placeholders, error states, `SubcomposeAsyncImage` for complex loading states, caching strategies.

#### **4. Navigation in Compose (Type-Safe)**

- **Navigation Architecture**
  _Description:_ Single Activity architecture, `NavHost`, `NavController`, navigation graph concepts.

- **Type-Safe Navigation (Kotlin Serialization)** [Updated]
  _Description:_ Defining routes as Serializable Objects/Data Classes (New standard), removing String-based routes.

- **Passing Arguments**
  _Description:_ Passing complex objects, optional arguments, retrieving results from the savedStateHandle.

- **Nested Navigation** [Added]
  _Description:_ Grouping related screens (e.g., Auth flow, Onboarding flow) into sub-graphs, modularizing navigation.

- **Bottom Navigation & Rail**
  _Description:_ Integrating `NavigationBar` with `NavHost`, handling back stack for tabs (saveState/restoreState).

- **Deep Links** [Added]
  _Description:_ Handling external URLs to open specific screens, `navDeepLink` builder.

#### **5. Side-Effects & Lifecycles**

- **The Side-Effect APIs**
  _Description:_ When to use `LaunchedEffect` (suspend functions), `SideEffect` (publishing state to non-compose), `DisposableEffect` (cleanup/teardown).

- **`rememberCoroutineScope`**
  _Description:_ Launching coroutines from user actions (clicks) vs. composition lifecycle.

- **`rememberUpdatedState`**
  _Description:_ Capturing values in long-running effects without restarting the effect.

- **`produceState` & `snapshotFlow`**
  _Description:_ Converting non-Compose state (Flows, LiveData) into State, and converting Compose State back into Flows.

- **Lifecycle Awareness**
  _Description:_ `LifecycleEventObserver`, handling ON_START/ON_RESUME within composables.

- **System Back Handling**
  _Description:_ `BackHandler` composable, intercepting back presses for custom logic (e.g., closing a drawer).

#### **6. Forms, Inputs & Sheets**

- **Text Inputs**
  _Description:_ `TextField` vs `OutlinedTextField`, input types (password, number), `VisualTransformation` (credit card formatting).

- **Keyboard Actions & Focus Management** [Added]
  _Description:_ IME actions (Done, Next, Search), `FocusRequester`, moving focus programmatically.

- **Pickers & Menus**
  _Description:_ `DatePicker`, `TimePicker` (input vs dial), `ExposedDropdownMenuBox` (combobox).

- **Bottom Sheets**
  _Description:_ `ModalBottomSheet` (overlay), `BottomSheetScaffold` (persistent), handling sheet state (expand/collapse/hide).

- **Form Validation Patterns** [Added]
  _Description:_ Real-time validation, error messages support, enabling/disabling submit buttons based on state.

#### **7. Clean MVVM with Compose**

- **Architectural Layers**
  _Description:_ Domain (UseCase), Data (Repository), UI (Screen + ViewModel), dependency direction.

- **State Management Patterns**
  _Description:_ `StateFlow` / `SharedFlow`, `collectAsStateWithLifecycle` (lifecycle-safe collection).

- **Handling UI Events (MVI concepts)**
  _Description:_ Modeling user actions as sealed classes (Intents), "One-time" events (Navigation, Snackbar) vs. State.

- **Dependency Injection (Hilt/Koin)**
  _Description:_ `@HiltViewModel`, injecting ViewModels into Composables, providing dependencies.

- **Network & Data Integration**
  _Description:_ Retrofit setup, Repository pattern implementation, handling loading/success/error states in UI.

- **Pagination**
  _Description:_ Implementing `Paging 3` library with Compose, `collectAsLazyPagingItems`, loading states for footer/header.

#### **8. Advanced Layouts & Graphics** [New Advanced Section]

- **ConstraintLayout in Compose**
  _Description:_ References, barriers, guidelines, chains, JSON-based constraints (MotionLayout concepts).

- **Custom Layouts**
  _Description:_ The `Layout` composable, measurement policy, `measure` and `place` logic, creating custom grids or circular layouts.

- **Canvas & Custom Drawing**
  _Description:_ `DrawScope`, drawing paths, arcs, shapes, blend modes, gradients (Brush).

- **Graphics Modifiers**
  _Description:_ `graphicsLayer` (rotation, scale, alpha), clipping shapes, render effects (blur - Android 12+).

#### **9. Animations**

- **State-Based Animations**
  _Description:_ `animate*AsState` (Float, Color, Dp), simple fire-and-forget value changes.

- **Visibility & Content Change**
  _Description:_ `AnimatedVisibility` (expand/shrink, fade), `AnimatedContent` (transitioning between different layouts).

- **Transition API**
  _Description:_ `updateTransition` for coordinating multiple values, `rememberInfiniteTransition` for pulsing/loading effects.

- **Gesture-Driven Animations**
  _Description:_ `draggable`, `swipeable` (AnchoredDraggable), parallax effects using scroll offsets.

- **Shared Element Transitions** [Added - New in Compose]
  _Description:_ Hero animations between navigation screens, `sharedElement` modifier.

#### **10. Interoperability & Migration** [New Advanced Section]

- **Compose in Views**
  _Description:_ Using `ComposeView` in XML layouts, `setViewCompositionStrategy` (disposing correctly).

- **Views in Compose**
  _Description:_ `AndroidView` composable, embedding MapView/AdView/CameraPreview, handling lifecycle updates for legacy views.

#### **11. Testing in Compose** [Expanded]

- **Test Semantics**
  _Description:_ The semantics tree, `testTag`, `contentDescription`, finding nodes (`onNodeWithText`, `onNodeWithTag`).

- **Assertions & Actions**
  _Description:_ `assertIsDisplayed`, `assertIsEnabled`, `performClick`, `performTextInput`, `performScrollTo`.

- **Screenshot Testing (Optional but good)**
  _Description:_ Using Roborazzi or Paparazzi to verify pixel-perfect UI rendering.

- **Isolating UI Tests**
  _Description:_ `createComposeRule` vs `createAndroidComposeRule`, testing isolated components without launching full activities.

#### **12. Performance & Internals** [Split from SDUI]

- **Stability System**
  _Description:_ `@Stable` vs `@Immutable`, how mutable objects break skipping, inferred stability.

- **Common Pitfalls**
  _Description:_ Reading state in composition vs. reading in layout/draw phases (deferring reads), unnecessary object allocations.

- **Tooling**
  _Description:_ Compose Compiler Metrics (reports), Layout Inspector, GPU Overdraw.

- **R8 & ProGuard**
  _Description:_ Keeping rule sets for shrinking, obfuscation impacts.

#### **13. Server Driven UI (SDUI)**

- **Concept & Architecture**
  _Description:_ JSON schema definition, mapping JSON types to Composable registries.

- **Versioning & Compatibility**
  _Description:_ Handling unknown components, backward compatibility, fallback UI.

- **Dynamic Navigation**
  _Description:_ Routing based on server responses, deep linking integration.

#### **14. Accessibility (A11y)** [New Section]

- **Semantics Modifier**
  _Description:_ Merging descendants, custom actions, headings, traversal order.

- **TalkBack & Font Scaling**
  _Description:_ Testing with screen readers, ensuring layouts adapt to large font sizes (sp vs dp).

#### **15. Real World Projects**

- **Book Library App (Offline First)**
  _Focus:_ Room Database, Local Storage, Complex Forms, Dark Mode, Multi-module structure.

- **Social/News Feed (Performance Focus)**
  _Focus:_ Infinite Scroll (Paging3), Video auto-play in lists, Nested scrolling, complex item layouts.

- **E-Commerce Dashboard (SDUI Focus)**
  _Focus:_ Dynamic home screen driven by JSON, complex grid layouts, analytics tracking.

#### **16. Interview Prep**

- **Theoretical Q&A:** Lifecycle, Side-effects, Compiler magic, State management.
- **Scenario-Based:** "How to debug excessive recomposition?", "Design a chat screen with bottom-up stacking", "Migrate a fragment to Compose".
- **System Design:** Designing a design system, planning navigation for a multi-module app.

#### **17. Resources & Cheat Sheets**

- **Mindmap:** A visual tree of the syllabus.
- **Common Modifiers Cheat Sheet:** Quick reference for alignment/styling.
- **Code Snippet Library:** Ready-to-use templates for Scaffolds, Lists, and Dialogs.
