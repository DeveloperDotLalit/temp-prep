---
layout: default
title: E-Commerce Dashboard (SDUI Focus)
parent: 15. Real World Projects
nav_order: 3
---

# E-Commerce Dashboard (SDUI Focus)

Here are your notes for **Topic 15.3**.

---

## **Topic 15.3: E-Commerce Dashboard (SDUI Focus)**

### **1. What It Is**

This project simulates a dynamic store homepage like Amazon, Flipkart, or Myntra.
The key characteristic is that the **App does not know what the homepage looks like**.
One day it might be [Banner, Carousel, Grid]. The next day (during a sale), it might be [Countdown Timer, Banner, Horizontal List].
This is achieved using **Server-Driven UI (SDUI)**.

**Key Constraints:**

- **Dynamic Layouts:** The screen structure is parsed from a JSON response.
- **Nested Complexity:** Vertical scrolling page containing horizontal carousels, grids, and banners.
- **Analytics:** Every click (Banner Click, Product Tap, Add to Cart) must be tracked genericly.

### **2. Why It Exists (The "Sale Day" Problem)**

Marketing teams need to change the app's layout instantly for Black Friday or Diwali sales. They cannot wait 48 hours for a Play Store update.
This project proves you can build **Generic UI Systems** rather than just hardcoded screens.

### **3. Architecture & Key Tech**

#### **A. The JSON Schema**

The server returns a list of "Sections".

```json
{
  "sections": [
    {
      "type": "hero_banner",
      "data": { "imageUrl": "...", "action": "open_sale" }
    },
    {
      "type": "horizontal_product_list",
      "title": "Best Sellers",
      "items": [ ... ]
    },
    {
      "type": "grid_2x2",
      "items": [ ... ]
    }
  ]
}

```

#### **B. The Component Registry**

A mapping logic that converts the string `"hero_banner"` into the Composable `@Composable fun HeroBanner(...)`.

#### **C. Analytics Interceptor**

Instead of every button calling `Firebase.logEvent(...)`, we use a central `InteractionHandler`. The UI just reports "I was clicked," and the Handler decides what to log.

### **4. Implementation Details**

#### **Step 1: The Generic Renderer**

This is the "Brain" of the screen. It iterates through the JSON sections and delegates to the correct Composable.

```kotlin
@Composable
fun HomeScreen(sections: List<UiSection>, onAction: (UiAction) -> Unit) {
    LazyColumn {
        items(sections) { section ->
            when (section.type) {
                "hero_banner" -> {
                    HeroBanner(
                        data = section.data,
                        onClick = { onAction(UiAction.BannerClick(section.id)) }
                    )
                }
                "horizontal_list" -> {
                    ProductCarousel(
                        data = section.data,
                        onProductClick = { id -> onAction(UiAction.ProductClick(id)) }
                    )
                }
                "grid_2x2" -> {
                    ProductGrid(
                        data = section.data,
                        onProductClick = { id -> onAction(UiAction.ProductClick(id)) }
                    )
                }
                // Fallback for unknown types (Safety)
                else -> Spacer(modifier = Modifier.height(0.dp))
            }

            // Add spacing between dynamic sections
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

```

#### **Step 2: Handling Nested Carousels**

The "Horizontal List" inside the "Vertical Page" is a classic performance trap.

- **Problem:** Nested scrolling conflicts.
- **Solution:** `LazyRow` works fine inside `LazyColumn` automatically in Compose, but ensure you manage state keys so scroll position is remembered.

```kotlin
@Composable
fun ProductCarousel(data: SectionData, onProductClick: (String) -> Unit) {
    Column {
        Text(text = data.title, style = MaterialTheme.typography.titleMedium)

        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(data.products) { product ->
                ProductCard(product, onClick = { onProductClick(product.id) })
            }
        }
    }
}

```

#### **Step 3: Centralized Analytics**

The UI doesn't know about Firebase. It just emits Actions.

```kotlin
class HomeViewModel(
    private val analytics: AnalyticsManager
) : ViewModel() {

    fun handleAction(action: UiAction) {
        when(action) {
            is UiAction.ProductClick -> {
                // 1. Navigation
                navigator.navigateToDetails(action.id)
                // 2. Analytics
                analytics.logEvent("product_view", mapOf("id" to action.id))
            }
            is UiAction.BannerClick -> {
                // ...
            }
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
Server-Driven UI (SDUI), Component Registry, Heterogeneous RecyclerView (in Compose terms), Nested Scrolling (`LazyRow` inside `LazyColumn`), Analytics Wrapper, JSON Deserialization (Polymorphism).

**Interview Speak Paragraph**

> "For the E-Commerce Dashboard, I implemented a Server-Driven UI architecture to allow for dynamic layout updates without app releases. The Dashboard screen is essentially a `LazyColumn` that renders a list of generic 'Section' objects parsed from a JSON response. I used a 'Registry' pattern to map section types—like 'HeroBanner' or 'ProductCarousel'—to specific Composable functions. This approach required careful handling of nested scrolling, specifically placing `LazyRows` inside the parent `LazyColumn`. I also centralized all user interactions into a single 'Action Handler' in the ViewModel, which allowed me to decouple the UI from the Analytics SDKs, making the code cleaner and easier to test."

---

Here are extended, detailed notes for **Topic 15.3: E-Commerce Dashboard (Advanced SDUI Implementation)**.

This section dives deep into the _mechanics_ of building a production-grade Server-Driven UI system, moving beyond the concept and into the code structure required to handle a complex E-Commerce app.

---

## **Topic 15.3 (Extended): SDUI Implementation Details**

### **1. The Challenge: Polymorphism**

In a standard app, you know exactly what you are parsing: `User` object or `Product` object.
In SDUI, the server sends a list of `Components`. The first item might be a `Banner`, the second a `Carousel`, the third a `Countdown`.

- **Problem:** How do you parse a JSON list where every item has a different shape?
- **Solution:** Polymorphic Serialization (using `kotlinx.serialization`).

### **2. The Advanced JSON Schema**

A realistic schema isn't just "Type" and "Data". It includes styling, layout modifiers, and actions.

```json
{
  "version": 2,
  "page_title": "Black Friday Sale",
  "background_color": "#F5F5F5",
  "components": [
    {
      "type": "hero_banner",
      "id": "banner_123",
      "data": {
        "image_url": "https://api.store.com/banner.jpg",
        "aspect_ratio": 1.77,
        "action": {
          "type": "deep_link",
          "url": "app://product/55"
        }
      }
    },
    {
      "type": "countdown_timer",
      "id": "timer_99",
      "data": {
        "target_timestamp": 1735689600,
        "bg_color": "#FF0000",
        "text_color": "#FFFFFF"
      }
    },
    {
      "type": "horizontal_grid",
      "id": "grid_1",
      "data": {
        "title": "Flash Deals",
        "items": [ ... ]
      }
    }
  ]
}

```

### **3. The Data Layer (Polymorphic Parsing)**

This is the most "Senior" part of the code. We use `kotlinx.serialization` to automatically map the `"type"` field to a specific Kotlin class.

```kotlin
@Serializable
sealed class SduiComponent {
    // Abstract properties every component must have
    abstract val id: String
}

// 1. Define the specific shapes
@Serializable
@SerialName("hero_banner") // Maps JSON "type": "hero_banner" to this class
data class HeroBannerComponent(
    override val id: String,
    val data: BannerData
) : SduiComponent()

@Serializable
@SerialName("countdown_timer")
data class TimerComponent(
    override val id: String,
    val data: TimerData
) : SduiComponent()

@Serializable
@SerialName("horizontal_grid")
data class GridComponent(
    override val id: String,
    val data: GridData
) : SduiComponent()

// 2. The Response Wrapper
@Serializable
data class PageResponse(
    val components: List<SduiComponent> // Automatically parses mixed types!
)

```

### **4. The UI Registry (The Render Engine)**

Instead of a giant `when` statement inside the Composable (which grows huge), we create a **Registry Interface**. This allows us to split components into different files.

**The Renderer:**

```kotlin
@Composable
fun SduiEngine(
    components: List<SduiComponent>,
    onAction: (Action) -> Unit // Global Action Handler
) {
    LazyColumn(
        contentPadding = PaddingValues(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp) // Gap between sections
    ) {
        items(
            items = components,
            key = { it.id }, // CRITICAL: SDUI needs stable keys for updates
            contentType = { it::class.simpleName } // Optimization for Compose
        ) { component ->

            // Delegate to specific Composables
            when (component) {
                is HeroBannerComponent -> HeroBannerView(component, onAction)
                is TimerComponent -> CountdownTimerView(component)
                is GridComponent -> HorizontalGridView(component, onAction)
                // Graceful Fallback for unknown types
                else -> UnknownComponentView()
            }
        }
    }
}

```

### **5. Handling Dynamic Actions (The Interaction Layer)**

Buttons in SDUI can't hardcode `navController.navigate()`. They must emit generic actions.

**The Action Model:**

```kotlin
@Serializable
sealed class Action {
    @SerialName("deep_link")
    data class DeepLink(val url: String) : Action()

    @SerialName("add_to_cart")
    data class AddToCart(val productId: String, val sku: String) : Action()

    @SerialName("toast")
    data class ShowToast(val message: String) : Action()
}

```

**The Action Handler (ViewModel/Activity):**

```kotlin
fun handleAction(action: Action) {
    when (action) {
        is Action.DeepLink -> {
            // Parses "app://product/55" -> Navigates to ProductDetails
            deepLinkManager.handle(action.url)
        }
        is Action.AddToCart -> {
            // Triggers API call
            cartRepository.add(action.productId)
            analytics.log("add_to_cart", action.productId)
        }
    }
}

```

### **6. SDUI State Management (The Hard Part)**

**Scenario:** You have a "Counter" component in SDUI. Does the server track the count, or the app?

- **Rule:** **Ephemeral UI State** (Animations, Scroll position, Countdown ticks) lives in **Compose**. **Business Data** (Cart count, Product Price) lives in the **Server**.

**Example: The Countdown Timer**
The Server sends the _Target Timestamp_. The App handles the _Ticking_.

```kotlin
@Composable
fun CountdownTimerView(component: TimerComponent) {
    // 1. Server provided the Target Time
    val targetTime = component.data.targetTimestamp

    // 2. Local State handles the "tick" UI
    var timeLeft by remember { mutableLongStateOf(targetTime - System.currentTimeMillis()) }

    LaunchedEffect(Unit) {
        while (timeLeft > 0) {
            delay(1000)
            timeLeft = targetTime - System.currentTimeMillis()
        }
    }

    Text(
        text = formatTime(timeLeft),
        color = Color(android.graphics.Color.parseColor(component.data.textColor))
    )
}

```

### **7. Implementation Interview Checklist**

- **Serialization:** "I use `kotlinx.serialization` with `@SerialName` for polymorphic parsing of heterogeneous lists."
- **Keys:** "I ensure every component from the server has a unique `id` so `LazyColumn` can optimize updates efficiently."
- **Theming:** "I parse Hex colors from the JSON (e.g., `#FF0000`) but wrap them in a `try-catch` or helper function to default to my app's theme colors if the server sends an invalid value."
- **Versioning:** "If the API sends a component type my app doesn't know (e.g., `'vr_view'`), my `when` block defaults to an empty `Spacer` so the app doesn't crash."

---

## Navigation

â† Previous
