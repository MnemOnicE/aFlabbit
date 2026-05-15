# Behavioral Standard Library (BSL)

The **Behavioral-Standard-Library (BSL)** is a modular, terminal-agnostic Human Execution Framework designed to execute, monitor, and manage complex workflows. It features a scalable architecture designed to run seamlessly on standard systems, with special optimizations, secure hardware hooks, and graceful fallbacks for Android environments via Termux.

## Core Features

- **Execution Primitives**: Build robust, multi-step workflows utilizing the generic `Primitive` and composite `Task` interfaces.
- **Advanced State Rollback**: Every task and primitive explicitly defines automated reversal and recovery behavior ensuring safety on failure.
- **Telemetry & Safety Wrappers**: Leverage built-in decorators and context managers (`telemetry_wrapper`, `ContextManagerWrapper`) for highly observable and predictable runtime safety.
- **Native Termux Integration**: Native Python wrappers designed to interface cleanly with Android's system API (Sensors, Dialogs, Battery Status) using standard Termux binaries (`termux-sensor`, `termux-dialog`, `termux-battery-status`).

## Project Structure

The project is structured entirely inside the `src/bsl/` directory to keep a clean root directory, adhering to standard Python packaging paradigms.

```
bsl/
├── src/bsl/
│   ├── __init__.py           # Package exports
│   ├── core_primitives.py    # `Primitive` and `Task` workflows
│   ├── telemetry.py          # SystemTelemetry tracking and monitoring
│   ├── termux.py             # Android wrapper and hardware hooks
│   └── wrappers.py           # Context managers and telemetry decorators
├── tests/                    # Unittests test suite
├── pyproject.toml            # Setuptools packaging specification
├── pytest.ini                # Pytest configuration
├── ROADMAP.md                # Development Roadmap tracking
└── README.md                 # Project Documentation
```

## Installation and Usage

To install the library in editable mode for local development:

```bash
pip install -e .
```

### Basic Example

```python
from bsl.core_primitives import Primitive, Task
from bsl.wrappers import telemetry_wrapper

class ExamplePrimitive(Primitive):
    @telemetry_wrapper
    def execute(self, *args, **kwargs):
        print("Executing primitive...")
        return True

    def rollback(self):
        print("Rolling back primitive...")

# Create and run a task
task = Task(name="My First Workflow")
task.add_primitive(ExamplePrimitive())

results = task.execute()
print(f"Task status: {task.status}")
```

### Termux Hardware API Example

```python
from bsl.termux import TermuxAPI

# Fails gracefully (returns None) on non-Termux systems
api = TermuxAPI()
battery_info = api.get_battery_status()

if battery_info:
    print(f"Battery: {battery_info['percentage']}%")
```

## Testing & Linting

BSL enforces strict standard compliance (`10.00/10` `pylint` and 0 `flake8` errors). The test suite does not require any external dependencies and operates on standard `unittest`. Tests can be executed seamlessly using `pytest`.

```bash
pytest
pylint src tests
flake8 src tests
```

See [ROADMAP.md](./ROADMAP.md) for more details regarding upcoming features and integrations.
