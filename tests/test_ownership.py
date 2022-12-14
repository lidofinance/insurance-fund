import brownie


def test_initial_owner(insurance_fund, deployer, owner):
    assert insurance_fund.owner() != deployer.address, "deployer should not be owner"
    assert insurance_fund.owner() == owner.address, "owner address should match"


def test_renounce_ownership(insurance_fund, owner, anyone):
    with brownie.reverts("DISABLED"):
        insurance_fund.renounceOwnership({"from": anyone})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"


def test_transfer_ownership_as_owner(insurance_fund, owner, stranger):
    tx = insurance_fund.transferOwnership(stranger.address, {"from": owner})

    assert insurance_fund.owner() == stranger.address, "stranger should now be owner"
    assert "OwnershipTransferred" in tx.events
    assert tx.events["OwnershipTransferred"]["previousOwner"] == owner.address
    assert tx.events["OwnershipTransferred"]["newOwner"] == stranger.address

    # test transfer back to the original owner

    tx = insurance_fund.transferOwnership(owner, {"from": stranger})

    assert insurance_fund.owner() == owner.address, "stranger should now be owner"
    assert "OwnershipTransferred" in tx.events
    assert tx.events["OwnershipTransferred"]["previousOwner"] == stranger.address
    assert tx.events["OwnershipTransferred"]["newOwner"] == owner.address


def test_transfer_ownership_to_zero_address(insurance_fund, owner):
    with brownie.reverts("Ownable: new owner is the zero address"):
        insurance_fund.transferOwnership(brownie.ZERO_ADDRESS, {"from": owner})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"


def test_transfer_ownership_as_stranger(insurance_fund, owner, stranger):
    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.transferOwnership(stranger.address, {"from": stranger})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"


def test_transfer_ownership_to_myself(insurance_fund, owner):
    insurance_fund.transferOwnership(owner, {"from": owner})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"
