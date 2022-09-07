import brownie

def test_transfer_ether_as_stranger(insurance_fund, destructable, stranger, ether_amount):
    prev_insurance_fund_balance = insurance_fund.balance()
    destructable.die(insurance_fund.address, {"from": stranger, "value": ether_amount})

    assert insurance_fund.balance() == prev_insurance_fund_balance + ether_amount, "insurance fund should receive ether"

    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.transferEther(stranger.address, ether_amount, {"from": stranger})


def test_transfer_ether_as_owner(insurance_fund, destructable, owner, stranger, ether_amount):
    prev_insurance_fund_balance = insurance_fund.balance()
    destructable.die(insurance_fund.address, {"from": owner, "value": ether_amount})

    assert insurance_fund.balance() == prev_insurance_fund_balance + ether_amount, "insurance fund should receive ether"

    prev_insurance_fund_balance = insurance_fund.balance()
    prev_stranger_balance = stranger.balance()
    tx = insurance_fund.transferEther(stranger.address, ether_amount, {"from": owner})

    assert stranger.balance() == prev_stranger_balance + ether_amount, "stranger should receive ether"
    assert insurance_fund.balance() == prev_insurance_fund_balance - ether_amount, "ether should be deducted from insurance fund"

    assert "EtherTransferred" in tx.events
    assert tx.events["EtherTransferred"]["_recipient"] == stranger.address
    assert tx.events["EtherTransferred"]["_amount"] == ether_amount

