# Задачи: Адаптация Spec-Kit для ML Проектов

**Feature Branch**: `specs/001-ml-adaptation`
**Status**: Implementation in Progress (0 CRITICAL issues)
**Version**: 1.3 (Remediation Round 5 - FINAL)
**Last Updated**: 2026-02-13
**Git Workflow**: feature/001-PX-name → specs/001-* → main

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

### Задача 1.0: Настройка ML окружения

**Файл:** `.ml-spec/scripts/setup-env.sh`
**Описание:** Интерактивный скрипт для проверки и настройки ML окружения с поддержкой различных package managers (conda/pip/uv)
**Зависимости:** Нет (самая первая задача!)
**Расчётное время:** 4 часа
**Приоритет:** КРИТИЧЕСКИЙ

**Критерии приемки:**

1. **Интерактивный скрипт setup-env.sh:**
    - [x] Определяет доступные package managers (conda, pip, uv, poetry)
    - [x] Задаёт пользователю вопрос: "Окружение готово?" [y/n]
    - [x] Если нет: запускает интерактивную настройку
    - [x] Если да: запускает только проверку (check_environment.py)
    - [x] Поддерживает создание conda environment / venv / uv venv
    - [x] Устанавливает зависимости из requirements-{conda|pip|uv}.txt
    - [x] Цветной вывод с эмодзи (Green ✓, Red ✗, Yellow ⚠)
    - [x] Exit code: 0 если OK, 1 если критические ошибки

2. **Python скрипт check_environment.py:**
    - [x] Проверяет Python >= 3.9
    - [x] Проверяет активный package manager (CONDA_PREFIX / VIRTUAL_ENV)
    - [x] Проверяет ML библиотеки: numpy, pandas, scikit-learn, torch, mlflow, dvc
    - [x] Проверяет development tools: pytest, black, mypy, pre-commit
    - [x] Опциональная проверка GPU/CUDA/ROCm
    - [x] Флаг --fix для автоматической установки недостающих пакетов
    - [x] Цветной табличный вывод (как в приложенном примере)
    - [x] Exit codes: 0=OK, 1=errors, 2=warnings

3. **Requirements файлы:**
    - [x] .ml-spec/config/requirements-pip.txt
    - [x] .ml-spec/config/requirements-conda.txt (или environment.yml)
    - [x] .ml-spec/config/requirements-uv.txt
    - [x] .ml-spec/config/requirements-dev.txt (dev tools only)

4. **Conda environment.yml:**
    - [x] Channels: pytorch, conda-forge, defaults
    - [x] Python 3.11
    - [x] Core ML: numpy, pandas, scikit-learn, matplotlib
    - [x] PyTorch >= 2.0
    - [x] MLOps: mlflow, dvc (через pip)
    - [x] Dev tools: pytest, black, mypy

5. **Интеграция с другими скриптами:**
     - [x] Все последующие скрипты (1.2+) вызывают check_environment.py в начале
     - [x] Graceful fail с подсказкой: "Run: bash setup-env.sh"
     
6. **Документация:**
     - [x] README-ML.md секция "Environment Setup Options"
     - [x] Примеры для conda / pip / uv
     - [x] Troubleshooting секция
     
**Примечания:**
- Идемпотентность: повторный запуск безопасен
- Cross-platform: Linux, macOS, Windows WSL
- User-friendly: понятные сообщения об ошибках

7. **Makefile creation:**
     - [x] Создание Makefile в корне проекта
     - [x] Target `setup`: выполняет `bash .ml-spec/scripts/setup-env.sh`
     - [x] Target `check`: выполняет `python .ml-spec/scripts/check_environment.py`
     - [x] User-friendly: `make setup` для инициализации вместо запоминания путей к скриптам

---

### Задача 1.1: Создать структуру директорий

**Файл:** `.specify/templates/`, `.qwen/commands/`, `.ml-spec/examples/`
**Описание:** Создать базовую структуру директорий для шаблонов, команд и примеров
**Dependencies:** None
**Estimated Time:** 2 часа
**Priority:** High

**Acceptance Criteria:**
- [x] Директория `.specify/templates/` создана
- [x] Директория `.qwen/commands/` создана
- [x] Директория `.ml-spec/examples/` создана
- [x] Директория `.ml-spec/examples/image-classification/` создана
- [x] Директория `.ml-spec/examples/tabular-classification/` создана
- [x] Директория `.ml-spec/examples/time-series-forecast/` создана

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
- [x] Файл `.ml-spec/config.yaml` создан
- [x] Секция `random_seed` со значением 42
- [x] Секция `train_val_test_split` с пропорциями 0.70/0.15/0.15
- [x] Секция `language` со значением `ru`
- [x] YAML синтаксис валиден

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
- [x] Файл `.pre-commit-config.yaml` создан с hooks: black, flake8, isort, mypy
- [x] Скрипт `.specify/scripts/setup-precommit.sh` создан для установки hooks
- [x] README.md обновлён с инструкциями по установке pre-commit
- [x] Hooks проходят успешно на текущем коде

**Testing:**
```bash
pre-commit install
pre-commit run --all-files
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ Все pre-commit проверки пройдены"
```

---

### Задача 1.4: Настроить DVC с поддержкой Яндекс.Диска

**Файл:** `.dvc/config`, `.dvc/config.local`, `.gitignore`
**Описание:** Настроить DVC для версионирования данных с поддержкой Яндекс.Диска (WebDAV)
**Dependencies:** 1.1
**Расчётное время:** 5 часов
**Приоритет:** ВЫСОКИЙ

**Критерии приемка:**

1. **WebDAV конфигурация:**
    ```
      Select DVC storage:
        1) Local filesystem (для начала)
        2) Яндекс.Диск (WebDAV)
        3) Яндекс Object Storage (S3-compatible)
        4) AWS S3
        5) Google Cloud Storage
      ```
    - [x] Для Яндекс.Диска: запрос WebDAV credentials
    - [x] Автоматическая настройка .dvc/config с WebDAV URL
    - [x] Тестирование подключения (dvc push test file)
    - [x] Документация setup для российских пользователей
    - [x] Примеры конфигурации в README-ML.md

2. **.dvc/config:**
    ```yaml
    # .dvc/config
    [core]
        remote = yandex

    ['remote "yandex"']
        url = webdav://webdav.yandex.ru/dvc-storage
        user = your-email@yandex.ru
        ask_password = true
    ```

3. **Безопасность:**
    - [x] Пароль НЕ сохраняется в plaintext
    - [x] Использование environment variables: YANDEX_WEBDAV_PASSWORD
    - [x] Добавить .dvc/config.local в .gitignore

4. **Интеграция с check_environment.py:**
    - [x] Скрипт проверяет наличие DVC
    - [x] Скрипт проверяет конфигурацию WebDAV
    - [x] Флаг --fix для автоматической настройки

5. **Документация:**
    - [x] README-ML.md секция "DVC & Data Versioning"
    - [x] Примеры для WebDAV, S3, Local
    - [x] Troubleshooting секция

**Testing:**
```bash
# Тест WebDAV подключения
dvc remote list
dvc push test-file.txt
dvc pull test-file.txt
```

---

**Итог по Фазе 1:** Задачи: 5, Время: 22 часа


---

## Фаза 2: Core ML Templates

**Цель:** Создать 4 основных ML шаблона для MVP
**Duration:** 15 дней (120 часов)

### Задача 2.2: Создать ml-spec-template.md

**Файл:** `.specify/templates/ml-spec-template.md`
**Описание:** Создать шаблон спецификации ML проекта с 10 основными секциями
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [x] Файл создан
- [x] Все 10 секций присутствуют
- [x] Placeholder'ы в формате {{VARIABLE}}
- [x] Примеры заполнения для каждой секции
- [x] Весь текст на русском языке
- [x] Технические термины: "Русский (English)"
- [x] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/ml-spec-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/ml-spec-template.md
grep -E '\{\{[A-Z_]+\}\}' .specify/templates/ml-spec-template.md
```

---

### Задача 2.3: Создать ml-plan-template.md

**Файл:** `.specify/templates/ml-plan-template.md`
**Описание:** Создать шаблон плана реализации ML проекта
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [x] Файл создан
- [x] Секция "Архитектура решения" с подразделами
- [x] Секция "Этапы реализации" с 5 этапами
- [x] Секция "Технологический стек" с подразделами
- [x] Placeholder'ы в формате {{VARIABLE}}
- [x] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/ml-plan-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/ml-plan-template.md
grep "Этап 1: EDA" .specify/templates/ml-plan-template.md
```

---

### Задача 2.4: Создать ml-tasks-template.md

**Файл:** `.specify/templates/ml-tasks-template.md`
**Описание:** Создать шаблон списка задач ML проекта
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [x] Файл создан
- [x] 4 группы задач присутствуют
- [x] Каждая задача имеет: ID, название, описание, приоритет
- [x] Placeholder'ы в формате {{VARIABLE}}
- [x] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/ml-tasks-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/ml-tasks-template.md
grep "## Подготовка данных" .specify/templates/ml-tasks-template.md
```

---

### Задача 2.5: Создать data-spec-template.md

**Файл:** `.specify/templates/data-spec-template.md`
**Описание:** Создать шаблон спецификации данных
**Dependencies:** 1.1
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [x] Файл создан
- [x] Секция "Обзор данных"
- [x] Секция "Схема данных"
- [x] Секция "Качество данных"
- [x] Секция "Стратегия предобработки"
- [x] Placeholder'ы в формате {{VARIABLE}}
- [x] Markdown синтаксис валиден

**Testing:**
```bash
test -f .specify/templates/data-spec-template.md && echo "✓ Файл существует"
markdownlint .specify/templates/data-spec-template.md
grep "random_seed" .specify/templates/data-spec-template.md
```

---

### Задача 2.6: Валидация монолитной структуры шаблонов

**Файл:** `.ml-spec/tests/test_template_structure.py`
**Описание:** Автоматическая проверка что все ML шаблоны монолитные (без file includes, modular imports)
**Зависимости:** Tasks 2.2, 2.3, 2.4, 2.5
**Расчётное время:** 2 часа
**Приоритет:** СРЕДНИЙ

**Критерии приемки:**

1. **Pytest тесты для монолитности:**
   ```python
   def test_template_is_monolithic(template_path):
       """Проверяет что шаблон не содержит file includes."""
       content = template_path.read_text()

       # Запрещённые паттерны
       assert "{% include" not in content  # Jinja2 includes
       assert "{{< include" not in content  # Hugo includes
       assert "import " not in content  # Python imports (если .py template)

       # Разрешённые паттерны
       assert "<!-- OPTIONAL SECTION:" in content  # OK: commented sections
   ```

2. **Проверка всех шаблонов:**
    - [x] ml-spec-template.md: монолитный ✓
    - [x] ml-plan-template.md: монолитный ✓
    - [x] ml-tasks-template.md: монолитный ✓
    - [x] data-spec-template.md: монолитный ✓

3. **Проверка опциональных секций:**
    - [x] Опциональные секции закомментированы в одном файле
    - [x] Не вынесены в отдельные файлы

4. **CI/CD интеграция:**
    - [x] Тест запускается в CI/CD pipeline
    - [x] Fail если шаблон не монолитный

**Testing:**
```bash
pytest .ml-spec/tests/test_template_structure.py -v
```

---

**Итог по Фазе 2:** Задачи: 5, Время: 26 часов


---

## Фаза 3: AI Command Prompts

**Цель:** Создать команды Qwen CLI для генерации артефактов
**Duration:** 10 дней (80 часов) (обновлено: 7 задач, 29 часов в деталях)

### Задача 3.2: Создать speckit.specify.toml

**Файл:** `.qwen/commands/speckit.specify.toml`
**Описание:** Создать TOML файл команды для генерации ML спецификации
**Dependencies:** 2.2
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [x] Файл `.qwen/commands/speckit.specify.toml` создан (расширение .toml, не .md)
- [x] Формат TOML валиден
- [x] Секция `description` на русском языке
- [x] Секция `prompt` с инструкцией для AI
- [x] Плейсхолдер `{{args}}` для аргументов (Qwen CLI использует {{args}}, не {{description}})
- [x] Ссылка на шаблон `.specify/templates/ml-spec-template.md`
- [x] Пример структуры:
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

### Задача 3.3: Создать speckit.plan.toml

**Файл:** `.qwen/commands/speckit.plan.toml`
**Описание:** Создать TOML файл команды для генерации ML плана
**Dependencies:** 2.3
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [x] Файл `.qwen/commands/speckit.plan.toml` создан (расширение .toml)
- [x] Формат TOML валиден
- [x] Плейсхолдер `{{args}}` для аргументов
- [x] Ссылка на шаблон `.specify/templates/ml-plan-template.md`

**Testing:**
```bash
test -f .qwen/commands/speckit.plan.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.plan.toml'))" && echo "✓ TOML валиден"
```

---

### Задача 3.4: Создать speckit.tasks.toml

**Файл:** `.qwen/commands/speckit.tasks.toml`
**Описание:** Создать TOML файл команды для генерации списка задач
**Dependencies:** 2.4
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [x] Файл `.qwen/commands/speckit.tasks.toml` создан (расширение .toml)
- [x] Формат TOML валиден
- [x] Плейсхолдер `{{args}}` для аргументов
- [x] Ссылка на шаблон `.specify/templates/ml-tasks-template.md`

**Testing:**
```bash
test -f .qwen/commands/speckit.tasks.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.tasks.toml'))" && echo "✓ TOML валиден"
```

---

### Задача 3.5: Создать speckit.clarify.toml

**Файл:** `.qwen/commands/speckit.clarify.toml`
**Описание:** Создать TOML файл команды для уточнения требований
**Dependencies:** 2.2
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [x] Файл `.qwen/commands/speckit.clarify.toml` создан (расширение .tomл)
- [x] Формат TOML валиден
- [x] Плейсхолдер `{{args}}` для аргументов

**Testing:**
```bash
test -f .qwen/commands/speckit.clarify.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.clarify.toml'))" && echo "✓ TOML валиден"
```

---

### Задача 3.6: Расширение команды speckit.specify ML-вопросами

**Файл:** `.qwen/commands/speckit.specify.toml`
**Описание:** Добавление ML-специфичных вопросов в команду /speckit.specify для сбора требований на этапе спецификации
**Зависимости:** Task 3.5
**Расчётное время:** 3 часа
**Приоритет:** ВЫСОКИЙ

**Критерии приемки:**

1. **ML-вопросы в speckit.specify.toml:**
    - [x] Секция "Performance Metrics": accuracy, precision, recall, F1-score, ROC-AUC, MAE, RMSE
    - [x] Секция "Data Quality": схема, типы, missing values, outliers, data leakage prevention
    - [x] Секция "Model Validation": train/val/test split, cross-validation, stratification
    - [x] Секция "Security & Privacy": GDPR compliance, anonymization, access control
    - [x] Секция "Versioning": MLflow, DVC, git-based tracking

2. **Интеграция в prompt:**
    ```toml
    [[prompt]]
    role = "system"
    content = """
    После сбора базовых требований задайте ML-специфичные вопросы:

    1. Метрики производительности: какие метрики критичны? (accuracy, F1-score, MAE?)
    2. Качество данных: какие требования к данным? (схема, missing values, outliers?)
    3. Стратегия валидации: как валидировать модель? (train/test split, cross-validation?)
    4. Безопасность данных: требования GDPR? Anonymization?
    5. Управление версиями: MLflow или DVC? Git-based tracking?
    """
    ```

3. **Alignment с FR-006:**
    - [x] Все 5 категорий вопросов из FR-006 присутствуют
    - [x] Вопросы на русском языке с англицизмами per FR-002

4. **Testing:**
    - [x] Запуск `/speckit.specify` генерирует `spec.md` с ML-секциями
    - [x] Вопросы задаются пользователю в правильном порядке

---

### Задача 3.7: Environment-Aware Clarification /speckit.clarify-ml

**Файл:** `.qwen/commands/speckit.clarify-ml.toml`
**Описание:** Создать команду `/speckit.clarify-ml` с автоматической проверкой окружения перед заданием вопросов
**Dependencies:** 3.5
**Estimated Time:** 5 часов (обновлено с +1 час для интеграции)
**Priority:** High

**Критерии приемки:**

1. **Context Injection from Environment:**
    - [x] Configure `.qwen/commands/speckit.clarify-ml.toml` to execute `python .ml-spec/scripts/check_environment.py --json` (read-only mode) before generating prompt
    - [x] Inject the JSON output into the System Prompt
    - [x] Rename command from `/speckit.clarify` to `/speckit.clarify-ml` (for clear distinction)
    
2. **Smart Prompting:**
    - [x] If `check_environment.py` detects GPU → Prompt shouldn't ask "Do you have a GPU?", but ask "I see an NVIDIA GPU. Should we configure mixed-precision training?"
    - [x] If `check_environment.py` detects missing libraries → Prompt should suggest adding them to requirements
    - [x] Environment-aware questions based on detected capabilities
    
3. **Command Workflow:**
    - [x] User runs `/speckit.clarify-ml`
    - [x] System runs `check_environment.py` (invisible to user)
    - [x] LLM receives context: `{ "gpu": true, "ram": "16GB", "libs": ["torch", "pandas"], "cuda": "11.8" }`
    - [x] LLM generates context-aware questions based on environment
    
4. **ML-специфичные вопросы:**
    - [x] Секция "Performance Metrics Questions" с вопросами о метриках (accuracy, F1, precision, recall, custom metrics)
    - [x] Секция "Data Quality Questions" с вопросами о качестве данных (schema validation, missing values, outliers, leakage prevention)
    - [x] Секция "Validation Strategy Questions" с вопросами о стратегии валидации (train/val/test split, cross-validation, stratification)
    - [x] Секция "Security & Privacy Questions" с вопросами о безопасности (GDPR, anonymization, access control, data retention)
    - [x] Секция "Version Control Questions" с вопросами о версионировании (MLflow, DVC, experiment tracking, model registry)
    - [x] Все вопросы на русском языке с примерами ответов
    - [x] TOML синтаксис валиден

**Example Structure:**
```toml
description = "Уточнение ML-специфичных требований проекта с автоматической проверкой окружения"

scripts = [
    'bash -c "python .ml-spec/scripts/check_environment.py --json"'
]

prompt = """
Сначала проанализируй информацию о текущем окружении:

{{$CHECK_ENV_OUTPUT}}

На основе этой информации задай пользователю следующие уточняющие вопросы для ML проекта:

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
```

**Testing:**
```bash
test -f .qwen/commands/speckit.clarify-ml.toml && echo "✓ Файл существует"
python3 -c "import toml; config=toml.load(open('.qwen/commands/speckit.clarify-ml.toml')); assert 'Метрики' in config['prompt']" && echo "✓ ML-вопросы присутствуют"
test -f .ml-spec/scripts/check_environment.py && echo "✓ Скрипт check_environment.py существует"
```

3. **Verification всех 5 категорий вопросов:**
     - [x] Performance Metrics: accuracy, precision, recall, F1-score, ROC-AUC, MAE, RMSE
     - [x] Data Quality: схема, типы, missing values, outliers, data leakage prevention
     - [x] Model Validation: train/val/test split, cross-validation, stratification
     - [x] Security & Privacy: GDPR compliance, anonymization, access control
     - [x] Versioning: MLflow, DVC, git-based tracking
     
     **Тест:** запустить `/speckit.clarify-ml` и убедиться что все 5 категорий вопросов задаются
     **Тест:** убедиться что check_environment.py автоматически запускается перед вопросами

---

### Задача 3.8: Команда настройки окружения /speckit.setup-ml

**Файл:** `.qwen/commands/speckit.setup-ml.toml`
**Время:** 3 часа
**Приоритет:** MEDIUM

**Описание:**
Создать команду, которая позволяет пользователю описать желаемое ML окружение на естественном языке, и агент генерирует/обновляет конфигурационные файлы (`requirements.txt`, `environment.yml`, `config.yaml`) перед физической установкой.

**Критерии приемки:**

1. **Natural Language Processing:**
    - [x] Input: "Мне нужно окружение для Computer Vision с PyTorch и Albumentations."
    - [x] Output: Обновляет `requirements.txt` с `torch`, `torchvision`, `albumentations` (с соответствующими ограничениями версии)
    
2. **Conflict Resolution:**
    - [x] System prompt должен инструктировать LLM проверять совместимость версий (например, "Если используется CUDA 11.8, используйте PyTorch 2.0.1+cu118")
    
3. **File Generation:**
    - [x] Команда может обновлять/создавать:
        - `.ml-spec/config/requirements-*.txt`
        - `.ml-spec/config/environment.yml`
        - `.ml-spec/config.yaml` (настройки проекта)
        
4. **Hand-off to Make:**
    - [x] Финальный вывод команды должен инструктировать пользователя: "Файлы конфигурации обновлены. Пожалуйста выполните `make setup` в терминале для применения изменений."
    
5. **Integration:**
    - [x] Добавить эту команду в основное меню помощи (CLI help)

**Пример структуры:**
```toml
description = "Настройка ML окружения на основе естественного описания"

prompt = """
На основе описания окружения пользователя, обнови следующие конфигурационные файлы:

{{args}}

При обновлении файлов:
1. Проверя совместимость версий библиотек
2. Используй стабильные версии для production
3. Предлагай альтернативы для разных типов окружений (CPU, GPU с CUDA, CPU с ROCm)

После обновления инструктировать пользователю запустить `make setup` для применения изменений.
```

**Testing:**
```bash
test -f .qwen/commands/speckit.setup-ml.toml && echo "✓ Файл существует"
python3 -c "import toml; toml.load(open('.qwen/commands/speckit.setup-ml.toml'))" && echo "✓ TOML валиден"
```

---

**Итог по Фазе 3:** Задачи: 7, Время: 29 часов (4+4+4+4+5+5+3)


---

## Фаза 4: Automation Scripts

**Цель:** Создать скрипты автоматизации для ML проектов
**Duration:** 8 дней (64 часов)

### Задача 4.2: Создать скрипт setup-ml.sh

**Файл:** `.specify/scripts/setup-ml.sh`
**Описание:** Создать bash скрипт для инициализации ML проекта
**Dependencies:** 1.1, 1.2
**Estimated Time:** 4 часа
**Priority:** High

**Acceptance Criteria:**
- [x] Скрипт создаёт структуру директорий (data/, notebooks/, src/, tests/, models/, results/, configs/)
- [x] Скрипт копирует конфигурационный файл
- [x] Скрипт исполняемый
- [x] Скрипт принимает аргумент: название проекта

**Testing:**
```bash
mkdir -p /tmp/test-ml-project
cd /tmp/test-ml-project && /home/gna/workspase/projects/spec-kit-ml-ru/.specify/scripts/setup-ml.sh test-project
test -d test-project/data/ && echo "✓ Структура создана"
rm -rf /tmp/test-ml-project
```

---

### Задача 4.3: Создать скрипт check-ml-env.sh

**Файл:** `.specify/scripts/check-ml-env.sh`
**Описание:** Создать bash скрипт для проверки зависимостей
**Dependencies:** 1.1
**Estimated Time:** 2 часа
**Priority:** Medium

**Acceptance Criteria:**
- [x] Скрипт проверяет версию Python (>= 3.9)
- [x] Скрипт проверяет наличие qwen CLI
- [x] Скрипт проверяет наличие markdownlint
- [x] Скрипт исполняемый

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

### Задача 5.2: Создать пример Image Classification

**Файл:** `.ml-spec/examples/image-classification/spec.md`, `plan.md`, `tasks.md`, `data-spec.md`
**Описание:** Создать полный пример проекта классификации изображений (Fashion MNIST)
**Dependencies:** 2.2, 2.3, 2.4, 2.5
**Estimated Time:** 12 часов
**Priority:** High

**Acceptance Criteria:**
- [x] spec.md создан с ML задачей classification
- [x] plan.md создан с архитектурой CNN
- [x] tasks.md создан с задачами для image classification
- [x] data-spec.md создан с описанием датасета Fashion MNIST
- [x] Все файлы на русском языке

**Testing:**
```bash
test -f .ml-spec/examples/image-classification/spec.md && echo "✓ spec.md существует"
test -f .ml-spec/examples/image-classification/plan.md && echo "✓ plan.md существует"
test -f .ml-spec/examples/image-classification/tasks.md && echo "✓ tasks.md существует"
test -f .ml-spec/examples/image-classification/data-spec.md && echo "✓ data-spec.md существует"
```

---

### Задача 5.3: Создать пример Tabular Classification

**Файл:** `.ml-spec/examples/tabular-classification/spec.md`, `plan.md`, `tasks.md`, `data-spec.md`
**Описание:** Создать полный пример проекта табличной классификации
**Dependencies:** 2.2, 2.3, 2.4, 2.5
**Estimated Time:** 12 часов
**Priority:** High

**Acceptance Criteria:**
- [x] spec.md создан с ML задачей classification
- [x] plan.md создан с архитектурой tree-based моделей
- [x] tasks.md создан с задачами для tabular classification
- [x] data-spec.md создан с описанием табличных данных
- [x] Все файлы на русском языке

**Testing:**
```bash
test -f .ml-spec/examples/tabular-classification/spec.md && echo "✓ spec.md существует"
test -f .ml-spec/examples/tabular-classification/plan.md && echo "✓ plan.md существует"
```

---

### Задача 5.4: Создать пример Time Series Forecast

**Файл:** `.ml-spec/examples/time-series-forecast/spec.md`, `plan.md`, `tasks.md`, `data-spec.md`
**Описание:** Создать полный пример проекта прогнозирования временных рядов
**Dependencies:** 2.2, 2.3, 2.4, 2.5
**Estimated Time:** 12 часов
**Priority:** High

**Acceptance Criteria:**
- [x] spec.md создан с ML задачей time_series_forecasting
- [x] plan.md создан с архитектурой ARIMA/LSTM
- [x] tasks.md создан с задачами для time series
- [x] data-spec.md создан с описанием временных рядов
- [x] Все файлы на русском языке

**Testing:**
```bash
test -f .ml-spec/examples/time-series-forecast/spec.md && echo "✓ spec.md существует"
test -f .ml-spec/examples/time-series-forecast/plan.md && echo "✓ plan.md существует"
```

---

### Задача 5.5: Создать README-ML.md

**Файл:** `README-ML.md`
**Описание:** Создать README документацию по использованию ML Spec-Kit
**Dependencies:** 5.2, 5.3, 5.4
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [x] Раздел "Описание проекта" с обзором адаптации Spec-Kit для ML
- [x] Раздел "Быстрый старт (Quick Start)" с примером за 5 минут
- [x] Раздел "Установка зависимостей" с инструкциями для Python 3.9+, Qwen CLI, markdownlint
- [x] Раздел "Структура проекта" с описанием директорий (.specify/, .qwen/, .ml-spec/)
- [x] Раздел "Как запустить обучение" (для примеров проектов)
- [x] Раздел "Как сделать inference" (для примеров проектов)
- [x] Раздел "Примеры использования" с командами /speckit.specify, /speckit.plan, /speckit.tasks
- [x] Раздел "Примеры проектов" со ссылками на .ml-spec/examples/
- [x] Раздел "FAQ" с ответами на распространённые вопросы
- [x] Раздел "Контакты" с информацией о проекте и авторах
- [x] Весь текст на русском языке
- [x] Соответствие структуре из Constitution #6

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

### Задача 5.6: Создать руководство по миграции

**Файл:** `MIGRATION-GUIDE.md`
**Описание:** Comprehensive руководство по миграции с оригинального Spec-Kit на ML-адаптированную версию
**Dependencies:** Все предыдущие задачи Phase 5
**Расчётное время:** 4 часа
**Приоритет:** ВЫСОКИЙ

**Критерии приемка:**

1. **Документ MIGRATION-GUIDE.md:**
    - [x] Секция "Что изменилось" (breaking changes)
    - [x] Таблица сравнения: старые vs новые команды
    - [x] Секция "Пошаговая миграция" с примерами
    - [x] Секция "Обратная совместимость" (что осталось)
    - [x] FAQ по типичным проблемам миграции
    - [x] Контрольный чеклист для пользователей

2. **Breaking changes таблица:**
    ```markdown
    | Что удалено | Чем заменено | Причина |
    |-------------|--------------|---------|
    | web-api-spec-template.md | ml-spec-template.md | Фокус на ML |
    | database-spec-template.md | data-spec-template.md | ML-терминология |
    ```

3. **Примеры миграции:**
    - [x] Пример 1: Конвертация старого spec.md в ML spec.md
    - [x] Пример 2: Адаптация существующего проекта
    - [x] Пример 3: Команды до/после миграции

4. **Backward compatibility секция:**
    - [x] Что продолжает работать без изменений
    - [x] Deprecation warnings (если есть)
    - [x] Timeline для удаления устаревших фич

---

### Задача 5.7: Создание CHANGELOG-ML.md

**Файл:** `CHANGELOG-ML.md`
**Описание:** Changelog для отслеживания изменений в ML адаптации Spec-Kit
**Зависимости:** Task 5.6
**Расчётное время:** 1 час
**Приоритет:** НИЗКИЙ

**Критерии приемки:**

1. **Структура CHANGELOG-ML.md:**
    ```markdown
    # Changelog - ML Адаптация Spec-Kit

    Формат: [Keep a Changelog](https://keepachangelog.com/ru/)
    Версионирование: [Semantic Versioning](https://semver.org/)

    ## [Unreleased]
    ### Added
    - Новые ML шаблоны (spec, plan, tasks, data-spec)
    - Команды /speckit.specify, /speckit.plan, /speckit.tasks адаптированы для ML

    ### Changed
    - Все артефакты теперь на русском языке

    ### Removed
    - Веб-шаблоны (web-api-spec, database-spec)

    ## [1.0.0] - 2026-02-13
    ### Added
    - Первая версия ML адаптации
    ```

2. **Update policy:**
    - [x] Каждое изменение логируется в CHANGELOG-ML.md
    - [x] Version bumps соответствуют semver
    - [x] Changelog review в PR process

**Testing:**
```bash
test -f CHANGELOG-ML.md && echo "✓ CHANGELOG-ML.md существует"
grep -q "## \[Unreleased\]" CHANGELOG-ML.md && echo "✓ Unreleased секция присутствует"
```

---

**Итог по Фазе 5:** Задачи: 6, Время: 47 часов


---

## Фаза 6: Testing & Polish

**Цель:** End-to-end тестирование, bug fixes, финальная документация
**Duration:** 10 дней (80 часов)

### Задача 6.2: Создать end-to-end тесты

**Файл:** `tests/integration/test_ml_speckit_workflow.py`
**Описание:** Создать интеграционные тесты для полного workflow
**Dependencies:** 3.2, 5.2
**Estimated Time:** 8 часов
**Priority:** High

**Acceptance Criteria:**
- [x] Тест генерации спецификации
- [x] Тест генерации плана из спецификации
- [x] Тест генерации задач из плана
- [x] Тест полного workflow
- [x] Все тесты проходят

**Testing:**
```bash
pytest tests/integration/test_ml_speckit_workflow.py -v
```

---

### Задача 6.3: Создать unit тесты для шаблонов

**Файл:** `tests/templates/test_ml_templates.py`
**Описание:** Написание unit и integration тестов для достижения 80% coverage согласно Constitution #12 и TR-001
**Dependencies:** 2.2, 2.3, 2.4, 2.5
**Estimated Time:** 8 часов
**Priority:** High (Constitution-mandated)

**Acceptance Criteria:**

1. **Test coverage >= 80% для production кода (Constitution #12, TR-001):**

   **Scope для 80% coverage:**
   - [ ] Все Python модули в `src/` (production code)
   - [ ] Все Python модули в `.qwen/commands/` (если есть Python helpers)
   - [ ] `.ml-spec/scripts/*.py` (Python скрипты, если применимо)

   **НЕ требуется 80% для:**
   - [ ] Bash скрипты (`.ml-spec/scripts/*.sh`, `.specify/scripts/*.sh`)
   - [ ] Template файлы (`.specify/templates/*.md`)
   - [ ] Configuration файлы (`.yaml`, `.toml`, `.json`)
   - [ ] Test файлы сами (`tests/*`)

   **Tooling:**
   - [ ] pytest-cov установлен: `pip install pytest-cov>=4.1`
   - [ ] Coverage config в `pyproject.toml` или `.coveragerc`:
     ```toml
     [tool.coverage.run]
     source = ["src/", ".qwen/", ".ml-spec/scripts/"]
     omit = ["*/tests/*", "*/test_*.py", "*/__pycache__/*"]

     [tool.coverage.report]
     fail_under = 80
     show_missing = true
     exclude_lines = [
         "pragma: no cover",
         "def __repr__",
         "if __name__ == .__main__.:",
         "raise NotImplementedError",
         "pass"
     ]
     ```

   **Reporting:**
   - [ ] HTML report: `pytest --cov --cov-report=html` → `htmlcov/index.html`
   - [ ] Terminal report показывает missing lines
   - [ ] Coverage badge в README.md: [![Coverage](...)]

2. **Unit tests для каждой функции:**
   - [ ] Все public functions/methods имеют тесты
   - [ ] Edge cases покрыты (empty input, None, invalid types)
   - [ ] Error handling протестирован (expected exceptions)

3. **Integration tests:**
   - [ ] Workflow тесты: specify → plan → tasks
   - [ ] Template generation end-to-end
   - [ ] File I/O operations (create, update, rollback)

4. **CI/CD integration:**
   - [ ] pytest runs с coverage check в GitHub Actions / GitLab CI
   - [ ] PR блокируется если coverage < 80%
   - [ ] Coverage trend tracking (optional but recommended)

**Примечание:** Эта задача реализует TR-001 (Testing Requirements) и Constitution #12. Coverage для src/ является обязательным требованием, а не опциональным.

**Testing:**
```bash
pytest tests/templates/test_ml_templates.py -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ Все тесты пройдены с coverage >= 80%"
open htmlcov/index.html  # Проверить coverage report визуально
```

---

### Задача 6.4: Bug fixes и исправления

**Файл:** N/A
**Описание:** Исправить все баги, найденные при тестировании
**Dependencies:** 6.2, 6.3
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

### Задача 6.5: Добавить type hints во весь CLI код

**Файл:** `src/specify_cli/__init__.py`, все модули в `src/`, `.specify/scripts/`, `.ml-spec/scripts/`
**Описание:** Добавить type hints во все функции и методы CLI согласно Constitution #3
**Dependencies:** 6.3
**Estimated Time:** 8 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Type hints добавлены во все публичные функции в `src/`
- [ ] Type hints добавлены во все методы классов в `src/`
- [ ] mypy проверка проходит без ошибок (`mypy src/ --strict`)
- [ ] Return types указаны явно
- [ ] Параметры функций аннотированы
- [ ] **Coverage для .specify/scripts/:**
   - [ ] Все `.specify/scripts/bash/*.sh` shell scripts: type comments для функций
   - [ ] Все `.specify/scripts/python/*.py`: полные type hints с mypy валидацией
- [ ] **Coverage для .ml-spec/scripts/:**
   - [ ] `setup-env.sh`: type comments для bash функций
   - [ ] `check_environment.py`: полные type hints (CheckResult, EnvironmentChecker классы)
   - [ ] Все utility scripts: type hints где применимо
- [ ] **Type checking configuration:**
   - [ ] `mypy.ini` включает секцию `[mypy-scripts.*]`
   - [ ] CI/CD запускает mypy на scripts/ директориях

**Testing:**
```bash
mypy src/ --strict
exit_code=$?
[ $exit_code -eq 0 ] && echo "✓ mypy проверка пройдена"
```

---

### Задача 6.6: Обеспечить русскоязычные docstrings во всех модулях

**Файл:** Все `.py` файлы в `src/`, `.specify/scripts/`, `.ml-spec/scripts/`, шаблоны
**Описание:** Добавить/обновить docstrings на русском языке (Google style) согласно Constitution #6
**Dependencies:** 6.5
**Estimated Time:** 6 часов
**Priority:** High

**Acceptance Criteria:**
- [ ] Все публичные модули в `src/` имеют docstrings на русском
- [ ] Все публичные классы в `src/` имеют docstrings на русском
- [ ] Все публичные функции в `src/` имеют docstrings на русском (Google style)
- [ ] Docstrings включают: описание, Args, Returns, Raises, Examples
- [ ] Примеры кода в docstrings корректны
- [ ] **Russian docstrings для scripts:**
   - [ ] `check_environment.py`: все классы и функции имеют русские docstrings
   - [ ] `setup-env.sh`: bash function комментарии на русском
   - [ ] Все `.specify/scripts/python/*.py`: русские docstrings
- [ ] **Template validation:**
   - [ ] Все template файлы имеют русские инструкции/комментарии
   - [ ] Placeholder объяснения на русском: `{{переменная}}` не `{{variable}}`
- [ ] **Validation script:**
   - [ ] Создать `validate-russian-docs.py` для проверки языка docstrings
   - [ ] Добавить в pre-commit hooks

**Testing:**
```bash
# Проверка наличия docstrings
python3 -c "import src.specify_cli; help(src.specify_cli)" | grep -q "Описание" && echo "✓ Docstrings на русском"

# Проверка стиля docstrings
pydocstyle src/ --convention=google
```

---

### Задача 6.7: Настроить CI проверку coverage

**Файл:** `.github/workflows/test.yml` или аналогичный CI конфиг
**Описание:** Добавить автоматическую проверку coverage >= 80% в CI pipeline
**Dependencies:** 6.3
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

### Задача 6.8: Верификация NFR-001 (Производительность)

**Файл:** `.ml-spec/tests/test_performance.py`
**Описание:** Benchmarks для проверки производительности генерации шаблонов
**Dependencies:** 6.7
**Расчётное время:** 4 часа
**Приоритет:** СРЕДНИЙ

**Критерии приемка:**

1. **Performance тесты:**
   - [ ] Тест: генерация spec.md < 10 секунд
   - [ ] Тест: генерация plan.md < 10 секунд
   - [ ] Тест: генерация tasks.md < 10 секунд
   - [ ] Тест: полный цикл (specify → plan → tasks) < 1 минуты
   - [ ] Тест: поддержка файлов до 5 МБ

2. **Reporting:**
   - [ ] JSON отчёт с метриками производительности
   - [ ] Сравнение с baseline (если есть)

***

### Задача 6.9: Верификация NFR-002 (Масштабируемость)

**Файл:** `.ml-spec/tests/test_scalability.py`
**Описание:** Тесты масштабируемости для множественных проектов
**Dependencies:** 6.8
**Расчётное время:** 3 часа
**Приоритет:** СРЕДНИЙ

**Критерии приемка:**

1. **Scalability тесты:**
   - [ ] Тест: 10 параллельных проектов в одном репозитории
   - [ ] Тест: проект с 100 файлами в examples/
   - [ ] Тест: шаблон размером 500 строк Markdown
   - [ ] Memory profiling: не более 512 МБ RAM

2. **Stress testing:**
   - [ ] Тест на граничных значениях (edge of spec)
   - [ ] Graceful degradation при превышении лимитов

***

### Задача 6.10: Верификация NFR-003 (Надежность)

**Файл:** `.ml-spec/tests/test_reliability.py`
**Описание:** Тесты надёжности и error handling
**Dependencies:** 6.9
**Расчётное время:** 4 часа
**Приоритет:** СРЕДНИЙ

**Критерии приемка:**

1. **Reliability тесты:**
   - [ ] Тест: graceful error messages (не stack trace)
   - [ ] Тест: rollback при ошибке генерации
   - [ ] Тест: валидация YAML/TOML конфигов
   - [ ] Тест: recovery после прерывания команды

2. **Error scenarios:**
   - [ ] Невалидный input
   - [ ] Отсутствующие файлы
   - [ ] Прерывание генерации (Ctrl+C)
   - [ ] Конфликты версий

---

### Задача 6.11: Верификация локализации (FR-002)

**Файл:** `.ml-spec/tests/test_localization.py`
**Описание:** Автоматическая проверка соблюдения требований FR-002 (русский язык) в шаблонах и скриптах.
**Dependencies:** 6.10
**Расчётное время:** 2 часа
**Приоритет:** ВЫСОКИЙ

**Критерии приемки:**

1. **Проверка шаблонов:**
   - [ ] Скрипт сканирует все `.md` файлы в `.specify/templates/`
   - [ ] Проверяет наличие кириллических символов в заголовках и описаниях (порог > 50% текста)
   - [ ] Проверяет формат терминов: "Русское (English)" при первом упоминании

2. **Проверка скриптов:**
   - [ ] Проверяет `print()` и `logging` сообщения в `.ml-spec/scripts/`
   - [ ] User-facing сообщения должны быть на русском
   - [ ] Error messages должны быть на русском

3. **CI/CD Integration:**
   - [ ] Fail build, если найдены чисто английские шаблоны (кроме специальных исключений)

**Testing:**
```bash
pytest .ml-spec/tests/test_localization.py -v
```

---

**Итог по Фазе 6:** Задачи: 10, Время: 89 часов

---

## Итоговая статистика проекта

### Общие показатели
- **Общее количество задач:** 35 (обновлено: +1 задача 3.8)
- **Общее время:** 219 часов (~27 рабочих дней) (фактическая сумма по фазам)
- **Количество фаз:** 6
- **Количество milestones:** 6

### Распределение по фазам
| Фаза | Задачи | Время | Milestone |
|------|--------|-------|-----------|
| Фаза 1: Инфраструктура | 5 | 22 часа | Инфраструктура готова |
| Фаза 2: Core Templates | 5 | 26 часов | Templates созданы |
| Фаза 3: AI Commands | 7 | 29 часов | Commands работают (обновлено) |
| Фаза 4: Automation | 2 | 6 часов | Automation готова |
| Фаза 5: Examples & Docs | 6 | 47 часов | Examples и docs готовы |
| Фаза 6: Testing & Polish | 10 | 89 часов | MVP готов к использованию |
| **ИТОГО** | **35** | **222 часов** | **6 milestones** (обновлено) |

**Верификация подсчёта:**
```bash
# Автоматический подсчёт задач:
grep -c "^### Задача" specs/001-ml-adaptation/tasks.md
# Expected: 35

# Вручную по фазам:
# Phase 1: 1.0, 1.1, 1.2, 1.3, 1.4 = 5 задач
# Phase 2: 2.2, 2.3, 2.4, 2.5, 2.6 = 5 задач
# Phase 3: 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8 = 7 задач
# Phase 4: 4.2, 4.3 = 2 задач
# Phase 5: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7 = 6 задач
# Phase 6: 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11 = 10 задач
# Total: 5 + 5 + 7 + 2 + 6 + 10 = 35 задач
```

### Критические изменения (Remediation Round 5 - FINAL):
- ✅ Добавлен TR-001: Testing Requirements (отдельная секция) - CRITICAL
- ✅ Уточнён NFR-003: измеримые критерии надёжности - HIGH
- ✅ Уточнён Task 6.3: coverage scope (src/ vs templates) - HIGH
- ✅ Уточнён FR-003: MVP (data-spec) vs Post-MVP (model+eval) - MEDIUM
- ✅ Исправлен подсчёт задач: 35 задач, 222 часов - MEDIUM
- ✅ Добавлено Future Work: roadmap Post-MVP шаблонов (v1.1-1.2) - MEDIUM
- ✅ Добавлен Task 3.8: Natural Language Environment Setup - LOW
- ✅ Обновлён Task 1.0: добавлен Makefile creation - LOW
- ✅ Обновлён Task 3.7: Environment-Aware Clarification - LOW

**Итого:** +12 часов (Task 6.3 расширен), +1 секция (TR-001), roadmap уточнён, +5 часов (Tasks 3.8, 3.7, 1.0)

### Критический путь
1.0 → 1.1 → 1.2 → 2.2 → 3.2 → 3.6 → 5.2 → 6.2 → 6.5 → 6.6 → 6.9

### Параллельные возможности
- **Фаза 1**: 1.1, 1.2 могут выполняться параллельно
- **Фаза 2**: 2.2, 2.3, 2.4, 2.5, 2.6 могут выполняться параллельно
- **Фаза 3**: 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8 могут выполняться параллельно
- **Фаза 4**: 4.2, 4.3 могут выполняться параллельно
- **Фаза 5**: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7 могут выполняться параллельно
- **Фаза 6**: 6.3, 6.5, 6.6, 6.8, 6.9, 6.10 могут выполняться параллельно

---

## User Stories Mapping

### US1: Адаптация шаблонов для ML проектов (Priority: P1)
**Задачи:** 2.2, 2.3, 2.4, 2.5, 2.6, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7
**Независимый тест:** Создать спецификацию для ML проекта и проверить, что шаблоны содержат нужные ML-секции.

### US2: Поддержка русскоязычных артефактов (Priority: P2)
**Задачи:** 6.11 (верификация), все задачи (требование ко всем артефактам)
**Независимый тест:** Запустить любую команду Spec-Kit и проверить, что результат на русском языке.

### US3: Поддержка ML-специфичных шаблонов (Priority: P3)
**Задачи:** 2.2, 2.3, 2.4, 2.5 (создание шаблонов), 5.2, 5.3, 5.4 (примеры)
**Независимый тест:** Создать спецификацию для ML проекта и проверить, что доступны шаблоны для data-spec, model-spec, evaluation-plan.

---

## Implementation Strategy

### MVP First (US1 Only)
1. Завершить Фазу 1: Setup (1.0, 1.1, 1.2, 1.3, 1.4)
2. Завершить Фазу 2: Templates (только базовые) (2.2, 2.3, 2.4, 2.5, 2.6)
3. Завершить Фазу 3: Commands (только для US1) (3.2, 3.3, 3.4, 3.5, 3.6, 3.7)
4. Создать один пример (5.2)
5. Базовое тестирование (6.2, 6.3, 6.4, 6.5, 6.6)
6. **STOP и VALIDATE**: Протестировать MVP

### Incremental Delivery
1. Фаза 1 + Фаза 2 → Foundation готово
2. Добавить Фазу 3 → Commands работают
3. Добавить Фазу 4 → Automation готова
4. Добавить Фазу 5 (5.2) → Первый пример готов
5. Добавить Фазу 5 (5.3, 5.4) → Все примеры готовы
6. Добавить Фазу 6 → MVP готов к использованию

---

**Версия**: 1.2 | **Дата**: 2026-02-13 | **Статус**: Ready for implementation (Remediation Round 3)
