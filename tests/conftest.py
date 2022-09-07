import pytest
import brownie
import eth_utils


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


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
def insurance_fund(owner):
    return brownie.InsuranceFund.deploy(owner.address, {"from": owner})


@pytest.fixture(scope="function")
def destructable(stranger):
    return brownie.Destructable.deploy({"from": stranger})


@pytest.fixture(
    scope="session",
    params=[0, 1, eth_utils.to_wei(1, "gwei"), eth_utils.to_wei(1, "ether")],
)
def ether_amount(request):
    return request.param
