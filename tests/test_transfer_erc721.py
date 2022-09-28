import pytest
import brownie

from utils.config import ERC721_TOKENS


@pytest.fixture(
    scope="function",
    params=ERC721_TOKENS,
)
def erc721(accounts, chain, request):
    (token_address, holder_address, token_id) = request.param[chain.id]
    token = brownie.interface.IERC721(token_address)
    holder = accounts.at(holder_address, True)
    return (token, holder, token_id)


def test_transfer_erc721_as_stranger(insurance_fund, erc721, stranger):
    (token, holder, tokenId) = erc721
    assert token.ownerOf(tokenId) == holder.address, "holder should own token"

    token.transferFrom(
        holder.address, insurance_fund.address, tokenId, {"from": holder}
    )

    assert (
        token.ownerOf(tokenId) == insurance_fund.address
    ), "insurance fund should receive token"

    with brownie.reverts("Ownable: caller is not the owner"):
        insurance_fund.transferERC721(
            token.address,
            holder.address,
            tokenId,
            "",
            {"from": stranger},
        )

    assert (
        token.ownerOf(tokenId) == insurance_fund.address
    ), "insurance fund should still own token"


def test_transfer_erc721_as_owner(insurance_fund, erc721, owner):
    (token, holder, tokenId) = erc721
    assert token.ownerOf(tokenId) == holder.address, "holder should own token"

    token.transferFrom(
        holder.address, insurance_fund.address, tokenId, {"from": holder}
    )

    assert (
        token.ownerOf(tokenId) == insurance_fund.address
    ), "insurance fund should receive token"

    tx = insurance_fund.transferERC721(
        token.address, holder.address, tokenId, "", {"from": owner}
    )

    assert token.ownerOf(tokenId) == holder.address, "holder should get token back"

    assert "ERC721Transferred" in tx.events
    assert tx.events["ERC721Transferred"]["_token"] == token.address
    assert tx.events["ERC721Transferred"]["_recipient"] == holder.address
    assert tx.events["ERC721Transferred"]["_tokenId"] == tokenId


def test_burn_erc721(insurance_fund, erc721, owner):
    (token, holder, tokenId) = erc721
    assert token.ownerOf(tokenId) == holder.address, "holder should own token"

    token.transferFrom(
        holder.address, insurance_fund.address, tokenId, {"from": holder}
    )

    assert (
        token.ownerOf(tokenId) == insurance_fund.address
    ), "insurance fund should receive token"

    with brownie.reverts("NO BURN"):
        insurance_fund.transferERC721(
            token.address, brownie.ZERO_ADDRESS, tokenId, "", {"from": owner}
        )

    assert (
        token.ownerOf(tokenId) == insurance_fund.address
    ), "insurance fund should still own token"
