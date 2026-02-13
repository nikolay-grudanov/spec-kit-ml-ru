# План реализации: Классификация табличных данных

**Branch**: `tabular-classification-example` | **Date**: 2026-02-13 | **Spec**: [link to spec]
**Input**: ML спецификация из `/specs/tabular-classification-example/spec.md`

## Резюме

Создание модели градиентного бустинга (XGBoost/LightGBM) для предсказания оттока клиентов банка с интерпретируемостью через SHAP.

## ML Контекст

**Язык/Версия**: Python 3.9+
**Основные зависимости**: pandas, numpy, scikit-learn, xgboost/lightgbm, shap, imbalanced-learn
**Хранение данных**: DVC для версионирования датасета, MLflow для версионирования моделей
**Тестирование**: pytest с покрытием >= 80%
**Платформа назначения**: CPU для обучения и инференса
**Тип проекта**: ML табличные данные (classification)
**Цели производительности**: AUC-ROC > 0.8, время инференса < 0.1 секунды
**Ограничения**: Воспроизводимость экспериментов, обработка несбалансированных классов
**Масштаб/Объем**: 10,000 клиентов для обучения, 2,000 для тестирования

## Проверка соответствия конституции

*Все ML принципы соблюдены: воспроизводимость, качество данных, код-архитектура, документация на русском*

## ML Структура проекта

```
tabular-classification/
├── data/
│   ├── raw/                 # Исходные данные (read-only)
│   ├── processed/           # Обработанные данные
│   └── external/            # Внешние источники
├── notebooks/
│   ├── 01_eda-tabular.ipynb  # EDA для табличных данных
│   ├── 02_baseline-model.ipynb # Baseline модель
│   └── 03_feature-engineering.ipynb # Feature engineering эксперименты
├── src/
│   ├── data/
│   │   ├── loader.py        # Загрузка табличных данных
│   │   └── preprocessing.py # Предобработка и feature engineering
│   ├── models/
│   │   ├── baseline_model.py # Baseline модель (Logistic Regression)
│   │   └── xgboost_model.py # XGBoost модель
│   ├── evaluation/
│   │   └── metrics.py       # Метрики для классификации
│   └── utils/
│       ├── shap_explainer.py # SHAP объяснения
│       └── visualization.py # Визуализация результатов
├── configs/
│   ├── experiment.yaml      # Конфигурации экспериментов
│   └── model_config.yaml    # Конфигурации моделей
├── models/                  # Сохраненные модели
├── results/                 # Результаты, графики
├── tests/
│   ├── unit/                # Unit тесты
│   ├── integration/         # Integration тесты
│   └── data_quality/        # Тесты качества данных
└── requirements.txt
```

## ML Pipeline архитектура

### Компоненты пайплайна

1. **Data Ingestion**: Загрузка данных о клиентах из CSV/Database
2. **Data Validation**: Проверка схемы данных, типов, диапазонов, пропущенных значений
3. **Preprocessing**: Imputation, encoding, feature engineering, scaling
4. **Feature Engineering**: Создание новых признаков, трансформация существующих
5. **Model Training**: XGBoost/LightGBM с handling class imbalance
6. **Model Evaluation**: Вычисление AUC-ROC, precision, recall, F1, confusion matrix
7. **Model Validation**: Проверка на hold-out тестовой выборке
8. **Model Serving**: API endpoint для предсказаний с SHAP объяснениями

### MLflow Tracking

- **Эксперименты**: Отдельный эксперимент для каждого типа модели и стратегии
- **Метрики**: auc-roc, accuracy, precision, recall, f1, log_loss
- **Артефакты**: confusion matrix, ROC curve, feature importance plots
- **Модели**: Регистрация обученных моделей с метаданными

### DVC Конфигурация

- **Данные**: Версионирование датасета клиентов
- **Пайплайн**: Отслеживание этапов предобработки и feature engineering
- **Версии**: Сопоставление версий данных и моделей

## ML Технические решения

### Выбор модели

- **Тип модели**: Gradient Boosting (XGBoost/LightGBM)
- **Обоснование**: Хорошая производительность на табличных данных, встроенная обработка пропущенных значений, поддержка интерпретируемости через SHAP
- **Альтернативы**: Random Forest, Logistic Regression, Neural Networks

### Гиперпараметры

- **Стратегия настройки**: Random search для XGBoost/LightGBM гиперпараметров
- **Критерии оптимизации**: AUC-ROC на валидационной выборке
- **Ограничения**: Время обучения < 30 минут на CPU

### Handling Class Imbalance

- **Стратегия**: SMOTE для oversampling minority class, class weights в loss function
- **Альтернативы**: Undersampling majority class, focal loss

### Интерпретируемость

- **Метод**: SHAP (SHapley Additive exPlanations)
- **Визуализация**: Summary plots, dependence plots, force plots
- **Альтернативы**: LIME, permutation feature importance

## ML Dependencies

### Runtime зависимости
```python
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
xgboost>=2.0.0
shap>=0.42.0
imbalanced-learn>=0.11.0
```

### Dev зависимости
```python
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.7.0
flake8>=6.1.0
mypy>=1.5.0
```

## ML Конфигурация

### Конфигурация эксперимента (experiment.yaml)
```yaml
experiment_name: churn_prediction
random_seed: 42
train_val_test_split: [0.7, 0.15, 0.15]
cross_validation_folds: 5
early_stopping_rounds: 50
```

### Конфигурация модели (model_config.yaml)
```yaml
model_type: xgboost
params:
  max_depth: 6
  learning_rate: 0.1
  n_estimators: 100
  subsample: 0.8
  colsample_bytree: 0.8
  scale_pos_weight: 5
class_weights: balanced
```

## ML Тестирование

### Тесты качества данных
- Проверка пропущенных значений
- Проверка типов данных
- Проверка диапазонов значений
- Проверка уникальности ID клиентов

### Тесты модели
- Unit тесты для компонентов модели
- Integration тесты для пайплайна
- Тесты на воспроизводимость

### Тесты качества кода
- >= 80% покрытие кода тестами
- mypy type checking
- black форматирование
- flake8 линтинг

## ML Метрики

### Основные метрики
- AUC-ROC (primary metric)
- Accuracy, Precision, Recall, F1-score
- Confusion matrix
- Log loss

### Дополнительные метрики
- Feature importance
- SHAP values
- Calibration curve
- Business metrics (expected churn reduction)

## ML Воспроизводимость

### Seed management
- Fixed random seed для всех операций (numpy, pandas, sklearn)
- Детерминистический split на train/val/test

### Version control
- DVC для версионирования данных
- MLflow для версионирования моделей
- Git для кода и конфигураций

### Documentation
- README с инструкциями по воспроизведению
- Jupyter notebooks с EDA
- MLflow run tracking

## ML Безопасность и конфиденциальность

### Защита данных
- Anonymization PII (личных данных)
- Проверка утечки PII в логах
- Права доступа к данным

### Проверки безопасности
- Validation input данных
- Rate limiting для API
- Monitoring аномалий

## ML Развертывание

### Serving
- FastAPI endpoint для предсказаний
- Docker контейнеризация
- Kubernetes для оркестрации

### Monitoring
- Prometheus metrics
- Data drift detection
- Model performance monitoring

## ML Риски и ограничения

### Технические риски
- Несбалансированные классы
- Пропущенные значения
- Категориальные признаки с высокой кардинальностью

### Ограничения модели
- Линейная комбинация признаков (для baseline)
- Зависимость от качества данных
- Потенциальное смещение в обучающих данных

## ML Следующие шаги

### Phase 1: Baseline
- Logistic Regression baseline
- Простая предобработка
- Оценка производительности

### Phase 2: Advanced
- XGBoost/LightGBM
- Advanced feature engineering
- Handling class imbalance

### Phase 3: Production
- API endpoint
- SHAP объяснения
- Monitoring
