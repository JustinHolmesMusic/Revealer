#!/usr/bin/python3
from ape import project
from ape.cli import get_user_selected_account

def main(account_id=None):
    deployer = get_user_selected_account()

    coordinator = project.Contribution.deploy(
        1687669457,  # June 25th
        sender=deployer,
        publish=True,
    )
    return coordinator
