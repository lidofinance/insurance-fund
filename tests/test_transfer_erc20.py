import brownie
from math import isclose

from utils.helpers import is_steth


def test_receive_erc20(insurance_fund, erc20, chain):
    (token, holder, one_coin) = erc20

    prev_holder_balance = token.balanceOf(holder.address)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address)

    token.transfer(insurance_fund.address, one_coin, {"from": holder})

    # sometimes we can lose 1 stWei during transfer
    if is_steth(chain.id, token.address):
        assert isclose(
            token.balanceOf(holder.address), prev_holder_balance - one_coin, abs_tol=1
        ), "holder should have one less coin with 1 stWei tolerance"
        assert isclose(
            token.balanceOf(insurance_fund.address),
            prev_insurance_fund_balance + one_coin,
            abs_tol=1,
        ), "insurance fund should have one more coin with 1 stWei tolerance"
    else:
        assert (
            token.balanceOf(holder.address) == prev_holder_balance - one_coin
        ), "holder should have one less coin"
        assert (
            token.balanceOf(insurance_fund.address)
            == prev_insurance_fund_balance + one_coin
        ), "insurance fund should have one more coin"


def test_transfer_erc20_as_stranger(insurance_fund, erc20, stranger):
    (token, holder, one_coin) = erc20
    token.transfer(insurance_fund.address, one_coin, {"from": holder})

    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address)
    prev_stranger_balance = token.balanceOf(stranger.address)

    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.transferERC20(
            token.address,
            stranger.address,
            prev_insurance_fund_balance,
            {"from": stranger},
        )

    assert (
        token.balanceOf(stranger.address) == prev_stranger_balance
    ), "stranger balance should stay unchanged"
    assert (
        token.balanceOf(insurance_fund.address) == prev_insurance_fund_balance
    ), "insurance fund balance should stay unchaged"


def test_transfer_erc20_as_owner(chain, insurance_fund, erc20, owner):
    (token, holder, one_coin) = erc20
    token.transfer(insurance_fund.address, one_coin, {"from": holder})

    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address)
    prev_owner_balance = token.balanceOf(owner.address)

    tx = insurance_fund.transferERC20(
        token.address, owner.address, prev_insurance_fund_balance, {"from": owner}
    )

    # sometimes we can lose 1 stWei during transfer
    if is_steth(chain.id, token.address):
        assert isclose(
            token.balanceOf(owner.address),
            prev_owner_balance + prev_insurance_fund_balance,
            abs_tol=1,
        )
        assert isclose(token.balanceOf(insurance_fund.address), 0, abs_tol=1)
    else:
        assert (
            token.balanceOf(owner.address)
            == prev_owner_balance + prev_insurance_fund_balance
        ), "owner should receive all tokens"
        assert (
            token.balanceOf(insurance_fund.address) == 0
        ), "insurance fund should have no tokens"

    assert "ERC20Transferred" in tx.events
    assert tx.events["ERC20Transferred"]["_token"] == token.address
    assert tx.events["ERC20Transferred"]["_recipient"] == owner.address
    assert tx.events["ERC20Transferred"]["_amount"] == prev_insurance_fund_balance


def test_burn_erc20(insurance_fund, erc20, owner):
    (token, holder, one_coin) = erc20
    token.transfer(insurance_fund.address, one_coin, {"from": holder})

    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address)
    prev_owner_balance = token.balanceOf(owner.address)

    with brownie.reverts("NO BURN"):
        insurance_fund.transferERC20(
            token.address, brownie.ZERO_ADDRESS, one_coin, {"from": owner}
        )

    assert (
        token.balanceOf(insurance_fund.address) == prev_insurance_fund_balance
    ), "insurance fund balance should stay unchaged"
    assert (
        token.balanceOf(owner.address) == prev_owner_balance
    ), "owner balance should stay unchaged"


def test_transfer_insufficient_erc20(insurance_fund, erc20, owner):
    (token, holder, one_coin) = erc20
    token.transfer(insurance_fund.address, one_coin, {"from": holder})

    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address)
    prev_owner_balance = token.balanceOf(owner.address)
    transfer_amount = prev_insurance_fund_balance + 10

    with brownie.reverts():
        insurance_fund.transferERC20(
            token.address, owner.address, transfer_amount, {"from": owner}
        )

    assert token.balanceOf(insurance_fund.address) == prev_insurance_fund_balance
    assert token.balanceOf(owner.address) == prev_owner_balance
