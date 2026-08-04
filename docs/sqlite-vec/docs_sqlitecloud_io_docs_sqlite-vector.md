# SQLite-Vector | SQLite Cloud Docs

> Source: [https://docs.sqlitecloud.io/docs/sqlite-vector](https://docs.sqlitecloud.io/docs/sqlite-vector)

#  SQLite-Vector

**SQLite Vector** is a cross-platform, ultra-efficient SQLite extension that brings vector search capabilities to your embedded database. It works seamlessly on **iOS, Android, Windows, Linux, and macOS** , using just **30MB of memory** by default. With support for **Float32, Float16, BFloat16, Int8, UInt8 and 1Bit** , and **highly optimized distance functions** , it’s the ideal solution for **Edge AI** applications.

Installed by default in SQLite Cloud[GitHub: https://github.com/sqliteai/sqlite-vector](<https://github.com/sqliteai/sqlite-vector>)

## Highlights

  * **No virtual tables required** – store vectors directly as `BLOB`s in ordinary tables
  * **Blazing fast** – optimized C implementation with SIMD acceleration
  * **Low memory footprint** – defaults to just 30MB of RAM usage
  * **Zero preindexing needed** – no long preprocessing or index-building phases
  * **Works offline** – perfect for on-device, privacy-preserving AI workloads
  * **Plug-and-play** – drop into existing SQLite workflows with minimal effort
  * **Cross-platform** – works out of the box on all major OSes

## Why Use SQLite-Vector?

Feature| SQLite-Vector| Traditional Solutions
---|---|---
Works with ordinary tables| ✅| ❌ (usually require special virtual tables)
Doesn’t need preindexing| ✅| ❌ (can take hours for large datasets)
Doesn’t need external server| ✅| ❌ (often needs Redis/FAISS/Weaviate/etc.)
Memory-efficient| ✅| ❌
Easy to use SQL| ✅| ❌ (often complex JOINs, subqueries)
Offline/Edge ready| ✅| ❌
Cross-platform| ✅| ❌

Unlike other vector databases or extensions that require complex setup, SQLite-Vector **just works** with your existing database schema and tools.

[ CLI ](<https://docs.sqlitecloud.io/docs/sqlite-memory-cli>)

[ Getting Started ](<https://docs.sqlitecloud.io/docs/sqlite-vector-getting-started>)
