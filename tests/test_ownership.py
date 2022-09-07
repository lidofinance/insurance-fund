import brownie


def test_initial_owner(insurance_fund, owner):
    assert insurance_fund.owner() == owner.address, "owner address should match"


def test_renounce_ownership_as_owner(insurance_fund, owner):
    with brownie.reverts("Renouncing ownership disabled!"):
        insurance_fund.renounceOwnership({"from": owner})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"

    
def test_renounce_ownership_as_stranger(insurance_fund, stranger, owner):
    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.renounceOwnership({"from": stranger})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"


def test_change_owner_as_owner(insurance_fund, owner, stranger):
    insurance_fund.changeOwner(stranger.address, {"from": owner})

    assert insurance_fund.owner() == stranger.address, "stranger should now be owner"


def test_change_owner_to_zero_address(insurance_fund, owner):
    with brownie.reverts("Ownable: new owner is the zero address"):
        insurance_fund.changeOwner(brownie.ZERO_ADDRESS, {"from": owner})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"


def test_change_owner_as_stranger(insurance_fund, owner, stranger):
    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.renounceOwnership({"from": stranger})

    assert insurance_fund.owner() == owner.address, "owner should remain unchanged"