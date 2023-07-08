
def test_dummy(contribution):
    print(contribution)

def test_properties(chain, contribution,  owner, receiver, threshold, countdownPeriod):
    assert owner == contribution.owner()
    assert receiver == contribution.beneficiary()
    assert contribution.countdownPeriod() == countdownPeriod
    assert contribution.threshold() == threshold
    assert contribution.deadline() > chain.pending_timestamp