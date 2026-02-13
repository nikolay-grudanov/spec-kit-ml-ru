# Data Model: ML Spec-Kit Адаптация

**Branch**: `001-ml-adaptation` | **Date**: 2026-02-13 | **Spec**: [spec.md](./spec.md)

## Overview

Данный документ описывает структуру данных и сущности для адаптации Spec-Kit для ML проектов. Все шаблоны реализованы как монолитные документы (согласно FR-012) с базовым набором секций и возможностью расширения опциональными секциями (FR-011).

---

## Сущности Templates

### Entity 1: ML Spec Template

**Описание**: Шаблон спецификации ML проекта (базовый)

**Поля**:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `title` | String | Да | Название ML проекта |
| `business_goal` | Text | Да | Описание бизнес-проблемы и ожидаемой ценности |
| `success_criteria` | List<String> | Да | Критерии успеха проекта |
| `ml_task_type` | Enum | Да | Тип ML задачи (классификация, регрессия, кластеризация и т.д.) |
| `ml_task_learning_type` | Enum | Да | Тип обучения (supervised, unsupervised, reinforcement) |
| `input_data` | Text | Да | Описание входных данных |
| `output_data` | Text | Да | Описание выходных данных |
| `data_source` | String | Да | Источник данных |
| `data_size` | String | Да | Размер датасета |
| `data_quality` | Text | Да | Описание качества данных |
| `business_metrics` | List<Metric> | Да | Бизнес-метрики |
| `ml_metrics` | List<Metric> | Да | ML метрики |
| `success_thresholds` | List<Threshold> | Да | Пороги значений метрик |
| `latency_requirement` | String | Нет | Требования к латентности (если применимо) |
| `hardware_constraints` | String | Нет | Ограничения по hardware (если применимо) |
| `model_performance` | String | Нет | Требования к производительности модели (если применимо) |

**Вложенные типы**:

```typescript
// Enum для типа ML задачи
enum MLTaskType {
  CLASSIFICATION = "классификация",
  REGRESSION = "регрессия",
  CLUSTERING = "кластеризация",
  ANOMALY_DETECTION = "обнаружение аномалий",
  TIME_SERIES_FORECASTING = "прогнозирование временных рядов",
  RECOMMENDATION = "рекомендательные системы",
  NLP = "обработка естественного языка",
  COMPUTER_VISION = "компьютерное зрение",
  OTHER = "другое"
}

// Enum для типа обучения
enum LearningType {
  SUPERVISED = "supervised",
  UNSUPERVISED = "unsupervised",
  REINFORCEMENT = "reinforcement",
  SEMI_SUPERVISED = "semi-supervised"
}

// Метрика
interface Metric {
  name: string              // Название метрики
  description: string       // Описание
  measurement_unit?: string // Единица измерения (если применимо)
}

// Порог значений метрики
interface Threshold {
  metric_name: string       // Название метрики
  minimum: number           // Минимальное значение
  target: number            // Целевое значение
  target_description?: string // Описание цели
}
```

**Валидация**:
- `title` не должен быть пустым
- `business_metrics` должен содержать минимум 1 метрику
- `ml_metrics` должен содержать минимум 1 метрику
- `success_thresholds` должен содержать минимум 1 порог
- Опциональные поля могут быть опущены

---

### Entity 2: ML Plan Template

**Описание**: Шаблон плана реализации ML проекта (базовый)

**Поля**:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `title` | String | Да | Название ML проекта |
| `data_pipeline` | Text | Да | Описание data pipeline |
| `model_architecture` | Text | Да | Описание архитектуры модели |
| `training_strategy` | Text | Да | Описание стратегии обучения |
| `serving_strategy` | Text | Да | Описание стратегии деплоя |
| `phases` | List<Phase> | Да | Этапы реализации |

**Вложенные типы**:

```typescript
// Этап реализации
interface Phase {
  id: number              // Порядковый номер этапа
  name: string            // Название этапа
  description: string      // Описание этапа
  tasks: List<string>     // Список задач этапа
  deliverables: List<string> // Артефакты этапа
}

// Предопределенные этапы (пример)
enum PhaseType {
  EDA = "Этап 1: EDA (Exploratory Data Analysis)",
  BASELINE = "Этап 2: Baseline модель",
  FEATURE_ENGINEERING = "Этап 3: Feature engineering",
  MAIN_MODEL = "Этап 4: Основная модель",
  EVALUATION = "Этап 5: Evaluation и error analysis"
}
```

**Валидация**:
- `title` не должен быть пустым
- `phases` должен содержать минимум 5 этапов (согласно ML workflow из constitution)
- Каждый этап должен иметь уникальный `id`
- Опциональные поля (MLOps, monitoring, serving) добавляются как дополнительные секции

---

### Entity 3: ML Tasks Template

**Описание**: Шаблон списка задач ML проекта (базовый)

**Поля**:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `title` | String | Да | Название ML проекта |
| `task_groups` | List<TaskGroup> | Да | Группы задач |

**Вложенные типы**:

```typescript
// Группа задач
interface TaskGroup {
  name: string              // Название группы
  description: string       // Описание группы
  tasks: List<Task>         // Список задач
}

// Задача
interface Task {
  id: string                // Уникальный идентификатор задачи
  title: string             // Название задачи
  description: string       // Описание задачи
  priority: Priority        // Приоритет
  estimated_hours?: number  // Оценка времени в часах (опционально)
  dependencies?: List<string> // Зависимости от других задач (опционально)
}

// Приоритет задачи
enum Priority {
  HIGH = "высокий",
  MEDIUM = "средний",
  LOW = "низкий"
}

// Предопределенные группы задач
enum TaskGroupType {
  DATA_PREPARATION = "Подготовка данных",
  EDA_FEATURE_ENGINEERING = "EDA и feature engineering",
  MODELING = "Моделирование",
  EVALUATION_DOCUMENTATION = "Оценка и документация"
}
```

**Валидация**:
- `title` не должен быть пустым
- `task_groups` должен содержать минимум 4 группы (Data Preparation, EDA, Modeling, Evaluation)
- Каждая задача должна иметь уникальный `id`
- Задачи могут иметь зависимости друг от друга

---

### Entity 4: Data Spec Template

**Описание**: Шаблон спецификации данных (базовый)

**Поля**:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `title` | String | Да | Название проекта или датасета |
| `data_overview` | DataOverview | Да | Обзор данных |
| `data_schema` | DataSchema | Да | Схема данных |
| `data_quality` | DataQuality | Да | Качество данных |
| `preprocessing_strategy` | PreprocessingStrategy | Да | Стратегия предобработки |

**Вложенные типы**:

```typescript
// Обзор данных
interface DataOverview {
  source: string            // Источник данных
  size: string             // Размер датасета
  format: string            // Формат данных (CSV, JSON, Parquet и т.д.)
  description: string       // Описание данных
}

// Схема данных
interface DataSchema {
  features: List<Feature>  // Список признаков
  target?: Target          // Целевая переменная (если применимо)
  relationships?: List<Relationship> // Взаимосвязи между признаками (опционально)
}

// Признак
interface Feature {
  name: string             // Название признака
  type: FeatureType        // Тип признака
  description: string      // Описание признака
  values?: List<string>    // Возможные значения (для категориальных признаков)
  range?: Range            // Диапазон значений (для числовых признаков)
}

// Тип признака
enum FeatureType {
  NUMERICAL = "числовой",
  CATEGORICAL = "категориальный",
  ORDINAL = "порядковый",
  TEXT = "текстовый",
  DATETIME = "дата/время",
  BOOLEAN = "логический",
  IMAGE = "изображение",
  AUDIO = "аудио",
  VIDEO = "видео",
  OTHER = "другой"
}

// Диапазон значений
interface Range {
  min: number              // Минимальное значение
  max: number              // Максимальное значение
  unit?: string            // Единица измерения (если применимо)
}

// Целевая переменная
interface Target {
  name: string             // Название целевой переменной
  type: TargetType        // Тип целевой переменной
  description: string      // Описание
}

// Тип целевой переменной
enum TargetType {
  BINARY = "бинарная",
  MULTICLASS = "мультикласс",
  REGRESSION = "регрессия",
  CONTINUOUS = "непрерывная"
}

// Взаимосвязь между признаками
interface Relationship {
  feature_1: string        // Первый признак
  feature_2: string        // Второй признак
  type: RelationshipType  // Тип взаимосвязи
  description: string      // Описание взаимосвязи
}

// Тип взаимосвязи
enum RelationshipType {
  CORRELATION = "корреляция",
  DEPENDENCY = "зависимость",
  HIERARCHY = "иерархия",
  OTHER = "другое"
}

// Качество данных
interface DataQuality {
  missing_values: MissingValuesInfo      // Информация о missing values
  duplicates: DuplicatesInfo              // Информация о дубликатах
  outliers: OutliersInfo                  // Информация об outliers
  data_types: DataTypesInfo               // Информация о типах данных
}

// Информация о missing values
interface MissingValuesInfo {
  percentage: number      // Процент missing values
  features_with_missing: List<string> // Список признаков с missing values
  handling_strategy: string // Стратегия обработки
}

// Информация о дубликатах
interface DuplicatesInfo {
  count: number            // Количество дубликатов
  percentage: number       // Процент дубликатов
  handling_strategy: string // Стратегия обработки
}

// Информация об outliers
interface OutliersInfo {
  features_with_outliers: List<string> // Список признаков с outliers
  detection_method: string             // Метод обнаружения
  handling_strategy: string            // Стратегия обработки
}

// Информация о типах данных
interface DataTypesInfo {
  correct_types: List<string>   // Список признаков с правильными типами
  incorrect_types: List<TypeError> // Список признаков с некорректными типами
}

// Ошибка типа данных
interface TypeError {
  feature: string               // Название признака
  current_type: string         // Текущий тип
  expected_type: string        // Ожидаемый тип
  conversion_strategy: string  // Стратегия конвертации
}

// Стратегия предобработки
interface PreprocessingStrategy {
  missing_values_handling: string      // Обработка missing values
  normalization_standardization: string // Нормализация/стандартизация
  categorical_encoding: string         // Encoding категориальных признаков
  feature_engineering: List<string>    // Feature engineering
  train_val_test_split: SplitStrategy // Стратегия разделения
}

// Стратегия разделения
interface SplitStrategy {
  train_ratio: number        // Доля train
  validation_ratio: number   // Доля validation
  test_ratio: number         // Доля test
  random_seed: number        // Random seed (по умолчанию 42)
  stratification?: boolean   // Стратификация (для классификации)
  time_based?: boolean       // Временное разделение (для временных рядов)
}
```

**Валидация**:
- `title` не должен быть пустым
- `data_schema.features` должен содержать минимум 1 признак
- `train_val_test_split` в сумме должен давать 1.0
- `random_seed` должен быть фиксирован (по умолчанию 42)

---

## Сущности Examples

### Entity 5: Image Classification Example

**Описание**: Пример проекта классификации изображений

**Поля**:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `spec` | MLSpec | Да | Спецификация проекта |
| `plan` | MLPlan | Да | План реализации |
| `tasks` | MLTasks | Да | Список задач |
| `data_spec` | DataSpec | Да | Спецификация данных |

**Специфичные поля для Image Classification**:
- `ml_task_type`: CLASSIFICATION
- `ml_task_learning_type`: SUPERVISED
- `data_format`: Изображения (PNG, JPEG, и т.д.)
- `input_data`: Изображения фиксированного размера (например, 224x224x3)
- `output_data`: Класс изображения (multiclass)
- `data_schema.features`: Массив пикселей, предобработанные изображения
- `model_architecture`: CNN (например, ResNet, EfficientNet)

---

### Entity 6: Tabular Classification Example

**Описание**: Пример проекта табличной классификации

**Поля**:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `spec` | MLSpec | Да | Спецификация проекта |
| `plan` | MLPlan | Да | План реализации |
| `tasks` | MLTasks | Да | Список задач |
| `data_spec` | DataSpec | Да | Спецификация данных |

**Специфичные поля для Tabular Classification**:
- `ml_task_type`: CLASSIFICATION
- `ml_task_learning_type`: SUPERVISED
- `data_format`: Табличные данные (CSV, Parquet)
- `input_data`: Признаки (числовые, категориальные)
- `output_data`: Класс (binary или multiclass)
- `data_schema.features`: Смешанные типы признаков
- `model_architecture`: Tree-based модели (XGBoost, LightGBM) или нейросети

---

### Entity 7: Time Series Forecast Example

**Описание**: Пример проекта прогнозирования временных рядов

**Поля**:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `spec` | MLSpec | Да | Спецификация проекта |
| `plan` | MLPlan | Да | План реализации |
| `tasks` | MLTasks | Да | Список задач |
| `data_spec` | DataSpec | Да | Спецификация данных |

**Специфичные поля для Time Series Forecast**:
- `ml_task_type`: TIME_SERIES_FORECASTING
- `ml_task_learning_type`: SUPERVISED
- `data_format`: Временные ряды (CSV с временным индексом)
- `input_data`: Исторические значения
- `output_data`: Прогноз на будущий период
- `data_schema.features`: Временной индекс, числовые признаки
- `model_architecture`: ARIMA, Prophet, LSTM, Transformer

**Специфичные поля для train_val_test_split**:
- `time_based`: true (обязательно для временных рядов)
- Разделение по времени (train → val → test)

---

## Связи между сущностями

### Отношения

1. **ML Spec → ML Plan**: ML Spec является основой для ML Plan
2. **ML Plan → ML Tasks**: ML Plan детализируется в ML Tasks
3. **ML Spec → Data Spec**: ML Spec ссылается на Data Spec
4. **Example Projects**: Каждый пример содержит все 4 сущности (Spec, Plan, Tasks, Data Spec)

### Диаграмма связей

```
┌─────────────┐
│  ML Spec    │
│  Template   │
└──────┬──────┘
       │
       ├──►┌─────────────┐
       │   │  ML Plan    │
       │   │  Template   │
       │   └──────┬──────┘
       │          │
       │          ├──►┌─────────────┐
       │          │   │  ML Tasks   │
       │          │   │  Template   │
       │          │   └─────────────┘
       │
       └──►┌─────────────┐
           │  Data Spec  │
           │  Template   │
           └─────────────┘

┌─────────────────────────────┐
│   Image Classification     │
│   Example Project           │
│   (содержит все 4 сущности)  │
└─────────────────────────────┘

┌─────────────────────────────┐
│   Tabular Classification    │
│   Example Project           │
│   (содержит все 4 сущности)  │
└─────────────────────────────┘

┌─────────────────────────────┐
│   Time Series Forecast      │
│   Example Project           │
│   (содержит все 4 сущности)  │
└─────────────────────────────┘
```

---

## Константы и предопределенные значения

### Предопределенные значения для Random Seed

```typescript
const RANDOM_SEED = 42; // Фиксированный seed для воспроизводимости
```

### Предопределенные разделы для Train/Val/Test Split

```typescript
const DEFAULT_SPLIT = {
  TRAIN_RATIO: 0.70,
  VALIDATION_RATIO: 0.15,
  TEST_RATIO: 0.15
};
```

### Предопределенные этапы ML Workflow (согласно Constitution)

```typescript
const ML_WORKFLOW_PHASES = [
  {
    id: 1,
    name: "Simple Baseline",
    description: "Логистическая регрессия / Random Forest / Mean prediction",
    estimated_hours: 2
  },
  {
    id: 2,
    name: "EDA",
    description: "Анализ распределений, корреляций, missing values, outliers",
    estimated_hours: 8
  },
  {
    id: 3,
    name: "Feature Engineering",
    description: "Создание новых признаков, feature selection, encoding, scaling",
    estimated_hours: 8
  },
  {
    id: 4,
    name: "Main Model Development",
    description: "Выбор архитектуры, hyperparameter tuning",
    estimated_hours: 16
  },
  {
    id: 5,
    name: "Evaluation & Error Analysis",
    description: "Метрики, confusion matrix, feature importance, SHAP values",
    estimated_hours: 4
  }
];
```

---

## Валидационные правила

### Общие правила

1. **Обязательные поля**: Все поля, помеченные как обязательные, должны быть заполнены
2. **Единство языка**: Все текстовые поля должны быть на русском языке
3. **Смешанный подход**: Технические термины должны дублироваться на английском в скобках при первом упоминании
4. **Consistency**: Ссылки между сущностями должны быть корректными (например, `success_thresholds` в ML Spec должны соответствовать `ml_metrics`)

### Специфические правила

1. **ML Spec**:
   - `business_metrics` и `ml_metrics` должны содержать минимум 1 метрику
   - `success_thresholds` должны ссылаться на метрики из `ml_metrics`

2. **ML Plan**:
   - `phases` должен содержать минимум 5 этапов (соответствующих ML workflow)
   - Этапы должны быть упорядочены по `id`

3. **ML Tasks**:
   - `task_groups` должен содержать минимум 4 группы
   - Задачи не должны иметь циклических зависимостей

4. **Data Spec**:
   - `data_schema.features` должен содержать минимум 1 признак
   - `train_val_test_split` в сумме должен давать 1.0
   - `random_seed` должен быть фиксирован (42 по умолчанию)

---

## Расширяемость (Post-MVP)

### Опциональные секции для шаблонов

1. **MLOps секции**:
   - Monitoring и alerting
   - Model drift detection
   - Automated retraining

2. **Serving секции**:
   - API endpoints (FastAPI)
   - Batch inference pipeline
   - Real-time inference

3. **Security секции**:
   - Data privacy (GDPR, CCPA)
   - Access controls
   - Encryption

4. **Compliance секции**:
   - Regulatory requirements
   - Audit logging
   - Model explainability

5. **Ethics секции**:
   - Bias detection
   - Fairness metrics
   - Ethical considerations

### Дополнительные шаблоны (Post-MVP)

1. **Model Spec Template**: Детальная спецификация модели (architecture, hyperparameters)
2. **Evaluation Template**: План оценки (metrics, validation strategy)
3. **Metrics Spec Template**: Определение метрик производительности модели
4. **Data Quality Spec Template**: Требования к качеству данных
5. **Validation Strategy Template**: Стратегия валидации модели
6. **Security & Privacy Template**: Требования безопасности и конфиденциальности данных
7. **Version Control Template**: Стратегия управления версиями моделей и экспериментов

---

**Версия**: 1.0 | **Дата**: 2026-02-13 | **Статус**: Завершено
