import pytest
import brownie
import eth_utils

from utils.config import ERC20_TOKENS, ERC721_TOKENS, ERC1155_TOKENS


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="session")
def deployer(accounts):
    return accounts.add()


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def stranger(accounts):
    return accounts[1]


@pytest.fixture(scope="session", params=["owner", "stranger"])
def anyone(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="function")
def insurance_fund(deployer, owner):
    return brownie.InsuranceFund.deploy(owner.address, {"from": deployer})


@pytest.fixture(scope="function")
def destructable(stranger):
    return brownie.Destructable.deploy({"from": stranger})


@pytest.fixture(scope="function")
def ether_rejector(stranger):
    return brownie.EtherRejector.deploy({"from": stranger})


@pytest.fixture(
    scope="session",
    params=[0, 1, eth_utils.to_wei(1, "gwei"), eth_utils.to_wei(1, "ether")],
)
def ether_amount(request):
    return request.param


@pytest.fixture(
    scope="function",
    params=ERC20_TOKENS,
)
def erc20(accounts, chain, request):
    (token_address, holder_address) = request.param[chain.id]
    token = brownie.interface.ERC20(token_address)
    holder = accounts.at(holder_address, True)
    one_coin = 10 ** token.decimals()
    return (token, holder, one_coin)


@pytest.fixture(
    scope="function",
    params=ERC721_TOKENS,
)
def erc721(accounts, chain, request):
    (token_address, holder_address, token_id) = request.param[chain.id]
    token = brownie.interface.IERC721(token_address)
    holder = accounts.at(holder_address, True)
    return (token, holder, token_id)


@pytest.fixture(
    scope="function",
    params=ERC1155_TOKENS,
)
def erc1155(accounts, chain, request):
    (token_address, holder_address, token_id) = request.param[chain.id]
    token = brownie.interface.IERC1155(token_address)
    holder = accounts.at(holder_address, True)
    return (token, holder, token_id)


@pytest.fixture(
    scope="function",
)
def unsafe_erc1155(stranger):
    token = brownie.UnsafeMockERC1155.deploy({"from": stranger})
    tokenId = 0
    return (token, stranger, tokenId)
