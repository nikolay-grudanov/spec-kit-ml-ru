# Quick Start: ML Spec-Kit

**Branch**: `001-ml-adaptation` | **Date**: 2026-02-13 | **Spec**: [spec.md](./spec.md)

## Быстрый старт

ML Spec-Kit — это адаптация GitHub Spec-Kit для ML/DS проектов. Все артефакты генерируются на русском языке с использованием ML-ориентированных шаблонов.

---

## Установка

### Требования

- Python 3.9+
- Qwen CLI (для интеграции с AI агентом)

### Установка Specify CLI

```bash
pip install specify-cli
```

### Настройка Qwen CLI

```bash
npm install -g qwen
qwen login
```

---

## Создание ML проекта

### Шаг 1: Инициализация проекта

```bash
specify init --ml
```

Эта команда создаст базовую структуру проекта с ML-ориентированными шаблонами.

### Шаг 2: Генерация спецификации

```bash
/speckit.specify Создать систему классификации изображений для определения типов одежды на основе датасета Fashion MNIST. Требуется точность (accuracy) не менее 90%.
```

Эта команда создаст файл `spec.md` с ML-ориентированной спецификацией.

**Пример спецификации**:
```markdown
# Спецификация ML проекта: Классификация одежды

## Бизнес-цель
- Автоматизация сортировки одежды на складе
- Сокращение времени обработки заказов на 30%

## Задача машинного обучения
- Тип задачи: классификация (classification)
- Входные данные: изображения одежды (28x28 пикселей)
- Выходные данные: тип одежды (10 классов)
- Тип обучения: supervised

## Данные
- Источник: Fashion MNIST
- Размер: 70,000 изображений
- Формат: PNG

## Метрики
- Бизнес-метрика: сокращение времени обработки заказов
- ML метрики: accuracy, F1-score
- Success thresholds: accuracy >= 90%

## Ограничения
- Latency: < 100ms на inference
- Hardware: CPU inference поддерживается
```

### Шаг 3: Генерация плана

```bash
/speckit.plan spec.md
```

Эта команда создаст файл `plan.md` с планом реализации.

**Пример плана**:
```markdown
# План реализации ML проекта: Классификация одежды

## Архитектура решения
- Data pipeline: загрузка изображений, нормализация
- Model architecture: CNN (ResNet-18)
- Training strategy: transfer learning
- Serving strategy: FastAPI endpoint

## Этапы реализации
- Этап 1: EDA (Exploratory Data Analysis)
  - Анализ распределения классов
  - Визуализация примеров
- Этап 2: Baseline модель
  - Логистическая регрессия
  - Цель: accuracy >= 70%
- Этап 3: Feature engineering
  - Аугментация изображений
  - Нормализация
- Этап 4: Основная модель
  - CNN (ResNet-18)
  - Hyperparameter tuning
- Этап 5: Evaluation и error analysis
  - Confusion matrix
  - SHAP values
```

### Шаг 4: Генерация задач

```bash
/speckit.tasks plan.md
```

Эта команда создаст файл `tasks.md` со списком задач.

**Пример задач**:
```markdown
# Задачи ML проекта: Классификация одежды

## Подготовка данных
- [ ] Загрузка данных из Fashion MNIST
- [ ] Разделение на train/val/test (70/15/15)
- [ ] Валидация качества данных

## EDA и feature engineering
- [ ] Анализ распределения классов
- [ ] Визуализация примеров каждого класса
- [ ] Реализация аугментации изображений
- [ ] Нормализация пикселей

## Моделирование
- [ ] Обучение baseline модели (логистическая регрессия)
- [ ] Обучение CNN (ResNet-18)
- [ ] Hyperparameter tuning (learning rate, batch size)

## Оценка и документация
- [ ] Расчет метрик (accuracy, F1-score)
- [ ] Создание confusion matrix
- [ ] Error analysis
- [ ] Создание model card
```

---

## Работа с примерами

ML Spec-Kit включает три полных примера проектов:

### 1. Классификация изображений (Image Classification)

```bash
cd .ml-spec/examples/image-classification
cat spec.md
cat plan.md
cat tasks.md
cat data-spec.md
```

### 2. Табличная классификация (Tabular Classification)

```bash
cd .ml-spec/examples/tabular-classification
cat spec.md
cat plan.md
cat tasks.md
cat data-spec.md
```

### 3. Прогнозирование временных рядов (Time Series Forecast)

```bash
cd .ml-spec/examples/time-series-forecast
cat spec.md
cat plan.md
cat tasks.md
cat data-spec.md
```

---

## Уточнение требований

Если вам нужно уточнить детали проекта, используйте команду `/speckit.clarify`:

```bash
/speckit.clarify spec.md Какие конкретные метрики качества данных важны для этого проекта?
```

Эта команда обновит файл `spec.md` с добавленными деталями.

---

## Структура проекта

```
ml-project/
├── spec.md              # Спецификация ML проекта
├── plan.md              # План реализации
├── tasks.md             # Список задач
├── data-spec.md         # Спецификация данных
├── .specify/            # Шаблоны Spec-Kit
│   └── templates/
│       ├── ml-spec-template.md
│       ├── ml-plan-template.md
│       ├── ml-tasks-template.md
│       └── data-spec-template.md
├── .qwen/               # Команды Qwen CLI
│   └── commands/
│       ├── speckit.specify.md
│       ├── speckit.plan.md
│       ├── speckit.tasks.md
│       └── speckit.clarify.md
├── .ml-spec/            # Примеры проектов
│   └── examples/
│       ├── image-classification/
│       ├── tabular-classification/
│       └── time-series-forecast/
├── data/                # Данные проекта
│   ├── raw/
│   ├── processed/
│   └── external/
├── notebooks/            # Jupyter notebooks
│   ├── 01_eda.ipynb
│   ├── 02_baseline.ipynb
│   └── 03_experiments.ipynb
├── src/                 # Production код
│   ├── data/
│   ├── models/
│   ├── evaluation/
│   └── utils/
├── tests/               # Тесты
├── models/              # Сохранённые модели
├── results/             # Графики, отчёты
└── configs/             # Конфигурации
```

---

## Полезные советы

### 1. Начните с простого

Создайте спецификацию для небольшого, понятного проекта, чтобы понять структуру шаблонов.

### 2. Используйте примеры

Посмотрите на примеры в `.ml-spec/examples/` для понимания структуры и содержания артефактов.

### 3. Итеративный процесс

Генерируйте артефакты последовательно: spec → plan → tasks. После уточнения требований можно перегенерировать.

### 4. Следуйте ML best practices

Шаблоны включают секции для reproducibility, data quality, metrics, evaluation и других best practices.

### 5. Документируйте решения

Используйте комментарии в артефактах для объяснения принятых решений.

---

## FAQ

**Q: Можно ли использовать старые веб-шаблоны Spec-Kit?**

A: Нет, ML-ориентированные шаблоны заменяют веб-ориентированные. Структура шаблонов полностью изменена для ML проектов.

**Q: Как создавать смешанные проекты (часть веб, часть ML)?**

A: Для смешанных проектов можно использовать веб-шаблоны для веб-части и ML-шаблоны для ML-части. Свяжите их ссылками в спецификациях.

**Q: Какие метрики являются обязательными в спецификации?**

A: Минимум одна бизнес-метрика и одна ML метрика. Success thresholds должны быть определены для ML метрик.

**Q: Как обеспечить воспроизводимость экспериментов?**

A: Используйте фиксированный random seed (42 по умолчанию), логируйте эксперименты в MLflow/Weights&Biases, версионируйте данные через DVC.

**Q: Как определить размер train/val/test split?**

A: Для большинства проектов используйте 70/15/15 (train/val/test). Для малых датасетов (<10k samples) используйте 5-fold cross-validation.

---

## Следующие шаги

1. **Изучите примеры**: `.ml-spec/examples/`
2. **Прочитайте документацию**: `README-ML.md`
3. **Изучите руководство по миграции**: `MIGRATION-GUIDE.md`
4. **Создайте первый ML проект**: Используйте `/speckit.specify` для генерации спецификации

---

## Поддержка

- GitHub Issues: [https://github.com/your-repo/spec-kit-ml-ru/issues](https://github.com/your-repo/spec-kit-ml-ru/issues)
- Документация: [README-ML.md](../README-ML.md)
- Примеры: [.ml-spec/examples/](../.ml-spec/examples/)

---

**Версия**: 1.0 | **Дата**: 2026-02-13
