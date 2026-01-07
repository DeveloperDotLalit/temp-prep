---
layout: default
title: Network & Data Integration
parent: 7. Clean MVVM with Compose
nav_order: 5
---

# Network & Data Integration

Here are your notes for **Topic 7.5**.

---

## **Topic 7.5: Network & Data Integration**

### **1. What It Is**

This topic connects your clean architecture to the real world. It covers fetching data from a REST API (using **Retrofit**), routing it through a **Repository**, and modeling the result as a UI State (Loading / Success / Error) that the Composable can render.

### **2. Why It Exists (The "Network on Main Thread" Rule)**

- **Safety:** You cannot perform network operations on the Main (UI) Thread. It freezes the app and causes an "Application Not Responding" (ANR) crash.
- **Abstraction:** The UI shouldn't know JSON exists. It just wants a list of `User` objects. The Repository handles the ugly JSON parsing and error handling.
- **State Handling:** Networks are slow and unreliable. You _must_ show the user what is happening (Loading spinner) or what went wrong (Error message).

### **3. How It Works (The Chain)**

1. **Retrofit Interface:** Defines the HTTP endpoints.
2. **Repository:** Calls Retrofit, catches exceptions (try-catch), and returns a safe result (usually a sealed class like `Resource<T>`).
3. **ViewModel:** Launches a coroutine, calls the Repository, and updates the `StateFlow`.
4. **UI:** Observes the `StateFlow` and switches layout based on the state.

### **4. Handling States (The Sealed Class Pattern)**

Instead of passing raw data, wrap it in a wrapper that describes the _status_ of the data.

```kotlin
// A generic wrapper for any data type T
sealed class Resource<out T> {
    data object Loading : Resource<Nothing>()
    data class Success<out T>(val data: T) : Resource<T>()
    data class Error(val message: String) : Resource<Nothing>()
}

```

### **5. Example: The Complete Flow**

**Step 1: The API (Retrofit)**

```kotlin
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<UserDto> // Suspend is key!
}

```

**Step 2: The Repository (The Safety Layer)**

```kotlin
class UserRepository @Inject constructor(private val api: ApiService) {

    // We emit flows so the UI gets updates (Loading -> Data)
    fun getUsers(): Flow<Resource<List<User>>> = flow {
        emit(Resource.Loading) // 1. Signal Loading
        try {
            val result = api.getUsers()
            // Map DTO to Domain Model here if needed
            emit(Resource.Success(result.map { it.toDomain() })) // 2. Signal Success
        } catch (e: Exception) {
            emit(Resource.Error("Network Failed: ${e.message}")) // 3. Signal Error
        }
    }
}

```

**Step 3: The UI (Reactive Switch)**

```kotlin
@Composable
fun UserListScreen(viewModel: UserViewModel) {
    val state by viewModel.userState.collectAsStateWithLifecycle()

    when (state) {
        is Resource.Loading -> {
            CircularProgressIndicator() // Show Spinner
        }
        is Resource.Error -> {
            Text("Error: ${(state as Resource.Error).message}", color = Color.Red)
            Button(onClick = { viewModel.retry() }) { Text("Retry") }
        }
        is Resource.Success -> {
            val users = (state as Resource.Success).data
            LazyColumn {
                items(users) { user -> Text(user.name) }
            }
        }
    }
}

```

### **6. Interview Prep**

**Interview Keywords**
Retrofit, Repository Pattern, `Resource<T>` / `Result<T>` Wrapper, `suspend` functions, Dispatchers.IO, Exception Handling, Mapper (DTO to Domain).

**Interview Speak Paragraph**

> "I integrate network calls by following the Repository pattern. I use Retrofit with Coroutines support to define my API endpoints as suspend functions. In the Repository layer, I wrap these calls in a `try-catch` block and expose the data as a `Flow<Resource<T>>`. This `Resource` sealed class encapsulates the three potential states: Loading, Success, and Error. The ViewModel collects this flow and updates the UI State. This ensures the UI is dumb—it simply reacts to the state by showing a progress bar, the data list, or an error message—while all the complexity of networking and error handling is contained within the Data layer."

---

**Next Step:**
We can load 10 items. But what if the server has 10,000 items? We can't load them all at once.
Ready for **Topic 7.6: Pagination**? This covers the Paging 3 library.

---

## Navigation

â† Previous
Next â†’
