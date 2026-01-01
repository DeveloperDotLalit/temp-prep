---
layout: default
title: "Dependency Injection"
nav_order: 3
has_children: true
---

# Dependency Injection

This is a smart adjustment. To truly reach an "Elite" level, you **must** understand Dagger. Hilt is just a wrapper around Dagger; if you understand Dagger's graph logic, Hilt becomes trivial. If you only know Hilt, debugging complex issues becomes a nightmare.

Here is the revised, comprehensive **"Zero to Elite" Roadmap** including Manual DI, Dagger 2, and Hilt.

### **Phase 1: The Fundamentals (Manual DI)**

- **The "Why" - Tight vs. Loose Coupling:** Understanding why `val engine = Engine()` is the root of all evil in scalable architecture.
- **Inversion of Control (IoC):** The principle of transferring the responsibility of object creation to a separate class.
- **Manual Constructor Injection:** The "Pure" way—passing dependencies via arguments without any libraries (Essential for understanding the _magic_ later).
- **Field & Setter Injection:** Handling Android Framework classes (Activities/Fragments) where constructors are unavailable.
- **The Application Container:** creating a custom `AppContainer` to manage Singletons and graph lifecycle manually.

### **Phase 2: Dagger 2 - The Engine (The Hard Part)**

- **Introduction to the Graph:** Understanding Dagger's Directed Acyclic Graph (DAG) and compile-time safety.
- **@Component & @Module:** The core building blocks—Modules provide recipes, Components cook the meal (wire it together).
- **Property Injection in Dagger:** How to inject into Activities using `(application as MyApp).component.inject(this)`.
- **Subcomponents:** Creating child graphs (e.g., `UserComponent` lives inside `AppComponent`) to manage encapsulation.
- **Custom Scopes:** Creating your own annotations (like `@LoggedUserScope`) to tie object lifecycles to user sessions, not just the app.

### **Phase 3: Hilt - The Android Standard (The Solution)**

- **The Migration Strategy:** How Hilt removes the boilerplate of Components and Modules we learned in Phase 2.
- **@InstallIn & Standard Components:** Mapping Dagger concepts to Hilt’s predefined containers (Singleton, ViewModel, Activity).
- **@AndroidEntryPoint:** The magic annotation that replaces the manual `inject(this)` calls from Phase 2.
- **ViewModel Injection:** The `@HiltViewModel` pattern which handles the complexities of `SavedStateHandle` automatically.
- **Context Injection:** Using `@ApplicationContext` and `@ActivityContext` without passing them manually.

### **Phase 4: Elite Scenarios & Architecture**

- **Qualifiers:** Handling multiple implementations of the same interface (e.g., `FakeRepository` vs `RealRepository`).
- **Assisted Injection:** The bridge between DI and runtime arguments (e.g., injecting a User ID into a ViewModel factory).
- **Multibindings (IntoSet/IntoMap):** The advanced Dagger/Hilt feature for plugin architectures (e.g., injecting multiple Analytics loggers at once).
- **Testing Strategy:** Swapping modules for UI Tests and Unit Tests using `@TestInstallIn`.
- **Under the Hood (Interview Gold):** How annotation processing works (KAPT/KSP) and reading the generated code to debug errors.

---

### **Next Step**

Shall we start strictly with **Phase 1: The Fundamentals**? We will begin by writing a "Bad Code" example with tight coupling and then refactoring it.

## Topics




## Modules / Phases

- [Phase 1: The Fundamentals](Phase1/index.md)
- [Phase 2: Dagger 2 - The Engine (The Hard Part)](Phase2/index.md)
- [Phase 3: Hilt - The Android Standard (The Solution)](Phase3/index.md)
- [Phase 4: Elite Scenarios & Architecture](Phase4/index.md)
