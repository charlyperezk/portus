## Hexagonal Service Framework (Python)

A robust and extensible base for building service layers using the Hexagonal Architecture (Ports & Adapters). This framework abstracts the complexities of data validation, transformation, persistence and event handling into clean, reusable components.

### Key Features

- **Hexagonal Architecture**: Ports and adapters ensure clean separation of concerns and make testing a breeze.
- **Composable Lifecycle Hooks**: Easily plug in validation, data transformation and post-operation actions using simple hook objects.
- **Reusability First**: Built-in hooks for required field validation, password hashing, static fields, and more.
- **Event-Driven Behavior without Coupling**: Trigger any side effect (like sending emails) after entity creation with `EmitEventHook`, without relying on a centralized EventBus.
- **Strong Typing & Generics**: Generic base classes support any DTO and entity model while ensuring type safety.
- **Repository Abstraction**: Works with any persistence mechanism thanks to port-based repository definitions.
- **Relational Validation**: `RelationRepository` interface allows checking foreign key constraints without coupling to infrastructure.

### Typical Use

- Build reusable domain services with minimal boilerplate.
- Easily integrate domain logic with REST APIs or CLI tools.
- Rapidly prototype new business logic while keeping infrastructure swappable.

### Technologies

- Python 3.11+
- Pydantic, dataclasses, typing
- Async/Await