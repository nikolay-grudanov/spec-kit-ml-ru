# Implementation Plan: ML Spec-Kit Адаптация

**Branch**: `001-ml-adaptation` | **Date**: 2026-02-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ml-adaptation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Адаптация GitHub Spec-Kit для ML/DS проектов с заменой веб-ориентированных шаблонов на ML-специфичные (data specs, model architectures, training plans). Все артефакты генерируются на русском языке с использованием смешанного подхода к техническим терминам (русское название + английский в скобках).

## Technical Context

**Language/Version**: Python 3.9+ (для CLI инструмента Specify), Markdown (для шаблонов)
**Primary Dependencies**: qwen CLI (для интеграции с AI агентом), существующая инфраструктура Spec-Kit
**Storage**: Файловая система (шаблоны в `.specify/templates/`, примеры в `.ml-spec/examples/`)
**Testing**: pytest (для CLI тестов), ручное тестирование сгенерированных артефактов
**Target Platform**: CLI инструмент (Linux/Mac/Windows)
**Project Type**: CLI инструмент / система шаблонов
**Performance Goals**: Latency < 100ms (p95), Throughput > 1 req/s, Full artifact generation < 1 minute (см. NFR-001 в spec.md)
**Constraints**: Все артефакты на русском языке, ML-ориентированная структура шаблонов, интеграция с Qwen CLI
**Scale/Scope**: 4 приоритетных шаблона для MVP (Data Spec, ML Spec, ML Plan, ML Tasks), 3 полных примера проектов (image classification, tabular classification, time series forecasting)

## Constitution Check

*GATE: Must pass before Phase 1 research. Re-check after Phase 1 design.*

### Гейты перед Phase 1:

✅ **PASS - Русскоязычность проекта**: Все генерируемые артефакты (шаблоны, примеры, документация) будут на русском языке согласно FR-002

✅ **PASS - ML Best Practices**: Шаблоны будут включать секции для reproducibility, data quality, metrics, evaluation согласно требованиямconstitution

✅ **PASS - Технологический стек**: Использование Python 3.9+ для CLI инструмента и стандартных ML библиотек в примерах

### Гейты для проверки после Phase 1 (Re-evaluated):

✅ **PASS - Структура шаблонов**: Монолитные шаблоны реализованы как единые документы без модульного разделения (FR-008). В `data-model.md` определены 4 монолитных шаблона: ML Spec, ML Plan, ML Tasks, Data Spec.

✅ **PASS - Расширяемость**: Базовые шаблоны для MVP поддерживают добавление опциональных секций (MLOps, monitoring, serving) без нарушения существующей структуры (FR-007). В `data-model.md` определены опциональные секции для Post-MVP: MLOps, Serving, Security, Compliance, Ethics.

✅ **PASS - Смешанный подход к терминам**: В `research.md` определен смешанный подход: русский текст для контента, английские термины в скобках при первом упоминании. В `contracts/commands.md` определены языковые требования для всех команд.

✅ **PASS - Примеры проектов**: В `data-model.md` определены 3 полных примера (image classification, tabular classification, time series forecasting) с обязательными секциями (spec, plan, tasks, data-spec). Каждый пример демонстрирует реальные ML сценарии.

✅ **PASS - ML Best Practices в шаблонах**: В `research.md` (Исследование 4) определено внедрение ML best practices в шаблоны:
- Reproducibility (random seed, experiment tracking)
- Data Quality (validation, leakage prevention)
- ML Workflow (baseline → EDA → feature engineering → model → evaluation)
- Metrics & Experiment Tracking (business metrics, ML metrics, logging)
- Documentation (README, model cards, docstrings)
- Deployment & MLOps (model versioning, serving)
- Ethics & Compliance (bias detection, data privacy)

✅ **PASS - Контракты команд**: В `contracts/commands.md` определены контракты для всех команд:
- `/speckit.specify` - генерация спецификации
- `/speckit.plan` - генерация плана
- `/speckit.tasks` - генерация задач
- `/speckit.clarify` - уточнение требований

✅ **PASS - Quickstart документация**: В `quickstart.md` создан краткий гайд для пользователей с примерами использования команд.

### Итоговая оценка Constitution Check:

**STATUS**: ✅ **ALL GATES PASSED**

Все требования constitution и feature spec учтены в дизайне Phase 1:
- Русскоязычность всех артефактов ✅
- Монолитные шаблоны с расширяемостью ✅
- ML Best Practices внедрены ✅
- Контракты команд определены ✅
- Примеры проектов спроектированы ✅
- Quickstart документация создана ✅

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 1 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
.specify/
├── templates/
│   ├── spec-template.md              # Шаблон спецификации ML проекта (базовый)
│   ├── plan-template.md              # Шаблон плана ML проекта (базовый)
│   ├── tasks-template.md             # Шаблон задач ML проекта (базовый)
│   ├── data-spec-template.md         # Шаблон спецификации данных (MVP)
│   ├── ml-spec-template.md           # Шаблон спецификации ML задачи (MVP)
│   ├── ml-plan-template.md           # Шаблон плана ML проекта (MVP)
│   ├── ml-tasks-template.md          # Шаблон задач ML проекта (MVP)
│   └── commands/
│       ├── specify.md                # Команда для генерации спецификации
│       ├── plan.md                   # Команда для генерации плана
│       ├── tasks.md                  # Команда для генерации задач
│       └── clarify.md                # Команда для уточнения требований

.qwen/                                # Интеграция с Qwen CLI
└── commands/
    ├── speckit.specify.toml         # Команда генерации спецификации (TOML формат)
    ├── speckit.plan.toml            # Команда генерации плана (TOML формат)
    ├── speckit.tasks.toml           # Команда генерации задач (TOML формат)
    └── speckit.clarify.toml         # Команда уточнения требований (TOML формат)

.ml-spec/                             # Примеры ML проектов
├── examples/
│   ├── image-classification/
│   │   ├── spec.md                   # Спецификация проекта классификации изображений
│   │   ├── plan.md                   # План реализации
│   │   ├── tasks.md                  # Список задач
│   │   └── data-spec.md              # Спецификация данных
│   ├── tabular-classification/
│   │   ├── spec.md                   # Спецификация табличной классификации
│   │   ├── plan.md                   # План реализации
│   │   ├── tasks.md                  # Список задач
│   │   └── data-spec.md              # Спецификация данных
│   └── time-series-forecast/
│       ├── spec.md                   # Спецификация прогнозирования временных рядов
│       ├── plan.md                   # План реализации
│       ├── tasks.md                  # Список задач
│       └── data-spec.md              # Спецификация данных

README-ML.md                           # Документация по использованию ML версии
MIGRATION-GUIDE.md                     # Руководство по миграции с оригинального Spec-Kit
CHANGELOG-ML.md                        # Журнал изменений ML версии

src/                                   # Существующий код Specify CLI (без изменений для MVP)
└── [текущая структура сохраняется]

tests/
├── templates/                         # Тесты шаблонов
│   ├── test_ml_spec_template.py
│   ├── test_ml_plan_template.py
│   ├── test_ml_tasks_template.py
│   └── test_data_spec_template.py
└── integration/
    ├── test_qwen_integration.py
    └── test_generation_workflow.py
```

**Structure Decision**: Выбрана структура Single project с сохранением существующей инфраструктуры Specify CLI. Все новые ML-специфичные файлы размещены в директориях `.specify/templates/` (для шаблонов), `.qwen/commands/` (для интеграции с Qwen CLI) и `.ml-spec/examples/` (для примеров проектов). Документация размещена в корне репозитория.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
