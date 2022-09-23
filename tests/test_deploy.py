import brownie

from utils.config import AGENT


def test_deploy_with_zero_address(owner):
    with brownie.reverts("ZERO ADDRESS"):
        brownie.InsuranceFund.deploy(brownie.ZERO_ADDRESS, {"from": owner})


def test_deploy_with_agent_address(owner, chain):
    instance = brownie.InsuranceFund.deploy(AGENT[chain.id], {"from": owner})
    assert instance.owner() == AGENT[chain.id], "contract's owner must be AGENT"
    assert instance.owner() != owner, "contract's owner must be AGENT"
