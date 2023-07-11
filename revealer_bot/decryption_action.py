import base64
import io
import json
from cryptography.fernet import Fernet
import discord
import requests
from nucypher.blockchain.eth.registry import InMemoryContractRegistry
from nucypher_core import ferveo

from nucypher.characters.lawful import Bob

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

        staking_provider_uri = "https://goerli.infura.io/v3/a11313ddcf61443898b6a47e952d255c"
        network = "lynx"
        coordinator_provider_uri = "https://polygon-mumbai.infura.io/v3/a11313ddcf61443898b6a47e952d255c"
        coordinator_network = "mumbai"

        bob = Bob(
            eth_provider_uri=staking_provider_uri,
            domain=network,
            coordinator_provider_uri=coordinator_provider_uri,
            coordinator_network=coordinator_network,
            registry=InMemoryContractRegistry.from_latest_publication(network=network),
        )

        bob.start_learning_loop(now=True)

        plaintext_of_symkey = bob.threshold_decrypt(
            ritual_id=15,  # Cuz 15
            ciphertext=ciphertext_to_decrypt_with_threshold,
            conditions=tmk_dict["conditions"],
        )

        f = Fernet(bytes(plaintext_of_symkey))
        bulk_ciphertext = base64.b64decode(tmk_dict['bulk_ciphertext'])
        hopefully_tony = f.decrypt(bulk_ciphertext)

        filelike = io.BytesIO(hopefully_tony)
        await message.reply("Here's what I found.", file=discord.File(filelike, filename=tmk_dict['filename']))
