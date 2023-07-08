import pytest

@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]

@pytest.fixture(scope="session")
def countdownPeriod():
    return 600

@pytest.fixture(scope="session")
def threshold():
    return 1000000000000000000

@pytest.fixture(scope="session")
def receiver(accounts):
    return accounts[1]

@pytest.fixture(scope='session', autouse=True)
def contribution(project, owner, countdownPeriod, threshold, receiver):
    vowelsounds_contracts_dependency_api = project.dependencies["contribution-contracts"]
    # simply use first entry - could be from github ('main') or local ('local')
    _, vowelsounds_contracts = list(vowelsounds_contracts_dependency_api.items())[0]
    compiled = vowelsounds_contracts.compile()
    return owner.deploy(vowelsounds_contracts.Contribution, countdownPeriod, threshold, receiver)
