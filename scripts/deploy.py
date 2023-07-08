#!/usr/bin/python3
from ape import project
from ape.cli import get_user_selected_account
from web3 import Web3


def main(account_id=None):
    deployer = get_user_selected_account()

    coordinator = project.TestnetContribution.deploy(
        120,
        Web3.to_wei(0.1, 'ether'),
        deployer,
        True,  # testnet mode
        sender=deployer,
        publish=True,
    )
    return coordinator
