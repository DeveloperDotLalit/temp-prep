---
layout: default
title: Mvvm Triangle
parent: Phase1
nav_order: 3
---

Here are your focused notes on **The MVVM Triangle (Model - View - ViewModel)**.

---

### **Topic: The MVVM Triangle (Model - View - ViewModel)**

#### **What It Is**

MVVM is a specific architectural pattern used to implement the "Separation of Concerns" in Android. It breaks your application into three distinct pieces, forming a triangle of responsibility:

1. **Model (The Data):** This represents the _truth_. It includes your database tables, API responses, and data objects (like a `User` class). It is blind to the UI.
2. **View (The UI):** This is the face of the app (Activity, Fragment, or Jetpack Compose). Its **only** job is to display data on the screen and capture user clicks. It is "dumb" because it doesn't make decisions.
3. **ViewModel (The Brain):** This is the middleman. It holds the data for the View and processes logic. It takes data from the Model and prepares it for the View.

#### **Why It Exists**

It exists to solve two huge problems:

1. **Decoupling:** We don't want the View to talk directly to the Database. If the View handles data, changing the UI might break the data logic.
2. **Data Survival:** In Android, if you rotate the screen, the Activity (View) is destroyed. If the data is inside the View, it is lost. The **ViewModel** lives outside the View, so the data survives the rotation.

#### **How It Works (The Reactive Flow)**

The magic of MVVM is that the View **observes** the ViewModel. It's like a subscriber watching a YouTube channel.

1. **User Action:** The user clicks a button in the **View**.
2. **Pass to Brain:** The View calls a function in the **ViewModel** (e.g., `viewModel.loadUser()`).
3. **Fetch Data:** The ViewModel asks the **Model** (Repository) for data.
4. **Update State:** The Model returns data, and the ViewModel updates its internal variable (like `_userState.value = newUser`).
5. **Auto-Update:** Because the **View** is "observing" that variable, the screen updates automatically. The ViewModel never manually touches the Views (e.g., it never calls `textView.setText()`).

#### **Example (The Weather App)**

Imagine a simple screen showing the temperature.

- **Model:** A data class `Weather(temp: Int, city: String)`. It knows nothing about screens.
- **ViewModel:** Holds a `LiveData` or `StateFlow` variable called `currentWeather`. It has a function `fetchWeather()` that gets data from the Model and updates the variable.
- **View (Activity):**
- It does **not** say: "Hey Textview, update yourself."
- It says: "Hey ViewModel, I am watching `currentWeather`. Whenever it changes, I will update the screen automatically."

```kotlin
// 1. Model: Just data
data class Weather(val temp: String)

// 2. ViewModel: The State Holder
class WeatherViewModel : ViewModel() {
    // This is the "Live" data the View watches
    val weatherState = MutableLiveData<Weather>()

    fun loadWeather() {
        // Imaginary call to Model
        val newWeather = Weather("25°C")
        weatherState.value = newWeather // Updates the state
    }
}

// 3. View: The Observer
class WeatherActivity : AppCompatActivity() {
    val viewModel = WeatherViewModel()

    fun onCreate() {
        // Start Observing
        viewModel.weatherState.observe(this) { weather ->
            // This runs automatically whenever data changes
            myTextView.text = weather.temp
        }

        button.setOnClickListener { viewModel.loadWeather() }
    }
}

```

#### **Interview Keywords**

State Holder, Observer Pattern, Decoupling, Unidirectional Data Flow, LiveData / StateFlow, Lifecycle Aware, Separation of Concerns.

#### **Interview Speak Paragraph**

> "I prefer MVVM because it clearly separates the UI from the business logic. The ViewModel acts as a state holder that survives configuration changes, while the View remains 'dumb,' only responsible for observing that state and rendering it. This makes the code easier to test because I can verify the logic in the ViewModel without needing an emulator."

---

**Would you like to proceed to the next topic: "Lifecycle Awareness"?**
