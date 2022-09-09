import brownie


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
            tokenId,
            holder.address,
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
        token.address, tokenId, holder.address, {"from": owner}
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
            token.address, tokenId, brownie.ZERO_ADDRESS, {"from": owner}
        )

    assert (
        token.ownerOf(tokenId) == insurance_fund.address
    ), "insurance fund should still own token"
