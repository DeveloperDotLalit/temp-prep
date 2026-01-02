---
layout: default
title: "Cheetsheet Design Patterns"
parent: "Design Patterns in Android"
nav_order: 7
---

# Cheetsheet Design Patterns

This is your **"Interview Survival Cheat Sheet"** for Design Patterns in Android. It is designed to be a quick-glance reference you can review 10 minutes before an interview to get your terminology and "Interview Speak" perfectly aligned.

---

## **Phase 1: Creational Patterns (The Builders)**

_Focus: How we create objects efficiently._

| Pattern                  | One-Sentence Pitch                                                   | Real-World Android Example                   |
| ------------------------ | -------------------------------------------------------------------- | -------------------------------------------- |
| **Singleton**            | Ensures only one instance exists (e.g., a Database).                 | `Room.databaseBuilder`, `Retrofit` instance. |
| **Factory**              | Hides creation logic; you ask for a type, it gives an object.        | `ViewModelProvider.Factory`.                 |
| **Builder**              | Constructs complex objects step-by-step using method chaining.       | `NotificationCompat.Builder`, `AlertDialog`. |
| **Dependency Injection** | Objects receive dependencies from outside rather than creating them. | **Hilt**, **Dagger**, **Koin**.              |

---

## **Phase 2: Structural Patterns (The Organizers)**

_Focus: How classes and objects relate to each other._

| Pattern       | One-Sentence Pitch                                                 | Real-World Android Example                    |
| ------------- | ------------------------------------------------------------------ | --------------------------------------------- |
| **Adapter**   | A bridge that makes two incompatible interfaces work together.     | `RecyclerView.Adapter` (Data to UI).          |
| **Facade**    | A simplified interface that hides a complex system behind it.      | **Repository Pattern** (Hiding API/DB logic). |
| **Proxy**     | A placeholder that controls access to a heavy or sensitive object. | **Lazy loading** images or "Loading" states.  |
| **Composite** | Treating a group of objects exactly like a single instance.        | `View` vs. `ViewGroup` (Layout hierarchy).    |

---

## **Phase 3: Behavioral Patterns (The Communicators)**

_Focus: How objects talk and react to each other._

| Pattern      | One-Sentence Pitch                                                  | Real-World Android Example                       |
| ------------ | ------------------------------------------------------------------- | ------------------------------------------------ |
| **Observer** | A "YouTube Subscriber" model where data changes notify listeners.   | `LiveData`, `StateFlow`, `SharedFlow`.           |
| **Strategy** | Swapping an algorithm or behavior at runtime via an interface.      | Different **Payment Methods** or **Sort logic**. |
| **Command**  | Turning an action into an object to support Undo or Queuing.        | `WorkManager` tasks, `Runnable` in Threads.      |
| **State**    | Changing an object's behavior automatically when its state changes. | **UI States** (Loading, Success, Error).         |

---

## **Phase 4: Architecture Patterns (The Big Picture)**

_Focus: The "Skeleton" of your entire app._

- **MVC:** (Legacy) Activity does everything; leads to "God Activities."
- **MVP:** (Testing Era) Uses a **Presenter** and **Interfaces** to decouple UI from logic.
- **MVVM:** (Modern Standard) Uses **ViewModel** to survive rotations and **LiveData** to update UI.
- **MVI:** (Reactive Era) **Unidirectional Data Flow**; one single immutable State for the whole screen.

---

## **Phase 5: The "Senior" Decision Matrix (Trade-offs)**

| The Struggle                         | The "Pro" Answer                                                                                               |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Boilerplate vs. Flexibility**      | "I prefer the boilerplate of Clean Architecture because it makes the app future-proof."                        |
| **Over-engineering vs. Scalability** | "I use enough architecture to keep it testable, but I don't add layers for features that don't exist (YAGNI)." |
| **Is Singleton an Anti-pattern?**    | "Only if misused as a global variable. I prefer DI Scopes to manage 'single instances' cleanly."               |
| **Composition over Inheritance**     | "Don't use deep 'BaseActivity' chains; use helper classes and delegates instead."                              |

---

## **Final Interview "Pro-Tips"**

1. **Don't just name-drop:** Always say, _"We use the Observer pattern because..."_
2. **Mention Testing:** Design patterns exist primarily to make code **testable**. Mentioning JUnit/MockK will win you points.
3. **The "It Depends" Rule:** When asked for the "best" pattern, always start with _"It depends on the project's scale and requirements..."_

---

**You are now fully prepared!** Would you like me to turn this into a **PDF-ready text format** you can save, or do you have any last-minute questions on any specific pattern before you head into your next interview?
