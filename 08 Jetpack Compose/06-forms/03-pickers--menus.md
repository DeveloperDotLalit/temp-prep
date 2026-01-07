---
layout: default
title: Pickers & Menus
parent: 6. Forms, Inputs & Sheets
nav_order: 3
---

# Pickers & Menus

Here are your notes for **Topic 6.3**.

---

## **Topic 6.3: Pickers & Menus**

### **1. What It Is**

These are the standard UI components for selecting specific values from a set.

- **`DatePicker` / `TimePicker`:** Modal dialogs for selecting dates and times without typing them manually.
- **`ExposedDropdownMenuBox`:** The Material Design version of a "Spinner" or "Combo Box." It looks like a TextField but opens a list of options when clicked.

### **2. Why It Exists (Validation & Space)**

- **Validation:** Asking a user to type a date is dangerous. Did they type "01/02/2023" (US format) or "02/01/2023" (EU format)? Pickers force a standardized input.
- **Space:** You can't list 50 countries as Radio Buttons. A Dropdown hides the list until needed, saving massive screen space.

### **3. How It Works**

#### **A. Date & Time Pickers (State Driven)**

Material 3 introduced new, powerful states for these.

- **The State:** You must create a `DatePickerState` or `TimePickerState` using `remember...`. This holds the selection.
- **The Dialog:** The picker is usually wrapped in a generic `DatePickerDialog` (which provides the "OK/Cancel" buttons).
- **Epoch Time:** **Warning!** `DatePicker` works with `Long` (milliseconds since 1970), not `LocalDate`. You often need to convert back and forth.

#### **B. TimePicker Modes**

- **Dial:** The classic clock face. Good for visual browsing.
- **Input:** Text boxes for Hour/Minute. Better for accessibility and power users who know exactly what time they want.

#### **C. Exposed Dropdown (The "Spinner")**

This is a composite component.

1. **The Box:** Wraps everything (`ExposedDropdownMenuBox`).
2. **The Anchor:** The `TextField` that shows the current choice. It is usually `readOnly = true` so the keyboard doesn't pop up.
3. **The Menu:** The `ExposedDropdownMenu` containing `DropdownMenuItem`s.

### **4. Example: The Dropdown Menu**

Implementing a "Select Coffee" dropdown. Note the use of `expanded` state.

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CoffeeDropdown() {
    val coffees = listOf("Latte", "Espresso", "Cappuccino")
    var expanded by remember { mutableStateOf(false) }
    var selectedOption by remember { mutableStateOf(coffees[0]) }

    // 1. The Wrapper
    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { expanded = !expanded } // Toggle open/close
    ) {
        // 2. The Anchor (The Text Field)
        TextField(
            value = selectedOption,
            onValueChange = {},
            readOnly = true, // Disable keyboard
            label = { Text("Choose Coffee") },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
            modifier = Modifier.menuAnchor() // REQUIRED: Tells Compose this connects to the menu
        )

        // 3. The List of Options
        ExposedDropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false } // Close when clicking outside
        ) {
            coffees.forEach { coffee ->
                DropdownMenuItem(
                    text = { Text(coffee) },
                    onClick = {
                        selectedOption = coffee
                        expanded = false // Close after selection
                    }
                )
            }
        }
    }
}

```

### **5. Interview Prep**

**Interview Keywords**
`DatePickerState`, Epoch Millis, `ExposedDropdownMenuBox`, `menuAnchor`, `readOnly` TextField, Modal vs. Input Mode, `ExperimentalMaterial3Api`.

**Interview Speak Paragraph**

> "For user input involving specific formats like dates or predefined lists, I stick to Material 3 components. For dates, I use `DatePickerDialog` combined with `rememberDatePickerState`. It's important to remember that this API works with Epoch milliseconds, so I always handle the conversion to `LocalDate` carefully. For dropdowns, I use the `ExposedDropdownMenuBox`. It replaces the old Spinner logic by combining a read-only `TextField` as an anchor with an `ExposedDropdownMenu`. This setup gives full control over the expansion state and allows for custom item styling that standard spinners lacked."

---

**Next Step:**
We have inputs, but how do we show complex content that slides up from the bottom?
Ready for **Topic 6.4: Bottom Sheets**? This is the modern replacement for many dialogs.

---

## Navigation

â† Previous
Next â†’
