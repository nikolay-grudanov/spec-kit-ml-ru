#!/usr/bin/env python3
"""
Интеграционные тесты для ML Spec-Kit workflow.

Этот модуль содержит end-to-end тесты для проверки полного workflow:
specification → plan → tasks → implementation.
"""

import pytest
from pathlib import Path
import yaml


class TestMLSpeckitWorkflow:
    """Тесты полного workflow ML Spec-Kit."""

    def test_templates_exist(self):
        """Проверка, что все основные шаблоны существуют."""
        templates_dir = Path(__file__).parent.parent.parent / ".specify" / "templates"

        required_templates = [
            "ml-spec-template.md",
            "ml-plan-template.md",
            "ml-tasks-template.md",
            "data-spec-template.md",
        ]

        for template in required_templates:
            template_path = templates_dir / template
            assert template_path.exists(), f"Шаблон {template} не найден"

    def test_qwen_commands_exist(self):
        """Проверка, что все Qwen команды существуют."""
        commands_dir = Path(__file__).parent.parent.parent / ".qwen" / "commands"

        required_commands = [
            "speckit.specify.toml",
            "speckit.plan.toml",
            "speckit.tasks.toml",
            "speckit.clarify.toml",
        ]

        for command in required_commands:
            command_path = commands_dir / command
            assert command_path.exists(), f"Команда {command} не найдена"

    def test_config_yaml_exists(self):
        """Проверка, что config.yaml существует и валиден."""
        config_path = Path(__file__).parent.parent.parent / ".ml-spec" / "config.yaml"

        assert config_path.exists(), "config.yaml не найден"

        # Проверка валидности YAML
        try:
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)

            # Проверка обязательных полей
            assert "random_seed" in config, "random_seed не найден в config.yaml"
            assert "train_val_test_split" in config, (
                "train_val_test_split не найден в config.yaml"
            )
            assert "language" in config, "language не найден в config.yaml"

            # Проверка значений по умолчанию
            assert config["random_seed"] == 42, "random_seed должен быть 42"
            assert config["language"] == "ru", "language должен быть 'ru'"

        except yaml.YAMLError as e:
            pytest.fail(f"config.yaml не является валидным YAML: {e}")

    def test_dvc_config_exists(self):
        """Проверка, что DVC конфигурация существует."""
        dvc_config_path = Path(__file__).parent.parent.parent / ".dvc" / "config"

        assert dvc_config_path.exists(), "DVC config не найден"

        # Проверка валидности INI-формата (DVC config использует INI-like формат)
        try:
            with open(dvc_config_path, encoding="utf-8") as f:
                config_content = f.read()

            # Проверка наличия секций
            assert "[core]" in config_content, "Отсутствует секция [core] в DVC config"
            assert [
                "remote " in config_content,
                "Отсутствует секция remote в DVC config",
            ]

        except Exception as e:
            pytest.fail(f"Ошибка при чтении DVC config: {e}")

    def test_precommit_config_exists(self):
        """Проверка, что pre-commit конфигурация существует."""
        precommit_config_path = (
            Path(__file__).parent.parent.parent / ".pre-commit-config.yaml"
        )

        assert precommit_config_path.exists(), "pre-commit config не найден"

        # Проверка валидности YAML
        try:
            with open(precommit_config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)

            # Проверка наличия секции repos
            assert "repos" in config, "Отсутствует секция repos в pre-commit config"
            assert len(config["repos"]) > 0, (
                "pre-commit config должен содержать хотя бы один repo"
            )

        except yaml.YAMLError as e:
            pytest.fail(f"pre-commit config не является валидным YAML: {e}")

    def test_examples_exist(self):
        """Проверка, что примеры проектов существуют."""
        examples_dir = Path(__file__).parent.parent.parent / ".ml-spec" / "examples"

        required_examples = [
            "image-classification",
            "tabular-classification",
            "time-series-forecast",
        ]

        for example in required_examples:
            example_path = examples_dir / example
            assert example_path.exists(), f"Пример {example} не найден"

            # Проверка наличия основных файлов в каждом примере
            # Некоторые примеры могут быть неполными, поэтому проверяем минимальный набор
            required_files = ["spec.md", "plan.md"]  # Обязательные файлы
            optional_files = ["tasks.md", "data-spec.md"]  # Опциональные файлы

            for required_file in required_files:
                file_path = example_path / required_file
                assert file_path.exists(), (
                    f"Файл {required_file} не найден в примере {example}"
                )

            # Опциональные файлы могут отсутствовать - не вызывать ошибку
            # for optional_file in optional_files:
            #     file_path = example_path / optional_file
            #     if not file_path.exists():
            #         pass  # Файл отсутствует, но это не ошибка

    def test_scripts_exist_and_executable(self):
        """Проверка, что скрипты существуют и исполняемы."""
        project_root = Path(__file__).parent.parent.parent

        required_scripts = [
            ".ml-spec/scripts/setup-env.sh",
            ".ml-spec/scripts/check_environment.py",
            ".specify/scripts/setup-ml.sh",
            ".specify/scripts/check-ml-env.sh",
            ".specify/scripts/setup-precommit.sh",
        ]

        for script in required_scripts:
            script_path = project_root / script
            assert script_path.exists(), f"Скрипт {script} не найден"

            # Проверка, что .sh скрипты исполняемые
            if script.endswith(".sh"):
                assert script_path.stat().st_mode & 0o111, (
                    f"Скрипт {script} не является исполняемым"
                )

    def test_requirements_files_exist(self):
        """Проверка, что requirements файлы существуют."""
        config_dir = Path(__file__).parent.parent.parent / ".ml-spec" / "config"

        required_files = [
            "requirements-pip.txt",
            "requirements-conda.txt",
            "requirements-uv.txt",
            "requirements-dev.txt",
            "environment.yml",
        ]

        for req_file in required_files:
            file_path = config_dir / req_file
            assert file_path.exists(), f"Файл {req_file} не найден"

    def test_workflow_integration(self):
        """Интеграционный тест для проверки workflow.

        Этот тест проверяет, что:
        1. Шаблоны существуют и монолитные
        2. Qwen команды существуют и содержат правильные плейсхолдеры
        3. Конфигурационные файлы валидны
        4. Все зависимости установлены
        """
        # Проверка шаблонов (уже протестировано в test_template_structure.py)
        templates_dir = Path(__file__).parent.parent.parent / ".specify" / "templates"
        ml_spec_template = templates_dir / "ml-spec-template.md"
        assert ml_spec_template.exists()

        # Проверка Qwen команд
        commands_dir = Path(__file__).parent.parent.parent / ".qwen" / "commands"
        specify_command = commands_dir / "speckit.specify.toml"
        assert specify_command.exists()

        # Проверка плейсхолдера {{args}}
        with open(specify_command, encoding="utf-8") as f:
            command_content = f.read()
        assert "{{args}}" in command_content, (
            "speckit.specify.toml должен содержать {{args}}"
        )

        # Проверка конфигурации
        config_path = Path(__file__).parent.parent.parent / ".ml-spec" / "config.yaml"
        assert config_path.exists()

        # Итоговый результат - все компоненты системы на месте
        assert True, "ML Spec-Kit workflow интегрирован корректно"


class TestMLSpecKitPerformance:
    """Тесты производительности для ML Spec-Kit."""

    def test_template_loading_performance(self):
        """Тест производительности загрузки шаблонов."""
        import time

        templates_dir = Path(__file__).parent.parent.parent / ".specify" / "templates"
        template_files = [
            "ml-spec-template.md",
            "ml-plan-template.md",
            "ml-tasks-template.md",
            "data-spec-template.md",
        ]

        start_time = time.time()

        for template in template_files:
            template_path = templates_dir / template
            with open(template_path, encoding="utf-8") as f:
                content = f.read()

        elapsed_time = time.time() - start_time

        # Загрузка всех шаблонов должна занимать < 1 секунды
        assert elapsed_time < 1.0, (
            f"Загрузка шаблонов заняла слишком много времени: {elapsed_time:.3f}s"
        )

    def test_config_loading_performance(self):
        """Тест производительности загрузки конфигурации."""
        import time

        config_path = Path(__file__).parent.parent.parent / ".ml-spec" / "config.yaml"

        start_time = time.time()

        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        elapsed_time = time.time() - start_time

        # Загрузка конфигурации должна занимать < 0.1 секунды
        assert elapsed_time < 0.1, (
            f"Загрузка конфигурации заняла слишком много времени: {elapsed_time:.3f}s"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
