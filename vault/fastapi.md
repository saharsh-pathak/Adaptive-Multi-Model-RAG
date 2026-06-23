# FastAPI Reference
FastAPI is a Python web framework built for fast APIs, type hints, validation, and clear OpenAPI generation.
## 1. Overview
- FastAPI is designed around Python type annotations.
- It gives automatic request parsing and response serialization.
- It generates interactive API docs by default.
- It works well for JSON APIs and service backends.
- It supports both sync and async endpoints.
- It pairs naturally with Pydantic models.
- It favors explicit data contracts over loose request handling.
- It is productive for prototypes and production systems alike.
- It fits well when API correctness matters.
## 2. App structure
- Start with a single application object and grow from there.
- Organize routes by domain rather than by HTTP method only.
- Keep settings, routers, schemas, and services separate.
- Use modules to avoid oversized endpoint files.
- Centralize dependency wiring when it becomes repetitive.
- Put reusable business logic outside the route layer.
- Keep startup and shutdown hooks small and understandable.
- Maintain a clean boundary between transport and domain code.
- A predictable folder structure helps the team move faster.
## 3. Routes and handlers
- Use descriptive path names that match resource intent.
- Choose HTTP methods according to the action being performed.
- Return typed responses whenever practical.
- Keep handlers thin so they delegate work to services.
- Raise HTTP exceptions for expected client-facing failures.
- Keep path and query parameters explicit in the signature.
- Use status codes intentionally rather than by habit.
- Add tags and summaries to improve documentation quality.
- Route code should be easy to read without the whole project open.
## 4. Validation and models
- Pydantic models define the shape of incoming and outgoing data.
- Validation errors should be precise and user friendly.
- Use field constraints for lengths, ranges, and formats.
- Separate input models from output models when needed.
- Optional fields should be deliberate, not accidental.
- Default values should reflect actual business behavior.
- Nested models make complex payloads easier to manage.
- Serialization rules should be tested with real examples.
- Validation is part of API design, not just implementation detail.
## 5. Dependencies
- Dependencies let you inject shared behavior into routes.
- They are useful for auth, DB sessions, and settings access.
- Keep dependency functions small and focused.
- Compose dependencies when the cross-cutting concern grows.
- Dependency injection improves testability and reuse.
- It also keeps route signatures readable.
- Use lifecycle-aware dependencies for resources that need cleanup.
- Avoid hiding business rules inside generic dependencies.
- Good dependency design makes the app easier to reason about.
## 6. Database integration
- Create a clear session or connection strategy early.
- Keep transactions scoped to the work being done.
- Separate persistence models from API models when needed.
- Handle connection errors with useful responses.
- Use migrations rather than manual schema drift.
- Ensure lazy session bugs do not leak across requests.
- Make repository or service layers own query logic.
- Consider async database drivers only if the stack benefits from them.
- Measure query performance before optimizing prematurely.
## 7. Async and background work
- Async endpoints help when the workload is I/O bound.
- Do not use async just because it sounds modern.
- CPU-heavy tasks should move out of the request path.
- Background tasks are useful for small deferred actions.
- For larger jobs, use a queue or worker system.
- The event loop should stay responsive under load.
- Blocking calls inside async endpoints can erase the benefit.
- Measure where latency is actually spent before refactoring.
- Concurrency works best when the whole stack cooperates.
## 8. Testing
- Use automated tests for routes, validation, and failure cases.
- Test both success paths and rejection paths.
- Client tests should confirm response shapes and status codes.
- Fixture-based tests help keep setup readable.
- Mock external services to avoid brittle dependencies.
- Include authentication and authorization scenarios.
- Regression tests protect against contract drift.
- A small, reliable test suite is better than a large flaky one.
- FastAPI testing should reflect real request payloads.
## 9. Deployment
- Run the app behind a real ASGI server in production.
- Keep environment configuration separate from code.
- Use health checks to support orchestration and monitoring.
- Log request identifiers and errors consistently.
- Ensure startup checks fail fast when dependencies are missing.
- Container images should be small and reproducible.
- Watch concurrency, worker counts, and memory use together.
- Deployment is part of the API design because it shapes reliability.
- Version your public API before clients depend on it.
## 10. Security and performance
- Validate every request as if it could be malicious.
- Protect secrets with environment management or a vault.
- Add rate limiting if the API is exposed broadly.
- Consider CORS carefully instead of enabling it blindly.
- Cache only when you understand freshness requirements.
- Profile slow endpoints before making assumptions.
- Minimize response payloads when clients do not need extra fields.
- Secure file uploads, background jobs, and admin routes explicitly.
- Good API performance comes from measurement, not folklore.
