**Unreleased**

* Stabilize scheduled polling windows and migrate invalid legacy checkpoints to a safe UTC lookback.
* Reject provider pages that exceed the requested local finding allowance before accumulation.
* Limit omitted-result pagination to 1,000 findings and exact-ID validation to 100 retained findings.
* Persist per-message SQS progress so capped polls resume at the unprocessed finding and delete only fully ingested messages.
