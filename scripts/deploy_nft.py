#!/usr/bin/python3
from ape import project
from ape.cli import get_user_selected_account


def main(account_id=None):
    deployer = get_user_selected_account()

    coordinator = project.VowelSoundsNFT.deploy(
        0x99Ca51a3534785ED619f46A79C7Ad65Fa8d85e7a,  # (Chiado AMB)
        sender=deployer,
        publish=True,
    )
    return coordinator
