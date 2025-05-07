# ![Portus Logo](docs/logo.png)

## Portus: A Modular, Hexagonal Service Framework

**Portus** is a lightweight and powerful framework for building reusable, decoupled services using a hexagonal (ports and adapters) architecture. It provides a flexible lifecycle system for CRUD operations, validations, transformations, triggers, and logging via hook orchestration.

- **Live Demo**: https://portus.onrender.com/docs

---

### ✨ Key Features

- **Hexagonal Architecture**: Clear separation between business logic (ports) and infrastructure (adapters).
- **Hook Orchestrator**: Simple, async-compatible executor for validations, transformations, triggers, and logs.
- **Composable & Reusable Hooks**: Built-in hooks like validators, related field setters, hashers, etc.
- **Contextual Internal Data**: Hooks can inject flags or metadata into an internal context to alter service behavior.
- **DTO Enrichment**: Populate additional fields in output DTOs with context-bound related entities.
- **Async & Decoupled Execution**: Perform side effects (emails, logs, metrics) cleanly and safely.
- **Trace Logging**: Track changes performed on internal data (e.g., field mutations, merges, context injections).
- **FastAPIRestController**: Declarative and minimal REST interface layer that binds DTOs, hooks, and services to FastAPI routes. Promotes clean, DRY endpoint definitions with automatic support for common operations (CRUD), validation, and response formatting.
- **AsyncSQLAlchemyAdapter**: Async-ready persistence layer built on SQLAlchemy 2.x. Provides a generic, reusable repository pattern with safe transactional boundaries, filtering support, and integration with hook-based data orchestration.

---

### 🔁 Recent Refactor Highlights

The service layer has been refactored to introduce a clear separation of concerns between basic and extended CRUD use cases:

**CrudService**:
- A minimal, reusable service that encapsulates only the fundamental operations (`create`, `read`, `update`, `delete`).
- Perfect for simple entities and systems with limited business logic.
- Promotes fast onboarding and reduces cognitive load.

**AdvancedCrudService**:
- Enabling advanced behaviors like:
  - Pre/post-processing with hooks (validators, transformers, triggers).
  - Context-driven logic and side-effect orchestration (e.g., trace logs, async jobs).
  - DTO enrichment with related entities or metadata.
- Designed for complex domain logic while maintaining a clean, testable interface.

This refactor aligns with `Hexagonal Architecture principles`, supports `async-first` design, and increases codebase scalability by promoting composition and single-responsibility separation.

---

### 📁 Project Structure

```

example/        # User and Country example (DTOs, entities, service, repositories, rest-controller)
src/            # Source code
    hooks/          # Hooks categorized by feature (validator, transformer, logger, triggerer)
    core/services/  # Service base classes (DefaultService, CRUDService)
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
| `src/hooks/relations/setter.py` | How relation context is set during data transformation |
| `src/common/context_schemas.py` | Defines `RelatedFieldContext` used in relation flags |
| `src/core/services/crud.py` | Service filters relation flags and passes them to the mapper |
| `src/mappers/default.py` | Enriches DTOs with related fields using the passed flags |

---

## 📊 Internal Data Trace Logging

Portus automatically `tracks changes` performed on internal data during each service operation.

Each operation's execution path is logged as a step-by-step trace, which is useful for:

- Debugging transformations and validations
- Auditing hook behavior
- Understanding data flow across services

How to enable logging:

```python
processed_data.print_trace(logger=logger.debug, prefix="CREATE FLOW")
```

You can also change the logger, prefix, or output style depending on the context (e.g., UPDATE FLOW, DELETE FLOW, etc).

## Screenshots

## ![Logs](docs/logs.png)

Debug mode. Logs will be saved on logs/app.log
Check example/user/config/loggers.py and src/common/logger.py

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
- FastAPI
- SQLAlchemy 2.x (modo async)
- Async/Await
- Type Hints & Generics
- Pytest + Fixtures
- SQLite
- Loguru

---