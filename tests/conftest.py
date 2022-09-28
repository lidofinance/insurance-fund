import pytest
import brownie


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
