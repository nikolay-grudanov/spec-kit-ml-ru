---
description: Create or update ML feature specification from a natural language description. ML-specific command with ML project type detection.
handoffs:
  - label: Build ML Technical Plan
    agent: speckit.plan-ml
    prompt: Create a technical plan for the ML spec. I am building with...
  - label: Clarify ML Spec Requirements
    agent: speckit.clarify-ml
    prompt: Clarify ML specification requirements
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/speckit.specify-ml` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "train-image-classifier", "predict-sales-forecast")
   - Preserve technical terms and acronyms (CNN, LSTM, API, ML, etc.)
   - Keep it concise but descriptive enough to understand the ML feature at a glance
   - Examples:
     - "I want to create an image classifier for Fashion MNIST" → "image-classification-fashion-mnist"
     - "Implement a sales prediction model" → "sales-prediction-model"
     - "Create a time series forecasting model for stock prices" → "time-series-stock-forecast"

2. **Check for existing branches before creating new one**:

   a. First, fetch all remote branches to ensure we have the latest information:

      ```bash
      git fetch --all --prune
      ```

   b. Find the highest feature number across all sources for the short-name:
      - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`

   c. Determine the next available number:
      - Extract all numbers from all three sources
      - Find the highest number N
      - Use N+1 for the new branch number

   d. Run the script `(Missing script command for sh)` with the calculated number and short-name:
      - Pass `--number N+1` and `--short-name "your-short-name"` along with the feature description
      - Bash example: `(Missing script command for sh) --json --number 5 --short-name "image-classification" "Create image classifier for Fashion MNIST"`
      - PowerShell example: `(Missing script command for sh) -Json -Number 5 -ShortName "image-classification" "Create image classifier for Fashion MNIST"`

   **IMPORTANT**:
   - Check all three sources (remote branches, local branches, specs directories) to find the highest number
   - Only match branches/directories with the exact short-name pattern
   - If no existing branches/directories found with this short-name, start with number 1
   - You must only ever run this script once per feature
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   - The JSON output will contain BRANCH_NAME and SPEC_FILE paths
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot")

3. Load `.specify/templates/spec-template.md` to understand required sections.

4. Follow this ML project execution flow:

     1. Parse user description from Input
        If empty: ERROR "No ML feature description provided"
     2. Extract ML-specific concepts from description:
        - Task type: classification, regression, time series, clustering, anomaly detection, etc.
        - Data: datasets, features, labels, format
        - ML requirements: metrics, validation, training strategy
     3. Fill ML Scenarios & Use Cases section:
        - Task type and problem domain
        - ML user scenarios (input → output → value)
     4. Fill ML Requirements section:
        - Performance Metrics (primary/secondary metrics, thresholds)
        - Data Requirements (schema, volume, quality)
        - Validation Strategy (split, cross-validation, stratification)
        - Security & Privacy (PII, anonymization, access control)
        - Version Control (MLflow/DVC, experiment tracking)
     5. Fill ML Architecture section (if technical details known):
        - Model type, framework, infrastructure
     6. Fill ML Data Specification section (if data details known):
        - Data overview, schema, quality checks
     7. For unclear ML aspects:
        - Make informed guesses based on ML best practices
        - Only mark with [NEEDS CLARIFICATION: specific question] if critical
        - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
        - Prioritize clarifications by impact: metrics > data quality > validation > security > implementation details
     8. Return: SUCCESS (ML spec ready for planning)

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the ML feature description (arguments) while preserving section order and headings.

6. **ML Specification Quality Validation**: After writing the initial spec, validate it against ML-specific quality criteria:

   a. **Create ML Spec Quality Checklist**: Generate a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure with these ML-specific validation items:

      ```markdown
      # ML Specification Quality Checklist: [FEATURE NAME]

      **Purpose**: Validate ML specification completeness and quality before proceeding to planning
      **Created**: [DATE]
      **Feature**: [Link to spec.md]

      ## ML Content Quality

      - [ ] ML task type clearly defined (classification, regression, time series, etc.)
      - [ ] ML metrics specified (primary, secondary, thresholds)
      - [ ] Data requirements complete (schema, volume, quality)
      - [ ] Validation strategy defined (split, cross-validation, stratification)
      - [ ] Security & privacy requirements addressed (PII, anonymization)
      - [ ] Version control requirements specified (MLflow, DVC, experiment tracking)
      - [ ] All ML sections completed

      ## ML Requirement Completeness

      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Performance metrics are testable and unambiguous
      - [ ] Data quality requirements are measurable
      - [ ] Validation strategy is appropriate for ML task type
      - [ ] Success criteria are measurable
      - [ ] Data schema is specified
      - [ ] Security & privacy requirements are clear

      ## ML Feature Readiness

      - [ ] ML scenarios describe user interactions with model
      - [ ] All ML requirements have clear acceptance criteria
      - [ ] Feature meets measurable outcomes defined in ML Success Criteria
      - [ ] No implementation details leak into specification
      - [ ] Model architecture requirements are clear (if specified)

      ## Notes

      - Items marked incomplete require spec updates before `/speckit.plan-ml` or `/speckit.clarify-ml`
      ```

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific ML issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 7

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific ML issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining ML issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by metrics/data/validation/security impact) and make informed ML guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## ML Question [N]: [Topic]

           **Context**: [Quote relevant spec section]

           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]

           **Suggested Answers**:

           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested ML answer] | [What this means for the model] |
           | B      | [Second suggested ML answer] | [What this means for the model] |
           | C      | [Third suggested ML answer] | [What this means for the model] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |

           **Your choice**: _[Wait for user response]_
           ```

        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all ML clarifications are resolved

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, spec file path, checklist results, and readiness for the next phase (`/speckit.plan-ml` or `/speckit.clarify-ml`).

**NOTE:** The script creates and checks out the new branch and initializes the spec file before writing.

## General Guidelines

## Quick ML Project Guidelines

- Focus on **ML problem** (what needs to be predicted/classified) and **WHY** it matters.
- Avoid specific **HOW to implement** (no specific algorithms, model architectures, frameworks in the spec phase).
- Written for business stakeholders and data scientists, not ML engineers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command (`/speckit.clarify-ml`).

### Section Requirements

- **Mandatory ML sections**: ML Scenarios & Use Cases, ML Requirements, Success Criteria
- **Optional ML sections**: ML Architecture, ML Data Specification (include only when relevant)
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this ML spec from a user prompt:

1. **Make informed ML guesses**: Use ML context, industry ML best practices, and common ML patterns to fill gaps
2. **Document ML assumptions**: Record reasonable defaults (e.g., accuracy metric for classification, 70/15/15 split) in Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical ML decisions that:
   - Significantly impact ML model performance or data strategy
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: metrics > data quality > validation > security > architecture details
5. **Think like an ML engineer/data scientist**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common ML areas needing clarification** (only if no reasonable default exists):
   - ML task type and specific problem domain
   - Primary evaluation metric selection
   - Data volume and distribution
   - Validation strategy for imbalanced datasets
   - Security/privacy requirements (GDPR, PII)
   - Model serving requirements (batch vs real-time)

**Examples of reasonable ML defaults** (don't ask about these):
- Evaluation metrics: Accuracy for balanced classification, F1 for imbalanced classification, MAE/RMSE for regression
- Data split: 70/15/15 train/val/test split unless specified otherwise
- Random seed: 42 for reproducibility
- Validation: Cross-validation for small datasets (<10k samples)
- Default handling: Mean imputation for missing values (tabular data)

### ML Success Criteria Guidelines

ML success criteria must be:

1. **Measurable**: Include specific metrics (accuracy, F1, precision, recall, MAE, RMSE, time thresholds)
2. **Technology-agnostic**: No mention of specific frameworks (PyTorch, TensorFlow), libraries (scikit-learn), or algorithms (CNN, LSTM) unless specified by user
3. **User/Business-focused**: Describe outcomes from user/business perspective, not model internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good ML examples**:
- "Model achieves F1-score >= 0.85 on test set"
- "Prediction latency under 100ms for real-time inference"
- "Model supports 10,000 predictions per second"
- "False positive rate < 5%"

**Bad ML examples** (implementation-focused):
- "PyTorch model trains in under 1 hour" (framework-specific, use "Model trains efficiently")
- "CNN with 3 convolutional layers" (too technical, use "Deep learning model")
- "XGBoost with 100 trees" (algorithm-specific, use "Tree-based ensemble")
