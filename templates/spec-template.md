# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

  <!--
    ACTION REQUIRED: Define measurable success criteria.
    These must be technology-agnostic and measurable.
  -->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

---

<!-- OPTIONAL ML SECTIONS: Include these sections if feature is an ML/Data Science project -->

## ML Scenarios & Use Cases *(ML projects only)*

  <!--
    ACTION REQUIRED: The content in this section represents placeholders.
    Fill them out with right ML scenarios.
  -->

### ML Task Type

- **Task Category**: [Classification/Regression/Clustering/Time Series Forecasting/Anomaly Detection/Recommendation System/Other]
- **Problem Domain**: [e.g., image classification, tabular data, text processing]
- **Business Impact**: [How this ML task solves a business problem]

### ML User Scenarios

1. **Scenario 1**: [Describe how users interact with the ML model]
   - Input: [What data users provide]
   - Output: [What predictions/insights users receive]
   - Value: [What business value this provides]

2. **Scenario 2**: [Describe another use case]
   - Input: [What data users provide]
   - Output: [What predictions/insights users receive]
   - Value: [What business value this provides]

---

## ML Requirements *(ML projects only)*

  <!--
    ACTION REQUIRED: The content in this section represents placeholders.
    Fill them out with right ML requirements.
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
  - Missing Values: [How to handle - deletion / imputation / ML-based]
  - Outliers: [Detection and handling strategy]
  - Data Leakage Prevention: [Strategies to prevent leakage]

### Validation Strategy (Стратегия валидации)

- **Train/Val/Test Split**: [e.g., 70/15/15 or custom]
- **Cross-Validation**: [Required? If yes, k-fold, stratified?]
- **Stratification**: [Required? For imbalanced classes?]
- **Random Seed**: [e.g., 42 for reproducibility]

### Security & Privacy (Безопасность и конфиденциальность)

- **Personal Data**: [Does data contain PII? GDPR/CCPA compliance?]
- **Anonymization**: [Required? Hashing, masking, aggregation?]
- **Access Control**: [Who has access to data and models?]
- **Data Encryption**: [Requirements for data at rest/in transit]

### Version Control & Reproducibility (Управление версиями)

- **Model Versioning**: [MLflow / DVC / git-based / other]
- **Experiment Tracking**: [MLflow / Weights & Biases / TensorBoard / custom]
- **Data Versioning**: [DVC / git-lfs / S3 versioning / required?]
- **Rollback Strategy**: [How to handle model failures in production]

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
  - Input Features: [Feature types, dimensions]
  - Output Format: [Predictions, probabilities, embeddings]

### Training Infrastructure

- **Framework**: [PyTorch / TensorFlow / scikit-learn / other]
- **Training Requirements**: [GPU/CPU, estimated training time, hyperparameter optimization]
- **Serving Requirements**: [REST API / batch inference / edge deployment]

---

## ML Data Specification *(ML projects only)*

  <!--
    ACTION REQUIRED: The content in this section represents placeholders.
    Fill them out with right data specs.
  -->

### Data Overview

- **Source**: [Where data comes from - database, API, files]
- **Format**: [CSV, JSON, Parquet, images, text, etc.]
- **Size**: [Number of rows/samples, storage requirements]
- **Update Frequency**: [Real-time, daily, weekly, static]

### Data Schema

| Field | Type | Description | Constraints |
|--------|------|-------------|-------------|
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

<!-- END OPTIONAL ML SECTIONS -->
