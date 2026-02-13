#!/usr/bin/env python3
"""
Проверка окружения для ML Spec-Kit (Environment Check Script)
Проверяет Python, библиотеки ML и development tools.
"""

import os
import sys
from typing import Tuple, List
import subprocess


class CheckResult:
    """Результат проверки (Check result class)."""

    def __init__(self, name: str, status: str, version: str = "", error: str = ""):
        self.name = name
        self.status = status  # "✓", "✗", "⚠"
        self.version = version
        self.error = error


def check_python() -> CheckResult:
    """Проверка версии Python (Check Python version)."""
    version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    if sys.version_info >= (3, 9):
        return CheckResult("Python", "✓", version)
    else:
        return CheckResult("Python", "✗", version, "Required: >=3.9")


def check_package(package_name: str, import_name: str = None) -> CheckResult:
    """Проверка установленного пакета (Check installed package)."""
    import_name = import_name or package_name

    try:
        mod = __import__(import_name)
        version = getattr(mod, "__version__", "")
        return CheckResult(package_name, "✓", version)
    except ImportError:
        return CheckResult(package_name, "✗", "", "Not installed")


def check_tool(tool_name: str, version_flag: str = "--version") -> CheckResult:
    """Проверка установленного инструмента (Check installed tool)."""
    try:
        result = subprocess.run(
            [tool_name, version_flag], capture_output=True, text=True, timeout=5
        )
        version = result.stdout.strip().split("\n")[0]
        return CheckResult(tool_name, "✓", version)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return CheckResult(tool_name, "✗", "", "Not installed")


def check_active_env() -> CheckResult:
    """Проверка активного виртуального окружения (Check active virtual environment)."""
    if "CONDA_PREFIX" in os.environ or "CONDA_DEFAULT_ENV" in os.environ:
        return CheckResult("Package Manager", "✓", "Conda")
    elif "VIRTUAL_ENV" in os.environ:
        return CheckResult("Package Manager", "✓", "VirtualEnv")
    else:
        return CheckResult("Package Manager", "⚠", "", "No active env detected")


def check_gpu() -> List[CheckResult]:
    """Проверка доступности GPU (Check GPU availability)."""
    results = []

    try:
        import torch

        if torch.cuda.is_available():
            results.append(CheckResult("CUDA", "✓", torch.version.cuda))
            results.append(CheckResult("GPU", "✓", torch.cuda.get_device_name(0)))
        else:
            results.append(CheckResult("CUDA", "✗", "", "Not available"))
    except ImportError:
        results.append(CheckResult("CUDA", "⚠", "", "PyTorch not installed"))

    return results


def print_table(results: List[CheckResult], section_title: str):
    """Печать таблицы результатов (Print results table)."""
    print(f"\n{section_title}")
    print("=" * 50)

    for result in results:
        if result.error:
            print(f"{result.status} {result.name}: {result.error}")
        else:
            print(f"{result.status} {result.name}: {result.version}")


def get_json_output(all_results: List[CheckResult]) -> dict:
    """Convert results to JSON format for programmatic use."""
    import json

    # Build environment info
    env_info = {
        "python": {"version": "", "status": "missing"},
        "package_manager": {"type": "", "status": "missing"},
        "libraries": {},
        "tools": {},
        "gpu": {"available": False, "cuda_version": "", "device": ""},
    }

    for result in all_results:
        name_lower = result.name.lower()

        if result.name == "Python":
            env_info["python"]["version"] = result.version
            env_info["python"]["status"] = "ok" if result.status == "✓" else "missing"

        elif result.name == "Package Manager":
            env_info["package_manager"]["type"] = (
                result.version.lower()
            )  # conda, virtualenv, etc.
            env_info["package_manager"]["status"] = (
                "ok" if result.status == "✓" else "missing"
            )

        elif result.name in [
            "NumPy",
            "Pandas",
            "Scikit-learn",
            "PyTorch",
            "MLflow",
            "DVC",
        ]:
            env_info["libraries"][name_lower.replace("-", "_")] = {
                "version": result.version,
                "status": "ok" if result.status == "✓" else "missing",
            }

        elif result.name in ["pytest", "black", "mypy", "pre-commit"]:
            env_info["tools"][name_lower.replace("-", "_")] = {
                "version": result.version,
                "status": "ok" if result.status == "✓" else "missing",
            }

        elif result.name == "CUDA":
            env_info["gpu"]["available"] = result.status == "✓"
            env_info["gpu"]["cuda_version"] = result.version

        elif result.name == "GPU":
            env_info["gpu"]["device"] = result.version

    # Add summary
    env_info["summary"] = {
        "all_ok": all(r.status == "✓" for r in all_results),
        "has_errors": any(r.status == "✗" for r in all_results),
        "has_warnings": any(r.status == "⚠" for r in all_results),
        "total_checks": len(all_results),
        "passed": sum(1 for r in all_results if r.status == "✓"),
        "failed": sum(1 for r in all_results if r.status == "✗"),
        "warnings": sum(1 for r in all_results if r.status == "⚠"),
    }

    return env_info


def main():
    """Главная функция (Main function)."""
    # Check for JSON mode
    json_mode = "--json" in sys.argv

    if not json_mode:
        print("\n🔍 Проверка окружения для ML Spec-Kit")
        print("=" * 50)

    all_results = []
    has_errors = False
    has_warnings = False

    # Python
    python_result = check_python()
    all_results.append(python_result)
    if not json_mode:
        print_table([python_result], "📦 Python")

    # Active environment
    env_result = check_active_env()
    all_results.append(env_result)
    if not json_mode:
        print_table([env_result], "📦 Package Manager")

    # ML libraries
    ml_results = [
        check_package("NumPy", "numpy"),
        check_package("Pandas", "pandas"),
        check_package("Scikit-learn", "sklearn"),
        check_package("PyTorch", "torch"),
        check_package("MLflow", "mlflow"),
        check_package("DVC", "dvc"),
    ]
    all_results.extend(ml_results)
    if not json_mode:
        print_table(ml_results, "📚 ML Библиотеки")

    # Development tools
    dev_results = [
        check_tool("pytest", "--version"),
        check_tool("black", "--version"),
        check_tool("mypy", "--version"),
        check_tool("pre-commit", "--version"),
    ]
    all_results.extend(dev_results)
    if not json_mode:
        print_table(dev_results, "🛠️  Development Tools")

    # GPU (optional)
    if "--gpu" in sys.argv or "--all" in sys.argv or json_mode:
        gpu_results = check_gpu()
        all_results.extend(gpu_results)
        if not json_mode:
            print_table(gpu_results, "🎮 GPU")

    # JSON output mode
    if json_mode:
        import json

        output = get_json_output(all_results)
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # Summary
    print("\n" + "=" * 50)
    for result in all_results:
        if result.status == "✗":
            has_errors = True
        elif result.status == "⚠":
            has_warnings = True

    if has_errors:
        print("❌ Обнаружены ошибки в окружении")
        print("\n💡 Для установки недостающих пакетов:")
        print("   conda: conda env update --file .ml-spec/config/environment.yml")
        print("   pip: pip install -r .ml-spec/config/requirements-pip.txt")
        print("   uv: uv pip install -r .ml-spec/config/requirements-uv.txt")
        sys.exit(1)
    elif has_warnings:
        print("⚠️  Обнаружены предупреждения")
        sys.exit(2)
    else:
        print("✅ Окружение настроено корректно!")
        sys.exit(0)


if __name__ == "__main__":
    main()
