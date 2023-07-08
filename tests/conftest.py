import pytest


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def receiver(accounts):
    return accounts[1]

@pytest.fixture(scope="session")
def not_owner(accounts):
    return accounts[2]

@pytest.fixture
def countdownPeriod():
    return 600

@pytest.fixture
def threshold():
    return 1000000000000000000


@pytest.fixture
def contribution(project, receiver, owner, countdownPeriod, threshold):
    return owner.deploy(project.Contribution, countdownPeriod, threshold, receiver)