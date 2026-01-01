---
layout: default
title: **Chapter 8: Scenario-Based Solutions**
parent: Phase8
nav_order: 6
grand_parent: Unit & UI Testing
---

Here are your in-depth study notes for **Phase 8, Scenario 6**.

This is common in "Hybrid" apps or apps that offload complex flows (like Checkout or Help Centers) to the web.

---

# **Chapter 8: Scenario-Based Solutions**

## **Scenario 6: Testing WebViews**

### **1. The Interview Question**

> **"Our app uses a WebView for the 'Terms of Service' and 'Checkout' screens. The buttons inside are HTML elements (`<button id="submit">`), not Android Views. Standard Espresso cannot see them. How do you automate a test that clicks the HTML Submit button and verifies the native app reacts correctly?"**

### **2. The Problem: The "Black Box"**

To standard Espresso, a `WebView` is just one giant view. It sees the container, but it **cannot** see the DOM (Document Object Model) inside.

- `onView(withId(R.id.my_webview))` -> **Found.**
- `onView(withId("submit_button_html_id"))` -> **Fail.**

### **3. The Solution: `Espresso-Web**`

Google provides a dedicated library that bridges this gap. It wraps **WebDriver Atoms** (the same tech used in Selenium) to inject JavaScript into the WebView and manipulate the HTML.

**Dependency:**

```kotlin
androidTestImplementation("androidx.test.espresso:espresso-web:3.5.1")

```

### **4. The Syntax (Web-Specific)**

Espresso-Web introduces a new entry point: `onWebView()`.
It follows a similar chain but with different atoms.

1. **Find:** `onWebView().withElement(findElement(Locator.ID, "html_id"))`
2. **Act:** `.perform(webClick())`
3. **Check:** `.check(webMatches(getText(), containsString("Success")))`

### **5. The Code Solution**

**Prerequisite:** Ensure JavaScript is enabled in your WebView setup.

```kotlin
// Import the Web interactions
import androidx.test.espresso.web.sugar.Web.onWebView
import androidx.test.espresso.web.webdriver.DriverAtoms.findElement
import androidx.test.espresso.web.webdriver.DriverAtoms.webClick
import androidx.test.espresso.web.webdriver.Locator

@Test
fun testWebView_loginFlow() {
    // 1. Initial Setup
    // Start the activity containing the WebView
    ActivityScenario.launch(WebViewActivity::class.java)

    // 2. Interact with HTML Input (Username)
    onWebView()
        .forceJavascriptEnabled() // Crucial if your test runs before the page loads fully
        .withElement(findElement(Locator.ID, "username_field")) // HTML ID
        .perform(driverAtoms.webKeys("user123"))

    // 3. Interact with HTML Input (Password)
    onWebView()
        .withElement(findElement(Locator.CSS_SELECTOR, ".password-class")) // CSS Selector
        .perform(driverAtoms.webKeys("secret"))

    // 4. Click HTML Button
    onWebView()
        .withElement(findElement(Locator.ID, "submit_btn"))
        .perform(webClick())

    // 5. Verify Result (Hybrid)
    // After clicking submit, the WebView might redirect, OR it might close and show Native UI.

    // Option A: Verify Web Content changed
    onWebView()
        .withElement(findElement(Locator.TAG_NAME, "h1"))
        .check(webMatches(driverAtoms.getText(), containsString("Welcome")))

    // Option B: Verify Native UI appeared (Bridge crossed)
    onView(withText("Login Successful")) // This is a Native TextView
        .check(matches(isDisplayed()))
}

```

### **6. Advanced: Testing the JavaScript Bridge (`@JavascriptInterface`)**

If your web page calls a native function (e.g., `Android.onPaymentSuccess()`), you verify this using **Mockito**.

1. Inject a Spy/Mock object into the WebView as the JavascriptInterface.
2. Perform the web click.
3. Verify the Spy method was called.

```kotlin
@Test
fun testJsBridge_callsNativeMethod() {
    // Inject the spy bridge
    val spyBridge = spyk(MyJsBridge())
    webView.addJavascriptInterface(spyBridge, "Android")

    // Click the HTML button that calls 'Android.doSomething()'
    onWebView().withElement(...).perform(webClick())

    // Verify Native code was triggered
    verify { spyBridge.doSomething() }
}

```

### **7. Summary for Interviews**

> "For Hybrid screens, standard Espresso view matchers don't work because the content is HTML, not native Views. I use the **Espresso-Web** library to solve this.
> Using `onWebView()`, I can locate DOM elements using standard Web Locators like ID, CSS Selectors, or XPath. I use WebDriver Atoms to drive interactions like `webClick()` or `webKeys()`. This allows me to fill out HTML forms and assert that the web page state changes or that the correct callback is sent to the Native app via the `@JavascriptInterface` bridge."

---

**Would you like to proceed to the final Scenario (7): "Testing File Uploads" (Mocking the Content Resolver)?**
