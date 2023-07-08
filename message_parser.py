import base64
import io
import json
import os

from cryptography.fernet import Fernet
import discord
import requests
from nucypher.blockchain.eth.registry import InMemoryContractRegistry
from nucypher_core import ferveo

from nucypher.characters.lawful import Bob

command_maping = [
    ("vegetables", "I like vegetables"),
    ("nft", "Once 10 ETH have been contributed the album will be relased and anyone can listen to the album."),
    ("threshold", "Threshold is an..."),
    ("contributed", "25 (variable) people have contributed"),
    ("website", "http://www.justinholmes.com/music.html"),
    ("art", "http://www.justinholmes.com/music.html"),
    ("justin", "http://www.justinholmes.com/talks.html"),
    ("decentralized",
     "The album.release is decentralized -- once the contract is enacted no one has control over when and how the album is released."),
    ("not enough", "Until 10 ETH have been contributed, the album will remain locked."),
    ("verify", "All transactions are stamped on the blockchain. Click this 'link' to view your transaction."),
    ("multiple", "Yes, everyone is welcome to contribute as many times as they like."),
    ("number", "NFT numbers will be allocated in order of the largest contribution to the smalled."),
    ("minimum",
     "There are two ways to think about contributions. Any contribution is welcome -- but ... have to be more than .1 ETH"),
    ("usd", "USD is welcomed as a contribution."),
    ("after",
     "Yes. Contributions to the artist are welomed after the album has been released. These contributions will not yeald an NFT and they will not be recorded on the album.release block chain."),
    ("3 ETH", "Once 3 ETH have been contribued, 3 songs will be release."),
    ("released", "The album is relased and open to all once 10 ETH have been contributed."),
]

bob = Bob(domain="lynx", eth_provider_uri="Nowhere")

async def decrypt_attached_tmk(message):

    if message.attachments:
        url = message.attachments[0].url
        tmk_filename = message.attachments[0].filename
        await message.reply(f"OK!  I'll try to see if {tmk_filename} can be decrypted using Threshold Network.")
        attachment_response = requests.get(url)

        try:
            json_str_repr_of_tmk = str(attachment_response.content, encoding="utf-8")
            tmk_dict = json.loads(json_str_repr_of_tmk)
        except:
            await message.reply("wrong file type or something")
            return
        print("--------- Threshold Decryption ---------")

        ciphertext_of_sym_key = bytes.fromhex(tmk_dict['encrypted_sym_key'])
        ciphertext_to_decrypt_with_threshold = ferveo.Ciphertext.from_bytes(ciphertext_of_sym_key)

        ######### BAAAAAAHB ########

        staking_provider_uri = os.environ["STAKING_PROVIDER_URI"]
        network = "lynx"
        coordinator_provider_uri = os.environ["COORDINATOR_PROVIDER_URI"]
        coordinator_network = "mumbai"

        bob = Bob(
            eth_provider_uri=staking_provider_uri,
            domain=network,
            coordinator_provider_uri=coordinator_provider_uri,
            coordinator_network=coordinator_network,
            registry=InMemoryContractRegistry.from_latest_publication(network=network),
        )

        bob.start_learning_loop(now=True)

        #### Nonsense
        ritual = self.get_ritual_from_id(15)
        cohort = self.resolve_cohort(ritual=ritual, timeout=20)




        cleartext_from_ciphertext = bob.decrypt_using_existing_decryption_request(
            tdr,
            participant_public_keys=ritual.participant_public_keys,
            cohort=cohort,
            threshold=1,
        )

        print(bytes(cleartext).decode())


     
    for question, reply in command_maping:

     if question in message.content.lower():
        await message.reply(reply)
