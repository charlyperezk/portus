# Portus

## Hexagonal Service Framework (Python)

A robust and extensible base for building service layers using the Hexagonal Architecture (Ports & Adapters). This framework abstracts the complexities of data validation, transformation, persistence, and event handling into clean, reusable components.

### Key Features

- **Hexagonal Architecture**: Ports and adapters ensure clean separation of concerns and make testing a breeze.
- **Composable Lifecycle Hooks**: Easily plug in validation, data transformation, and post-operation actions using simple hook objects.
- **Reusability First**: Built-in hooks for required field validation, password hashing, static fields, and more.
- **Event-Driven Behavior without Coupling**: Trigger any side effect (like sending emails) after entity creation with `EmitEventHook`, without relying on a centralized EventBus.
- **Parallel Execution of Validations and Triggers**: Execute validations and triggers in parallel to improve performance, especially with large datasets or heavy logic.
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

---

## Running Tests

To ensure the framework works correctly and remains reliable, we have included a suite of automated tests.

### Prerequisites

1. Ensure you have Python 3.11+ installed.
2. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install testing dependencies:

    ```bash
    pip install pytest pytest-asyncio
    ```

### Running the Tests

To run the tests, simply execute the following command from the project root:

```bash
pytest
```

This will automatically discover and run all the tests in the `tests` folder.

### Test Coverage

Tests are organized into the following categories:

- **Unit Tests**: Tests for individual functions and methods.
- **Integration Tests**: Tests that validate the integration of various components.
- **Async Tests**: Tests for asynchronous code.

Tests are automatically detected and run by `pytest`. You can specify individual tests or test modules using the `-k` option, for example:

```bash
pytest -k test_user_flow
```

### Handling Warnings

If you see warnings during test execution (such as deprecation warnings), they can be suppressed by configuring your pytest setup or using appropriate flags.

To run tests while ignoring warnings, use:

```bash
pytest -p no:warnings
```