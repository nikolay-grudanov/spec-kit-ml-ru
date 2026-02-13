---
description: Decompose an ML technical plan into actionable implementation tasks.
handoffs:
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

The text the user typed after `/speckit.tasks-ml` in the triggering message **is** optional additional context or task filtering preferences. Assume the ML technical plan from `IMPL_PLAN` is the primary source of truth.

Given the ML implementation plan (from `IMPL_PLAN`), decompose it into actionable tasks:

1. **Load and analyze the ML implementation plan**:
   - Read `IMPL_PLAN` (plan.md) completely
   - Identify all implementation phases
   - Extract technical tasks from each phase
   - Note dependencies between tasks
   - Note ML-specific requirements (data pipeline, model training, evaluation, deployment, MLOps)

2. **Decompose the plan into task groups**:

   Create these task groups based on the plan phases:

   ## Group 1: Data Preparation & EDA
   - Data collection and ingestion tasks
   - Exploratory data analysis (EDA) tasks
   - Data cleaning and validation tasks
   - Feature engineering tasks
   - Data splitting tasks
   - Data versioning tasks

   ## Group 2: Model Development
   - Baseline model implementation tasks
   - Model architecture design tasks
   - Training loop implementation tasks
   - Hyperparameter optimization tasks
   - Experiment tracking setup tasks

   ## Group 3: Model Evaluation & Optimization
   - Validation tasks
   - Performance evaluation tasks
   - Model optimization tasks
   - Error analysis and debugging tasks

   ## Group 4: Deployment Preparation
   - Model serialization and versioning tasks
   - Serving infrastructure tasks
   - API/inference pipeline tasks
   - Monitoring setup tasks

   ## Group 5: Testing & Production Rollout
   - Integration testing tasks
   - Performance testing tasks
   - A/B testing tasks (if applicable)
   - Production deployment tasks
   - Monitoring and observability tasks

3. **Format each task with**:
   - **Task ID**: Unique identifier (e.g., DATA-001, MODEL-005, DEPLOY-010)
   - **Title**: Concise description of the task
   - **Description**: Detailed explanation of what the task involves
   - **Priority**: Critical (P0), High (P1), Medium (P2), Low (P3)
   - **Dependencies**: Other tasks that must be completed first
   - **Estimated Effort**: Time estimate (hours or days)
   - **Acceptance Criteria**: Specific conditions for task completion
   - **Definition of Done**: Clear testable completion criteria

4. **Write the task breakdown** to `TASKS_FILE` using a structured format with task IDs, priorities, dependencies, and clear deliverables.

5. **Task Dependency Management**:
   - Ensure dependencies are correctly identified
   - Identify critical path tasks (blocking tasks with no slack)
   - Suggest parallelization opportunities (tasks that can be done simultaneously)

6. **Task Quality Validation**: Ensure each task is:
   - Actionable and specific (not vague)
   - Testable with clear acceptance criteria
   - Properly estimated with realistic time
   - Aligned with the plan's technical approach

7. Report completion with the task file path and readiness for implementation (`/speckit.implement`).

**NOTE**: Tasks should be detailed enough for implementation but should not include code-level specifics. Focus on deliverables and acceptance criteria.

## General Guidelines

### ML Task Prioritization Guidelines

**Critical (P0) Tasks**:
- Block all other work
- Must be completed first
- Examples: Data pipeline setup, ML framework installation, infrastructure provisioning

**High (P1) Tasks**:
- Important for project success
- Should be completed early
- Examples: Feature engineering, baseline model implementation, evaluation setup

**Medium (P2) Tasks**:
- Important but not blocking
- Can be done in parallel with other tasks
- Examples: Hyperparameter tuning, model optimization, monitoring setup

**Low (P3) Tasks**:
- Nice to have but not critical
- Can be deferred if time-constrained
- Examples: Documentation improvements, code cleanup, additional analysis

### ML Task Estimation Guidelines

**Data Tasks**:
- EDA: 1-3 days for small datasets, 3-5 days for complex
- Feature engineering: 2-5 days depending on complexity
- Data cleaning: 1-2 days

**Model Development Tasks**:
- Baseline model: 1-2 days
- Model architecture design: 1-3 days
- Training loop: 2-5 days
- Hyperparameter optimization: 2-4 days

**Evaluation Tasks**:
- Validation: 1-2 days
- Performance evaluation: 1 day
- Error analysis: 1-2 days

**Deployment Tasks**:
- Model versioning: 0.5 day
- API development: 2-4 days
- Monitoring setup: 1-2 days

### ML Task Dependencies Examples

**Common Dependencies**:
- Model development depends on: Data pipeline completion
- Evaluation depends on: Model training completion
- Deployment depends on: Model versioning and validation
- Hyperparameter tuning depends on: Baseline model

**Parallelization Opportunities**:
- Feature engineering for different features can be parallel
- Data quality checks can run in parallel with EDA
- Model architecture design can be done alongside data tasks
- Monitoring setup can be done alongside API development

### Definition of Done for ML Tasks

Each ML task is "done" when:

1. **Data Tasks**:
   - Code is written and tested
   - Data is validated and documented
   - Features are extracted and saved
   - Versioning commit is made

2. **Model Development Tasks**:
   - Model is trained and saved
   - Training metrics are logged
   - Model achieves baseline performance
   - Code is reviewed (if required)

3. **Evaluation Tasks**:
   - Test set evaluation is complete
   - Metrics are calculated and documented
   - Comparison with baseline is done
   - Results are saved and versioned

4. **Deployment Tasks**:
   - Model is versioned and accessible
   - API is deployed and tested
   - Monitoring is configured and receiving data
   - Rollback strategy is tested

5. **MLOps Tasks**:
   - Experiment tracking is set up
   - CI/CD pipeline is working
   - Version control is properly configured

### Risk-Based Task Prioritization

**Data Quality Risks**:
- Prioritize data validation and cleaning tasks
- Add buffer time for unexpected data issues

**Performance Risks**:
- Prioritize evaluation and optimization tasks early
- Allow time for iterative improvements

**Infrastructure Risks**:
- Prioritize setup and configuration tasks first
- Address scaling and reliability tasks

**Reproducibility Risks**:
- Prioritize experiment tracking and versioning tasks
- Ensure random seed control from the start

### Task Grouping Best Practices

**Granular Tasks**:
- Break down large tasks into smaller subtasks (1-2 days each)
- Makes progress visible and manageable
- Enables parallelization

**Deliverable-Focused Tasks**:
- Each task should produce a clear deliverable
- Examples: "Cleaned dataset", "Trained model v1", "Deployed API"
- Avoid vague tasks like "Work on model"

**Testable Tasks**:
- Every task must have clear acceptance criteria
- Include how to test the deliverable
- Examples: "Tested on validation set with accuracy > 0.8", "API responds in < 200ms"

### Common ML Task Checklist

**Data Tasks**:
- [ ] Data sources identified and accessible
- [ ] Data quality issues documented
- [ ] Features engineered and validated
- [ ] Train/val/test split created
- [ ] Data versioning set up

**Model Tasks**:
- [ ] Baseline model implemented
- [ ] Training pipeline functional
- [ ] Hyperparameters optimized
- [ ] Model evaluated on test set
- [ ] Performance metrics meet requirements

**MLOps Tasks**:
- [ ] Experiment tracking configured (MLflow, etc.)
- [ ] Model versioning implemented
- [ ] CI/CD pipeline working
- [ ] Monitoring and logging set up

**Deployment Tasks**:
- [ ] Model serialized and versioned
- [ ] Serving infrastructure deployed
- [ ] API tested and documented
- [ ] Monitoring dashboards active
- [ ] Rollback strategy tested

### Success Criteria for Task Breakdown

A good ML task breakdown should:

1. **Be comprehensive**: Cover all aspects of the plan (data, model, evaluation, deployment, MLOps)
2. **Be actionable**: Each task is specific, testable, and has clear deliverables
3. **Have clear priorities**: Critical/High/Medium/Low with dependencies identified
4. **Include realistic estimates**: Time estimates based on task complexity and dependencies
5. **Support parallelization**: Identify tasks that can be done simultaneously
6. **Include MLOps**: Experiment tracking, versioning, monitoring, CI/CD as first-class tasks
7. **Have clear DoD**: Each task has testable acceptance criteria
