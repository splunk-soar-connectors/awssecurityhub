**Unreleased**

* Stabilize scheduled polling windows and migrate invalid legacy checkpoints to a safe UTC lookback.
* Reject provider pages that exceed the requested local finding allowance before accumulation.
* Persist per-message SQS progress so capped polls resume at the unprocessed finding and delete only fully ingested messages.
