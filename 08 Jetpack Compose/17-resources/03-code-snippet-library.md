---
layout: default
title: Code Snippet Library
parent: 17. Resources & Cheat Sheets
nav_order: 3
---

# Code Snippet Library

Here are your notes for **Topic 1.7: Code Snippet Library**.

---

## **Topic 1.7: Code Snippet Library**

### **1. What It Is**

This is your "Copy-Paste" arsenal. Instead of typing the boilerplate for a screen structure or a popup dialog from memory every time, you keep these optimized templates ready. They follow the best practices (like handling padding in Scaffolds or using keys in Lists).

### **2. Why It Exists (Velocity)**

- **Boilerplate Reduction:** You shouldn't waste brain power remembering the exact parameter name for `onDismissRequest`.
- **Correctness:** These snippets prevent common bugs (e.g., forgetting to use `innerPadding` in a Scaffold, which causes content to be hidden behind the Top Bar).

---

### **3. The Templates**

#### **A. The Standard Screen (Scaffold)**

A full-screen layout with a Top Bar, a Floating Action Button, and a content area that respects system bars.

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScreenTemplate() {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Screen Title") },
                navigationIcon = {
                    IconButton(onClick = { /* Back */ }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { /* Action */ }) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) { innerPadding ->
        // CRITICAL: You must apply 'innerPadding' to your content
        // to prevent it from overlapping with the TopBar or BottomBar.
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentAlignment = Alignment.Center
        ) {
            Text("Body Content Goes Here")
        }
    }
}

```

#### **B. The Optimized List (LazyColumn)**

A scrolling list that is performant and handles user interactions.

```kotlin
@Composable
fun <T> ListTemplate(
    items: List<T>,
    onItemClick: (T) -> Unit
) {
    LazyColumn(
        contentPadding = PaddingValues(16.dp), // Add spacing around the list
        verticalArrangement = Arrangement.spacedBy(8.dp) // Space between items
    ) {
        items(
            count = items.size,
            // OPTIMIZATION: Always provide a stable key if possible!
            // This helps Compose update only changed items.
            key = { index -> items[index].hashCode() }
        ) { index ->
            val item = items[index]

            // The Item Row
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(Color.LightGray)
                    .clickable { onItemClick(item) } // Handle Click
                    .padding(horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(text = "Item $index")
            }
        }
    }
}

```

#### **C. The Alert Dialog**

A standard popup asking for user confirmation.

```kotlin
@Composable
fun ConfirmationDialog(
    showDialog: Boolean,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit
) {
    if (showDialog) {
        AlertDialog(
            onDismissRequest = { onDismiss() }, // User clicks outside or Back button
            title = { Text("Delete Item?") },
            text = { Text("This action cannot be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    onConfirm()
                    onDismiss()
                }) {
                    Text("Delete", color = Color.Red)
                }
            },
            dismissButton = {
                TextButton(onClick = { onDismiss() }) {
                    Text("Cancel")
                }
            }
        )
    }
}

```

---

### **4. Interview Prep**

**Interview Keywords**
Scaffold `innerPadding`, `LazyColumn` contentPadding vs. modifier padding, `key` optimization, `AlertDialog` state management, Slot API.

**Interview Speak Paragraph**

> "When building screens in Compose, I rely on the `Scaffold` component to handle the standard material layout structure. A crucial detail often missed is utilizing the `innerPadding` parameter provided by the Scaffold lambda; failing to apply this to the body content causes it to be obscured by the TopBar. For lists, I always use `LazyColumn` with explicitly defined `keys` to ensure efficient recomposition, and I prefer using `contentPadding` over modifier padding to ensure the scroll content isn't clipped at the edges."

---

Here are additional, ready-to-use snippets for common UI patterns.

### **D. The Bottom Sheet (Modal)**

A popup that slides up from the bottom. Great for menus or secondary details.

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SimpleBottomSheet(
    showSheet: Boolean,
    onDismiss: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState()

    if (showSheet) {
        ModalBottomSheet(
            onDismissRequest = onDismiss,
            sheetState = sheetState
        ) {
            // Sheet Content
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("Options", style = MaterialTheme.typography.titleLarge)
                Spacer(modifier = Modifier.height(16.dp))
                Button(
                    onClick = { /* Do something */ },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Share")
                }
                TextButton(
                    onClick = onDismiss,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Cancel")
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

```

### **E. Tab Layout (Pager Integration)**

A standard Tab row that switches content. Often used with `HorizontalPager`.

```kotlin
@Composable
fun TabScreen() {
    var selectedTabIndex by remember { mutableIntStateOf(0) }
    val tabs = listOf("Home", "Search", "Profile")

    Column {
        TabRow(selectedTabIndex = selectedTabIndex) {
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedTabIndex == index,
                    onClick = { selectedTabIndex = index },
                    text = { Text(title) }
                )
            }
        }

        // Content Area
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text("Current Tab: ${tabs[selectedTabIndex]}")
        }
    }
}

```

### **F. Loading & Error States**

A utility to handle the 3 states of network data: Loading, Error, and Success.

```kotlin
@Composable
fun <T> ContentWithState(
    isLoading: Boolean,
    error: String?,
    content: @Composable () -> Unit
) {
    Box(modifier = Modifier.fillMaxSize()) {
        when {
            isLoading -> {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            }
            error != null -> {
                Column(
                    modifier = Modifier.align(Alignment.Center),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text("Error: $error", color = Color.Red)
                    Button(onClick = { /* Retry Logic */ }) { Text("Retry") }
                }
            }
            else -> {
                content()
            }
        }
    }
}

```

### **G. Custom Top Bar (Center Aligned)**

Sometimes the default `TopAppBar` isn't enough. Here's a custom centered one.

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CenteredTopBar(
    title: String,
    onBackClick: () -> Unit
) {
    CenterAlignedTopAppBar(
        title = {
            Text(
                text = title,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        },
        navigationIcon = {
            IconButton(onClick = onBackClick) {
                Icon(
                    imageVector = Icons.Default.ArrowBack,
                    contentDescription = "Back"
                )
            }
        },
        actions = {
            IconButton(onClick = { /* Settings */ }) {
                Icon(
                    imageVector = Icons.Default.Settings,
                    contentDescription = "Settings"
                )
            }
        }
    )
}

```

Here are a few more high-utility snippets to round out your library.

### **H. The Image Grid (LazyVerticalGrid)**

A photo-gallery style layout. It automatically calculates column widths.

```kotlin
@Composable
fun PhotoGrid(photos: List<String>) {
    LazyVerticalGrid(
        columns = GridCells.Adaptive(minSize = 128.dp), // Auto-fit columns
        contentPadding = PaddingValues(8.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(photos) { photoUrl ->
            // Use Coil or standard Image here
            Box(
                modifier = Modifier
                    .aspectRatio(1f) // Force square shape
                    .clip(RoundedCornerShape(8.dp))
                    .background(Color.LightGray)
            ) {
                // Image( ... )
            }
        }
    }
}

```

### **I. Network Image with Placeholder (Coil)**

If you use the **Coil** library (standard for Compose), here is a robust wrapper that handles loading and error states gracefully.

_Dependency:_ `io.coil-kt:coil-compose:2.x`

```kotlin
@Composable
fun NetworkImage(
    url: String,
    modifier: Modifier = Modifier
) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(url)
            .crossfade(true)
            .build(),
        contentDescription = null,
        contentScale = ContentScale.Crop,
        modifier = modifier.clip(RoundedCornerShape(8.dp)),
        // Show a gray box while loading
        placeholder = painterResource(R.drawable.placeholder_image),
        // Show an error icon if it fails
        error = painterResource(R.drawable.error_image)
    )
}

```

### **J. Expandable Card (FAQ Style)**

A row that expands to show more text when clicked, with a smooth built-in animation.

```kotlin
@Composable
fun ExpandableCard(title: String, body: String) {
    var expanded by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .animateContentSize() // AUTOMATIC ANIMATION MAGIC
            .clickable { expanded = !expanded },
        shape = RoundedCornerShape(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Header Row
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.weight(1f)
                )
                Icon(
                    imageVector = if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                    contentDescription = "Expand"
                )
            }

            // Expandable Content
            if (expanded) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = body,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}

```

### **K. The "Clean" Search Bar**

A nice looking search input field that clears itself when the 'X' is clicked.

```kotlin
@Composable
fun SearchInput(
    query: String,
    onQueryChange: (String) -> Unit,
    onSearch: () -> Unit
) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        placeholder = { Text("Search...") },
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = { onQueryChange("") }) {
                    Icon(Icons.Default.Clear, contentDescription = "Clear")
                }
            }
        },
        singleLine = true,
        shape = RoundedCornerShape(24.dp), // Pill shape
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
        keyboardActions = KeyboardActions(onSearch = { onSearch() })
    )
}

```

---

---

## Navigation

â† Previous
