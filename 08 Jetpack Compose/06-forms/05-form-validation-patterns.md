---
layout: default
title: Form Validation Patterns
parent: 6. Forms, Inputs & Sheets
nav_order: 5
---

# Form Validation Patterns

Here are your notes for **Topic 6.5**.

---

## **Topic 6.5: Form Validation Patterns**

### **1. What It Is**

Form validation is the logic that ensures user input meets specific criteria (e.g., "Is this a valid email?", "Is the password strong enough?") before allowing them to proceed.
In Compose, this is handled via **State**. The UI reacts instantly to the validation state, showing red error text or disabling the "Submit" button in real-time.

### **2. Why It Exists (UX & Data Integrity)**

- **Real-time Feedback:** Waiting until the user clicks "Submit" to tell them they made a typo 5 fields ago is bad UX. It's better to show the error instantly or as soon as they finish typing.
- **Safety:** Preventing the submission of bad data saves backend costs and prevents server errors.

### **3. How It Works (The Pattern)**

There are three main strategies:

1. **State Holders:** Create a data class or state variables to hold:

- The `input` (String).
- The `error` (String? or Boolean).
- The `isValid` (Boolean).

2. **Validation Function:** A pure function that checks the input and returns the error state.
3. **UI Reaction:**

- `isError` parameter on `OutlinedTextField` turns the box red.
- `supportingText` shows the specific error message.
- `Button(enabled = isValid)` disables the submit button automatically.

### **4. Example: Real-time Email Validation**

This example shows an email field that turns red if the format is wrong, and a button that stays disabled until the email is valid.

```kotlin
@Composable
fun LoginForm() {
    // 1. STATE
    var email by remember { mutableStateOf("") }

    // 2. DERIVED STATE (Validation Logic)
    // We use derivedStateOf so we don't recalculate logic on every frame,
    // only when 'email' changes.
    val isEmailValid by remember {
        derivedStateOf {
            email.isNotEmpty() && android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()
        }
    }

    // Determine if we should show an error.
    // Trick: Don't show error while user is typing empty string (initial state).
    val showError = email.isNotEmpty() && !isEmailValid

    Column(modifier = Modifier.padding(16.dp)) {
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email Address") },

            // 3. UI FEEDBACK
            isError = showError, // Turns border red
            supportingText = {
                if (showError) {
                    Text("Invalid email format", color = MaterialTheme.colorScheme.error)
                }
            },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        // 4. BUTTON CONTROL
        Button(
            onClick = { /* Submit */ },
            enabled = isEmailValid, // Disabled until valid
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`derivedStateOf`, `isError`, `supportingText`, Real-time Validation, Debouncing (optional), UX Feedback Loop.

**Interview Speak Paragraph**

> "For form validation in Compose, I prefer a reactive, real-time approach. I derive the validation state (isValid) directly from the input state using `derivedStateOf`. This allows me to bind the `isError` and `supportingText` parameters of the `OutlinedTextField` directly to this boolean, providing immediate visual feedback. Furthermore, I control the `enabled` state of the submit button based on the overall validity of the form. This prevents invalid submissions at the UI level, creating a smoother user experience than showing a generic error dialog after the button is clicked."

---

**Congratulations!** You have completed **Part 6: Forms, Inputs & Sheets**.
You can now build fully interactive, data-collecting apps.

Now, we need to structure this mess of code properly.
**Are you ready to start Topic 7: Clean MVVM with Compose?**
_This is where we turn "Spaghetti Code" into "Professional Architecture"._

---

## Navigation

â† Previous
