# Installation - Agent Development Kit (ADK)

> Source: [https://adk.dev/get-started/installation/](https://adk.dev/get-started/installation/)

[ Skip to content ](<https://adk.dev/get-started/installation/#advanced-setup>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/get-started/installation.md> "Edit this page on GitHub") [ ](<https://adk.dev/get-started/installation/index.md> "View this page as Markdown")

# Advanced setup[¶](<https://adk.dev/get-started/installation/#advanced-setup> "Permanent link")

This page provides detailed installation and configuration instructions for ADK across supported languages. For a guided introduction, start with the [quickstart for your language](<https://adk.dev/get-started/>).

PythonTypeScriptGoJavaKotlin

**Create & activate virtual environment**

We recommend creating a virtual Python environment using [venv](<https://docs.python.org/3/library/venv.html>):
    
    [](<https://adk.dev/get-started/installation/#__codelineno-0-1>)python3 -m venv .venv
    
Now, you can activate the virtual environment using the appropriate command for your operating system and environment:
    
    [](<https://adk.dev/get-started/installation/#__codelineno-1-1>)# Mac / Linux
    [](<https://adk.dev/get-started/installation/#__codelineno-1-2>)source .venv/bin/activate
    [](<https://adk.dev/get-started/installation/#__codelineno-1-3>)
    [](<https://adk.dev/get-started/installation/#__codelineno-1-4>)# Windows CMD:
    [](<https://adk.dev/get-started/installation/#__codelineno-1-5>).venv\Scripts\activate.bat
    [](<https://adk.dev/get-started/installation/#__codelineno-1-6>)
    [](<https://adk.dev/get-started/installation/#__codelineno-1-7>)# Windows PowerShell:
    [](<https://adk.dev/get-started/installation/#__codelineno-1-8>).venv\Scripts\Activate.ps1
    
**Install ADK**
    
    [](<https://adk.dev/get-started/installation/#__codelineno-2-1>)pip install google-adk
    
(Optional) Verify your installation:
    
    [](<https://adk.dev/get-started/installation/#__codelineno-3-1>)pip show google-adk
    
**Install ADK and ADK DevTools**
    
    [](<https://adk.dev/get-started/installation/#__codelineno-4-1>)npm install @google/adk @google/adk-devtools
    
**Prerequisites:** Go 1.25 or later is required for ADK Go v2.0.0.

**Create a new Go module**

If you are starting a new project, you can create a new Go module:
    
    [](<https://adk.dev/get-started/installation/#__codelineno-5-1>)go mod init example.com/my-agent
    
**Install ADK Go v2.0.0**

To add ADK Go v2.0.0 to your project, run the following command:
    
    [](<https://adk.dev/get-started/installation/#__codelineno-6-1>)go get google.golang.org/adk/v2
    
This will add ADK Go v2.0.0 as a dependency to your `go.mod` file.

(Optional) Verify your installation by checking your `go.mod` file for the `google.golang.org/adk/v2` entry.

Still using ADK Go v1.x?

If you are not yet ready to upgrade to v2.0.0, you can continue using the v1.x release line:
    
    [](<https://adk.dev/get-started/installation/#__codelineno-7-1>)go get google.golang.org/adk@v1
    
See the [ADK 2.0 release page](<https://adk.dev/2.0/>) for upgrade guidance, including breaking changes and migration steps for ADK Go 1.x projects.

You can either use maven or gradle to add the `google-adk` and `google-adk-dev` package.

`google-adk` is the core Java ADK library. Java ADK also comes with a pluggable example SpringBoot server to run your agents seamlessly. This optional package is present as part of `google-adk-dev`.

If you are using maven, add the following to your `pom.xml`:

pom.xml
    
    [](<https://adk.dev/get-started/installation/#__codelineno-8-1>)<?xml version="1.0" encoding="UTF-8"?>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-2>)<project xmlns="http://maven.apache.org/POM/4.0.0"
    [](<https://adk.dev/get-started/installation/#__codelineno-8-3>)        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    [](<https://adk.dev/get-started/installation/#__codelineno-8-4>)        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    [](<https://adk.dev/get-started/installation/#__codelineno-8-5>)    <modelVersion>4.0.0</modelVersion>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-6>)
    [](<https://adk.dev/get-started/installation/#__codelineno-8-7>)    <groupId>com.example.agent</groupId>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-8>)    <artifactId>adk-agents</artifactId>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-9>)    <version>1.0-SNAPSHOT</version>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-10>)
    [](<https://adk.dev/get-started/installation/#__codelineno-8-11>)    <!-- Specify the version of Java you'll be using -->
    [](<https://adk.dev/get-started/installation/#__codelineno-8-12>)    <properties>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-13>)        <maven.compiler.source>17</maven.compiler.source>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-14>)        <maven.compiler.target>17</maven.compiler.target>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-15>)        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-16>)    </properties>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-17>)
    [](<https://adk.dev/get-started/installation/#__codelineno-8-18>)    <dependencies>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-19>)        <!-- The ADK core dependency -->
    [](<https://adk.dev/get-started/installation/#__codelineno-8-20>)        <dependency>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-21>)            <groupId>com.google.adk</groupId>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-22>)            <artifactId>google-adk</artifactId>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-23>)            <version>1.6.0</version>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-24>)        </dependency>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-25>)        <!-- The ADK dev web UI to debug your agent -->
    [](<https://adk.dev/get-started/installation/#__codelineno-8-26>)        <dependency>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-27>)            <groupId>com.google.adk</groupId>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-28>)            <artifactId>google-adk-dev</artifactId>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-29>)            <version>1.6.0</version>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-30>)        </dependency>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-31>)    </dependencies>
    [](<https://adk.dev/get-started/installation/#__codelineno-8-32>)
    [](<https://adk.dev/get-started/installation/#__codelineno-8-33>)</project>
    
Here's a [complete pom.xml](<https://github.com/google/adk-docs/tree/main/examples/java/cloud-run/pom.xml>) file for reference.

If you are using gradle, add the dependency to your build.gradle:

build.gradle
    
    [](<https://adk.dev/get-started/installation/#__codelineno-9-1>)dependencies {
    [](<https://adk.dev/get-started/installation/#__codelineno-9-2>)    implementation 'com.google.adk:google-adk:1.6.0'
    [](<https://adk.dev/get-started/installation/#__codelineno-9-3>)    implementation 'com.google.adk:google-adk-dev:1.6.0'
    [](<https://adk.dev/get-started/installation/#__codelineno-9-4>)}
    
You should also configure Gradle to pass `-parameters` to `javac`. (Alternatively, use `@Schema(name = "...")`).

**Use ADK Kotlin on the JVM**

For Kotlin on the JVM, add the ADK core library and the KSP annotation processor to your `build.gradle.kts`:

build.gradle.kts
    
    [](<https://adk.dev/get-started/installation/#__codelineno-10-1>)plugins {
    [](<https://adk.dev/get-started/installation/#__codelineno-10-2>)    kotlin("jvm") version "2.1.20"
    [](<https://adk.dev/get-started/installation/#__codelineno-10-3>)    id("com.google.devtools.ksp") version "2.1.20-2.0.1"
    [](<https://adk.dev/get-started/installation/#__codelineno-10-4>)}
    [](<https://adk.dev/get-started/installation/#__codelineno-10-5>)
    [](<https://adk.dev/get-started/installation/#__codelineno-10-6>)dependencies {
    [](<https://adk.dev/get-started/installation/#__codelineno-10-7>)    implementation("com.google.adk:google-adk-kotlin-core:0.5.0")
    [](<https://adk.dev/get-started/installation/#__codelineno-10-8>)    ksp("com.google.adk:google-adk-kotlin-processor:0.5.0")
    [](<https://adk.dev/get-started/installation/#__codelineno-10-9>)}
    
The KSP processor generates code for the `@Tool` annotation used to register function tools. See the [Kotlin Quickstart](<https://adk.dev/get-started/kotlin/>) for a complete project setup.

Back to top 