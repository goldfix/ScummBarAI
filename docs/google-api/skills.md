# Skills for ADK agents - Agent Development Kit (ADK)

> Source: [https://adk.dev/skills/](https://adk.dev/skills/)

[ Skip to content ](<https://adk.dev/skills/#skills-for-adk-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/skills/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/skills/index.md> "View this page as Markdown")

# Skills for ADK agents[¶](<https://adk.dev/skills/#skills-for-adk-agents> "Permanent link")

Supported in ADKPython v1.25.0TypeScript v0.6.1Go v1.2.0Experimental

An agent **_Skill_** is a self-contained unit of functionality that an ADK agent can use to perform a specific task. An agent Skill encapsulates the necessary instructions, resources, and tools required for a task, based on the [Agent Skill specification](<https://agentskills.io/specification>). The structure of a Skill allows it to be loaded incrementally to minimize the impact on the operating context window of the agent.

Experimental

The Skills feature is experimental. We welcome your feedback via the respective ADK GitHub repositories: [ADK Python](<https://github.com/google/adk-python/issues/new?template=feature_request.md&labels=skills>), [ADK TypeScript](<https://github.com/google/adk-js/issues/new?template=feature_request.md&labels=skills>), [ADK Go](<https://github.com/google/adk-go/issues/new?template=feature_request.md&labels=skills>).

## Get started[¶](<https://adk.dev/skills/#get-started> "Permanent link")

Use the `SkillToolset` class to make one or more Skills available to your agent. You can define [skills in code](<https://adk.dev/skills/#inline-skills>) or load [skills from a filesystem](<https://adk.dev/skills/#filesystem-skills>).

PythonTypeScriptGo
    
    [](<https://adk.dev/skills/#__codelineno-0-1>)import pathlib
    [](<https://adk.dev/skills/#__codelineno-0-2>)
    [](<https://adk.dev/skills/#__codelineno-0-3>)from google.adk import Agent
    [](<https://adk.dev/skills/#__codelineno-0-4>)from google.adk.skills import load_skill_from_dir
    [](<https://adk.dev/skills/#__codelineno-0-5>)from google.adk.tools import skill_toolset
    [](<https://adk.dev/skills/#__codelineno-0-6>)
    [](<https://adk.dev/skills/#__codelineno-0-7>)weather_skill = load_skill_from_dir(
    [](<https://adk.dev/skills/#__codelineno-0-8>)    pathlib.Path(__file__).parent / "skills" / "weather_skill"
    [](<https://adk.dev/skills/#__codelineno-0-9>))
    [](<https://adk.dev/skills/#__codelineno-0-10>)
    [](<https://adk.dev/skills/#__codelineno-0-11>)my_skill_toolset = skill_toolset.SkillToolset(
    [](<https://adk.dev/skills/#__codelineno-0-12>)    skills=[weather_skill],
    [](<https://adk.dev/skills/#__codelineno-0-13>)    additional_tools=[get_weather_tool],
    [](<https://adk.dev/skills/#__codelineno-0-14>))
    [](<https://adk.dev/skills/#__codelineno-0-15>)
    [](<https://adk.dev/skills/#__codelineno-0-16>)root_agent = Agent(
    [](<https://adk.dev/skills/#__codelineno-0-17>)    model="gemini-flash-latest",
    [](<https://adk.dev/skills/#__codelineno-0-18>)    name="skill_user_agent",
    [](<https://adk.dev/skills/#__codelineno-0-19>)    description="An agent that can use specialized skills.",
    [](<https://adk.dev/skills/#__codelineno-0-20>)    instruction=(
    [](<https://adk.dev/skills/#__codelineno-0-21>)        "You are a helpful assistant that can leverage skills to perform tasks."
    [](<https://adk.dev/skills/#__codelineno-0-22>)    ),
    [](<https://adk.dev/skills/#__codelineno-0-23>)    tools=[
    [](<https://adk.dev/skills/#__codelineno-0-24>)        my_skill_toolset,
    [](<https://adk.dev/skills/#__codelineno-0-25>)    ],
    [](<https://adk.dev/skills/#__codelineno-0-26>))
    
For a complete code example of an ADK agent with a Skill, including both file-based and in-line Skill definitions, see the code sample [skills_agent](<https://github.com/google/adk-python/tree/main/contributing/samples/environment_and_skills/skills_agent>).
    
    [](<https://adk.dev/skills/#__codelineno-1-1>)import {Agent, FunctionTool, SkillToolset, loadSkillFromDir} from '@google/adk';
    [](<https://adk.dev/skills/#__codelineno-1-2>)import * as path from 'node:path';
    [](<https://adk.dev/skills/#__codelineno-1-3>)import {z} from 'zod';
    [](<https://adk.dev/skills/#__codelineno-1-4>)
    [](<https://adk.dev/skills/#__codelineno-1-5>)const weatherSkill = await loadSkillFromDir(
    [](<https://adk.dev/skills/#__codelineno-1-6>)  path.join(__dirname, 'skills/weather_skill')
    [](<https://adk.dev/skills/#__codelineno-1-7>));
    [](<https://adk.dev/skills/#__codelineno-1-8>)
    [](<https://adk.dev/skills/#__codelineno-1-9>)const getWeatherTool = new FunctionTool({
    [](<https://adk.dev/skills/#__codelineno-1-10>)  name: 'get_weather',
    [](<https://adk.dev/skills/#__codelineno-1-11>)  description: 'Gets the weather for a given location.',
    [](<https://adk.dev/skills/#__codelineno-1-12>)  parameters: z.object({
    [](<https://adk.dev/skills/#__codelineno-1-13>)    location: z.string().describe('The city and state, e.g. San Francisco, CA'),
    [](<https://adk.dev/skills/#__codelineno-1-14>)  }),
    [](<https://adk.dev/skills/#__codelineno-1-15>)  execute: async ({location}) => {
    [](<https://adk.dev/skills/#__codelineno-1-16>)    return {
    [](<https://adk.dev/skills/#__codelineno-1-17>)      location,
    [](<https://adk.dev/skills/#__codelineno-1-18>)      temperature: '72°F',
    [](<https://adk.dev/skills/#__codelineno-1-19>)      condition: 'Sunny',
    [](<https://adk.dev/skills/#__codelineno-1-20>)    };
    [](<https://adk.dev/skills/#__codelineno-1-21>)  },
    [](<https://adk.dev/skills/#__codelineno-1-22>)});
    [](<https://adk.dev/skills/#__codelineno-1-23>)
    [](<https://adk.dev/skills/#__codelineno-1-24>)const mySkillToolset = new SkillToolset([weatherSkill], {
    [](<https://adk.dev/skills/#__codelineno-1-25>)  additionalTools: [getWeatherTool],
    [](<https://adk.dev/skills/#__codelineno-1-26>)});
    [](<https://adk.dev/skills/#__codelineno-1-27>)
    [](<https://adk.dev/skills/#__codelineno-1-28>)const rootAgent = new Agent({
    [](<https://adk.dev/skills/#__codelineno-1-29>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/skills/#__codelineno-1-30>)  name: 'skill_user_agent',
    [](<https://adk.dev/skills/#__codelineno-1-31>)  description: 'An agent that can use specialized skills.',
    [](<https://adk.dev/skills/#__codelineno-1-32>)  instruction:
    [](<https://adk.dev/skills/#__codelineno-1-33>)    'You are a helpful assistant that can leverage skills to perform tasks.',
    [](<https://adk.dev/skills/#__codelineno-1-34>)  tools: [mySkillToolset],
    [](<https://adk.dev/skills/#__codelineno-1-35>)});
    [](<https://adk.dev/skills/#__codelineno-1-36>)
    [](<https://adk.dev/skills/#__codelineno-1-37>)export default rootAgent;
    
    [](<https://adk.dev/skills/#__codelineno-2-1>)import (
    [](<https://adk.dev/skills/#__codelineno-2-2>)    "context"
    [](<https://adk.dev/skills/#__codelineno-2-3>)    "os"
    [](<https://adk.dev/skills/#__codelineno-2-4>)
    [](<https://adk.dev/skills/#__codelineno-2-5>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/skills/#__codelineno-2-6>)    "google.golang.org/adk/v2/tool/skilltoolset/skill"
    [](<https://adk.dev/skills/#__codelineno-2-7>)    "google.golang.org/adk/v2/tool/skilltoolset"
    [](<https://adk.dev/skills/#__codelineno-2-8>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/skills/#__codelineno-2-9>))
    [](<https://adk.dev/skills/#__codelineno-2-10>)
    [](<https://adk.dev/skills/#__codelineno-2-11>)mySkillToolset, err := skilltoolset.New(ctx, skilltoolset.Config{
    [](<https://adk.dev/skills/#__codelineno-2-12>)    Source: skill.NewFileSystemSource(os.DirFS("./skills")),
    [](<https://adk.dev/skills/#__codelineno-2-13>)})
    [](<https://adk.dev/skills/#__codelineno-2-14>)if err != nil {
    [](<https://adk.dev/skills/#__codelineno-2-15>)    // handle error
    [](<https://adk.dev/skills/#__codelineno-2-16>)}
    [](<https://adk.dev/skills/#__codelineno-2-17>)
    [](<https://adk.dev/skills/#__codelineno-2-18>)rootAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/skills/#__codelineno-2-19>)    Name:        "skill_user_agent",
    [](<https://adk.dev/skills/#__codelineno-2-20>)    Model:       model,
    [](<https://adk.dev/skills/#__codelineno-2-21>)    Description: "An agent that can use specialized skills.",
    [](<https://adk.dev/skills/#__codelineno-2-22>)    Instruction: "You are a helpful assistant that can leverage skills to perform tasks.",
    [](<https://adk.dev/skills/#__codelineno-2-23>)    Toolsets:    []tool.Toolset{mySkillToolset},
    [](<https://adk.dev/skills/#__codelineno-2-24>)})
    [](<https://adk.dev/skills/#__codelineno-2-25>)if err != nil {
    [](<https://adk.dev/skills/#__codelineno-2-26>)    // handle error
    [](<https://adk.dev/skills/#__codelineno-2-27>)}
    
For a complete example, see the code sample in [skills](<https://github.com/google/adk-go/tree/main/examples/skills>).

Check your working directory
    
    Ensure that 'skills/' directory exist in your current working directory and contains the sub-directories for the Skills you want to use in your agent.
    
## Skill structure[¶](<https://adk.dev/skills/#skill-structure> "Permanent link")

The Skills feature allows you to create modular packages of Skill instructions and resources that agents can load on demand. This approach helps you organize your agent's capabilities and optimize the context window by only loading instructions when they are needed. The structure of Skills is organized into three levels:

  * **L1 (Metadata):** Provides metadata for skill discovery. This information is defined in the frontmatter section of the `SKILL.md` file and includes properties such as the Skill name and description.
  * **L2 (Instructions):** Contains the primary instructions for the Skill, loaded when the Skill is triggered by the agent. This information is defined in the body of the `SKILL.md` file.
  * **L3 (Resources):** Includes additional resources such as reference materials, assets, and scripts that can be loaded as needed. These resources are organized into the following directories:
    * `references/`: Additional Markdown files with extended instructions, workflows, or guidance.
    * `assets/`: Resource materials such as database schemas, API documentation, templates, or examples.
    * `scripts/`: Executable scripts supported by the agent runtime.

### System instructions for using skills[¶](<https://adk.dev/skills/#system-instructions-for-using-skills> "Permanent link")

The `SkillToolset` provides a default system instruction to the agent that outlines how it should interact with skills. These instructions include the following key points:

  * You must use the `load_skill` tool to read a skill's instructions before using it.
  * You must follow the instructions in the skill definition exactly.
  * You must use the `load_skill_resource` tool to view files within a skill's directory.
  * You must use the `run_skill_script` to run scripts from a skill's `scripts/` directory.

### Skill validation[¶](<https://adk.dev/skills/#skill-validation> "Permanent link")

The frontmatter of a skill's `SKILL.md` file is validated to ensure that it meets the following requirements:

  * **name** :
    * Must be 64 characters or less.
    * Must be in lowercase, kebab-case (a-z, 0-9, and hyphens).
    * Must not have leading, trailing, or consecutive hyphens.
  * **description** :
    * Must not be empty.
    * Must be 1024 characters or less.

### Skills directory structure[¶](<https://adk.dev/skills/#skills-directory-structure> "Permanent link")

The following directory structure shows the recommended way to include Skills in your ADK agent project. The `example-skill/` directory shown below, and any parallel Skill directories, must follow the [Agent Skill specification](<https://agentskills.io/specification>) file structure. Only the `SKILL.md` file is required.
    
    [](<https://adk.dev/skills/#__codelineno-3-1>)my_agent/
    [](<https://adk.dev/skills/#__codelineno-3-2>)    agent.py (or agent.ts / main.go)
    [](<https://adk.dev/skills/#__codelineno-3-3>)    .env
    [](<https://adk.dev/skills/#__codelineno-3-4>)    skills/
    [](<https://adk.dev/skills/#__codelineno-3-5>)        example-skill/        # Skill
    [](<https://adk.dev/skills/#__codelineno-3-6>)            SKILL.md          # main instructions (required)
    [](<https://adk.dev/skills/#__codelineno-3-7>)            references/
    [](<https://adk.dev/skills/#__codelineno-3-8>)                REFERENCE.md  # detailed API reference
    [](<https://adk.dev/skills/#__codelineno-3-9>)                FORMS.md      # form-filling guide
    [](<https://adk.dev/skills/#__codelineno-3-10>)                *.md          # domain-specific information
    [](<https://adk.dev/skills/#__codelineno-3-11>)            assets/
    [](<https://adk.dev/skills/#__codelineno-3-12>)                *.*           # templates, images, data
    [](<https://adk.dev/skills/#__codelineno-3-13>)            scripts/
    [](<https://adk.dev/skills/#__codelineno-3-14>)                *.py          # utility scripts (Python)
    [](<https://adk.dev/skills/#__codelineno-3-15>)                *.js          # utility scripts (JavaScript)
    [](<https://adk.dev/skills/#__codelineno-3-16>)                *.ts          # utility scripts (TypeScript)
    
## Skill sources[¶](<https://adk.dev/skills/#skill-sources> "Permanent link")

You can define [skills within the code](<https://adk.dev/skills/#inline-skills>) or read [skills from a filesystem](<https://adk.dev/skills/#filesystem-skills>).

### Define Skills in code[¶](<https://adk.dev/skills/#inline-skills> "Permanent link")

You can define Skills within the code of your agent, as shown below.

PythonTypeScriptGo
    
    [](<https://adk.dev/skills/#__codelineno-4-1>)from google.adk.skills import models
    [](<https://adk.dev/skills/#__codelineno-4-2>)
    [](<https://adk.dev/skills/#__codelineno-4-3>)greeting_skill = models.Skill(
    [](<https://adk.dev/skills/#__codelineno-4-4>)    frontmatter=models.Frontmatter(
    [](<https://adk.dev/skills/#__codelineno-4-5>)        name="greeting-skill",
    [](<https://adk.dev/skills/#__codelineno-4-6>)        description=(
    [](<https://adk.dev/skills/#__codelineno-4-7>)            "A friendly greeting skill that can say hello to a specific person."
    [](<https://adk.dev/skills/#__codelineno-4-8>)        ),
    [](<https://adk.dev/skills/#__codelineno-4-9>)    ),
    [](<https://adk.dev/skills/#__codelineno-4-10>)    instructions=(
    [](<https://adk.dev/skills/#__codelineno-4-11>)        "Step 1: Read the 'references/hello_world.txt' file to understand how"
    [](<https://adk.dev/skills/#__codelineno-4-12>)        " to greet the user. Step 2: Return a greeting based on the reference."
    [](<https://adk.dev/skills/#__codelineno-4-13>)    ),
    [](<https://adk.dev/skills/#__codelineno-4-14>)    resources=models.Resources(
    [](<https://adk.dev/skills/#__codelineno-4-15>)        references={
    [](<https://adk.dev/skills/#__codelineno-4-16>)            "hello_world.txt": "Hello! So glad to have you here!",
    [](<https://adk.dev/skills/#__codelineno-4-17>)            "example.md": "This is an example reference.",
    [](<https://adk.dev/skills/#__codelineno-4-18>)        },
    [](<https://adk.dev/skills/#__codelineno-4-19>)    ),
    [](<https://adk.dev/skills/#__codelineno-4-20>))
    
    [](<https://adk.dev/skills/#__codelineno-5-1>)import {Agent, Skill, SkillToolset} from '@google/adk';
    [](<https://adk.dev/skills/#__codelineno-5-2>)
    [](<https://adk.dev/skills/#__codelineno-5-3>)const greetingSkill: Skill = {
    [](<https://adk.dev/skills/#__codelineno-5-4>)  frontmatter: {
    [](<https://adk.dev/skills/#__codelineno-5-5>)    name: 'greeting-skill',
    [](<https://adk.dev/skills/#__codelineno-5-6>)    description: 'A friendly greeting skill that can say hello to a specific person.',
    [](<https://adk.dev/skills/#__codelineno-5-7>)  },
    [](<https://adk.dev/skills/#__codelineno-5-8>)  instructions:
    [](<https://adk.dev/skills/#__codelineno-5-9>)    "Step 1: Read the 'references/hello_world.txt' file to understand how to greet the user. Step 2: Return a greeting based on the reference.",
    [](<https://adk.dev/skills/#__codelineno-5-10>)  resources: {
    [](<https://adk.dev/skills/#__codelineno-5-11>)    references: {
    [](<https://adk.dev/skills/#__codelineno-5-12>)      'hello_world.txt': 'Hello! So glad to have you here!',
    [](<https://adk.dev/skills/#__codelineno-5-13>)      'example.md': 'This is an example reference.',
    [](<https://adk.dev/skills/#__codelineno-5-14>)    },
    [](<https://adk.dev/skills/#__codelineno-5-15>)  },
    [](<https://adk.dev/skills/#__codelineno-5-16>)};
    [](<https://adk.dev/skills/#__codelineno-5-17>)
    [](<https://adk.dev/skills/#__codelineno-5-18>)const mySkillToolset = new SkillToolset([greetingSkill]);
    [](<https://adk.dev/skills/#__codelineno-5-19>)
    [](<https://adk.dev/skills/#__codelineno-5-20>)const rootAgent = new Agent({
    [](<https://adk.dev/skills/#__codelineno-5-21>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/skills/#__codelineno-5-22>)  name: 'greeting_agent',
    [](<https://adk.dev/skills/#__codelineno-5-23>)  description: 'An agent that uses an inline greeting skill.',
    [](<https://adk.dev/skills/#__codelineno-5-24>)  instruction: 'You are a helpful assistant that uses skills to greet people.',
    [](<https://adk.dev/skills/#__codelineno-5-25>)  tools: [mySkillToolset],
    [](<https://adk.dev/skills/#__codelineno-5-26>)});
    [](<https://adk.dev/skills/#__codelineno-5-27>)
    [](<https://adk.dev/skills/#__codelineno-5-28>)export default rootAgent;
    
Note

ADK Go does not currently provide a standard Source for inline skills, though this may be added in the future. To define skills directly in code, you must implement the `skill.Source` interface yourself, as shown below.
    
    [](<https://adk.dev/skills/#__codelineno-6-1>)import (
    [](<https://adk.dev/skills/#__codelineno-6-2>)    "context"
    [](<https://adk.dev/skills/#__codelineno-6-3>)    "io"
    [](<https://adk.dev/skills/#__codelineno-6-4>)    "slices"
    [](<https://adk.dev/skills/#__codelineno-6-5>)    "strings"
    [](<https://adk.dev/skills/#__codelineno-6-6>)
    [](<https://adk.dev/skills/#__codelineno-6-7>)    "google.golang.org/adk/v2/tool/skilltoolset/skill"
    [](<https://adk.dev/skills/#__codelineno-6-8>))
    [](<https://adk.dev/skills/#__codelineno-6-9>)
    [](<https://adk.dev/skills/#__codelineno-6-10>)// Example implementation of a static in-memory skill.Source:
    [](<https://adk.dev/skills/#__codelineno-6-11>)type StaticSource struct{}
    [](<https://adk.dev/skills/#__codelineno-6-12>)
    [](<https://adk.dev/skills/#__codelineno-6-13>)func (s *StaticSource) ListFrontmatters(ctx context.Context) ([]*skill.Frontmatter, error) {
    [](<https://adk.dev/skills/#__codelineno-6-14>)    return []*skill.Frontmatter{
    [](<https://adk.dev/skills/#__codelineno-6-15>)        {Name: "greeting-skill", Description: "A friendly greeting skill that can say hello to a specific person."},
    [](<https://adk.dev/skills/#__codelineno-6-16>)    }, nil
    [](<https://adk.dev/skills/#__codelineno-6-17>)}
    [](<https://adk.dev/skills/#__codelineno-6-18>)
    [](<https://adk.dev/skills/#__codelineno-6-19>)func (s *StaticSource) LoadFrontmatter(ctx context.Context, name string) (*skill.Frontmatter, error) {
    [](<https://adk.dev/skills/#__codelineno-6-20>)    if name != "greeting-skill" {
    [](<https://adk.dev/skills/#__codelineno-6-21>)        return nil, skill.ErrSkillNotFound
    [](<https://adk.dev/skills/#__codelineno-6-22>)    }
    [](<https://adk.dev/skills/#__codelineno-6-23>)    return &skill.Frontmatter{Name: "greeting-skill", Description: "A friendly greeting skill that can say hello to a specific person."}, nil
    [](<https://adk.dev/skills/#__codelineno-6-24>)}
    [](<https://adk.dev/skills/#__codelineno-6-25>)
    [](<https://adk.dev/skills/#__codelineno-6-26>)func (s *StaticSource) LoadInstructions(ctx context.Context, name string) (string, error) {
    [](<https://adk.dev/skills/#__codelineno-6-27>)    if name != "greeting-skill" {
    [](<https://adk.dev/skills/#__codelineno-6-28>)        return "", skill.ErrSkillNotFound
    [](<https://adk.dev/skills/#__codelineno-6-29>)    }
    [](<https://adk.dev/skills/#__codelineno-6-30>)    return "Step 1: Read the 'references/hello_world.txt' file to understand how to greet the user. Step 2: Return a greeting based on the reference.", nil
    [](<https://adk.dev/skills/#__codelineno-6-31>)}
    [](<https://adk.dev/skills/#__codelineno-6-32>)
    [](<https://adk.dev/skills/#__codelineno-6-33>)func (s *StaticSource) ListResources(ctx context.Context, name, subpath string) ([]string, error) {
    [](<https://adk.dev/skills/#__codelineno-6-34>)    if name != "greeting-skill" {
    [](<https://adk.dev/skills/#__codelineno-6-35>)        return nil, skill.ErrSkillNotFound
    [](<https://adk.dev/skills/#__codelineno-6-36>)    }
    [](<https://adk.dev/skills/#__codelineno-6-37>)    if !slices.Contains([]string{"", ".", "references", "references/"}, subpath) {
    [](<https://adk.dev/skills/#__codelineno-6-38>)        return nil, skill.ErrResourceNotFound
    [](<https://adk.dev/skills/#__codelineno-6-39>)    }
    [](<https://adk.dev/skills/#__codelineno-6-40>)    return []string{"references/hello_world.txt", "references/example.md"}, nil
    [](<https://adk.dev/skills/#__codelineno-6-41>)}
    [](<https://adk.dev/skills/#__codelineno-6-42>)
    [](<https://adk.dev/skills/#__codelineno-6-43>)func (s *StaticSource) LoadResource(ctx context.Context, name, resourcePath string) (io.ReadCloser, error) {
    [](<https://adk.dev/skills/#__codelineno-6-44>)    if name != "greeting-skill" {
    [](<https://adk.dev/skills/#__codelineno-6-45>)        return nil, skill.ErrSkillNotFound
    [](<https://adk.dev/skills/#__codelineno-6-46>)    }
    [](<https://adk.dev/skills/#__codelineno-6-47>)    switch resourcePath {
    [](<https://adk.dev/skills/#__codelineno-6-48>)    case "references/hello_world.txt":
    [](<https://adk.dev/skills/#__codelineno-6-49>)        return io.NopCloser(strings.NewReader("Hello! So glad to have you here!")), nil
    [](<https://adk.dev/skills/#__codelineno-6-50>)    case "references/example.md":
    [](<https://adk.dev/skills/#__codelineno-6-51>)        return io.NopCloser(strings.NewReader("This is an example reference.")), nil
    [](<https://adk.dev/skills/#__codelineno-6-52>)    default:
    [](<https://adk.dev/skills/#__codelineno-6-53>)        return nil, skill.ErrResourceNotFound
    [](<https://adk.dev/skills/#__codelineno-6-54>)    }
    [](<https://adk.dev/skills/#__codelineno-6-55>)}
    
Note

The `Source` interface can be backed by any data store (such as a database) to support dynamic use cases like live updates and personalization.

### Read Skills from filesystem[¶](<https://adk.dev/skills/#filesystem-skills> "Permanent link")

PythonGo
    
    [](<https://adk.dev/skills/#__codelineno-7-1>)import pathlib
    [](<https://adk.dev/skills/#__codelineno-7-2>)
    [](<https://adk.dev/skills/#__codelineno-7-3>)from google.adk.skills import load_skill_from_dir
    [](<https://adk.dev/skills/#__codelineno-7-4>)from google.adk.tools import skill_toolset
    [](<https://adk.dev/skills/#__codelineno-7-5>)
    [](<https://adk.dev/skills/#__codelineno-7-6>)greeting_skill = load_skill_from_dir(
    [](<https://adk.dev/skills/#__codelineno-7-7>)    pathlib.Path(__file__).parent / "skills" / "greeting-skill"
    [](<https://adk.dev/skills/#__codelineno-7-8>))
    [](<https://adk.dev/skills/#__codelineno-7-9>)weather_skill = load_skill_from_dir(
    [](<https://adk.dev/skills/#__codelineno-7-10>)    pathlib.Path(__file__).parent / "skills" / "weather-skill"
    [](<https://adk.dev/skills/#__codelineno-7-11>))
    [](<https://adk.dev/skills/#__codelineno-7-12>)
    [](<https://adk.dev/skills/#__codelineno-7-13>)my_skill_toolset = skill_toolset.SkillToolset(
    [](<https://adk.dev/skills/#__codelineno-7-14>)    skills=[weather_skill, greeting_skill],
    [](<https://adk.dev/skills/#__codelineno-7-15>))
    
    [](<https://adk.dev/skills/#__codelineno-8-1>)import (
    [](<https://adk.dev/skills/#__codelineno-8-2>)    "os"
    [](<https://adk.dev/skills/#__codelineno-8-3>)
    [](<https://adk.dev/skills/#__codelineno-8-4>)    "google.golang.org/adk/v2/tool/skilltoolset/skill"
    [](<https://adk.dev/skills/#__codelineno-8-5>)    "google.golang.org/adk/v2/tool/skilltoolset"
    [](<https://adk.dev/skills/#__codelineno-8-6>))
    [](<https://adk.dev/skills/#__codelineno-8-7>)
    [](<https://adk.dev/skills/#__codelineno-8-8>)// ...
    [](<https://adk.dev/skills/#__codelineno-8-9>)
    [](<https://adk.dev/skills/#__codelineno-8-10>)source := skill.NewFileSystemSource(os.DirFS("./skills"))
    [](<https://adk.dev/skills/#__codelineno-8-11>)
    [](<https://adk.dev/skills/#__codelineno-8-12>)// This example doesn't use any optional wrappers, but you can use them if
    [](<https://adk.dev/skills/#__codelineno-8-13>)// needed, e.g.:
    [](<https://adk.dev/skills/#__codelineno-8-14>)//   source, _, err = skill.WithFrontmatterPreloadSource(ctx, source)
    [](<https://adk.dev/skills/#__codelineno-8-15>)//   source, _, err = skill.WithCompletePreloadSource(ctx, source)
    [](<https://adk.dev/skills/#__codelineno-8-16>)// For more information about these and other wrappers, see
    [](<https://adk.dev/skills/#__codelineno-8-17>)// https://pkg.go.dev/google.golang.org/adk/v2/tool/skilltoolset/skill#Source.
    [](<https://adk.dev/skills/#__codelineno-8-18>)
    [](<https://adk.dev/skills/#__codelineno-8-19>)skillToolset, err := skilltoolset.New(ctx, skilltoolset.Config{
    [](<https://adk.dev/skills/#__codelineno-8-20>)    Source: source,
    [](<https://adk.dev/skills/#__codelineno-8-21>)})
    [](<https://adk.dev/skills/#__codelineno-8-22>)if err != nil {
    [](<https://adk.dev/skills/#__codelineno-8-23>)    // handle error
    [](<https://adk.dev/skills/#__codelineno-8-24>)}
    
## Skill processing and validation[¶](<https://adk.dev/skills/#skill-processing-and-validation> "Permanent link")

When you include skills in your agent, the agent uses a standardized process to interact with them. This process includes a system-level instruction for how to use skills, a defined format for how skills are represented, and a set of validation rules for skill definitions.

## Next steps[¶](<https://adk.dev/skills/#next-steps> "Permanent link")

Check out these resources for building agents with Skills:

  * [Skills in Python - code sample](<https://github.com/google/adk-python/tree/main/contributing/samples/environment_and_skills/skills_agent>)
  * [Skills in Go - code sample](<https://github.com/google/adk-go/tree/main/examples/skills>)
  * Agent Skills [specification documentation](<https://agentskills.io/>)

Back to top 