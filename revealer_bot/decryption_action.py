import io

import discord
import requests
from nucypher.characters.lawful import Ursula
from nucypher_core import ferveo

from revealer_bot.bob_and_other_networky_things import bob
from revealer_bot.tmk import TMK, FilePlaintext, decrypt


async def decrypt_attached_tmk(message):

    if message.attachments:
        url = message.attachments[0].url
        tmk_filename = message.attachments[0].filename
        await message.reply(f"OK!  I'll try to see if {tmk_filename} can be decrypted using Threshold Network.")
        attachment_response = requests.get(url)

        try:
            tmk = TMK.from_bytes(attachment_response.content)
        except Exception:
            await message.reply("wrong file type or something")
            return

        print("--------- Threshold Decryption ---------")
        ciphertext_to_decrypt_with_threshold = ferveo.Ciphertext.from_bytes(tmk.encrypted_sym_key)

        ######### BAAAAAAHB ########

        try:
            plaintext_of_symkey = bob.threshold_decrypt(
                ritual_id=91,  # Cuz 91
                ciphertext=ciphertext_to_decrypt_with_threshold,
                conditions=tmk.conditions,
            )
        except Ursula.NotEnoughUrsulas as e:
            # Bad bad
            status = e.args[0]
            error_message = status
            if "Decryption conditions not satisfied" in status:
                error_message = "Decryption condition not satisfied"

            await message.reply(error_message)
            return

        plaintext_of_symkey = bytes(plaintext_of_symkey)
        cleartext = decrypt(ciphertext=tmk.bulk_ciphertext, plaintext_of_symkey=plaintext_of_symkey)
        payload = FilePlaintext.from_bytes(cleartext)
        filelike = io.BytesIO(payload.file_content)

        await message.reply(
            "Here's what I found.",
            file=discord.File(filelike, filename=payload.metadata["filename"]),
        )
