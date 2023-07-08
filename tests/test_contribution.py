from __future__ import annotations
import ape
import pytest


def test_properties(chain, contribution: ape.Contract, owner: ape.Account, receiver: ape.Account, threshold: int, countdownPeriod: int):
    assert owner == contribution.owner()
    assert receiver == contribution.beneficiary()
    assert contribution.countdownPeriod() == countdownPeriod
    assert contribution.threshold() == threshold
    assert contribution.deadline() > chain.pending_timestamp


def test_not_being_able_to_contribute_after_deadline(chain: ape.chain, contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, countdownPeriod: int):

    # contribution before deadline should work
    # transfer 1 wei from not_owner to contribution contract
    #  function contribute() external payable {
    contribution.contribute(sender=not_owner, value=1)

    # contribution after deadline should fail
    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)


    with ape.reverts("Cannot contribute after the deadline"):
        contribution.contribute(sender=not_owner, value=1)


def test_album_release(contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, receiver: ape.Account, threshold: int):

    # get balance of the contribution contract
    assert contribution.balance == 0
    assert contribution.isReleased() == False

    contribution.contribute(sender=not_owner, value=threshold // 2)
    assert contribution.balance == threshold // 2
    assert contribution.isReleased() == False


    contribution.contribute(sender=not_owner, value=threshold // 2 + 1)
    assert contribution.balance >= threshold
    assert contribution.isReleased() == True


def test_cannot_withdraw_funds_before_deadline(contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, receiver: ape.Account, threshold: int):
    contribution.contribute(sender=not_owner, value=threshold // 2)
    with ape.reverts("Cannot withdraw funds before deadline"):
        contribution.withdraw(sender=receiver)


def test_withdraw_funds_after_deadline(chain: ape.chain, contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, receiver: ape.Account, threshold: int, countdownPeriod: int):
    receiver_balance_before = receiver.balance

    contribution_amount = threshold // 4
    contribution.contribute(sender=not_owner, value=contribution_amount)
    contribution.contribute(sender=owner, value=contribution_amount)

    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)

    # Didn't reach threshold
    assert contribution.isReleased() == False 

    # only receiver can withdraw
    with ape.reverts("Only the beneficiary can withdraw funds"):
        contribution.withdraw(sender=not_owner)
    
    with ape.reverts("Only the beneficiary can withdraw funds"):
        contribution.withdraw(sender=owner)
    
    assert contribution.balance == contribution_amount * 2
    
    contribution.withdraw(sender=receiver)

    # this doesn't work because of the gas cost
    # assert receiver.balance == receiver_balance_before + contribution_amount * 2

    assert receiver.balance >= receiver_balance_before + contribution_amount * 2 - threshold // 10

    assert contribution.balance == 0