# Model Context Protocol
MCP defines a standard way for models to talk to tools, resources, and prompts through a shared interface.
## 1. What MCP is
- MCP gives clients a common protocol for connecting to external capabilities.
- It reduces one-off integrations between apps and tool providers.
- It makes tool discovery and invocation more predictable.
- It is useful when the model needs live data or controlled actions.
- It helps separate product logic from integration plumbing.
- It supports a cleaner boundary between host, client, and server.
- It can expose files, databases, APIs, and workflows in a uniform way.
- It lowers the cost of adding a new tool source.
- It gives teams a pattern for portability across hosts.
## 2. Core architecture
- A host application owns the user experience and coordinates requests.
- A client manages the protocol connection to an MCP server.
- A server exposes capabilities such as tools, resources, and prompts.
- Each role has a narrower responsibility than a custom integration stack.
- The protocol encourages structured discovery before execution.
- The server should present a stable contract to the client.
- The host should decide policy, permissions, and UX behavior.
- The client should relay messages and state without adding business rules.
- The architecture works best when responsibilities stay explicit.
## 3. Transport and sessions
- Transports carry protocol messages between client and server.
- Session state should be handled carefully to avoid unexpected resets.
- Connection errors need clear retry and recovery behavior.
- The protocol should tolerate short interruptions gracefully.
- Message framing must be consistent so requests and responses stay aligned.
- Latency matters because interactive agents need fast tool access.
- Timeouts should be visible to users when an action stalls.
- Long-running work should be reported in a structured way.
- Logging transport events helps explain integration failures.
## 4. Tools and resources
- Tools are actions that a model can ask the server to perform.
- Resources are read-oriented entities such as files or records.
- Prompts are reusable templates that package a task shape.
- Discovery lets the client inspect what the server offers before use.
- Tool schemas should be explicit about inputs and outputs.
- Resource identifiers should be stable and descriptive.
- Keep tool names narrow so each action does one thing well.
- Separate read and write capabilities when the domain is sensitive.
- Prefer structured outputs so the model can reason over them cleanly.
## 5. Prompt design
- Prompt templates should reduce ambiguity for repetitive tasks.
- They can encode domain conventions that users should not repeat.
- Keep prompt text small enough to remain readable and auditable.
- Avoid hiding important policy inside vague instructions.
- Use prompts to standardize task setup, not to replace tool logic.
- Prompts work best when combined with clear tool descriptions.
- Treat prompt libraries as product surface, not throwaway text.
- Version prompts so you can trace behavior changes.
- Evaluate prompts against real workflows before shipping them.
## 6. Security and permissions
- Servers should expose only the capabilities a client truly needs.
- Access control should be enforced before sensitive data is returned.
- Write actions should require stronger checks than read actions.
- User consent should be clear whenever a tool changes state.
- Secrets must not be embedded directly in prompt text or logs.
- Least privilege is the right default for both clients and servers.
- Audit trails help explain who called what and when.
- Validate inputs aggressively before handing them to downstream systems.
- Treat every external server as untrusted until policy says otherwise.
## 7. Client implementation
- The client should normalize protocol details into a stable local API.
- It should hide transport mechanics from the rest of the app.
- Caching can improve speed, but stale capabilities must be refreshed.
- UI should distinguish discovery, execution, and results.
- Client code should handle partial failures without crashing the host.
- A good client exposes clear progress and error states.
- Session lifecycle management is part of client responsibility.
- Retry logic should be bounded and predictable.
- Tests should cover protocol compatibility across version changes.
## 8. Server implementation
- Servers should keep handler logic small and composable.
- Each tool handler should validate inputs before work begins.
- Resource handlers should return consistent shapes and metadata.
- Good servers document capabilities as carefully as code.
- Server logs should separate normal usage from errors.
- Backward compatibility matters when clients depend on schemas.
- Tool execution should be idempotent when possible.
- Expensive operations should report progress or status updates.
- A server should fail clearly when a capability is unavailable.
## 9. Debugging and testing
- Start with protocol traces when an integration behaves strangely.
- Check whether the client sent the right capability request.
- Verify that tool schemas match the server implementation.
- Test with minimal prompts before adding more complexity.
- Simulate missing permissions and malformed inputs early.
- Regression tests should cover both successful and failing calls.
- Debugging is easier when logs include stable request identifiers.
- Use sample servers to isolate host-side bugs from protocol bugs.
- Validate that results round-trip cleanly through serialization.
## 10. Deployment patterns
- Keep dev, staging, and production servers separate when possible.
- Expose only the servers needed for a given environment.
- Track protocol versions to avoid accidental incompatibility.
- Roll out new tools gradually and watch usage metrics.
- Favor explicit configuration over hidden defaults.
- Document which hosts connect to which servers.
- Use observability to measure latency, error rate, and saturation.
- Treat deployment as part of the product, not just infrastructure.
- Regularly review tool inventories for drift and unused endpoints.
