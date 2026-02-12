# API Contracts: ML Spec-Kit Команды

**Branch**: `001-ml-adaptation` | **Date**: 2026-02-13 | **Spec**: [spec.md](./spec.md)

## Overview

Документ описывает контракты для команд ML Spec-Kit. Команды интегрированы с Qwen CLI и используют TOML формат командных файлов.

---

## Command 1: `/speckit.specify` - Генерация спецификации

### Описание

Команда для генерации спецификации ML проекта на основе описания пользователя. Использует шаблон `.specify/templates/ml-spec-template.md`.

### Входные параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `description` | String | Да | Описание ML проекта на русском языке |
| `output_file` | String | Нет | Путь для сохранения спецификации (по умолчанию: `spec.md`) |

### Пример использования

```bash
/speckit.specify Создать систему классификации изображений для определения типов одежды на основе датасета Fashion MNIST. Требуется точность (accuracy) не менее 90%.
```

### Выходные данные

**Формат**: Markdown файл

**Структура**:
```markdown
# Спецификация ML проекта: [Название]

## Бизнес-цель
- Описание бизнес-проблемы
- Ожидаемая ценность
- Success criteria

## Задача машинного обучения
- Тип задачи (классификация, регрессия, кластеризация и т.д.)
- Входные данные (Input)
- Выходные данные (Output)
- Тип обучения (supervised, unsupervised, reinforcement)

## Данные
- Источник данных
- Размер и структура
- Качество данных
- Требования к предобработке

## Метрики
- Бизнес-метрики
- ML метрики
- Success thresholds

## Ограничения
- Latency требования
- Hardware ограничения
- Производительность модели
```

### Контракт (OpenAPI-like)

```yaml
openapi: 3.0.0
info:
  title: ML Spec-Kit Command API
  version: 1.0.0
  description: API для команд ML Spec-Kit

paths:
  /speckit.specify:
    post:
      summary: Генерация спецификации ML проекта
      description: Использует Qwen CLI для генерации спецификации на основе шаблона
      operationId: generateSpec
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                description:
                  type: string
                  description: Описание ML проекта
                  example: "Создать систему классификации изображений для определения типов одежды"
                output_file:
                  type: string
                  description: Путь для сохранения спецификации
                  default: "spec.md"
                  example: "spec.md"
              required:
                - description
      responses:
        '200':
          description: Спецификация успешно сгенерирована
          content:
            text/markdown:
              schema:
                type: string
                example: |
                  # Спецификация ML проекта: Классификация одежды
                  
                  ## Бизнес-цель
                  ...
        '400':
          description: Некорректные входные данные
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Описание проекта не может быть пустым"
```

### Валидация

- `description` не должен быть пустым
- `description` должен быть на русском языке
- `output_file` должен иметь расширение `.md`
- Минимальная длина `description`: 10 символов

---

## Command 2: `/speckit.plan` - Генерация плана

### Описание

Команда для генерации плана реализации ML проекта на основе существующей спецификации. Использует шаблон `.specify/templates/ml-plan-template.md`.

### Входные параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `spec_file` | String | Да | Путь к файлу спецификации |
| `output_file` | String | Нет | Путь для сохранения плана (по умолчанию: `plan.md`) |

### Пример использования

```bash
/speckit.plan spec.md
```

### Выходные данные

**Формат**: Markdown файл

**Структура**:
```markdown
# План реализации ML проекта: [Название]

## Архитектура решения
- Data pipeline
- Model architecture
- Training strategy
- Serving strategy

## Этапы реализации
- Этап 1: EDA (Exploratory Data Analysis)
- Этап 2: Baseline модель
- Этап 3: Feature engineering
- Этап 4: Основная модель
- Этап 5: Evaluation и error analysis

## Технологический стек
- Data processing
- ML фреймворки
- Experiment tracking
- Deployment
```

### Контракт (OpenAPI-like)

```yaml
paths:
  /speckit.plan:
    post:
      summary: Генерация плана реализации ML проекта
      description: Использует Qwen CLI для генерации плана на основе спецификации
      operationId: generatePlan
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                spec_file:
                  type: string
                  description: Путь к файлу спецификации
                  example: "spec.md"
                output_file:
                  type: string
                  description: Путь для сохранения плана
                  default: "plan.md"
                  example: "plan.md"
              required:
                - spec_file
      responses:
        '200':
          description: План успешно сгенерирован
          content:
            text/markdown:
              schema:
                type: string
                example: |
                  # План реализации ML проекта: Классификация одежды
                  
                  ## Архитектура решения
                  ...
        '400':
          description: Некорректные входные данные
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Файл спецификации не найден"
        '404':
          description: Файл спецификации не найден
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Файл spec.md не существует"
```

### Валидация

- `spec_file` должен существовать
- `spec_file` должен быть валидным Markdown файлом
- `spec_file` должен содержать обязательные секции (Бизнес-цель, Задача ML, Данные, Метрики)
- `output_file` должен иметь расширение `.md`

---

## Command 3: `/speckit.tasks` - Генерация задач

### Описание

Команда для генерации списка задач ML проекта на основе существующего плана. Использует шаблон `.specify/templates/ml-tasks-template.md`.

### Входные параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `plan_file` | String | Да | Путь к файлу плана |
| `output_file` | String | Нет | Путь для сохранения задач (по умолчанию: `tasks.md`) |

### Пример использования

```bash
/speckit.tasks plan.md
```

### Выходные данные

**Формат**: Markdown файл

**Структура**:
```markdown
# Задачи ML проекта: [Название]

## Подготовка данных
- Загрузка данных
- Data quality checks
- Разделение на train/val/test

## EDA и feature engineering
- Анализ распределений
- Feature selection
- Feature creation

## Моделирование
- Baseline модель
- Основная модель
- Hyperparameter tuning

## Оценка и документация
- Метрики и графики
- Error analysis
- Model card
```

### Контракт (OpenAPI-like)

```yaml
paths:
  /speckit.tasks:
    post:
      summary: Генерация списка задач ML проекта
      description: Использует Qwen CLI для генерации задач на основе плана
      operationId: generateTasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                plan_file:
                  type: string
                  description: Путь к файлу плана
                  example: "plan.md"
                output_file:
                  type: string
                  description: Путь для сохранения задач
                  default: "tasks.md"
                  example: "tasks.md"
              required:
                - plan_file
      responses:
        '200':
          description: Задачи успешно сгенерированы
          content:
            text/markdown:
              schema:
                type: string
                example: |
                  # Задачи ML проекта: Классификация одежды
                  
                  ## Подготовка данных
                  ...
        '400':
          description: Некорректные входные данные
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Файл плана не найден"
        '404':
          description: Файл плана не найден
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Файл plan.md не существует"
```

### Валидация

- `plan_file` должен существовать
- `plan_file` должен быть валидным Markdown файлом
- `plan_file` должен содержать обязательные секции (Архитектура решения, Этапы реализации)
- `output_file` должен иметь расширение `.md`

---

## Command 4: `/speckit.clarify` - Уточнение требований

### Описание

Команда для уточнения требований к ML проекту. Используется для получения дополнительных деталей от пользователя и дополнения существующей спецификации.

### Входные параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `spec_file` | String | Да | Путь к файлу спецификации |
| `question` | String | Да | Вопрос или запрос на уточнение |
| `output_file` | String | Нет | Путь для сохранения обновленной спецификации (по умолчанию: перезаписывает `spec_file`) |

### Пример использования

```bash
/speckit.clarify spec.md Какие конкретные метрики качества данных важны для этого проекта?
```

### Выходные данные

**Формат**: Markdown файл

**Структура**: Обновленная спецификация с добавленными деталями.

### Контракт (OpenAPI-like)

```yaml
paths:
  /speckit.clarify:
    post:
      summary: Уточнение требований ML проекта
      description: Использует Qwen CLI для уточнения и дополнения спецификации
      operationId: clarifyRequirements
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                spec_file:
                  type: string
                  description: Путь к файлу спецификации
                  example: "spec.md"
                question:
                  type: string
                  description: Вопрос или запрос на уточнение
                  example: "Какие конкретные метрики качества данных важны для этого проекта?"
                output_file:
                  type: string
                  description: Путь для сохранения обновленной спецификации
                  example: "spec.md"
              required:
                - spec_file
                - question
      responses:
        '200':
          description: Спецификация успешно обновлена
          content:
            text/markdown:
              schema:
                type: string
                example: |
                  # Спецификация ML проекта: Классификация одежды
                  
                  ## Бизнес-цель
                  ...
                  
                  ## Метрики качества данных (добавлено)
                  ...
        '400':
          description: Некорректные входные данные
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Вопрос не может быть пустым"
        '404':
          description: Файл спецификации не найден
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Файл spec.md не существует"
```

### Валидация

- `spec_file` должен существовать
- `spec_file` должен быть валидным Markdown файлом
- `question` не должен быть пустым
- `question` должен быть на русском языке
- Минимальная длина `question`: 5 символов

---

## Общие правила валидации

### Языковые требования

1. **Входные данные**: Все описания и вопросы должны быть на русском языке
2. **Выходные данные**: Все сгенерированные артефакты должны быть на русском языке
3. **Технические термины**: Дублировать на английском в скобках при первом упоминании

### Формат файлов

1. **Markdown**: Все выходные файлы должны быть в формате Markdown (.md)
2. **Кодировка**: UTF-8
3. **Строка перевода**: Unix (LF)

### Проверка существования файлов

1. **Spec file**: Должен существовать для команд `/speckit.plan` и `/speckit.clarify`
2. **Plan file**: Должен существовать для команды `/speckit.tasks`
3. **Template files**: Должны существовать в `.specify/templates/`

### Обработка ошибок

1. **Файл не найден**: Вернуть HTTP 404 с описанием ошибки
2. **Некорректные входные данные**: Вернуть HTTP 400 с описанием ошибки
3. **Ошибка генерации**: Вернуть HTTP 500 с описанием ошибки

---

## Интеграция с Qwen CLI

### Формат командных файлов (TOML)

Пример для `/speckit.specify`:

```toml
description = "Генерация спецификации ML проекта"

[prompt]
template = """
Используй шаблон `.specify/templates/ml-spec-template.md` для генерации спецификации ML проекта на основе следующего описания: {{description}}

Требования:
- Все артефакты на русском языке
- Технические термины дублировать на английском в скобках при первом упоминании
- Включить секции: бизнес-цель, данные, метрики, ограничения
"""

[arguments]
description = { type = "string", required = true }
output_file = { type = "string", default = "spec.md" }
```

### Структура директорий

```
.qwen/
└── commands/
    ├── speckit.specify.md    # Команда для генерации спецификации
    ├── speckit.plan.md       # Команда для генерации плана
    ├── speckit.tasks.md      # Команда для генерации задач
    └── speckit.clarify.md    # Команда для уточнения требований
```

### Плейсхолдеры

- `{{description}}`: Описание проекта (для `/speckit.specify`)
- `{{spec_file}}`: Путь к спецификации (для `/speckit.plan` и `/speckit.clarify`)
- `{{plan_file}}`: Путь к плану (для `/speckit.tasks`)
- `{{question}}`: Вопрос для уточнения (для `/speckit.clarify`)

---

## Пример полного workflow

```bash
# Шаг 1: Генерация спецификации
/speckit.specify Создать систему классификации изображений для определения типов одежды на основе датасета Fashion MNIST. Требуется точность (accuracy) не менее 90%.

# Шаг 2: Генерация плана на основе спецификации
/speckit.plan spec.md

# Шаг 3: Генерация задач на основе плана
/speckit.tasks plan.md

# Шаг 4 (опционально): Уточнение требований
/speckit.clarify spec.md Какие конкретные метрики качества данных важны для этого проекта?

# Шаг 5 (опционально): Перегенерация плана после уточнения
/speckit.plan spec.md
```

---

## Дополнительные команды (Post-MVP)

### `/speckit.data-spec` - Генерация спецификации данных

**Описание**: Команда для генерации спецификации данных.

**Входные параметры**:
- `description`: Описание датасета
- `output_file`: Путь для сохранения (по умолчанию: `data-spec.md`)

### `/speckit.eval-plan` - Генерация плана оценки

**Описание**: Команда для генерации плана оценки модели.

**Входные параметры**:
- `spec_file`: Путь к спецификации
- `output_file`: Путь для сохранения (по умолчанию: `eval-plan.md`)

---

**Версия**: 1.0 | **Дата**: 2026-02-13 | **Статус**: Завершено
