import brownie
import pytest


@pytest.mark.parametrize("amount", [1, 2**256 - 1])
def test_receive_erc1155_safely(insurance_fund, erc1155, amount):
    (token, holder, token_id) = erc1155

    assert (
        token.balanceOf(holder.address, token_id) >= amount
    ), "holder should own tokens"

    prev_holder_balance = token.balanceOf(holder.address, token_id)

    with brownie.reverts(""):
        token.safeTransferFrom(
            holder.address,
            insurance_fund.address,
            token_id,
            amount,
            "",
            {"from": holder},
        )

    assert (
        token.balanceOf(holder.address, token_id) == prev_holder_balance
    ), "holder should still own tokens"


@pytest.mark.parametrize("amount", [1, 2**256 - 1])
def test_receive_unsafe_erc1155(insurance_fund, unsafe_erc1155, amount):
    (token, holder, token_id) = unsafe_erc1155

    assert (
        token.balanceOf(holder.address, token_id) >= amount
    ), "holder should own tokens"

    prev_holder_balance = token.balanceOf(holder.address, token_id)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address, token_id)

    token.safeTransferFrom(
        holder.address,
        insurance_fund.address,
        token_id,
        amount,
        "",
        {"from": holder},
    )

    assert (
        token.balanceOf(holder.address, token_id) == prev_holder_balance - amount
    ), "tokens should be deducted from holder"
    assert (
        token.balanceOf(insurance_fund.address, token_id)
        == prev_insurance_fund_balance + amount
    ), "insurance fund should receive tokens"


@pytest.mark.parametrize("amount", [1, 2**256 - 1])
def test_transfer_unsafe_erc1155_as_stranger(
    insurance_fund, unsafe_erc1155, stranger, amount
):
    (token, holder, token_id) = unsafe_erc1155
    assert (
        token.balanceOf(holder.address, token_id) >= amount
    ), "holder should own tokens"

    prev_holder_balance = token.balanceOf(holder.address, token_id)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address, token_id)

    token.safeTransferFrom(
        holder.address,
        insurance_fund.address,
        token_id,
        amount,
        "",
        {"from": holder},
    )

    assert (
        token.balanceOf(holder.address, token_id) == prev_holder_balance - amount
    ), "tokens should be deducted from holder"
    assert (
        token.balanceOf(insurance_fund.address, token_id)
        == prev_insurance_fund_balance + amount
    ), "insurance fund should receive tokens"

    prev_stranger_balance = token.balanceOf(stranger.address, token_id)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address, token_id)

    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.transferERC1155(
            token.address, stranger.address, token_id, amount, "", {"from": stranger}
        )

    assert (
        token.balanceOf(stranger.address, token_id) == prev_stranger_balance
    ), "stranger balance should stay unchanged"
    assert (
        token.balanceOf(insurance_fund.address, token_id) == prev_insurance_fund_balance
    ), "insurance fund balance should stay unchanged"


@pytest.mark.parametrize("amount", [1, 2**256 - 1])
def test_transfer_unsafe_erc1155_as_owner(
    insurance_fund, unsafe_erc1155, owner, stranger, amount
):
    (token, holder, token_id) = unsafe_erc1155
    assert (
        token.balanceOf(holder.address, token_id) >= amount
    ), "holder should own tokens"

    prev_holder_balance = token.balanceOf(holder.address, token_id)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address, token_id)

    token.safeTransferFrom(
        holder.address,
        insurance_fund.address,
        token_id,
        amount,
        "",
        {"from": holder},
    )

    assert (
        token.balanceOf(holder.address, token_id) == prev_holder_balance - amount
    ), "tokens should be deducted from holder"
    assert (
        token.balanceOf(insurance_fund.address, token_id)
        == prev_insurance_fund_balance + amount
    ), "insurance fund should receive tokens"

    prev_stranger_balance = token.balanceOf(stranger.address, token_id)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address, token_id)

    data = "hello"
    data_hex = data.encode("utf-8").hex()

    tx = insurance_fund.transferERC1155(
        token.address, stranger.address, token_id, amount, data_hex, {"from": owner}
    )

    assert (
        token.balanceOf(stranger.address, token_id) == prev_stranger_balance + amount
    ), "stranger should receive tokens"
    assert (
        token.balanceOf(insurance_fund.address, token_id)
        == prev_insurance_fund_balance - amount
    ), "tokens should be deducted from insurance fund"

    assert "ERC1155Transferred" in tx.events
    assert tx.events["ERC1155Transferred"]["_token"] == token.address
    assert tx.events["ERC1155Transferred"]["_recipient"] == stranger.address
    assert tx.events["ERC1155Transferred"]["_tokenId"] == token_id
    assert tx.events["ERC1155Transferred"]["_amount"] == amount
    assert tx.events["ERC1155Transferred"]["_data"] == "0x" + data_hex


@pytest.mark.parametrize("amount", [1, 2**256 - 1])
def test_burn_unsafe_erc1155(insurance_fund, unsafe_erc1155, owner, amount):
    (token, holder, token_id) = unsafe_erc1155
    assert (
        token.balanceOf(holder.address, token_id) >= amount
    ), "holder should own tokens"

    prev_holder_balance = token.balanceOf(holder.address, token_id)
    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address, token_id)

    token.safeTransferFrom(
        holder.address,
        insurance_fund.address,
        token_id,
        amount,
        "",
        {"from": holder},
    )

    assert (
        token.balanceOf(holder.address, token_id) == prev_holder_balance - amount
    ), "tokens should be deducted from holder"
    assert (
        token.balanceOf(insurance_fund.address, token_id)
        == prev_insurance_fund_balance + amount
    ), "insurance fund should receive tokens"

    prev_insurance_fund_balance = token.balanceOf(insurance_fund.address, token_id)

    data = "hello"
    data_hex = data.encode("utf-8").hex()

    with brownie.reverts("NO BURN"):
        insurance_fund.transferERC1155(
            token.address,
            brownie.ZERO_ADDRESS,
            token_id,
            amount,
            data_hex,
            {"from": owner},
        )

    assert (
        token.balanceOf(insurance_fund.address, token_id) == prev_insurance_fund_balance
    ), "insurance fund balance should stay unchanged"
