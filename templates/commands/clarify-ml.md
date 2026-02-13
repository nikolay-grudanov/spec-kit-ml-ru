---
description: Identify underspecified areas in the current ML feature specification by asking up to 5 highly targeted ML-specific clarification questions and encoding answers back into the spec. Supports ML projects only.
handoffs:
  - label: Build ML Technical Plan
    agent: speckit.plan-ml
    prompt: Create a technical plan for the ML spec. I am building with...
scripts:
   sh: scripts/bash/check-prerequisites.sh --json --paths-only
   ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Goal: Detect and reduce ambiguity or missing decision points in the active ML feature specification and record ML-specific clarifications directly in the spec file.

Note: This ML clarification workflow is expected to run (and be completed) BEFORE invoking `/speckit.plan-ml`. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

Execution steps:

1. Run `{SCRIPT}` from repo root **once** (combined `--json --paths-only` mode / `-Json -PathsOnly`). Parse minimal JSON payload fields:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`
   - (Optionally capture `IMPL_PLAN`, `TASKS` for future chained flows.)
   - If JSON parsing fails, abort and instruct user to re-run `/speckit.specify-ml` or verify feature branch environment.
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. Load the current ML spec file. Perform a structured ML-specific ambiguity & coverage scan using this taxonomy. For each category, mark status: Clear / Partial / Missing. Produce an internal coverage map used for prioritization (do not output raw map unless no questions will be asked).

   **ML Model Scope & Behavior**:
   - ML task type (classification, regression, time series, clustering, anomaly detection, recommendation)
   - Training strategy (supervised, unsupervised, semi-supervised, reinforcement learning)
   - Inference requirements (batch vs real-time, latency targets)
   - Model size constraints (for edge deployment)

   **ML Data Model**:
   - Feature engineering requirements
   - Target variable definition and encoding
   - Data preprocessing pipeline (imputation, scaling, encoding)
   - Feature importance and selection strategy
   - Data augmentation requirements (for images/text)
   - Data volume and distribution assumptions

   **ML Model Training**:
   - Training data volume and distribution
   - Hyperparameter optimization strategy (grid search, random search, Bayesian)
   - Early stopping criteria
   - Regularization techniques (L1/L2, dropout, batch norm)
   - Class imbalance handling (oversampling, undersampling, class weights)

   **ML Model Evaluation**:
   - Validation strategy (train/val/test split, cross-validation, time-based split)
   - Primary evaluation metrics (accuracy, F1, precision, recall, MAE, RMSE, ROC-AUC)
   - Secondary metrics for monitoring
   - Threshold selection for binary classification
   - Calibration requirements
   - Baseline comparison needs

   **ML Production Requirements**:
   - Model serving infrastructure (REST API, batch inference, edge deployment)
   - Model monitoring and drift detection
   - A/B testing strategy
   - Model update and retraining schedule
   - Rollback strategy for model failures

   **ML Security & Privacy**:
   - Data anonymization requirements (GDPR, CCPA)
   - Model privacy concerns (adversarial attacks, model inversion)
   - Data encryption requirements (at rest, in transit)
   - Access control for models and data

   **ML Reproducibility & Versioning**:
   - Random seed requirements
   - MLflow/DVC integration for experiment tracking
   - Model versioning strategy
   - Data versioning requirements
   - Code and dependency versioning

   For each category with Partial or Missing status, add a candidate ML-specific question opportunity unless:
   - Clarification would not materially change ML model architecture, evaluation strategy, or validation approach
   - Information is better deferred to ML planning phase (note internally)
   - The choice significantly impacts ML model performance or data strategy
   - Multiple reasonable interpretations exist with different ML implications
   - No reasonable ML default exists

3. Generate (internally) a prioritized queue of candidate ML clarification questions (maximum 5). Do NOT output them all at once. Apply these constraints:
   - Maximum of 10 total questions across the whole session.
   - Each question must be answerable with EITHER:
      - A short multiple‑choice selection (2–5 distinct, mutually exclusive options), OR
      - A one-word / short‑phrase answer (explicitly constrain: "Answer in <=5 words").
   - Only include ML questions whose answers materially impact ML model architecture, data modeling, evaluation strategy, training approach, deployment, or MLOps validation.
   - Ensure ML category coverage balance: attempt to cover the highest impact unresolved ML areas first; avoid asking two low-impact ML questions when a single high-impact ML area (e.g., evaluation strategy) is unresolved.
   - Exclude ML questions already answered, trivial ML stylistic preferences, or ML plan-level execution details (unless blocking ML correctness).
   - Favor ML clarifications that reduce downstream rework risk or prevent misaligned ML evaluation tests.
   - If more than 5 ML categories remain unresolved, select the top 5 by (Impact * Uncertainty) heuristic.

4. Sequential questioning loop (interactive):
   - Present EXACTLY ONE ML question at a time.
   - For multiple‑choice ML questions:
      - **Analyze all options** and determine the **most suitable option** based on:
         - ML best practices for the specific task type
         - Common patterns in similar ML implementations
         - Risk reduction (performance, overfitting, data quality)
         - Alignment with any explicit ML project goals or constraints visible in the spec
      - Present your **recommended option prominently** at the top with clear reasoning (1-2 sentences explaining why this is the best choice).
      - Format as: `**Recommended:** Option [X] - <reasoning>`
      - Then render all options as a Markdown table:

        | Option | Description |
        |--------|-------------|
        | A | <Option A description> |
        | B | <Option B description> |
        | C | <Option C description> (add D/E as needed up to 5) |
        | Short | Provide a different short answer (<=5 words) (Include only if free-form alternative is appropriate) |

      - After the table, add: `You can reply with the option letter (e.g., "A"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.`

   - For short‑answer ML style (no meaningful discrete options):
      - Provide your **suggested answer** based on ML best practices and context.
      - Format as: `**Suggested:** <your proposed answer> - <brief reasoning>`
      - Then output: `Format: Short answer (<=5 words). You can accept the suggestion by saying "yes" or "suggested", or provide your own answer.`

   - After the user answers:
      - If the user replies with "yes", "recommended", or "suggested", use your previously stated recommendation/suggestion as the answer.
      - Otherwise, validate the answer maps to one option or fits the <=5 word constraint.
      - If ambiguous, ask for a quick disambiguation (count still belongs to the same question; do not advance).
      - Once satisfactory, record it in working memory (do not yet write to disk) and move to the next queued ML question.
   - Stop asking further ML questions when:
      - All critical ML ambiguities resolved early (remaining queued items become unnecessary), OR
      - User signals completion ("done", "good", "no more"), OR
      - You reach 5 asked ML questions.
   - Never reveal future queued ML questions in advance.
   - If no valid ML questions exist at start, immediately report no critical ML ambiguities.

5. Integration after EACH accepted ML answer (incremental update approach):
   - Maintain in-memory representation of the spec (loaded once at start) plus the raw file contents.
   - For the first integrated answer in this session:
      - Ensure a `## Clarifications` section exists (create it just after the highest-level contextual/overview section per the spec template if missing).
      - Under it, create (if not present) a `### Session YYYY-MM-DD` subheading for today.
   - Append a bullet line immediately after acceptance: `- Q: <question> → A: <final answer>`.
   - Then immediately apply the ML clarification to the most appropriate ML section(s):
      - ML task type clarification → Update or add bullet in ML Scenarios & Use Cases
      - ML metrics clarification → Update or add bullet in ML Requirements / Performance Metrics
      - Data quality clarification → Update or add bullet in ML Requirements / Data Requirements
      - Validation strategy clarification → Update or add bullet in ML Requirements / Validation Strategy
      - Security/privacy clarification → Update or add bullet in ML Requirements / Security & Privacy
      - Version control clarification → Update or add bullet in ML Requirements / Version Control
      - Model architecture clarification → Update or add bullet in ML Architecture
      - Data schema/features clarification → Update or add bullet in ML Data Specification
      - ML evaluation ambiguity → Update or add bullet in ML Model Evaluation (if section exists in spec)
      - Production/clarification → Update or add bullet in ML Production Requirements (if section exists in spec)
      - If the clarification invalidates an earlier ambiguous statement, replace that statement instead of duplicating; leave no obsolete contradictory text.
   - Save the spec file AFTER each integration to minimize risk of context loss (atomic overwrite).
   - Preserve formatting: do not reorder unrelated sections; keep heading hierarchy intact.
   - Keep each inserted ML clarification minimal and testable (avoid narrative drift).

6. Validation (performed after EACH write plus final pass):
   - Clarifications session contains exactly one bullet per accepted answer (no duplicates).
   - Total asked (accepted) ML questions ≤ 5.
   - Updated ML sections contain no lingering vague placeholders the new answer was meant to resolve.
   - No contradictory earlier statement remains (scan for now-invalid alternative choices removed).
   - Markdown structure valid; only allowed new headings: `## Clarifications`, `### Session YYYY-MM-DD`.
   - Terminology consistency: same canonical term used across all updated ML sections.

7. Write the updated spec back to `FEATURE_SPEC`.

8. Report completion (after questioning loop ends or early termination):
   - Number of ML questions asked & answered.
   - Path to updated spec.
   - ML sections touched (list names).
   - Coverage summary table listing each ML taxonomy category with Status: Resolved (was Partial/Missing and addressed), Deferred (exceeds question quota or better suited for ML planning), Clear (already sufficient), Outstanding (still Partial/Missing but low impact).
   - If any Outstanding or Deferred remain, recommend whether to proceed to `/speckit.plan-ml` or run `/speckit.clarify-ml` again later post-plan.
   - Suggested next command.

## General Guidelines

### ML Example Reference (For AI Generation)

When clarifying ML specification:

1. **Load appropriate ML example** (BEFORE asking questions):
   - ML project examples are located in `.ml-spec/examples/`
   - Choose ONE example that matches your task type:
     * `image-classification/` - For computer vision tasks (image classification, object detection, segmentation)
     * `tabular-classification/` - For structured data tasks (classification, regression on CSV/database data)
     * `time-series-forecast/` - For time series tasks (forecasting, anomaly detection on sequential data)
   - Load the selected example's spec.md to understand what sections are typically well-specified
   - Use the example as a reference for clarifications that are commonly needed vs already covered
   - Focus your questions on areas where your spec differs from the example or lacks detail

2. **Compare with example**: Identify gaps between your spec and the example's spec

3. **Question prioritization**: Ask questions that would bring your spec closer to the example's completeness level

Behavior rules:

- If no meaningful ML ambiguities found (or all potential ML questions would be low-impact), respond: "No critical ML ambiguities detected worth formal clarification." and suggest proceeding.
- If ML spec file missing, instruct user to run `/speckit.specify-ml` first (do not create a new ML spec here).
- Never exceed 5 total asked ML questions (clarification retries for a single question do not count as new questions).
- Avoid speculative ML tech stack questions unless the absence blocks ML functional clarity.
- Respect user early termination signals ("stop", "done", "proceed").
- If no ML questions asked due to full ML coverage, output a compact ML coverage summary (all categories Clear) then suggest advancing.
- If quota reached with unresolved high-impact ML categories remaining, explicitly flag them under Deferred with rationale.

Context for prioritization: $ARGUMENTS
