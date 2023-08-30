from collections import defaultdict
from typing import Dict


def calculate_leaders(contribution_metadata) -> Dict[str, int]:
    """
    Takes three lists (from solidity arrays) and returns a dictionary of leaders.
    """
    contributors = contribution_metadata[0]
    amounts = contribution_metadata[1]
    combined = contribution_metadata[2]
    datetime = contribution_metadata[3]

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
