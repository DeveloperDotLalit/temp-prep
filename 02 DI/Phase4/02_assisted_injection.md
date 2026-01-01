---
layout: default
title: Phase 3: Hilt – Topic 6: Assisted Injection
parent: Phase4
nav_order: 2
---

Here are the detailed notes for the sixth topic of Phase 3, strictly adhering to the "Book Style" format and the interview summary structure.

---

# Phase 3: Hilt – Topic 6: Assisted Injection

In our journey so far, we have relied on Dagger to provide **100%** of the dependencies for our classes. If a `UserRepository` needs a `RemoteDataSource`, Dagger finds it in the graph and provides it.

**The Problem: The Runtime Gap**
Real-world applications often require dependencies that Dagger **cannot** know about at compile time.
Consider a `DetailsViewModel` that needs two things:

1. `UserRepository` (Known by Dagger/Graph).
2. `currentUserId` (NOT known by Dagger. It comes from the `Intent` or `Navigation Args` when the user taps a specific item).

You cannot write `@Inject constructor(val repo: Repo, val id: String)`. Dagger will fail because it doesn't know where to find that specific `String id`.

**The Naive Solution (Mutator Methods)**
A junior developer solves this by making the ID mutable:

```kotlin
class DetailsViewModel @Inject constructor(val repo: Repo) {
    var userId: String? = null // Mutable and Nullable :(

    fun setID(id: String) {
        this.userId = id
    }
}

```

This is bad architecture. It forces the class to exist in an "invalid state" (where `userId` is null) until someone remembers to call `setID`. We want **Constructor Injection** so the class is valid and immutable from the moment it is born.

**The Elite Solution: Assisted Injection**
Assisted Injection is a pattern where we ask Dagger to "assist" us. We tell Dagger: _"I will provide the `userId` at runtime; you provide the `UserRepository` from the graph, and please combine them into a factory for me."_

### 1. The Three Annotations

To implement this, we use three specific annotations that replace standard injection.

1. **`@AssistedInject`**: Replaces `@Inject` on the constructor.
2. **`@Assisted`**: Tags the specific parameter that comes from Runtime (Manual).
3. **`@AssistedFactory`**: Tags an interface that acts as the "Creator."

### 2. Code Demonstration

**Step 1: The Class (The Consumer)**
We define our class. Notice we mix Graph args (`repository`) and Runtime args (`userId`).

```kotlin
class DetailsService @AssistedInject constructor(
    // 1. Dependency from Graph (Dagger handles this)
    private val repository: UserRepository,

    // 2. Dependency from Runtime (We handle this)
    @Assisted private val userId: String
) {
    fun performAction() {
        println("Performing action for user: $userId with repo: $repository")
    }
}

```

**Step 2: The Factory (The Interface)**
We must define an interface that tells Dagger what the factory looks like.

- The function name doesn't matter (usually `create`).
- The parameters MUST match the `@Assisted` parameters in the class above.

```kotlin
@AssistedFactory
interface DetailsServiceFactory {
    // We pass the runtime argument here.
    // Dagger returns the fully constructed object.
    fun create(userId: String): DetailsService
}

```

**Step 3: The Usage (The Activity)**
Now, instead of injecting the `DetailsService` directly (which is impossible), we inject the **Factory**.

```kotlin
@AndroidEntryPoint
class DetailsActivity : AppCompatActivity() {

    // 1. Inject the Factory (Dagger knows how to build this!)
    @Inject lateinit var factory: DetailsServiceFactory

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 2. Get the ID from the Intent (Runtime Data)
        val userIdFromIntent = intent.getStringExtra("USER_ID") ?: "Default"

        // 3. Use the Factory to create the object
        // We provide the ID; Dagger internally provides the Repository.
        val service = factory.create(userIdFromIntent)

        service.performAction()
    }
}

```

### 3. Assisted Injection in ViewModels

_Note: Hilt has special support for this via `@HiltViewModel` combined with `SavedStateHandle`. Usually, you don't need manual Assisted Injection for ViewModels because `SavedStateHandle` already holds the navigation arguments/Intent extras automatically._

However, for **Workers** (WorkManager) or generic helper classes, Assisted Injection is the only way to combine dynamic data with static dependencies cleanly.

### 4. Why This is "Elite"

Assisted Injection preserves **Immutability**.
By using the factory, we can keep `val userId: String` as a read-only property in the constructor. We never have to create a `lateinit var` or a setter method. The object is guaranteed to be fully initialized with both its data (ID) and its tools (Repository) before any method can be called.

---

## 🛑 Interview Summary: Assisted Injection

### **Keywords**

Runtime Arguments, Compile-Time Dependencies, Factory Pattern, `@AssistedInject`, `@Assisted`, `@AssistedFactory`, Immutability, Dynamic Instantiation, Partial Injection, Boilerplate Generation

### **Paragraph for Interview**

"When I need to construct an object that requires both dependencies from the Dagger graph (like a Repository) and arguments known only at runtime (like a User ID from an Intent), I use Assisted Injection. Standard injection fails here because Dagger cannot resolve the runtime argument. Instead of resorting to setter injection—which creates mutable state and temporal coupling—I use `@AssistedInject` on the constructor and mark the dynamic arguments with `@Assisted`. I then define an interface annotated with `@AssistedFactory`. Dagger generates the implementation of this factory, allowing me to inject the factory into my Activity, pass the runtime arguments to its `create()` method, and receive a fully constructed, immutable object with all dependencies satisfied."

---

### **End of Phase 3**

You have now conquered the specific tools of Hilt.

1. **Migration:** How Hilt wraps Dagger.
2. **Hierarchy:** Standard Components (`@InstallIn`).
3. **ViewModels:** `@HiltViewModel` and `by viewModels`.
4. **Context:** `@ApplicationContext`.
5. **Qualifiers:** Disambiguating types.
6. **Assisted Injection:** Runtime arguments.

We are now entering the final stage. **Phase 4: Elite Architecture & Testing**.
This is where we talk about "System Design" level topics.

- How do I verify my graph works?
- How do I use Multibindings to build plugin systems?
- How does this all work under the hood (KAPT/KSP)?

We will start with **Phase 4, Topic 1: Multibindings (IntoSet / IntoMap)**.
_This is the secret weapon for building scalable, plugin-based apps._

Shall we proceed to **Phase 4**?
