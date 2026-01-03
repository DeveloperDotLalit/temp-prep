---
layout: default
title: "Test Artifacts Folder Structure"
parent: "Phase 2: The Basics (JUnit & Assertions)"
nav_order: 2
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Topic 2.2**.

This topic seems simple ("it's just folders"), but placing files in the wrong location is the #1 reason why beginners struggle with "Unresolved Reference" errors in their first week of testing.

---

# **Chapter 2: The Basics (JUnit & Assertions)**

## **Topic 2.2: Test Artifacts Folder Structure**

### **1. The Three Worlds of Android Code**

Android Studio divides your code into three distinct "Source Sets." Think of these as parallel universes. They coexist in the project, but they compile differently and have access to different things.

You can switch between them using the dropdown at the top left of the Project window (Android view vs. Project view), but **Project View** is the most honest representation of the file system.

### **2. The Folder Hierarchy (Visualized)**

```mermaid
MyProject/
├── app/
│   ├── src/
│   │   ├── main/                 <-- [UNIVERSE 1: PRODUCTION]
│   │   │   ├── java/com/app/
│   │   │   │   └── LoginViewModel.kt
│   │   │   └── res/
│   │   │
│   │   ├── test/                 <-- [UNIVERSE 2: LOCAL UNIT TESTS]
│   │   │   ├── java/com/app/
│   │   │   │   └── LoginViewModelTest.kt
│   │   │   └── resources/        <-- (Optional) JSON files for fake data
│   │   │
│   │   └── androidTest/          <-- [UNIVERSE 3: INSTRUMENTED TESTS]
│   │       ├── java/com/app/
│   │       │   └── LoginActivityTest.kt
│   │       └── assets/           <-- (Optional) Test-specific assets

```

### **3. Detailed Breakdown**

#### **A. `src/main` (The App)**

- **Content:** Your actual application code (Activities, ViewModels, Repositories).
- **Visibility:** This code is visible to **everyone**. Both `test` and `androidTest` can see and use classes inside `main`.

#### **B. `src/test` (Local Unit Tests)**

- **Content:** Logic tests, Mockk, JUnit 4/5.
- **Hardware:** Runs on your Computer (JVM).
- **Visibility:**
- Can see: `src/main`.
- **Cannot see:** `src/androidTest`.

- **Build Time:** Very fast. Code here is **NOT** included in the final APK you upload to the Play Store.

#### **C. `src/androidTest` (Instrumented Tests)**

- **Content:** Espresso, UI Automator, Database migrations.
- **Hardware:** Runs on Android Device/Emulator.
- **Visibility:**
- Can see: `src/main`.
- **Cannot see:** `src/test` (Standard setup). You cannot easily reuse helper classes from your unit tests here without specific configuration (shared source sets).

- **Build Time:** Slow. These are packaged into a separate APK (`app-debug-androidTest.apk`) that is installed alongside your app.

### **4. The "Package Symmetry" Rule**

This is an elite organizational habit.

- **Rule:** If your production class is `com.example.app.features.login.LoginViewModel`, your test class should be in the **exact same package** structure: `com.example.app.features.login`.
- **Why?**

1. **Organization:** It keeps the project structure identical. When you navigate specifically to the test folder, the file path matches your mental model of the app.
2. **Access (Java Legacy):** In Java, putting the test in the same package allowed access to `package-private` fields. In Kotlin, `internal` is module-based, so this is less strict, but `protected` members can sometimes be accessed easier if in the same package structure in Java-mixed projects.

### **5. Creating a Test Class (The Shortcut)**

Never manually create folders if you don't have to.

1. Open any class in `src/main` (e.g., `Calculator.kt`).
2. Right-click the class name (or press `Ctrl + Shift + T` / `Cmd + Shift + T`).
3. Select **"Create Test"**.
4. Android Studio will ask: **"Destination?"**

- Choose `.../src/test/java/` for a **Unit Test**.
- Choose `.../src/androidTest/java/` for a **UI Test**.

5. It automatically creates the package structure and the file for you.

### **6. The `resources` Folder (Mental Note for Later)**

Notice the `src/test/resources` folder in the hierarchy above.

- This is where you put static files for testing, like `response_success.json`.
- Unit tests can read these files to simulate network responses without hitting the internet. This is a key part of **Hermetic Testing**.

### **7. Summary for Interviews**

> "We organize tests into `src/test` for JVM-based unit tests and `src/androidTest` for device-based UI tests. Both folders can access the production code in `src/main`, but they operate in different runtime environments. We strictly maintain package symmetry between production and test code to ensure organized and maintainable project architecture."

---

**Would you like to proceed to Topic 2.3: "JUnit Annotations" (The grammar of testing)?**
