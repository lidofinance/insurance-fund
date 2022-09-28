import brownie
import pytest
import eth_utils


@pytest.fixture(
    scope="session",
    params=[0, 1, eth_utils.to_wei(1, "gwei"), eth_utils.to_wei(1, "ether")],
)
def ether_amount(request):
    return request.param


@pytest.fixture(scope="function")
def destructable(stranger):
    return brownie.Destructable.deploy({"from": stranger})


@pytest.fixture(scope="function")
def ether_rejector(stranger):
    return brownie.EtherRejector.deploy({"from": stranger})


def test_receive_ether(insurance_fund, anyone, ether_amount):
    prev_insurance_fund_balance = insurance_fund.balance()
    prev_anyone_balance = anyone.balance()

    revert_string = (
        "" if ether_amount == 0 else "Cannot send ether to nonpayable function"
    )
    with brownie.reverts(revert_string):
        anyone.transfer(insurance_fund.address, ether_amount)

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance
    ), "insurance fund balance should remain unchanged"
    assert (
        anyone.balance() == prev_anyone_balance
    ), "sender balance should remain unchanged"


def test_receive_ether_via_selfdestruct(
    insurance_fund, destructable, anyone, ether_amount
):
    prev_insurance_fund_balance = insurance_fund.balance()
    prev_anyone_balance = anyone.balance()

    tx = destructable.die(
        insurance_fund.address, {"from": anyone, "value": ether_amount}
    )
    tx_fee = tx.gas_used * tx.gas_price

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance + ether_amount
    ), "insurance fund should receive ether"
    assert (
        anyone.balance() == prev_anyone_balance - ether_amount - tx_fee
    ), "sender balance should be less by amount of ether sent plus gas fees"


def test_transfer_ether_as_stranger(
    insurance_fund, destructable, stranger, ether_amount
):
    prev_insurance_fund_balance = insurance_fund.balance()
    destructable.die(insurance_fund.address, {"from": stranger, "value": ether_amount})

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance + ether_amount
    ), "insurance fund should receive ether"

    prev_insurance_fund_balance = insurance_fund.balance()

    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.transferEther(stranger.address, ether_amount, {"from": stranger})

    assert insurance_fund.balance() == prev_insurance_fund_balance


def test_transfer_ether_as_owner(
    insurance_fund, destructable, owner, stranger, ether_amount
):
    prev_insurance_fund_balance = insurance_fund.balance()
    destructable.die(insurance_fund.address, {"from": owner, "value": ether_amount})

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance + ether_amount
    ), "insurance fund should receive ether"

    prev_insurance_fund_balance = insurance_fund.balance()
    prev_stranger_balance = stranger.balance()
    tx = insurance_fund.transferEther(stranger.address, ether_amount, {"from": owner})

    assert (
        stranger.balance() == prev_stranger_balance + ether_amount
    ), "stranger should receive ether"
    assert (
        insurance_fund.balance() == prev_insurance_fund_balance - ether_amount
    ), "ether should be deducted from insurance fund"

    assert "EtherTransferred" in tx.events
    assert tx.events["EtherTransferred"]["_recipient"] == stranger.address
    assert tx.events["EtherTransferred"]["_amount"] == ether_amount


def test_burn_ether(insurance_fund, destructable, owner, ether_amount):
    prev_insurance_fund_balance = insurance_fund.balance()
    destructable.die(insurance_fund.address, {"from": owner, "value": ether_amount})

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance + ether_amount
    ), "insurance fund should receive ether"

    prev_insurance_fund_balance = insurance_fund.balance()

    with brownie.reverts("NO BURN"):
        insurance_fund.transferEther(
            brownie.ZERO_ADDRESS, ether_amount, {"from": owner}
        )

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance
    ), "insurance fund balance should stay unchanged"


def test_transfer_fail(
    insurance_fund, destructable, ether_rejector, owner, ether_amount
):
    prev_insurance_fund_balance = insurance_fund.balance()
    destructable.die(insurance_fund.address, {"from": owner, "value": ether_amount})

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance + ether_amount
    ), "insurance fund should receive ether"

    prev_rejector_balance = ether_rejector.balance()
    prev_insurance_fund_balance = insurance_fund.balance()

    with brownie.reverts("TRANSFER FAILED"):
        insurance_fund.transferEther(
            ether_rejector.address, ether_amount, {"from": owner}
        )

    assert (
        ether_rejector.balance() == prev_rejector_balance
    ), "ether rejector balance should stay unchanged"
    assert (
        insurance_fund.balance() == prev_insurance_fund_balance
    ), "insurance fund balance should stay unchanged"


def test_transfer_insufficient_balance(
    insurance_fund, destructable, owner, stranger, ether_amount
):
    prev_insurance_fund_balance = insurance_fund.balance()
    destructable.die(insurance_fund.address, {"from": owner, "value": ether_amount})

    assert (
        insurance_fund.balance() == prev_insurance_fund_balance + ether_amount
    ), "insurance fund should receive ether"

    prev_strange_balance = stranger.balance()
    prev_insurance_fund_balance = insurance_fund.balance()
    transfer_amount = prev_insurance_fund_balance + 1

    with brownie.reverts("TRANSFER FAILED"):
        insurance_fund.transferEther(stranger.address, transfer_amount, {"from": owner})

    assert (
        stranger.balance() == prev_strange_balance
    ), "stranger balance should stay unchanged"
    assert (
        insurance_fund.balance() == prev_insurance_fund_balance
    ), "insurance fund balance should stay unchanged"
