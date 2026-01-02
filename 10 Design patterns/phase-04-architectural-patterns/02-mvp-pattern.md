---
layout: default
title: "MVP Pattern"
parent: "Phase 4: Architectural Patterns"
nav_order: 2
---

# MVP Pattern

### **MVP (Model-View-Presenter): The Great Divorce**

If MVC was a messy marriage where the Activity did everything, **MVP** is the "legal divorce" that finally separates the UI from the Logic.

Think of **MVP** like a **News Broadcast**:

- **The Model (The Research Team):** They get the raw facts and data from the field.
- **The View (The News Anchor):** They look good on camera and read whatever is on the teleprompter. They don't know _if_ the news is true; they just show it.
- **The Presenter (The Producer):** They sit in the booth, talk to the research team, and tell the Anchor exactly what to say through their earpiece.

---

### **1. What It Is**

**MVP** is a derivative of MVC that focuses on making the code **Unit Testable** by moving all the decision-making logic out of the Activity and into a plain Kotlin class called the **Presenter**.

1. **Model:** Still the data layer (Room, Retrofit).
2. **View:** The Activity or Fragment. It is now "Dumb." It only handles UI (showing a progress bar, setting text) and doesn't make any decisions.
3. **Presenter:** The "Middleman." it handles the logic. It tells the View _exactly_ what to do (e.g., "Show the loading spinner now").

---

### **2. Why It Exists (The Problem it Solves)**

In MVC, the Activity (Controller) was "God." It was hard to test because it was tied to the Android Framework.

- **The Solution:** MVP uses **Interfaces** (Contracts) to talk. The Presenter doesn't know it's talking to an Activity; it just knows it's talking to "something that can show a user's name."
- **The Benefit:** You can test the Presenter using a 100% pure JUnit test on your computer without an emulator, because there is no Android code (like `Context` or `Toast`) inside it.

---

### **3. How It Works (The Contract)**

The heart of MVP is the **Contract**. This is an interface that defines the relationship:

- **View Interface:** What the UI can do (e.g., `showLoading()`, `displayUser()`).
- **Presenter Interface:** What the user can do (e.g., `onButtonClicked()`).

---

### **4. Example (The "Clean" Way)**

#### **The Contract**

```kotlin
interface UserContract {
    interface View {
        fun showLoading()
        fun hideLoading()
        fun displayUser(name: String)
    }

    interface Presenter {
        fun loadUser()
    }
}

```

#### **The Presenter (No Android code here!)**

```kotlin
class UserPresenter(private val view: UserContract.View) : UserContract.Presenter {

    private val repository = UserRepository()

    override fun loadUser() {
        view.showLoading()
        val user = repository.getUser() // Data fetch
        view.hideLoading()
        view.displayUser(user.name)
    }
}

```

#### **The View (The Activity)**

```kotlin
class UserActivity : AppCompatActivity(), UserContract.View {

    private lateinit var presenter: UserPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_user)

        presenter = UserPresenter(this)

        btnLoad.setOnClickListener { presenter.loadUser() }
    }

    override fun displayUser(name: String) {
        tvName.text = name // The Activity is just a servant to the Presenter
    }
    // ... implement showLoading / hideLoading
}

```

---

### **5. Logical Flow (Text Diagram)**

```text
User Interaction  ----> [ View (Activity) ]
                              |
                              | 1. "User clicked button"
                              v
                        [ Presenter ] <---- 2. Fetches Data ----> [ Model ]
                              |
                              | 3. "Hey View, show this name!"
                              v
                        [ View (Activity) ] ----> Updates XML UI

```

---

### **6. Interview Keywords**

- **Contract Interface:** The bridge between View and Presenter.
- **Decoupling:** Breaking the tight bond between UI and Logic.
- **Unit Testing:** The main reason people switched to MVP.
- **Dumb View:** A View that does nothing but display what it's told.
- **1-to-1 Relationship:** One Presenter usually controls exactly one View.

---

### **7. Interview Speak Paragraph**

> "MVP, or Model-View-Presenter, was designed to solve the 'God Activity' problem found in MVC by completely decoupling the business logic from the Android lifecycle. By introducing a 'Presenter' that communicates with the 'View' through an interface, we make the logic independent of the Android framework. This allows us to write pure JUnit tests for our business logic. While MVP was a massive leap forward in testability, its main drawback is that the Presenter often ends up with a lot of boilerplate code and manually manages the View's state, which is why modern Android development has largely shifted toward MVVM."

---

### **Common Interview Question**

**"What is the biggest disadvantage of MVP?"**

- **Your Answer:** "The two biggest issues are **Boilerplate** and **Lifecycle.** You have to define interfaces for every single screen, which is a lot of code. Also, the Presenter holds a reference to the View. If the Activity is destroyed (like on a screen rotation) and the Presenter is still running a background task, it can cause a **Memory Leak** or a crash if it tries to update a View that no longer exists. We have to manually handle `attachView()` and `detachView()` to stay safe."

---

**Ready to move on to the "King" of modern Android architecture: MVVM (Model-View-ViewModel)?** Or should we recap why MVP was replaced?

---

[â¬… Back to Phase](../) | [Next âž¡](../)
