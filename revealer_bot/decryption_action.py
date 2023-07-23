import base64
import io
import json
from typing import cast

import discord
import requests
from cryptography.fernet import Fernet
from nucypher_core import ferveo

from revealer_bot.bob_and_other_networky_things import bob
from revealer_bot.types import TMK


async def decrypt_attached_tmk(message):

    if message.attachments:
        url = message.attachments[0].url
        tmk_filename = message.attachments[0].filename
        await message.reply(
            f"OK!  I'll try to see if {tmk_filename} can be decrypted using Threshold Network."
        )
        attachment_response = requests.get(url)

        try:
            json_str_repr_of_tmk = str(attachment_response.content, encoding="utf-8")
            tmk_dict = cast(TMK, json.loads(json_str_repr_of_tmk))
        except json.JSONDecodeError:
            await message.reply("wrong file type or something")
            return
        print("--------- Threshold Decryption ---------")

        ciphertext_of_sym_key = bytes.fromhex(tmk_dict["encrypted_sym_key"])
        ciphertext_to_decrypt_with_threshold = ferveo.Ciphertext.from_bytes(ciphertext_of_sym_key)

        ######### BAAAAAAHB ########

        plaintext_of_symkey = bob.threshold_decrypt(
            ritual_id=15,  # Cuz 15
            ciphertext=ciphertext_to_decrypt_with_threshold,
            conditions=tmk_dict["conditions"],
        )

        f = Fernet(bytes(plaintext_of_symkey))
        bulk_ciphertext = base64.b64decode(tmk_dict["bulk_ciphertext"])
        hopefully_tony = f.decrypt(bulk_ciphertext)

        filelike = io.BytesIO(hopefully_tony)
        await message.reply(
            "Here's what I found.", file=discord.File(filelike, filename=tmk_dict["filename"])
        )
