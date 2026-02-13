<!-- 
Sync Impact Report:
Version change: 1.0.0 → 1.0.1 (minor update)
Added sections: ML-specific templates and structure
Removed sections: Original web-dev template placeholders
Templates requiring updates: 
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/plan-template.md ✅ updated  
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/data-spec-template.md ✅ created
  - .specify/templates/model-spec-template.md ✅ created
  - .specify/templates/evaluation-template.md ✅ created
  - .specify/templates/ml-spec-template.md ✅ created
  - .specify/templates/ml-plan-template.md ✅ created
  - .specify/templates/ml-tasks-template.md ✅ created
  - .specify/templates/commands/*.md ⚠ pending review
Examples requiring updates:
  - .ml-spec/examples/image-classification/ ✅ created
  - .ml-spec/examples/tabular-classification/ ✅ created
  - .ml-spec/examples/time-series-forecast/ ✅ created
Documentation requiring updates:
  - README-ML.md ✅ created
  - MIGRATION-GUIDE.md ✅ created
Follow-up TODOs: Update command prompts for ML focus
-->

# spec-kit-ml-ru Constitution

## Core Principles

### 1. Воспроизводимость экспериментов
Критично для ML:
- Random seed фиксирован (42 по умолчанию) во всех экспериментах
- Все эксперименты логируются в MLflow или Weights&Biases
- Версионирование данных через DVC
- requirements.txt с точными версиями (==, не >=)
- Конфигурации экспериментов в YAML файлах
- Git commits связаны с experiment IDs

Обязательно в каждом эксперименте:
```python
import random
import numpy as np
import torch

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
```

### 2. Качество и безопасность данных
Data Quality Gates:
- Валидация схемы данных перед обучением (pydantic schemas)
- Проверка типов, диапазонов, missing values
- Data leakage prevention: split данных ДО любого preprocessing
- Тесты на data quality (pytest-based)
- Документирование источников данных

Data Leakage Prevention:
```python
# ✅ ПРАВИЛЬНО:
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
scaler.fit(X_train)  # Только на train!
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ❌ НЕПРАВИЛЬНО:
scaler.fit(X)  # Утечка информации из test!
X_scaled = scaler.transform(X)
X_train, X_test = train_test_split(X_scaled)
```

Production Monitoring:
- Data drift detection (Evidently AI)
- Feature distribution monitoring
- Anomaly detection на входных данных

### 3. Код и архитектура
Python Best Practices:
- Python 3.9+ обязательно
- Type hints везде (mypy проверка)
- Docstrings на русском (Google style)
- Black для форматирования
- isort для импортов
- flake8 для линтинга
- pre-commit hooks обязательны

Структура проекта (cookiecutter data science):
```
project/
├── data/
│   ├── raw/           # Исходные данные (read-only)
│   ├── processed/     # Обработанные данные
│   └── external/      # Внешние источники
├── notebooks/         # Jupyter для EDA и экспериментов
│   ├── 01_eda.ipynb
│   ├── 02_baseline.ipynb
│   └── 03_experiments.ipynb
├── src/               # Production код
│   ├── data/
│   │   ├── loader.py
│   │   └── preprocessor.py
│   ├── models/
│   │   ├── baseline.py
│   │   └── main_model.py
│   ├── evaluation/
│   │   └── metrics.py
│   └── utils/
├── tests/             # Pytest тесты (coverage >= 80%)
├── models/            # Сохранённые модели
├── results/           # Графики, отчёты
├── configs/           # YAML конфигурации
├── .ml-spec/          # ML Spec-Kit
└── requirements.txt
```

Разделение Concerns:
- Jupyter notebooks ТОЛЬКО для EDA и исследований
- Production код в .py модулях
- Никакого бизнес-логики в notebooks
- Переиспользуемые функции в src/

Testing Requirements:
- pytest для всех тестов
- Coverage >= 80% для src/
- Unit tests для функций
- Integration tests для pipelines
- Fixtures для тестовых данных

### 4. ML Workflow и best practices
Обязательная Последовательность:

ШАГ 1: Simple Baseline
- Логистическая регрессия / Random Forest / Mean prediction
- Цель: быстро получить baseline метрику
- Время: 1-2 часа максимум

ШАГ 2: EDA (Exploratory Data Analysis)
- Jupyter notebook с анализом
- Распределения признаков
- Корреляции
- Missing values analysis
- Outlier detection
- Документировать находки

ШАГ 3: Feature Engineering
- Создание новых признаков
- Feature selection
- Encoding категориальных
- Scaling числовых
- Документировать rationale

ШАГ 4: Main Model Development
- Выбор архитектуры на основе EDA
- Iterative improvements
- Hyperparameter tuning (Optuna / Grid Search)

ШАГ 5: Evaluation & Error Analysis
- Confusion matrix (классификация)
- Feature importance
- SHAP values
- Error analysis (где модель ошибается)

Train/Val/Test Split:
- Train: 70% (stratified для классификации)
- Validation: 15%
- Test: 15%
- Random seed: 42
- Stratification по target для классификации

Cross-Validation:
- 5-fold CV для малых датасетов (< 10k samples)
- Stratified K-Fold для классификации
- Time Series Split для временных рядов

### 5. Метрики и experiment tracking
Метрики:

Обязательно определить:
- Бизнес-метрика (что важно для бизнеса)
- ML-метрика (что оптимизирует модель)
- Связь между ними

Логировать в MLflow/WandB:
- Training loss (каждую эпоху)
- Validation loss (каждую эпоху)
- Primary metric (accuracy/F1/MAE)
- Secondary metrics
- Training time
- System metrics (GPU usage, memory)
- Hyperparameters
- Model artifacts
- Config files

Визуализация:
- Training curves (loss, metrics vs epochs)
- Confusion matrix (классификация)
- ROC/PR curves (бинарная классификация)
- Residual plots (регрессия)
- Feature importance plots
- Сохранять все графики в results/

Artifacts:
- Модель (.pkl / .pt / .h5)
- Конфиг эксперимента (.yaml)
- Метрики (.json)
- Графики (.png)
- Logs (.log)

### 6. Документация на русском
README.md (обязательные разделы):
- Описание проекта
- Быстрый старт (Quick Start)
- Установка зависимостей
- Структура проекта
- Как запустить обучение
- Как сделать inference
- Примеры использования
- Контакты

Model Cards:
Для каждой production модели:
- Описание задачи
- Архитектура модели
- Training data описание
- Метрики производительности
- Limitations (ограничения)
- Ethical considerations
- Use cases (когда использовать)
- Maintenance (как обновлять)

Комментарии и Docstrings:
```python
def train_model(X_train: np.ndarray, y_train: np.ndarray, config: dict) -> BaseEstimator:
    """
    Обучает ML модель на тренировочных данных.
    
    Args:
        X_train: Признаки для обучения, shape (n_samples, n_features)
        y_train: Целевая переменная, shape (n_samples,)
        config: Конфигурация модели с гиперпараметрами
    
    Returns:
        Обученная модель
    
    Raises:
        ValueError: Если размеры X_train и y_train не совпадают
    
    Example:
        >>> config = {'max_depth': 6, 'n_estimators': 100}
        >>> model = train_model(X_train, y_train, config)
    """
    # Валидация входных данных
    if len(X_train) != len(y_train):
        raise ValueError("Размеры X_train и y_train должны совпадать")
    
    # Инициализация модели
    model = XGBClassifier(**config)
    
    # Обучение
    model.fit(X_train, y_train)
    
    return model
```

SPEC.md для каждого ML проекта:
- Бизнес-цель
- ML задача (тип, input/output)
- Данные (источник, размер, качество)
- Ограничения (latency, hardware)
- Success criteria
- Out of scope

### 7. Deployment и MLOps
Model Versioning:
- Semantic versioning: v1.0.0
- Major: breaking changes в API
- Minor: новые features
- Patch: bug fixes
- Git tags для каждой версии

Model Registry:
```python
# Регистрация модели
registry.register_model(
    model=trained_model,
    version="1.0.0",
    metrics={"accuracy": 0.95, "f1": 0.93},
    description="XGBoost классификатор с tuned hyperparameters"
)

# Установка production версии
registry.set_production("1.0.0")

# Rollback если нужно
registry.rollback(to_version="0.9.0")
```

API Serving (FastAPI):
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Model API", version="1.0.0")

class PredictionRequest(BaseModel):
    features: list[float]

@app.post("/predict")
async def predict(request: PredictionRequest):
    prediction = model.predict([request.features])
    return {"prediction": float(prediction)}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

Docker:
- Dockerfile для каждой модели
- docker-compose для локальной разработки
- Никаких секретов в образах
- Health checks обязательны

CI/CD Pipeline:
1. Run tests (pytest)
2. Check code quality (black, flake8, mypy)
3. Build Docker image
4. Test Docker image
5. Deploy to staging
6. Run integration tests
7. Deploy to production (manual approval)

Production Monitoring:
- Latency: p50, p95, p99
- Throughput: requests/sec
- Model accuracy drift
- Error rate
- Resource usage (CPU, memory, GPU)
- Alerts при отклонениях

### 8. Этика и compliance
Bias Detection:
- Проверка на bias по защищённым признакам (пол, возраст, раса)
- Fairness metrics (demographic parity, equal opportunity)
- Регулярный audit моделей в production

Data Privacy:
- GDPR compliance если применимо
- Анонимизация персональных данных
- Right to be forgotten implementation
- Data retention policies

Explainability:
- SHAP values для feature importance
- LIME для локальных объяснений
- Attention visualization (для deep learning)
- Human-in-the-loop для critical decisions

Model Limitations:
- Документировать когда модель НЕ работает
- Edge cases
- Known biases
- Uncertainty quantification

### 9. Технологический стек
Обязательные Библиотеки:

Data Processing:
- pandas >= 2.0 (табличные данные)
- numpy >= 1.24 (численные операции)
- dask (если данные > RAM)

Machine Learning (Classical):
- scikit-learn >= 1.3 (baseline, preprocessing)
- XGBoost >= 2.0 (gradient boosting)
- LightGBM >= 4.0 (альтернатива XGBoost)

Deep Learning:
- PyTorch >= 2.0 (ПРИОРИТЕТ)
- TensorFlow >= 2.13 (если legacy код)
- torchvision (computer vision)
- transformers (NLP, если нужно)

Visualization:
- matplotlib >= 3.7
- seaborn >= 0.12
- plotly >= 5.0 (интерактивные графики)

Experiment Tracking:
- MLflow >= 2.0 (ПРИОРИТЕТ)
- или Weights & Biases (если team collaboration)

Model Serving:
- FastAPI >= 0.100 (REST API)
- Pydantic >= 2.0 (validation)
- uvicorn (ASGI server)

Utilities:
- pyyaml (конфиги)
- python-dotenv (env variables)
- loguru (логирование)

Development Tools:
- pytest >= 7.0
- black (форматирование)
- flake8 (линтинг)
- mypy (type checking)
- isort (сортировка импортов)
- pre-commit (git hooks)

Data Versioning:
- DVC >= 3.0 (если большие датасеты)

ЗАПРЕЩЁННЫЕ библиотеки:
❌ Deprecated libraries
❌ Unmaintained packages
❌ Libraries без type stubs

Принцип минимализма:
- Добавлять зависимости только если реально нужны
- Регулярно чистить unused dependencies
- Предпочитать стандартную библиотеку

### 10. Git workflow
Branching Strategy:

main (protected):
- Production-ready код
- Только через PR
- Требуется code review
- CI/CD passed

develop:
- Integration branch
- Feature branches merge сюда

feature/[name]:
- Новые фичи
- Эксперименты
- Naming: feature/image-augmentation

experiment/[name]:
- ML эксперименты
- Naming: experiment/xgboost-tuning

hotfix/[name]:
- Critical bug fixes
- Merge напрямую в main

Commit Messages (на русском):
```
feat: Добавлен XGBoost классификатор
fix: Исправлена утечка данных в preprocessing
docs: Обновлён README с примерами
test: Добавлены тесты для data loader
refactor: Рефакторинг feature engineering pipeline
perf: Оптимизирован inference на 30%
```

Pull Request Requirements:
- Title и description на русском
- Связь с issue/task
- Code review от 1+ человека
- CI/CD passed (все тесты зелёные)
- Documentation updated
- Changelog updated

Code Review Checklist:
- [ ] Код следует PEP 8
- [ ] Type hints присутствуют
- [ ] Docstrings на русском
- [ ] Тесты написаны и проходят
- [ ] Нет data leakage
- [ ] Random seed зафиксирован
- [ ] Documentation обновлена
- [ ] Нет hardcoded values

### 11. Русскоговорность проекта
ЧТО НА РУССКОМ:

✅ Спецификации (.md файлы)
✅ Документация (README, guides, tutorials)
✅ Комментарии в коде
✅ Docstrings
✅ Логи и error messages
✅ Commit messages
✅ PR descriptions
✅ Issues и discussions
✅ Model cards
✅ Reports и presentations

ЧТО НА АНГЛИЙСКОМ:

🔤 Код (переменные, функции, классы)
🔤 Названия файлов и директорий
🔤 Git branch names
🔤 Dependencies (requirements.txt)
🔤 Config keys (YAML)
🔤 API endpoints

Пример:
```python
def train_classifier(data: pd.DataFrame, target_column: str) -> XGBClassifier:
    """
    Обучает классификатор на предоставленных данных.
    
    Функция выполняет следующие шаги:
    1. Разделение на признаки и целевую переменную
    2. Train/test split с фиксированным random_seed
    3. Обучение модели
    
    Args:
        data: Датафрейм с признаками и целевой переменной
        target_column: Название колонки с target
    
    Returns:
        Обученный классификатор XGBoost
    """
    # Разделение на X и y
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Обучение модели
    model = XGBClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    return model
```

### 12. Testing — no exceptions
Обязательные Правила:

❌ ЗАПРЕЩЕНО:
- Коммитить код без тестов
- "Быстрые эксперименты" без тестов
- Деплоить без integration tests
- Использовать test data в training
- Skip tests в CI/CD

✅ ОБЯЗАТЕЛЬНО:
- pytest для всех тестов
- Coverage >= 80% для src/
- Unit tests для каждой функции
- Integration tests для pipelines
- Fixtures для test data
- Parametrize для множественных тестов

Пример теста:
```python
import pytest
import numpy as np
from src.data.preprocessor import StandardScaler

@pytest.fixture
def sample_data():
    """Тестовые данные для preprocessor."""
    return np.array([[1, 2], [3, 4], [5, 6]])

def test_standard_scaler_fit(sample_data):
    """Тест обучения StandardScaler."""
    scaler = StandardScaler()
    scaler.fit(sample_data)
    
    # Проверяем что mean вычислен
    assert scaler.mean_ is not None
    assert len(scaler.mean_) == 2
    
    # Проверяем значения mean
    expected_mean = np.array([3.0, 4.0])
    np.testing.assert_array_almost_equal(scaler.mean_, expected_mean)

def test_standard_scaler_transform(sample_data):
    """Тест трансформации данных."""
    scaler = StandardScaler()
    scaler.fit(sample_data)
    transformed = scaler.transform(sample_data)
    
    # Проверяем shape
    assert transformed.shape == sample_data.shape
    
    # Проверяем что mean близко к 0
    assert np.abs(transformed.mean()) < 1e-10

@pytest.mark.parametrize("invalid_data", [
    np.array([]),  # Пустой массив
    np.array([1, 2, 3]),  # 1D массив
    None,  # None
])
def test_standard_scaler_invalid_input(invalid_data):
    """Тест обработки невалидных входных данных."""
    scaler = StandardScaler()
    
    with pytest.raises(ValueError):
        scaler.fit(invalid_data)
```

Test Coverage:
```bash
# Запуск тестов с coverage
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Минимум 80% для merge
# Цель: 90%+
```

## Итоговый checklist для каждого ML проекта

Перед началом:
- [ ] Создана ветка feature/[name] или experiment/[name]
- [ ] Прочитана constitution
- [ ] Создана SPEC.md с требованиями

Data:
- [ ] Данные задокументированы (источник, размер, качество)
- [ ] Data quality tests написаны
- [ ] Train/val/test split до preprocessing
- [ ] Random seed зафиксирован (42)
- [ ] DVC настроен (если большие данные)

Code:
- [ ] Структура проекта cookiecutter data science
- [ ] Type hints везде
- [ ] Docstrings на русском (Google style)
- [ ] pre-commit hooks настроены
- [ ] Tests coverage >= 80%

ML:
- [ ] Baseline модель обучена
- [ ] EDA выполнен и задокументирован
- [ ] Feature engineering документирован
- [ ] Эксперименты логируются в MLflow
- [ ] Training curves сохранены
- [ ] Error analysis выполнен

Evaluation:
- [ ] Confusion matrix (для классификации)
- [ ] Feature importance analysis
- [ ] SHAP values (для production)
- [ ] Метрики документированы

Documentation:
- [ ] README.md обновлён
- [ ] Model card создан
- [ ] SPEC.md актуален
- [ ] Примеры использования добавлены

Deployment (если нужно):
- [ ] FastAPI endpoint создан
- [ ] Docker образ собран и протестирован
- [ ] Health check работает
- [ ] Monitoring настроен
- [ ] Rollback strategy определена

Ethics:
- [ ] Bias detection выполнен
- [ ] Fairness metrics проверены
- [ ] Limitations документированы
- [ ] Data privacy compliance

Before merge:
- [ ] Все тесты зелёные
- [ ] Code review passed
- [ ] Documentation обновлена
- [ ] CHANGELOG.md обновлён
- [ ] CI/CD pipeline прошёл

## Governance
Конституция имеет высший приоритет над всеми другими практиками. Любые изменения должны быть задокументированы и одобрены. Все pull request и code review должны проверять соблюдение этих принципов. Сложность должна быть оправдана, используйте подход "начинайте с простого".

**Version**: 1.0.0 | **Ratified**: 2026-02-13 | **Last Amended**: 2026-02-13
