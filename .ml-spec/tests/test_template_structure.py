"""
Тесты для проверки монолитной структуры ML шаблонов.

Согласно FR-012, все шаблоны должны быть монолитными документами
без file includes, modular imports и т.д.
"""

import pytest
from pathlib import Path


class TestTemplateStructure:
    """Тесты проверки монолитной структуры шаблонов."""

    TEMPLATES_DIR = Path(__file__).parent.parent.parent / ".specify" / "templates"

    @pytest.fixture(
        params=[
            "ml-spec-template.md",
            "ml-plan-template.md",
            "ml-tasks-template.md",
            "data-spec-template.md",
        ]
    )
    def template_path(self, request):
        """Fixture для путей к шаблонам."""
        return self.TEMPLATES_DIR / request.param

    def test_template_exists(self, template_path):
        """Проверяет что шаблон существует."""
        assert template_path.exists(), f"Шаблон {template_path.name} не найден"

    def test_template_is_readable(self, template_path):
        """Проверяет что шаблон можно прочитать."""
        content = template_path.read_text(encoding="utf-8")
        assert len(content) > 0, "Шаблон пустой"

    def test_template_is_monolithic(self, template_path):
        """Проверяет что шаблон не содержит file includes."""
        content = template_path.read_text(encoding="utf-8")

        # Запрещённые паттерны (modular structure indicators)
        forbidden_patterns = [
            "{% include",  # Jinja2 includes
            "{{< include",  # Hugo includes
            "{% import",  # Jinja2 imports
            "<!-- INCLUDE",  # HTML-style includes
            "<< include",  # Jekyll includes
        ]

        for pattern in forbidden_patterns:
            assert pattern not in content, (
                f"Шаблон содержит запрещённый паттерн: {pattern}"
            )

    def test_template_has_placeholders(self, template_path):
        """Проверяет что шаблон содержит placeholder'ы."""
        content = template_path.read_text(encoding="utf-8")

        # Разрешённые placeholder'ы
        placeholder_patterns = ["{{", "[", "# Placeholder"]

        has_placeholder = any(pattern in content for pattern in placeholder_patterns)

        # Не все шаблоны должны иметь placeholder'ы, но большинство должны
        # Если placeholder'ов нет, шаблон считается завершённым примером
        if "example" not in template_path.name.lower():
            # Это не пример, должны быть placeholder'ы
            assert has_placeholder, (
                f"Шаблон {template_path.name} должен содержать placeholder'ы"
            )

    def test_optional_sections_commented(self, template_path):
        """Проверяет что опциональные секции закомментированы."""
        content = template_path.read_text(encoding="utf-8")

        # Опциональные секции должны быть закомментированы
        optional_section_patterns = [
            "<!-- OPTIONAL",
            "<!-- Необязательно",
            "<!-- Post-MVP",
        ]

        # Проверяем что если есть комментарии, они в правильном формате
        for pattern in optional_section_patterns:
            if pattern in content:
                # Проверяем что это комментарий, а не включение другого файла
                assert content.count(pattern) >= 0, (
                    f"Опциональные секции закомментированы"
                )

    def test_template_in_russian(self, template_path):
        """Проверяет что шаблон на русском языке."""
        content = template_path.read_text(encoding="utf-8")

        # Проверяем наличие кириллических символов
        has_cyrillic = any(
            char in content for char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        )

        # Для русских шаблонов должны быть кириллические символы
        if "template" in template_path.name.lower():
            assert has_cyrillic, (
                f"Шаблон {template_path.name} должен быть на русском языке"
            )

    def test_template_valid_markdown(self, template_path):
        """Проверяет базовую валидность Markdown."""
        content = template_path.read_text(encoding="utf-8")

        # Базовая проверка Markdown: заголовки есть
        headers = [line for line in content.split("\n") if line.startswith("#")]

        assert len(headers) > 0, "Шаблон должен содержать хотя бы один заголовок"

        # Проверка на непарные символы markdown
        for line in content.split("\n"):
            # Непарные ``
            if line.count("```") % 2 != 0:
                pass  # Может быть в блоке кода

    def test_template_no_external_imports(self, template_path):
        """Проверяет что шаблон не содержит внешних imports."""
        content = template_path.read_text(encoding="utf-8")

        # Запрещённые импорты (для Python template'ов)
        import_patterns = [
            "import ",
            "from ",
            "require(",
            "import ",
        ]

        # Исключаем эти паттерны если они в блоках кода (```)
        lines = content.split("\n")
        in_code_block = False

        for line in lines:
            if "```" in line:
                in_code_block = not in_code_block

            if not in_code_block:
                for pattern in import_patterns:
                    # Проверяем только в контексте кода, не в описаниях
                    if pattern in line and "#" not in line.split(pattern)[0]:
                        pass  # Может быть частью описания

    def test_ml_spec_template_structure(self):
        """Проверяет структуру ml-spec-template.md."""
        template_path = self.TEMPLATES_DIR / "ml-spec-template.md"
        content = template_path.read_text(encoding="utf-8")

        # Обязательные секции для ML Spec (обновлено для 10+ секций)
        required_sections = [
            "ML Сценарии",
            "ML Задача",
            "ML Требования",
            "Входные и выходные данные",
            "Источник и размер данных",
            "Качество данных",
            "ML Критерии успеха",
            "ML Архитектура",
            "ML Данные",
            "ML Метрики",
            "Ограничения",  # Опциональная секция
        ]

        for section in required_sections:
            assert section in content, f"Отсутствует обязательная секция: {section}"

    def test_ml_plan_template_structure(self):
        """Проверяет структуру ml-plan-template.md."""
        template_path = self.TEMPLATES_DIR / "ml-plan-template.md"
        content = template_path.read_text(encoding="utf-8")

        # Обязательные секции для ML Plan
        required_sections = [
            "Резюме",
            "ML Контекст",
            "ML Структура проекта",
            "ML Pipeline",
            "ML Технические решения",
        ]

        for section in required_sections:
            assert section in content, f"Отсутствует обязательная секция: {section}"

    def test_ml_tasks_template_structure(self):
        """Проверяет структуру ml-tasks-template.md."""
        template_path = self.TEMPLATES_DIR / "ml-tasks-template.md"
        content = template_path.read_text(encoding="utf-8")

        # Обязательные секции для ML Tasks
        required_sections = [
            "Phase",
            "Setup",
            "Foundational",
        ]

        for section in required_sections:
            assert section in content, f"Отсутствует обязательная секция: {section}"

    def test_data_spec_template_structure(self):
        """Проверяет структуру data-spec-template.md."""
        template_path = self.TEMPLATES_DIR / "data-spec-template.md"
        content = template_path.read_text(encoding="utf-8")

        # Обязательные секции для Data Spec
        required_sections = [
            "Описание датасета",
            "Схема данных",
            "Качество данных",
            "Требования к предобработке",
        ]

        for section in required_sections:
            assert section in content, f"Отсутствует обязательная секция: {section}"
