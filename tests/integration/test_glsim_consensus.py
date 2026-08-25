from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "independently score how useful"
STANDARD = "A helpful review is relevant, describes specific use conditions, reports concrete strengths or weaknesses, and gives evidence useful to another buyer."

def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"helpfulness": 3, "relevant": True})}})
    return {"validators": [v.to_dict() for v in validators]}

def test_five_validator_review_reputation():
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "helpful_review_check.py")
    deployed = factory.deploy_contract_tx(args=[STANDARD], wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    contract = factory.build_contract(extract_contract_address(deployed))
    submitted = contract.submit_review(args=["r-1", "A commuter helmet used daily in humid weather for one month.", "The vents worked well below 30C, but the rear dial loosened twice during rough rides."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(submitted)
    evaluated = contract.evaluate_review(args=["r-1"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(evaluated)
    assert contract.get_review(args=["r-1"]).call()["status"] == "HELPFUL"

