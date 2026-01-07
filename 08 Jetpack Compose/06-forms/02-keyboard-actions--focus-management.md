---
layout: default
title: Keyboard Actions & Focus Management
parent: 6. Forms, Inputs & Sheets
nav_order: 2
---

# Keyboard Actions & Focus Management

Here are your notes for **Topic 6.2**.

---

## **Topic 6.2: Keyboard Actions & Focus Management**

### **1. What It Is**

This topic covers how to control the "flow" of a form using the soft keyboard.

- **Keyboard Actions:** What happens when you press the blue button on the keyboard (e.g., "Next", "Search", "Done").
- **Focus Management:** How to programmatically move the blinking cursor from one box to another (e.g., jumping from "First Name" to "Last Name" automatically).

### **2. Why It Exists (The "Tab" Key Experience)**

On a PC, you press "Tab" to fly through a form. On mobile, you expect the keyboard's bottom-right button to do the same.

- **Bad UX:** The user types their email, presses "Enter", and the keyboard just adds a new line or does nothing. They have to manually tap the "Password" box.
- **Good UX:** The user presses "Next", and the cursor instantly jumps to the "Password" box. When they finish the password, they press "Done", and the keyboard hides or submits the form.

### **3. How It Works**

#### **A. The `FocusRequester**`

To move focus effectively, you need a handle on the component you want to focus _on_.

- You create a `FocusRequester` object.
- You attach it to a TextField using `.modifier.focusRequester(ref)`.
- You call `ref.requestFocus()` when you want to jump there.

#### **B. The `FocusManager**`

This is a system service you can grab via `LocalFocusManager.current`.
It has helper methods like:

- `moveFocus(FocusDirection.Down)`: Automatically finds the next field below.
- `clearFocus()`: Hides the keyboard and removes cursor from everything.

### **4. Example: The Two-Field Login Form**

This example shows how pressing "Next" on the Username field jumps to the Password field.

```kotlin
@Composable
fun LoginForm() {
    // 1. Create references to control focus
    val passwordFocusRequester = remember { FocusRequester() }
    val focusManager = LocalFocusManager.current

    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Column {
        // Field 1: Username
        OutlinedTextField(
            value = username,
            onValueChange = { username = it },
            label = { Text("Username") },
            // A. Configure the Keyboard Button to be "Next"
            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
            // B. Define what happens when "Next" is clicked
            keyboardActions = KeyboardActions(
                onNext = {
                    // Jump to the password field specifically
                    passwordFocusRequester.requestFocus()
                }
            )
        )

        Spacer(modifier = Modifier.height(8.dp))

        // Field 2: Password
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            modifier = Modifier
                // C. Attach the reference so we can find this field later
                .focusRequester(passwordFocusRequester),

            // D. Configure Keyboard to be "Done"
            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
            keyboardActions = KeyboardActions(
                onDone = {
                    // Hide keyboard and clear focus
                    focusManager.clearFocus()
                    // TODO: triggerLogin()
                }
            )
        )
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`FocusRequester`, `LocalFocusManager`, IME Actions (`ImeAction.Next`), `KeyboardActions`, `requestFocus()`, Accessibility flow.

**Interview Speak Paragraph**

> "To create a seamless form experience in Compose, I rely on `FocusRequester` and `KeyboardActions`. Instead of forcing users to manually tap each field, I configure the `KeyboardOptions` to show the 'Next' action on intermediate fields. In the `onNext` callback, I use a `FocusRequester` attached to the subsequent field to programmatically call `requestFocus()`, moving the cursor automatically. For the final field, I use `ImeAction.Done` and call `LocalFocusManager.current.clearFocus()` to close the keyboard, ensuring the input flow feels native and efficient."

---

**Next Step:**
Text is easy, but what about dates, times, and dropdowns?
Ready for **Topic 6.3: Pickers & Menus**? We'll look at the complex input widgets.

---

## Navigation

â† Previous
Next â†’
