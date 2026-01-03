---
layout: default
title: "DB Migration Testing"
parent: "Phase 8: Scenario-Based Solutions"
nav_order: 1
grand_parent: "Unit & UI Testing"
---

Here are your in-depth study notes for **Phase 8, Scenario 1**.

This is arguably the most dangerous operation in Android development. If you mess up a UI test, a button doesn't work. If you mess up a DB Migration, **your users lose all their data** after an update. Interviewers ask this to test your "Risk Management."

---

# **Chapter 8: Scenario-Based Solutions**

## **Scenario 1: DB Migration Testing**

### **1. The Interview Question**

> **"We have an existing app with thousands of users. We need to add a new column to the `User` table in the next release. How do you ensure that when users update the app, their existing data isn't wiped out?"**

### **2. The Concept: Room's `MigrationTestHelper**`

You cannot test migrations by just running the app. You need a specialized test that simulates the update process programmatically.

- **Goal:** Verify that `Schema V1` + `Migration Script` = `Schema V2` (with data intact).
- **Requirement:** Room needs to know what "Version 1" looked like. You must export your schema history.

### **3. The Setup (Critical Prerequisite)**

You must configure your `build.gradle` to export schemas to a JSON file.

**Step A: `build.gradle**`

```kotlin
android {
    defaultConfig {
        javaCompileOptions {
            annotationProcessorOptions {
                // Tells Room to save the schema JSONs to this folder
                arguments += ["room.schemaLocation": "$projectDir/schemas".toString()]
            }
        }
    }
}

dependencies {
    androidTestImplementation("androidx.room:room-testing:2.6.1")
}

```

**Step B: The Database Class**

```kotlin
@Database(entities = [User::class], version = 2, exportSchema = true) // Must be true!
abstract class AppDatabase : RoomDatabase() { ... }

```

- _Note:_ When you build version 1, a `1.json` file appears. When you change to version 2, a `2.json` file appears. **Commit these files to Git.**

### **4. The Test Logic (The 4 Steps)**

To test a migration from Version 1 to Version 2:

1. **Create V1:** Use the helper to create a database using the `1.json` schema. Insert some test data (e.g., "User A").
2. **Close:** Close the database connection to simulate the app closing during update.
3. **Migrate:** Re-open the database using the helper, specifying `version 2`. This triggers your migration script.
4. **Validate:** Check two things:

- Does the new column exist? (Schema check)
- Is "User A" still there? (Data integrity check)

### **5. The Code Solution**

**The Migration Script (Production Code):**

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // SQL command to add the column
        database.execSQL("ALTER TABLE User ADD COLUMN phone_number TEXT NOT NULL DEFAULT ''")
    }
}

```

**The Test (AndroidTest):**

```kotlin
@RunWith(AndroidJUnit4::class)
class MigrationTest {

    private val TEST_DB = "migration-test"

    // The Magic Helper provided by Room
    @get:Rule
    val helper = MigrationTestHelper(
        InstrumentationRegistry.getInstrumentation(),
        AppDatabase::class.java.canonicalName,
        FrameworkSQLiteOpenHelperFactory()
    )

    @Test
    fun migrate1to2() {
        // STEP 1: Create DB in Version 1
        var db = helper.createDatabase(TEST_DB, 1).apply {
            // Insert data manually using SQL (Entities might have changed, so use raw SQL)
            execSQL("INSERT INTO User (id, name) VALUES (1, 'John Doe')")
            close() // STEP 2: Close it
        }

        // STEP 3: Migrate to Version 2
        // If this fails, the test crashes immediately
        db = helper.runMigrationsAndValidate(
            TEST_DB,
            2,    // Target Version
            true, // Validate Dropped Tables?
            MIGRATION_1_2 // The script being tested
        )

        // STEP 4: Validate Data
        // Query the new DB to ensure data survived
        val cursor = db.query("SELECT * FROM User WHERE id = 1")
        assertThat(cursor.moveToFirst()).isTrue()

        // Check old data
        assertThat(cursor.getString(cursor.getColumnIndex("name"))).isEqualTo("John Doe")

        // Check new column exists (should be default value)
        assertThat(cursor.getString(cursor.getColumnIndex("phone_number"))).isEqualTo("")
    }
}

```

### **6. Summary for Interviews**

> "To handle database migrations safely, I rely on Room's `exportSchema` feature to generate JSON history files for every database version.
> When adding a new column, I write a `Migration` object and a corresponding integration test using `MigrationTestHelper`. The test follows a strict sequence: it creates a database instance using the old schema (V1), inserts dummy data via raw SQL, closes it, and then runs the migration script to open it in V2. Finally, I query the database to assert that the old data persists and the new schema columns are present. I run these tests in my CI pipeline to ensure no update ever causes data loss."

---

**Would you like to proceed to Scenario 2: "Testing Runtime Permissions" (Handling system dialogs)?**
