---
layout: default
title: R8 & ProGuard
parent: 12. Performance & Internals
nav_order: 4
---

# R8 & ProGuard

Here are your notes for **Topic 10.7**.

---

## **Topic 10.7: R8 & ProGuard**

### **1. What It Is**

- **ProGuard:** The legacy tool used for code shrinking and obfuscation.
- **R8:** The modern, default compiler from Google that replaces ProGuard. It is faster and integrates directly into the Android build process (specifically the D8 dexer).
- **The Connection:** R8 uses the **same rules files** (`proguard-rules.pro`) as ProGuard. So, we still write "ProGuard Rules," but R8 is the engine executing them.

### **2. Why It Exists (Size & Security)**

1. **Shrinking (Tree Shaking):** It detects unreachable code. If you include a huge library but only use one function, R8 deletes the rest of the library from your APK.
2. **Obfuscation:** It renames classes and methods to short, meaningless names (e.g., `UserRepository` becomes `a.b.c`). This makes reverse engineering harder and reduces the `classes.dex` file size.
3. **Optimization:** It rewrites code to be more efficient (e.g., inlining functions, removing unused variables).

### **3. How It Works**

R8 starts at the "Entry Points" of your app (Activities, Services, Manifest entries). It traces every function call like a spiderweb.

- **Mark:** "I use `MainActivity`, so keep it." -> "MainActivity calls `LoginVM`, so keep that."
- **Sweep:** Anything _not_ touched by the spiderweb is deleted.

### **4. The Danger Zone (Reflection & Serialization)**

R8 is aggressive. It deletes anything it thinks is unused.

- **The Crash:** If you use **Reflection** (looking up a class by its String name) or **JSON Parsing** (GSON/Moshi looking for field names matching JSON keys), R8 doesn't see a direct code reference.
- **Result:** It deletes or renames your data class fields. The JSON parser fails to find `userName` because R8 renamed it to `a`.

### **5. Keeping Rules (The Fix)**

You must tell R8: "Do not touch this specific class!"

#### **A. The `@Keep` Annotation (Preferred)**

Add `@Keep` to the specific class or function.

```kotlin
@Keep // Tells R8: Keep this class and its name exactly as is.
data class UserJson(
    val id: String,
    val name: String
)

```

#### **B. The `proguard-rules.pro` File**

Used for third-party libraries where you can't add annotations.

```proguard
# Keep all classes in the model package
-keep class com.myapp.data.model.** { *; }

# Keep specific Retrofit interfaces
-keep interface retrofit2.** { *; }

```

### **6. Example: Enabling It**

In your `build.gradle.kts`:

```kotlin
android {
    buildTypes {
        release {
            // 1. Turn on R8
            isMinifyEnabled = true
            // 2. Turn on Resource Shrinking (removes unused images)
            isShrinkResources = true

            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}

```

### **7. Interview Prep**

**Interview Keywords**
R8 vs ProGuard, Minification, Tree Shaking, Obfuscation, Reflection crashes, `@Keep`, Mapping File (for de-obfuscating stack traces), `isMinifyEnabled`.

**Interview Speak Paragraph**

> "In production builds, I enable `isMinifyEnabled` to utilize R8 for code shrinking and obfuscation. While this significantly reduces APK size and adds a layer of security, it introduces risks for code relying on reflection, such as GSON serialization or Retrofit. R8 might rename or remove fields that aren't explicitly referenced in the code path. To prevent runtime crashes, I proactively add `@Keep` annotations to my DTOs (Data Transfer Objects) and maintain a clean `proguard-rules.pro` file for third-party libraries that rely on introspection. I also ensure the `mapping.txt` file is uploaded to the Play Console so I can read de-obfuscated crash reports."

---

**This concludes the core technical notes.**

You now have a complete set of notes covering the lifecycle of an Android App:

1. **Architecture:** MVVM, Clean Architecture.
2. **UI:** Compose, Layouts, Graphics.
3. **Data:** Room, Retrofit, Paging.
4. **Performance:** Stability, R8, Startup.
5. **Quality:** Testing, Interoperability.

**Would you like me to:**

1. **Compile all these topics into a single downloadable PDF?**
2. **Start a "Mock Interview" session** where I ask you questions based on these notes?

---

## Navigation

â† Previous
