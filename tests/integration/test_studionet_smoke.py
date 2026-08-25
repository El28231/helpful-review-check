from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

STANDARD = "A helpful review is relevant, describes specific use conditions, reports concrete strengths or weaknesses, and gives evidence useful to another buyer."

@pytest.mark.integration
def test_studionet_review_reputation(default_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "helpful_review_check.py")
    deployed = factory.deploy_contract_tx(args=[STANDARD], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=default_account)
    submitted = contract.submit_review(args=["r-1", "A commuter helmet used daily in humid weather for one month.", "The vents worked well below 30C, but the rear dial loosened twice during rough rides."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(submitted)
    evaluated = contract.evaluate_review(args=["r-1"]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(evaluated)
    review = contract.get_review(args=["r-1"]).call()
    assert 0 <= review["score"] <= 3
    print(f"STUDIONET_ADDRESS={address}")
    print(f"STUDIONET_DEPLOY_TX={deployed['hash']}")
    print(f"STUDIONET_WRITE_TX={evaluated['hash']}")
    print(f"STUDIONET_RESULT={review['status']}")

