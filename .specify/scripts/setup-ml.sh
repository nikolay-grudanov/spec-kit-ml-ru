#!/bin/bash

# Скрипт для инициализации ML проекта
# Использование: bash .specify/scripts/setup-ml.sh <project-name>

set -e

# Получаем путь к корню проекта (2 уровня выше от .specify/scripts)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Ошибка: не указано название проекта${NC}"
    echo "Использование: bash .specify/scripts/setup-ml.sh <project-name>"
    exit 1
fi

PROJECT_NAME=$1
PROJECT_DIR="$PROJECT_ROOT/$PROJECT_NAME"

echo ""
echo "🚀 Инициализация ML проекта: $PROJECT_NAME"
echo "========================================"
echo ""

# Проверка существования директории
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}⚠️  Директория '$PROJECT_DIR' уже существует${NC}"
    read -p "Продолжить в существующей директории? [y/n]: " continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        exit1
    fi
else
    mkdir -p "$PROJECT_DIR"
    echo -e "${GREEN}✓${NC} Директория создана: $PROJECT_DIR"
fi

# Переходим в директорию проекта
cd "$PROJECT_DIR"

# Создание структуры директорий
echo ""
echo "📁 Создание структуры проекта..."

# Data directories
mkdir -p data/raw data/processed data/external
echo -e "${GREEN}✓${NC} data/raw/"
echo -e "${GREEN}✓${NC} data/processed/"
echo -e "${GREEN}✓${NC} data/external/"

# Notebook directories
mkdir -p notebooks
echo -e "${GREEN}✓${NC} notebooks/"

# Source directories
mkdir -p src/data src/models src/evaluation src/utils
echo -e "${GREEN}✓${NC} src/data/"
echo -e "${GREEN}✓${NC} src/models/"
echo -e "${GREEN}✓${NC} src/evaluation/"
echo -e "${GREEN}✓${NC} src/utils/"

# Test directories
mkdir -p tests/unit tests/integration tests/data_quality
echo -e "${GREEN}✓${NC} tests/unit/"
echo -e "${GREEN}✓${NC} tests/integration/"
echo -e "${GREEN}✓${NC} tests/data_quality/"

# Config directories
mkdir -p configs
echo -e "${GREEN}✓${NC} configs/"

# Models and results directories
mkdir -p models results logs
echo -e "${GREEN}✓${NC} models/"
echo -e "${GREEN}✓${NC} results/"
echo -e "${GREEN}✓${NC} logs/"

# Копирование конфигурационного файла
echo ""
echo "📋 Настройка конфигурации..."

if [ -f "$PROJECT_ROOT/.ml-spec/config.yaml" ]; then
    cp "$PROJECT_ROOT/.ml-spec/config.yaml" config.yaml
    echo -e "${GREEN}✓${NC} config.yaml скопирован из $PROJECT_ROOT/.ml-spec/config.yaml"
else
    echo -e "${YELLOW}⚠️  Файл конфигурации не найден: $PROJECT_ROOT/.ml-spec/config.yaml${NC}"
    echo -e "${YELLOW}⚠️  Создан базовый config.yaml${NC}"
    
    # Создание базового config.yaml
    cat > config.yaml << EOF
# Конфигурация ML проекта: $PROJECT_NAME

# Настройки воспроизводимости
random_seed: 42

# Настройки разделения данных
train_val_test_split:
  train: 0.70
  validation: 0.15
  test: 0.15

# Язык артефактов
language: ru

# Experiment tracking
experiment_tracking:
  tool: mlflow
  tracking_uri: ./mlruns

# Data versioning
data_versioning:
  tool: dvc
  remote: local
EOF
    echo -e "${GREEN}✓${NC} config.yaml создан"
fi

# Создание __init__.py файлов
echo ""
echo "📝 Создание Python модулей..."

for dir in src src/data src/models src/evaluation src/utils; do
    if [ ! -f "$dir/__init__.py" ]; then
        touch "$dir/__init__.py"
        echo -e "${GREEN}✓${NC} $dir/__init__.py"
    fi
done

# Создание .gitkeep файлов для пустых директорий
echo ""
echo "🔒 Создание .gitkeep файлов..."

for dir in data/raw data/processed data/external tests/unit tests/integration tests/data_quality; do
    touch "$dir/.gitkeep"
    echo -e "${GREEN}✓${NC} $dir/.gitkeep"
done

# Создание базовых файлов
echo ""
echo "📄 Создание базовых файлов..."

# README.md
if [ ! -f "README.md" ]; then
    cat > README.md << EOF
# $PROJECT_NAME

## Описание

ML проект: $PROJECT_NAME

## Быстрый старт

1. Настройка окружения:
    \`\`\`bash
    cd $PROJECT_ROOT && make setup
    # Или:
    bash .ml-spec/scripts/setup-env.sh
    \`\`\`

2. Установка зависимостей:
    \`\`\`bash
    cd $PROJECT_ROOT && pip install -r .ml-spec/config/requirements-pip.txt
    # Или с Makefile:
    make setup
    \`\`\`

3. Запуск экспериментов:
    \`\`\`bash
    cd $PROJECT_NAME && jupyter notebook notebooks/01_eda.ipynb
    \`\`\`

## Структура проекта

- \`data/\` - Данные проекта
  - \`raw/\` - Исходные данные (read-only)
  - \`processed/\` - Обработанные данные
  - \`external/\` - Внешние источники
- \`notebooks/\` - Jupyter notebooks
- \`src/\` - Исходный код
  - \`data/\` - Загрузка и обработка данных
  - \`models/\` - Модели
  - \`evaluation/\` - Оценка моделей
  - \`utils/\` - Утилиты
- \`tests/\` - Тесты
  - \`unit/\` - Unit тесты
  - \`integration/\` - Integration тесты
  - \`data_quality/\` - Тесты качества данных
- \`configs/\` - Конфигурации экспериментов
- \`models/\` - Сохраненные модели
- \`results/\` - Графики и отчёты
- \`logs/\` - Логи

## Документация

Для генерации спецификации, плана и задач используйте команды Qwen CLI:
- \`/speckit.specify <описание проекта>\` - Генерация ML спецификации
- \`/speckit.plan\` - Генерация ML плана реализации
- \`/speckit.tasks\` - Генерация списка задач
- \`/speckit.clarify\` - Уточнение требований

## Быстрый старт (Quick Start)

Используйте Makefile для упрощенного workflow:
- \`make help\` - Показать все доступные команды
- \`make setup\` - Настроить ML окружение
- \`make check\` - Проверить окружение
- \`make init <project-name>\` - Создать новый ML проект
- \`make test\` - Запустить тесты
- \`make lint\` - Проверить код стиль

## Конфигурация

Основные настройки находятся в \`config.yaml\`.
Дополнительные настройки в \`configs/experiment.yaml\` и \`configs/model_config.yaml\`.
EOF
    echo -e "${GREEN}✓${NC} README.md создан"
fi

# requirements.txt
if [ ! -f "requirements.txt" ]; then
    if [ -f "$PROJECT_ROOT/.ml-spec/config/requirements-pip.txt" ]; then
        cp "$PROJECT_ROOT/.ml-spec/config/requirements-pip.txt" requirements.txt
        echo -e "${GREEN}✓${NC} requirements.txt создан"
    else
        echo -e "${YELLOW}⚠️  Файл requirements-pip.txt не найден${NC}"
    fi
fi

# .gitignore
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*\$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual environments
venv/
.venv/
ENV/
env/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# ML
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep
models/*
results/
logs/
mlruns/

# IDE
.vscode/
.idea/
*.swp
.DS_Store
EOF
    echo -e "${GREEN}✓${NC} .gitignore создан"
fi

echo ""
echo "========================================"
echo -e "${GREEN}✨ Проект '$PROJECT_NAME' успешно инициализирован!${NC}"
echo ""
echo "📝 Следующие шаги:"
echo "  1. Перейдите в директорию: cd $PROJECT_NAME"
echo "  2. Настройте окружение: cd $PROJECT_ROOT && make setup"
echo "  3. Установите зависимости: pip install -r requirements.txt"
echo "  4. Начните работу с Jupyter notebooks"
echo ""
echo "💡 Для генерации документации используйте команды Qwen CLI"
echo ""
