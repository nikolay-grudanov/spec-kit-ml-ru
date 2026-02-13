#!/bin/bash

# Скрипт для установки pre-commit hooks в ML Spec-Kit проекте
# Использование: bash .specify/scripts/setup-precommit.sh

set -e

echo "🔧 Настройка pre-commit hooks для ML Spec-Kit..."

# Проверка наличия pre-commit
if ! command -v pre-commit &> /dev/null; then
    echo "⚠️  pre-commit не установлен. Установка через pip..."
    pip install pre-commit
fi

# Проверка наличия конфигурационного файла
if [ ! -f .pre-commit-config.yaml ]; then
    echo "❌ Файл .pre-commit-config.yaml не найден!"
    exit 1
fi

# Установка hooks
echo "📦 Установка pre-commit hooks..."
pre-commit install

# Запуск hooks на всех файлах для проверки
echo "✅ Запуск pre-commit hooks на всех файлах..."
pre-commit run --all-files || {
    echo ""
    echo "⚠️  Некоторые pre-commit проверки не прошли."
    echo "💡 Исправьте проблемы и запустите: pre-commit run --all-files"
    exit 1
}

echo ""
echo "✨ Pre-commit hooks успешно настроены!"
echo ""
echo "📝 Информация:"
echo "  - Hooks будут автоматически запускаться перед каждым коммитом"
echo "  - Для ручного запуска используйте: pre-commit run --all-files"
echo "  - Для обновления hooks используйте: pre-commit autoupdate"
echo ""
