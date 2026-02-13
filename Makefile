.PHONY: help setup check clean

# Default target
help:
	@echo "ML Spec-Kit Make Commands"
	@echo "========================"
	@echo ""
	@echo "Available targets:"
	@echo "  make setup    - Setup ML environment"
	@echo "  make check     - Check environment"
	@echo "  make init      - Create new ML project"
	@echo "  make clean     - Clean temporary files"
	@echo ""
	@echo "Examples:"
	@echo "  make setup"
	@echo "  make init my-project"
	@echo ""

# Setup ML environment
setup:
	@echo "🚀 Setting up ML environment..."
	@bash .ml-spec/scripts/setup-env.sh

# Check environment
check:
	@echo "🔍 Checking environment..."
	@python3 .ml-spec/scripts/check_environment.py

# Check environment with GPU
check-gpu:
	@echo "🔍 Checking environment with GPU..."
	@python3 .ml-spec/scripts/check_environment.py --gpu

# Initialize new ML project
init:
	@echo "❌ Error: Project name required"
	@echo "Usage: make init <project-name>"
	@echo "Example: make init my-ml-project"
	@exit 1

# Initialize with project name
%:
	@if [ -z "$*" ]; then \
		echo "❌ Error: Project name required"; \
		echo "Usage: make init <project-name>"; \
		exit 1; \
	fi
	@echo "🚀 Initializing ML project: $*"
	@bash .specify/scripts/setup-ml.sh $*

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✓ Temporary files cleaned"

# Install pre-commit hooks
pre-commit:
	@echo "🔧 Installing pre-commit hooks..."
	@bash .specify/scripts/setup-precommit.sh

# Run tests
test:
	@echo "🧪 Running tests..."
	@python3 -m pytest tests/ -v --cov=src --cov-report=term-missing

# Run tests with coverage report
test-coverage:
	@echo "🧪 Running tests with coverage..."
	@python3 -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
	@echo "✓ Coverage report generated: htmlcov/index.html"

# Lint code
lint:
	@echo "🔍 Linting code..."
	@black src/ tests/ --check
	@mypy src/ --strict
	@flake8 src/ tests/

# Format code
format:
	@echo "✨ Formatting code..."
	@black src/ tests/
	@isort src/ tests/ --profile black

# Type check
type-check:
	@echo "🔍 Type checking code..."
	@mypy src/ --strict

# Run pre-commit on all files
pre-commit-all:
	@echo "🔧 Running pre-commit on all files..."
	@pre-commit run --all-files

# DVC commands
dvc-init:
	@echo "📦 Initializing DVC..."
	@dvc init

dvc-add-data:
	@echo "📦 Adding data to DVC..."
	@dvc add data/raw data/processed

dvc-push:
	@echo "📤 Pushing data to remote..."
	@dvc push

dvc-pull:
	@echo "📥 Pulling data from remote..."
	@dvc pull
