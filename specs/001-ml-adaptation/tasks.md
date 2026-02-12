# Задачи: Адаптация Spec-Kit для ML Проектов

**Input**: Design documents from `/specs/001-ml-adaptation/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/commands.md, quickstart.md

**Формат**: `[ID] [P?] [Story] Description`

- **[P]**: Можно выполнить параллельно (разные файлы, без зависимостей)
- **[Story]**: Какой user story принадлежит задача (US1, US2, US3)
- В описаниях указаны точные пути к файлам

**Организация**: Задачи сгруппированы по фазам для последовательной реализации.

---

## Фаза 1: Подготовка Инфраструктуры

**Цель:** Создать базовую структуру директорий и конфигурационные файлы
**Duration:** 5 дней (40 часов)

### Задача 1.1: Создать структуру директорий

**Файл:** `.specify/templates/`, `.qwen/commands/`, `.ml-spec/examples/`
**Описание:** Создать базовую структуру директорий для шаблонов, команд и примеров
**Dependencies:** None
**Estimated Time:** 2 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Директория `.specify/templates/` создана
- [ ] Директория `.qwen/commands/` создана
- [ ] Директория `.ml-spec/examples/` создана
- [ ] Директория `.ml-spec/examples/image-classification/` создана
- [ ] Директория `.ml-spec/examples/tabular-classification/` создана
- [ ] Директория `.ml-spec/examples/time-series-forecast/` создана

**Testing:**
```bash
test -d .specify/templates/ && echo "✓ .specify/templates/ существует"
test -d .qwen/commands/ && echo "✓ .qwen/commands/ существует"
test -d .ml-spec/examples/ && echo "✓ .ml-spec/examples/ существует"
```

---

### Задача 1.2: Создать конфигурационный файл

**Файл:** `.ml-spec/config.yaml`
**Описание:** Создать конфигурационный файл с настройками по умолчанию
**Dependencies:** 1.1
**Estimated Time:** 3 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл `.ml-spec/config.yaml` создан
- [ ] Секция `random_seed` со значением 42
- [ ] Секция `train_val_test_split` с пропорциями 0.70/0.15/0.15
- [ ] Секция `language` со значением `ru`
- [ ] YAML синтаксис валиден

**Testing:**
```bash
test -f .ml-spec/config.yaml && echo "✓ config.yaml существует"
python3 -c "import yaml; yaml.safe_load(open('.ml-spec/config.yaml'))" && echo "✓ YAML валиден"
```

---

### Задача 1.3: Настроить pre-commit hooks

**Файл:** `.pre-commit-config.yaml`, `.specify/scripts/setup-precommit.sh`
**Описание:** Настроить pre-commit hooks для автоматической проверки качества кода согласно Constitution #3
**Dependencies:** 1.1
**Estimated Time:** 3 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл `.pre-commit-config.yaml` создан с hooks: black, flake8, isort, mypy
- [ ] Скрипт `.specify/scripts/setup-precommit.sh` создан для установки hooks
- [ ] README.md обновлён с инструкциями по установке pre-commit
- [ ] Hooks проходят успешно на текущем коде

**Testing:**
```bash
pre-commit install
pre-commit run --all-files
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ Все pre-commit проверки пройдены"
```

---

**Итог по Фазе 1:** Задачи: 3, Время: 8 часов


---

## Фаза 2: Core ML Templates

**Цель:** Создать 4 основных ML шаблона для MVP
**Duration:** 15 дней (120 часов)

### Задача 2.1: Создать ml-spec-template.md

**Файл:** `.specify/templates/ml-spec-template.md`
**Описание:** Создать шаблон спецификации ML проекта с 10 основными секциями
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл создан
- [ ] Все 10 секций присутствуют
- [ ] Placeholder'ы в формате {{VARIABLE}}
- [ ] Примеры заполнения для каждой секции
- [ ] Весь текст на русском языке
- [ ] Технические термины: "Русский (English)"
- [ ] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/ml-spec-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/ml-spec-template.md
grep -E '\{\{[A-Z_]+\}\}' .specify/templates/ml-spec-template.md
```

---

### Задача 2.2: Создать ml-plan-template.md

**Файл:** `.specify/templates/ml-plan-template.md`
**Описание:** Создать шаблон плана реализации ML проекта
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл создан
- [ ] Секция "Архитектура решения" с подразделами
- [ ] Секция "Этапы реализации" с 5 этапами
- [ ] Секция "Технологический стек" с подразделами
- [ ] Placeholder'ы в формате {{VARIABLE}}
- [ ] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/ml-plan-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/ml-plan-template.md
grep "Этап 1: EDA" .specify/templates/ml-plan-template.md
```

---

### Задача 2.3: Создать ml-tasks-template.md

**Файл:** `.specify/templates/ml-tasks-template.md`
**Описание:** Создать шаблон списка задач ML проекта
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл создан
- [ ] 4 группы задач присутствуют
- [ ] Каждая задача имеет: ID, название, описание, приоритет
- [ ] Placeholder'ы в формате {{VARIABLE}}
- [ ] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/ml-tasks-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/ml-tasks-template.md
grep "## Подготовка данных" .specify/templates/ml-tasks-template.md
```

---

### Задача 2.4: Создать data-spec-template.md

**Файл:** `.specify/templates/data-spec-template.md`
**Описание:** Создать шаблон спецификации данных
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл создан
- [ ] Секция "Обзор данных"
- [ ] Секция "Схема данных"
- [ ] Секция "Качество данных"
- [ ] Секция "Стратегия предобработки"
- [ ] Placeholder'ы в формате {{VARIABLE}}
- [ ] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/data-spec-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/data-spec-template.md
grep "random_seed" .specify/templates/data-spec-template.md
```

---

**Итог по Фазе 2:** Задачи: 4, Время: 24 часа


---

## Фаза 3: AI Command Prompts

**Цель:** Создать команды Qwen CLI для генерации артефактов
**Duration:** 10 дней (80 часов)

### Задача 3.1: Создать speckit.specify.toml

**Файл:** `.qwen/commands/speckit.specify.toml`
**Описание:** Создать TOML файл команды для генерации ML спецификации
**Dependencies:** 2.1
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл `.qwen/commands/speckit.specify.toml` создан (расширение .toml, не .md)
- [ ] Формат TOML валиден
- [ ] Секция `description` на русском языке
- [ ] Секция `prompt` с инструкцией для AI
- [ ] Плейсхолдер `{{args}}` для аргументов (Qwen CLI использует {{args}}, не {{description}})
- [ ] Ссылка на шаблон `.specify/templates/ml-spec-template.md`
- [ ] Пример структуры:
  ```toml
  description = "Генерация ML спецификации проекта"
  
  prompt = """
  Используя шаблон из `.specify/templates/ml-spec-template.md`, 
  создай ML спецификацию для проекта: {{args}}
  
  Следуй требованиям FR-002: русский язык + смешанный подход к терминам.
  """
  ```

**Testing:**
```bash
test -f .qwen/commands/speckit.specify.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.specify.toml'))" && echo "✓ TOML валиден"
grep -q "{{args}}" .qwen/commands/speckit.specify.toml && echo "✓ Плейсхолдер {{args}} присутствует"
```

---

### Задача 3.2: Создать speckit.plan.toml

**Файл:** `.qwen/commands/speckit.plan.toml`
**Описание:** Создать TOML файл команды для генерации ML плана
**Dependencies:** 2.2
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл `.qwen/commands/speckit.plan.toml` создан (расширение .toml)
- [ ] Формат TOML валиден
- [ ] Плейсхолдер `{{args}}` для аргументов
- [ ] Ссылка на шаблон `.specify/templates/ml-plan-template.md`

**Testing:**
```bash
test -f .qwen/commands/speckit.plan.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.plan.toml'))" && echo "✓ TOML валиден"
```

---

### Задача 3.3: Создать speckit.tasks.toml

**Файл:** `.qwen/commands/speckit.tasks.toml`
**Описание:** Создать TOML файл команды для генерации списка задач
**Dependencies:** 2.3
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл `.qwen/commands/speckit.tasks.toml` создан (расширение .toml)
- [ ] Формат TOML валиден
- [ ] Плейсхолдер `{{args}}` для аргументов
- [ ] Ссылка на шаблон `.specify/templates/ml-tasks-template.md`

**Testing:**
```bash
test -f .qwen/commands/speckit.tasks.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.tasks.toml'))" && echo "✓ TOML валиден"
```

---

### Задача 3.4: Создать speckit.clarify.toml

**Файл:** `.qwen/commands/speckit.clarify.toml`
**Описание:** Создать TOML файл команды для уточнения требований
**Dependencies:** 2.1
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Файл `.qwen/commands/speckit.clarify.toml` создан (расширение .toml)
- [ ] Формат TOML валиден
- [ ] Плейсхолдер `{{args}}` для аргументов

**Testing:**
```bash
test -f .qwen/commands/speckit.clarify.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.clarify.toml'))" && echo "✓ TOML валиден"
```

---

### Задача 3.5: Расширить speckit.clarify.toml ML-специфичными вопросами

**Файл:** `.qwen/commands/speckit.clarify.toml`
**Описание:** Добавить в команду уточнения вопросы согласно FR-006 (метрики, данные, валидация, безопасность, версионирование)
**Dependencies:** 3.4
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Секция "Performance Metrics Questions" с вопросами о метриках (accuracy, F1, precision, recall, custom metrics)
- [ ] Секция "Data Quality Questions" с вопросами о качестве данных (schema validation, missing values, outliers, leakage prevention)
- [ ] Секция "Validation Strategy Questions" с вопросами о стратегии валидации (train/val/test split, cross-validation, stratification)
- [ ] Секция "Security & Privacy Questions" с вопросами о безопасности (GDPR, anonymization, access control, data retention)
- [ ] Секция "Version Control Questions" с вопросами о версионировании (MLflow, DVC, experiment tracking, model registry)
- [ ] Все вопросы на русском языке с примерами ответов
- [ ] TOML синтаксис валиден

**Example Structure:**
```toml
description = "Уточнение ML-специфичных требований проекта"

prompt = """
Задай пользователю следующие уточняющие вопросы для ML проекта:

## Метрики производительности модели:
1. Какая основная метрика для оценки модели? (accuracy, F1, precision, recall, MAE, RMSE, ROC-AUC)
2. Есть ли дополнительные метрики для мониторинга?
3. Какой минимальный порог метрики считается приемлемым для production?

## Качество данных:
1. Какова ожидаемая схема данных? (типы столбцов, допустимые значения)
2. Как обрабатывать missing values? (удаление, заполнение средним, ML imputation)
3. Какие проверки качества данных требуются перед обучением?
4. Как предотвратить data leakage? (split ДО preprocessing)

## Стратегия валидации:
1. Какое разделение train/val/test? (по умолчанию 70/15/15)
2. Требуется ли cross-validation? (для малых датасетов < 10k)
3. Нужна ли stratification? (для классификации с несбалансированными классами)

## Безопасность и конфиденциальность:
1. Содержат ли данные персональную информацию? (GDPR compliance)
2. Требуется ли анонимизация данных?
3. Кто имеет доступ к данным и моделям?

## Управление версиями:
1. Какая система версионирования моделей? (MLflow, DVC, git-based)
2. Как отслеживать эксперименты? (MLflow, Weights & Biases)
3. Какая стратегия для rollback моделей в production?

Ответы на эти вопросы будут использованы для генерации детальной спецификации.
"""
```

**Testing:**
```bash
test -f .qwen/commands/speckit.clarify.toml && echo "✓ Файл существует"
python3 -c "import toml; config=toml.load(open('.qwen/commands/speckit.clarify.toml')); assert 'Метрики' in config['prompt']" && echo "✓ ML-вопросы присутствуют"
```

---

**Итог по Фазе 3:** Задачи: 5, Время: 20 часов


---

## Фаза 4: Automation Scripts

**Цель:** Создать скрипты автоматизации для ML проектов
**Duration:** 8 дней (64 часов)

### Задача 4.1: Создать скрипт setup-ml.sh

**Файл:** `.specify/scripts/setup-ml.sh`
**Описание:** Создать bash скрипт для инициализации ML проекта
**Dependencies:** 1.1, 1.2
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [ ] Скрипт создаёт структуру директорий (data/, notebooks/, src/, tests/, models/, results/, configs/)
- [ ] Скрипт копирует конфигурационный файл
- [ ] Скрипт исполняемый
- [ ] Скрипт принимает аргумент: название проекта

**Testing:**
```bash
mkdir -p /tmp/test-ml-project
cd /tmp/test-ml-project && /home/gna/workspase/projects/spec-kit-ml-ru/.specify/scripts/setup-ml.sh test-project
test -d test-project/data/ && echo "✓ Структура создана"
rm -rf /tmp/test-ml-project
```

---

### Задача 4.2: Создать скрипт check-ml-env.sh

**Файл:** `.specify/scripts/check-ml-env.sh`
**Описание:** Создать bash скрипт для проверки зависимостей
**Dependencies:** 1.1
**Estimated Time:** 2 часа
**Priority:** Medium

**Acceptance Criteria:**
- [ ] Скрипт проверяет версию Python (>= 3.9)
- [ ] Скрипт проверяет наличие qwen CLI
- [ ] Скрипт проверяет наличие markdownlint
- [ ] Скрипт исполняемый

**Testing:**
```bash
.specify/scripts/check-ml-env.sh
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ Все проверки пройдены"
```

---

**Итог по Фазе 4:** Задачи: 2, Время: 6 часов

---

## Фаза 5: Examples & Documentation

**Цель:** Создать примеры ML проектов и документацию
**Duration:** 20 дней (160 часов)

### Задача 5.1: Создать пример Image Classification

**Файл:** `.ml-spec/examples/image-classification/spec.md`, `plan.md`, `tasks.md`, `data-spec.md`
**Описание:** Создать полный пример проекта классификации изображений (Fashion MNIST)
**Dependencies:** 2.1, 2.2, 2.3, 2.4
**Estimated Time:** 12 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] spec.md создан с ML задачей classification
- [ ] plan.md создан с архитектурой CNN
- [ ] tasks.md создан с задачами для image classification
- [ ] data-spec.md создан с описанием датасета Fashion MNIST
- [ ] Все файлы на русском языке

**Testing:**
```bash
test -f .ml-spec/examples/image-classification/spec.md && echo "✓ spec.md существует"
test -f .ml-spec/examples/image-classification/plan.md && echo "✓ plan.md существует"
test -f .ml-spec/examples/image-classification/tasks.md && echo "✓ tasks.md существует"
test -f .ml-spec/examples/image-classification/data-spec.md && echo "✓ data-spec.md существует"
```

---

### Задача 5.2: Создать пример Tabular Classification

**Файл:** `.ml-spec/examples/tabular-classification/spec.md`, `plan.md`, `tasks.md`, `data-spec.md`
**Описание:** Создать полный пример проекта табличной классификации
**Dependencies:** 2.1, 2.2, 2.3, 2.4
**Estimated Time:** 12 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] spec.md создан с ML задачей classification
- [ ] plan.md создан с архитектурой tree-based моделей
- [ ] tasks.md создан с задачами для tabular classification
- [ ] data-spec.md создан с описанием табличных данных
- [ ] Все файлы на русском языке

**Testing:**
```bash
test -f .ml-spec/examples/tabular-classification/spec.md && echo "✓ spec.md существует"
test -f .ml-spec/examples/tabular-classification/plan.md && echo "✓ plan.md существует"
```

---

### Задача 5.3: Создать пример Time Series Forecast

**Файл:** `.ml-spec/examples/time-series-forecast/spec.md`, `plan.md`, `tasks.md`, `data-spec.md`
**Описание:** Создать полный пример проекта прогнозирования временных рядов
**Dependencies:** 2.1, 2.2, 2.3, 2.4
**Estimated Time:** 12 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] spec.md создан с ML задачей time_series_forecasting
- [ ] plan.md создан с архитектурой ARIMA/LSTM
- [ ] tasks.md создан с задачами для time series
- [ ] data-spec.md создан с описанием временных рядов
- [ ] Все файлы на русском языке

**Testing:**
```bash
test -f .ml-spec/examples/time-series-forecast/spec.md && echo "✓ spec.md существует"
test -f .ml-spec/examples/time-series-forecast/plan.md && echo "✓ plan.md существует"
```

---

### Задача 5.4: Создать README-ML.md

**Файл:** `README-ML.md`
**Описание:** Создать README документацию по использованию ML Spec-Kit
**Dependencies:** 5.1, 5.2, 5.3
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Раздел "Описание проекта" с обзором адаптации Spec-Kit для ML
- [ ] Раздел "Быстрый старт (Quick Start)" с примером за 5 минут
- [ ] Раздел "Установка зависимостей" с инструкциями для Python 3.9+, Qwen CLI, markdownlint
- [ ] Раздел "Структура проекта" с описанием директорий (.specify/, .qwen/, .ml-spec/)
- [ ] Раздел "Как запустить обучение" (для примеров проектов)
- [ ] Раздел "Как сделать inference" (для примеров проектов)
- [ ] Раздел "Примеры использования" с командами /speckit.specify, /speckit.plan, /speckit.tasks
- [ ] Раздел "Примеры проектов" со ссылками на .ml-spec/examples/
- [ ] Раздел "FAQ" с ответами на распространённые вопросы
- [ ] Раздел "Контакты" с информацией о проекте и авторах
- [ ] Весь текст на русском языке
- [ ] Соответствие структуре из Constitution #6

**Testing:**
```bash
test -f README-ML.md && echo "✓ README-ML.md существует"
grep -q "## Быстрый старт" README-ML.md && echo "✓ Раздел Quick Start присутствует"
grep -q "## Установка" README-ML.md && echo "✓ Раздел Установка присутствует"
grep -q "## Структура проекта" README-ML.md && echo "✓ Раздел Структура присутствует"
grep -q "## Как запустить обучение" README-ML.md && echo "✓ Раздел Training присутствует"
grep -q "## Контакты" README-ML.md && echo "✓ Раздел Контакты присутствует"
```

---

**Итог по Фазе 5:** Задачи: 4, Время: 42 часа


---

## Фаза 6: Testing & Polish

**Цель:** End-to-end тестирование, bug fixes, финальная документация
**Duration:** 10 дней (80 часов)

### Задача 6.1: Создать end-to-end тесты

**Файл:** `tests/integration/test_ml_speckit_workflow.py`
**Описание:** Создать интеграционные тесты для полного workflow
**Dependencies:** 3.1, 5.1
**Estimated Time:** 8 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Тест генерации спецификации
- [ ] Тест генерации плана из спецификации
- [ ] Тест генерации задач из плана
- [ ] Тест полного workflow
- [ ] Все тесты проходят

**Testing:**
```bash
pytest tests/integration/test_ml_speckit_workflow.py -v
```

---

### Задача 6.2: Создать unit тесты для шаблонов

**Файл:** `tests/templates/test_ml_templates.py`
**Описание:** Создать unit тесты для валидации всех ML шаблонов
**Dependencies:** 2.1, 2.2, 2.3, 2.4
**Estimated Time:** 6 часов
**Priority:** Medium

**Acceptance Criteria:**
- [ ] Тест для ml-spec-template.md (валидация всех 10 секций)
- [ ] Тест для ml-plan-template.md (валидация структуры плана)
- [ ] Тест для ml-tasks-template.md (валидация формата задач)
- [ ] Тест для data-spec-template.md (валидация схемы данных)
- [ ] **Test coverage >= 80% для всех модулей в src/** (Constitution #12)
- [ ] Coverage report генерируется в HTML формате
- [ ] Все тесты проходят

**Testing:**
```bash
pytest tests/templates/test_ml_templates.py -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ Все тесты пройдены с coverage >= 80%"
open htmlcov/index.html  # Проверить coverage report визуально
```

---

### Задача 6.3: Bug fixes и исправления

**Файл:** N/A
**Описание:** Исправить все баги, найденные при тестировании
**Dependencies:** 6.1, 6.2
**Estimated Time:** 8 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Все тесты проходят без ошибок
- [ ] Все известные баги исправлены
- [ ] Code review выполнен

**Testing:**
```bash
pytest tests/ -v
```

---

### Задача 6.4: Добавить type hints во весь CLI код

**Файл:** `src/specify_cli/__init__.py` и все модули в `src/`
**Описание:** Добавить type hints во все функции и методы CLI согласно Constitution #3
**Dependencies:** 6.2
**Estimated Time:** 8 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Type hints добавлены во все публичные функции
- [ ] Type hints добавлены во все методы классов
- [ ] mypy проверка проходит без ошибок (`mypy src/ --strict`)
- [ ] Return types указаны явно
- [ ] Параметры функций аннотированы

**Testing:**
```bash
mypy src/ --strict
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ mypy проверка пройдена"
```

---

### Задача 6.5: Обеспечить русскоязычные docstrings во всех модулях

**Файл:** Все `.py` файлы в `src/`, `.specify/scripts/`, шаблоны
**Описание:** Добавить/обновить docstrings на русском языке (Google style) согласно Constitution #6
**Dependencies:** 6.4
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Все публичные модули имеют docstrings на русском
- [ ] Все публичные классы имеют docstrings на русском
- [ ] Все публичные функции имеют docstrings на русском (Google style)
- [ ] Docstrings включают: описание, Args, Returns, Raises, Examples
- [ ] Примеры кода в docstrings корректны

**Testing:**
```bash
# Проверка наличия docstrings
python3 -c "import src.specify_cli; help(src.specify_cli)" | grep -q "Описание" && echo "✓ Docstrings на русском"

# Проверка стиля docstrings
pydocstyle src/ --convention=google
```

---

### Задача 6.6: Настроить CI проверку coverage

**Файл:** `.github/workflows/test.yml` или аналогичный CI конфиг
**Описание:** Добавить автоматическую проверку coverage >= 80% в CI pipeline
**Dependencies:** 6.2
**Estimated Time:** 2 часа
**Priority:** Medium

**Acceptance Criteria:**
- [ ] CI workflow создан или обновлён
- [ ] Step для запуска pytest с coverage
- [ ] Fail CI если coverage < 80%
- [ ] Coverage report загружается как artifact
- [ ] Badge с coverage добавлен в README-ML.md

**Testing:**
```bash
# Локальный тест CI команды
pytest tests/ --cov=src --cov-fail-under=80 -v
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ CI команда работает"
```

---

**Итог по Фазе 6:** Задачи: 6, Время: 46 часов

---

## Итоговая статистика проекта

### Общие показатели
- **Общее количество задач:** 24
- **Общее время:** 141 часа (~18 рабочих дней)
- **Количество фаз:** 6
- **Количество milestones:** 6

### Распределение по фазам
| Фаза | Задачи | Время | Milestone |
|------|--------|-------|-----------|
| Фаза 1: Инфраструктура | 3 | 8 часов | Инфраструктура готова |
| Фаза 2: Core Templates | 4 | 24 часов | Templates созданы |
| Фаза 3: AI Commands | 5 | 20 часов | Commands работают |
| Фаза 4: Automation | 2 | 6 часов | Automation готова |
| Фаза 5: Examples & Docs | 4 | 42 часов | Examples и docs готовы |
| Фаза 6: Testing & Polish | 6 | 46 часов | MVP готов к использованию |
| **ИТОГО** | **24** | **141 часа** | **6 milestones** |

### Критический путь
1.1 → 1.2 → 1.3 → 2.1 → 3.1 → 3.5 → 5.1 → 6.1 → 6.4 → 6.5 → 6.3

### Параллельные возможности
- **Фаза 2**: 2.1, 2.2, 2.3, 2.4 могут выполняться параллельно
- **Фаза 3**: 3.1, 3.2, 3.3, 3.4 могут выполняться параллельно
- **Фаза 5**: 5.1, 5.2, 5.3 могут выполняться параллельно

---

## User Stories Mapping

### US1: Адаптация шаблонов для ML проектов (Priority: P1)
**Задачи:** 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4
**Независимый тест:** Создать спецификацию для ML проекта и проверить, что шаблоны содержат нужные ML-секции.

### US2: Поддержка русскоязычных артефактов (Priority: P2)
**Задачи:** Все задачи (требование ко всем артефактам)
**Независимый тест:** Запустить любую команду Spec-Kit и проверить, что результат на русском языке.

### US3: Поддержка ML-специфичных шаблонов (Priority: P3)
**Задачи:** 2.1, 2.2, 2.3, 2.4 (создание шаблонов), 5.1, 5.2, 5.3 (примеры)
**Независимый тест:** Создать спецификацию для ML проекта и проверить, что доступны шаблоны для data-spec, model-spec, evaluation-plan.

---

## Implementation Strategy

### MVP First (US1 Only)
1. Завершить Фазу 1: Setup
2. Завершить Фазу 2: Templates (только базовые)
3. Завершить Фазу 3: Commands (только для US1)
4. Создать один пример (5.1)
5. Базовое тестирование (6.1, 6.2)
6. **STOP и VALIDATE**: Протестировать MVP

### Incremental Delivery
1. Фаза 1 + Фаза 2 → Foundation готово
2. Добавить Фазу 3 → Commands работают
3. Добавить Фазу 4 → Automation готова
4. Добавить Фазу 5 (5.1) → Первый пример готов
5. Добавить Фазу 5 (5.2, 5.3) → Все примеры готовы
6. Добавить Фазу 6 → MVP готов к использованию

---

**Версия**: 1.0 | **Дата**: 2026-02-13 | **Статус**: Ready for implementation
