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
    - ML task type (Computer Vision, NLP, Tabular, RL, etc.)
    - Framework preferences (PyTorch, TensorFlow, scikit-learn)
    - GPU requirements (CUDA version, ROCm)
    - Additional libraries needed
    - Development tools needed

3. **Ask user for preferences using `question` tool** (MUST do this BEFORE updating any configuration files):

    **Question 1: Environment Type**
    Use the `question` tool with this JSON structure:
    ```json
    {
      "questions": [
        {
          "header": "Тип окружения",
          "question": "Хотите создать новое окружение или использовать текущее?",
          "options": [
            {
              "label": "Новое изолированное окружение",
              "description": "Рекомендуется для чистого старта проекта"
            },
            {
              "label": "Использовать текущее окружение",
              "description": "Быстрее, но могут быть конфликты версий"
            }
          ],
          "multiple": false
        }
      ]
    }
    ```
    
    **Question 2: Package Manager**
    Use the `question` tool with this JSON structure:
    ```json
    {
      "questions": [
        {
          "header": "Пакетный менеджер",
          "question": "Какой пакетный менеджер хотите использовать для установки?",
          "options": [
            {
              "label": "conda",
              "description": "Рекомендуется для изолированных окружений"
            },
            {
              "label": "pip",
              "description": "Универсальный, быстрый"
            },
            {
              "label": "uv",
              "description": "Новый быстрый менеджер, совместим с pip"
            }
          ],
          "multiple": false
        }
      ]
    }
    ```
    
    **Question 3: GPU Support** (if GPU detected or not specified)
    Use the `question` tool with this JSON structure:
    ```json
    {
      "questions": [
        {
          "header": "Поддержка GPU",
          "question": "Какую поддержку GPU хотите настроить?",
          "options": [
            {
              "label": "Автоматически",
              "description": "Определить и настроить доступный GPU"
            },
            {
              "label": "CUDA (NVIDIA GPU)",
              "description": "Поддержка NVIDIA CUDA"
            },
            {
              "label": "ROCm (AMD GPU)",
              "description": "Поддержка AMD ROCm"
            },
            {
              "label": "CPU только",
              "description": "Без поддержки GPU"
            }
          ],
          "multiple": false
        }
      ]
    }
    ```
    
    **Question 4: Development Tools** (optional)
    Use the `question` tool with this JSON structure:
    ```json
    {
      "questions": [
        {
          "header": "Инструменты разработки",
          "question": "Нужны ли дополнительные инструменты разработки?",
          "options": [
            {
              "label": "Полный набор",
              "description": "pytest, black, mypy, pre-commit, coverage"
            },
            {
              "label": "Базовый набор",
              "description": "pytest, black"
            },
            {
              "label": "Только необходимые",
              "description": "pytest"
            },
            {
              "label": "Без инструментов",
              "description": "Инструменты разработки не нужны"
            }
          ],
          "multiple": false
        }
      ]
    }
    ```
    
    **IMPORTANT**: Wait for user to respond with ALL question answers before proceeding. Use the answers to guide configuration file updates in step 4.

4. **Update configuration files**:

    Based on the analysis and user's answers from step 3, update or create the following files:

    **a) `.ml-spec/config/requirements-pip.txt`** (if pip or uv selected):
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

    **b) `.ml-spec/config/environment.yml`** (if conda selected):
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

    **c) `.ml-spec/config/requirements-uv.txt`** (if uv selected):
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

    **d) `.ml-spec/config.yaml`**:
    ```yaml
    project:
      name: "{{PROJECT_NAME}}"
      type: "ml"
      language: "ru"
    
    environment:
      python_version: "3.11"
      cuda_version: "{{CUDA_VERSION}}"  # if GPU
      random_seed: 42
      package_manager: "{{USER_SELECTED_MANAGER}}"  # conda, pip, or uv
    
    training:
      train_val_test_split: [0.7, 0.15, 0.15]
      batch_size: 32
      epochs: 100
    
    tracking:
      experiment_tracker: "mlflow"
      model_registry: "mlflow"
      data_versioning: "dvc"
    ```

    **Note**: Use user's answers from step 3 to customize:
    - Package selection based on ML task type
    - GPU support version (CUDA/ROCm/CPU)
    - Development tools based on user preference
    - Package manager specific file updates

5. **Version compatibility checks**:
    - If CUDA 11.8 detected → Use PyTorch 2.0.1+cu118
    - If CUDA 12.1 detected → Use PyTorch 2.1.0+cu121
    - If ROCm detected → Use PyTorch with ROCm support
    - If CPU only → Use CPU-only PyTorch
    - Adjust versions based on user's selected package manager

6. **Generate configuration summary**:
    Create a summary of changes made:
    - Which files were created/updated
    - Key dependencies added
    - Version constraints applied
    - User preferences applied (environment type, package manager, GPU, dev tools)
    - Next steps for user

7. **Ask for installation preference using `question` tool**:

    After updating configuration files, use the `question` tool to present user with choices:

    **Question 5: Installation Method**
    Use the `question` tool with this JSON structure:
    ```json
    {
      "questions": [
        {
          "header": "Установка окружения",
          "question": "Конфигурационные файлы обновлены. Как хотите установить окружение?",
          "options": [
            {
              "label": "🤖 Автоматически",
              "description": "AI выполнит установку за вас (make setup)"
            },
            {
              "label": "👤 Вручную",
              "description": "Показать команды для самостоятельной установки"
            },
            {
              "label": "👀 Предпросмотр",
              "description": "Показать подготовленный стек пакетов"
            }
          ],
          "multiple": false
        }
      ]
    }
    ```

    Wait for user response before proceeding with installation (if option A selected).

8. **Handle installation based on user's choice**:

    **If Option A (Automatic):**
    - Run `make setup` or `bash .ml-spec/scripts/setup-env.sh`
    - Monitor output for errors
    - Report progress to user using formatted messages:
      - "✅ Environment setup started..."
      - "📦 Installing packages..."
      - "🔧 Configuring tools..."
      - "✅ Setup complete!"
    - If errors occur, show troubleshooting steps in Russian

    **If Option B (Manual):**
    - Provide step-by-step instructions in Russian:
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

    **If Option C (Preview):**
    - Show prepared configuration without installing in Russian:
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
      
      💡 Для установки выберите опцию A или B
      ```

## Interactive Workflow Example

**User:** `/speckit.setup-ml Мне нужно окружение для Computer Vision с PyTorch`

**AI (Step 3):** Asks questions using `question` tool:
```
[Question 1] Тип окружения
Хотите создать новое окружение или использовать текущее?

[Новое изолированное окружение] - Рекомендуется для чистого старта проекта
[Использовать текущее окружение] - Быстрее, но могут быть конфликты версий
```
User selects: "Новое изолированное окружение"

```
[Question 2] Пакетный менеджер
Какой пакетный менеджер хотите использовать для установки?

[conda] - Рекомендуется для изолированных окружений
[pip] - Универсальный, быстрый
[uv] - Новый быстрый менеджер, совместим с pip
```
User selects: "conda"

```
[Question 3] Поддержка GPU
Какую поддержку GPU хотите настроить?

[Автоматически] - Определить и настроить доступный GPU
[CUDA (NVIDIA GPU)] - Поддержка NVIDIA CUDA
[ROCm (AMD GPU)] - Поддержка AMD ROCm
[CPU только] - Без поддержки GPU
```
User selects: "Автоматически"

**AI (Step 4):** Updates configuration files based on user's choices

**AI (Step 7):** Asks final question:
```
[Question 5] Установка окружения
Конфигурационные файлы обновлены. Как хотите установить окружение?

[🤖 Автоматически] - AI выполнит установку за вас (make setup)
[👤 Вручную] - Показать команды для самостоятельной установки
[👀 Предпросмотр] - Показать подготовленный стек пакетов
```
User selects: "🤖 Автоматически"

**AI (Step 8):** Runs automatic installation and reports progress

## Environment Configuration Examples

**Example 1: Computer Vision with PyTorch**
```
/speckit.setup-ml Мне нужно окружение для Computer Vision с PyTorch и Albumentations
```
AI asks using `question` tool:
- Question 1: New or existing environment?
- Question 2: Package manager preference?
- Question 3: GPU support?

User answers questions → AI configures environment based on preferences

Result:
- torch, torchvision, albumentations
- opencv-python, pillow
- GPU support based on user choice

**Example 2: NLP with Transformers**
```
/speckit.setup-ml Нужно окружение для NLP с трансформерами
```
AI asks using `question` tool:
- Question 1: New or existing environment?
- Question 2: Package manager preference?

User answers questions → AI configures environment based on preferences

Result:
- transformers, datasets, tokenizers
- torch or tensorflow
- huggingface-hub

**Example 3: Tabular Data with scikit-learn**
```
/speckit.setup-ml Табличные данные, scikit-learn, XGBoost, LightGBM
```
AI asks using `question` tool:
- Question 1: New or existing environment?
- Question 2: Package manager preference?

User answers questions → AI configures environment based on preferences

Result:
- scikit-learn, xgboost, lightgbm
- pandas, numpy
- optuna for hyperparameter tuning

**Example 4: Full MLOps stack**
```
/speckit.setup-ml Полный MLOps стек с MLflow, DVC, Kubeflow
```
AI asks using `question` tool:
- Question 1: New or existing environment?
- Question 2: Package manager preference?
- Question 4: Development tools needed?

User answers questions → AI configures environment based on preferences

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
5. Respect user's preference for new vs existing environment

## Error Handling

If configuration fails:
1. Show clear error message in Russian
2. Suggest manual configuration
3. Provide example configurations
4. Link to troubleshooting guide

If `question` tool is not available or fails:
1. Fall back to text-based questions
2. Present options as numbered list in this format:
   ```
   ## Вопрос 1: Тип окружения
   
   Хотите создать новое окружение или использовать текущее?
   
   [1] Новое изолированное окружение (рекомендуется для чистого старта)
   [2] Использовать текущее окружение (быстрее, но могут быть конфликты версий)
   
   Ваш ответ: _
   ```
3. Wait for user to respond with option number (1, 2, 3, etc.)
4. Continue with remaining questions sequentially

## Notes

- This command only UPDATES configuration files
- Physical installation happens in `make setup`
- MUST use `question` tool to collect user preferences before updating files
- Idempotent: can be run multiple times safely
- Supports conda, pip, and uv package managers
- All questions and responses must be in Russian
