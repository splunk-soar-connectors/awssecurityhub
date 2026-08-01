**Unreleased**

* Stabilize scheduled polling windows and migrate invalid legacy checkpoints to a safe UTC lookback.
* Preserve older valid checkpoints during migration so unprocessed findings remain in the polling window.
* Reject provider pages that exceed the requested local finding allowance before accumulation.
* Limit omitted-result pagination to 1,000 findings and exact-ID validation to 100 retained findings.
* Persist per-message SQS progress so capped polls resume at the unprocessed finding.
* Track SQS ingestion by exact message occurrence and delete only fully ingested messages.
* Rotate capped SQS retries past persistent failures and report deferred or invalid messages.
* Continue direct polling after individual ingestion failures without checkpointing past the earliest failure.
