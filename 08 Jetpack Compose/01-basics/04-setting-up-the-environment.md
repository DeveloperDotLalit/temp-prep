---
layout: default
title: Setting up the Environment
parent: 1. Introduction + Basic Composables
nav_order: 4
---

# Setting up the Environment

Here are your notes for **Topic 1.4**.

---

## **Topic 1.4: Setting up the Environment**

### **1. What It Is**

This topic covers the practical steps to prepare your project for Jetpack Compose. It involves configuring the Gradle build system and, most importantly, managing library versions using the **BOM (Bill of Materials)**.

### **2. Why It Exists (The "Dependency Hell" Problem)**

Compose isn't just one library; it's a collection of many (ui, material, animation, foundation, runtime, etc.).

- **The Problem:** In the early days, you had to manually set versions for each one: `ui:1.2.0`, `material:1.0.1`, `animation:1.3.0`. If you messed up and picked versions that weren't tested together, your app would crash.
- **The Solution (BOM):** The Bill of Materials is a "Version Master." You specify **one** version for the BOM (e.g., `2024.10.01`), and the BOM automatically tells Gradle which versions of the individual libraries (ui, material, etc.) are compatible with that master version.

### **3. How It Works**

**A. Android Studio Template**

- When creating a new project, choose **"Empty Activity"** (with the Compose logo).
- _Note:_ Do not choose "Empty Views Activity"—that is for the old XML system.

**B. The Gradle Setup (`build.gradle.kts`)**
You need to enable the Compose feature flag and add the dependencies.

**C. The BOM Mechanism**

1. You import the BOM using `platform(...)`.
2. You import the libraries (like `ui` or `material3`) **without** specifying a version number.
3. Gradle looks at the BOM to find the correct version.

### **4. Example: The `build.gradle.kts` (Module Level)**

```kotlin
android {
    buildFeatures {
        // 1. Enable Compose
        compose = true
    }
    composeOptions {
        // 2. Match the Compiler Extension to your Kotlin version
        kotlinCompilerExtensionVersion = "1.5.1"
    }
}

dependencies {
    // 3. The BOM (The Master Version)
    implementation(platform("androidx.compose:compose-bom:2024.09.00"))

    // 4. The Libraries (No version numbers needed here!)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")

    // Debug tools (only for debug builds)
    debugImplementation("androidx.compose.ui:ui-tooling")
}

```

### **5. Interview Prep**

**Interview Keywords**
BOM (Bill of Materials), Transitive Dependencies, Version Catalog, Kotlin Compiler Extension, Semantic Versioning.

**Interview Speak Paragraph**

> "When setting up a Compose project, the most critical best practice is using the Compose BOM (Bill of Materials). Instead of micromanaging individual versions for the UI, Material, and Animation libraries—which can lead to binary incompatibility crashes—I define a single BOM version. This ensures that all Compose dependencies are pulled in at versions that are guaranteed to work together. It simplifies upgrades and maintenance significantly."

---

**Next Step:**
Now that our environment is ready, let's start designing. Ready for **Topic 1.5: Theme, Typography, Colors, Shapes**? This is how we make the app look beautiful and consistent.

---

## Navigation

â† Previous
Next â†’
