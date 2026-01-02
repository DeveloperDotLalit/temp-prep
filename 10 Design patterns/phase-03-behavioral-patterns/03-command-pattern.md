---
layout: default
title: "Command Pattern"
parent: "Phase 3: Behavioral Patterns"
nav_order: 3
---

# Command Pattern

### **Command Pattern: The "Remote Control" Pattern**

Think of the **Command Pattern** like a **Universal Remote Control**. You have buttons for "Power On," "Volume Up," and "Mute." The remote doesn't know _how_ the TV turns on or _how_ the speaker increases volume. It just holds a "command" (the button) that tells the device to do its job. Because each button is an object, you can even record a "Macro" (a list of commands) to turn on the TV, dim the lights, and start the DVD player all with one click.

---

### **1. What It Is**

The **Command Pattern** is a behavioral design pattern that turns a request or an action into a **stand-alone object**. This object contains all the information needed to perform the action (the method to call, the arguments, and the object that owns the method).

In Android, this is the secret sauce behind **Undo/Redo** functionality and how systems like **WorkManager** or **Intent Services** queue up tasks to be executed later.

---

### **2. Why It Exists (The Problem it Solves)**

Imagine you are building a **Photo Editor** with many buttons: Crop, Rotate, and Brightness.

- **The Problem:** If the "Rotate" button has the rotation logic hardcoded inside its `onClick` listener, it becomes very hard to:

1. **Undo the action:** The button doesn't "remember" what it did.
2. **Queue actions:** You can't save a list of "things to do" to run in the background.
3. **Reuse logic:** If you want a "Menu Item" to do the same thing as the "Button," you have to copy-paste the code.

- **The Solution:** You create a `RotateCommand` object. When the button is clicked, it just says: `command.execute()`. Because it's an object, you can store it in a **Stack** (a list). To "Undo," you just pop the last command from the stack and call `command.undo()`.

**Key Benefits:**

- **Decoupling:** The object that _triggers_ the command (the Button) is separate from the object that _knows how_ to do the work (the Logic).
- **Undo/Redo:** Since actions are objects, you can keep a history of them.
- **Deferred Execution:** You can create a command now but run it later (useful for offline syncing or background tasks).

---

### **3. How It Works**

1. **The Command Interface:** Usually has an `execute()` method (and optionally `undo()`).
2. **The Concrete Command:** Implements the interface and links the "Receiver" (the logic) to the action.
3. **The Receiver:** The class that actually does the heavy lifting (e.g., the `ImageLibrary` that rotates the pixels).
4. **The Invoker:** The object that triggers the command (e.g., a `Button` or a `Timer`).

---

### **4. Example (Practical Android/Kotlin)**

#### **The Scenario: A Smart Home App (Light Control with Undo)**

```kotlin
// 1. The Command Interface
interface Command {
    fun execute()
    fun undo()
}

// 2. The Receiver (The logic)
class Light {
    fun turnOn() = println("Light is ON 💡")
    fun turnOff() = println("Light is OFF 🌑")
}

// 3. Concrete Command for "ON"
class LightOnCommand(private val light: Light) : Command {
    override fun execute() = light.turnOn()
    override fun undo() = light.turnOff()
}

// 4. The Invoker (The Remote Control)
class RemoteControl {
    private val history = mutableListOf<Command>()

    fun pressButton(command: Command) {
        command.execute()
        history.add(command) // Save for undo
    }

    fun pressUndo() {
        if (history.isNotEmpty()) {
            val lastCommand = history.removeAt(history.size - 1)
            lastCommand.undo()
        }
    }
}

// --- HOW TO USE IT ---
fun main() {
    val livingRoomLight = Light()
    val remote = RemoteControl()

    val turnOn = LightOnCommand(livingRoomLight)

    remote.pressButton(turnOn) // Output: Light is ON
    remote.pressUndo()         // Output: Light is OFF
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
[ Invoker (Button) ] --calls--> [ Command Object ] --triggers--> [ Receiver (Logic) ]
        |                              |                           |
        | (Doesn't know logic)         | (Encapsulates request)    | (Performs work)
        v                              v                           v
   "Button Clicked" --------> "Execute Rotate" ---------> "Update Image Pixels"

```

---

### **6. Interview Keywords**

- **Encapsulation of a Request:** Turning an action into an object.
- **Invoker vs. Receiver:** Separating the "trigger" from the "logic."
- **Callback Replacement:** A more powerful way to handle events than simple callbacks.
- **Undo/Redo Stack:** Storing commands to reverse actions.
- **WorkManager/JobScheduler:** Real-world Android examples of queuing commands.

---

### **7. Interview Speak Paragraph**

> "The Command Pattern is a behavioral design pattern that encapsulates a request as an object, thereby letting us parameterize clients with different requests, queue or log requests, and support undoable operations. In Android, it’s particularly useful for decoupling UI components from the business logic. For instance, when implementing an 'Undo' feature or managing background tasks with `WorkManager`, we treat each action as a command object. This way, the component triggering the action doesn't need to know the implementation details, making the code more modular, testable, and flexible for complex task scheduling."

---

### **Interview "Pro-Tip" (The "Android Internal" Question)**

An interviewer might ask: **"Where do we see the Command pattern in the Android Framework?"**

- **Your Answer:** "We see it in **`Runnable`** and **`Thread`**. When you pass a `Runnable` (the Command) to a `Thread` (the Invoker), the thread doesn't know what's inside the `run()` method; it just executes it. We also see it in **`Intent`** services, where an `Intent` acts as a command object that tells a background service what task to perform."

---

**Would you like to move to the final Behavioral Pattern—the State Pattern—or are you ready to start Phase 4: Architectural Patterns (MVC, MVP, MVVM)?**

---

[â¬… Back to Phase](../) | [Next âž¡](../)
