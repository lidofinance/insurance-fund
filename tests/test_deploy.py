import brownie

def test_deploy_with_zero_address(owner):
    with brownie.reverts("ZERO ADDRESS"):
        brownie.InsuranceFund.deploy(brownie.ZERO_ADDRESS, {"from": owner})
