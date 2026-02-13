---
description: Configure ML environment based on natural language description. Updates requirements.txt, environment.yml, and config.yaml files before physical installation. Use this before running `make setup`.
handoffs:
  - label: Setup Environment
    agent: speckit.setup-ml
    prompt: Run make setup to apply the configuration changes
---

## User Input

```text
$ARGUMENTS
```

## Outline

Goal: Configure ML project environment based on user's natural language description.

This command analyzes the user's requirements and updates configuration files accordingly. After running this command, the user must execute `make setup` or `bash .ml-spec/scripts/setup-env.sh` to apply the changes.

**Execution steps:**

1. **Check current environment** (optional but recommended):
   Run `.ml-spec/scripts/check_environment.py --json` to detect current setup:
   - Python version
   - Available package managers (conda, pip, uv)
   - Installed ML libraries
   - GPU/CUDA availability
   
   Parse the JSON output to understand the current state.

2. **Analyze user requirements** from `$ARGUMENTS`:
   Extract key information:
   - ML task type (Computer Vision, NLP, Tabular, etc.)
   - Framework preferences (PyTorch, TensorFlow, scikit-learn)
   - GPU requirements (CUDA version, ROCm)
   - Additional libraries needed
   - Development tools needed

3. **Update configuration files**:

   Based on the analysis, update or create the following files:

   **a) `.ml-spec/config/requirements-pip.txt`**:
   ```
   # ML Libraries
   torch>=2.0.0
   torchvision>=0.15.0
   numpy>=1.24.0
   pandas>=2.0.0
   scikit-learn>=1.3.0
   
   # MLOps
   mlflow>=2.8.0
   dvc>=3.0.0
   
   # Development
   pytest>=7.4.0
   black>=23.0.0
   mypy>=1.5.0
   ```

   **b) `.ml-spec/config/environment.yml`** (for conda):
   ```yaml
   name: ml-project
   channels:
     - pytorch
     - conda-forge
     - defaults
   dependencies:
     - python=3.11
     - pytorch>=2.0.0
     - torchvision
     - numpy
     - pandas
     - scikit-learn
     - matplotlib
     - seaborn
     - jupyter
     - pip
     - pip:
       - mlflow>=2.8.0
       - dvc>=3.0.0
   ```

   **c) `.ml-spec/config.yaml`**:
   ```yaml
   project:
     name: "{{PROJECT_NAME}}"
     type: "ml"
     language: "ru"
   
   environment:
     python_version: "3.11"
     cuda_version: "{{CUDA_VERSION}}"  # if GPU
     random_seed: 42
   
   training:
     train_val_test_split: [0.7, 0.15, 0.15]
     batch_size: 32
     epochs: 100
   
   tracking:
     experiment_tracker: "mlflow"
     model_registry: "mlflow"
     data_versioning: "dvc"
   ```

4. **Version compatibility checks**:
   - If CUDA 11.8 detected → Use PyTorch 2.0.1+cu118
   - If CUDA 12.1 detected → Use PyTorch 2.1.0+cu121
   - If ROCm detected → Use PyTorch with ROCm support
   - If CPU only → Use CPU-only PyTorch

5. **Generate configuration summary**:
   Create a summary of changes made:
   - Which files were created/updated
   - Key dependencies added
   - Version constraints applied
   - Next steps for the user

6. **Interactive Setup Options** (present to user):
   
   After updating configuration files, present the user with 3 choices:
   
   ```
   ✅ Configuration files updated successfully!
   
   📋 Files created/updated:
   - .ml-spec/config/requirements-pip.txt
   - .ml-spec/config/environment.yml  
   - .ml-spec/config.yaml
   
   🤔 Что вы хотите сделать дальше?
   
   [1] 🤖 Установить автоматически — AI выполнит установку за вас
       (make setup + настройка окружения)
   
   [2] 👤 Установить вручную — я покажу команды для самостоятельной установки
       (вы контролируете каждый шаг)
   
   [3] 👀 Предпросмотр — показать подготовленный стек пакетов без установки
       (просмотр requirements перед установкой)
   
   Выберите вариант (1/2/3):
   ```
   
   **Option 1: Автоматическая установка**
   - Run `make setup` или `bash .ml-spec/scripts/setup-env.sh`
   - Monitor output for errors
   - Report progress to user:
     - "✅ Environment setup started..."
     - "📦 Installing packages..."
     - "🔧 Configuring tools..."
     - "✅ Setup complete!"
   - If errors occur, show troubleshooting steps
   
   **Option 2: Ручная установка**
   Provide step-by-step instructions:
   ```bash
   # Шаг 1: Проверить текущее окружение
   make check
   
   # Шаг 2: Запустить установку
   make setup
   
   # Или вручную:
   bash .ml-spec/scripts/setup-env.sh
   
   # Шаг 3: Проверить установку
   make check
   ```
   
   **Option 3: Предпросмотр стека**
   Show prepared configuration without installing:
   ```
   📋 Подготовленный стек пакетов:
   
   🐍 Python: 3.11
   📦 Package Manager: conda
   
   🔬 ML Libraries:
   - torch>=2.0.0 (PyTorch)
   - torchvision>=0.15.0
   - albumentations>=1.3.0
   - numpy>=1.24.0
   - pandas>=2.0.0
   
   🛠️ Development Tools:
   - pytest>=7.4.0
   - black>=23.0.0
   - mypy>=1.5.0
   
   📊 MLOps:
   - mlflow>=2.8.0
   - dvc>=3.0.0
   
   💡 Для установки выберите опцию [1] или [2]
   ```
   
   **Default behavior:** If user doesn't specify preference, show preview (Option 3) first.

## Interactive Workflow Example

**User:** `/speckit.setup-ml Мне нужно окружение для Computer Vision с PyTorch`

**AI:** 
1. Анализирует запрос (Computer Vision + PyTorch)
2. Обновляет конфигурационные файлы
3. Предлагает 3 варианта:

```
✅ Конфигурация обновлена!

🤔 Что вы хотите сделать дальше?

[1] 🤖 Установить автоматически
[2] 👤 Установить вручную  
[3] 👀 Предпросмотр стека

Выберите вариант (1/2/3): 
```

**Scenario A - User selects [1] Auto-install:**
```
🚀 Запускаю автоматическую установку...
📦 Создаю conda окружение 'ml-project'...
⬇️  Устанавливаю pytorch=2.1.0...
⬇️  Устанавливаю torchvision...
⬇️  Устанавливаю albumentations...
🔧 Настраиваю pre-commit hooks...
✅ Установка завершена успешно!

💡 Проверьте: make check
```

**Scenario B - User selects [2] Manual:**
```
👤 Инструкция для ручной установки:

# 1. Проверить окружение
make check

# 2. Запустить установку  
bash .ml-spec/scripts/setup-env.sh

# 3. Проверить результат
make check
```

**Scenario C - User selects [3] Preview:**
```
👀 Предпросмотр подготовленного стека:

🐍 Python: 3.11
📦 Manager: conda

🔬 ML Libraries (6 packages):
✓ torch>=2.0.0+cu118 (CUDA 11.8)
✓ torchvision>=0.15.0
✓ albumentations>=1.3.0
...

💡 Всего пакетов: 15
💡 Ожидаемое время установки: ~5 минут

Хотите установить? [1] Авто / [2] Ручная
```

## Environment Configuration Examples

**Example 1: Computer Vision with PyTorch**
```
/speckit.setup-ml Мне нужно окружение для Computer Vision с PyTorch и Albumentations
```
Result:
- torch, torchvision, albumentations
- opencv-python, pillow
- GPU support if available

**Example 2: NLP with Transformers**
```
/speckit.setup-ml Нужно окружение для NLP с трансформерами
```
Result:
- transformers, datasets, tokenizers
- torch or tensorflow
- huggingface-hub

**Example 3: Tabular Data with scikit-learn**
```
/speckit.setup-ml Табличные данные, scikit-learn, XGBoost, LightGBM
```
Result:
- scikit-learn, xgboost, lightgbm
- pandas, numpy
- optuna for hyperparameter tuning

**Example 4: Full MLOps stack**
```
/speckit.setup-ml Полный MLOps стек с MLflow, DVC, Kubeflow
```
Result:
- mlflow, dvc
- kubernetes-client (for Kubeflow)
- docker
- prometheus-client (for monitoring)

## Conflict Resolution

When updating existing files:
1. Preserve user customizations (comments, extra packages)
2. Add new requirements with compatible versions
3. Never downgrade existing packages without warning
4. Log all changes made

## Error Handling

If configuration fails:
1. Show clear error message in Russian
2. Suggest manual configuration
3. Provide example configurations
4. Link to troubleshooting guide

## Notes

- This command only UPDATES configuration files
- Physical installation happens in `make setup`
- Idempotent: can be run multiple times safely
- Supports conda, pip, and uv package managers