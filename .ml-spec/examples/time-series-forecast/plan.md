# План реализации: Прогнозирование временных рядов

**Branch**: `time-series-forecast-example` | **Date**: 2026-02-13 | **Spec**: [link to spec]
**Input**: ML спецификация из `/specs/time-series-forecast-example/spec.md`

## Резюме

Создание модели для прогнозирования спроса на товары с использованием Prophet/LightGBM approach, учитывающей сезонность, тренды и внешние факторы.

## ML Контекст

**Язык/Версия**: Python 3.9+
**Основные зависимости**: pandas, numpy, scikit-learn, prophet/lightgbm, holidays, plotly
**Хранение данных**: DVC для версионирования датасета, MLflow для версионирования моделей
**Тестирование**: pytest с покрытием >= 80%
**Платформа назначения**: CPU для обучения и инференса
**Тип проекта**: ML временные ряды (forecasting)
**Цели производительности**: MAPE < 0.15, время обновления модели < 1 часа
**Ограничения**: Воспроизводимость экспериментов, учет внешних факторов, онлайн-обновление
**Масштаб/Объем**: 2 года исторических данных (ежедневные), 1000+ товаров

## Проверка соответствия конституции

*Все ML принципы соблюдены: воспроизводимость, качество данных, код-архитектура, документация на русском*

## ML Структура проекта

```
time-series-forecast/
├── data/
│   ├── raw/                 # Исходные данные (read-only)
│   ├── processed/           # Обработанные данные
│   └── external/            # Внешние источники (праздники, погода)
├── notebooks/
│   ├── 01_eda-timeseries.ipynb  # EDA для временных рядов
│   ├── 02_baseline-forecast.ipynb # Baseline модель
│   └── 03_external-factors.ipynb # Эксперименты с внешними факторами
├── src/
│   ├── data/
│   │   ├── loader.py        # Загрузка временных рядов
│   │   └── preprocessing.py # Предобработка и feature engineering
│   ├── models/
│   │   ├── baseline_model.py # Baseline модель (Prophet)
│   │   └── lgbm_model.py    # LightGBM модель с feature engineering
│   ├── evaluation/
│   │   └── metrics.py       # Метрики для прогнозирования
│   └── utils/
│       ├── external_features.py # Генерация внешних признаков
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

1. **Data Ingestion**: Загрузка исторических данных о продажах из database/API
2. **Data Validation**: Проверка временных меток, отсутствующих значений, аномалий
3. **Preprocessing**: Imputation, агрегация по времени, создание временных признаков
4. **Feature Engineering**: Создание lag features, rolling windows, calendar features
5. **External Factors**: Загрузка и интеграция праздников, акций, погоды
6. **Model Training**: Prophet/LightGBM с учетом внешних факторов
7. **Model Evaluation**: Вычисление MAPE, MAE, RMSE, WMAPE
8. **Model Validation**: Backtesting и hold-out проверка
9. **Model Serving**: API endpoint для прогнозов и онлайн-обновления

### MLflow Tracking

- **Эксперименты**: Отдельный эксперимент для каждого товара или категории
- **Метрики**: mape, mae, rmse, wmape, smape
- **Артефакты**: Forecast plots, error plots, feature importance
- **Модели**: Регистрация обученных моделей с метаданными

### DVC Конфигурация

- **Данные**: Версионирование исторических продаж и внешних факторов
- **Пайплайн**: Отслеживание этапов feature engineering и model training
- **Версии**: Сопоставление версий данных и моделей

## ML Технические решения

### Выбор модели

- **Тип модели**: Prophet + LightGBM hybrid approach
- **Обоснование**: Prophet хорошо справляется с сезонностью и трендами, LightGBM позволяет учитывать внешние факторы и complex interactions
- **Альтернативы**: ARIMA, LSTM/GRU, Temporal Fusion Transformer

### Гиперпараметры

- **Стратегия настройки**: Grid search для Prophet, Random search для LightGBM
- **Критерии оптимизации**: MAPE на валидационной выборке
- **Ограничения**: Время обучения < 1 часа для всех товаров

### Feature Engineering

- **Temporal features**: Day of week, month, quarter, year, holidays
- **Lag features**: Sales from previous periods (1, 7, 30 days)
- **Rolling windows**: Moving averages, standard deviations
- **External features**: Holidays, promotions, weather, economic indicators

### Внешние факторы

- **Праздники**: Использование holidays package для календаря праздников
- **Акции**: Интеграция с системой управления акциями
- **Погода**: API для получения погодных данных
- **Экономические индикаторы**: CPI, unemployment rate (опционально)

## ML Dependencies

### Runtime зависимости
```python
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
prophet>=1.1.4
lightgbm>=4.0.0
holidays>=0.34
plotly>=5.15.0
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
experiment_name: demand_forecasting
random_seed: 42
forecast_horizon: 30
train_val_test_split: [0.7, 0.15, 0.15]
backtest_windows: 5
```

### Конфигурация модели (model_config.yaml)
```yaml
model_type: prophet_lgbm_hybrid
prophet_params:
  yearly_seasonality: true
  weekly_seasonality: true
  daily_seasonality: false
lgbm_params:
  num_leaves: 31
  learning_rate: 0.05
  n_estimators: 200
external_factors:
  holidays: true
  promotions: true
  weather: false
```

## ML Тестирование

### Тесты качества данных
- Проверка непрерывности временного ряда
- Проверка отсутствующих значений
- Проверка аномалий (выбросы)
- Проверка корректности временных меток

### Тесты модели
- Unit тесты для компонентов модели
- Integration тесты для пайплайна
- Backtesting тесты для точности прогнозов
- Тесты на воспроизводимость

### Тесты качества кода
- >= 80% покрытие кода тестами
- mypy type checking
- black форматирование
- flake8 линтинг

## ML Метрики

### Основные метрики
- MAPE (Mean Absolute Percentage Error) - primary metric
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- WMAPE (Weighted MAPE)

### Дополнительные метрики
- Bias (систематическая ошибка)
- SMAPE (Symmetric MAPE)
- Forecast accuracy по категориям товаров
- Business metrics (stockout rate, overstock cost)

## ML Воспроизводимость

### Seed management
- Fixed random seed для всех операций (numpy, pandas, sklearn)
- Детерминистический split на train/val/test
- Фиксированные даты для train/validation split

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
- Проверка утечки PII в логах
- Права доступа к данным продаж
- Валидация входных данных

### Проверки безопасности
- Validation входных признаков
- Rate limiting для API
- Monitoring аномалий в прогнозах

## ML Развертывание

### Serving
- FastAPI endpoint для прогнозов
- Docker контейнеризация
- Kubernetes для оркестрации

### Online Learning
- Scheduled retraining (ежедневно/еженедельно)
- Incremental model updates
- Drift detection

### Monitoring
- Prometheus metrics
- Forecast accuracy monitoring
- Data drift detection
- Model performance degradation alerts

## ML Риски и ограничения

### Технические риски
- Пропущенные значения в исторических данных
- Резкие изменения спроса (шоки)
- Нехватка исторических данных для новых товаров

### Ограничения модели
- Зависимость от качества исторических данных
- Ограниченная точность для новых товаров
- Необходимость регулярного обновления

## ML Следующие шаги

### Phase 1: Baseline
- Prophet baseline model
- Простые временные признаки
- Оценка производительности

### Phase 2: Advanced
- LightGBM с feature engineering
- Внешние факторы (праздники, акции)
- Гибридный подход

### Phase 3: Production
- API endpoint для прогнозов
- Online learning и retraining
- Monitoring и alerts
