import brownie

from utils.config import AGENT


def test_deploy_events(deployer, owner):
    tx = brownie.InsuranceFund.deploy(owner.address, {"from": deployer}).tx
    assert "OwnershipTransferred" in tx.events
    assert (
        len(tx.events["OwnershipTransferred"]) == 2
    ), "there should be 2 ownership transfers"
    assert tx.events["OwnershipTransferred"][0]["previousOwner"] == brownie.ZERO_ADDRESS
    assert tx.events["OwnershipTransferred"][0]["newOwner"] == deployer.address
    assert tx.events["OwnershipTransferred"][1]["previousOwner"] == deployer.address
    assert tx.events["OwnershipTransferred"][1]["newOwner"] == owner.address


def test_deploy_with_zero_address(owner):
    with brownie.reverts("ZERO ADDRESS"):
        brownie.InsuranceFund.deploy(brownie.ZERO_ADDRESS, {"from": owner})


def test_deploy_with_agent_address(owner, chain):
    instance = brownie.InsuranceFund.deploy(AGENT[chain.id], {"from": owner})
    assert instance.owner() == AGENT[chain.id], "contract's owner must be AGENT"
    assert instance.owner() != owner, "contract's owner must be AGENT"
