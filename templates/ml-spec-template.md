# ML Specification Template (ML Spec-Template)

**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"

---

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: ML user stories should be PRIORITIZED as ML journeys ordered by importance.
  Each ML story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Model) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each ML story, where P1 is most critical.
  Think of each ML story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this ML user journey in plain language]

**Why this priority**: [Explain the ML value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific ML action] and delivers [specific ML value]"]

**Acceptance Scenarios**:

1. **Given** [initial ML state], **When** [ML action], **Then** [expected ML outcome]
2. **Given** [initial ML state], **When** [ML action], **Then** [expected ML outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this ML user journey in plain language]

**Why this priority**: [Explain the ML value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific ML action] and delivers [specific ML value]"]

**Acceptance Scenarios**:

1. **Given** [initial ML state], **When** [ML action], **Then** [expected ML outcome]
2. **Given** [initial ML state], **When** [ML action], **Then** [expected ML outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this ML user journey in plain language]

**Why this priority**: [Explain the ML value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific ML action] and delivers [specific ML value]"]

**Acceptance Scenarios**:

1. **Given** [initial ML state], **When** [ML action], **Then** [expected ML outcome]
2. **Given** [initial ML state], **When** [ML action], **Then** [expected ML outcome]

---

[Add more ML user stories as needed, each with an assigned priority]

---

## ML Scenarios & Use Cases *(ML projects only)*

### ML Task Type

- **Task Category**: [Classification/Regression/Clustering/Time Series Forecasting/Anomaly Detection/Recommendation System/Other]
- **Problem Domain**: [e.g., image classification, tabular data, text processing]
- **Business Impact**: [How this ML task solves a business problem]

### ML User Scenarios

1. **Scenario 1**: [Describe how users interact with ML model]
   - **Input**: [What data users provide]
   - **Output**: [What predictions/insights users receive]
   - **Value**: [What business value this provides]

2. **Scenario 2**: [Describe another ML use case]
   - **Input**: [What data users provide]
   - **Output**: [What predictions/insights users receive]
   - **Value**: [What business value this provides]

---

## ML Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with right ML functional requirements.
-->

### Performance Metrics (Метрики производительности)

- **Primary Metric**: [accuracy / F1-score / precision / recall / MAE / RMSE / ROC-AUC / custom metric]
- **Secondary Metrics**: [Additional metrics for monitoring]
- **Minimum Threshold**: [Acceptable threshold for production]
- **Business Metrics**: [How ML metrics relate to business KPIs]

### Data Requirements (Требования к данным)

- **Data Schema**: [Expected structure, types, constraints]
- **Data Volume**: [Size of dataset, number of samples]
- **Data Quality Requirements**:
  - **Missing Values**: [How to handle - deletion / mean imputation / ML-based imputation]
  - **Outliers**: [Detection and handling strategy]
  - **Data Leakage Prevention**: [Strategies to prevent leakage]

### Validation Strategy (Стратегия валидации)

- **Train/Val/Test Split**: [e.g., 70/15/15 or custom]
- **Cross-Validation**: [Required? If yes, k-fold, stratified?]
- **Stratification**: [Required? For imbalanced classes?]
- **Random Seed**: [e.g., 42 for reproducibility]

### Security & Privacy (Безопасность и конфиденциальность)

- **Personal Data**: [Does data contain PII? GDPR/CCPA compliance?]
- **Anonymization**: [Required? Hashing, masking, aggregation, differential privacy?]
- **Access Control**: [Who has access to data and models?]
- **Data Encryption**: [Requirements for data at rest/in transit]

### Version Control & Reproducibility (Управление версиями)

- **Model Versioning**: [MLflow / DVC / git-based / other]
- **Experiment Tracking**: [MLflow / Weights & Biases / TensorBoard / custom]
- **Rollback Strategy**: [How to handle model failures in production]
- **Data Versioning**: [DVC / git-lfs / S3 versioning / required?]

---

## ML Architecture *(ML projects only)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with right ML architecture details.
-->

### Model Type & Architecture

- **Model Type**: [CNN / LSTM / Random Forest / XGBoost / Transformer / other]
- **Key Components**: [e.g., embedding layer, attention mechanism, ensemble methods]
- **Input/Output**:
  - **Input Features**: [Feature types, dimensions]
  - **Output Format**: [Predictions, probabilities, embeddings]

### Training Infrastructure

- **Framework**: [PyTorch / TensorFlow / scikit-learn / other]
- **Training Requirements**: [GPU/CPU, estimated training time, hyperparameter optimization]
- **Serving Requirements**: [REST API / batch inference / edge deployment]

---

## ML Data Specification *(ML projects only)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with right ML data specification.
-->

### Data Overview

- **Source**: [Where data comes from - database, API, files]
- **Format**: [CSV, JSON, Parquet, images, text, etc.]
- **Size**: [Number of rows/samples, storage requirements]
- **Update Frequency**: [Real-time, daily, weekly, static]

### Data Schema

| Field | Type | Description | Constraints |
|--------|------|-------------|----------|
| [field1] | [type] | [description] | [constraints] |
| [field2] | [type] | [description] | [constraints] |

### Data Quality Checks

- **Validation Rules**: [Schema validation, range checks, required fields]
- **Preprocessing Pipeline**: [Imputation, scaling, encoding, feature engineering]
- **Feature Selection**: [Manual, automatic, importance-based]

### Data Split Strategy

- **Training Set**: [Percentage or number of samples]
- **Validation Set**: [Percentage or number of samples]
- **Test Set**: [Percentage or number of samples]
- **Temporal Split**: [For time series: train before date X, val before date Y]

---

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable ML success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable ML metric, e.g., "Model achieves F1-score >= 0.85"]
- **SC-002**: [Measurable ML metric, e.g., "Model predictions complete in under 100ms"]
- **SC-003**: [Business metric, e.g., "10% accuracy improvement = $100K revenue increase"]
- **SC-004**: [ML system performance, e.g., "Model training completes in under 2 hours"]
