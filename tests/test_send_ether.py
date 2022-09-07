import brownie


def test_send_ether(insurance_fund, anyone, ether_amount):
    prev_insurance_fund_balance = insurance_fund.balance()
    prev_anyone_balance = anyone.balance()

    revert_string = "" if ether_amount == 0 else "Cannot send ether to nonpayable function"
    with brownie.reverts(revert_string):
        anyone.transfer(insurance_fund.address, ether_amount)

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance
    ), "insurance fund balance should remain unchanged"
    assert (
        anyone.balance() == prev_anyone_balance
    ), "sender balance should remain unchanged"


def test_send_ether_via_selfdestruct(insurance_fund, destructable, anyone, ether_amount):
    prev_insurance_fund_balance = insurance_fund.balance()
    prev_anyone_balance = anyone.balance()

    tx = destructable.die(insurance_fund.address, {"from": anyone, "value": ether_amount})
    tx_fee = tx.gas_used * tx.gas_price

    assert insurance_fund.balance() == prev_insurance_fund_balance + ether_amount, "insurance fund should receive ether"
    assert anyone.balance() == prev_anyone_balance - ether_amount - tx_fee, "sender balance should be less by amount of ether sent plus gas fees"


