# Helpful Review Check

Maintains a multi-review quality registry and accumulates transparent helpful-review totals for each reviewer address.

## Core workflow

- The owner stores a project-specific review standard.
- Callers submit uniquely identified product reviews with product context.
- Validators return a relevance flag and helpfulness score from 0 to 3.
- The contract stores the result and updates the author's reviewed and helpful totals.

## Reuse model

One deployment can hold up to 500 reviews under the same standard. Reviewer reputation accumulates within that registry.

## Why GenLayer

Specificity, relevance, and decision usefulness are semantic properties of natural-language reviews. GenLayer makes the scoring shared and replayable while deterministic code maintains the reputation totals.

## Evidence and source boundary

The stored standard, product context, and review text are the complete evidence for each score. The contract does not fetch product listings or verify reviewer purchases.

## Safety boundary

It does not verify purchases, identities, product facts, defamation claims, or the truth of a review. The contract holds no funds, has no upgrade hook, and never treats a model result as real-world certification.

## Verify locally

```text
python -m pip install -r requirements.txt
genvm-lint check contracts/helpful_review_check.py
genvm-lint typecheck contracts/helpful_review_check.py
pytest tests/direct -q
python tests/run_glsim.py --no-browser --seed 210821
gltest tests/integration/test_glsim_consensus.py -q --network localnet
```

Run the last two commands in separate terminals. Live StudioNet testing is opt-in and uses dedicated owner-specific keys outside this repository:

```text
gltest tests/integration/test_studionet_smoke.py -q -s --network studionet
```

Never commit a populated .env file, private key, keystore, or wallet password.

## Repository map

- contracts: deployable Intelligent Contract
- tests/direct: hardened state, authorization, malformed-output, and validator tests
- tests/integration: five-validator GLSim and live StudioNet flows
- deployments: public deployment and transaction evidence only
- SOURCE_POLICY.md: evidence authority and collection limits
- AUDIT.md: review-readiness checks and residual limitations
