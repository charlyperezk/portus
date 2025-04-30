# ![Portus Logo](docs/logo.png)

## Portus: A Modular, Hexagonal Service Framework

**Portus** is a lightweight and powerful framework for building reusable, decoupled services using a hexagonal (ports and adapters) architecture. It provides a flexible lifecycle system for CRUD operations, validations, transformations, triggers, and logging via hook orchestration.

---

### ✨ Key Features

- **Hexagonal Architecture**: Clear separation between business logic (ports) and infrastructure (adapters).
- **Hook Orchestrator**: Simple, async-compatible executor for validations, transformations, triggers, and logs.
- **Composable & Reusable Hooks**: Built-in hooks like validators, related field setters, hashers, etc.
- **Contextual Internal Data**: Hooks can inject flags or metadata into an internal context to alter service behavior.
- **Passive & Active Behavior**: Easily switch between soft deletion or hard deletion by setting context flags.
- **DTO Enrichment**: Populate additional fields in output DTOs with context-bound related entities.
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
- Fluent context control using `set_context`, `get_context`, `get_flags_within_context`.
- Stronger flag typing via `ContextFlag` and `RelatedFieldContext`.
- DTO generation extended via contextual relationship injection.

---

### 📁 Project Structure

```
hooks/          # Hooks categorized by feature (validator, transformer, logger, triggerer)
core/services/  # Service base classes (DefaultService, CRUDService)
example/user/   # User domain example (DTOs, entities, service, repositories)
ports/          # Interfaces for input/output
adapters/       # Concrete implementations (e.g., in-memory repo, notification adapters)
mappers/        # Entity-to-DTO and vice versa
common/         # Shared types, internal data, context flags, exceptions
tests/          # Unit and integration tests

```
---

## 🧠 Context Flag System

Portus promotes a clean way of enriching `InternalData` with contextual metadata — without polluting domain logic or data.

### What is `context`?

Each `InternalData` object contains a `context` dictionary that allows hooks, validators, and service layers to store temporary or behavioral data.

### Why use it?

- To alter service flow (e.g., passive vs. hard deletion)
- To store cross-cutting flags (e.g., `skip_validation`)
- To provide metadata for logging or event dispatchers

## 🧩 Example: Enriching DTOs Using Context Flags

This example demonstrates how to use `InternalData` context to inject related fields into DTOs via flags.  
It follows the `Portus` flow where related context flags are isolated and passed to the mapper.

---

## 🔨 Step-by-Step

```python
# 1. Inside a hook or transformation step (see: hooks/relations/setter.py)
data: InternalData = data.set_context_flag(
    "relation_setted_country",  # <- flag key (prefixed for filtering)
    RelatedFieldContext(
        key="country",                          # <- final DTO field name
        value={"id": 1, "name": "Argentina"}    # <- related object as dict
    )
)
```

```python
# 2. Inside the service (see: core/services/crud.py)
# Retrieve only related context flags (e.g., "relation_setted_*")
related_field_flags = data.get_flags_within_context(prefix="relation_setted")

# Pass only the related flags to the mapper
read_dto = self.mapper.to_dto(entity, related_field_flags)
```

---

## 🔁 Summary of the Flow

1. ✅ A hook sets contextual data using `set_context_flag(...)`.
2. 🔍 The service filters context using `get_flags_within_context(prefix="relation_setted")`.
3. 📦 The filtered flags are passed directly to the mapper for DTO enrichment.
4. 🧩 The mapper injects the values into the DTO fields accordingly.

---

## 📁 Where to Look

| File | Description |
|------|-------------|
| `hooks/relations/setter.py` | How relation context is set during data transformation |
| `common/context_schemas.py` | Defines `RelatedFieldContext` used in relation flags |
| `core/services/crud.py` | Service filters relation flags and passes them to the mapper |
| `mappers/default.py` | Enriches DTOs with related fields using the passed flags |

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