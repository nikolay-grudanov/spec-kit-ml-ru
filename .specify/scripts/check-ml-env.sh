#!/bin/bash

# Скрипт для проверки зависимостей ML Spec-Kit
# Использование: bash .specify/scripts/check-ml-env.sh

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "🔍 Проверка зависимостей ML Spec-Kit"
echo "===================================="
echo ""

# Счётчики
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

check_command() {
    local name=$1
    local command=$2

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if command -v $command &> /dev/null; then
        version=$($command --version 2>&1 | head -1)
        echo -e "${GREEN}✓${NC} $name: $version"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $name: не установлен"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_version() {
    local name=$1
    local command=$2
    local min_version=$3

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if command -v $command &> /dev/null; then
        current_version=$($command --version 2>&1 | grep -oP '\d+\.\d+\.\d+|\d+\.\d+' | head -1)
        if [ -n "$current_version" ]; then
            echo -e "${GREEN}✓${NC} $name: $current_version"

            # Сравнение версий (простая проверка)
            if [ "$current_version" = "$min_version" ] || [ "$current_version" ">" "$min_version" ]; then
                return 0
            fi
        fi
    fi

    echo -e "${RED}✗${NC} $name: требуется версия >= $min_version"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
    return 1
}

check_file() {
    local name=$1
    local file=$2

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $name: найден"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $name: не найден ($file)"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Запуск Python скрипта проверки окружения
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")"

python3 "$PROJECT_ROOT/.ml-spec/scripts/check_environment.py"
