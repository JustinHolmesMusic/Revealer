#!/usr/bin/python3
from ape import project
from ape.cli import get_user_selected_account


def main(account_id=None):
    deployer = get_user_selected_account()

    coordinator = project.VowelSoundsNFT.deploy(
        0x99CA51A3534785ED619F46A79C7AD65FA8D85E7A,  # (Chiado AMB)
        sender=deployer,
        publish=True,
    )
    return coordinator
