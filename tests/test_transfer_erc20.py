def test_transfer_erc20(insurance_fund, erc20):
    (token, holder, one_coin) = erc20

    prev_holder_balance = token.balanceOf(holder.address)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address)

    token.transfer(insurance_fund.address, one_coin, {"from": holder})

    assert (
        token.balanceOf(holder.address) == prev_holder_balance - one_coin
    ), "holder should have one less coin"
    assert (
        token.balanceOf(insurance_fund.address)
        == prev_insurance_fund_balance + one_coin,
        "insurance fund should have one more coin",
    )
