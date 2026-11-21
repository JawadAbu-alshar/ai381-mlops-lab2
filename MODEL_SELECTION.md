# Model selection

## The question
The model predicts whether a customer is likely to churn. A false negative may cause the company to lose a customer without offering retention support, while a false positive may spend a retention offer on a customer who would stay.

## Candidates
| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---:|---:|---:|---:|---:|---|
| logreg | Simple, fast baseline for tabular churn data | 0.792 | 0.587 | 0.182 (two-year) | 4.438 | 4 | df434d066e2b4a178610f9b3993eef2c |
| random_forest | Non-linear ensemble model | 0.725 | 0.520 | 0.000 (two-year) | 13.450 | 3427 | cf48c7ba6b2d4993a266dbb2716f569c |
| gradient_boosting | Boosted-tree alternative for complex patterns | 0.731 | 0.531 | 0.182 (two-year) | 3.776 | 141 | f26af6e5845648078cd88b245fd5d917 |

## The champion
I selected logreg. It has the best overall F1 (0.587) and AUC (0.792), the best month-to-month slice F1 (0.643), low p95 latency (4.438 ms), and the smallest model size (4 KB). I accepted its lower one-year slice F1 (0.375 versus 0.400 for the two tree models), because it has much better overall performance and ties gradient_boosting on the weakest two-year slice.

## My promotion rules
- Latency budget (p95): 30 ms, because all valid candidates should respond quickly enough for an API while leaving margin for a slower CI runner.
- Minimum gain to replace the champion (F1 points): 0.010, because a 1-point F1 improvement is meaningful enough to justify replacing a stable production model.

## What I would check next
I would collect more data for the two-year contract slice because its F1 is the weakest. I would also monitor whether customer behavior or churn rates change over time.