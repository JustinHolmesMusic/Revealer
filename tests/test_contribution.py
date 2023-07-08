from __future__ import annotations
import base64   
import ape
import pytest


def test_properties(chain, contribution: ape.Contract, owner: ape.Account, receiver: ape.Account, threshold: int, countdownPeriod: int):
    assert owner == contribution.owner()
    assert receiver == contribution.beneficiary()
    assert contribution.countdownPeriod() == countdownPeriod
    assert contribution.threshold() == threshold
    assert contribution.deadline() > chain.pending_timestamp
    assert contribution.isKeySet() == False

@pytest.fixture
def commit_secret(contribution: ape.Contract, owner: ape.Account, dummy_key_ciphertext_base64, dummy_key_hash):
    contribution.commitSecret(dummy_key_hash, dummy_key_ciphertext_base64, sender=owner)

def test_set_secret(contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, dummy_key_ciphertext_base64, dummy_key_hash):
    # only owner can set secret

    assert contribution.isKeySet() == False

    with ape.reverts("Only the contract owner can call this function."):
        #     function commitSecret(bytes32 _hash, bytes memory _ciphertext) external onlyOwner {
        contribution.commitSecret(dummy_key_hash, dummy_key_ciphertext_base64, sender=not_owner)
    
    contribution.commitSecret(dummy_key_hash, dummy_key_ciphertext_base64, sender=owner)

    assert contribution.isKeySet() == True


@pytest.mark.usefixtures("commit_secret")
def test_reveal_secret(contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, dummy_key_base64, dummy_key_hash, threshold: int):

    with ape.reverts("Material has not been set for a release."):
        contribution.revealSecret(dummy_key_base64, sender=owner)
    
    # send enough ether to the contract to meet the threshold
    contribution.contribute(sender=not_owner, value=threshold + 1)

    contribution.revealSecret(dummy_key_base64, sender=owner)
    assert contribution.keyPlaintext() == dummy_key_base64


@pytest.mark.usefixtures("commit_secret")
def test_not_being_able_to_contribute_after_deadline(chain: ape.chain, contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, countdownPeriod: int):

    # contribution before deadline should work
    # transfer 1 wei from not_owner to contribution contract
    #  function contribute() external payable {
    contribution.contribute(sender=not_owner, value=1)

    # contribution after deadline should fail
    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)


    with ape.reverts("Cannot contribute after the deadline"):
        contribution.contribute(sender=not_owner, value=1)


@pytest.mark.usefixtures("commit_secret")
def test_album_release(contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, receiver: ape.Account, threshold: int):

    # get balance of the contribution contract
    assert contribution.balance == 0
    assert contribution.materialReleaseConditionMet() == False

    contribution.contribute(sender=not_owner, value=threshold // 2)
    assert contribution.balance == threshold // 2
    assert contribution.materialReleaseConditionMet() == False


    contribution.contribute(sender=not_owner, value=threshold // 2 + 1)
    assert contribution.balance >= threshold
    assert contribution.materialReleaseConditionMet() == True


@pytest.mark.usefixtures("commit_secret")
def test_cannot_withdraw_funds_before_deadline(contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, receiver: ape.Account, threshold: int):
    contribution.contribute(sender=not_owner, value=threshold // 2)
    with ape.reverts("Cannot withdraw funds before deadline"):
        contribution.withdraw(sender=receiver)


@pytest.mark.usefixtures("commit_secret")
def test_withdraw_funds_after_deadline(chain: ape.chain, contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account, receiver: ape.Account, threshold: int, countdownPeriod: int):
    receiver_balance_before = receiver.balance

    contribution_amount = threshold // 4
    contribution.contribute(sender=not_owner, value=contribution_amount)
    contribution.contribute(sender=owner, value=contribution_amount)

    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)

    # Didn't reach threshold
    assert contribution.materialReleaseConditionMet() == False 

    # only receiver can withdraw
    with ape.reverts("Only the beneficiary can call this function."):
        contribution.withdraw(sender=not_owner)
    
    with ape.reverts("Only the beneficiary can call this function."):
        contribution.withdraw(sender=owner)
    
    assert contribution.balance == contribution_amount * 2
    
    contribution.withdraw(sender=receiver)

    # this doesn't work because of the gas cost
    # assert receiver.balance == receiver_balance_before + contribution_amount * 2

    assert receiver.balance >= receiver_balance_before + contribution_amount * 2 - threshold // 10

    assert contribution.balance == 0


