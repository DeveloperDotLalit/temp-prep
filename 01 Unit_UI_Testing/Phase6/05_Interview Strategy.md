---
layout: default
title: **Chapter 6: The Elite Level (System & Architecture)**
parent: Phase6
nav_order: 5
---

Here are your in-depth study notes for **Topic 6.5**.

This is the "Soft Skills" section of technical testing. In a Senior/Lead interview, knowing _how_ to write code is expected; knowing _how to talk about problems_ is what gets you hired.

---

# **Chapter 6: The Elite Level (System & Architecture)**

## **Topic 6.5: Interview Strategy & Tricky Questions**

### **Question 1: "How do you handle flaky tests?"**

_The Interviewer is asking:_ "Do you understand stability, CI/CD pipelines, and asynchronous synchronization?"

#### **The "Elite" Answer Structure:**

1. **Philosophy:** Start by stating that you view flakiness as a critical issue, not an annoyance. A flaky test is worse than no test because it destroys trust.
2. **Diagnosis:** Explain _why_ tests flake (Race conditions, Network, Shared State).
3. **Resolution:** Explain your toolkit (IdlingResources, Hermetic Servers).
4. **Mitigation:** Explain your process (Quarantine).

#### **Sample Response:**

> "I treat flaky tests with zero tolerance because they erode the team's trust in the CI/CD pipeline. When I encounter a flaky test, I follow a three-step process:
>
> 1. **Isolate & Reproduce:** I run the test locally 100 times in a loop to reproduce the failure.
> 2. **Identify the Root Cause:**
>
> - If it's **Network** related (timeouts), I implement **Hermetic Testing** using MockWebServer to remove the internet dependency.
> - If it's **Concurrency** related (checking UI before data loads), I ensure we are using **IdlingResources** or proper Coroutine Test Dispatchers, rather than `Thread.sleep()`.
> - If it's **Shared State** (one test affecting another), I check my `@After` teardown methods to ensure databases or Singletons are reset.
>
> 3. **Quarantine:** If I can't fix it immediately, I annotate it with `@FlakyTest` and exclude it from the blocking CI gate. A flaky test should never block a deployment, but it must be ticketed and fixed, not ignored."

---

### **Question 2: "How do you test a Singleton?"**

_The Interviewer is asking:_ "Do you understand Dependency Injection and why Global State is bad?"

#### **The Trap:**

Singletons are hard to test because they hold state across multiple tests. If Test A sets `User.instance.name = "Bob"`, Test B will see "Bob" instead of null, causing it to fail.

#### **Strategy A: The Architecture Answer (Best)**

> "Ideally, I avoid accessing Singletons directly in my classes. Instead, I inject them.
> Even if a class is a Singleton, I make it implement an interface. In my ViewModel, I ask for the Interface in the constructor, not the concrete Singleton.
> **Production:** Hilt provides the real Singleton instance.
> **Test:** I pass a `mockk<MyInterface>()`.
> By treating the Singleton as just another dependency to be injected, testing becomes trivial because I mock the behavior rather than managing the global static instance."

#### **Strategy B: The Legacy Code Answer (The "Hack")**

Sometimes you have to test old code where you can't use Hilt.

> "If I am working with legacy code where the Singleton is accessed directly via `getInstance()`, I add a helper method specifically for testing to reset its state.
> I verify the state, and then in the `@After` method, I explicitly clear the Singleton instance to ensure test isolation."

```kotlin
object MySingleton {
    private var instance: MySingleton? = null

    // The Hack: Only visible to tests
    @VisibleForTesting
    fun setInstance(newInstance: MySingleton) {
        instance = newInstance
    }

    @VisibleForTesting
    fun clear() {
        instance = null
    }
}

```

---

### **Question 3: "How do you test private methods?"**

_The Interviewer is asking:_ "Do you understand encapsulation?"

#### **The Only Correct Answer:**

> "**You don't.**
> Private methods are implementation details. We test the **Public API** (the public methods) that call those private methods. If I test a private method directly, I couple my test to the specific implementation, making refactoring impossible.
> If a private method is so complex that I feel the urge to test it in isolation, that is a 'Code Smell'. It suggests that the logic belongs in a separate helper class. I would extract that private method into a new public class (e.g., `PasswordValidator`), test that class exhaustively, and then inject it back into the original class."

---

### **Question 4: "What is 100% Code Coverage, and is it a good goal?"**

_The Interviewer is asking:_ "Are you pragmatic or dogmatic?"

#### **The "Elite" Answer:**

> "100% coverage is a vanity metric, not a quality metric. I can write a test that executes every line of code but asserts nothing, achieving 100% coverage with zero value.
> I aim for high coverage (80%+) in **Business Logic** layers (ViewModels, UseCases, Utils) because that's where the risk lies. I accept lower coverage in the UI layer (Activities/Fragments) or Glue code (Hilt Modules) because the ROI of testing those lines is low and the maintenance cost is high. I use JaCoCo to identify _untested branches_ in complex logic, not just to chase a number."

---

**This concludes the official Roadmap.**

You are now armed with the technical skills and the strategic answers to crush an Android Interview. Good luck!
