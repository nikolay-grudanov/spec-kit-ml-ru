# AGENTS.md

## About Spec Kit and Specify

**GitHub Spec Kit** is a comprehensive toolkit for implementing Spec-Driven Development (SDD) - a methodology that emphasizes creating clear specifications before implementation. The toolkit includes templates, scripts, and workflows that guide development teams through a structured approach to building software.

**Specify CLI** is the command-line interface that bootstraps projects with the Spec Kit framework. It sets up the necessary directory structures, templates, and AI agent integrations to support the Spec-Driven Development workflow.

The toolkit supports multiple AI coding assistants, allowing teams to use their preferred tools while maintaining consistent project structure and development practices.

---

## Build, Lint, and Test Commands

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run a single test file
pytest tests/test_extensions.py

# Run a specific test
pytest tests/test_extensions.py::test_function_name

# Run tests with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "test_manifest"
```

### Building the Package
```bash
# Build wheel and source distribution
python -m build

# Or using hatchling directly
hatchling build
```

### Installation
```bash
# Install in development mode
pip install -e .

# Install with test dependencies
pip install -e ".[test]"
```

---

## Code Style Guidelines

### Python Version
- **Required**: Python 3.11+
- Use modern Python features (e.g., match statements, union operators `|`, walrus operator `:=`)

### Import Style
```python
# Standard library imports first
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

# Third-party imports second
import typer
import httpx
from rich.console import Console
from packaging import version as pkg_version
```

### Type Hints
- Use Python 3.10+ union syntax: `str | None` instead of `Optional[str]`
- Import specific types from `typing` only when needed: `Optional[T]`, `Dict[K, V]`, `List[T]`
- Add type hints to all function parameters and return values

### Naming Conventions
```python
# Constants: UPPER_CASE with underscores
AGENT_CONFIG = {}
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell"}

# Functions and variables: snake_case
def get_key() -> str:
    selected_index = 0

# Classes: PascalCase
class ExtensionManager:
    class ExtensionError(Exception):
        pass

# Private functions: leading underscore
def _github_token(cli_token: str | None = None) -> str | None:
```

### Docstrings
Use Google-style docstrings with Args, Returns, and Raises sections:

```python
def check_tool(tool: str, tracker: StepTracker = None) -> bool:
    """Check if a tool is installed.

    Args:
        tool: Name of the tool to check
        tracker: Optional StepTracker to update with results

    Returns:
        True if tool is found, False otherwise
    """
```

### Error Handling
- Define custom exception classes for module-specific errors
- Use descriptive error messages
- Raise exceptions with context about what went wrong
- Use typer.Exit for CLI errors (clean exit with message)

```python
class ExtensionError(Exception):
    """Base exception for extension-related errors."""
    pass

class ValidationError(ExtensionError):
    """Raised when extension manifest validation fails."""
    pass
```

### File Organization
- `src/specify_cli/` - Main package source
- `tests/` - All test files (pytest convention: `test_*.py`)
- Each module should have a single responsibility
- Keep modules under 500 lines when possible

### Constants and Configuration
- Define constants at module level in UPPER_CASE
- Use `AGENT_CONFIG` dictionary as single source of truth for agent metadata
- Configuration should be externalized (YAML/TOML) rather than hardcoded

### Dependencies
- Use `pyproject.toml` for dependency management
- Pin versions only when necessary for stability
- Prefer standard library over third-party packages when feasible

---

## General Practices

- **Version management**: Any changes to `__init__.py` for the Specify CLI require a version rev in `pyproject.toml` and addition to `CHANGELOG.md`
- **Path handling**: Always use `pathlib.Path` instead of string paths
- **Cross-platform**: Code must work on Windows, macOS, and Linux (use `os.name == "nt"` for Windows checks)
- **Testing**: Write tests for all public APIs and complex logic
- **Security**: Validate user input, especially file paths and URLs (use `Path.resolve()` and path containment checks)
- **Logging**: Use `rich` for user-facing output, avoid `print()` statements

---

## Active Technologies
- **Python 3.11+** - Primary language for CLI tool
- **Markdown/TOML** - Template and command file formats
- **Rich** - Terminal output and UI
- **Typer** - CLI framework
- **pytest** - Testing framework with pytest-cov for coverage
- **hatchling** - Build backend

---

## Recent Changes
- ML adaptation: Added Python 3.9+ (now 3.11+), Markdown templates + qwen CLI integration
