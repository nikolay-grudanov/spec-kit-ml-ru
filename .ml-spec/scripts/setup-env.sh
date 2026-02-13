#!/bin/bash

# Интерактивный скрипт настройки ML окружения
# Использование: bash .ml-spec/scripts/setup-env.sh

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo ""
echo "🚀 Настройка ML окружения для Spec-Kit"
echo "=========================================="
echo ""

# Функция для определения доступных package managers
detect_package_managers() {
    local managers=()
    
    if command -v conda &> /dev/null; then
        managers+=("conda")
    fi
    
    if command -v uv &> /dev/null; then
        managers+=("uv")
    fi
    
    # pip всегда доступен в Python
    if command -v pip3 &> /dev/null; then
        managers+=("pip")
    fi
    
    if [ ${#managers[@]} -eq 0 ]; then
        echo -e "${RED}❌ Ошибка: не найден package manager (conda, uv, pip)${NC}"
        exit 1
    fi
    
    echo "${managers[@]}"
}

# Определение доступных package managers
AVAILABLE_MANAGERS=($(detect_package_managers))
echo -e "${BLUE}📦 Обнаружены package managers:${NC}"
for manager in "${AVAILABLE_MANAGERS[@]}"; do
    echo "  - $manager"
done
echo ""

# Вопрос пользователю
echo -e "${YELLOW}Окружение готово? [y/n]${NC}"
read -p "> " env_ready

if [[ $env_ready =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔍 Запуск проверки окружения..."
    python3 "$PROJECT_ROOT/.ml-spec/scripts/check_environment.py"
    exit_code=$?
    exit $exit_code
else
    echo ""
    echo -e "${BLUE}🛠️  Настройка окружения...${NC}"
    echo ""
fi

# Выбор package manager
echo "Выберите package manager для настройки:"
select pkg_manager in "${AVAILABLE_MANAGERS[@]}" "Exit"; do
    case $pkg_manager in
        "Exit")
            echo "Выход..."
            exit 0
            ;;
        *)
            echo -e "${GREEN}✓ Выбран: $pkg_manager${NC}"
            break
            ;;
    esac
done

# Настройка окружения
case $pkg_manager in
    "conda")
        setup_conda
        ;;
    "uv")
        setup_uv
        ;;
    "pip")
        setup_pip
        ;;
esac

# Функция настройки Conda
setup_conda() {
    echo ""
    echo -e "${BLUE}📦 Настройка Conda окружения...${NC}"
    
    # Проверка существования окружения
    if conda env list | grep -q "ml-spec-kit"; then
        echo -e "${YELLOW}⚠️  Окружение 'ml-spec-kit' уже существует${NC}"
        read -p "Обновить существующее окружение? [y/n]: " update_env
        if [[ ! $update_env =~ ^[Yy]$ ]]; then
            return
        fi
    else
        echo "Создание нового окружения..."
        conda env create -f "$PROJECT_ROOT/.ml-spec/config/environment.yml"
        echo -e "${GREEN}✓ Окружение 'ml-spec-kit' создано${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}💡 Активируйте окружение командой:${NC}"
    echo "   conda activate ml-spec-kit"
}

# Функция настройки UV
setup_uv() {
    echo ""
    echo -e "${BLUE}📦 Настройка UV окружения...${NC}"
    
    if [ ! -d "$PROJECT_ROOT/.venv" ]; then
        echo "Создание виртуального окружения..."
        uv venv "$PROJECT_ROOT/.venv"
        echo -e "${GREEN}✓ UV виртуальное окружение создано${NC}"
    else
        echo -e "${YELLOW}⚠️  Виртуальное окружение уже существует${NC}"
    fi
    
    echo "Установка зависимостей..."
    uv pip install -r "$PROJECT_ROOT/.ml-spec/config/requirements-uv.txt"
    echo -e "${GREEN}✓ Зависимости установлены${NC}"
    
    echo ""
    echo -e "${BLUE}💡 Активируйте окружение командой:${NC}"
    echo "   source .venv/bin/activate"
}

# Функция настройки PIP
setup_pip() {
    echo ""
    echo -e "${BLUE}📦 Настройка PIP окружения...${NC}"
    
    if [ ! -d "$PROJECT_ROOT/.venv" ]; then
        echo "Создание виртуального окружения..."
        python3 -m venv "$PROJECT_ROOT/.venv"
        echo -e "${GREEN}✓ Виртуальное окружение создано${NC}"
    else
        echo -e "${YELLOW}⚠️  Виртуальное окружение уже существует${NC}"
    fi
    
    echo "Установка зависимостей..."
    source "$PROJECT_ROOT/.venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$PROJECT_ROOT/.ml-spec/config/requirements-pip.txt"
    deactivate
    echo -e "${GREEN}✓ Зависимости установлены${NC}"
    
    echo ""
    echo -e "${BLUE}💡 Активируйте окружение командой:${NC}"
    echo "   source .venv/bin/activate"
}

# Установка development tools
echo ""
echo -e "${BLUE}🛠️  Установка development tools...${NC}"

# Проверка активного окружения
if [ -n "$VIRTUAL_ENV" ] || [ -n "$CONDA_PREFIX" ]; then
    echo "Установка dev tools..."
    pip install -r "$PROJECT_ROOT/.ml-spec/config/requirements-dev.txt"
    echo -e "${GREEN}✓ Development tools установлены${NC}"
else
    echo -e "${YELLOW}⚠️  Сначала активируйте окружение для установки dev tools${NC}"
fi

# Финальная проверка
echo ""
echo "=========================================="
echo -e "${GREEN}✨ Настройка окружения завершена!${NC}"
echo ""
echo "📝 Следующие шаги:"
echo "  1. Активируйте окружение"
echo "  2. Проверьте окружение: python3 .ml-spec/scripts/check_environment.py"
echo "  3. Создайте ML проект: bash .specify/scripts/setup-ml.sh <project-name>"
echo ""
