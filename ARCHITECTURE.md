# Architecture

## Responsibility boundary

The application may collect inputs and display state. HelpfulReviewCheck owns the bounded on-chain record, authorization rules, semantic consensus call, and consequential state transition. There is no hidden backend or autonomous source collector.

## State machine

Each review moves once from PENDING to HELPFUL or NOT_HELPFUL; reviewer counters update atomically.

## Storage model

The contract stores review standard, per-review context/text/author/status/score, review IDs, and per-author reviewed/helpful totals. Text is normalized and field-length-bounded before storage.

## Consensus boundary

The leader serializes only stored case data into canonical JSON and requests an exact JSON schema. Validators independently run the same prompt and normalization path. A validator accepts only an allowed, structurally valid value that exactly matches its own result. Exceptions and malformed output fail closed.

## Authorization and invariants

Anyone may submit a unique review ID or trigger evaluation. A pending review can be evaluated once and cannot be overwritten.

## Reuse and distinctness

One deployment can hold up to 500 reviews under the same standard. Reviewer reputation accumulates within that registry.

This is a many-record reputation ledger with deterministic aggregate counters, not a single review classifier or product-identity check.
