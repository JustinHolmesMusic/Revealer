from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

import ape
import pytest
from web3 import Web3


def calculate_leaders(contribution_metadata) -> Dict[str, int]:
    """
    Takes three lists (from solidity arrays) and returns a dictionary of leaders.
    """
    contributors = contribution_metadata[0]
    amounts = contribution_metadata[1]
    combined = contribution_metadata[2]
    datetime = contribution_metadata[3]  # noqa

    contributors_by_address = defaultdict(list)

    for counter, contributor in enumerate(contributors):
        is_combined = combined[counter]
        amount = amounts[counter]

        if is_combined:
            if not contributors_by_address[contributor]:
                # This ought to be an impossible situaiton - how did they dcombine with a bid that didn't exist?
                contributors_by_address[contributor].append(0)
            contributors_by_address[contributor][0] += amount
        else:
            contributors_by_address[contributor].append(amount)

    return contributors_by_address


def test_properties(
    chain,
    contribution: ape.Contract,
    owner: ape.Account,
    beneficiary: ape.Account,
    threshold: int,
    countdownPeriod: int,
):
    assert owner == contribution.owner()
    assert beneficiary == contribution.beneficiary()
    assert contribution.countdownPeriod() == countdownPeriod
    assert contribution.threshold() == threshold
    assert contribution.deadline() == 0
    assert contribution.isKeySet() is False


@pytest.fixture
def commit_secret(contribution: ape.Contract, owner: ape.Account, dummy_key_ciphertext_base64, dummy_key_hash):
    contribution.commitSecret(dummy_key_hash, dummy_key_ciphertext_base64, sender=owner)


def test_set_secret(
    contribution: ape.Contract,
    owner: ape.Account,
    not_owner: ape.Account,
    dummy_key_ciphertext_base64,
    dummy_key_hash,
):
    # only owner can set secret

    assert contribution.isKeySet() == False

    with ape.reverts("Only the contract owner can call this function."):
        #     function commitSecret(bytes32 _hash, bytes memory _ciphertext) external onlyOwner {
        contribution.commitSecret(dummy_key_hash, dummy_key_ciphertext_base64, sender=not_owner)

    contribution.commitSecret(dummy_key_hash, dummy_key_ciphertext_base64, sender=owner)

    assert contribution.isKeySet() == True

    # cannot set secret twice
    with ape.reverts("Key already set."):
        contribution.commitSecret(dummy_key_hash, dummy_key_ciphertext_base64, sender=owner)


@pytest.mark.usefixtures("commit_secret")
def test_reveal_secret(
    contribution: ape.Contract,
    owner: ape.Account,
    not_owner: ape.Account,
    dummy_key_base64,
    dummy_key_hash,
    threshold: int,
):
    with ape.reverts("Material has not been set for a release."):
        contribution.revealSecret(dummy_key_base64, sender=owner)

    # send enough ether to the contract to meet the threshold
    contribution.contribute(sender=not_owner, value=threshold + 1)

    contribution.revealSecret(dummy_key_base64, sender=owner)
    assert contribution.keyPlaintext() == dummy_key_base64


@pytest.mark.usefixtures("commit_secret")
def test_not_being_able_to_contribute_after_deadline(
    chain: ape.chain,
    contribution: ape.Contract,
    owner: ape.Account,
    not_owner: ape.Account,
    countdownPeriod: int,
):

    # contribution before deadline should work
    # transfer 1 wei from not_owner to contribution contract
    #  function contribute() external payable {
    contribution.contribute(sender=not_owner, value=Web3.to_wei(1, "ether"))

    expected_time_remaining = chain.pending_timestamp + contribution.initialWindow()

    # 2 seconds have passed
    negative_two_seconds = contribution.deadline() - expected_time_remaining
    assert negative_two_seconds == -2

    # Go forward by a countdown period  TODO: What if countdownPeriod is longer than initial window?
    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)
    chain.mine()

    time_remaining_if_we_hadnt_advanced = contribution.initialWindow()

    # ...but actually we need to adjust for two mined bloocks.
    time_remaining_if_we_hadnt_advanced -= 4

    # ...but we expect the actual time remaining to be one countdownPeriod less, because we advanced..
    actual_time_remaining = contribution.deadline() - chain.pending_timestamp
    assert time_remaining_if_we_hadnt_advanced - actual_time_remaining == countdownPeriod

    # ...and having advanced one countdownPeriod, plus 4 seconds for two blocks, we can still contribute.
    contribution.contribute(sender=not_owner, value=Web3.to_wei(1, "ether"))

    # Now we advance to within one countdownPeriod of the deadline.
    chain.provider.set_timestamp(contribution.deadline() - countdownPeriod + 300)

    # Indeed, we're within one countdownPeriod of the deadline.
    assert contribution.deadline() - chain.pending_timestamp < countdownPeriod

    # The ClockReset event has never been emitted
    clock_reset_query = contribution.ClockReset.query("*")
    len(clock_reset_query) == 0

    # We can still contribute - this causes the deadline to advance.
    contribution.contribute(sender=not_owner, value=Web3.to_wei(1, "ether"))

    # Now, the deadline has moved to exactly one countdownPeriod ahead of the current time.
    assert contribution.deadline() - chain.blocks.head.timestamp == countdownPeriod

    # ...and the ClockReset event was emitted.
    clock_reset_query = contribution.ClockReset.query("*")
    len(clock_reset_query) == 1

    # We'll advance one more time, more than a whole countdownPeriod..
    chain.provider.set_timestamp(chain.blocks.head.timestamp + countdownPeriod + 10)

    # Now, the deadline has passed.
    assert contribution.deadline() - chain.blocks.head.timestamp < 0

    # And thus, we can't contribute.
    with ape.reverts("Cannot contribute after the deadline"):
        contribution.contribute(sender=not_owner, value=Web3.to_wei(1, "ether"))


@pytest.mark.usefixtures("commit_secret")
def test_album_release(
    contribution: ape.Contract,
    owner: ape.Account,
    not_owner: ape.Account,
    beneficiary: ape.Account,
    threshold: int,
):
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
def test_contribute_mapping(contribution: ape.Contract, owner: ape.Account, not_owner: ape.Account):
    contribution.contribute(sender=not_owner, value=Web3.to_wei(1, "ether"))
    assert contribution.balance == Web3.to_wei(1, "ether")
    assert contribution.totalContributedByAddress(not_owner) == Web3.to_wei(1, "ether")

    contribution.contribute(sender=not_owner, value=Web3.to_wei(2, "ether"))
    assert contribution.balance == Web3.to_wei(3, "ether")
    assert contribution.totalContributedByAddress(not_owner) == Web3.to_wei(3, "ether")
    #
    # assert contribution.getContributionsByAddress(not_owner) == [Web3.to_wei(1, "ether"), Web3.to_wei(2, "ether")]
    # contribution.contributeAndCombine(sender=not_owner, value=Web3.to_wei(4, "ether"))
    # assert contribution.getContributionsByAddress(not_owner) == [Web3.to_wei(5, "ether"), Web3.to_wei(2, "ether")]
    # assert contribution.totalContributedByAddress(owner) == 0
    #
    # contribution.contribute(sender=owner, value=Web3.to_wei(4, "ether"))
    # assert contribution.balance == Web3.to_wei(11, "ether")
    # assert contribution.totalContributedByAddress(owner) == Web3.to_wei(4, "ether")
    #
    # assert contribution.totalContributedByAddress(beneficiary) == 0


@pytest.mark.usefixtures("commit_secret")
def test_withdraw_funds_after_deadline_threshold_not_met(
    chain: ape.chain,
    contribution: ape.Contract,
    owner: ape.Account,
    not_owner: ape.Account,
    beneficiary: ape.Account,
    threshold: int,
    countdownPeriod: int,
):
    beneficiary_balance_before = beneficiary.balance

    contribution_amount = threshold // 4
    contribution.contribute(sender=not_owner, value=contribution_amount)
    contribution.contribute(sender=owner, value=contribution_amount)

    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)

    # Didn't reach threshold
    assert contribution.materialReleaseConditionMet() is False

    # only beneficiary can withdraw
    with ape.reverts("Only the beneficiary can call this function."):
        contribution.withdraw(sender=not_owner)

    with ape.reverts("Only the beneficiary can call this function."):
        contribution.withdraw(sender=owner)

    assert contribution.balance == contribution_amount * 2

    with ape.reverts("Material has not been set for a release."):
        contribution.withdraw(sender=beneficiary)

    contribution.contribute(sender=owner, value=Web3.to_wei(1, "ether"))
    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)
    contribution.withdraw(sender=beneficiary)

    # this doesn't work because of the gas cost
    # assert beneficiary.balance == beneficiary_balance_before + contribution_amount * 2

    assert beneficiary.balance >= beneficiary_balance_before + contribution_amount * 2 - threshold // 10
    assert contribution.balance == 0


@pytest.mark.usefixtures("commit_secret")
def test_withdraw_funds_after_deadline_fulfilled_threshold(
    chain: ape.chain,
    contribution: ape.Contract,
    owner: ape.Account,
    not_owner: ape.Account,
    beneficiary: ape.Account,
    threshold: int,
    countdownPeriod: int,
):
    beneficiary_balance_before = beneficiary.balance

    contribution_amount = int(threshold * 2 / 3)
    contribution.contribute(sender=not_owner, value=contribution_amount)
    contribution.contribute(sender=owner, value=contribution_amount)

    chain.provider.set_timestamp(chain.pending_timestamp + countdownPeriod + 1)

    # Reached threshold
    assert contribution.materialReleaseConditionMet() == True
    assert contribution.balance == contribution_amount * 2

    contribution.withdraw(sender=beneficiary)

    # this doesn't work because of the gas cost
    # assert beneficiary.balance == beneficiary_balance_before + contribution_amount * 2

    assert beneficiary.balance >= beneficiary_balance_before + contribution_amount * 2 - threshold // 10
    assert contribution.balance == 0


@pytest.mark.usefixtures("commit_secret")
def test_contributors_collation(
    chain: ape.chain,
    contribution: ape.Contract,
    accounts: List[ape.Account],
    beneficiary: ape.Account,
    threshold: int,
    countdownPeriod: int,
):
    # beneficiary_balance_before = beneficiary.balance

    half_an_ether = Web3.to_wei(0.5, "ether")
    two_ether = Web3.to_wei(2, unit="ether")
    two_and_a_half_ether = Web3.to_wei(2.5, unit="ether")

    first_contributor = accounts[2]
    second_contributor = accounts[3]

    # Two contributors; let's see them in the contributors collation.

    contribution.contribute(sender=first_contributor, value=half_an_ether)
    contribution.contribute(sender=second_contributor, value=two_ether)

    contribution_metadata = contribution.getAllContributions()
    leaders_at_first = calculate_leaders(contribution_metadata)

    assert sum(leaders_at_first[first_contributor.address]) == half_an_ether
    assert sum(leaders_at_first[second_contributor.address]) == two_ether

    # Now contributor one contributes again, to take the lead.
    contribution.contributeAndCombine(sender=first_contributor, value=two_ether)

    contribution_metadata_part_two = contribution.getAllContributions()

    contributions_by_address_after_first_contributor_took_the_lead = calculate_leaders(contribution_metadata_part_two)

    assert contributions_by_address_after_first_contributor_took_the_lead[first_contributor.address][0] == two_and_a_half_ether

    assert contributions_by_address_after_first_contributor_took_the_lead[second_contributor.address][0] == two_ether
