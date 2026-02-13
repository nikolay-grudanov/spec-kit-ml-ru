---
description: Create or update ML technical implementation plan from an ML feature specification.
handoffs:
  - label: Decompose into ML Tasks
    agent: speckit.tasks-ml
    prompt: Create a task breakdown for the ML plan. I am building with...
  - label: Build ML Prototype
    agent: speckit.implement
    prompt: Start implementing the ML feature...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/speckit.plan-ml` in the triggering message **is** optional additional context or preferences. Assume the ML specification from `FEATURE_SPEC` is the primary source of truth.

Given the ML specification (from `FEATURE_SPEC`), create a comprehensive technical implementation plan:

1. **Load and analyze the ML specification**:
   - Read `FEATURE_SPEC` (spec.md) completely
   - Identify ML task type (classification, regression, time series, clustering, etc.)
   - Extract ML requirements (metrics, data, validation, security, versioning)
   - Note ML architecture requirements (if specified)
   - Note data specification (if provided)

2. **Determine ML task type and appropriate architecture**:

   **Classification Tasks**:
   - Image classification: CNN, Vision Transformer (ViT), ResNet
   - Tabular classification: Random Forest, XGBoost, LightGBM, Neural Network
   - Text classification: RNN, LSTM, Transformer (BERT, GPT)

   **Regression Tasks**:
   - Tabular regression: Linear Regression, Random Forest, XGBoost, Neural Network
   - Time series: ARIMA, LSTM, Transformer-based models

   **Clustering Tasks**:
   - K-means, DBSCAN, Hierarchical clustering
   - Dimensionality reduction: PCA, t-SNE, UMAP

   **Time Series Forecasting**:
   - ARIMA, Prophet, LSTM, Transformer-based models
   - Seasonality handling
   - Trend and anomaly detection

   **Anomaly Detection**:
   - Isolation Forest, One-Class SVM, Autoencoder

   **Recommendation Systems**:
   - Collaborative filtering, Content-based filtering
   - Matrix factorization, Deep learning approaches

3. **Design the implementation plan structure**:

   Include these sections in the plan:

   ## ML Architecture & Technical Stack
   - Model architecture (type, layers, components)
   - Framework selection (PyTorch, TensorFlow, scikit-learn, etc.)
   - Infrastructure requirements (GPU/CPU, memory, storage)
   - Serving infrastructure (REST API, batch inference, edge deployment)

   ## Data Pipeline & Engineering
   - Data ingestion and loading
   - Feature engineering and preprocessing
   - Data validation and quality checks
   - Feature scaling and encoding
   - Train/val/test split strategy
   - Data augmentation (if applicable)

   ## Model Training Strategy
   - Training data preparation
   - Model architecture design
   - Hyperparameter optimization strategy
   - Training loop design (epochs, batch size, learning rate)
   - Regularization techniques (L1/L2, dropout, batch norm)
   - Early stopping criteria
   - Class imbalance handling (if applicable)

   ## Model Evaluation & Validation
   - Evaluation metrics (primary, secondary, business metrics)
   - Validation strategy (cross-validation, stratification)
   - Test dataset evaluation
   - Threshold selection (for binary classification)
   - Calibration requirements
   - Baseline comparison

   ## Model Deployment & Monitoring
   - Serving infrastructure (API, batch, edge)
   - Model monitoring and drift detection
   - A/B testing strategy
   - Rollback and retraining strategy
   - Performance monitoring (latency, throughput, accuracy)

   ## MLOps & Infrastructure
   - Experiment tracking (MLflow, Weights & Biases, TensorBoard)
   - Model versioning (MLflow, DVC, git-based)
   - Data versioning (DVC, git-lfs, S3)
   - CI/CD pipeline
   - Resource provisioning and scaling

   ## Implementation Phases (5 Phases)
   Break down implementation into these phases:

   ### Phase 1: Data Preparation & EDA (Exploratory Data Analysis)
   - Data collection and validation
   - Exploratory data analysis (EDA)
   - Data cleaning and preprocessing
   - Feature engineering
   - Train/val/test split
   - Estimated time: [e.g., 2-3 days]

   ### Phase 2: Model Development
   - Baseline model implementation
   - Model architecture design
   - Training loop implementation
   - Hyperparameter tuning
   - Estimated time: [e.g., 5-7 days]

   ### Phase 3: Model Evaluation & Optimization
   - Validation on test set
   - Performance evaluation against baseline
   - Model optimization
   - Error analysis
   - Estimated time: [e.g., 2-3 days]

   ### Phase 4: Deployment Preparation
   - Model serialization and versioning
   - Serving infrastructure setup
   - API or inference pipeline development
   - Monitoring setup
   - Estimated time: [e.g., 2-3 days]

   ### Phase 5: Testing & Production Rollout
   - Integration testing
   - Performance testing
   - A/B testing (if applicable)
   - Production deployment
   - Monitoring and observability
   - Estimated time: [e.g., 2-3 days]

4. **Write the implementation plan** to `IMPL_PLAN` using a structured format with clear sections and actionable steps.

5. **Plan Quality Validation**: Ensure the plan is:
   - Technically feasible for the ML task type
   - Aligned with ML requirements from spec
   - Includes MLOps considerations (experiment tracking, versioning, monitoring)
   - Has realistic time estimates for each phase
   - Identifies dependencies and risks

6. Report completion with the plan file path and readiness for task decomposition (`/speckit.tasks-ml`).

**NOTE**: This plan assumes the ML specification is already complete and validated via `/speckit.specify-ml` and `/speckit.clarify-ml`.

## General Guidelines

### ML Task-Specific Considerations

**For Classification**:
- Always specify: number of classes, class imbalance handling, multiclass vs binary
- Consider: baseline accuracy, F1-score vs accuracy tradeoff

**For Regression**:
- Always specify: error metric (MAE, RMSE, R²), feature importance
- Consider: outlier handling, normalization needs

**For Time Series**:
- Always specify: temporal split (not random), seasonality, trend handling
- Consider: lag features, rolling windows, forecast horizon

**For Clustering**:
- Always specify: number of clusters (if known), distance metric
- Consider: cluster interpretation, outlier handling

**For Anomaly Detection**:
- Always specify: anomaly threshold, false positive/negative rates
- Consider: baseline normal behavior, seasonal patterns

**For Recommendation Systems**:
- Always specify: cold-start problem, user-item matrix, evaluation metrics
- Consider: popularity bias, diversity, novelty

### MLOps Best Practices

- **Experiment Tracking**: Always include MLflow or equivalent for reproducibility
- **Data Versioning**: Use DVC or equivalent for dataset tracking
- **Model Versioning**: Version models before deployment with clear version numbers
- **Monitoring**: Set up drift detection and performance monitoring from day 1
- **Rollback**: Have a strategy to rollback to previous model version if issues arise
- **CI/CD**: Automate training, evaluation, and deployment pipelines

### Risk Mitigation

Address these common ML risks in the plan:

- **Data Quality Risk**: Poor data quality can lead to poor model performance
  - Mitigation: Extensive EDA, data validation, quality checks
- **Overfitting Risk**: Model memorizes training data, poor generalization
  - Mitigation: Cross-validation, regularization, early stopping, test set evaluation
- **Concept Drift**: Model performance degrades over time as data distribution changes
  - Mitigation: Monitoring, periodic retraining, drift detection
- **Data Leakage**: Information from test/validation set leaks into training
  - Mitigation: Split data BEFORE preprocessing, strict separation of pipelines
- **Reproducibility Risk**: Results cannot be reproduced
  - Mitigation: Fixed random seeds, experiment tracking, data/model versioning

### Technology Selection Guidance

When the specification doesn't specify technologies, recommend appropriate choices:

**Deep Learning** (images, text, complex patterns):
- Frameworks: PyTorch, TensorFlow
- Models: CNN, Transformer (BERT, GPT, ViT)
- Hardware: GPU (CUDA, ROCm) required for training

**Classical ML** (tabular data, smaller datasets):
- Frameworks: scikit-learn, XGBoost, LightGBM
- Models: Random Forest, Gradient Boosting, SVM
- Hardware: CPU usually sufficient

**Time Series** (forecasting):
- Libraries: Prophet, statsmodels, PyTorch/TensorFlow for deep learning
- Approaches: ARIMA, LSTM, Transformer-based

**Clustering/Unsupervised**:
- Libraries: scikit-learn, PyTorch
- Algorithms: K-means, DBSCAN, Autoencoder
- Evaluation: Silhouette score, Davies-Bouldin index

### Success Criteria for Plans

A good ML implementation plan should:

1. **Be task-appropriate**: Architecture and approach match the ML problem type
2. **Be comprehensive**: Cover data, model, training, evaluation, deployment, MLOps
3. **Be actionable**: Each phase has clear deliverables and time estimates
4. **Include MLOps**: Experiment tracking, versioning, monitoring, CI/CD
5. **Be realistic**: Time estimates and resources match the problem complexity
6. **Address risks**: Identify and mitigate common ML risks (overfitting, data quality, drift)
