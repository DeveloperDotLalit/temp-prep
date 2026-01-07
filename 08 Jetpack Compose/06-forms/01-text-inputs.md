---
layout: default
title: Text Inputs
parent: 6. Forms, Inputs & Sheets
nav_order: 1
---

# Text Inputs

Here are your notes for **Topic 6.1**.

---

# Topic 6: Forms, Inputs & Sheets

## **Topic 6.1: Text Inputs**

### **1. What It Is**

Text Inputs allow users to type data into your app. In Compose, there are two main visual styles provided by Material Design:

- **`TextField`:** A box with a filled background and an underline (High emphasis).
- **`OutlinedTextField`:** A box with a border and a transparent background (Medium emphasis, standard for forms).

### **2. Why It Exists (The "State" Trap)**

In the old XML View system, an `EditText` handled its own state. You typed "A", and the view updated itself to show "A".
**In Compose, TextFields are stateless.**

- **The Trap:** If you just write `TextField(value = "Hello", onValueChange = {})`, and try to type, **nothing happens**.
- **The Reason:** You told the TextField the value is "Hello". When you typed "A", you didn't tell it to change the value. It listened to you, but you kept feeding it "Hello".
- **The Fix:** You must use **State Hoisting**. You hold the variable, and when the user types, you update the variable.

### **3. How It Works**

#### **A. Controlling the Keyboard (`KeyboardOptions`)**

You don't want a full text keyboard when asking for a PIN code.

- **`keyboardType`:** Sets the keys shown (Number, Email, Phone, Password).
- **`imeAction`:** Sets the "Enter" button icon/behavior (Next, Done, Search, Send).

#### **B. Visual Transformation**

This separates **Data** from **Display**.

- **Data:** The actual string in memory ("1234").
- **Display:** What the user sees ("\*\*\*\*").
- **Use Cases:** Passwords (`PasswordVisualTransformation`), Credit Card grouping (adding spaces every 4 digits), or Phone numbers.

### **4. Example: A Secure Password Field**

This example combines all three concepts: Style, Keyboard Type, and Visual Transformation.

```kotlin
@Composable
fun PasswordInput() {
    // 1. STATE: We hold the text here.
    var password by remember { mutableStateOf("") }
    var isVisible by remember { mutableStateOf(false) }

    OutlinedTextField(
        // 2. BINDING: UI reflects the state
        value = password,
        onValueChange = { password = it }, // Update state when user types
        label = { Text("Password") },

        // 3. KEYBOARD: Show numbers/symbols + "Done" checkmark
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Password,
            imeAction = ImeAction.Done
        ),

        // 4. TRANSFORMATION: Hide text unless isVisible is true
        visualTransformation = if (isVisible) VisualTransformation.None else PasswordVisualTransformation(),

        // 5. ICON: Toggle visibility
        trailingIcon = {
            IconButton(onClick = { isVisible = !isVisible }) {
                val icon = if (isVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff
                Icon(icon, contentDescription = "Toggle Password")
            }
        }
    )
}

```

### **5. Interview Prep**

**Interview Keywords**
State Hoisting, `onValueChange`, `VisualTransformation`, `KeyboardOptions`, IME Actions, Stateless Widget.

**Interview Speak Paragraph**

> "In Compose, TextFields are strictly controlled components, meaning they do not hold their own state. To make a text field editable, I must hoist the state—creating a variable using `remember` and updating it inside the `onValueChange` callback. For user experience, I always configure the `KeyboardOptions` to match the input type (like `Number` or `Email`) and define the appropriate IME action (like 'Next' or 'Done'). Finally, for sensitive or formatted data, I use `VisualTransformation` to alter how the text renders—such as masking characters for passwords—without changing the actual underlying data string."

---

**Next Step:**
The user has typed "Hello", but how do they move to the next box without tapping it?
Ready for **Topic 6.2: Keyboard Actions & Focus Management [Added]**? This is the difference between a clunky form and a smooth one.

---

## Navigation

Next â†’
