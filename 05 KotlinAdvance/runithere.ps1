# Root directory
$rootPath = ".\Kotlin_Interview_Roadmap"

# Phase definitions
$phases = @(
    @{
        PhaseNumber = 1
        PhaseTitle  = "The Foundation (Building Blocks)"
        FolderName  = "Phase 1 - The Foundation (Building Blocks)"
        Topics = @(
            "Variables: val vs var",
            "Basic Data Types & Type Inference",
            "String Templates",
            "Control Flow: if / else / when",
            "Loops & Ranges",
            "Basic Functions & Unit",
            "Default & Named Arguments"
        )
    },
    @{
        PhaseNumber = 2
        PhaseTitle  = "Object-Oriented Kotlin"
        FolderName  = "Phase 2 - Object-Oriented Kotlin"
        Topics = @(
            "Classes & Objects",
            "Constructors: Primary vs Secondary",
            "Inheritance & the open Keyword",
            "Interfaces",
            "Visibility Modifiers",
            "Abstract Classes"
        )
    },
    @{
        PhaseNumber = 3
        PhaseTitle  = "The Kotlin Way (Idiomatic Features)"
        FolderName  = "Phase 3 - The Kotlin Way"
        Topics = @(
            "Null Safety",
            "Data Classes",
            "Extension Functions",
            "Singleton Pattern (object)",
            "Companion Objects",
            "Sealed Classes & Interfaces"
        )
    },
    @{
        PhaseNumber = 4
        PhaseTitle  = "Functional Programming & Scoping"
        FolderName  = "Phase 4 - Functional Programming"
        Topics = @(
            "Lambdas & Higher-Order Functions",
            "Scope Functions",
            "Collections: Mutable vs Immutable",
            "Collection Operations"
        )
    },
    @{
        PhaseNumber = 5
        PhaseTitle  = "Advanced Topics & Coroutines"
        FolderName  = "Phase 5 - Advanced Topics"
        Topics = @(
            "Generics",
            "Delegation",
            "Coroutines Basics",
            "Suspend Functions",
            "Dispatchers",
            "Flow Basics"
        )
    },
    @{
        PhaseNumber = 6
        PhaseTitle  = "LeetCode Essentials (Kotlin)"
        FolderName  = "Phase 6 - LeetCode Essentials"
        Topics = @(
            "Array & String Manipulation",
            "HashMap & HashSet Mastery",
            "Sliding Window & Two Pointers",
            "Stack & Queue Implementations",
            "Sorting & Comparators"
        )
    },
    @{
        PhaseNumber = 7
        PhaseTitle  = "Real-World Interview Scenarios"
        FolderName  = "Phase 7 - Interview Scenarios"
        Topics = @(
            "Refactor Java Code to Kotlin",
            "Debugging Crashes",
            "Designing API Response Handlers",
            "Code Review Simulation"
        )
    },
    @{
        PhaseNumber = 8
        PhaseTitle  = "Interview Questions & Answers"
        FolderName  = "Phase 8 - Interview Q&A"
        Topics = @(
            "Rapid Fire Theory",
            "Deep Dive Explanations",
            "Tricky Output Questions"
        )
    }
)

# Create root folder
New-Item -ItemType Directory -Path $rootPath -Force | Out-Null

foreach ($phase in $phases) {
    $phasePath = Join-Path $rootPath $phase.FolderName
    New-Item -ItemType Directory -Path $phasePath -Force | Out-Null

    $index = 1
    foreach ($topic in $phase.Topics) {
        $fileNumber = "{0:D2}" -f $index
        $safeName = $topic -replace "[^a-zA-Z0-9 ]", "" -replace " ", "_"
        $fileName = "${fileNumber}_${safeName}.md"
        $filePath = Join-Path $phasePath $fileName

        if (-not (Test-Path $filePath)) {
            $content = @"
---
layout: default
title: "$topic"
parent: "$($phase.PhaseTitle)"
nav_order: $index
---

# $topic

<!-- Content starts here -->
"@
            Set-Content -Path $filePath -Value $content -Encoding UTF8
        }

        $index++
    }
}

Write-Host "✅ GitHub Pages docs structure generated successfully!"
