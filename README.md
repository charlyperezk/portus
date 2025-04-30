# ![Portus Logo](docs/logo.png)

## Portus: A Modular, Hexagonal Service Framework

**Portus** is a lightweight and powerful framework for building reusable, decoupled services using a hexagonal (ports and adapters) architecture. It provides a flexible lifecycle system for CRUD operations, validations, transformations, triggers, and logging via hook orchestration.

---

### ✨ Key Features

- **Hexagonal Architecture**: Clear separation between business logic (ports) and infrastructure (adapters).
- **Hook Orchestrator**: Simple, async-compatible executor for validations, transformations, triggers, and logs.
- **Composable & Reusable Hooks**: Built-in hooks like validators, related field setters, hashers, etc.
- **Context-Aware Internal Data**: Easily enrich your domain data with contextual or related fields.
- **Async & Decoupled Execution**: Perform side effects (emails, logs, metrics) cleanly and safely.

---

### 🔁 Recent Refactor Highlights

**Previous Version**:
- Depended on `LifeCycle`, `CompositeHook`, and nested lifecycle logic.
- Service logic was tightly coupled with hook management.

**Current Version**:
- Uses a centralized `HookOrchestrator` for managing lifecycle logic.
- Introduces a declarative and functional model:
  - `DataValidatorHook`
  - `DataTransformerHook`
  - `DataTriggererHook`
  - `LogCompositorHook`
- Simpler `CRUDService` with rich context merging and DTO enrichment.

---

### 📁 Project Structure

```
hooks/          # Hooks categorized by feature (validator, transformer, logger, triggerer)
core/services/  # Service base classes (DefaultService, CRUDService)
example/user/   # User domain example (DTOs, entities, service, repositories)
ports/          # Interfaces for input/output
adapters/       # Concrete implementations (e.g., in-memory repo, notification adapters)
mappers/        # Entity-to-DTO mappers
common/         # Shared types, internal data, exceptions
tests/          # Unit and integration tests
```
---

## Context Usage Guidelines

Portus introduces a lightweight mechanism for passing auxiliary execution flags or metadata during the processing of internal data, without polluting the core business fields.

### What is `context`?

Each `InternalData` object contains a `context` dictionary that allows hooks, validators, and service layers to store temporary or behavioral data.

### Why use it?

- To alter service flow (e.g., passive vs. hard deletion)
- To store cross-cutting flags (e.g., `skip_validation`)
- To provide metadata for logging or event dispatchers

### Example

```python
data = data.with_context("pasive_deletion", True)

if "pasive_deletion" in data.get_context():
    await self._persist(...)
else:
    self.repository.delete(id)
```
---

### 🧪 Running Tests

```bash
pytest
```

Install dependencies first:

```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio
```

---

### 🛠️ Tech Stack

- Python 3.11+
- Pydantic v2
- Async/Await
- Type Hints & Generics
- Pytest + Fixtures

---