# Action confirmations - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools-custom/confirmation/](https://adk.dev/tools-custom/confirmation/)

[ Skip to content ](<https://adk.dev/tools-custom/confirmation/#get-action-confirmation-for-adk-tools>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools-custom/confirmation.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools-custom/confirmation/index.md> "View this page as Markdown")

# Get action confirmation for ADK Tools[¶](<https://adk.dev/tools-custom/confirmation/#get-action-confirmation-for-adk-tools> "Permanent link")

Supported in ADKPython v1.14.0TypeScript v0.2.0Go v0.3.0Experimental

Some agent workflows require confirmation for decision making, verification, security, or general oversight. In these cases, you want to get a response from a human or supervising system before proceeding with a workflow. The _Tool Confirmation_ feature in the Agent Development Kit (ADK) allows an ADK Tool to pause its execution and interact with a user or other system for confirmation or to gather structured data before proceeding. You can use Tool Confirmation with an ADK Tool in the following ways:

  * **[Boolean Confirmation](<https://adk.dev/tools-custom/confirmation/#boolean-confirmation>):** You can configure a tool with a confirmation flag or provider. This option pauses the tool for a yes or no confirmation response.
  * **[Advanced Confirmation](<https://adk.dev/tools-custom/confirmation/#advanced-confirmation>):** For scenarios requiring structured data responses, you can configure a tool with a text prompt to explain the confirmation and an expected response.

Experimental

The Tool Confirmation feature is experimental and has some [known limitations](<https://adk.dev/tools-custom/confirmation/#known-limitations>). We welcome your [feedback](<https://github.com/google/adk-python/issues/new?template=feature_request.md&labels=tool%20confirmation>)!

You can configure how a request is communicated to a user, and the system can also use [remote responses](<https://adk.dev/tools-custom/confirmation/#remote-response>) sent via the ADK server's REST API. When using the confirmation feature with the ADK web user interface, the agent workflow displays a dialog box to the user to request input, as shown in Figure 1:

![Screenshot of default user interface for tool confirmation](https://adk.dev/assets/confirmation-ui.png)

**Figure 1.** Example confirmation response request dialog box using an advanced, tool response implementation.

The following sections describe how to use this feature for the confirmation scenarios. For a complete code sample, see the [human_tool_confirmation](<https://github.com/google/adk-python/blob/fc90ce968f114f84b14829f8117797a4c256d710/contributing/samples/human_tool_confirmation/agent.py>) example. There are additional ways to incorporate human input into your agent workflow, for more details, see the [Human-in-the-loop](<https://adk.dev/workflows/patterns/#human-in-the-loop>) agent pattern.

## Boolean confirmation[¶](<https://adk.dev/tools-custom/confirmation/#boolean-confirmation> "Permanent link")

When your tool only requires a simple `yes` or `no` from the user, you can append a confirmation step. In Python, Go, and Java, you can enable this by wrapping the tool with the `FunctionTool` class and setting the `require_confirmation` parameter (or equivalent) to `True`. In TypeScript, you implement this logic manually within the `execute` function using the `ToolContext`.

The following examples show how to enable boolean confirmation:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-1>)root_agent = Agent(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-2>)    # ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-3>)    tools = [
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-4>)        # Set require_confirmation to True to require user confirmation
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-5>)        # for the tool call.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-6>)        FunctionTool(reimburse, require_confirmation=True),
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-7>)    ],
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-8>)    # ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-9>))
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-10>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-11>)# This implementation method requires minimal code, but is limited to simple
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-12>)# approvals from the user or confirming system. For a complete example of this
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-13>)# approach, see the following code sample for a more detailed example:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-0-14>)# https://github.com/google/adk-python/blob/main/contributing/samples/human_tool_confirmation/agent.py
    
Note

ADK for TypeScript currently requires manual implementation of confirmation logic within the tool's `execute` function.
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-1>)/**
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-2>) * A reimbursement tool with dynamic confirmation logic.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-3>) */
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-4>)export const reimburseTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-5>)  name: 'reimburse',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-6>)  description: 'Reimburse an amount. Large amounts (>1000) require manager approval.',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-7>)  parameters: z.object({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-8>)    amount: z.coerce.number().describe('The amount to reimburse.'),
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-9>)  }),
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-10>)  execute: async ({amount}, toolContext) => {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-11>)    // 1. Check if we already have a confirmed response.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-12>)    if (toolContext?.toolConfirmation?.confirmed) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-13>)      const isLarge = amount > 1000;
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-14>)      return {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-15>)        status: 'SUCCESS',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-16>)        message: isLarge 
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-17>)          ? `Large reimbursement of ${amount} approved by manager and processed.`
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-18>)          : `Reimbursement of ${amount} has been successfully processed.`,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-19>)      };
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-20>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-21>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-22>)    // 2. Request a tool confirmation.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-23>)    const isLarge = amount > 1000;
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-24>)    toolContext?.requestConfirmation({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-25>)      hint: isLarge 
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-26>)        ? `The amount ${amount} exceeds the $1000 limit and requires manager approval.`
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-27>)        : `Do you want to reimburse ${amount}?`,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-28>)      payload: {amount},
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-29>)    });
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-30>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-31>)    // 3. Return a status that tells the agent we are waiting.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-32>)    // Note: The model won't see this until the turn resumes after confirmation.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-33>)    return {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-34>)      status: isLarge ? 'AWAITING_MANAGER_APPROVAL' : 'AWAITING_CONFIRMATION',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-35>)      message: 'This request requires approval to proceed.',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-36>)    };
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-37>)  },
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-38>)});
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-39>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-40>)export const rootAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-41>)  name: 'Finance_Assistant',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-42>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-43>)  instruction: `You are a Finance Assistant. 
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-44>)  - You MUST use the 'reimburse' tool for ALL reimbursement requests.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-45>)  - MANDATORY: Every tool call MUST be accompanied by a text response in the same message.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-46>)  - THRESHOLD LOGIC:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-47>)    - For amounts <= 1000: Say "I am initiating the reimbursement request for [amount]. Please confirm it to proceed."
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-48>)    - For amounts > 1000: Say "I am initiating the reimbursement request for [amount]. Since this exceeds $1000, manager approval is required. Please confirm the request to submit it for review."
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-49>)  - EXAMPLES:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-50>)    User: "Reimburse me $45"
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-51>)    Model: "I am initiating the reimbursement request for 45. Please confirm it to proceed." [Tool Call: reimburse(amount=45)]
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-52>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-53>)    User: "Reimburse me $2500"
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-54>)    Model: "I am initiating the reimbursement request for 2500. Since this exceeds $1000, manager approval is required. Please confirm the request to submit it for review." [Tool Call: reimburse(amount=2500)]
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-55>)  - If the user provides a currency symbol (like $), ignore it and pass only the number to the tool.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-56>)  - In the Web UI, the user will see a 'Confirm' button. In the terminal, the user should simulate a confirmation response.`,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-57>)  tools: [reimburseTool],
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-1-58>)});
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-1>)reimburseTool, _ := functiontool.New(functiontool.Config{
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-2>)    Name:        "reimburse",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-3>)    Description: "Reimburse an amount",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-4>)    // Set RequireConfirmation to true to require user confirmation
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-5>)    // for the tool call.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-6>)    RequireConfirmation: true,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-7>)}, func(ctx tool.Context, args ReimburseArgs) (ReimburseResult, error) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-8>)    // actual implementation
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-9>)    return ReimburseResult{Status: "ok"}, nil
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-10>)})
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-11>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-12>)rootAgent, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-13>)    // ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-14>)    Tools: []tool.Tool{reimburseTool},
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-2-15>)})
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-1>)LlmAgent rootAgent = LlmAgent.builder()
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-2>)    // ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-3>)    .tools(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-4>)        // Set requireConfirmation to true to require user confirmation
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-5>)        // for the tool call.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-6>)        FunctionTool.create(myClassInstance, "reimburse", true)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-7>)    )
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-8>)    // ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-3-9>)    .build();
    
### Require confirmation function[¶](<https://adk.dev/tools-custom/confirmation/#require-confirmation-function> "Permanent link")

You can modify the behavior of the confirmation requirement by using a function that returns a boolean response based on the tool's input. In TypeScript, this is handled by adding conditional logic to your `execute` function.

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-1>)async def confirmation_threshold(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-2>)    amount: int, tool_context: ToolContext
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-3>)) -> bool:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-4>)  """Returns true if the amount is greater than 1000."""
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-5>)  return amount > 1000
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-6>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-7>)root_agent = Agent(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-8>)    # ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-9>)    tools = [
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-10>)        # Pass the threshold function to dynamically require confirmation
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-11>)        FunctionTool(reimburse, require_confirmation=confirmation_threshold),
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-12>)    ],
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-13>)    # ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-4-14>))
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-5-1>)/* 
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-5-2>)  Note: In TypeScript, dynamic threshold logic is implemented 
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-5-3>)  directly within the tool's 'execute' function as shown above.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-5-4>)*/
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-1>)reimburseTool, _ := functiontool.New(functiontool.Config{
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-2>)    Name:        "reimburse",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-3>)    Description: "Reimburse an amount",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-4>)    // RequireConfirmationProvider allows for dynamic determination
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-5>)    // of whether user confirmation is needed.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-6>)    RequireConfirmationProvider: func(args ReimburseArgs) bool {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-7>)        return args.Amount > 1000
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-8>)    },
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-9>)}, func(ctx tool.Context, args ReimburseArgs) (ReimburseResult, error) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-10>)    // actual implementation
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-11>)    return ReimburseResult{Status: "ok"}, nil
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-6-12>)})
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-1>)// In ADK Java, dynamic threshold confirmation logic is evaluated directly
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-2>)// inside the tool logic using the ToolContext rather than via a lambda parameter.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-3>)public Map<String, Object> reimburse(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-4>)    @Schema(name="amount") int amount, ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-5>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-6>)  // 1. Dynamic threshold check
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-7>)  if (amount > 1000) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-8>)    Optional<ToolConfirmation> toolConfirmation = toolContext.toolConfirmation();
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-9>)    if (toolConfirmation.isEmpty()) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-10>)       toolContext.requestConfirmation("Amount > 1000 requires approval.");
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-11>)       return Map.of("status", "Pending manager approval.");
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-12>)    } else if (!toolConfirmation.get().confirmed()) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-13>)       return Map.of("status", "Reimbursement rejected.");
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-14>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-15>)  }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-16>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-17>)  // 2. Proceed with actual tool logic
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-18>)  return Map.of("status", "ok", "reimbursedAmount", amount);
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-19>)}
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-20>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-21>)LlmAgent rootAgent = LlmAgent.builder()
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-22>)    // ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-23>)    .tools(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-24>)        // No requireConfirmation flag is set because the custom threshold
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-25>)        // logic is already handled inside the method!
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-26>)        FunctionTool.create(this, "reimburse")
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-27>)    )
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-28>)    // ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-7-29>)    .build();
    
## Advanced confirmation[¶](<https://adk.dev/tools-custom/confirmation/#advanced-confirmation> "Permanent link")

When a tool confirmation requires more details for the user or a more complex response, use a tool_confirmation implementation. This approach extends the `ToolContext` object to add a text description of the request for the user and allows for more complex response data. When implementing tool confirmation this way, you can pause a tool's execution, request specific information, and then resume the tool with the provided data.

This confirmation flow has a request stage where the system assembles and sends an input request human response, and a response stage where the system receives and processes the returned data.

### Confirmation definition[¶](<https://adk.dev/tools-custom/confirmation/#confirmation-definition> "Permanent link")

When creating a Tool with advanced confirmation, use the `Tool Context Request Confirmation` method with `hint` and `payload` parameters:

  * `hint`: Descriptive message that explains what is needed from the user.
  * `payload`: The structure of the data you expect in return. This must be serializable into a JSON-formatted string.

For a complete example of this approach, see the [human_tool_confirmation](<https://github.com/google/adk-python/blob/fc90ce968f114f84b14829f8117797a4c256d710/contributing/samples/human_tool_confirmation/agent.py>) code sample. Keep in mind that the agent workflow tool execution pauses while a confirmation is obtained. After confirmation is received, you can access the confirmation response in the `tool_confirmation.payload` object and then proceed with the execution of the workflow.

The following code shows an example implementation for a tool that processes time off requests for an employee:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-1>)def request_time_off(days: int, tool_context: ToolContext):
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-2>)    """Request day off for the employee."""
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-3>)    # ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-4>)    tool_confirmation = tool_context.tool_confirmation
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-5>)    if not tool_confirmation:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-6>)        tool_context.request_confirmation(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-7>)            hint=(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-8>)                'Please approve or reject the tool call request_time_off() by'
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-9>)                ' responding with a FunctionResponse with an expected'
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-10>)                ' ToolConfirmation payload.'
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-11>)            ),
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-12>)            payload={
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-13>)                'approved_days': 0,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-14>)            },
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-15>)        )
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-16>)        # Return intermediate status indicating that the tool is waiting for
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-17>)        # a confirmation response:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-18>)        return {'status': 'Manager approval is required.'}
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-19>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-20>)    approved_days = tool_confirmation.payload['approved_days']
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-21>)    approved_days = min(approved_days, days)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-22>)    if approved_days == 0:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-23>)        return {'status': 'The time off request is rejected.', 'approved_days': 0}
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-24>)    return {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-25>)        'status': 'ok',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-26>)        'approved_days': approved_days,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-8-27>)    }
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-1>)/**
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-2>) * A tool that requests time off for an employee.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-3>) * It uses the Advanced Confirmation pattern to request manager approval.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-4>) */
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-5>)export const requestTimeOffTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-6>)  name: 'request_time_off',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-7>)  description: 'Request days off for the employee.',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-8>)  parameters: z.object({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-9>)    days: z.number().describe('The number of days requested.'),
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-10>)  }),
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-11>)  execute: async ({days}, toolContext) => {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-12>)    const confirmation = toolContext?.toolConfirmation;
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-13>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-14>)    if (!confirmation) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-15>)      // Step 1: Request confirmation with a payload
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-16>)      toolContext?.requestConfirmation({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-17>)        hint:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-18>)          'Please approve or reject the tool call request_time_off() by ' +
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-19>)          'responding with a FunctionResponse with an expected ' +
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-20>)          'ToolConfirmation payload.',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-21>)        payload: {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-22>)          approved_days: 0,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-23>)        },
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-24>)      });
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-25>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-26>)      // Return a descriptive status to the agent
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-27>)      return {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-28>)        status: 'PENDING_MANAGER_APPROVAL',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-29>)        message: `A request for ${days} days is pending manager approval.`,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-30>)      };
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-31>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-32>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-33>)    // Step 2: Process the confirmation response
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-34>)    if (!confirmation.confirmed) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-35>)      return {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-36>)        status: 'CANCELLED',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-37>)        message: 'The request was cancelled by the user.',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-38>)      };
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-39>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-40>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-41>)    let approvedDays = (confirmation.payload as any)['approved_days'] as number;
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-42>)    approvedDays = Math.min(approvedDays, days);
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-43>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-44>)    if (approvedDays === 0) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-45>)      return {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-46>)        status: 'REJECTED',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-47>)        message: 'The time off request was rejected by the manager.',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-48>)        approved_days: 0,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-49>)      };
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-50>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-51>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-52>)    return {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-53>)      status: 'SUCCESS',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-54>)      message: `The request for ${days} days was approved (Total approved: ${approvedDays}).`,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-55>)      approved_days: approvedDays,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-56>)    };
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-57>)  },
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-58>)});
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-59>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-60>)export const rootAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-61>)  name: 'HR_Assistant',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-62>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-63>)  instruction: `You are an HR Assistant. 
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-64>)  1. Use the 'request_time_off' tool to help employees with leave requests.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-65>)  2. MANDATORY: Every tool call MUST be accompanied by a text response in the same message.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-66>)  3. EXAMPLE:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-67>)     User: "I want 5 days off"
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-68>)     Model: "I am initiating your leave request for 5 days. Management approval is required, so please confirm this request." [Tool Call: request_time_off(days=5)]
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-69>)  4. In the terminal, if they want to 'confirm', tell them to simulate a confirmation response. 
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-70>)  5. Once confirmed, the system will automatically provide the result of the approval.`,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-71>)  tools: [requestTimeOffTool],
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-9-72>)});
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-1>)func requestTimeOff(ctx tool.Context, args RequestTimeOffArgs) (map[string]any, error) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-2>)    confirmation := ctx.ToolConfirmation()
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-3>)    if confirmation == nil {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-4>)        ctx.RequestConfirmation(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-5>)            "Please approve or reject the tool call requestTimeOff() by "+
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-6>)            "responding with a FunctionResponse with an expected "+
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-7>)            "ToolConfirmation payload.",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-8>)            map[string]any{"approved_days": 0},
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-9>)        )
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-10>)        return map[string]any{"status": "Manager approval is required."}, nil
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-11>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-12>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-13>)    payload := confirmation.Payload.(map[string]any)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-14>)    // Values in map[string]any from JSON are float64 by default in Go
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-15>)    approvedDays := int(payload["approved_days"].(float64))
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-16>)    approvedDays = min(approvedDays, args.Days)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-17>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-18>)    if approvedDays == 0 {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-19>)        return map[string]any{"status": "The time off request is rejected.", "approved_days": 0}, nil
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-20>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-21>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-22>)    return map[string]any{
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-23>)        "status": "ok",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-24>)        "approved_days": approvedDays,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-25>)    }, nil
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-10-26>)}
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-1>)public Map<String, Object> requestTimeOff(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-2>)    @Schema(name="days") int days,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-3>)    ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-4>)    // Request day off for the employee.
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-5>)    // ...
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-6>)    Optional<ToolConfirmation> toolConfirmation = toolContext.toolConfirmation();
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-7>)    if (toolConfirmation.isEmpty()) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-8>)        toolContext.requestConfirmation(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-9>)            "Please approve or reject the tool call requestTimeOff() by " +
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-10>)            "responding with a FunctionResponse with an expected " +
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-11>)            "ToolConfirmation payload.",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-12>)            Map.of("approved_days", 0)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-13>)        );
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-14>)        // Return intermediate status indicating that the tool is waiting for
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-15>)        // a confirmation response:
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-16>)        return Map.of("status", "Manager approval is required.");
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-17>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-18>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-19>)    Map<String, Object> payload = (Map<String, Object>) toolConfirmation.get().payload();
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-20>)    int approvedDays = (int) payload.get("approved_days");
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-21>)    approvedDays = Math.min(approvedDays, days);
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-22>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-23>)    if (approvedDays == 0) {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-24>)        return Map.of("status", "The time off request is rejected.", "approved_days", 0);
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-25>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-26>)
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-27>)    return Map.of(
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-28>)        "status", "ok",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-29>)        "approved_days", approvedDays
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-30>)    );
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-11-31>)}
    
## Remote confirmation with REST API[¶](<https://adk.dev/tools-custom/confirmation/#remote-response> "Permanent link")

If there is no active user interface for a human confirmation of an agent workflow, you can handle the confirmation through a command-line interface or by routing it through another channel like email or a chat application. To confirm the tool call, the user or calling application needs to send a `FunctionResponse` event with the tool confirmation data.

You can send the request to the ADK API server's `/run` or `/run_sse` endpoint, or directly to the ADK runner. The following example uses a `curl` command to send the confirmation to the `/run_sse` endpoint:
    
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-1>) curl -X POST http://localhost:8000/run_sse \
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-2>) -H "Content-Type: application/json" \
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-3>) -d '{
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-4>)    "app_name": "human_tool_confirmation",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-5>)    "user_id": "user",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-6>)    "session_id": "7828f575-2402-489f-8079-74ea95b6a300",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-7>)    "new_message": {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-8>)        "parts": [
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-9>)            {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-10>)                "function_response": {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-11>)                    "id": "adk-13b84a8c-c95c-4d66-b006-d72b30447e35",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-12>)                    "name": "adk_request_confirmation",
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-13>)                    "response": {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-14>)                        "confirmed": true,
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-15>)                        "payload": {
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-16>)                            "approved_days": 5
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-17>)                        }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-18>)                    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-19>)                }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-20>)            }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-21>)        ],
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-22>)        "role": "user"
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-23>)    }
    [](<https://adk.dev/tools-custom/confirmation/#__codelineno-12-24>)}'
    
A REST-based response for a confirmation must meet the following requirements:

  * The `id` in the `function_response` should match the `function_call_id` from the `adk_request_confirmation` `FunctionCall` event.
  * The `name` should be `adk_request_confirmation`.
  * The `response` object contains the `confirmed` status and any additional `payload` data.

Note: Confirmation with Resume feature

If your ADK agent workflow is configured with the [Resume](<https://adk.dev/runtime/resume/>) feature, you also must include the Invocation ID (`invocation_id`) parameter with the confirmation response. The Invocation ID you provide must be the same invocation that generated the confirmation request, otherwise the system starts a new invocation with the confirmation response. If your agent uses the Resume feature, consider including the Invocation ID as a parameter with your confirmation request, so it can be included with the response. For more details on using the Resume feature, see [Resume stopped agents](<https://adk.dev/runtime/resume/>).

## Known limitations[¶](<https://adk.dev/tools-custom/confirmation/#known-limitations> "Permanent link")

The tool confirmation feature has the following limitations:

  * [DatabaseSessionService](<https://adk.dev/api-reference/python/google-adk.html#google.adk.sessions.DatabaseSessionService>) is not supported by this feature.
  * [VertexAiSessionService](<https://adk.dev/api-reference/python/google-adk.html#google.adk.sessions.VertexAiSessionService>) is not supported by this feature.

## Next steps[¶](<https://adk.dev/tools-custom/confirmation/#next-steps> "Permanent link")

For more information on building ADK tools for agent workflows, see [Function tools](<https://adk.dev/tools-custom/function-tools/>).

Back to top 