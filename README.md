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

### Folder Structure
<pre markdown>```
├── .gitignore                      # Files/directories to ignore in Git commits
├── AUTHORS.rst                     # Project authors and contributors
├── LICENSE.TXT                     # Project license (e.g., MIT)
├── README.md                       # High‑level overview, install & usage instructions
├── adapters                        # Ports & Adapters layer
│   ├── __init__.py
│   ├── input                       # HTTP/CLI controllers, web handlers, etc.
│   │   └── __init__.py
│   └── output                      # Infrastructure implementations
│       ├── __init__.py
│       ├── in_memory               # In‑memory repo implementations for tests
│       │   ├── __init__.py
│       │   ├── base.py             # Generic CRUD repo interface
│       │   └── related_repo_base.py# In‑memory RelationRepository
│       └── notifications.py        # Adapter for sending emails, SMS, etc.
├── common                          # Shared core utilities
│   ├── __init__.py
│   ├── internal_data.py            # Immutable InternalData class
│   └── types.py                    # TypeVars, aliases (TInternalData, T_ID…)
├── core                            # Domain‑agnostic core logic
│   ├── __init__.py
│   └── services
│       ├── __init__.py
│       └── default.py              # Generic Service base class
├── docs                            # Static documentation assets
│   └── flow_example.png            # Visual flowchart of create/update lifecycle
├── example                         # Sample “User” domain demonstrating usage
│   └── user
│       ├── dtos
│       │   ├── __init__.py
│       │   ├── country_dtos.py     # Pydantic Create/Read/Update DTOs
│       │   └── user_dtos.py
│       ├── entities
│       │   ├── __init__.py
│       │   ├── country.py          # Dataclass domain model
│       │   └── user.py
│       ├── repositories
│       │   ├── __init__.py
│       │   ├── country_repository.py
│       │   └── user_repository.py  # Concrete CrudRepository implementations
│       └── service
│           ├── __init__.py
│           ├── hooks.py            # Lifecycle hooks map for UserService
│           └── methods             # Jinja‑generated create/update/delete code
│               ├── __init__.py
│               ├── country_setter.py
│               ├── create.py
│               ├── delete.py
│               └── update.py
│           └── user_service.py     # UserService extends core Service
├── hooks                           # Core, reusable hook implementations
│   ├── __init__.py
│   ├── base
│   │   ├── __init__.py
│   │   ├── hook.py                 # Hook & AsyncHook protocols
│   │   └── life_cycle.py           # CompositeHook, LifeCycle orchestration
│   ├── core
│   │   ├── __init__.py
│   │   ├── setters                 # Data enrichment hooks
│   │   │   ├── __init__.py
│   │   │   ├── compute_fields.py   # ComputedFieldsHook
│   │   │   ├── related_field.py    # RelationResolverHook
│   │   │   ├── static_setter.py    # StaticFieldSetterHook
│   │   │   └── utils.py            # Pure functions for setters
│   │   └── validators              # Validation hooks
│   │       ├── __init__.py
│   │       ├── related_exists.py   # RelationExistsHook
│   │       └── required_fields.py  # RequiredFieldsHook
│   ├── functions                   # Pure functions used by hooks
│   │   ├── __init__.py
│   │   ├── id_generation.py        # assign_id()
│   │   ├── security.py             # hash_password()
│   │   ├── send_email.py           # send_email()
│   │   └── timestamp.py            # set_timestamp()
│   └── triggers                    # Side‑effect hooks
│       ├── __init__.py
│       └── emit_event.py           # EmitEventHook for post‑action callbacks
├── main.py                         # Entry point wiring-up example services
├── mappers                         # Mapping between DTOs, entities & internal data
│   ├── __init__.py
│   ├── base.py                     # Mapper interface
│   └── default.py                  # DefaultMapper implementation
├── ports                           # Port definitions (input/output interfaces)
│   ├── __init__.py
│   ├── input
│   │   ├── __init__.py
│   │   └── crud.py                 # CRUDPort for service layer
│   └── output
│       ├── __init__.py
│       ├── notifications.py        # NotificationPort interface
│       └── repository
│           ├── __init__.py
│           ├── related_repository.py
│           └── repository.py       # CrudRepository interface
├── pyproject.toml                  # Build config, dependencies
└── test                            # Test suite root
    └── conftest.py                 # Fixtures (in-memory repos, sample DTOs, etc.)
</pre>
### Typical Use

- Build reusable domain services with minimal boilerplate.
- Easily integrate domain logic with REST APIs or CLI tools.
- Rapidly prototype new business logic while keeping infrastructure swappable.

### Technologies

- Python 3.11+
- Pydantic, dataclasses, typing
- Async/Await