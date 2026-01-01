---
layout: default
title: "ProjectSetup"
parent: "The Question Bank"
nav_order: 13
---

# Android Project Setup

## Tell me what things do you consider when you are going to create a new app from the scratch?

That is a broad, strategic question that an experienced developer should address by outlining a clear, phased approach that covers everything from initial discovery to final deployment preparation. This shows organizational skill and forward-thinking.

| Role/Category                         | Question                                                                                                             |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Project Initiation/Strategy**       | **What are the key considerations and steps you take when starting a new Android application project from scratch?** |
| **What the Interviewer is Expecting** | \* A structured, phased approach (Discovery, Architecture, Setup, Development).                                      |
|                                       | \* Key non-technical decisions (target audience, minimum OS version).                                                |
|                                       | \* Technical fundamentals (Build System, Architecture Pattern, Modularity).                                          |
|                                       | \* Preparation for quality and distribution (Testing, CI/CD).                                                        |

> **Proper Answer:**
> "Starting a new app is exciting because it’s the best time to establish good practices that will save hundreds of hours later. I break the process down into three major phases: **Discovery & Planning, Core Setup, and Development Standards.**
>
> ---
>
> ## 1. 🔍 Phase 1: Discovery and Strategic Planning
>
> This phase establishes the 'why' and 'who' of the app, which guides all subsequent technical decisions.
>
> - **Target Audience & Devices:**
> - **Minimum SDK (`minSdkVersion`):** Determining the lowest Android OS version we will support. This impacts which Jetpack libraries and APIs we can use. We check Play Console data for common devices if applicable.
> - **Screen Support:** Deciding if we need to support tablets, foldables, or specialized devices (TVs, Wear OS).
>
> - **Core Feature Set & Non-Functional Requirements (NFRs):**
> - What are the 3-5 absolute core user flows?
> - What are the critical NFRs (e.g., performance targets, offline support requirements, security/HIPAA compliance)?
>
> - **Monetization & Distribution:**
> - Will the app use In-App Billing (Google Play Billing Library)?
> - Do we need Dynamic Feature Modules (DFM) for modular delivery or smaller initial install size?
>
> ---
>
> ## 2. ⚙️ Phase 2: Core Technical Setup
>
> Once the requirements are clear, the next step is establishing the foundational technical stack.
>
> - **Architecture Pattern:** We implement **Clean MVVM** as the base architecture to ensure separation of concerns and testability.
> - **Build System & Modularity:**
> - **Build Tool:** Use **Gradle** with **Kotlin DSL (KTS)** for type safety.
> - **Structure:** Immediately implement a **Multi-Module Structure** (separating layers and features) to enable faster build times and strict dependency management.
> - **Dependency Management:** Set up a **Version Catalog (`libs.versions.toml`)** for centralized dependency management.
>
> - **Programming Language & UI:**
> - The primary language is **Kotlin**.
> - The UI toolkit is **Jetpack Compose** unless legacy constraints dictate otherwise.
>
> - **Core Libraries:** Integrate the core Jetpack libraries:
> - **ViewModel** and **Navigation**.
> - **Hilt/Dagger** for Dependency Injection.
> - **Retrofit/OkHttp** for networking.
> - **Room** or **DataStore** for persistence.
>
> ---
>
> ## 3. ✅ Phase 3: Quality and Automation Standards
>
> These steps ensure the app is built for quality and efficient delivery from day one.
>
> - **Testing Strategy Setup:**
> - Configure **JUnit** and **MockK** for local unit testing of the Domain and ViewModel layers.
> - Configure **Espresso** or **Compose Testing** for UI/instrumented testing.
>
> - **CI/CD Pipeline:**
> - Set up a basic CI pipeline (e.g., GitHub Actions/GitLab CI) to run checks on every pull request (Lint, Unit Tests, Code Formatting).
> - Establish secrets management for keystores and API keys.
>
> - **Code Quality:**
> - Implement **Ktlint** and **Detekt** to enforce coding standards and catch common bugs automatically.
> - Establish a standardized **logging and analytics** wrapper to keep third-party dependencies isolated from the core code.
>
> By following these steps, the project starts with a robust, scalable, and quality-focused foundation, making development faster and easier in the long run."

---

---

## any other things do you consider before creating new project?

That's a smart way to ensure all bases are covered. Beyond the foundational technical and architectural decisions, an experienced developer needs to consider several practical, operational, and team-related factors _before_ writing the first line of feature code.

Here are additional critical considerations before starting a new Android project:

---

## 🧐 Additional Pre-Project Considerations

### 1. 🌐 Internationalization (i18n) and Localization (l10n)

- **String Resource Strategy:** Determine early if the app will support multiple languages. This means committing to using **`strings.xml`** for **all user-facing text** from day one, rather than hardcoding.
- **Plurals and Context:** Plan for complex strings like plurals (`plurals.xml`) and formatted strings.
- **RTL Support:** If supporting languages like Arabic or Hebrew, ensure the UI structure is tested for **Right-to-Left (RTL)** layout mirroring early in the design process to avoid costly refactoring later.

### 2. 🛡️ Security and Privacy Policy Compliance

- **API Key Management:** Decide on the security strategy for API keys (e.g., storing them in Gradle properties, using NDK for hiding, or integrating a dedicated secret manager). **Never commit them directly to Git.**
- **Personal Identifiable Information (PII):** Plan how to handle, store, and transmit sensitive user data. If local storage is used, determine if encryption is necessary (e.g., using Jetpack Security library for `EncryptedSharedPreferences`).
- **Permissions Strategy:** Audit the minimal permissions required by the app and plan for the new, stricter **runtime permission** model, particularly for sensitive permissions like location or camera.

### 3. 🎨 Design System and UI Consistency

- **Theme and Styles:** Establish a custom **Material 3 Theme** (`Theme.kt` for Compose or `styles.xml` for Views) immediately. Define primary, secondary, and tertiary color palettes and typography scales to ensure all developers use a consistent visual language.
- **Reusability Plan:** Identify common UI elements (buttons, loading spinners, input fields) that need to be created as reusable **Compose functions** or **custom XML views** and placed in the `:core:common` module.

### 4. 📈 Monitoring and Observability

- **Crash Reporting:** Integrate a crash reporting tool (e.g., Firebase Crashlytics, Sentry) immediately after core setup. This is vital for capturing errors missed in testing.
- **Analytics Setup:** Define the key user events that need tracking (e.g., button clicks, screen visits, conversion funnels). Set up a wrapper class for the analytics tool (e.g., Firebase Analytics) to ensure the core business logic is not directly dependent on the vendor's library.
- **Performance Benchmarking:** Identify critical user journeys (e.g., launch time, checkout) and integrate **macrobenchmarks** to automatically track performance regressions over time via the CI pipeline.

### 5. 🤝 Team Collaboration and Standards

- **Git Strategy:** Define the team's Git workflow (e.g., **GitFlow** or **GitHub Flow**). Establish clear branching and Pull Request (PR) review requirements.
- **Code Review Checklist:** Create a formal checklist for PRs covering testing, style, security, and architectural adherence.
- **Documentation:** Start a README file and architecture decision record (ADR) to document key choices (e.g., "Why we chose Hilt over Koin," "Why we use StateFlow instead of LiveData").

By addressing these five areas before starting feature development, you create a foundation that ensures the app is not just functional, but also maintainable, secure, and ready for collaboration.
