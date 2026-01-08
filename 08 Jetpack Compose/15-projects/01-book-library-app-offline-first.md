---
layout: default
title: Book Library App (Offline First)
parent: 15. Real World Projects
nav_order: 1
---

# Book Library App (Offline First)

Here are your notes for **Topic 15.1**.

---

# Topic 15: Real World Projects

## **Topic 15.1: Book Library App (Offline First)**

### **1. What It Is**

This is the classic "Capstone Project" for Android developers. It is a CRUD (Create, Read, Update, Delete) application that allows users to manage a collection of books.
**Key Constraints:**

- **Offline First:** The app must work perfectly without the internet. Data is saved locally on the device.
- **Complex Forms:** It's not just a "To-Do" list. Books have Titles, Authors, ISBNs (Validation), Genres (Dropdowns), and Read Status (Toggles).
- **Modern Polish:** It supports Dark Mode and uses a Multi-Module architecture to separate concerns.

### **2. Why It Exists (The Skills Matrix)**

Building this proves you understand the **Data Layer** and **Persistence**.

- **Room:** Shows you can map Objects to SQL tables.
- **State Management:** Shows you can handle Form Validation (e.g., "Save" button disabled until ISBN is valid).
- **Architecture:** Shows you know how to decouple the UI from the Database using Repositories and ViewModels.

### **3. Architecture & Key Tech**

#### **A. Multi-Module Structure**

Instead of one giant `app` module, we split it up to speed up builds and enforce separation.

1. **`:core:data`**: Contains Room Entities, DAOs, and the Database instance.
2. **`:core:designsystem`**: Contains `Type.kt`, `Color.kt`, and reusable buttons/inputs.
3. **`:feature:library`**: The screen showing the list of books.
4. **`:feature:addbook`**: The screen with the complex form.
5. **`:app`**: The glue that connects them (Navigation).

#### **B. The "Offline First" Pattern**

The **Database is the Single Source of Truth**.

1. **Read:** The UI observes `Flow<List<Book>>` from the DAO.
2. **Write:** When the user clicks "Save", the ViewModel calls `repository.insert(book)`.
3. **Update:** Room automatically emits the new list via the Flow. The UI updates instantly.

### **4. Implementation Details**

#### **Step 1: Room Setup (`:core:data`)**

Define the table and the access methods.

```kotlin
// 1. The Entity (Table)
@Entity(tableName = "books")
data class BookEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val title: String,
    val author: String,
    val isRead: Boolean,
    val genre: String // Stored as String, mapped to Enum in UI
)

// 2. The DAO (Access)
@Dao
interface BookDao {
    // Return Flow for real-time updates
    @Query("SELECT * FROM books ORDER BY title ASC")
    fun getAllBooks(): Flow<List<BookEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBook(book: BookEntity)

    @Delete
    suspend fun deleteBook(book: BookEntity)
}

```

#### **Step 2: Complex Form with Validation (`:feature:addbook`)**

Handling multiple inputs and validation logic.

```kotlin
@Composable
fun AddBookScreen(viewModel: AddBookViewModel) {
    // State Hoisting: ViewModel holds the raw inputs
    val title by viewModel.title.collectAsStateWithLifecycle()
    val isbn by viewModel.isbn.collectAsStateWithLifecycle()

    // Derived State: Is the form valid?
    val isFormValid by remember {
        derivedStateOf { title.isNotEmpty() && isbn.length == 13 }
    }

    Column(modifier = Modifier.padding(16.dp)) {
        OutlinedTextField(
            value = title,
            onValueChange = { viewModel.updateTitle(it) },
            label = { Text("Book Title") },
            isError = title.isEmpty() // Visual Feedback
        )

        OutlinedTextField(
            value = isbn,
            onValueChange = { if (it.length <= 13) viewModel.updateIsbn(it) },
            label = { Text("ISBN (13 digits)") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = { viewModel.saveBook() },
            enabled = isFormValid, // Disable until valid
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Save to Library")
        }
    }
}

```

#### **Step 3: Handling Dark Mode**

We don't hardcode colors like `Color.Black`. We use **MaterialTheme tokens**.

```kotlin
// In your Composable
Text(
    text = "Library",
    // Uses Black in Light Mode, White in Dark Mode automatically
    color = MaterialTheme.colorScheme.onBackground
)

Surface(
    // Uses White in Light Mode, Dark Grey in Dark Mode
    color = MaterialTheme.colorScheme.background
) { ... }

```

### **5. Interview Prep**

**Interview Keywords**
Room Database, `Flow` (Reactive updates), Single Source of Truth, DAO, Entity, Multi-Module, Feature Modules, `derivedStateOf` (Form Validation), Dark Mode (`onBackground`).

**Interview Speak Paragraph**

> "One of my key projects is an offline-first Book Library app built with a multi-module architecture. I separated the data layer into a dedicated `:core:data` module, using **Room** as the single source of truth. By exposing a `Flow<List<Book>>` from the DAO, the UI in the `:feature:library` module reacts instantly to database changes without manual refreshes. For the 'Add Book' feature, I implemented a complex form with real-time validation logic—disabling the submit button until the ISBN and Title met specific criteria. I also implemented full Dark Mode support by strictly adhering to `MaterialTheme` color tokens instead of hardcoding hex values."

---

**Next Step:**
This was the Offline app. Now let's look at the Online app.
Ready for **Topic 15.2: Chat/Social App (Real-Time)**?

---

## Navigation

Next â†’
