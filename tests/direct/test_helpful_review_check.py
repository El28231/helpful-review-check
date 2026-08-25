from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "helpful_review_check.py"
SDK = "v0.2.16"
PROMPT = "independently score how useful"
STANDARD = "A helpful review is relevant, describes specific use conditions, reports concrete strengths or weaknesses, and gives evidence useful to another buyer."


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), STANDARD, sdk_version=SDK)


def test_reviews_build_reviewer_reputation(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    contract.submit_review("r-1", "A commuter helmet used daily in humid weather for one month.", "The vents worked well below 30C, but the rear dial loosened twice during rough rides.")
    direct_vm.mock_llm(PROMPT, json.dumps({"helpfulness": 3, "relevant": True}))
    contract.evaluate_review("r-1")
    assert contract.get_review("r-1")["status"] == "HELPFUL"
    assert contract.get_reputation("0x" + direct_bob.hex()) == {"reviewed": 1, "helpful": 1}
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_duplicate_review_and_bad_score_fail_closed(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.submit_review("same", "A planning application used by a five-person team for two weeks.", "Setup was quick, but recurring tasks lost their labels after import from CSV.")
    with direct_vm.expect_revert("review_id_exists"):
        contract.submit_review("same", "Another context long enough to be otherwise valid for this registry.", "Another review long enough to be otherwise valid and useful to a buyer.")
    direct_vm.mock_llm(PROMPT, json.dumps({"helpfulness": 4, "relevant": True}))
    with direct_vm.expect_revert("invalid_score"):
        contract.evaluate_review("same")
    assert contract.get_review("same")["status"] == "PENDING"

