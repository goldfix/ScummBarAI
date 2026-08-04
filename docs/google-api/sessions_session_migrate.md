# Migrate sessions - Agent Development Kit (ADK)

> Source: [https://adk.dev/sessions/session/migrate/](https://adk.dev/sessions/session/migrate/)

[ Skip to content ](<https://adk.dev/sessions/session/migrate/#session-database-schema-migration>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/sessions/session/migrate.md> "Edit this page on GitHub") [ ](<https://adk.dev/sessions/session/migrate/index.md> "View this page as Markdown")

# Session database schema migration[¶](<https://adk.dev/sessions/session/migrate/#session-database-schema-migration> "Permanent link")

Supported in ADKPython v1.22.1

If you are using `DatabaseSessionService` and upgrading to ADK Python release v1.22.0 or higher, you should migrate your database to the new session database schema. Starting with ADK Python release v1.22.0, the database schema for `DatabaseSessionService` has been updated from `v0`, which is a pickle-based serialization, to `v1`, which uses JSON-based serialization. Previous `v0` session schema databases will continue to work with ADK Python v1.22.0 and higher versions, but the `v1` schema may be required in future releases.

## Migrate session database[¶](<https://adk.dev/sessions/session/migrate/#migrate-session-database> "Permanent link")

A migration script is provided to facilitate the migration process. The script reads data from your existing database, converts it to the new format, and writes it to a new database. You can run the migration using the ADK Command Line Interface (CLI) `migrate session` command, as shown in the following examples:

Required: ADK Python v1.22.1 or higher

ADK Python v1.22.1 is required for this procedure because it includes the migration command line interface function and bug fixes to support the session database schema change.

SQLitePostgreSQL
    
    [](<https://adk.dev/sessions/session/migrate/#__codelineno-0-1>)adk migrate session \
    [](<https://adk.dev/sessions/session/migrate/#__codelineno-0-2>)  --source_db_url=sqlite:///source.db \
    [](<https://adk.dev/sessions/session/migrate/#__codelineno-0-3>)  --dest_db_url=sqlite:///dest.db
    
    [](<https://adk.dev/sessions/session/migrate/#__codelineno-1-1>)adk migrate session \
    [](<https://adk.dev/sessions/session/migrate/#__codelineno-1-2>)  --source_db_url=postgresql://localhost:5432/v0 \
    [](<https://adk.dev/sessions/session/migrate/#__codelineno-1-3>)  --dest_db_url=postgresql://localhost:5432/v1
    
After running the migration, update your `DatabaseSessionService` configuration to use the new database URL you specified for `dest_db_url`.

Back to top 