# Evidence and Source Policy

## Authoritative evidence

The stored standard, product context, and review text are the complete evidence for each score. The contract does not fetch product listings or verify reviewer purchases.

## Collection and provenance

Deployers and callers must collect text lawfully, verify provenance when it matters, and remove secrets or unnecessary personal data. On-chain storage proves which text was evaluated, not who authored it or whether it is true.

## Source selection and freshness

The contract performs no web request, search, browsing, API lookup, or hidden source selection. It makes no live-data or freshness claim. When facts or policies change, use the contract's documented update path or deploy a new appropriate instance.

## Prompt-injection and output controls

Caller text is untrusted data. It is canonicalized into a delimited payload; the prompt forbids treating embedded text as instructions. Only the documented strict JSON shape and closed values can pass normalization and validator replay.

## Production boundary

It does not verify purchases, identities, product facts, defamation claims, or the truth of a review. Higher-stakes applications need independent provenance, identity, privacy, appeal, and human-review processes proportionate to risk.
