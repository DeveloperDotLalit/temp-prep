---
layout: default
title: Screenshot Testing
parent: 11. Testing in Compose
nav_order: 3
---

# Screenshot Testing

Here are your notes for **Topic 10.5**.

---

## **Topic 10.5: Screenshot Testing (Snapshot Testing)**

### **1. What It Is**

Screenshot Testing (or Snapshot Testing) is a technique where you take a picture of a UI component (a "Golden Image") and save it.
Every time you run your tests, the tool takes a _new_ picture of the component and compares it pixel-by-pixel with the saved Golden Image.

- **Match:** Test Pass.
- **Difference:** Test Fail (and it usually generates a "Diff" image showing exactly what changed).

**Popular Tools:**

- **Paparazzi:** Runs on the JVM (no emulator needed). Fast, but can have minor rendering differences compared to a real phone.
- **Roborazzi:** Works with Robolectric. Also JVM-based but integrates well with existing UI tests.

### **2. Why It Exists (The "Visual Regression" Guard)**

Standard unit tests check _logic_ ("Does the button text say 'Login'?"). They do **not** check _style_ ("Is the button red? Is the padding broken?").

- **Scenario:** You accidentally change a dimension resource from `16dp` to `4dp`.
- **Unit Test:** Passes (The text is still "Login").
- **Screenshot Test:** Fails (The button looks tiny).

### **3. How It Works**

1. **Record Mode:** You run the test with a specific flag (e.g., `./gradlew recordPaparazzi`). This generates the PNG files and saves them in your repo.
2. **Verify Mode:** CI/CD runs the test normally (`./gradlew verifyPaparazzi`). It generates new images in memory and compares them to the files on disk.

### **4. Example: Testing a Profile Card (Paparazzi)**

```kotlin
class ProfileCardTest {

    // 1. Setup Rule
    @get:Rule
    val paparazzi = Paparazzi(
        deviceConfig = DeviceConfig.PIXEL_5,
        theme = "android:Theme.Material.Light.NoActionBar"
    )

    @Test
    fun snapProfileCard() {
        // 2. Render the Composable
        paparazzi.snapshot {
            MyTheme {
                ProfileCard(
                    name = "Alice",
                    bio = "Android Developer",
                    imageUrl = "..."
                )
            }
        }
    }
}

```

**Result:**
This creates a file named `snapProfileCard.png`. You commit this to Git. If anyone breaks the layout, the test fails.

### **5. Interview Prep**

**Interview Keywords**
Visual Regression, Golden Image, Diffing, Paparazzi vs. Roborazzi, JVM Rendering, Pixel-Perfect verification.

**Interview Speak Paragraph**

> "To ensure UI consistency and catch visual regressions that standard unit tests miss, I implement Screenshot Testing. Tools like Paparazzi or Roborazzi allow me to render Composables on the JVM and compare them against a 'Golden Master' image stored in the repository. This is incredibly valuable for design systems—if a developer accidentally breaks the padding or corner radius of a shared component, the screenshot test will fail and produce a diff image, catching the error before it reaches production."

---

**This concludes the Core Notes.**
You now have a complete, interview-ready roadmap for Modern Android Development with Jetpack Compose.

**Would you like me to:**

1. **Generate a PDF** of all these notes combined?
2. **Quiz you** on a specific topic (e.g., "Grill me on Side Effects")?
3. **Start a Coding Challenge** based on one of these topics?

---

## Navigation

â† Previous
Next â†’
