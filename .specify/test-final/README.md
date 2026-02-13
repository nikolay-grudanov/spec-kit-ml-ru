# test-final

## Описание

ML проект: test-final

## Быстрый старт

1. Настройка окружения:
    ```bash
    make setup
    # Или:
    bash .ml-spec/scripts/setup-env.sh
    ```

2. Установка зависимостей:
   ```bash
   pip install -r ../../.ml-spec/config/requirements-pip.txt
   ```

3. Запуск экспериментов:
   ```bash
   jupyter notebook notebooks/01_eda.ipynb
   ```

## Структура проекта

- `data/` - Данные проекта
  - `raw/` - Исходные данные (read-only)
  - `processed/` - Обработанные данные
  - `external/` - Внешние источники
- `notebooks/` - Jupyter notebooks
- `src/` - Исходный код
  - `data/` - Загрузка и обработка данных
  - `models/` - Модели
  - `evaluation/` - Оценка моделей
  - `utils/` - Утилиты
- `tests/` - Тесты
  - `unit/` - Unit тесты
  - `integration/` - Integration тесты
  - `data_quality/` - Тесты качества данных
- `configs/` - Конфигурации экспериментов
- `models/` - Сохраненные модели
- `results/` - Графики и отчёты
- `logs/` - Логи

## Документация

Для генерации спецификации, плана и задач используйте команды Qwen CLI:
- `/speckit.specify <описание проекта>` - Генерация ML спецификации
- `/speckit.plan` - Генерация ML плана реализации
- `/speckit.tasks` - Генерация списка задач
- `/speckit.clarify` - Уточнение требований

## Быстрый старт (Quick Start)

Используйте Makefile для упрощенного workflow:
- `make help` - Показать все доступные команды
- `make setup` - Настроить ML окружение
- `make check` - Проверить окружение
- `make init <project-name>` - Создать новый ML проект
- `make test` - Запустить тесты
- `make lint` - Проверить код стиль

## Конфигурация

Основные настройки находятся в `config.yaml`.
Дополнительные настройки в `configs/experiment.yaml` и `configs/model_config.yaml`.
