import brownie
import pytest


@pytest.mark.parametrize("amount", [1, 2**256 - 1])
def test_receive_erc1155_safely(insurance_fund, erc1155, owner, amount):
    (token, holder, token_id) = erc1155

    assert token.balanceOf(holder.address, token_id) >= amount

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

    assert token.balanceOf(holder.address, token_id) == prev_holder_balance
